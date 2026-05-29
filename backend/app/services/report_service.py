"""
报告服务模块
处理年度报告、周报相关的业务逻辑
"""

import json
import re
from collections import Counter
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException, NotFoundException
from app.models.report import AnnualReport, WeeklyBrief
from app.models.review import Review
from app.models.store import Store


async def get_annual_report(
    db: AsyncSession,
    store_id: UUID,
    year: int,
) -> AnnualReport:
    """
    获取年度报告

    Args:
        db: 数据库会话
        store_id: 门店ID
        year: 年份

    Returns:
        AnnualReport: 年度报告对象

    Raises:
        NotFoundException: 报告不存在
    """
    stmt = select(AnnualReport).where(
        and_(
            AnnualReport.store_id == store_id,
            AnnualReport.year == year,
        )
    ).order_by(AnnualReport.generated_at.desc())
    result = await db.execute(stmt)
    report = result.scalars().first()

    if not report:
        raise NotFoundException(f"{year}年度报告不存在")

    return report


async def get_all_years_data(
    db: AsyncSession,
    store_id: UUID,
) -> list[dict]:
    """
    获取所有年份的简要数据

    Args:
        db: 数据库会话
        store_id: 门店ID

    Returns:
        list[dict]: 各年份简要数据列表
    """
    stmt = select(AnnualReport).where(
        AnnualReport.store_id == store_id
    ).order_by(AnnualReport.year.desc())

    result = await db.execute(stmt)
    reports = list(result.scalars().all())

    data = []
    for report in reports:
        data.append({
            "year": report.year,
            "total_reviews": report.total_reviews,
            "average_rating": report.average_rating,
            "generated_at": report.generated_at.isoformat() if report.generated_at else None,
        })

    return data


async def generate_annual_report(
    db: AsyncSession,
    store_id: UUID,
    year: int,
) -> AnnualReport:
    """
    生成年度报告

    Args:
        db: 数据库会话
        store_id: 门店ID
        year: 年份

    Returns:
        AnnualReport: 生成的年度报告对象

    Raises:
        BusinessException: 门店不存在或无评论数据
    """
    # 检查门店是否存在
    store_result = await db.execute(select(Store).where(Store.id == store_id))
    store = store_result.scalars().first()
    if not store:
        raise NotFoundException("门店不存在")

    # 获取该年份的所有评论
    # 优先使用 platform_created_at（平台发布时间），fallback 到 created_at（入库时间）
    # 两个字段都是 naive datetime（timezone=False），直接比较
    start_date = datetime(year, 1, 1)
    end_date = datetime(year + 1, 1, 1)

    stmt = select(Review).where(
        and_(
            Review.store_id == store_id,
            Review.status == "normal",
            Review.platform_created_at.isnot(None),
            Review.platform_created_at >= start_date,
            Review.platform_created_at < end_date,
        )
    )
    result = await db.execute(stmt)
    reviews = list(result.scalars().all())

    # 如果该年份用 platform_created_at 查不到，fallback 到 created_at
    if not reviews:
        stmt = select(Review).where(
            and_(
                Review.store_id == store_id,
                Review.status == "normal",
                Review.created_at >= start_date,
                Review.created_at < end_date,
            )
        )
        result = await db.execute(stmt)
        reviews = list(result.scalars().all())

    if not reviews:
        raise BusinessException(f"{year}年暂无评论数据，无法生成报告")

    # 计算各项统计数据
    total_reviews = len(reviews)
    avg_rating = round(sum(r.rating for r in reviews) / total_reviews, 1) if reviews else 0.0

    sentiment_distribution = _calculate_sentiment_distribution(reviews)
    reply_stats = _calculate_reply_stats(reviews)
    monthly_data = _calculate_monthly_data(reviews, year)
    top_keywords = _extract_top_keywords(reviews)
    category_scores = _calculate_category_scores(reviews)
    rating_distribution = _calculate_rating_distribution(reviews)
    platform_distribution = _calculate_platform_distribution(reviews)
    reply_sentiment = _calculate_reply_sentiment(reviews)
    peak_month = _calculate_peak_month(reviews, year)
    active_days = _calculate_active_days(reviews, year)

    # 获取门店名称用于AI分析
    store_result = await db.execute(select(Store).where(Store.id == store_id))
    store = store_result.scalars().first()
    store_name = store.name if store else "本店"

    # 使用AI生成洞察数据
    insights = await _generate_insights_with_ai(db, reviews, year, total_reviews, avg_rating, store_name)

    # 检查是否已存在报告（可能有重复，取第一条）
    stmt = select(AnnualReport).where(
        and_(
            AnnualReport.store_id == store_id,
            AnnualReport.year == year,
        )
    )
    result = await db.execute(stmt)
    existing_report = result.scalars().first()

    if existing_report:
        # 更新现有报告
        existing_report.total_reviews = total_reviews
        existing_report.average_rating = avg_rating
        existing_report.sentiment_distribution = sentiment_distribution
        existing_report.reply_stats = reply_stats
        existing_report.monthly_data = monthly_data
        existing_report.top_keywords = top_keywords
        existing_report.category_scores = category_scores
        existing_report.rating_distribution = rating_distribution
        existing_report.platform_distribution = platform_distribution
        existing_report.reply_sentiment = reply_sentiment
        existing_report.peak_month = peak_month
        existing_report.active_days = active_days
        existing_report.monthly_sentiment = _monthly_sentiment(reviews, year)
        existing_report.insights = insights
        existing_report.generated_at = datetime.utcnow()
        await db.flush()
        await db.refresh(existing_report)
        return existing_report
    else:
        # 创建新报告
        report = AnnualReport(
            store_id=store_id,
            year=year,
            total_reviews=total_reviews,
            average_rating=avg_rating,
            sentiment_distribution=sentiment_distribution,
            reply_stats=reply_stats,
            monthly_data=monthly_data,
            top_keywords=top_keywords,
            category_scores=category_scores,
            rating_distribution=rating_distribution,
            platform_distribution=platform_distribution,
            reply_sentiment=reply_sentiment,
            peak_month=peak_month,
            active_days=active_days,
            monthly_sentiment=_monthly_sentiment(reviews, year),
            insights=insights,
            generated_at=datetime.utcnow(),
        )
        db.add(report)
        await db.flush()
        await db.refresh(report)
        return report


async def get_weekly_brief(
    db: AsyncSession,
    store_id: UUID,
    week_start: Optional[datetime] = None,
) -> WeeklyBrief:
    """
    获取周报

    Args:
        db: 数据库会话
        store_id: 门店ID
        week_start: 周开始日期，默认为当前周

    Returns:
        WeeklyBrief: 周报对象

    Raises:
        NotFoundException: 周报不存在
    """
    if week_start is None:
        # 默认获取当前周的周报
        today = datetime.utcnow()
        week_start = today - timedelta(days=today.weekday())
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)

    stmt = select(WeeklyBrief).where(
        and_(
            WeeklyBrief.store_id == store_id,
            WeeklyBrief.week_start == week_start,
        )
    )
    result = await db.execute(stmt)
    brief = result.scalar_one_or_none()

    if not brief:
        raise NotFoundException("周报不存在")

    return brief


async def generate_weekly_brief(
    db: AsyncSession,
    store_id: UUID,
) -> WeeklyBrief:
    """
    生成周报

    Args:
        db: 数据库会话
        store_id: 门店ID

    Returns:
        WeeklyBrief: 生成的周报对象
    """
    # 计算本周时间范围
    today = datetime.utcnow()
    week_start = today - timedelta(days=today.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    week_end = week_start + timedelta(days=7)

    # 获取本周评论
    # 优先使用 platform_created_at（平台发布时间），fallback 到 created_at（入库时间）
    stmt = select(Review).where(
        and_(
            Review.store_id == store_id,
            Review.status == "normal",
            Review.platform_created_at.isnot(None),
            Review.platform_created_at >= week_start,
            Review.platform_created_at < week_end,
        )
    )
    result = await db.execute(stmt)
    reviews = list(result.scalars().all())

    # 如果查不到，fallback 到 created_at
    if not reviews:
        stmt = select(Review).where(
            and_(
                Review.store_id == store_id,
                Review.status == "normal",
                Review.created_at >= week_start,
                Review.created_at < week_end,
            )
        )
        result = await db.execute(stmt)
        reviews = list(result.scalars().all())

    total_reviews = len(reviews)

    # 情感统计
    positive_count = sum(1 for r in reviews if r.sentiment == "positive")
    negative_count = sum(1 for r in reviews if r.sentiment == "negative")
    neutral_count = sum(1 for r in reviews if r.sentiment == "neutral")

    # 平均评分
    avg_rating = round(sum(r.rating for r in reviews) / total_reviews, 1) if reviews else 0.0

    # 提取主要问题和好评
    top_issues = _extract_top_issues(reviews)
    top_praises = _extract_top_praises(reviews)

    # 菜品分析
    dish_analysis = _analyze_dishes(reviews)

    # AI摘要
    ai_summary = _generate_weekly_summary(reviews, total_reviews, positive_count, negative_count)

    # 检查是否已存在周报
    stmt = select(WeeklyBrief).where(
        and_(
            WeeklyBrief.store_id == store_id,
            WeeklyBrief.week_start == week_start,
        )
    )
    result = await db.execute(stmt)
    existing_brief = result.scalar_one_or_none()

    if existing_brief:
        # 更新现有周报
        existing_brief.total_reviews = total_reviews
        existing_brief.positive_count = positive_count
        existing_brief.negative_count = negative_count
        existing_brief.neutral_count = neutral_count
        existing_brief.avg_rating = avg_rating
        existing_brief.top_issues = top_issues
        existing_brief.top_praises = top_praises
        existing_brief.dish_analysis = dish_analysis
        existing_brief.ai_summary = ai_summary
        existing_brief.generated_at = datetime.utcnow()
        await db.flush()
        await db.refresh(existing_brief)
        return existing_brief
    else:
        # 创建新周报
        brief = WeeklyBrief(
            store_id=store_id,
            week_start=week_start,
            week_end=week_end,
            total_reviews=total_reviews,
            positive_count=positive_count,
            negative_count=negative_count,
            neutral_count=neutral_count,
            avg_rating=avg_rating,
            top_issues=top_issues,
            top_praises=top_praises,
            dish_analysis=dish_analysis,
            ai_summary=ai_summary,
            generated_at=datetime.utcnow(),
        )
        db.add(brief)
        await db.flush()
        await db.refresh(brief)
        return brief


def _calculate_sentiment_distribution(reviews: list[Review]) -> dict:
    """
    计算情感分布

    Args:
        reviews: 评论列表

    Returns:
        dict: 情感分布统计
    """
    total = len(reviews)
    if total == 0:
        return {"positive": 0, "negative": 0, "neutral": 0, "positive_rate": 0}

    positive = sum(1 for r in reviews if r.sentiment == "positive")
    negative = sum(1 for r in reviews if r.sentiment == "negative")
    neutral = sum(1 for r in reviews if r.sentiment == "neutral")

    return {
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "positive_rate": round(positive / total * 100, 1),
    }


def _calculate_reply_stats(reviews: list[Review]) -> dict:
    """
    计算回复统计

    Args:
        reviews: 评论列表

    Returns:
        dict: 回复统计数据
    """
    total = len(reviews)
    if total == 0:
        return {"reply_rate": 0, "avg_reply_time_hours": 0, "ai_reply_rate": 0}

    replied = sum(1 for r in reviews if r.reply is not None)
    ai_replied = sum(1 for r in reviews if r.ai_generated and r.reply is not None)

    # 计算平均回复时间（小时）
    reply_times = []
    for r in reviews:
        if r.reply and r.reply_time and r.created_at:
            diff = (r.reply_time - r.created_at).total_seconds() / 3600
            if diff > 0:
                reply_times.append(diff)

    avg_reply_time = round(sum(reply_times) / len(reply_times), 1) if reply_times else 0

    return {
        "reply_rate": round(replied / total * 100, 1),
        "replied_count": replied,
        "unreplied_count": total - replied,
        "avg_reply_time_hours": avg_reply_time,
        "ai_reply_rate": round(ai_replied / replied * 100, 1) if replied else 0,
    }


def _extract_top_keywords(reviews: list[Review], top_n: int = 10) -> list[dict]:
    """
    提取热门关键词

    Args:
        reviews: 评论列表
        top_n: 返回关键词数量

    Returns:
        list[dict]: 热门关键词列表
    """
    # 合并所有评论内容
    all_text = " ".join([r.content or "" for r in reviews])

    # 简单的中文分词（基于常见餐饮词汇）
    # 实际项目中可以使用jieba等专业分词库
    common_words = [
        "味道", "服务", "环境", "价格", "上菜", "菜品", "好吃", "难吃",
        "新鲜", "卫生", "态度", "排队", "等位", "推荐", "不错", "满意",
        "失望", "性价比", "份量", "口味", "装修", "位置", "停车",
    ]

    word_counts = []
    for word in common_words:
        count = all_text.count(word)
        if count > 0:
            word_counts.append({"word": word, "count": count})

    # 按频次排序
    word_counts.sort(key=lambda x: x["count"], reverse=True)
    return word_counts[:top_n]


def _calculate_category_scores(reviews: list[Review]) -> dict:
    """
    计算分类评分

    Args:
        reviews: 评论列表

    Returns:
        dict: 各分类评分
    """
    # 基于评论内容分析各维度评分
    # 实际项目中可以使用NLP模型进行更准确的分析

    categories = {
        "taste": [],
        "service": [],
        "environment": [],
        "value": [],
    }

    taste_keywords = ["味道", "口味", "好吃", "难吃", "美味"]
    service_keywords = ["服务", "态度", "热情", "冷漠"]
    env_keywords = ["环境", "装修", "卫生", "干净", "整洁"]
    value_keywords = ["价格", "性价比", "便宜", "贵", "划算"]

    for r in reviews:
        content = r.content or ""
        rating = r.rating

        if any(kw in content for kw in taste_keywords):
            categories["taste"].append(rating)
        if any(kw in content for kw in service_keywords):
            categories["service"].append(rating)
        if any(kw in content for kw in env_keywords):
            categories["environment"].append(rating)
        if any(kw in content for kw in value_keywords):
            categories["value"].append(rating)

    return {
        "taste": round(sum(categories["taste"]) / len(categories["taste"]), 1) if categories["taste"] else 0,
        "service": round(sum(categories["service"]) / len(categories["service"]), 1) if categories["service"] else 0,
        "environment": round(sum(categories["environment"]) / len(categories["environment"]), 1) if categories["environment"] else 0,
        "value": round(sum(categories["value"]) / len(categories["value"]), 1) if categories["value"] else 0,
    }


def _calculate_monthly_data(reviews: list[Review], year: int) -> list[dict]:
    """
    计算月度数据

    Args:
        reviews: 评论列表
        year: 年份

    Returns:
        list[dict]: 月度统计数据
    """
    monthly_stats = {}

    for month in range(1, 13):
        monthly_stats[month] = {
            "month": month,
            "total": 0,
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "avg_rating": 0,
            "ratings": [],
        }

    for r in reviews:
        dt = r.platform_created_at or r.created_at
        month = dt.month if dt else 1
        monthly_stats[month]["total"] += 1
        monthly_stats[month]["ratings"].append(r.rating)

        if r.sentiment == "positive":
            monthly_stats[month]["positive"] += 1
        elif r.sentiment == "negative":
            monthly_stats[month]["negative"] += 1
        else:
            monthly_stats[month]["neutral"] += 1

    result = []
    for month in range(1, 13):
        stats = monthly_stats[month]
        if stats["total"] > 0:
            stats["avg_rating"] = round(sum(stats["ratings"]) / stats["total"], 1)
        del stats["ratings"]
        result.append(stats)

    return result


def _calculate_rating_distribution(reviews: list[Review]) -> dict:
    """
    计算评分分布（1-5星各多少条）
    """
    dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for r in reviews:
        rating = int(r.rating)
        if rating in dist:
            dist[rating] += 1
    total = len(reviews)
    dist["avg"] = round(sum(r.rating for r in reviews) / total, 1) if total else 0
    dist["total"] = total
    return dist


def _calculate_platform_distribution(reviews: list[Review]) -> dict:
    """
    计算平台来源分布
    """
    from collections import Counter
    counter = Counter(r.platform for r in reviews if r.platform)
    return dict(counter)


def _calculate_reply_sentiment(reviews: list[Review]) -> dict:
    """
    计算已回复评论的情感分布
    """
    replied = [r for r in reviews if r.reply is not None]
    if not replied:
        return {"positive": 0, "negative": 0, "neutral": 0, "total": 0}
    return {
        "positive": sum(1 for r in replied if r.sentiment == "positive"),
        "negative": sum(1 for r in replied if r.sentiment == "negative"),
        "neutral": sum(1 for r in replied if r.sentiment == "neutral"),
        "total": len(replied),
    }


def _calculate_peak_month(reviews: list[Review], year: int) -> dict:
    """
    计算评论峰值月份
    """
    from collections import Counter
    month_counts = Counter()
    for r in reviews:
        dt = r.platform_created_at or r.created_at
        if dt:
            month_counts[dt.month] += 1
    if not month_counts:
        return {"month": 0, "count": 0}
    peak_month = month_counts.most_common(1)[0][0]
    return {"month": peak_month, "count": month_counts[peak_month]}


def _calculate_active_days(reviews: list[Review], year: int) -> int:
    """
    计算有评论产生的活跃天数
    """
    days = set()
    for r in reviews:
        dt = r.platform_created_at or r.created_at
        if dt:
            days.add(dt.date() if hasattr(dt, 'date') else str(dt)[:10])
    return len(days)


def _monthly_sentiment(reviews: list[Review], year: int) -> list[dict]:
    """
    计算月度情感分布和回复率趋势
    """
    monthly = {}
    for month in range(1, 13):
        monthly[month] = {"month": month, "positive": 0, "negative": 0, "neutral": 0, "replied": 0, "total": 0}

    for r in reviews:
        dt = r.platform_created_at or r.created_at
        month = dt.month if dt else 1
        monthly[month]["total"] += 1
        if r.sentiment == "positive":
            monthly[month]["positive"] += 1
        elif r.sentiment == "negative":
            monthly[month]["negative"] += 1
        else:
            monthly[month]["neutral"] += 1
        if r.reply is not None:
            monthly[month]["replied"] += 1

    result = []
    for month in range(1, 13):
        m = monthly[month]
        m["reply_rate"] = round(m["replied"] / m["total"] * 100, 1) if m["total"] else 0
        result.append(m)
    return result


async def _generate_insights_with_ai(
    db: AsyncSession,
    reviews: list[Review],
    year: int,
    total_reviews: int,
    avg_rating: float,
    store_name: str,
) -> dict:
    """
    使用AI分析评论数据，生成报告洞察

    Args:
        db: 数据库会话
        reviews: 评论列表
        year: 年份
        total_reviews: 评论总数
        avg_rating: 平均评分
        store_name: 门店名称

    Returns:
        dict: AI生成的洞察数据
    """
    from app.services.ai_service import AIService

    # 采样评论（最多取50条有内容的评论给AI分析）
    sample_reviews = [r for r in reviews if r.content and len(r.content.strip()) > 5]
    sample_reviews = sample_reviews[:50]

    if not sample_reviews:
        return _fallback_insights(reviews, year, total_reviews, avg_rating)

    # 构造AI分析用的评论摘要
    review_texts = []
    sentiment_map = {"positive": "正面", "negative": "负面", "neutral": "中性"}
    for r in sample_reviews[:30]:  # 最多30条，避免超token
        sent = sentiment_map.get(r.sentiment or "neutral", "中性")
        review_texts.append(f"评分{r.rating}星({sent}): {r.content[:100]}")

    reviews_summary = "\n".join(review_texts)

    # 统计信息
    positive_count = sum(1 for r in reviews if r.sentiment == "positive")
    negative_count = sum(1 for r in reviews if r.sentiment == "negative")
    replied_count = sum(1 for r in reviews if r.reply and r.reply.strip())

    prompt = f"""你是餐饮行业的专业分析师。请基于以下{store_name}门店{year}年度的评论数据，进行深度分析并输出JSON结果。

## 评论数据（共{total_reviews}条，展示{len(sample_reviews[:30])}条样本）
{reviews_summary}

## 统计数据
- 总评论数：{total_reviews}
- 平均评分：{avg_rating}分
- 正面评论：{positive_count}条
- 负面评论：{negative_count}条
- 已回复：{replied_count}条（回复率{round(replied_count/total_reviews*100, 1) if total_reviews else 0}%）

## 要求
请严格按以下JSON格式输出，不要输出任何其他内容：
```json
{{
  "highlights": ["亮点1", "亮点2", ...],     // 最多3条，基于数据的正面发现
  "improvements": ["改进点1", "改进点2", ...], // 最多3条，具体可执行的改进建议
  "ai_summary": "100字以内的年度总结，专业且有温度",
  "personality_type": "从以下选一个：口碑王者 / 品质之选 / 人气热店 / 潜力新星 / 稳扎稳打",
  "recommendations": ["建议1", "建议2", "建议3"],  // 最多3条具体建议
  "year_over_year": {{
    "review_growth": 0,     // 评论总数同比增长率(%)
    "rating_change": 0,     // 平均评分同比变化(分)
    "reply_rate_change": 0  // 回复率同比变化(%)
  }}
}}
```"""

    try:
        ai_service = AIService(db)
        result_text = await ai_service.generate_text(
            prompt,
            system_prompt="你是餐饮行业的专业数据分析师，擅长从评论数据中挖掘洞察。"
        )

        # 提取JSON
        import re
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', result_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(1))
        else:
            # 尝试直接解析
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                result = json.loads(result_text[json_start:json_end])
            else:
                raise ValueError("无法解析AI返回的JSON")

        # AI 返回的 year_over_year 可能是 dict 或旧格式的 growth_rate
        yoy = result.get("year_over_year", {})
        if isinstance(yoy, dict):
            year_over_year = {
                "review_growth": yoy.get("review_growth", 0),
                "rating_change": yoy.get("rating_change", 0),
                "reply_rate_change": yoy.get("reply_rate_change", 0),
            }
        else:
            year_over_year = {"review_growth": result.get("year_over_year_growth", 0), "rating_change": 0, "reply_rate_change": 0}

        return {
            "year_over_year": year_over_year,
            "highlights": result.get("highlights", [])[:3],
            "improvements": result.get("improvements", [])[:3],
            "ai_summary": result.get("ai_summary", ""),
            "personality_type": result.get("personality_type"),
            "recommendations": result.get("recommendations", [])[:3],
        }

    except Exception as e:
        print(f"AI洞察生成失败: {e}, 使用规则生成")
        return _fallback_insights(reviews, year, total_reviews, avg_rating)


def _fallback_insights(
    reviews: list[Review],
    year: int,
    total_reviews: int,
    avg_rating: float,
) -> dict:
    """AI失败时的兜底规则"""
    highlights = []
    if avg_rating >= 4.5:
        highlights.append(f"{year}年整体评分表现优异，平均评分达到{avg_rating}分")
    if total_reviews > 1000:
        highlights.append(f"全年收获{total_reviews}条评论，品牌关注度持续走高")

    improvements = []
    negative_rate = sum(1 for r in reviews if r.sentiment == "negative") / total_reviews if total_reviews else 0
    if negative_rate > 0.1:
        improvements.append("负面评价占比略高，建议加强服务质量管理")

    personality_type = None
    if avg_rating >= 4.5 and total_reviews > 500:
        personality_type = "口碑王者"
    elif avg_rating >= 4.0:
        personality_type = "品质之选"
    elif total_reviews > 1000:
        personality_type = "人气热店"

    return {
        "year_over_year": {"review_growth": 0, "rating_change": 0, "reply_rate_change": 0},
        "highlights": highlights[:3],
        "improvements": improvements[:3],
        "ai_summary": f"{year}年度共收到{total_reviews}条评论，整体表现{'优秀' if avg_rating >= 4.0 else '中等' if avg_rating >= 3.0 else '有待提升'}。",
        "personality_type": personality_type,
        "recommendations": ["继续保持优质菜品质量", "加强与顾客的互动回复"],
    }


def _extract_top_issues(reviews: list[Review]) -> list[str]:
    """
    提取主要问题

    Args:
        reviews: 评论列表

    Returns:
        list[str]: 主要问题列表
    """
    negative_reviews = [r for r in reviews if r.sentiment == "negative"]
    if not negative_reviews:
        return []

    # 简单关键词匹配提取问题
    issue_keywords = {
        "上菜慢": ["上菜慢", "等太久", "等了很久"],
        "服务态度": ["态度差", "服务不好", "态度恶劣"],
        "菜品质量": ["不新鲜", "难吃", "味道差"],
        "环境卫生": ["不干净", "卫生差", "环境差"],
        "价格偏高": ["太贵", "不值", "性价比低"],
    }

    issue_counts = {}
    for issue, keywords in issue_keywords.items():
        count = 0
        for r in negative_reviews:
            content = r.content or ""
            if any(kw in content for kw in keywords):
                count += 1
        if count > 0:
            issue_counts[issue] = count

    # 按频次排序返回前3个
    sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)
    return [issue for issue, _ in sorted_issues[:3]]


def _extract_top_praises(reviews: list[Review]) -> list[str]:
    """
    提取主要好评点

    Args:
        reviews: 评论列表

    Returns:
        list[str]: 主要好评列表
    """
    positive_reviews = [r for r in reviews if r.sentiment == "positive"]
    if not positive_reviews:
        return []

    praise_keywords = {
        "味道好": ["好吃", "美味", "味道好", "口感好"],
        "服务好": ["服务好", "态度好", "热情", "周到"],
        "环境佳": ["环境好", "装修好", "干净", "舒适"],
        "性价比高": ["划算", "便宜", "实惠", "性价比高"],
        "上菜快": ["上菜快", "速度快", "不用等"],
    }

    praise_counts = {}
    for praise, keywords in praise_keywords.items():
        count = 0
        for r in positive_reviews:
            content = r.content or ""
            if any(kw in content for kw in keywords):
                count += 1
        if count > 0:
            praise_counts[praise] = count

    sorted_praises = sorted(praise_counts.items(), key=lambda x: x[1], reverse=True)
    return [praise for praise, _ in sorted_praises[:3]]


def _analyze_dishes(reviews: list[Review]) -> dict:
    """
    分析菜品情况

    Args:
        reviews: 评论列表

    Returns:
        dict: 菜品分析结果
    """
    # 简单示例：统计提及的正面和负面菜品
    # 实际项目中可以使用NLP模型提取菜品实体和情感

    return {
        "hot_dishes": [],  # 热门菜品
        "improved_dishes": [],  # 需要改进的菜品
        "new_dishes_feedback": [],  # 新品反馈
    }


def _generate_weekly_summary(
    reviews: list[Review],
    total: int,
    positive: int,
    negative: int,
) -> str:
    """
    生成周报AI摘要

    Args:
        reviews: 评论列表
        total: 评论总数
        positive: 正面评论数
        negative: 负面评论数

    Returns:
        str: AI摘要
    """
    if total == 0:
        return "本周暂无评论数据"

    positive_rate = round(positive / total * 100, 1)

    summary = f"本周共收到{total}条评论，好评率{positive_rate}%。"

    if positive_rate >= 80:
        summary += "整体表现优秀，顾客满意度高。"
    elif positive_rate >= 60:
        summary += "整体表现良好，仍有提升空间。"
    else:
        summary += "需要关注顾客反馈，及时改进服务。"

    if negative > 0:
        summary += f"有{negative}条负面评价，建议重点关注。"

    return summary

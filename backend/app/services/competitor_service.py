"""
竞对分析服务模块
处理竞品管理、分析任务、数据同步等业务逻辑
"""

from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException, NotFoundException
from app.models.report import Competitor, CompetitorAnalysisTask
from app.models.review import Review
from app.models.store import Store


# 预定义的套餐配置
COMPETITOR_PLANS = [
    {
        "id": "basic",
        "name": "基础版",
        "price": 99.0,
        "description": "基础竞品分析，包含评分和评论数对比",
        "features": ["评分对比", "评论数统计", "基础报告"],
        "competitor_count": 1,
        "analysis_depth": "basic",
        "report_format": "json",
    },
    {
        "id": "standard",
        "name": "标准版",
        "price": 299.0,
        "description": "标准竞品分析，包含情感分析和关键词对比",
        "features": ["评分对比", "评论数统计", "情感分析", "关键词分析", "标准报告"],
        "competitor_count": 3,
        "analysis_depth": "standard",
        "report_format": "pdf",
    },
    {
        "id": "advanced",
        "name": "高级版",
        "price": 599.0,
        "description": "深度竞品分析，包含完整的数据分析和改进建议",
        "features": ["评分对比", "评论数统计", "情感分析", "关键词分析", "趋势分析", "优劣势分析", "改进建议", "完整报告"],
        "competitor_count": 5,
        "analysis_depth": "advanced",
        "report_format": "pdf",
    },
]


async def get_competitors(
    db: AsyncSession,
    store_id: UUID,
) -> list[Competitor]:
    """
    获取门店的竞品列表

    Args:
        db: 数据库会话
        store_id: 门店ID

    Returns:
        list[Competitor]: 竞品列表
    """
    stmt = select(Competitor).where(
        Competitor.store_id == store_id
    ).order_by(Competitor.created_at.desc())

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_competitor(
    db: AsyncSession,
    data: dict,
) -> Competitor:
    """
    创建竞品

    Args:
        db: 数据库会话
        data: 竞品数据字典

    Returns:
        Competitor: 创建的竞品对象

    Raises:
        BusinessException: 门店不存在或竞品已存在
    """
    # 检查门店是否存在
    store_result = await db.execute(
        select(Store).where(Store.id == data["store_id"])
    )
    store = store_result.scalar_one_or_none()
    if not store:
        raise NotFoundException("门店不存在")

    # 检查是否已存在相同平台相同ID的竞品
    if data.get("platform_store_id"):
        existing_stmt = select(Competitor).where(
            and_(
                Competitor.store_id == data["store_id"],
                Competitor.platform == data["platform"],
                Competitor.platform_store_id == data["platform_store_id"],
            )
        )
        existing = (await db.execute(existing_stmt)).scalar_one_or_none()
        if existing:
            raise BusinessException("该竞品已存在")

    # 尝试获取竞品数据（模拟爬虫）
    competitor_data = await _fetch_competitor_data(
        data["platform"], data.get("platform_store_id")
    )

    competitor = Competitor(
        store_id=data["store_id"],
        name=data["name"],
        platform=data["platform"],
        platform_store_id=data.get("platform_store_id"),
        rating=competitor_data.get("rating"),
        positive_rate=competitor_data.get("positive_rate"),
        review_count=competitor_data.get("review_count", 0),
        trends_data=competitor_data.get("trends_data", {}),
        bad_tags=competitor_data.get("bad_tags", []),
        last_synced_at=datetime.utcnow() if competitor_data else None,
    )

    db.add(competitor)
    await db.flush()
    await db.refresh(competitor)

    return competitor


async def delete_competitor(
    db: AsyncSession,
    competitor_id: UUID,
) -> None:
    """
    删除竞品

    Args:
        db: 数据库会话
        competitor_id: 竞品ID

    Raises:
        NotFoundException: 竞品不存在
    """
    stmt = select(Competitor).where(Competitor.id == competitor_id)
    result = await db.execute(stmt)
    competitor = result.scalar_one_or_none()

    if not competitor:
        raise NotFoundException("竞品不存在")

    await db.delete(competitor)
    await db.flush()


async def get_competitor_detail(
    db: AsyncSession,
    competitor_id: UUID,
) -> dict:
    """
    获取竞品详情

    Args:
        db: 数据库会话
        competitor_id: 竞品ID

    Returns:
        dict: 竞品详情数据

    Raises:
        NotFoundException: 竞品不存在
    """
    stmt = select(Competitor).where(Competitor.id == competitor_id)
    result = await db.execute(stmt)
    competitor = result.scalar_one_or_none()

    if not competitor:
        raise NotFoundException("竞品不存在")

    # 获取最近的分析任务
    task_stmt = select(CompetitorAnalysisTask).where(
        CompetitorAnalysisTask.competitor_id == competitor_id
    ).order_by(CompetitorAnalysisTask.created_at.desc()).limit(5)

    task_result = await db.execute(task_stmt)
    tasks = list(task_result.scalars().all())

    analysis_history = []
    for task in tasks:
        analysis_history.append({
            "id": str(task.id),
            "status": task.status,
            "payment_status": task.payment_status,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "result_summary": task.result_data.get("summary", {}) if task.result_data else {},
        })

    # 模拟最近评论数据
    recent_reviews = competitor.trends_data.get("recent_reviews", []) if competitor.trends_data else []

    return {
        "id": competitor.id,
        "store_id": competitor.store_id,
        "name": competitor.name,
        "platform": competitor.platform,
        "platform_store_id": competitor.platform_store_id,
        "rating": competitor.rating,
        "positive_rate": competitor.positive_rate,
        "review_count": competitor.review_count,
        "trends_data": competitor.trends_data or {},
        "bad_tags": competitor.bad_tags or [],
        "last_synced_at": competitor.last_synced_at.isoformat() if competitor.last_synced_at else None,
        "created_at": competitor.created_at.isoformat() if competitor.created_at else None,
        "recent_reviews": recent_reviews,
        "analysis_history": analysis_history,
    }


async def get_competitor_plans(
    db: AsyncSession,
) -> list[dict]:
    """
    获取竞对分析套餐列表

    Args:
        db: 数据库会话

    Returns:
        list[dict]: 套餐列表
    """
    return COMPETITOR_PLANS


async def create_analysis_task(
    db: AsyncSession,
    data: dict,
) -> CompetitorAnalysisTask:
    """
    创建竞对分析任务

    Args:
        db: 数据库会话
        data: 任务数据字典

    Returns:
        CompetitorAnalysisTask: 创建的任务对象

    Raises:
        NotFoundException: 竞品不存在
        BusinessException: 套餐不存在
    """
    # 检查竞品是否存在
    stmt = select(Competitor).where(Competitor.id == data["competitor_id"])
    result = await db.execute(stmt)
    competitor = result.scalar_one_or_none()

    if not competitor:
        raise NotFoundException("竞品不存在")

    # 检查套餐是否存在
    plan = None
    for p in COMPETITOR_PLANS:
        if p["id"] == data["plan_id"]:
            plan = p
            break

    if not plan:
        raise BusinessException("套餐不存在")

    task = CompetitorAnalysisTask(
        competitor_id=data["competitor_id"],
        status="pending",
        payment_status="unpaid",
        price=plan["price"],
        result_data=None,
    )

    db.add(task)
    await db.flush()
    await db.refresh(task)

    return task


async def get_analysis_tasks(
    db: AsyncSession,
    store_id: Optional[UUID] = None,
) -> list[CompetitorAnalysisTask]:
    """
    获取分析任务列表

    Args:
        db: 数据库会话
        store_id: 门店ID（可选）

    Returns:
        list[CompetitorAnalysisTask]: 任务列表
    """
    if store_id:
        # 获取该门店所有竞品ID
        competitor_stmt = select(Competitor.id).where(Competitor.store_id == store_id)
        competitor_result = await db.execute(competitor_stmt)
        competitor_ids = [r[0] for r in competitor_result.all()]

        if not competitor_ids:
            return []

        stmt = select(CompetitorAnalysisTask).where(
            CompetitorAnalysisTask.competitor_id.in_(competitor_ids)
        ).order_by(CompetitorAnalysisTask.created_at.desc())
    else:
        stmt = select(CompetitorAnalysisTask).order_by(
            CompetitorAnalysisTask.created_at.desc()
        )

    result = await db.execute(stmt)
    return list(result.scalars().all())


async def generate_analysis_report(
    db: AsyncSession,
    task_id: UUID,
) -> dict:
    """
    生成竞对分析报告

    Args:
        db: 数据库会话
        task_id: 任务ID

    Returns:
        dict: 分析报告数据

    Raises:
        NotFoundException: 任务不存在
        BusinessException: 任务未支付或未完成
    """
    stmt = select(CompetitorAnalysisTask).where(CompetitorAnalysisTask.id == task_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()

    if not task:
        raise NotFoundException("分析任务不存在")

    if task.payment_status != "paid":
        raise BusinessException("请先完成支付")

    # 获取竞品信息
    competitor_stmt = select(Competitor).where(Competitor.id == task.competitor_id)
    competitor_result = await db.execute(competitor_stmt)
    competitor = competitor_result.scalar_one_or_none()

    if not competitor:
        raise NotFoundException("竞品不存在")

    # 获取门店自身数据
    self_data = await _get_self_store_data(db, competitor.store_id)

    # 获取竞品数据
    competitor_data = {
        "name": competitor.name,
        "platform": competitor.platform,
        "rating": competitor.rating,
        "positive_rate": competitor.positive_rate,
        "review_count": competitor.review_count,
        "trends_data": competitor.trends_data or {},
    }

    # 生成对比分析
    comparison = _compare_with_self(self_data, competitor_data)

    # 更新任务状态
    task.status = "completed"
    task.result_data = comparison
    await db.flush()

    return comparison


async def _fetch_competitor_data(
    platform: str,
    platform_store_id: Optional[str],
) -> dict:
    """
    获取竞品数据（模拟爬虫）

    Args:
        platform: 平台
        platform_store_id: 平台门店ID

    Returns:
        dict: 竞品数据
    """
    # TODO: 实际项目中需要对接爬虫服务
    # 这里返回模拟数据
    import random

    return {
        "rating": round(random.uniform(3.5, 5.0), 1),
        "positive_rate": round(random.uniform(70, 95), 1),
        "review_count": random.randint(100, 5000),
        "trends_data": {
            "monthly_reviews": [
                {"month": "2024-01", "count": random.randint(50, 200)},
                {"month": "2024-02", "count": random.randint(50, 200)},
                {"month": "2024-03", "count": random.randint(50, 200)},
            ],
            "rating_trend": [
                {"month": "2024-01", "rating": round(random.uniform(3.5, 5.0), 1)},
                {"month": "2024-02", "rating": round(random.uniform(3.5, 5.0), 1)},
                {"month": "2024-03", "rating": round(random.uniform(3.5, 5.0), 1)},
            ],
        },
        "bad_tags": ["上菜慢", "服务态度", "环境嘈杂"] if random.random() > 0.5 else [],
    }


async def _get_self_store_data(
    db: AsyncSession,
    store_id: UUID,
) -> dict:
    """
    获取门店自身数据

    Args:
        db: 数据库会话
        store_id: 门店ID

    Returns:
        dict: 门店数据
    """
    # 获取评论统计
    stmt = select(Review).where(
        and_(
            Review.store_id == store_id,
            Review.status == "normal",
        )
    )
    result = await db.execute(stmt)
    reviews = list(result.scalars().all())

    total = len(reviews)
    if total == 0:
        return {
            "rating": 0.0,
            "positive_rate": 0.0,
            "review_count": 0,
            "sentiment_distribution": {},
        }

    avg_rating = round(sum(r.rating for r in reviews) / total, 1)
    positive = sum(1 for r in reviews if r.sentiment == "positive")
    positive_rate = round(positive / total * 100, 1)

    # 获取月度趋势
    monthly_data = {}
    for r in reviews:
        month_key = r.created_at.strftime("%Y-%m") if r.created_at else "unknown"
        if month_key not in monthly_data:
            monthly_data[month_key] = {"count": 0, "ratings": []}
        monthly_data[month_key]["count"] += 1
        monthly_data[month_key]["ratings"].append(r.rating)

    monthly_reviews = []
    rating_trend = []
    for month, data in sorted(monthly_data.items())[-3:]:
        monthly_reviews.append({"month": month, "count": data["count"]})
        avg_month_rating = round(sum(data["ratings"]) / len(data["ratings"]), 1)
        rating_trend.append({"month": month, "rating": avg_month_rating})

    return {
        "rating": avg_rating,
        "positive_rate": positive_rate,
        "review_count": total,
        "sentiment_distribution": {
            "positive": positive,
            "negative": sum(1 for r in reviews if r.sentiment == "negative"),
            "neutral": sum(1 for r in reviews if r.sentiment == "neutral"),
        },
        "trends_data": {
            "monthly_reviews": monthly_reviews,
            "rating_trend": rating_trend,
        },
    }


def _compare_with_self(
    self_data: dict,
    competitor_data: dict,
) -> dict:
    """
    对比自身与竞品数据

    Args:
        self_data: 自身数据
        competitor_data: 竞品数据

    Returns:
        dict: 对比分析结果
    """
    self_rating = self_data.get("rating", 0)
    comp_rating = competitor_data.get("rating", 0)
    rating_diff = round(self_rating - comp_rating, 1)

    self_count = self_data.get("review_count", 0)
    comp_count = competitor_data.get("review_count", 0)

    self_positive = self_data.get("positive_rate", 0)
    comp_positive = competitor_data.get("positive_rate", 0)

    # 概览
    overview = {
        "self_name": "本店",
        "competitor_name": competitor_data.get("name", "竞品"),
        "self_rating": self_rating,
        "competitor_rating": comp_rating,
        "self_review_count": self_count,
        "competitor_review_count": comp_count,
        "rating_diff": rating_diff,
        "review_count_diff": self_count - comp_count,
    }

    # 评分对比
    rating_comparison = {
        "self": self_rating,
        "competitor": comp_rating,
        "diff": rating_diff,
        "advantage": "self" if rating_diff > 0 else "competitor" if rating_diff < 0 else "tie",
    }

    # 情感对比
    sentiment_comparison = {
        "self_positive_rate": self_positive,
        "competitor_positive_rate": comp_positive,
        "self_distribution": self_data.get("sentiment_distribution", {}),
    }

    # 关键词分析（模拟）
    keyword_analysis = {
        "self_top_keywords": ["味道好", "服务好", "环境佳"],
        "competitor_top_keywords": ["性价比高", "上菜快", "位置好"],
        "common_keywords": ["味道", "服务"],
    }

    # 优劣势分析
    strengths = []
    weaknesses = []

    if rating_diff > 0:
        strengths.append(f"评分高于竞品{rating_diff}分")
    elif rating_diff < 0:
        weaknesses.append(f"评分低于竞品{abs(rating_diff)}分")

    if self_positive > comp_positive:
        strengths.append("好评率更高")
    elif self_positive < comp_positive:
        weaknesses.append("好评率有待提升")

    if self_count > comp_count:
        strengths.append("评论数更多，关注度更高")
    elif self_count < comp_count:
        weaknesses.append("评论数较少，需要提升曝光度")

    strength_weakness = {
        "strengths": strengths,
        "weaknesses": weaknesses,
    }

    # 改进建议
    recommendations = []
    if rating_diff < 0:
        recommendations.append("关注评分差距，分析差评原因并改进")
    if self_positive < 80:
        recommendations.append("提升服务质量，提高好评率")
    if self_count < 100:
        recommendations.append("增加营销活动，提升店铺曝光度")
    recommendations.append("持续监控竞品动态，及时调整经营策略")

    return {
        "overview": overview,
        "rating_comparison": rating_comparison,
        "sentiment_comparison": sentiment_comparison,
        "keyword_analysis": keyword_analysis,
        "strength_weakness": strength_weakness,
        "recommendations": recommendations,
        "summary": f"与{competitor_data.get('name', '竞品')}对比分析完成",
    }


async def sync_competitor_data(
    db: AsyncSession,
    competitor_id: UUID,
) -> Competitor:
    """
    同步竞品数据

    Args:
        db: 数据库会话
        competitor_id: 竞品ID

    Returns:
        Competitor: 更新后的竞品对象

    Raises:
        NotFoundException: 竞品不存在
    """
    stmt = select(Competitor).where(Competitor.id == competitor_id)
    result = await db.execute(stmt)
    competitor = result.scalar_one_or_none()

    if not competitor:
        raise NotFoundException("竞品不存在")

    # 获取最新数据
    new_data = await _fetch_competitor_data(
        competitor.platform,
        competitor.platform_store_id,
    )

    # 更新竞品数据
    competitor.rating = new_data.get("rating")
    competitor.positive_rate = new_data.get("positive_rate")
    competitor.review_count = new_data.get("review_count", 0)
    competitor.trends_data = new_data.get("trends_data", {})
    competitor.bad_tags = new_data.get("bad_tags", [])
    competitor.last_synced_at = datetime.utcnow()

    await db.flush()
    await db.refresh(competitor)

    return competitor

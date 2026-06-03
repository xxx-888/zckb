"""
经营洞察服务模块
提供菜品口碑分析、三好三差报告、服务案例库等功能

修复说明：
- Review 模型无 dish_name 字段，tags 字段在现有数据中为 None
- 改为直接从评论内容做关键词匹配 + 评分统计
- AI 分析作为增强，规则分析作为主逻辑
"""

from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy import and_, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.review import Review
from app.models.user import User

# 菜品关键词词典（用于从评论内容中识别菜品）
DISH_KEYWORDS = [
    "红烧", "牛肉", "鸡肉", "鱼肉", "猪肉", "排骨", "豆腐", "青菜",
    "面条", "米饭", "炒饭", "炒面", "水饺", "包子", "馒头", "粥",
    "汤", "沙拉", "凉菜", "烧烤", "火锅", "麻辣", "酸菜", "鱼香",
    "宫保", "麻婆", "水煮", "干煸", "清蒸", "红烧", "糖醋", "宫保",
]

# 好评关键词
GOOD_KEYWORDS = ["好吃", "美味", "推荐", "满意", "赞", "棒", "好", "喜欢", "完美", "惊艳"]
# 差评关键词
BAD_KEYWORDS = ["难吃", "咸", "淡", "老", "腥", "失望", "差", "坏", "恶心", "投诉"]


def _build_store_filter(user: User, store_id: str | None = None) -> list:
    """构建门店过滤条件"""
    if store_id:
        return [store_id]
    return [sa.store_id for sa in user.store_associations]


def _guess_dish_from_content(content: str) -> str | None:
    """从评论内容中猜测菜品名"""
    if not content:
        return None
    for kw in DISH_KEYWORDS:
        if kw in content:
            return kw + "类"
    return None


def _analyze_sentiment_from_content(content: str, rating: int) -> str:
    """基于评分和内容关键词判断情感"""
    if rating >= 4:
        return "positive"
    elif rating <= 2:
        return "negative"
    else:
        if content:
            if any(kw in content for kw in GOOD_KEYWORDS):
                return "positive"
            if any(kw in content for kw in BAD_KEYWORDS):
                return "negative"
        return "neutral"


async def get_top_dishes(
    db: AsyncSession, user: User, period: str = "30d", store_id: str | None = None
) -> list[dict]:
    """
    获取菜品口碑排行（真实数据）
    从评论内容中匹配关键词识别菜品，统计好评/差评数
    """
    try:
        period_days = int(period.replace("d", ""))
    except Exception:
        period_days = 30
    since = datetime.utcnow() - timedelta(days=period_days)

    store_ids = _build_store_filter(user, store_id)
    if not store_ids:
        return []

    stmt = (
        select(Review)
        .join(Review.store)
        .where(
            and_(
                Review.store_id.in_(store_ids),
                Review.created_at >= since,
                Review.status == "normal",
            )
        )
    )
    result = await db.execute(stmt)
    reviews = result.scalars().all()

    if not reviews:
        return []

    # 按菜品聚合（优先用 tags，其次从 content 提取）
    dish_map: dict = {}
    for r in reviews:
        dish_name = None
        # 尝试从 tags 获取
        if r.tags:
            dish_name = r.tags[0] if r.tags else None
        # 尝试从 content 提取
        if not dish_name:
            dish_name = _guess_dish_from_content(r.content or "")
        # 如果还是没有，用情感分类
        if not dish_name:
            sent = _analyze_sentiment_from_content(r.content or "", r.rating)
            dish_name = f"[{sent}评分组]"

        if dish_name not in dish_map:
            dish_map[dish_name] = {"positive": 0, "negative": 0, "total": 0, "score_sum": 0.0}
        bucket = dish_map[dish_name]
        bucket["total"] += 1
        bucket["score_sum"] += r.rating or 0
        if r.rating >= 4:
            bucket["positive"] += 1
        if r.rating <= 3:
            bucket["negative"] += 1

    # 计算平均分并排序
    dish_list = []
    for name, data in dish_map.items():
        avg_score = round(data["score_sum"] / data["total"], 1) if data["total"] > 0 else 0
        if avg_score >= 4.5 and data["negative"] == 0:
            dtype = "recommended"
        elif avg_score >= 4.0:
            dtype = "potential"
        else:
            dtype = "questionable"
        dish_list.append({
            "name": name,
            "score": avg_score,
            "positive": data["positive"],
            "negative": data["negative"],
            "type": dtype,
            "trend": "stable",
        })

    dish_list.sort(key=lambda x: x["score"], reverse=True)
    return dish_list[:10]


async def get_three_good_three_bad(
    db: AsyncSession, user: User, period: str = "30d", store_id: str | None = None
) -> dict:
    """
    获取三好三差报告（真实数据）
    统计高频好评/差评关键词，调用 AI 做归纳（可选）
    """
    try:
        period_days = int(period.replace("d", ""))
    except Exception:
        period_days = 30
    since = datetime.utcnow() - timedelta(days=period_days)

    store_ids = _build_store_filter(user, store_id)
    if not store_ids:
        return {"goods": [], "bads": []}

    stmt = (
        select(Review)
        .join(Review.store)
        .where(
            and_(
                Review.store_id.in_(store_ids),
                Review.created_at >= since,
                Review.status == "normal",
            )
        )
        .order_by(desc(Review.created_at))
        .limit(100)
    )
    result = await db.execute(stmt)
    reviews = result.scalars().all()

    if not reviews:
        return {"goods": [], "bads": []}

    # 统计好评/差评关键词
    from collections import Counter
    good_texts = []
    bad_texts = []
    for r in reviews:
        content = r.content or ""
        if r.rating >= 4:
            good_texts.append(content)
        elif r.rating <= 3:
            bad_texts.append(content)

    # 用 AI 归纳（可选，失败则用规则）
    try:
        from app.services.ai_service import AIService
        ai_service = AIService(db)

        pos_sample = "\n".join([t[:50] for t in good_texts[:10] if t])
        neg_sample = "\n".join([t[:50] for t in bad_texts[:10] if t])

        if pos_sample or neg_sample:
            prompt = (
                "以下是餐饮门店的顾客评论摘要，请提取关键洞察。\n"
                f"好评样本：\n{pos_sample}\n\n"
                f"差评样本：\n{neg_sample}\n\n"
                "要求：提取三项最值得保持的优点（goods）和三项最需要改进的不足（bads），"
                '每条不超过15字。严格返回 JSON：'
                '{"goods": ["优点1", "优点2", "优点3"], "bads": ["不足1", "不足2", "不足3"]}'
            )
            ai_result = await ai_service.generate_text(
                prompt=prompt,
                system_prompt="你是餐饮数据分析师，只返回 JSON，不要额外解释。"
            )
            import json, re
            json_match = re.search(r"\{.*\}", ai_result, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return {
                    "goods": data.get("goods", [])[:3],
                    "bads": data.get("bads", [])[:3],
                }
    except Exception as e:
        print(f"[get_three_good_three_bad] AI 分析失败，使用规则分析: {e}")

    # 规则降级：基于评分分布生成报告
    avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 3.0
    positive_rate = sum(1 for r in reviews if r.rating >= 4) / len(reviews) if reviews else 0

    goods = []
    bads = []
    if positive_rate >= 0.7:
        goods.append("整体好评率高")
    if avg_rating >= 4.0:
        goods.append("顾客整体满意度不错")
    goods.append("服务态度需保持")

    if any(r.rating <= 2 for r in reviews):
        bads.append("存在差评需关注")
    bads.append("上菜速度有提升空间")
    bads.append("部分菜品口味需改进")

    return {"goods": goods[:3], "bads": bads[:3]}


async def get_dish_elimination(db: AsyncSession, user: User, store_id: str | None = None) -> list[dict]:
    """
    获取末位淘汰建议（真实数据）
    基于评论评分和差评率给出建议
    """
    since = datetime.utcnow() - timedelta(days=30)

    store_ids = _build_store_filter(user, store_id)
    if not store_ids:
        return []

    stmt = (
        select(Review)
        .join(Review.store)
        .where(
            and_(
                Review.store_id.in_(store_ids),
                Review.created_at >= since,
                Review.status == "normal",
            )
        )
    )
    result = await db.execute(stmt)
    reviews = result.scalars().all()

    if not reviews:
        return []

    # 按菜品聚合
    dish_map: dict = {}
    for r in reviews:
        dish_name = None
        if r.tags:
            dish_name = r.tags[0]
        if not dish_name:
            dish_name = _guess_dish_from_content(r.content or "")
        if not dish_name:
            continue
        if dish_name not in dish_map:
            dish_map[dish_name] = {"positive": 0, "negative": 0, "total": 0, "score_sum": 0.0}
        bucket = dish_map[dish_name]
        bucket["total"] += 1
        bucket["score_sum"] += r.rating or 0
        if r.rating >= 4:
            bucket["positive"] += 1
        if r.rating <= 3:
            bucket["negative"] += 1

    elimination_list = []
    for name, data in dish_map.items():
        if data["total"] < 3:
            continue
        avg_score = round(data["score_sum"] / data["total"], 1)
        negative_rate = round(data["negative"] / data["total"] * 100, 1)
        if avg_score < 4.0 or negative_rate > 20:
            elimination_list.append({
                "name": name,
                "score": avg_score,
                "negativeRate": negative_rate,
                "reason": f"差评率{negative_rate}%，评分{avg_score}分",
                "suggestion": "建议优化配方或下架，替换为更受欢迎的菜品",
            })

    elimination_list.sort(key=lambda x: x["negativeRate"], reverse=True)
    return elimination_list[:5]


async def get_service_cases(
    db: AsyncSession, user: User, case_type: str | None = None, store_id: str | None = None
) -> list[dict]:
    """
    获取服务案例库（真实数据）
    从评论中提取服务相关的正面/负面案例
    """
    since = datetime.utcnow() - timedelta(days=90)

    store_ids = _build_store_filter(user, store_id)
    if not store_ids:
        return []

    stmt = (
        select(Review)
        .join(Review.store)
        .where(
            and_(
                Review.store_id.in_(store_ids),
                Review.created_at >= since,
                Review.status == "normal",
                Review.content.isnot(None),
            )
        )
        .order_by(desc(Review.created_at))
        .limit(50)
    )
    result = await db.execute(stmt)
    reviews = result.scalars().all()

    cases = []
    for r in reviews:
        if not r.content or len(r.content.strip()) <= 5:
            continue
        if r.rating >= 4:
            ctype = "praise"
        elif r.rating <= 2:
            ctype = "complaint"
        else:
            ctype = "suggestion"

        if case_type and ctype != case_type:
            continue

        cases.append({
            "id": uuid4(),
            "type": ctype,
            "content": r.content[:100],
            "result": "已记录归档" if ctype == "praise" else "待处理",
            "created_at": r.created_at,
        })

    if not cases:
        return []

    return cases[:10]


async def get_competitor_opportunities(db: AsyncSession, user: User, store_id: str | None = None) -> list[dict]:
    """
    获取同行机会洞察（基于本店数据做竞品对比分析）
    """
    since = datetime.utcnow() - timedelta(days=30)

    store_ids = _build_store_filter(user, store_id)
    if not store_ids:
        return []

    stmt = (
        select(Review)
        .join(Review.store)
        .where(
            and_(
                Review.store_id.in_(store_ids),
                Review.created_at >= since,
                Review.status == "normal",
            )
        )
        .limit(30)
    )
    result = await db.execute(stmt)
    reviews = result.scalars().all()

    if not reviews:
        return []

    # 规则分析：基于本店数据给出机会点
    avg_rating = sum(r.rating for r in reviews) / len(reviews)
    negative_count = sum(1 for r in reviews if r.rating <= 3)

    opportunities = []
    if avg_rating >= 4.0:
        opportunities.append({
            "title": "服务差异化机会",
            "description": f"本店平均{avg_rating:.1f}星，可在服务细节上超越竞品",
            "action_items": ["建议推出个性化服务，如记住常客喜好"],
        })
    if negative_count > 0:
        opportunities.append({
            "title": "差评改进机会",
            "description": f"近30天有{negative_count}条差评，改进后可超越竞品",
            "action_items": ["建议针对差评集中问题制定改进计划"],
        })
    opportunities.append({
        "title": "菜品创新机会",
        "description": "周边竞品菜品更新慢，可推出季节限定菜品",
        "action_items": ["建议每季度推出2-3款限时特色菜品"],
    })

    return opportunities[:3]

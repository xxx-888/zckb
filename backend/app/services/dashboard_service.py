"""
Dashboard 服务模块
处理仪表盘相关的业务逻辑，包括核心统计、平台分布、门店排行等
"""

from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import and_, case, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.review import Review, ReplyAudit
from app.models.store import Store, StorePlatform
from app.models.user import User, UserStore

# 平台配色与图标映射
PLATFORM_CONFIG = {
    "meituan": {"color": "#FFD100", "icon": "meituan"},
    "dianping": {"color": "#FF6633", "icon": "dianping"},
    "douyin": {"color": "#161823", "icon": "douyin"},
    "taobao": {"color": "#FF5000", "icon": "taobao"},
    "jd": {"color": "#E4393C", "icon": "jd"},
}


async def _fetch_user_store_ids(db: AsyncSession, user: User) -> Optional[list]:
    """
    预查询用户可见的门店 ID 列表。
    返回 None 表示可见所有门店（管理员），返回空列表表示无门店。
    用 Python 列表替代 SQL 子查询，避免 SAWarning 笛卡尔积。
    """
    if user.role in ("SUPER_ADMIN", "HQ", "OPERATOR"):
        return None
    result = await db.execute(
        select(UserStore.store_id).where(UserStore.user_id == user.id)
    )
    return [row[0] for row in result.all()]


def _review_store_filter(store_ids: Optional[list]):
    """基于预查询的 ID 列表构建 Review.store_id 过滤条件"""
    if store_ids is None:
        return None
    if not store_ids:
        return False  # 匹配不到任何记录
    return Review.store_id.in_(store_ids)


def _store_filter(store_ids: Optional[list]):
    """基于预查询的 ID 列表构建 Store.id 过滤条件"""
    if store_ids is None:
        return None
    if not store_ids:
        return False
    return Store.id.in_(store_ids)


def _get_period_days(period: str) -> int:
    """将周期字符串转换为天数"""
    mapping = {"1d": 1, "7d": 7, "30d": 30, "90d": 90}
    return mapping.get(period, 30)


def _calc_trend(current: float, previous: float) -> float:
    """计算环比趋势百分比"""
    if previous == 0:
        return 100.0 if current > 0 else 0.0
    return round((current - previous) / previous * 100, 1)


def _get_period_range(period: str):
    """获取当期和上期的时间范围"""
    now = datetime.utcnow()
    days = _get_period_days(period)

    if period == "1d":
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return today_start, today_start - timedelta(days=1), today_start
    else:
        current_start = now - timedelta(days=days)
        previous_start = now - timedelta(days=days * 2)
        return current_start, previous_start, current_start


def _review_conditions(store_ids: Optional[list], extra=None):
    """构建 Review 基础查询条件（基于预查询 ID 列表，无子查询）"""
    conds = [Review.status == "normal"]
    sf = _review_store_filter(store_ids)
    if sf is not None:
        conds.append(sf)
    if extra:
        conds.extend(extra)
    return conds


async def get_core_stats(
    db: AsyncSession,
    user: User,
    period: str = "30d",
    store_ids: Optional[list] = None,
) -> dict:
    """
    获取核心统计数据 — 合并为 2 个查询（当期+上期）。
    """
    if store_ids is None:
        store_ids = await _fetch_user_store_ids(db, user)

    current_start, previous_start, period_end = _get_period_range(period)

    # ========== 当期统计 ==========
    current_base = _review_conditions(store_ids, [Review.created_at >= current_start])

    current_dedup = (
        select(
            Review.platform_review_id,
            func.avg(Review.rating).label("rating"),
            func.max(case((Review.sentiment == "positive", 1), else_=0)).label("is_positive"),
            func.max(case((Review.reply.isnot(None), 1), else_=0)).label("is_replied"),
            func.max(case((Review.ai_generated.is_(True), 1), else_=0)).label("is_ai"),
        )
        .where(and_(*current_base))
        .group_by(Review.platform_review_id)
    ).subquery()

    current_stats = (
        await db.execute(
            select(
                func.count().label("total"),
                func.avg(current_dedup.c.rating).label("avg_rating"),
                func.sum(current_dedup.c.is_positive).label("positive"),
                func.sum(current_dedup.c.is_replied).label("replied"),
                func.sum(current_dedup.c.is_ai).label("ai_replied"),
            )
            .select_from(current_dedup)
        )
    ).one()

    current_total = current_stats.total or 0
    current_avg = float(current_stats.avg_rating) if current_stats.avg_rating else 0.0
    current_positive = current_stats.positive or 0
    current_replied = current_stats.replied or 0
    current_ai_replied = current_stats.ai_replied or 0

    # ========== 上期统计 ==========
    previous_base = _review_conditions(store_ids, [
        Review.created_at >= previous_start,
        Review.created_at < period_end,
    ])
    previous_dedup = (
        select(
            Review.platform_review_id,
            func.avg(Review.rating).label("rating"),
            func.max(case((Review.sentiment == "positive", 1), else_=0)).label("is_positive"),
            func.max(case((Review.reply.isnot(None), 1), else_=0)).label("is_replied"),
            func.max(case((Review.ai_generated.is_(True), 1), else_=0)).label("is_ai"),
        )
        .where(and_(*previous_base))
        .group_by(Review.platform_review_id)
    ).subquery()

    previous_stats = (
        await db.execute(
            select(
                func.count().label("total"),
                func.avg(previous_dedup.c.rating).label("avg_rating"),
                func.sum(previous_dedup.c.is_positive).label("positive"),
                func.sum(previous_dedup.c.is_replied).label("replied"),
                func.sum(previous_dedup.c.is_ai).label("ai_replied"),
            )
            .select_from(previous_dedup)
        )
    ).one()

    previous_total = previous_stats.total or 0
    previous_avg = float(previous_stats.avg_rating) if previous_stats.avg_rating else 0.0
    previous_positive = previous_stats.positive or 0
    previous_replied = previous_stats.replied or 0

    # 计算比率
    current_positive_rate = round(current_positive / current_total * 100, 1) if current_total else 0.0
    previous_positive_rate = round(previous_positive / previous_total * 100, 1) if previous_total else 0.0
    current_reply_rate = round(current_replied / current_total * 100, 1) if current_total else 0.0
    previous_reply_rate = round(previous_replied / previous_total * 100, 1) if previous_total else 0.0
    current_ai_rate = round(current_ai_replied / current_total * 100, 1) if current_total else 0.0

    return {
        "total_reviews": current_total,
        "review_trend": _calc_trend(current_total, previous_total),
        "avg_rating": round(current_avg, 1),
        "rating_trend": _calc_trend(round(current_avg, 1), round(previous_avg, 1)),
        "positive_rate": current_positive_rate,
        "positive_trend": _calc_trend(current_positive_rate, previous_positive_rate),
        "ai_reply_rate": current_ai_rate,
        "reply_trend": _calc_trend(current_reply_rate, previous_reply_rate),
    }


async def get_platform_distribution(
    db: AsyncSession,
    user: User,
    period: str = "30d",
    store_ids: Optional[list] = None,
) -> list[dict]:
    """获取平台分布数据（按 platform_review_id 去重）"""
    if store_ids is None:
        store_ids = await _fetch_user_store_ids(db, user)

    days = _get_period_days(period)
    now = datetime.utcnow()
    period_start = now - timedelta(days=days)

    conditions = _review_conditions(store_ids, [Review.created_at >= period_start])

    dedup = (
        select(Review.platform_review_id, Review.platform)
        .where(and_(*conditions))
        .group_by(Review.platform_review_id, Review.platform)
    ).subquery()

    stmt = (
        select(dedup.c.platform, func.count().label("count"))
        .group_by(dedup.c.platform)
    )
    result = await db.execute(stmt)
    platform_data = result.all()

    total = sum(row.count for row in platform_data)
    distribution = []
    for row in platform_data:
        config = PLATFORM_CONFIG.get(row.platform, {"color": "#999999", "icon": ""})
        distribution.append({
            "platform": row.platform,
            "count": row.count,
            "percentage": round(row.count / total * 100, 1) if total else 0.0,
            "color": config["color"],
            "icon": config["icon"],
        })
    distribution.sort(key=lambda x: x["count"], reverse=True)
    return distribution


async def get_recent_reviews(
    db: AsyncSession,
    user: User,
    limit: int = 10,
    period: str = "30d",
    store_ids: Optional[list] = None,
) -> list[Review]:
    """获取最新评论列表（按 platform_review_id 去重，用 CTE）"""
    if store_ids is None:
        store_ids = await _fetch_user_store_ids(db, user)

    days = _get_period_days(period)
    now = datetime.utcnow()
    period_start = now - timedelta(days=days)

    conditions = _review_conditions(store_ids, [Review.created_at >= period_start])
    where_clause = and_(*conditions)

    latest_cte = (
        select(
            Review.platform_review_id,
            func.max(Review.created_at).label("max_time"),
        )
        .where(where_clause)
        .group_by(Review.platform_review_id)
    ).cte("latest_reviews")

    stmt = (
        select(Review)
        .options(joinedload(Review.store))
        .join(
            latest_cte,
            and_(
                Review.platform_review_id == latest_cte.c.platform_review_id,
                Review.created_at == latest_cte.c.max_time,
            ),
        )
        .order_by(Review.created_at.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_store_rankings(
    db: AsyncSession,
    user: User,
    limit: int = 10,
    period: str = "30d",
    store_ids: Optional[list] = None,
) -> list[dict]:
    """获取门店排行榜（用子查询预聚合 Review 数据）"""
    if store_ids is None:
        store_ids = await _fetch_user_store_ids(db, user)

    days = _get_period_days(period)
    now = datetime.utcnow()
    period_start = now - timedelta(days=days)

    store_conditions = [Store.status == "active"]
    sf = _store_filter(store_ids)
    if sf is not None:
        store_conditions.append(sf)
    store_where = and_(*store_conditions)

    review_sub = (
        select(
            Review.store_id,
            func.count(func.distinct(Review.platform_review_id)).label("review_count"),
            func.avg(Review.rating).label("avg_rating"),
        )
        .where(and_(Review.status == "normal", Review.created_at >= period_start))
        .group_by(Review.store_id)
    ).subquery()

    stmt = (
        select(
            Store.id,
            Store.name,
            Store.health_score,
            func.coalesce(review_sub.c.review_count, 0).label("review_count"),
            review_sub.c.avg_rating,
        )
        .outerjoin(review_sub, Store.id == review_sub.c.store_id)
        .where(store_where)
        .order_by(review_sub.c.avg_rating.desc().nullslast())
        .limit(limit)
    )
    result = await db.execute(stmt)
    rows = result.all()

    rankings = []
    for row in rows:
        avg_rating = round(float(row.avg_rating), 1) if row.avg_rating else 0.0
        health_score = row.health_score or 0.0
        health = "good" if health_score >= 80 else ("warning" if health_score >= 60 else "danger")
        rankings.append({
            "name": row.name,
            "score": avg_rating,
            "reviews": row.review_count,
            "trend": 0.0,
            "health": health,
            "health_score": health_score,
        })
    return rankings


async def get_health_status(
    db: AsyncSession,
    user: User,
    store_ids: Optional[list] = None,
) -> list[dict]:
    """获取数据源健康状态"""
    if store_ids is None:
        store_ids = await _fetch_user_store_ids(db, user)

    sf = _store_filter(store_ids)
    store_where = sf if sf is not None else True

    stmt = (
        select(
            StorePlatform.platform,
            func.max(StorePlatform.last_sync_at).label("last_sync"),
            func.count(func.distinct(StorePlatform.store_id)).label("store_count"),
        )
        .join(Store, StorePlatform.store_id == Store.id)
        .where(store_where)
        .group_by(StorePlatform.platform)
    )
    result = await db.execute(stmt)
    platform_data = result.all()

    now = datetime.utcnow()
    health_list = []
    for row in platform_data:
        last_sync = row.last_sync
        if last_sync:
            hours = (now - last_sync).total_seconds() / 3600
            status = "normal" if hours < 24 else ("warning" if hours < 48 else "error")
            sync_time = last_sync.isoformat()
        else:
            status = "error"
            sync_time = None
        health_list.append({"platform": row.platform, "status": status, "time": sync_time})

    existing = {item["platform"] for item in health_list}
    for p in PLATFORM_CONFIG:
        if p not in existing:
            health_list.append({"platform": p, "status": "error", "time": None})

    return health_list


async def get_alerts(
    db: AsyncSession,
    user: User,
    store_ids: Optional[list] = None,
) -> list[dict]:
    """获取异常警告列表"""
    if store_ids is None:
        store_ids = await _fetch_user_store_ids(db, user)

    alerts = []
    base_conds = _review_conditions(store_ids)
    where_clause = and_(*base_conds)
    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)

    # 高风险评论
    high_risk_sub = (
        select(Review.platform_review_id)
        .where(and_(where_clause, Review.risk_level == "high"))
        .group_by(Review.platform_review_id)
    ).subquery()
    high_risk_count = (
        await db.execute(select(func.count()).select_from(high_risk_sub))
    ).scalar() or 0
    if high_risk_count > 0:
        alerts.append({
            "id": "high_risk_reviews", "type": "risk",
            "title": "高风险评论预警",
            "description": f"当前有 {high_risk_count} 条高风险评论需要处理",
            "severity": "high", "timestamp": now.isoformat(),
        })

    # 未回复差评
    unanswered_sub = (
        select(Review.platform_review_id)
        .where(and_(
            where_clause,
            Review.sentiment == "negative",
            Review.reply.is_(None),
            Review.created_at >= week_ago,
        ))
        .group_by(Review.platform_review_id)
    ).subquery()
    unanswered_count = (
        await db.execute(select(func.count()).select_from(unanswered_sub))
    ).scalar() or 0
    if unanswered_count > 0:
        alerts.append({
            "id": "unanswered_negative", "type": "reply",
            "title": "差评未回复提醒",
            "description": f"近7天有 {unanswered_count} 条差评尚未回复",
            "severity": "medium", "timestamp": now.isoformat(),
        })

    # 待审核 AI 回复
    pending_count = (
        await db.execute(
            select(func.count()).select_from(ReplyAudit).where(ReplyAudit.status == "pending")
        )
    ).scalar() or 0
    if pending_count > 0:
        alerts.append({
            "id": "pending_ai_replies", "type": "audit",
            "title": "AI 回复待审核",
            "description": f"当前有 {pending_count} 条 AI 回复草稿待审核",
            "severity": "low", "timestamp": now.isoformat(),
        })

    # 评分下降
    recent_avg = (
        await db.execute(
            select(func.avg(Review.rating)).where(and_(where_clause, Review.created_at >= week_ago))
        )
    ).scalar() or 0.0
    prev_avg = (
        await db.execute(
            select(func.avg(Review.rating)).where(
                and_(where_clause, Review.created_at >= week_ago - timedelta(days=7), Review.created_at < week_ago)
            )
        )
    ).scalar() or 0.0
    if prev_avg > 0 and recent_avg < prev_avg * 0.9:
        alerts.append({
            "id": "rating_decline", "type": "trend",
            "title": "评分下降预警",
            "description": f"近7天平均评分 {round(float(recent_avg), 1)}，较前7天下降 {round((1 - recent_avg / prev_avg) * 100, 1)}%",
            "severity": "medium", "timestamp": now.isoformat(),
        })

    return alerts


async def get_store_health(
    db: AsyncSession,
    user: User,
    store_ids: Optional[list] = None,
) -> list[dict]:
    """获取门店健康值（一条 SQL 同时算 review_count/avg_rating/replied_count）"""
    if store_ids is None:
        store_ids = await _fetch_user_store_ids(db, user)

    store_conditions = [Store.status == "active"]
    sf = _store_filter(store_ids)
    if sf is not None:
        store_conditions.append(sf)
    store_where = and_(*store_conditions)

    review_sub = (
        select(
            Review.store_id,
            func.count(Review.platform_review_id).label("review_count"),
            func.avg(Review.rating).label("avg_rating"),
            func.sum(case((Review.reply.isnot(None), 1), else_=0)).label("replied_count"),
        )
        .where(Review.status == "normal")
        .group_by(Review.store_id)
    ).subquery()

    stmt = (
        select(
            Store.id,
            Store.name,
            Store.health_score,
            func.coalesce(review_sub.c.review_count, 0).label("review_count"),
            func.coalesce(review_sub.c.avg_rating, 0).label("avg_rating"),
            func.coalesce(review_sub.c.replied_count, 0).label("replied_count"),
        )
        .outerjoin(review_sub, Store.id == review_sub.c.store_id)
        .where(store_where)
        .order_by(Store.health_score.desc().nullslast())
    )
    result = await db.execute(stmt)
    rows = result.all()

    health_list = []
    for row in rows:
        rc = row.review_count
        reply_rate = round(row.replied_count / rc * 100, 1) if rc else 0.0
        health_score = row.health_score or 0.0
        health_list.append({
            "store_id": str(row.id),
            "store_name": row.name,
            "health_score": health_score,
            "review_count": rc,
            "avg_rating": round(float(row.avg_rating), 1) if row.avg_rating else 0.0,
            "reply_rate": reply_rate,
            "trend": 0.0,
        })
    return health_list


async def get_dashboard_overview(
    db: AsyncSession,
    user: User,
    period: str = "30d",
) -> dict:
    """
    聚合接口：一次性返回 Dashboard 所需的所有数据。
    预查询 store_ids 一次，传给所有子函数，避免重复查询和子查询笛卡尔积。
    """
    import asyncio

    # 预查询一次 store_ids，传给所有子函数
    store_ids = await _fetch_user_store_ids(db, user)

    (
        core_stats,
        platform_data,
        recent_reviews,
        store_rankings,
        health_status,
        store_health,
        alerts,
    ) = await asyncio.gather(
        get_core_stats(db, user, period, store_ids),
        get_platform_distribution(db, user, period, store_ids),
        get_recent_reviews(db, user, 5, period, store_ids),
        get_store_rankings(db, user, 5, period, store_ids),
        get_health_status(db, user, store_ids),
        get_store_health(db, user, store_ids),
        get_alerts(db, user, store_ids),
    )

    return {
        "core_stats": core_stats,
        "platform_data": platform_data,
        "recent_reviews": recent_reviews,
        "store_rankings": store_rankings,
        "health_status": health_status,
        "store_health": store_health,
        "alerts": alerts,
    }

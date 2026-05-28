"""
Dashboard 服务模块
处理仪表盘相关的业务逻辑，包括核心统计、平台分布、门店排行等
"""

from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.review import Review
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


def _build_store_filter(user: User) -> Optional:
    """
    根据用户角色构建门店可见性过滤条件。
    - HQ / OPERATOR：可见所有门店
    - STORE：仅可见关联门店
    """
    if user.role in ("HQ", "OPERATOR"):
        return None

    return Store.id.in_(
        select(UserStore.store_id).where(UserStore.user_id == user.id)
    )


def _get_period_days(period: str) -> int:
    """将周期字符串转换为天数"""
    mapping = {"1d": 1, "7d": 7, "30d": 30, "90d": 90}
    return mapping.get(period, 30)


def _calc_trend(current: float, previous: float) -> float:
    """
    计算环比趋势百分比

    Args:
        current: 当前值
        previous: 上期值

    Returns:
        float: 趋势百分比（正数表示增长）
    """
    if previous == 0:
        return 100.0 if current > 0 else 0.0
    return round((current - previous) / previous * 100, 1)


async def get_core_stats(
    db: AsyncSession,
    user: User,
    period: str = "30d",
) -> dict:
    """
    获取核心统计数据

    Args:
        db: 数据库会话
        user: 当前用户
        period: 统计周期 (7d/30d/90d)

    Returns:
        dict: 核心统计数据
    """
    days = _get_period_days(period)
    now = datetime.utcnow()

    if period == "1d":
        # 按自然天计算：current_start = 今天 UTC 00:00:00
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        current_start = today_start
        previous_start = today_start - timedelta(days=1)
        # 昨天的范围是 [previous_start, current_start)
    else:
        current_start = now - timedelta(days=days)
        previous_start = now - timedelta(days=days * 2)

    # 构建基础条件
    base_conditions = [Review.status == "normal"]
    store_filter = _build_store_filter(user)
    if store_filter is not None:
        base_conditions.append(store_filter)

    # 当期统计
    current_conditions = base_conditions + [Review.created_at >= current_start]
    current_where = and_(*current_conditions)

    # 上期统计
    previous_conditions = base_conditions + [
        Review.created_at >= previous_start,
        Review.created_at < current_start,
    ]
    previous_where = and_(*previous_conditions)

    # 当期评论总数
    current_total = (
        await db.execute(
            select(func.count()).select_from(Review).where(current_where)
        )
    ).scalar() or 0

    # 上期评论总数
    previous_total = (
        await db.execute(
            select(func.count()).select_from(Review).where(previous_where)
        )
    ).scalar() or 0

    # 当期平均评分
    current_avg = (
        await db.execute(select(func.avg(Review.rating)).where(current_where))
    ).scalar() or 0.0

    # 上期平均评分
    previous_avg = (
        await db.execute(select(func.avg(Review.rating)).where(previous_where))
    ).scalar() or 0.0

    # 当期正面率
    current_positive = (
        await db.execute(
            select(func.count())
            .select_from(Review)
            .where(and_(current_where, Review.sentiment == "positive"))
        )
    ).scalar() or 0

    # 上期正面率
    previous_positive = (
        await db.execute(
            select(func.count())
            .select_from(Review)
            .where(and_(previous_where, Review.sentiment == "positive"))
        )
    ).scalar() or 0

    # 当期回复率
    current_replied = (
        await db.execute(
            select(func.count())
            .select_from(Review)
            .where(and_(current_where, Review.reply.isnot(None)))
        )
    ).scalar() or 0

    # 上期回复率
    previous_replied = (
        await db.execute(
            select(func.count())
            .select_from(Review)
            .where(and_(previous_where, Review.reply.isnot(None)))
        )
    ).scalar() or 0

    # 当期 AI 回复率
    current_ai_replied = (
        await db.execute(
            select(func.count())
            .select_from(Review)
            .where(and_(current_where, Review.ai_generated.is_(True)))
        )
    ).scalar() or 0

    # 上期 AI 回复率
    previous_ai_replied = (
        await db.execute(
            select(func.count())
            .select_from(Review)
            .where(and_(previous_where, Review.ai_generated.is_(True)))
        )
    ).scalar() or 0

    # 计算趋势
    review_trend = _calc_trend(current_total, previous_total)
    rating_trend = _calc_trend(round(float(current_avg), 1), round(float(previous_avg), 1))

    current_positive_rate = (
        round(current_positive / current_total * 100, 1) if current_total else 0.0
    )
    previous_positive_rate = (
        round(previous_positive / previous_total * 100, 1) if previous_total else 0.0
    )
    positive_trend = _calc_trend(current_positive_rate, previous_positive_rate)

    current_reply_rate = (
        round(current_replied / current_total * 100, 1) if current_total else 0.0
    )
    previous_reply_rate = (
        round(previous_replied / previous_total * 100, 1) if previous_total else 0.0
    )
    reply_trend = _calc_trend(current_reply_rate, previous_reply_rate)

    current_ai_rate = (
        round(current_ai_replied / current_total * 100, 1) if current_total else 0.0
    )
    previous_ai_rate = (
        round(previous_ai_replied / previous_total * 100, 1) if previous_total else 0.0
    )
    ai_reply_rate = current_ai_rate

    return {
        "total_reviews": current_total,
        "review_trend": review_trend,
        "avg_rating": round(float(current_avg), 1),
        "rating_trend": rating_trend,
        "positive_rate": current_positive_rate,
        "positive_trend": positive_trend,
        "ai_reply_rate": ai_reply_rate,
        "reply_trend": reply_trend,
    }


async def get_platform_distribution(
    db: AsyncSession,
    user: User,
    period: str = "30d",
) -> list[dict]:
    """
    获取平台分布数据

    Args:
        db: 数据库会话
        user: 当前用户
        period: 统计周期 (1d/7d/30d/90d)

    Returns:
        list[dict]: 各平台评论数量和占比
    """
    days = _get_period_days(period)
    now = datetime.utcnow()
    period_start = now - timedelta(days=days)

    conditions = [Review.status == "normal", Review.created_at >= period_start]
    store_filter = _build_store_filter(user)
    if store_filter is not None:
        conditions.append(store_filter)

    where_clause = and_(*conditions)

    # 按平台统计
    stmt = (
        select(Review.platform, func.count().label("count"))
        .where(where_clause)
        .group_by(Review.platform)
    )
    result = await db.execute(stmt)
    platform_data = result.all()

    total = sum(row.count for row in platform_data)

    distribution = []
    for row in platform_data:
        config = PLATFORM_CONFIG.get(row.platform, {"color": "#999999", "icon": ""})
        distribution.append(
            {
                "platform": row.platform,
                "count": row.count,
                "percentage": round(row.count / total * 100, 1) if total else 0.0,
                "color": config["color"],
                "icon": config["icon"],
            }
        )

    # 按数量降序排列
    distribution.sort(key=lambda x: x["count"], reverse=True)

    return distribution


async def get_recent_reviews(
    db: AsyncSession,
    user: User,
    limit: int = 10,
    period: str = "30d",
) -> list[Review]:
    """
    获取最新评论列表

    Args:
        db: 数据库会话
        user: 当前用户
        limit: 返回数量
        period: 统计周期 (1d/7d/30d/90d)

    Returns:
        list[Review]: 最新评论列表
    """
    days = _get_period_days(period)
    now = datetime.utcnow()
    period_start = now - timedelta(days=days)

    conditions = [Review.status == "normal", Review.created_at >= period_start]
    store_filter = _build_store_filter(user)
    if store_filter is not None:
        conditions.append(store_filter)

    where_clause = and_(*conditions)

    stmt = (
        select(Review)
        .options(joinedload(Review.store))
        .where(where_clause)
        .order_by(Review.created_at.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_store_rankings(
    db: AsyncSession,
    user: User,
    limit: int = 10,
) -> list[dict]:
    """
    获取门店排行榜

    Args:
        db: 数据库会话
        user: 当前用户
        limit: 返回数量

    Returns:
        list[dict]: 门店排行数据
    """
    # 基础条件
    store_conditions = [Store.status == "active"]
    store_filter = _build_store_filter(user)
    if store_filter is not None:
        store_conditions.append(store_filter)

    store_where = and_(*store_conditions)

    # 查询门店及其评论统计
    stmt = (
        select(
            Store.id,
            Store.name,
            Store.health_score,
            func.count(Review.id).label("review_count"),
            func.avg(Review.rating).label("avg_rating"),
        )
        .outerjoin(Review, and_(Review.store_id == Store.id, Review.status == "normal"))
        .where(store_where)
        .group_by(Store.id, Store.name, Store.health_score)
        .order_by(func.avg(Review.rating).desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    rows = result.all()

    rankings = []
    for idx, row in enumerate(rows):
        avg_rating = round(float(row.avg_rating), 1) if row.avg_rating else 0.0
        health_score = row.health_score or 0.0

        # 健康状态
        if health_score >= 80:
            health = "good"
        elif health_score >= 60:
            health = "warning"
        else:
            health = "danger"

        rankings.append(
            {
                "name": row.name,
                "score": avg_rating,
                "reviews": row.review_count,
                "trend": 0.0,  # TODO: 与上期对比计算趋势
                "health": health,
                "health_score": health_score,
            }
        )

    return rankings


async def get_health_status(
    db: AsyncSession,
    user: User,
) -> list[dict]:
    """
    获取数据源健康状态

    Args:
        db: 数据库会话
        user: 当前用户

    Returns:
        list[dict]: 各平台数据源健康状态
    """
    conditions = []
    store_filter = _build_store_filter(user)
    if store_filter is not None:
        conditions.append(store_filter)

    store_where = and_(*conditions) if conditions else True

    # 查询各平台的最后同步时间
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
            hours_since_sync = (now - last_sync).total_seconds() / 3600
            if hours_since_sync < 24:
                status = "normal"
            elif hours_since_sync < 48:
                status = "warning"
            else:
                status = "error"
            sync_time = last_sync.isoformat()
        else:
            status = "error"
            sync_time = None

        health_list.append(
            {
                "platform": row.platform,
                "status": status,
                "time": sync_time,
            }
        )

    # 确保所有平台都有记录
    existing_platforms = {item["platform"] for item in health_list}
    for platform in PLATFORM_CONFIG:
        if platform not in existing_platforms:
            health_list.append(
                {
                    "platform": platform,
                    "status": "error",
                    "time": None,
                }
            )

    return health_list


async def get_alerts(
    db: AsyncSession,
    user: User,
) -> list[dict]:
    """
    获取异常警告列表

    Args:
        db: 数据库会话
        user: 当前用户

    Returns:
        list[dict]: 异常警告列表
    """
    alerts = []
    conditions = [Review.status == "normal"]
    store_filter = _build_store_filter(user)
    if store_filter is not None:
        conditions.append(store_filter)
    where_clause = and_(*conditions)

    # 1. 检查高风险评论
    high_risk_stmt = (
        select(func.count())
        .select_from(Review)
        .where(and_(where_clause, Review.risk_level == "high"))
    )
    high_risk_count = (await db.execute(high_risk_stmt)).scalar() or 0
    if high_risk_count > 0:
        alerts.append(
            {
                "id": "high_risk_reviews",
                "type": "risk",
                "title": "高风险评论预警",
                "description": f"当前有 {high_risk_count} 条高风险评论需要处理",
                "severity": "high",
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

    # 2. 检查未回复的差评（最近7天）
    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)
    unanswered_negative_stmt = (
        select(func.count())
        .select_from(Review)
        .where(
            and_(
                where_clause,
                Review.sentiment == "negative",
                Review.reply.is_(None),
                Review.created_at >= week_ago,
            )
        )
    )
    unanswered_count = (await db.execute(unanswered_negative_stmt)).scalar() or 0
    if unanswered_count > 0:
        alerts.append(
            {
                "id": "unanswered_negative",
                "type": "reply",
                "title": "差评未回复提醒",
                "description": f"近7天有 {unanswered_count} 条差评尚未回复",
                "severity": "medium",
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

    # 3. 检查待审核的 AI 回复
    from app.models.review import ReplyAudit

    pending_audit_stmt = select(func.count()).select_from(ReplyAudit).where(
        ReplyAudit.status == "pending"
    )
    pending_count = (await db.execute(pending_audit_stmt)).scalar() or 0
    if pending_count > 0:
        alerts.append(
            {
                "id": "pending_ai_replies",
                "type": "audit",
                "title": "AI 回复待审核",
                "description": f"当前有 {pending_count} 条 AI 回复草稿待审核",
                "severity": "low",
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

    # 4. 检查评分下降趋势（近7天 vs 前7天）
    recent_avg_stmt = select(func.avg(Review.rating)).where(
        and_(where_clause, Review.created_at >= week_ago)
    )
    recent_avg = (await db.execute(recent_avg_stmt)).scalar() or 0.0

    prev_week_start = week_ago - timedelta(days=7)
    prev_avg_stmt = select(func.avg(Review.rating)).where(
        and_(where_clause, Review.created_at >= prev_week_start, Review.created_at < week_ago)
    )
    prev_avg = (await db.execute(prev_avg_stmt)).scalar() or 0.0

    if prev_avg > 0 and recent_avg < prev_avg * 0.9:
        alerts.append(
            {
                "id": "rating_decline",
                "type": "trend",
                "title": "评分下降预警",
                "description": f"近7天平均评分 {round(float(recent_avg), 1)}，较前7天下降 {round((1 - recent_avg / prev_avg) * 100, 1)}%",
                "severity": "medium",
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

    return alerts


async def get_store_health(
    db: AsyncSession,
    user: User,
) -> list[dict]:
    """
    获取门店健康值列表

    Args:
        db: 数据库会话
        user: 当前用户

    Returns:
        list[dict]: 门店健康值数据
    """
    # 基础条件
    store_conditions = [Store.status == "active"]
    store_filter = _build_store_filter(user)
    if store_filter is not None:
        store_conditions.append(store_filter)

    store_where = and_(*store_conditions)

    # 查询门店及其评论统计
    stmt = (
        select(
            Store.id,
            Store.name,
            Store.health_score,
            func.count(Review.id).label("review_count"),
            func.avg(Review.rating).label("avg_rating"),
            func.count().filter(Review.reply.isnot(None)).label("replied_count"),
        )
        .outerjoin(Review, and_(Review.store_id == Store.id, Review.status == "normal"))
        .where(store_where)
        .group_by(Store.id, Store.name, Store.health_score)
        .order_by(Store.health_score.desc().nullslast())
    )
    result = await db.execute(stmt)
    rows = result.all()

    health_list = []
    for row in rows:
        review_count = row.review_count
        avg_rating = round(float(row.avg_rating), 1) if row.avg_rating else 0.0
        replied_count = row.replied_count
        reply_rate = (
            round(replied_count / review_count * 100, 1) if review_count else 0.0
        )
        health_score = row.health_score or 0.0

        health_list.append(
            {
                "store_id": str(row.id),
                "store_name": row.name,
                "health_score": health_score,
                "review_count": review_count,
                "avg_rating": avg_rating,
                "reply_rate": reply_rate,
                "trend": 0.0,  # TODO: 与上期对比计算趋势
            }
        )

    return health_list

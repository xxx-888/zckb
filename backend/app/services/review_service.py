"""
评论服务模块
处理评论相关的业务逻辑，包括 CRUD、统计、相似评论、快速回复等
"""

from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy import and_, case, distinct, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.exceptions import BusinessException, NotFoundException
from app.models.review import ReplyAudit, Review
from app.models.user import User, UserStore


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


def _build_store_filter(store_ids: Optional[list]) -> Optional:
    """
    根据预查询的门店 ID 列表构建 Review.store_id 过滤条件。
    不再引用 Store 表，避免与 joinedload(Review.store) 产生笛卡尔积。
    """
    if store_ids is None:
        return None  # 管理员：不过滤
    if not store_ids:
        return False  # 无门店：匹配不到任何记录
    return Review.store_id.in_(store_ids)


async def get_reviews(
    db: AsyncSession,
    user: User,
    filters: dict,
) -> tuple[list[Review], int]:
    """
    获取评论列表（根据用户角色过滤可见评论）

    Args:
        db: 数据库会话
        user: 当前用户
        filters: 筛选参数字典

    Returns:
        tuple: (评论列表, 总数)
    """
    conditions = [Review.status == "normal"]

    # 角色过滤（预查询 store IDs，避免笛卡尔积）
    store_ids = await _fetch_user_store_ids(db, user)
    store_filter = _build_store_filter(store_ids)
    if store_filter is not None:
        conditions.append(store_filter)

    # 情感筛选
    if filters.get("sentiment"):
        conditions.append(Review.sentiment == filters["sentiment"])

    # 门店筛选
    if filters.get("store_id"):
        conditions.append(Review.store_id == filters["store_id"])

    # 平台筛选
    if filters.get("platform"):
        conditions.append(Review.platform == filters["platform"])

    # 评分范围
    if filters.get("rating_min") is not None:
        conditions.append(Review.rating >= filters["rating_min"])
    if filters.get("rating_max") is not None:
        conditions.append(Review.rating <= filters["rating_max"])

    # 是否有回复
    if filters.get("has_reply") is True:
        conditions.append(Review.reply.isnot(None))
    elif filters.get("has_reply") is False:
        conditions.append(Review.reply.is_(None))

    # 是否有图片
    if filters.get("has_image") is True:
        conditions.append(Review.images.isnot(None))
        conditions.append(func.array_length(Review.images, 1) > 0)
    elif filters.get("has_image") is False:
        conditions.append(
            or_(Review.images.is_(None), func.array_length(Review.images, 1) == 0)
        )

    # 关键词搜索
    if filters.get("keyword"):
        keyword = f"%{filters['keyword']}%"
        conditions.append(
            or_(
                Review.content.ilike(keyword),
                Review.user_name.ilike(keyword),
            )
        )

    # 日期范围（按平台评论时间筛选，无评论时间则按入库时间）
    if filters.get("start_date"):
        try:
            start = datetime.strptime(filters["start_date"], "%Y-%m-%d")
            conditions.append(
                or_(Review.platform_created_at >= start, and_(Review.platform_created_at.is_(None), Review.created_at >= start))
            )
        except ValueError:
            pass
    if filters.get("end_date"):
        try:
            end = datetime.strptime(filters["end_date"], "%Y-%m-%d") + timedelta(days=1)
            conditions.append(
                or_(Review.platform_created_at < end, and_(Review.platform_created_at.is_(None), Review.created_at < end))
            )
        except ValueError:
            pass

    where_clause = and_(*conditions)

    # 查询总数（使用 distinct 避免笛卡尔积）
    count_stmt = select(func.count(distinct(Review.id))).select_from(Review).where(where_clause)
    total = (await db.execute(count_stmt)).scalar() or 0

    # 分页查询
    page = filters.get("page", 1)
    page_size = filters.get("page_size", 20)
    offset = (page - 1) * page_size

    stmt = (
        select(Review)
        .options(joinedload(Review.store))
        .where(where_clause)
        .order_by(Review.platform_created_at.desc().nullslast(), Review.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    # 使用 unique() 去除 JOIN 导致的重复行（必须在 scalars() 之后调用）
    reviews = result.scalars().unique().all()

    return reviews, total


async def get_review_by_id(
    db: AsyncSession,
    review_id: UUID,
) -> Review:
    """
    根据 ID 获取评论

    Args:
        db: 数据库会话
        review_id: 评论 ID

    Returns:
        Review: 评论对象

    Raises:
        NotFoundException: 评论不存在
    """
    result = await db.execute(select(Review).options(joinedload(Review.store)).where(Review.id == review_id))
    review = result.scalar_one_or_none()

    if not review:
        raise NotFoundException("评论不存在")

    return review


async def create_review(
    db: AsyncSession,
    review_data: dict,
) -> Review:
    """
    创建评论（爬虫入库用）

    Args:
        db: 数据库会话
        review_data: 评论数据字典

    Returns:
        Review: 创建成功的评论对象

    Raises:
        BusinessException: 平台评论 ID 重复
    """
    # 检查平台评论 ID 是否已存在
    stmt = select(Review).where(
        and_(
            Review.platform == review_data["platform"],
            Review.platform_review_id == review_data["platform_review_id"],
        )
    )
    existing = (await db.execute(stmt)).scalar_one_or_none()
    if existing:
        raise BusinessException("该平台评论已存在，请勿重复导入")

    review = Review(**review_data)
    db.add(review)
    await db.flush()
    await db.refresh(review)

    return review


async def update_review(
    db: AsyncSession,
    review_id: UUID,
    data: dict,
) -> Review:
    """
    更新评论

    Args:
        db: 数据库会话
        review_id: 评论 ID
        data: 更新数据字典

    Returns:
        Review: 更新后的评论对象

    Raises:
        NotFoundException: 评论不存在
    """
    review = await get_review_by_id(db, review_id)

    for key, value in data.items():
        if value is not None and hasattr(review, key):
            setattr(review, key, value)

    # 如果设置了回复内容，同时更新回复时间
    if data.get("reply") is not None:
        review.reply_time = datetime.utcnow()

    await db.flush()
    await db.refresh(review)

    return review


async def delete_review(
    db: AsyncSession,
    review_id: UUID,
) -> None:
    """
    删除评论（软删除，将状态设为 deleted）

    Args:
        db: 数据库会话
        review_id: 评论 ID

    Raises:
        NotFoundException: 评论不存在
    """
    review = await get_review_by_id(db, review_id)
    review.status = "deleted"
    await db.flush()


async def batch_delete_reviews(
    db: AsyncSession,
    review_ids: list[UUID],
) -> int:
    """
    批量删除评论（软删除）

    Args:
        db: 数据库会话
        review_ids: 评论 ID 列表

    Returns:
        int: 实际删除的数量
    """
    stmt = (
        select(Review)
        .where(
            and_(
                Review.id.in_(review_ids),
                Review.status == "normal",
            )
        )
    )
    result = await db.execute(stmt)
    reviews = list(result.scalars().all())

    count = 0
    for review in reviews:
        review.status = "deleted"
        count += 1

    await db.flush()
    return count


async def get_similar_reviews(
    db: AsyncSession,
    review_id: UUID,
    limit: int = 5,
) -> list[Review]:
    """
    获取相似评论（基于相同门店和情感，按评分相近排序）

    Args:
        db: 数据库会话
        review_id: 评论 ID
        limit: 返回数量

    Returns:
        list[Review]: 相似评论列表

    Raises:
        NotFoundException: 评论不存在
    """
    review = await get_review_by_id(db, review_id)

    stmt = (
        select(Review)
        .where(
            and_(
                Review.id != review_id,
                Review.store_id == review.store_id,
                Review.sentiment == review.sentiment,
                Review.status == "normal",
            )
        )
        .order_by(
            func.abs(Review.rating - review.rating).asc(),
            Review.created_at.desc(),
        )
        .limit(limit)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def quick_reply(
    db: AsyncSession,
    review_id: UUID,
    reply_content: str,
    user_id: UUID,
) -> Review:
    """
    快速回复评论

    Args:
        db: 数据库会话
        review_id: 评论 ID
        reply_content: 回复内容
        user_id: 操作用户 ID

    Returns:
        Review: 更新后的评论对象

    Raises:
        NotFoundException: 评论不存在
    """
    review = await get_review_by_id(db, review_id)

    review.reply = reply_content
    review.reply_time = datetime.utcnow()
    review.ai_generated = False

    await db.flush()
    await db.refresh(review)

    return review


async def approve_reply(
    db: AsyncSession,
    review_id: UUID,
    user_id: UUID,
) -> ReplyAudit:
    """
    移动端用户发送 AI 回复 → 创建待审核记录（pending）
    后台管理员在回复审核页面通过后才真正发布

    如果该评论已有 pending 审核记录，更新内容即可，不重复创建。
    如果审核记录已 approved/sent（说明已经回复过），直接返回。

    Args:
        db: 数据库会话
        review_id: 评论 ID
        user_id: 提交用户 ID

    Returns:
        ReplyAudit: 审核记录

    Raises:
        NotFoundException: 评论不存在
        BusinessException: 该评论没有可提交的 AI 回复
    """
    review = await get_review_by_id(db, review_id)

    # 查找是否已有审核记录
    from sqlalchemy import select as sa_select
    stmt = sa_select(ReplyAudit).where(ReplyAudit.review_id == review_id)
    result = await db.execute(stmt)
    existing_audit = result.scalar_one_or_none()

    # 获取待提交的回复内容（优先用户编辑后的草稿，其次 AI 草稿，最后已有正式回复）
    reply_content = review.ai_reply_draft or (existing_audit.ai_reply_content if existing_audit else None)

    if not reply_content:
        raise BusinessException("该评论没有可提交的回复内容")

    if existing_audit:
        # 已有审核记录：更新内容，重置为 pending（允许重新提交）
        if existing_audit.status in ("approved", "sent"):
            # 已经正式回复过了，不允许重新提交
            return existing_audit
        existing_audit.ai_reply_content = reply_content
        existing_audit.status = "pending"
        existing_audit.reject_reason = None
        existing_audit.risk_level = _calculate_risk_level(review)
        await db.flush()
        await db.refresh(existing_audit)
        return existing_audit

    # 创建新的审核记录（状态为 pending，等待后台管理员审核）
    audit = ReplyAudit(
        review_id=review_id,
        store_id=review.store_id,
        ai_reply_content=reply_content,
        status="pending",
        risk_level=_calculate_risk_level(review),
        scores={
            "realism": 85,
            "empathy": 90,
            "concreteness": 80,
            "consistency": 85,
        },
    )
    db.add(audit)

    # 将 AI 草稿清空（已提交审核）
    review.ai_reply_draft = None

    await db.flush()
    await db.refresh(audit)

    return audit


def _calculate_risk_level(review) -> str:
    """根据评分计算风险等级"""
    if review.rating <= 2:
        return "high"
    elif review.rating == 3:
        return "medium"
    else:
        return "low"


async def get_review_stats(
    db: AsyncSession,
    user: User,
    period: str = "30d",
) -> dict:
    """
    获取评论统计数据

    Args:
        db: 数据库会话
        user: 当前用户
        period: 统计周期 (7d/30d/90d/all)

    Returns:
        dict: 统计数据
    """
    # 计算时间范围
    now = datetime.utcnow()
    if period == "7d":
        start_date = now - timedelta(days=7)
    elif period == "30d":
        start_date = now - timedelta(days=30)
    elif period == "90d":
        start_date = now - timedelta(days=90)
    else:
        start_date = None

    conditions = [Review.status == "normal"]

    # 角色过滤（预查询 store IDs，避免笛卡尔积）
    store_ids = await _fetch_user_store_ids(db, user)
    store_filter = _build_store_filter(store_ids)
    if store_filter is not None:
        conditions.append(store_filter)

    # 时间过滤
    if start_date:
        conditions.append(Review.created_at >= start_date)

    where_clause = and_(*conditions)

    # 总评论数
    total_stmt = select(func.count()).select_from(Review).where(where_clause)
    total_reviews = (await db.execute(total_stmt)).scalar() or 0

    # 情感分布
    sentiment_stmt = (
        select(Review.sentiment, func.count())
        .where(where_clause)
        .group_by(Review.sentiment)
    )
    sentiment_result = await db.execute(sentiment_stmt)
    sentiment_map = dict(sentiment_result.all())

    positive_count = sentiment_map.get("positive", 0)
    negative_count = sentiment_map.get("negative", 0)
    neutral_count = sentiment_map.get("neutral", 0)

    # 平均评分
    avg_stmt = select(func.avg(Review.rating)).where(where_clause)
    avg_rating = (await db.execute(avg_stmt)).scalar() or 0.0
    avg_rating = round(float(avg_rating), 1)

    # 回复率
    reply_rate_stmt = select(
        func.count().filter(Review.reply.isnot(None)),
        func.count(),
    ).where(where_clause)
    replied, total_for_rate = (await db.execute(reply_rate_stmt)).one()
    reply_rate = round(replied / total_for_rate * 100, 1) if total_for_rate else 0.0

    # AI 回复率
    ai_reply_stmt = select(
        func.count().filter(Review.ai_generated.is_(True)),
        func.count().filter(Review.reply.isnot(None)),
    ).where(where_clause)
    ai_replied, total_replied = (await db.execute(ai_reply_stmt)).one()
    ai_reply_rate = (
        round(ai_replied / total_replied * 100, 1) if total_replied else 0.0
    )

    return {
        "total_reviews": total_reviews,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "neutral_count": neutral_count,
        "avg_rating": avg_rating,
        "reply_rate": reply_rate,
        "ai_reply_rate": ai_reply_rate,
        "period": period,
    }


async def like_review(
    db: AsyncSession,
    review_id: UUID,
) -> Review:
    """
    赞同评论

    Args:
        db: 数据库会话
        review_id: 评论 ID

    Returns:
        Review: 评论对象

    Raises:
        NotFoundException: 评论不存在
    """
    review = await get_review_by_id(db, review_id)
    # TODO: 实现点赞逻辑，可扩展 likes 字段或创建点赞表
    await db.refresh(review)
    return review

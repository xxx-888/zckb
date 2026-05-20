"""
订阅服务模块
处理订阅计划查询、用户订阅、升级等业务逻辑
"""

from datetime import date, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException, NotFoundException
from app.models.subscription import SubscriptionPlan, UserSubscription


async def get_plans(db: AsyncSession) -> list[SubscriptionPlan]:
    """
    获取所有启用的订阅计划

    Args:
        db: 数据库会话

    Returns:
        list[SubscriptionPlan]: 启用的订阅计划列表
    """
    result = await db.execute(
        select(SubscriptionPlan).where(SubscriptionPlan.is_active == True)  # noqa: E712
    )
    return list(result.scalars().all())


async def get_current_subscription(
    db: AsyncSession,
    user_id: UUID,
) -> UserSubscription | None:
    """
    获取用户当前有效订阅

    Args:
        db: 数据库会话
        user_id: 用户ID

    Returns:
        UserSubscription | None: 当前有效订阅，无则返回 None
    """
    result = await db.execute(
        select(UserSubscription).where(
            UserSubscription.user_id == user_id,
            UserSubscription.status.in_(["trial", "active"]),
        )
    )
    return result.scalar_one_or_none()


async def subscribe_plan(
    db: AsyncSession,
    user_id: UUID,
    plan_id: UUID,
) -> UserSubscription:
    """
    用户订阅新计划

    Args:
        db: 数据库会话
        user_id: 用户ID
        plan_id: 套餐ID

    Returns:
        UserSubscription: 创建的订阅记录

    Raises:
        BusinessException: 已有有效订阅或套餐不存在
    """
    # 检查是否已有有效订阅
    existing = await get_current_subscription(db, user_id)
    if existing:
        raise BusinessException("您已有有效订阅，请先取消当前订阅或直接升级")

    # 查询目标套餐
    result = await db.execute(
        select(SubscriptionPlan).where(SubscriptionPlan.id == plan_id)
    )
    plan = result.scalar_one_or_none()
    if not plan:
        raise NotFoundException("订阅套餐不存在")
    if not plan.is_active:
        raise BusinessException("该订阅套餐已下架")

    # 创建订阅（默认30天试用期）
    today = date.today()
    subscription = UserSubscription(
        user_id=user_id,
        plan_id=plan_id,
        status="trial",
        start_date=today,
        end_date=today + timedelta(days=30),
        auto_renew=True,
    )
    db.add(subscription)
    await db.flush()
    await db.refresh(subscription)

    return subscription


async def upgrade_plan(
    db: AsyncSession,
    user_id: UUID,
    plan_id: UUID,
) -> UserSubscription:
    """
    升级用户订阅计划

    Args:
        db: 数据库会话
        user_id: 用户ID
        plan_id: 目标套餐ID

    Returns:
        UserSubscription: 更新后的订阅记录

    Raises:
        BusinessException: 无有效订阅或套餐不存在
    """
    # 获取当前订阅
    current = await get_current_subscription(db, user_id)
    if not current:
        raise BusinessException("您当前没有有效订阅，请先订阅")

    # 不能降级到相同或更低的套餐
    if current.plan_id == plan_id:
        raise BusinessException("您已订阅该套餐")

    # 查询目标套餐
    result = await db.execute(
        select(SubscriptionPlan).where(SubscriptionPlan.id == plan_id)
    )
    plan = result.scalar_one_or_none()
    if not plan:
        raise NotFoundException("订阅套餐不存在")
    if not plan.is_active:
        raise BusinessException("该订阅套餐已下架")

    # 更新订阅
    current.plan_id = plan_id
    current.status = "active"
    current.end_date = date.today() + timedelta(days=365)
    await db.flush()
    await db.refresh(current)

    return current


async def cancel_subscription(
    db: AsyncSession,
    user_id: UUID,
) -> UserSubscription:
    """
    取消用户订阅

    Args:
        db: 数据库会话
        user_id: 用户ID

    Returns:
        UserSubscription: 更新后的订阅记录

    Raises:
        BusinessException: 无有效订阅
    """
    current = await get_current_subscription(db, user_id)
    if not current:
        raise BusinessException("您当前没有有效订阅")

    current.status = "cancelled"
    current.auto_renew = False
    await db.flush()
    await db.refresh(current)

    return current


async def check_subscription_limit(
    db: AsyncSession,
    user_id: UUID,
    feature: str,
) -> bool:
    """
    检查用户订阅是否达到功能限制

    Args:
        db: 数据库会话
        user_id: 用户ID
        feature: 功能名称 (stores / reviews)

    Returns:
        bool: True 表示未达限制，False 表示已达限制
    """
    subscription = await get_current_subscription(db, user_id)
    if not subscription:
        return False

    plan = subscription.plan

    if feature == "stores":
        from app.models.store import Store
        from app.models.user import UserStore

        # 查询用户关联的门店数
        result = await db.execute(
            select(UserStore).where(UserStore.user_id == user_id)
        )
        store_count = len(list(result.scalars().all()))
        return store_count < plan.max_stores

    if feature == "reviews":
        from sqlalchemy import func

        from app.models.review import Review
        from app.models.store import Store
        from app.models.user import UserStore

        if not plan.max_reviews_per_month:
            return True

        # 查询用户关联的所有门店
        result = await db.execute(
            select(UserStore.store_id).where(UserStore.user_id == user_id)
        )
        store_ids = list(result.scalars().all())
        if not store_ids:
            return True

        # 查询本月评论数
        from datetime import datetime

        now = datetime.now()
        month_start = datetime(now.year, now.month, 1)

        result = await db.execute(
            select(func.count(Review.id)).where(
                Review.store_id.in_(store_ids),
                Review.created_at >= month_start,
            )
        )
        review_count = result.scalar() or 0
        return review_count < plan.max_reviews_per_month

    return True

"""
订阅服务模块
处理订阅计划查询、用户订阅、升级等业务逻辑
"""

from datetime import date, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import BusinessException, NotFoundException
from app.models.subscription import SubscriptionPlan, UserSubscription, PaymentRecord


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
        select(UserSubscription)
        .options(selectinload(UserSubscription.plan))
        .where(
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
    
    # 重新查询以预加载 plan 关系
    result = await db.execute(
        select(UserSubscription)
        .options(selectinload(UserSubscription.plan))
        .where(UserSubscription.id == subscription.id)
    )
    return result.scalar_one()


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
    
    # 重新查询以预加载 plan 关系
    result = await db.execute(
        select(UserSubscription)
        .options(selectinload(UserSubscription.plan))
        .where(UserSubscription.id == current.id)
    )
    return result.scalar_one()


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
    
    # 重新查询以预加载 plan 关系
    result = await db.execute(
        select(UserSubscription)
        .options(selectinload(UserSubscription.plan))
        .where(UserSubscription.id == current.id)
    )
    return result.scalar_one()


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


# ==================== 管理员套餐管理 ====================


async def get_all_plans(
    db: AsyncSession,
    include_inactive: bool = True,
) -> list[SubscriptionPlan]:
    """
    获取所有订阅套餐（管理员用）

    Args:
        db: 数据库会话
        include_inactive: 是否包含未启用的套餐

    Returns:
        list[SubscriptionPlan]: 套餐列表
    """
    query = select(SubscriptionPlan)
    if not include_inactive:
        query = query.where(SubscriptionPlan.is_active == True)
    query = query.order_by(SubscriptionPlan.price_yearly.asc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def create_plan(
    db: AsyncSession,
    data: "SubscriptionPlanCreateRequest",
) -> SubscriptionPlan:
    """
    创建订阅套餐（管理员用）

    Args:
        db: 数据库会话
        data: 创建请求数据

    Returns:
        SubscriptionPlan: 创建的套餐对象
    """
    from app.schemas.subscription import SubscriptionPlanCreateRequest
    if isinstance(data, dict):
        data = SubscriptionPlanCreateRequest(**data)

    plan = SubscriptionPlan(
        name=data.name,
        price_monthly=data.price_monthly,
        price_yearly=data.price_yearly,
        features=data.features,
        max_stores=data.max_stores,
        max_reviews_per_month=data.max_reviews_per_month,
        is_active=data.is_active,
    )
    db.add(plan)
    await db.flush()
    await db.refresh(plan)
    return plan


async def update_plan(
    db: AsyncSession,
    plan_id: UUID,
    data: "SubscriptionPlanUpdateRequest",
) -> SubscriptionPlan:
    """
    更新订阅套餐（管理员用）

    Args:
        db: 数据库会话
        plan_id: 套餐ID
        data: 更新请求数据

    Returns:
        SubscriptionPlan: 更新后的套餐对象

    Raises:
        NotFoundException: 套餐不存在
    """
    from app.schemas.subscription import SubscriptionPlanUpdateRequest
    if isinstance(data, dict):
        data = SubscriptionPlanUpdateRequest(**data)

    result = await db.execute(
        select(SubscriptionPlan).where(SubscriptionPlan.id == plan_id)
    )
    plan = result.scalar_one_or_none()
    if not plan:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("订阅套餐不存在")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(plan, field, value)

    await db.flush()
    await db.refresh(plan)
    return plan


async def delete_plan(
    db: AsyncSession,
    plan_id: UUID,
) -> None:
    """
    删除订阅套餐（管理员用）

    Args:
        db: 数据库会话
        plan_id: 套餐ID

    Raises:
        NotFoundException: 套餐不存在
        BusinessException: 套餐已被订阅，无法删除
    """
    result = await db.execute(
        select(SubscriptionPlan).where(SubscriptionPlan.id == plan_id)
    )
    plan = result.scalar_one_or_none()
    if not plan:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("订阅套餐不存在")

    # 检查是否有用户订阅了该套餐
    from sqlalchemy import func
    from app.models.subscription import UserSubscription
    sub_result = await db.execute(
        select(func.count(UserSubscription.id)).where(
            UserSubscription.plan_id == plan_id,
            UserSubscription.status.in_(["trial", "active"]),
        )
    )
    if sub_result.scalar() > 0:
        from app.core.exceptions import BusinessException
        raise BusinessException("该套餐已有用户订阅，无法删除")

    await db.delete(plan)
    await db.flush()


async def toggle_plan_status(
    db: AsyncSession,
    plan_id: UUID,
) -> SubscriptionPlan:
    """
    切换套餐启用/禁用状态（管理员用）

    Args:
        db: 数据库会话
        plan_id: 套餐ID

    Returns:
        SubscriptionPlan: 更新后的套餐对象
    """
    result = await db.execute(
        select(SubscriptionPlan).where(SubscriptionPlan.id == plan_id)
    )
    plan = result.scalar_one_or_none()
    if not plan:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("订阅套餐不存在")

    plan.is_active = not plan.is_active
    await db.flush()
    await db.refresh(plan)
    return plan


# ==================== 支付模拟 ====================


async def create_payment(
    db: AsyncSession,
    user_id: UUID,
    subscription_id: UUID,
    amount: float,
    payment_method: str,
    billing_cycle: str = "yearly",
) -> PaymentRecord:
    """
    创建支付记录

    Args:
        db: 数据库会话
        user_id: 用户ID
        subscription_id: 订阅ID
        amount: 支付金额
        payment_method: 支付方式（wechat/alipay）
        billing_cycle: 计费周期（monthly/yearly）

    Returns:
        PaymentRecord: 创建的支付记录
    """
    import uuid
    from datetime import datetime
    from app.models.subscription import PaymentRecord

    payment = PaymentRecord(
        id=str(uuid.uuid4()),
        user_id=str(user_id),
        subscription_id=str(subscription_id),
        amount=amount,
        payment_method=payment_method,
        billing_cycle=billing_cycle,
        status="pending",
    )
    db.add(payment)
    await db.flush()
    await db.refresh(payment)
    return payment


async def simulate_pay(
    db: AsyncSession,
    payment_id: UUID,
) -> PaymentRecord:
    """
    模拟支付成功

    Args:
        db: 数据库会话
        payment_id: 支付记录ID

    Returns:
        PaymentRecord: 更新后的支付记录

    Raises:
        NotFoundException: 支付记录不存在
    """
    from app.models.subscription import PaymentRecord
    from datetime import datetime
    import uuid

    result = await db.execute(
        select(PaymentRecord).where(PaymentRecord.id == str(payment_id))
    )
    payment = result.scalar_one_or_none()
    if not payment:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("支付记录不存在")

    payment.status = "success"
    payment.transaction_id = f"SIM_{uuid.uuid4().hex[:16].upper()}"
    payment.paid_at = datetime.now()

    # 激活用户订阅
    from app.models.subscription import UserSubscription
    from datetime import date, timedelta
    result = await db.execute(
        select(UserSubscription).where(
            UserSubscription.id == payment.subscription_id,
        )
    )
    subscription = result.scalar_one_or_none()
    if subscription:
        subscription.status = "active"
        if not subscription.start_date:
            today = date.today()
            subscription.start_date = today
            # 根据计费周期设置结束日期
            if payment.billing_cycle == "monthly":
                subscription.end_date = today + timedelta(days=30)
            else:
                subscription.end_date = today + timedelta(days=365)

    await db.flush()
    await db.refresh(payment)
    return payment


async def get_payment(
    db: AsyncSession,
    payment_id: UUID,
) -> PaymentRecord:
    """
    查询支付记录

    Args:
        db: 数据库会话
        payment_id: 支付记录ID

    Returns:
        PaymentRecord: 支付记录

    Raises:
        NotFoundException: 支付记录不存在
    """
    from app.models.subscription import PaymentRecord
    result = await db.execute(
        select(PaymentRecord).where(PaymentRecord.id == str(payment_id))
    )
    payment = result.scalar_one_or_none()
    if not payment:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("支付记录不存在")
    return payment

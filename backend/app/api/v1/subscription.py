"""
订阅路由模块
处理订阅计划查询、用户订阅、升级、取消等接口
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.core.response import success
from app.models.user import User
from app.schemas.subscription import (
    SubscriptionPlanResponse,
    UpgradeRequest,
    UserSubscriptionResponse,
    PaymentRecordResponse,
    CreatePaymentRequest,
)
from app.services import subscription_service

router = APIRouter(prefix="/subscription", tags=["订阅管理"])


@router.get("/plans", summary="获取所有订阅计划")
async def get_plans(
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    获取所有启用的订阅计划
    - 返回计划列表，包含价格、功能特性等信息
    """
    plans = await subscription_service.get_plans(db)

    return success(
        data=[
            SubscriptionPlanResponse.model_validate(plan).model_dump(mode="json")
            for plan in plans
        ],
    )


@router.get("/current", summary="获取当前用户订阅")
async def get_current_subscription(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    获取当前登录用户的有效订阅信息
    - 无订阅时返回 data 为 null
    """
    subscription = await subscription_service.get_current_subscription(
        db, current_user.id
    )

    if not subscription:
        return success(data=None, message="暂无有效订阅")

    return success(
        data=UserSubscriptionResponse.model_validate(subscription).model_dump(
            mode="json"
        ),
    )


@router.post("/upgrade", summary="升级订阅")
async def upgrade_subscription(
    request: UpgradeRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    升级/订阅新计划
    - 若当前无订阅，则创建新订阅（30天试用）
    - 若当前有订阅，则升级到目标计划
    """
    # 先尝试升级，若无订阅则走订阅流程
    try:
        subscription = await subscription_service.upgrade_plan(
            db, current_user.id, request.plan_id
        )
        message = "订阅升级成功"
    except Exception:
        subscription = await subscription_service.subscribe_plan(
            db, current_user.id, request.plan_id
        )
        message = "订阅成功，已开启30天试用"

    return success(
        data=UserSubscriptionResponse.model_validate(subscription).model_dump(
            mode="json"
        ),
        message=message,
    )


@router.post("/cancel", summary="取消订阅")
async def cancel_subscription(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    取消当前订阅
    - 取消后自动续费将关闭
    - 当前周期内仍可继续使用
    """
    subscription = await subscription_service.cancel_subscription(
        db, current_user.id
    )

    return success(
        data=UserSubscriptionResponse.model_validate(subscription).model_dump(
            mode="json"
        ),
        message="订阅已取消",
    )


# ==================== 支付模拟 ====================


@router.post("/payment/create", summary="创建支付订单")
async def create_payment(
    data: CreatePaymentRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    创建支付订单
    - 先创建/获取订阅记录（trial状态）
    - 创建支付记录（状态：pending）
    - 返回支付ID和金额
    """
    from app.models.subscription import SubscriptionPlan, UserSubscription
    from uuid import UUID
    from datetime import date, timedelta
    
    # 查询套餐
    result = await db.execute(
        select(SubscriptionPlan).where(SubscriptionPlan.id == str(data.plan_id))
    )
    plan = result.scalar_one_or_none()
    if not plan:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("订阅套餐不存在")
    
    # 先查找有效状态的订阅记录
    result = await db.execute(
        select(UserSubscription).where(
            UserSubscription.user_id == str(current_user.id),
            UserSubscription.plan_id == str(data.plan_id),
            UserSubscription.status.in_(["trial", "active"]),
        ).order_by(UserSubscription.created_at.desc()).limit(1)
    )
    subscription = result.scalar_one_or_none()
    
    if not subscription:
        # 没有有效记录，检查是否有已取消/过期的记录可复用
        result = await db.execute(
            select(UserSubscription).where(
                UserSubscription.user_id == str(current_user.id),
                UserSubscription.plan_id == str(data.plan_id),
                UserSubscription.status.in_(["expired", "cancelled"]),
            ).order_by(UserSubscription.created_at.desc()).limit(1)
        )
        old_subscription = result.scalar_one_or_none()
        
        if old_subscription:
            # 复用的记录，重置状态
            old_subscription.status = "trial"
            old_subscription.start_date = date.today()
            old_subscription.end_date = None  # 支付成功后再根据 billing_cycle 设置
            old_subscription.auto_renew = True
            await db.flush()
            await db.refresh(old_subscription)
            subscription = old_subscription
        else:
            # 创建新的订阅记录（trial 状态，end_date 由支付时根据 billing_cycle 设置）
            today = date.today()
            subscription = UserSubscription(
                user_id=str(current_user.id),
                plan_id=str(data.plan_id),
                status="trial",
                start_date=today,
                end_date=None,  # 支付成功后再根据 billing_cycle 设置
                auto_renew=True,
            )
            db.add(subscription)
            await db.flush()
            await db.refresh(subscription)
    
    # 创建支付记录，传入正确的 subscription.id 和 billing_cycle
    amount = plan.price_monthly if getattr(data, 'billing_cycle', 'yearly') == 'monthly' else plan.price_yearly
    payment = await subscription_service.create_payment(
        db, current_user.id, subscription.id, amount, data.payment_method, data.billing_cycle
    )
    
    return success(
        data=PaymentRecordResponse.model_validate(payment).model_dump(mode="json"),
        message="支付订单已创建",
    )


@router.get("/payment/{payment_id}", summary="查询支付状态")
async def get_payment(
    payment_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    查询支付记录状态
    """
    payment = await subscription_service.get_payment(db, payment_id)
    
    # 检查权限
    if str(payment.user_id) != str(current_user.id):
        from app.core.exceptions import BusinessException
        raise BusinessException("无权查看该支付记录")
    
    return success(
        data=PaymentRecordResponse.model_validate(payment).model_dump(mode="json")
    )


@router.post("/payment/{payment_id}/simulate", summary="模拟支付成功")
async def simulate_payment(
    payment_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    模拟支付成功
    - 更新支付记录为成功
    - 自动激活用户订阅（365天）
    """
    payment = await subscription_service.simulate_pay(db, payment_id)
    
    # 检查权限
    if str(payment.user_id) != str(current_user.id):
        from app.core.exceptions import BusinessException
        raise BusinessException("无权操作该支付记录")
    
    return success(
        data=PaymentRecordResponse.model_validate(payment).model_dump(mode="json"),
        message="支付成功，订阅已激活",
    )

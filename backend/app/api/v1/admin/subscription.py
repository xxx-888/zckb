"""
管理员订阅套餐管理路由
提供套餐的 CRUD 管理接口，仅管理员可访问
"""

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.core.deps import get_current_active_user, require_roles
from app.core.response import success, paginated
from app.models.user import User
from app.schemas.subscription import (
    SubscriptionPlanResponse,
    SubscriptionPlanCreateRequest,
    SubscriptionPlanUpdateRequest,
)
from app.services import subscription_service

router = APIRouter(prefix="/admin/subscription", tags=["管理员-订阅管理"])


@router.get("/plans", summary="获取所有订阅套餐（管理员）")
async def get_all_plans(
    include_inactive: bool = Query(True, description="是否包含未启用的套餐"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    获取所有订阅套餐列表（管理员用，可查看未启用的套餐）
    """
    plans = await subscription_service.get_all_plans(db, include_inactive=include_inactive)
    return success(
        data=[SubscriptionPlanResponse.model_validate(p).model_dump(mode="json") for p in plans]
    )


@router.post("/plans", summary="创建订阅套餐（管理员）")
async def create_plan(
    data: SubscriptionPlanCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    创建新的订阅套餐
    """
    plan = await subscription_service.create_plan(db, data)
    return success(
        data=SubscriptionPlanResponse.model_validate(plan).model_dump(mode="json"),
        message="创建成功",
    )


@router.put("/plans/{plan_id}", summary="更新订阅套餐（管理员）")
async def update_plan(
    plan_id: str,
    data: SubscriptionPlanUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    更新订阅套餐信息
    """
    plan = await subscription_service.update_plan(db, plan_id, data)
    return success(
        data=SubscriptionPlanResponse.model_validate(plan).model_dump(mode="json"),
        message="更新成功",
    )


@router.delete("/plans/{plan_id}", summary="删除订阅套餐（管理员）")
async def delete_plan(
    plan_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    删除订阅套餐（仅限无用户订阅的套餐）
    """
    await subscription_service.delete_plan(db, plan_id)
    return success(message="删除成功")


@router.patch("/plans/{plan_id}/toggle", summary="启用/禁用套餐（管理员）")
async def toggle_plan_status(
    plan_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    切换套餐的启用/禁用状态
    """
    plan = await subscription_service.toggle_plan_status(db, plan_id)
    status = "启用" if plan.is_active else "禁用"
    return success(
        data=SubscriptionPlanResponse.model_validate(plan).model_dump(mode="json"),
        message=f"已{status}该套餐",
    )


# ==================== 订阅记录管理 ====================


@router.get("/records", summary="获取所有用户订阅记录（管理员）")
async def get_all_subscription_records(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
    user_id: Optional[str] = Query(None, description="按用户ID筛选"),
    status: Optional[str] = Query(None, description="按状态筛选: trial/active/expired/cancelled"),
    plan_id: Optional[str] = Query(None, description="按套餐ID筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
):
    """
    获取所有用户的订阅记录，支持筛选和分页
    """
    from uuid import UUID
    user_id_uuid = UUID(user_id) if user_id else None
    plan_id_uuid = UUID(plan_id) if plan_id else None
    
    result = await subscription_service.get_all_subscription_records(
        db, user_id=user_id_uuid, status=status, plan_id=plan_id_uuid,
        page=page, page_size=page_size
    )
    
    # 转换为响应格式
    items = []
    for sub in result["items"]:
        items.append({
            "id": str(sub.id),
            "user_id": str(sub.user_id),
            "user": {
                "id": str(sub.user.id),
                "username": sub.user.username,
                "email": sub.user.email,
            } if sub.user else None,
            "plan_id": str(sub.plan_id),
            "plan": {
                "id": str(sub.plan.id),
                "name": sub.plan.name,
                "price_monthly": sub.plan.price_monthly,
                "price_yearly": sub.plan.price_yearly,
            } if sub.plan else None,
            "status": sub.status,
            "start_date": str(sub.start_date) if sub.start_date else None,
            "end_date": str(sub.end_date) if sub.end_date else None,
            "auto_renew": sub.auto_renew,
            "created_at": sub.created_at.isoformat() if sub.created_at else None,
        })
    
    return paginated(
        items=items,
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
    )


@router.patch("/records/{subscription_id}/status", summary="更新订阅状态（管理员）")
async def update_subscription_status(
    subscription_id: str,
    status: str = Query(..., description="新状态: trial/active/expired/cancelled"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    管理员手动更新订阅状态
    """
    from uuid import UUID
    subscription = await subscription_service.update_subscription_status(
        db, UUID(subscription_id), status
    )
    return success(
        data={
            "id": str(subscription.id),
            "status": subscription.status,
            "start_date": str(subscription.start_date) if subscription.start_date else None,
            "end_date": str(subscription.end_date) if subscription.end_date else None,
        },
        message="订阅状态已更新"
    )


# ==================== 支付记录管理 ====================


@router.get("/payments", summary="获取所有支付记录（管理员）")
async def get_all_payment_records(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
    user_id: Optional[str] = Query(None, description="按用户ID筛选"),
    status: Optional[str] = Query(None, description="按支付状态筛选: pending/success/failed/refunded"),
    payment_method: Optional[str] = Query(None, description="按支付方式筛选: wechat/alipay"),
    start_date: Optional[str] = Query(None, description="支付开始日期 (ISO格式)"),
    end_date: Optional[str] = Query(None, description="支付结束日期 (ISO格式)"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
):
    """
    获取所有支付记录，支持筛选和分页
    """
    from uuid import UUID
    user_id_uuid = UUID(user_id) if user_id else None
    
    result = await subscription_service.get_all_payment_records(
        db, user_id=user_id_uuid, status=status, payment_method=payment_method,
        start_date=start_date, end_date=end_date,
        page=page, page_size=page_size
    )
    
    # 转换为响应格式
    items = []
    for payment in result["items"]:
        items.append({
            "id": str(payment.id),
            "user_id": str(payment.user_id),
            "user": {
                "id": str(payment.user.id),
                "username": payment.user.username,
                "email": payment.user.email,
            } if payment.user else None,
            "subscription_id": str(payment.subscription_id) if payment.subscription_id else None,
            "amount": payment.amount,
            "payment_method": payment.payment_method,
            "status": payment.status,
            "transaction_id": payment.transaction_id,
            "paid_at": payment.paid_at.isoformat() if payment.paid_at else None,
            "billing_cycle": payment.billing_cycle,
            "created_at": payment.created_at.isoformat() if payment.created_at else None,
        })
    
    return paginated(
        items=items,
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
    )


@router.patch("/payments/{payment_id}/status", summary="更新支付状态（管理员）")
async def update_payment_status(
    payment_id: str,
    status: str = Query(..., description="新状态: pending/success/failed/refunded"),
    transaction_id: Optional[str] = Query(None, description="交易流水号"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
) -> dict:
    """
    管理员手动更新支付状态
    """
    from uuid import UUID
    payment = await subscription_service.update_payment_status(
        db, UUID(payment_id), status, transaction_id
    )
    return success(
        data={
            "id": str(payment.id),
            "status": payment.status,
            "paid_at": payment.paid_at.isoformat() if payment.paid_at else None,
            "transaction_id": payment.transaction_id,
        },
        message="支付状态已更新"
    )

"""
管理员订阅套餐管理路由
提供套餐的 CRUD 管理接口，仅管理员可访问
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_active_user, require_roles
from app.core.response import success
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

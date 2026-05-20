"""
订阅路由模块
处理订阅计划查询、用户订阅、升级、取消等接口
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.core.response import success
from app.models.user import User
from app.schemas.subscription import (
    SubscriptionPlanResponse,
    UpgradeRequest,
    UserSubscriptionResponse,
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

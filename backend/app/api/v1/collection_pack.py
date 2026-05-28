"""
采集套餐用户端路由
处理采集套餐列表、购买、余额查询、订单查询
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.schemas.collection_pack import (
    CollectionOrderResponse,
    CollectionPackResponse,
    CreateCollectionOrderRequest,
    UserCollectionBalanceResponse,
)
from app.services.collection_pack_service import (
    create_order,
    get_packs,
    get_user_balance,
    get_user_orders,
)

router = APIRouter(prefix="/collection-packs", tags=["采集套餐（用户端）"])

@router.get("/plans", response_model=list[CollectionPackResponse])
async def get_available_packs(db: AsyncSession = Depends(get_db)):
    """获取可用的采集套餐列表"""
    packs = await get_packs(db, active_only=True)
    return [CollectionPackResponse.model_validate(p) for p in packs]


@router.post("/purchase", response_model=CollectionOrderResponse)
async def purchase_pack(
    data: CreateCollectionOrderRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """购买采集套餐（模拟支付，直接成功）"""
    order = await create_order(db, str(current_user.id), data)
    return CollectionOrderResponse(
        id=order.id,
        user_id=order.user_id,
        pack_id=order.pack_id,
        pack_name=order.pack.name if order.pack else "",
        credit_amount=order.pack.credit_amount if order.pack else 0,
        amount=order.amount,
        payment_method=order.payment_method,
        status=order.status,
        transaction_id=order.transaction_id,
        paid_at=order.paid_at,
        created_at=order.created_at,
    )


@router.get("/balance", response_model=UserCollectionBalanceResponse)
async def get_my_balance(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """获取我的积分余额"""
    balance = await get_user_balance(db, str(current_user.id))
    return UserCollectionBalanceResponse(
        user_id=balance.user_id,
        balance=balance.balance,
        total_purchased=balance.total_purchased,
    )


@router.get("/my-orders", response_model=list[CollectionOrderResponse])
async def get_my_orders(
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """获取我的采集订单列表"""
    orders, _ = await get_user_orders(db, str(current_user.id), page, page_size)
    return [CollectionOrderResponse(**o) for o in orders]

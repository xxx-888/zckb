"""
采集套餐 Service
处理采集套餐 CRUD、订单创建、积分充值等业务逻辑
"""

from datetime import datetime, timezone
from typing import Any, Optional, Tuple
from uuid import UUID, uuid4

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.collection_pack import (
    CollectionPack,
    CollectionOrder,
    UserCollectionBalance,
)
from app.schemas.collection_pack import (
    CollectionPackCreateRequest,
    CollectionPackUpdateRequest,
    CreateCollectionOrderRequest,
)


# ==================== 采集套餐管理（后台）====================

async def get_packs(db: AsyncSession, *, active_only: bool = False) -> list[CollectionPack]:
    """获取采集套餐列表"""
    stmt = select(CollectionPack)
    if active_only:
        stmt = stmt.where(CollectionPack.is_active == True)
    stmt = stmt.order_by(CollectionPack.price.asc())
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_pack_by_id(db: AsyncSession, pack_id: str) -> Optional[CollectionPack]:
    """根据 ID 获取套餐"""
    stmt = select(CollectionPack).where(CollectionPack.id == UUID(pack_id))
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_pack(db: AsyncSession, data: CollectionPackCreateRequest) -> CollectionPack:
    """创建采集套餐"""
    pack = CollectionPack(
        name=data.name,
        credit_amount=data.credit_amount,
        price=data.price,
        description=data.description,
        is_active=data.is_active,
    )
    db.add(pack)
    await db.commit()
    await db.refresh(pack)
    return pack


async def update_pack(db: AsyncSession, pack_id: str, data: CollectionPackUpdateRequest) -> Optional[CollectionPack]:
    """更新采集套餐"""
    pack = await get_pack_by_id(db, pack_id)
    if not pack:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(pack, field, value)
    await db.commit()
    await db.refresh(pack)
    return pack


async def delete_pack(db: AsyncSession, pack_id: str) -> bool:
    """删除采集套餐"""
    pack = await get_pack_by_id(db, pack_id)
    if not pack:
        return False
    await db.delete(pack)
    await db.commit()
    return True


# ==================== 积分余额管理 ====================

async def get_user_balance(db: AsyncSession, user_id: str) -> UserCollectionBalance:
    """获取用户积分余额，不存在则创建"""
    stmt = select(UserCollectionBalance).where(UserCollectionBalance.user_id == user_id)
    result = await db.execute(stmt)
    balance = result.scalar_one_or_none()
    if not balance:
        balance = UserCollectionBalance(
            user_id=user_id,
            balance=0,
            total_purchased=0,
        )
        db.add(balance)
        await db.commit()
        await db.refresh(balance)
    return balance


async def deduct_credits(db: AsyncSession, user_id: str, amount: int) -> UserCollectionBalance:
    """
    扣除用户积分
    :raises CreditInsufficientException: 积分不足时抛出 (402)
    """
    from app.core.exceptions import CreditInsufficientException
    
    balance = await get_user_balance(db, user_id)
    if balance.balance < amount:
        raise CreditInsufficientException(
            message=f"采集积分不足，需要 {amount} 积分，当前余额 {balance.balance}",
            code=402,
        )
    balance.balance -= amount
    await db.flush()
    return balance


# ==================== 采集订单（用户端 + 后台）====================

async def create_order(
    db: AsyncSession,
    user_id: str,
    data: CreateCollectionOrderRequest,
) -> CollectionOrder:
    """创建采集订单（模拟支付，直接成功）"""
    pack = await get_pack_by_id(db, str(data.pack_id))
    if not pack or not pack.is_active:
        raise HTTPException(status_code=400, detail="套餐不存在或未启用")

    order = CollectionOrder(
        user_id=user_id,
        pack_id=UUID(str(data.pack_id)),
        amount=pack.price,
        payment_method=data.payment_method,
        status="success",  # 模拟支付，直接成功
        paid_at=datetime.now(timezone.utc),
        transaction_id=f"COL{uuid4().hex[:16].upper()}",
    )
    db.add(order)
    await db.flush()

    # 充值积分到用户余额
    balance = await get_user_balance(db, user_id)
    balance.balance += pack.credit_amount
    balance.total_purchased += pack.credit_amount

    await db.commit()
    await db.refresh(order)
    return order


async def get_user_orders(
    db: AsyncSession,
    user_id: str,
    page: int = 1,
    page_size: int = 20,
) -> Tuple[list[dict], int]:
    """获取当前用户的采集订单列表"""
    from app.models.user import User
    stmt = (
        select(
            CollectionOrder,
            CollectionPack.name.label("pack_name"),
            CollectionPack.credit_amount,
        )
        .join(CollectionPack, CollectionPack.id == CollectionOrder.pack_id)
        .where(CollectionOrder.user_id == user_id)
        .order_by(CollectionOrder.created_at.desc())
    )
    # 统计总数
    count_stmt = select(func.count()).select_from(CollectionOrder).where(CollectionOrder.user_id == user_id)
    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    rows = result.all()

    orders = []
    for row in rows:
        order, pack_name, credit_amount = row[0], row[1], row[2]
        orders.append({
            "id": str(order.id),
            "user_id": str(order.user_id),
            "pack_id": str(order.pack_id),
            "pack_name": pack_name,
            "credit_amount": credit_amount,
            "amount": order.amount,
            "payment_method": order.payment_method,
            "status": order.status,
            "transaction_id": order.transaction_id,
            "paid_at": order.paid_at,
            "created_at": order.created_at,
        })
    return orders, total


async def get_all_orders(
    db: AsyncSession,
    *,
    user_id: Optional[str] = None,
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> Tuple[list[dict], int]:
    """获取所有采集订单（后台管理）"""
    from app.models.user import User
    stmt = (
        select(
            CollectionOrder,
            CollectionPack.name.label("pack_name"),
            CollectionPack.credit_amount,
            User.username.label("user_name"),
            User.email,
        )
        .join(CollectionPack, CollectionPack.id == CollectionOrder.pack_id)
        .join(User, User.id == CollectionOrder.user_id)
        .order_by(CollectionOrder.created_at.desc())
    )
    count_stmt = select(func.count()).select_from(CollectionOrder)
    if user_id:
        stmt = stmt.where(CollectionOrder.user_id == user_id)
        count_stmt = count_stmt.where(CollectionOrder.user_id == user_id)
    if status:
        stmt = stmt.where(CollectionOrder.status == status)
        count_stmt = count_stmt.where(CollectionOrder.status == status)

    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    rows = result.all()

    orders = []
    for row in rows:
        order, pack_name, credit_amount, user_name, email = row[0], row[1], row[2], row[3], row[4]
        orders.append({
            "id": str(order.id),
            "user_id": str(order.user_id),
            "user_name": user_name,
            "email": email,
            "pack_id": str(order.pack_id),
            "pack_name": pack_name,
            "credit_amount": credit_amount,
            "amount": order.amount,
            "payment_method": order.payment_method,
            "status": order.status,
            "transaction_id": order.transaction_id,
            "paid_at": order.paid_at,
            "created_at": order.created_at,
        })
    return orders, total


async def update_order_status(
    db: AsyncSession,
    order_id: str,
    new_status: str,
) -> Optional[CollectionOrder]:
    """修改采集订单状态（后台管理）"""
    stmt = select(CollectionOrder).where(CollectionOrder.id == order_id)
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    if not order:
        return None
    order.status = new_status
    await db.flush()
    await db.commit()
    await db.refresh(order)
    return order

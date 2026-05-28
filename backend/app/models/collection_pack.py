"""采集套餐相关模型：CollectionPack、UserCollectionBalance、CollectionOrder。"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, GUID

if TYPE_CHECKING:
    from .user import User


class CollectionPack(BaseModel):
    """采集套餐表（按量付费积分包）。"""

    __tablename__ = "collection_packs"

    name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="套餐名称（如：500条采集包）"
    )
    credit_amount: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="包含积分数量（条）"
    )
    price: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.0, comment="价格（元）"
    )
    description: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, comment="套餐描述"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, comment="是否启用"
    )

    # -- 关系 --
    orders: Mapped[list["CollectionOrder"]] = relationship(
        "CollectionOrder", back_populates="pack", lazy="selectin"
    )


class UserCollectionBalance(BaseModel):
    """用户积分余额表。"""

    __tablename__ = "user_collection_balances"

    user_id: Mapped[str] = mapped_column(
        GUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        unique=True,
        comment="用户ID",
    )
    balance: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="当前剩余积分"
    )
    total_purchased: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="累计购买积分"
    )

    # -- 关系 --
    user: Mapped["User"] = relationship("User")


class CollectionOrder(BaseModel):
    """采集订单表。"""

    __tablename__ = "collection_orders"

    user_id: Mapped[str] = mapped_column(
        GUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="用户ID",
    )
    pack_id: Mapped[str] = mapped_column(
        GUID(),
        ForeignKey("collection_packs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="套餐ID",
    )
    amount: Mapped[float] = mapped_column(
        Float, nullable=False, comment="支付金额"
    )
    payment_method: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="支付方式: wechat/alipay"
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        comment="状态: pending/success/failed",
    )
    transaction_id: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, comment="交易流水号"
    )
    paid_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="支付时间"
    )

    # -- 关系 --
    user: Mapped["User"] = relationship("User")
    pack: Mapped["CollectionPack"] = relationship(
        "CollectionPack", back_populates="orders"
    )

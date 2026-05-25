"""订阅相关模型：SubscriptionPlan、UserSubscription。"""

from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Boolean, Date, DateTime, Enum, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, GUID

if TYPE_CHECKING:
    from .user import User


class SubscriptionPlan(BaseModel):
    """订阅套餐表。"""

    __tablename__ = "subscription_plans"

    name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="套餐名称(标准版/旗舰版/企业版)"
    )
    price_monthly: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.0, comment="月价格"
    )
    price_yearly: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.0, comment="年价格"
    )
    features: Mapped[Optional[list[str]]] = mapped_column(
        JSON, nullable=True, comment="功能特性列表(JSON数组)"
    )
    max_stores: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1, comment="最大门店数"
    )
    max_reviews_per_month: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="每月最大评论数"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, comment="是否启用"
    )

    # -- 关系 --
    user_subscriptions: Mapped[list[UserSubscription]] = relationship(
        "UserSubscription", back_populates="plan", lazy="selectin"
    )


class UserSubscription(BaseModel):
    """用户订阅表。"""

    __tablename__ = "user_subscriptions"

    user_id: Mapped[str] = mapped_column(
        GUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="用户ID",
    )
    plan_id: Mapped[str] = mapped_column(
        GUID(),
        ForeignKey("subscription_plans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="套餐ID",
    )
    status: Mapped[str] = mapped_column(
        Enum("trial", "active", "expired", "cancelled", name="subscription_status"),
        nullable=False,
        default="trial",
        comment="状态: trial-试用, active-活跃, expired-已过期, cancelled-已取消",
    )
    start_date: Mapped[date] = mapped_column(
        Date, nullable=False, comment="开始日期"
    )
    end_date: Mapped[Optional[date]] = mapped_column(
        Date, nullable=True, comment="结束日期"
    )
    auto_renew: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, comment="是否自动续费"
    )

    # -- 关系 --
    user: Mapped[User] = relationship("User", back_populates="subscriptions")
    plan: Mapped[SubscriptionPlan] = relationship(
        "SubscriptionPlan", back_populates="user_subscriptions"
    )


class PaymentRecord(BaseModel):
    """支付记录表。"""

    __tablename__ = "payment_records"

    user_id: Mapped[str] = mapped_column(
        GUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="用户ID",
    )
    subscription_id: Mapped[Optional[str]] = mapped_column(
        GUID(),
        ForeignKey("user_subscriptions.id", ondelete="SET NULL"),
        nullable=True,
        comment="订阅ID",
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
        comment="状态: pending/success/failed/refunded",
    )
    transaction_id: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, comment="交易流水号"
    )
    paid_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="支付时间"
    )

    # -- 关系 --
    user: Mapped[User] = relationship("User")

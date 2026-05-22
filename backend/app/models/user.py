"""用户相关模型：User、UserStore、Region。"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, BaseModel, GUID

if TYPE_CHECKING:
    from .settings import ReplyTemplate, UserNotificationSetting
    from .store import Store
    from .subscription import UserSubscription


class User(BaseModel):
    """用户表。"""

    __tablename__ = "users"

    phone: Mapped[Optional[str]] = mapped_column(
        String(20), unique=True, nullable=True, index=True, comment="手机号"
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(255), unique=True, nullable=True, index=True, comment="邮箱"
    )
    username: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="用户名"
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="加密密码"
    )
    avatar: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, comment="头像URL"
    )
    role: Mapped[str] = mapped_column(
        Enum("HQ", "OPERATOR", "STORE", name="user_role"),
        nullable=False,
        default="STORE",
        comment="角色: HQ-总部, OPERATOR-运营, STORE-门店",
    )
    status: Mapped[str] = mapped_column(
        Enum("active", "disabled", name="user_status"),
        nullable=False,
        default="active",
        comment="状态: active-启用, disabled-禁用",
    )
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=False),
        nullable=True,
        comment="最后登录时间",
    )

    # -- 关系 --
    owned_stores: Mapped[list[Store]] = relationship(
        "Store", back_populates="owner", lazy="selectin"
    )
    store_associations: Mapped[list[UserStore]] = relationship(
        "UserStore", back_populates="user", lazy="selectin"
    )
    subscriptions: Mapped[list[UserSubscription]] = relationship(
        "UserSubscription", back_populates="user", lazy="selectin"
    )
    reply_templates: Mapped[list[ReplyTemplate]] = relationship(
        "ReplyTemplate", back_populates="user", lazy="selectin"
    )
    notification_setting: Mapped[Optional[UserNotificationSetting]] = relationship(
        "UserNotificationSetting", back_populates="user", uselist=False, lazy="selectin"
    )


class UserStore(Base):
    """用户-门店关联表（多对多）。"""

    __tablename__ = "user_stores"

    user_id: Mapped[str] = mapped_column(
        GUID(),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        comment="用户ID",
    )
    store_id: Mapped[str] = mapped_column(
        GUID(),
        ForeignKey("stores.id", ondelete="CASCADE"),
        primary_key=True,
        comment="门店ID",
    )
    role_in_store: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="门店内角色",
    )

    # -- 关系 --
    user: Mapped[User] = relationship("User", back_populates="store_associations")
    store: Mapped[Store] = relationship("Store", back_populates="user_associations")


class Region(BaseModel):
    """区域层级表（省/市/区）。"""

    __tablename__ = "regions"

    name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="区域名称"
    )
    parent_id: Mapped[Optional[UUID]] = mapped_column(
        GUID(),
        ForeignKey("regions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="父级区域ID",
    )
    level: Mapped[str] = mapped_column(
        Enum("province", "city", "district", name="region_level"),
        nullable=False,
        comment="层级: province-省, city-市, district-区",
    )
    code: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True, index=True, comment="行政区划代码"
    )

    # -- 关系 --
    parent: Mapped[Optional[Region]] = relationship(
        "Region", remote_side="Region.id", lazy="selectin"
    )
    children: Mapped[list[Region]] = relationship(
        "Region", back_populates="parent", lazy="selectin"
    )
    stores: Mapped[list[Store]] = relationship(
        "Store", back_populates="region", lazy="selectin"
    )

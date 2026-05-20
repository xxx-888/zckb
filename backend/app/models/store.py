"""门店相关模型：Store、StorePlatform。"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, GUID

if TYPE_CHECKING:
    from .report import AnnualReport, WeeklyBrief, Competitor
    from .review import Review
    from .settings import AutoReplyConfig
    from .user import Region, UserStore


class Store(BaseModel):
    """门店表。"""

    __tablename__ = "stores"

    name: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="门店名称"
    )
    type: Mapped[str] = mapped_column(
        Enum("restaurant", "hotel", "beverage", name="store_type"),
        nullable=False,
        comment="门店类型: restaurant-餐饮, hotel-酒店, beverage-饮品",
    )
    address: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, comment="门店地址"
    )
    owner_name: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, comment="店主姓名"
    )
    phone: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True, comment="联系电话"
    )
    status: Mapped[str] = mapped_column(
        Enum("active", "pending", "inactive", name="store_status"),
        nullable=False,
        default="pending",
        comment="状态: active-活跃, pending-待审核, inactive-停用",
    )
    health_score: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True, comment="健康评分"
    )
    platform_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="关联平台数量"
    )
    review_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="评论总数"
    )
    region_id: Mapped[Optional[UUID]] = mapped_column(
        GUID(),
        ForeignKey("regions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="区域ID",
    )

    # -- 关系 --
    region: Mapped[Optional[Region]] = relationship(
        "Region", back_populates="stores"
    )
    platforms: Mapped[list[StorePlatform]] = relationship(
        "StorePlatform", back_populates="store", lazy="selectin"
    )
    user_associations: Mapped[list[UserStore]] = relationship(
        "UserStore", back_populates="store", lazy="selectin"
    )
    reviews: Mapped[list[Review]] = relationship(
        "Review", back_populates="store", lazy="selectin"
    )
    auto_reply_config: Mapped[Optional[AutoReplyConfig]] = relationship(
        "AutoReplyConfig", back_populates="store", uselist=False, lazy="selectin"
    )
    annual_reports: Mapped[list[AnnualReport]] = relationship(
        "AnnualReport", back_populates="store", lazy="selectin"
    )
    weekly_briefs: Mapped[list[WeeklyBrief]] = relationship(
        "WeeklyBrief", back_populates="store", lazy="selectin"
    )
    competitors: Mapped[list[Competitor]] = relationship(
        "Competitor", back_populates="store", lazy="selectin"
    )


class StorePlatform(BaseModel):
    """门店-平台关联表。"""

    __tablename__ = "store_platforms"

    store_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="门店ID",
    )
    platform: Mapped[str] = mapped_column(
        Enum(
            "meituan", "dianping", "douyin", "taobao", "jd",
            name="store_platform_name",
        ),
        nullable=False,
        comment="平台名称",
    )
    platform_store_id: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, comment="平台侧门店ID"
    )
    platform_store_name: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, comment="平台侧门店名称"
    )
    connected: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, comment="是否已连接"
    )
    last_sync_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=False), nullable=True, comment="最后同步时间"
    )
    sync_status: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, comment="同步状态"
    )
    config: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="平台配置(JSON)"
    )

    # -- 关系 --
    store: Mapped[Store] = relationship("Store", back_populates="platforms")

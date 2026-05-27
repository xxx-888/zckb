"""Region model for hierarchical area management (province/city/district)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import Enum as SQLEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, UUID, Base
from app.models.store import Store

if TYPE_CHECKING:
    from .user import User


class Region(BaseModel, Base):
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
        SQLEnum("province", "city", "district", name="region_level"),
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
    # -- 多对多反向关系：关联的用户 --
    users: Mapped[list[User]] = relationship(
        "User",
        secondary="user_regions",
        lazy="selectin",
        back_populates="regions",
    )

"""User-Region association table for many-to-many relationship."""
from sqlalchemy import Column, ForeignKey, Table, UUID

from app.models.base import Base, GUID

# 用户-区域关联表（多对多）
user_regions = Table(
    "user_regions",
    Base.metadata,
    Column("user_id", GUID(), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, comment="用户ID"),
    Column("region_id", GUID(), ForeignKey("regions.id", ondelete="CASCADE"), primary_key=True, comment="区域ID"),
    comment="用户-区域关联表（多对多）"
)

"""
经营看板数据模型：营业额记录、套餐核销记录、门店运营指标、运营分析意见。
初期由运营手动录入（Excel导入），未来通过API自动同步。
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from .base import BaseModel, GUID

if TYPE_CHECKING:
    from .store import Store
    from .user import User


class RevenueRecord(BaseModel):
    """营业额记录表。按门店+日期粒度记录每日经营数据。"""

    __tablename__ = "revenue_records"

    store_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="门店ID",
    )
    record_date: Mapped[date] = mapped_column(
        Date, nullable=False, index=True, comment="记录日期"
    )
    total_revenue: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="总营业额"
    )
    meituan_revenue: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="美团营业额"
    )
    douyin_revenue: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="抖音营业额"
    )
    other_revenue: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="其他收入(到店/现金)"
    )
    visitor_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="到店人数"
    )
    table_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="接待桌数"
    )
    avg_people_per_table: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="桌均人数"
    )
    avg_per_capita: Mapped[float] = mapped_column(
        Float, nullable=False, default=0, comment="人均消费"
    )
    notes: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="备注"
    )
    created_by: Mapped[Optional[UUID]] = mapped_column(
        GUID(),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="录入人ID",
    )


class PackageRecord(BaseModel):
    """套餐核销记录表。按门店+周期+商品粒度记录套餐购买和核销数据。"""

    __tablename__ = "package_records"

    store_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="门店ID",
    )
    period_start: Mapped[date] = mapped_column(
        Date, nullable=False, index=True, comment="周期开始日期"
    )
    period_end: Mapped[date] = mapped_column(
        Date, nullable=False, index=True, comment="周期结束日期"
    )
    product_name: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="商品名称"
    )
    meituan_buy: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="美团购买数"
    )
    meituan_verify: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="美团核销券数"
    )
    douyin_buy: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="抖音购买数"
    )
    douyin_verify: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="抖音核销券数"
    )
    notes: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="备注"
    )
    created_by: Mapped[Optional[UUID]] = mapped_column(
        GUID(),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="录入人ID",
    )


class StoreMetric(BaseModel):
    """门店运营指标表。按门店+日期+平台粒度记录各平台运营数据。"""

    __tablename__ = "store_metrics"

    store_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="门店ID",
    )
    metric_date: Mapped[date] = mapped_column(
        Date, nullable=False, index=True, comment="指标日期"
    )
    platform: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True, comment="平台名称(meituan/dianping/douyin)"
    )
    # 榜单
    ranking_name: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, comment="榜单名称(如: 大学城烤串人气榜)"
    )
    ranking_position: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, comment="当前排名"
    )
    prev_ranking_position: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, comment="上一周期排名"
    )
    # 评分
    star_rating: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True, comment="当前星级"
    )
    prev_star_rating: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True, comment="上一周期星级"
    )
    # 流量
    impressions: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="曝光次数/人数"
    )
    visits: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="访问次数/人数"
    )
    purchases: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="购买人数"
    )
    verifications: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="核销人数"
    )
    new_favorites: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="新增收藏人数"
    )
    checkins: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="打卡人数"
    )
    scan_count: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="扫码人数"
    )
    product_impressions: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="商品曝光人数"
    )
    product_visits: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="商品访问人数"
    )
    product_purchases: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="商品购买人数"
    )
    # 评价
    new_reviews: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="新评价数"
    )
    new_bad_reviews: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="新中差评数"
    )
    bad_keywords: Mapped[Optional[list[str]]] = mapped_column(
        JSON, nullable=True, comment="差评关键词列表"
    )
    notes: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="备注"
    )
    created_by: Mapped[Optional[UUID]] = mapped_column(
        GUID(),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="录入人ID",
    )


class OperationAnalysis(BaseModel):
    """运营分析意见表。按门店+周期粒度记录分析意见和下周目标。"""

    __tablename__ = "operation_analyses"

    store_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="门店ID",
    )
    period_start: Mapped[date] = mapped_column(
        Date, nullable=False, index=True, comment="周期开始日期"
    )
    period_end: Mapped[date] = mapped_column(
        Date, nullable=False, index=True, comment="周期结束日期"
    )
    analysis_opinion: Mapped[str] = mapped_column(
        Text, nullable=False, default="", comment="分析意见"
    )
    goals: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=list, comment="下周目标列表"
    )
    created_by: Mapped[Optional[UUID]] = mapped_column(
        GUID(),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="创建人ID",
    )

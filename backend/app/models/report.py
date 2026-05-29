"""报告相关模型：AnnualReport、WeeklyBrief、Competitor、CompetitorAnalysisTask。"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, GUID

if TYPE_CHECKING:
    from .store import Store


class AnnualReport(BaseModel):
    """年度报告表。"""

    __tablename__ = "annual_reports"

    store_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="门店ID",
    )
    year: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="年份"
    )
    total_reviews: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="评论总数"
    )
    average_rating: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True, comment="平均评分"
    )
    sentiment_distribution: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="情感分布(JSON)"
    )
    reply_stats: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="回复统计(JSON)"
    )
    monthly_data: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="月度数据(JSON)"
    )
    top_keywords: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="热门关键词(JSON)"
    )
    category_scores: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="分类评分(JSON)"
    )
    insights: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
        comment="洞察(JSON): year_over_year/highlights/improvements/ai_summary",
    )
    rating_distribution: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="评分分布(JSON)"
    )
    platform_distribution: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="平台来源分布(JSON)"
    )
    reply_sentiment: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="回复情感分布(JSON)"
    )
    peak_month: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="峰值月份(JSON)"
    )
    active_days: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="活跃天数"
    )
    monthly_sentiment: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="月度情感/回复率趋势(JSON)"
    )
    generated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=False), nullable=True, comment="生成时间"
    )

    # -- 关系 --
    store: Mapped[Store] = relationship("Store", back_populates="annual_reports")


class WeeklyBrief(BaseModel):
    """周报简报表。"""

    __tablename__ = "weekly_briefs"

    store_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="门店ID",
    )
    week_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False, comment="周开始日期"
    )
    week_end: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False, comment="周结束日期"
    )
    total_reviews: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="本周评论总数"
    )
    positive_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="正面评论数"
    )
    negative_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="负面评论数"
    )
    neutral_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="中性评论数"
    )
    avg_rating: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True, comment="平均评分"
    )
    top_issues: Mapped[Optional[list[str]]] = mapped_column(
        JSON, nullable=True, comment="主要问题列表"
    )
    top_praises: Mapped[Optional[list[str]]] = mapped_column(
        JSON, nullable=True, comment="主要好评列表"
    )
    dish_analysis: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="菜品分析(JSON)"
    )
    ai_summary: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="AI 摘要"
    )
    generated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=False), nullable=True, comment="生成时间"
    )

    # -- 关系 --
    store: Mapped[Store] = relationship("Store", back_populates="weekly_briefs")


class Competitor(BaseModel):
    """竞品表。"""

    __tablename__ = "competitors"

    store_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="门店ID",
    )
    name: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="竞品名称"
    )
    platform: Mapped[str] = mapped_column(
        Enum(
            "meituan", "dianping", "douyin", "taobao", "jd",
            name="competitor_platform",
        ),
        nullable=False,
        comment="平台",
    )
    platform_store_id: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, comment="平台侧门店ID"
    )
    rating: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True, comment="评分"
    )
    positive_rate: Mapped[Optional[float]] = mapped_column(
        Float, nullable=True, comment="好评率"
    )
    review_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="评论数"
    )
    trends_data: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="趋势数据(JSON)"
    )
    bad_tags: Mapped[Optional[list[str]]] = mapped_column(
        JSON, nullable=True, comment="差评标签列表"
    )
    last_synced_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=False), nullable=True, comment="最后同步时间"
    )

    # -- 关系 --
    store: Mapped[Store] = relationship("Store", back_populates="competitors")
    analysis_tasks: Mapped[list[CompetitorAnalysisTask]] = relationship(
        "CompetitorAnalysisTask", back_populates="competitor", lazy="selectin"
    )


class CompetitorAnalysisTask(BaseModel):
    """竞品分析任务表。"""

    __tablename__ = "competitor_analysis_tasks"

    competitor_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("competitors.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="竞品ID",
    )
    status: Mapped[str] = mapped_column(
        Enum(
            "pending", "collecting", "analyzing", "completed", "failed",
            name="competitor_analysis_status",
        ),
        nullable=False,
        default="pending",
        comment="状态: pending-待处理, collecting-采集中, analyzing-分析中, completed-已完成, failed-失败",
    )
    payment_status: Mapped[str] = mapped_column(
        Enum("unpaid", "paid", name="competitor_payment_status"),
        nullable=False,
        default="unpaid",
        comment="支付状态: unpaid-未支付, paid-已支付",
    )
    price: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.0, comment="价格"
    )
    result_data: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="分析结果数据(JSON)"
    )

    # -- 关系 --
    competitor: Mapped[Competitor] = relationship(
        "Competitor", back_populates="analysis_tasks"
    )

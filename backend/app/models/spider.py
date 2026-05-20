"""爬虫相关模型：SpiderPlatform、SpiderSyncLog、SpiderTask。"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import BigInteger, DateTime, Enum, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, BaseModel, GUID, TimestampMixin


class SpiderPlatform(BaseModel):
    """爬虫平台表。"""

    __tablename__ = "spider_platforms"

    name: Mapped[str] = mapped_column(
        Enum(
            "meituan", "dianping", "douyin", "taobao", "jd",
            name="spider_platform_name",
        ),
        nullable=False,
        unique=True,
        comment="平台名称: meituan/dianping/douyin/taobao/jd",
    )
    display_name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="显示名称"
    )
    status: Mapped[str] = mapped_column(
        Enum("active", "paused", "error", name="spider_platform_status"),
        nullable=False,
        default="active",
        comment="状态: active-活跃, paused-暂停, error-异常",
    )
    reliability: Mapped[float] = mapped_column(
        Float, nullable=False, default=1.0, comment="可靠性评分"
    )
    error_log: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="错误日志"
    )
    config: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="配置(JSON，含cookies等)"
    )
    last_sync_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=False), nullable=True, comment="最后同步时间"
    )

    # -- 关系 --
    sync_logs: Mapped[list[SpiderSyncLog]] = relationship(
        "SpiderSyncLog", back_populates="platform", lazy="selectin"
    )
    tasks: Mapped[list[SpiderTask]] = relationship(
        "SpiderTask", back_populates="platform", lazy="selectin"
    )


class SpiderSyncLog(BaseModel):
    """爬虫同步日志表。"""

    __tablename__ = "spider_sync_logs"

    platform_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("spider_platforms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="平台ID",
    )
    store_id: Mapped[Optional[UUID]] = mapped_column(
        GUID(),
        ForeignKey("stores.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="门店ID",
    )
    status: Mapped[str] = mapped_column(
        Enum("running", "success", "failed", name="spider_sync_status"),
        nullable=False,
        comment="状态: running-运行中, success-成功, failed-失败",
    )
    records_synced: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="同步记录数"
    )
    error_message: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="错误信息"
    )
    duration_ms: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="耗时(毫秒)"
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=False), nullable=True, comment="开始时间"
    )
    finished_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=False), nullable=True, comment="结束时间"
    )

    # -- 关系 --
    platform: Mapped[SpiderPlatform] = relationship(
        "SpiderPlatform", back_populates="sync_logs"
    )


class SpiderTask(TimestampMixin, Base):
    """爬虫任务表（使用 BigInteger 自增ID）。"""

    __tablename__ = "spider_tasks"

    # 覆盖基类的 UUID 主键，使用 BigInteger 自增
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="任务ID(自增)",
    )

    platform_id: Mapped[UUID] = mapped_column(
        GUID(),
        ForeignKey("spider_platforms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="平台ID",
    )
    store_id: Mapped[Optional[UUID]] = mapped_column(
        GUID(),
        ForeignKey("stores.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="门店ID",
    )
    task_type: Mapped[str] = mapped_column(
        Enum("full_sync", "incremental", "reply", name="spider_task_type"),
        nullable=False,
        comment="任务类型: full_sync-全量同步, incremental-增量同步, reply-回复同步",
    )
    status: Mapped[str] = mapped_column(
        Enum("pending", "running", "success", "failed", name="spider_task_status"),
        nullable=False,
        default="pending",
        comment="状态: pending-待执行, running-运行中, success-成功, failed-失败",
    )
    priority: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="优先级"
    )
    result: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="任务结果(JSON)"
    )
    error_message: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="错误信息"
    )
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=False), nullable=True, comment="计划执行时间"
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=False), nullable=True, comment="开始执行时间"
    )
    finished_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=False), nullable=True, comment="执行完成时间"
    )

    # -- 关系 --
    platform: Mapped[SpiderPlatform] = relationship(
        "SpiderPlatform", back_populates="tasks"
    )

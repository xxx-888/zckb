"""AI 配置相关模型：AIModelConfig、AIPromptTemplate、AIRuleEngine、AIProcessingLog。"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Boolean, Enum, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, GUID

if TYPE_CHECKING:
    from .review import Review


class AIModelConfig(BaseModel):
    """AI 模型配置表。"""

    __tablename__ = "ai_model_configs"

    provider: Mapped[str] = mapped_column(
        Enum(
            "openai", "zhipu", "wenxin", "deepseek", "local",
            name="ai_provider",
        ),
        nullable=False,
        comment="提供商: openai/zhipu/wenxin/deepseek/local",
    )
    model_name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="模型名称"
    )
    api_key_encrypted: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, comment="加密后的API Key"
    )
    endpoint_url: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True, comment="API端点URL"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, comment="是否启用"
    )
    priority: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="优先级(数值越大优先级越高)"
    )
    max_tokens: Mapped[int] = mapped_column(
        Integer, nullable=False, default=2048, comment="最大token数"
    )
    temperature: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.7, comment="温度参数"
    )
    config: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="额外配置"
    )

    # -- 关系 --
    processing_logs: Mapped[list[AIProcessingLog]] = relationship(
        "AIProcessingLog", back_populates="model_config", lazy="selectin"
    )


class AIPromptTemplate(BaseModel):
    """AI 提示词模板表。"""

    __tablename__ = "ai_prompt_templates"

    name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="模板名称"
    )
    type: Mapped[str] = mapped_column(
        Enum(
            "good_review", "bad_review", "neutral_review", "appeal", "weekly_report",
            name="prompt_template_type",
        ),
        nullable=False,
        comment="模板类型",
    )
    template_text: Mapped[str] = mapped_column(
        Text, nullable=False, comment="模板文本"
    )
    variables: Mapped[Optional[list[str]]] = mapped_column(
        JSON, nullable=True, comment="变量列表"
    )
    system_prompt: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="系统提示词"
    )
    is_default: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, comment="是否为默认模板"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, comment="是否启用"
    )


class AIRuleEngine(BaseModel):
    """AI 规则引擎表。"""

    __tablename__ = "ai_rule_engines"

    name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="规则名称"
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="规则描述"
    )
    rules: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True, comment="规则定义"
    )
    priority: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="优先级"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, comment="是否启用"
    )


class AIProcessingLog(BaseModel):
    """AI 处理日志表。"""

    __tablename__ = "ai_processing_logs"

    review_id: Mapped[Optional[UUID]] = mapped_column(
        GUID(),
        ForeignKey("reviews.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="关联评论ID",
    )
    model_config_id: Mapped[Optional[UUID]] = mapped_column(
        GUID(),
        ForeignKey("ai_model_configs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="模型配置ID",
    )
    input_tokens: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="输入token数"
    )
    output_tokens: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="输出token数"
    )
    processing_time_ms: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, comment="处理耗时(毫秒)"
    )
    status: Mapped[str] = mapped_column(
        Enum("success", "failed", name="ai_processing_status"),
        nullable=False,
        comment="处理状态: success-成功, failed-失败",
    )
    error_message: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="错误信息"
    )
    input_text: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="输入文本"
    )
    output_text: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="输出文本"
    )

    # -- 关系 --
    review: Mapped[Optional[Review]] = relationship(
        "Review", back_populates="processing_logs"
    )
    model_config: Mapped[Optional[AIModelConfig]] = relationship(
        "AIModelConfig", back_populates="processing_logs"
    )

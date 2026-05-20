"""
通知相关 Schema
定义通知渠道、规则、历史、模板等请求/响应数据结构
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ==================== 通知渠道 ====================


class NotificationChannelResponse(BaseModel):
    """通知渠道响应"""

    id: UUID
    name: str
    type: str
    webhook_url: Optional[str] = None
    config: Optional[dict] = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationChannelCreateRequest(BaseModel):
    """创建通知渠道请求"""

    name: str = Field(..., description="渠道名称", min_length=1, max_length=100)
    type: str = Field(..., description="渠道类型: wechat/dingtalk/feishu/email/sms/push")
    webhook_url: Optional[str] = Field(None, description="Webhook URL", max_length=500)
    config: Optional[dict] = Field(None, description="渠道配置")


class NotificationChannelUpdateRequest(BaseModel):
    """更新通知渠道请求"""

    name: Optional[str] = Field(None, description="渠道名称", min_length=1, max_length=100)
    webhook_url: Optional[str] = Field(None, description="Webhook URL", max_length=500)
    config: Optional[dict] = Field(None, description="渠道配置")
    is_active: Optional[bool] = Field(None, description="是否启用")


# ==================== 通知规则 ====================


class NotificationRuleResponse(BaseModel):
    """通知规则响应"""

    id: UUID
    name: str
    channel_id: UUID
    channel_name: Optional[str] = None
    event_type: str
    condition: Optional[dict] = None
    frequency: str
    is_active: bool

    model_config = {"from_attributes": True}


class NotificationRuleCreateRequest(BaseModel):
    """创建通知规则请求"""

    name: str = Field(..., description="规则名称", min_length=1, max_length=100)
    channel_id: UUID = Field(..., description="渠道ID")
    event_type: str = Field(..., description="事件类型: new_review/negative_alert/weekly_report/spider_status")
    condition: Optional[dict] = Field(None, description="触发条件")
    frequency: Optional[str] = Field("realtime", description="频率: realtime/daily/weekly")


class NotificationRuleUpdateRequest(BaseModel):
    """更新通知规则请求"""

    name: Optional[str] = Field(None, description="规则名称", min_length=1, max_length=100)
    channel_id: Optional[UUID] = Field(None, description="渠道ID")
    event_type: Optional[str] = Field(None, description="事件类型")
    condition: Optional[dict] = Field(None, description="触发条件")
    frequency: Optional[str] = Field(None, description="频率")
    is_active: Optional[bool] = Field(None, description="是否启用")


# ==================== 通知历史 ====================


class NotificationHistoryResponse(BaseModel):
    """通知历史响应"""

    id: UUID
    rule_name: Optional[str] = None
    channel_name: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    recipient: Optional[str] = None
    status: str
    latency_ms: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ==================== 通知模板 ====================


class NotificationTemplateResponse(BaseModel):
    """通知模板响应"""

    id: UUID
    name: str
    event_type: str
    template_text: str
    variables: Optional[list[str]] = None
    is_active: bool

    model_config = {"from_attributes": True}


class NotificationTemplateCreateRequest(BaseModel):
    """创建通知模板请求"""

    name: str = Field(..., description="模板名称", min_length=1, max_length=100)
    event_type: str = Field(..., description="事件类型: new_review/negative_alert/weekly_report/spider_status")
    template_text: str = Field(..., description="模板文本")
    variables: Optional[list[str]] = Field(None, description="变量列表")


class NotificationTemplateUpdateRequest(BaseModel):
    """更新通知模板请求"""

    name: Optional[str] = Field(None, description="模板名称", min_length=1, max_length=100)
    template_text: Optional[str] = Field(None, description="模板文本")
    variables: Optional[list[str]] = Field(None, description="变量列表")
    is_active: Optional[bool] = Field(None, description="是否启用")

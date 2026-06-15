"""
审核相关 Schema
定义回复审核列表、详情、统计等请求/响应数据结构
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AuditItemResponse(BaseModel):
    """审核项响应"""
    id: UUID
    review_id: UUID
    store_name: Optional[str] = None
    store_id: Optional[str] = None
    user_name: Optional[str] = None
    user_avatar: Optional[str] = None
    rating: Optional[int] = None
    content: Optional[str] = None
    platform: Optional[str] = None
    ai_reply: Optional[str] = None
    status: str
    risk_level: Optional[str] = None
    scores: Optional[dict] = None
    reject_reason: Optional[str] = None
    auditor_name: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    model_config = {"from_attributes": True}


class AuditListResponse(BaseModel):
    """审核列表响应"""
    items: list[AuditItemResponse]
    total: int
    page: int
    pageSize: int


class AuditStatsResponse(BaseModel):
    """审核统计响应"""
    pending_count: int = 0
    approved_count: int = 0
    rejected_count: int = 0
    sent_count: int = 0
    total_count: int = 0
    avg_processing_time: Optional[float] = None


class AuditApproveRequest(BaseModel):
    """审核通过请求"""
    pass


class AuditRejectRequest(BaseModel):
    """审核拒绝请求"""
    reason: str = Field(..., description="拒绝原因", min_length=1)


class AuditRegenerateRequest(BaseModel):
    """重新生成回复请求"""
    pass


class AuditActionResponse(BaseModel):
    """审核操作响应"""
    id: UUID
    status: str
    ai_reply: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    auditor_name: Optional[str] = None
    model_config = {"from_attributes": True}

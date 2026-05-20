"""
差评处理模块Schema定义
用于差评自动回复审核相关接口的请求和响应模型
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class NegativeReplyTaskResponse(BaseModel):
    """差评任务响应模型"""

    id: UUID = Field(..., description="任务ID")
    review_id: UUID = Field(..., description="评论ID")
    user_name: Optional[str] = Field(None, description="用户昵称")
    rating: int = Field(..., description="评分")
    content: Optional[str] = Field(None, description="评论内容")
    platform: str = Field(..., description="平台")
    ai_draft: Optional[str] = Field(None, description="AI草稿回复")
    risk: Optional[str] = Field(None, description="风险等级: high/medium/low")
    scores: Optional[dict] = Field(None, description="评分详情")
    status: str = Field(..., description="状态: pending/approved/rejected/sent")
    created_at: datetime = Field(..., description="创建时间")


class NegativeReplyTaskListResponse(BaseModel):
    """差评任务列表响应模型"""

    items: list[NegativeReplyTaskResponse] = Field(..., description="任务列表")
    total: int = Field(..., description="总数")
    page: int = Field(..., description="当前页")
    pageSize: int = Field(..., description="每页大小")


class NegativeReplyHistoryResponse(BaseModel):
    """差评处理历史响应模型"""

    id: UUID = Field(..., description="记录ID")
    review_id: UUID = Field(..., description="评论ID")
    user_name: Optional[str] = Field(None, description="用户昵称")
    content: Optional[str] = Field(None, description="评论内容")
    rating: int = Field(..., description="评分")
    platform: str = Field(..., description="平台")
    ai_draft: Optional[str] = Field(None, description="AI草稿")
    final_reply: Optional[str] = Field(None, description="最终回复")
    status: str = Field(..., description="状态")
    created_at: datetime = Field(..., description="创建时间")


class ApproveRequest(BaseModel):
    """批准请求模型"""

    pass


class RejectRequest(BaseModel):
    """驳回请求模型"""

    reason: str = Field(..., description="驳回原因")

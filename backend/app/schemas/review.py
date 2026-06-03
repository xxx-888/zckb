"""
评论相关 Schema
定义评论列表、详情、统计、筛选等请求/响应数据结构
"""

from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class ReviewResponse(BaseModel):
    """评论响应"""

    id: UUID
    store_id: UUID
    store_name: Optional[str] = None
    platform: str
    platform_review_id: str
    user_name: Optional[str] = None
    user_avatar: Optional[str] = None
    rating: int
    content: Optional[str] = None
    images: Optional[list[Union[str, dict]]] = None

    @field_validator("images", mode="before")
    @classmethod
    def normalize_images(cls, v):
        """将 images 中可能的 dict 对象转为 url 字符串"""
        if not v or not isinstance(v, list):
            return v
        result = []
        for item in v:
            if isinstance(item, str):
                result.append(item)
            elif isinstance(item, dict):
                url = item.get("url") or item.get("originUrl") or item.get("bigUrl") or item.get("thumbUrl") or ""
                result.append(url if url else str(item))
            else:
                result.append(str(item))
        return result
    sentiment: Optional[str] = None
    tags: Optional[list[str]] = None
    reply: Optional[str] = None
    reply_time: Optional[datetime] = None
    ai_generated: bool = False
    ai_reply_draft: Optional[str] = None
    risk_level: Optional[str] = None
    status: str = "normal"
    platform_created_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ReviewListResponse(BaseModel):
    """评论列表响应"""

    items: list[ReviewResponse]
    total: int
    page: int
    pageSize: int


class ReviewStatsResponse(BaseModel):
    """评论统计响应"""

    total_reviews: int = 0
    positive_count: int = 0
    negative_count: int = 0
    neutral_count: int = 0
    avg_rating: float = 0.0
    reply_rate: float = 0.0
    ai_reply_rate: float = 0.0
    period: Optional[str] = None


class ReviewCreateRequest(BaseModel):
    """创建评论请求"""

    store_id: UUID = Field(..., description="门店ID")
    platform: str = Field(..., description="来源平台")
    platform_review_id: str = Field(..., description="平台侧评论ID")
    user_name: Optional[str] = Field(None, description="评论者昵称")
    rating: int = Field(..., description="评分(1-5)", ge=1, le=5)
    content: Optional[str] = Field(None, description="评论内容")
    images: Optional[list[str]] = Field(None, description="评论图片URL列表")
    raw_json: Optional[dict] = Field(None, description="原始爬虫数据")


class ReviewUpdateRequest(BaseModel):
    """更新评论请求"""

    reply: Optional[str] = Field(None, description="商家回复内容")
    status: Optional[str] = Field(None, description="状态: normal/appealed/deleted")


class ReviewFilterParams(BaseModel):
    """评论筛选参数"""

    sentiment: Optional[str] = Field(None, description="情感: positive/negative/neutral")
    keyword: Optional[str] = Field(None, description="关键词搜索")
    store_id: Optional[UUID] = Field(None, description="门店ID")
    platform: Optional[str] = Field(None, description="来源平台")
    rating_min: Optional[int] = Field(None, description="最低评分", ge=1, le=5)
    rating_max: Optional[int] = Field(None, description="最高评分", ge=1, le=5)
    has_reply: Optional[bool] = Field(None, description="是否有回复")
    has_image: Optional[bool] = Field(None, description="是否有图片")
    start_date: Optional[str] = Field(None, description="开始日期(YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="结束日期(YYYY-MM-DD)")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")


class SimilarReviewResponse(BaseModel):
    """相似评论响应"""

    id: UUID
    user_name: Optional[str] = None
    content: Optional[str] = None
    rating: int
    sentiment: Optional[str] = None
    similarity_score: float = 0.0

    model_config = {"from_attributes": True}


class QuickReplyRequest(BaseModel):
    """快速回复请求"""

    reply_content: str = Field(..., description="回复内容", min_length=1)


class BatchDeleteRequest(BaseModel):
    """批量删除请求"""

    ids: list[UUID] = Field(..., description="评论ID列表", min_length=1)

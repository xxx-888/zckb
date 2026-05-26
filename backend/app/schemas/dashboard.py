"""
Dashboard 相关 Schema
定义仪表盘核心统计、平台分布、门店排行等响应数据结构
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CoreStatsResponse(BaseModel):
    """核心统计响应"""

    total_reviews: int = 0
    review_trend: float = 0.0
    avg_rating: float = 0.0
    rating_trend: float = 0.0
    positive_rate: float = 0.0
    positive_trend: float = 0.0
    ai_reply_rate: float = 0.0
    reply_trend: float = 0.0


class PlatformDistributionResponse(BaseModel):
    """平台分布响应"""

    platform: str
    count: int = 0
    percentage: float = 0.0
    color: str = "#1890ff"
    icon: str = ""


class RecentReviewResponse(BaseModel):
    """最新评论响应"""

    id: UUID
    store_name: Optional[str] = None
    user_name: Optional[str] = None
    content: Optional[str] = None
    rating: int
    sentiment: Optional[str] = None
    platform: str
    time: Optional[datetime] = None

    model_config = {"from_attributes": True}


class StoreRankingResponse(BaseModel):
    """门店排行响应"""

    name: str
    score: float = 0.0
    reviews: int = 0
    trend: float = 0.0
    health: str = "good"
    health_score: Optional[float] = None


class HealthStatusResponse(BaseModel):
    """数据源健康状态响应"""

    platform: str
    status: str = "normal"
    time: Optional[str] = None


class AlertResponse(BaseModel):
    """异常警告响应"""

    id: str
    type: str
    title: str
    description: str
    severity: str = "info"
    timestamp: Optional[str] = None


class StoreHealthResponse(BaseModel):
    """门店健康值响应"""

    store_id: UUID
    store_name: str
    health_score: float = 0.0
    review_count: int = 0
    avg_rating: float = 0.0
    reply_rate: float = 0.0
    trend: float = 0.0

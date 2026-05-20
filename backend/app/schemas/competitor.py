"""
竞对分析相关 Schema
定义竞品管理、分析任务、分析结果等请求/响应数据结构
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CompetitorResponse(BaseModel):
    """竞品响应"""

    id: UUID
    store_id: UUID
    name: str = Field(..., description="竞品名称")
    platform: str = Field(..., description="平台: meituan/dianping/douyin/taobao/jd")
    platform_store_id: Optional[str] = Field(None, description="平台侧门店ID")
    rating: Optional[float] = Field(None, description="评分")
    positive_rate: Optional[float] = Field(None, description="好评率")
    review_count: int = Field(0, description="评论数")
    trends_data: dict = Field(default_factory=dict, description="趋势数据")
    bad_tags: list[str] = Field(default_factory=list, description="差评标签列表")
    last_synced_at: Optional[datetime] = Field(None, description="最后同步时间")
    created_at: datetime

    model_config = {"from_attributes": True}


class CompetitorPlanResponse(BaseModel):
    """竞对分析套餐响应"""

    id: str = Field(..., description="套餐ID")
    name: str = Field(..., description="套餐名称")
    price: float = Field(..., description="价格")
    description: str = Field(..., description="套餐描述")
    features: list[str] = Field(default_factory=list, description="包含功能列表")
    competitor_count: int = Field(..., description="可分析竞品数量")
    analysis_depth: str = Field(..., description="分析深度: basic/standard/advanced")
    report_format: str = Field(..., description="报告格式: pdf/excel/json")


class CompetitorTaskResponse(BaseModel):
    """竞对分析任务响应"""

    id: UUID
    competitor_name: str = Field(..., description="竞品名称")
    platform: str = Field(..., description="平台")
    status: str = Field(..., description="状态: pending/collecting/analyzing/completed/failed")
    payment_status: str = Field(..., description="支付状态: unpaid/paid")
    price: float = Field(0.0, description="价格")
    result_data: Optional[dict] = Field(None, description="分析结果数据")
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class CompetitorTaskCreateRequest(BaseModel):
    """创建竞对分析任务请求"""

    competitor_id: UUID = Field(..., description="竞品ID")
    plan_id: str = Field(..., description="套餐ID")


class CompetitorCreateRequest(BaseModel):
    """创建竞品请求"""

    store_id: UUID = Field(..., description="门店ID")
    name: str = Field(..., description="竞品名称", min_length=1, max_length=255)
    platform: str = Field(..., description="平台: meituan/dianping/douyin/taobao/jd")
    platform_store_id: Optional[str] = Field(None, description="平台侧门店ID", max_length=100)


class CompetitorAnalysisResultResponse(BaseModel):
    """竞对分析结果响应"""

    overview: dict = Field(default_factory=dict, description="概览对比")
    rating_comparison: dict = Field(default_factory=dict, description="评分对比")
    sentiment_comparison: dict = Field(default_factory=dict, description="情感对比")
    keyword_analysis: dict = Field(default_factory=dict, description="关键词分析")
    strength_weakness: dict = Field(default_factory=dict, description="优劣势分析")
    recommendations: list[str] = Field(default_factory=list, description="改进建议")


class CompetitorDetailResponse(BaseModel):
    """竞品详情响应"""

    id: UUID
    store_id: UUID
    name: str
    platform: str
    platform_store_id: Optional[str]
    rating: Optional[float]
    positive_rate: Optional[float]
    review_count: int
    trends_data: dict
    bad_tags: list[str]
    last_synced_at: Optional[datetime]
    recent_reviews: list[dict] = Field(default_factory=list, description="最近评论")
    analysis_history: list[dict] = Field(default_factory=list, description="分析历史")

    model_config = {"from_attributes": True}


class CompetitorListResponse(BaseModel):
    """竞品列表响应"""

    items: list[CompetitorResponse]
    total: int


class CompetitorTaskListResponse(BaseModel):
    """竞对分析任务列表响应"""

    items: list[CompetitorTaskResponse]
    total: int


class GenerateReportRequest(BaseModel):
    """生成分析报告请求"""

    competitor_id: UUID = Field(..., description="竞品ID")
    analysis_type: str = Field("full", description="分析类型: full/quick/custom")


class CompetitorSyncRequest(BaseModel):
    """同步竞品数据请求"""

    competitor_id: UUID = Field(..., description="竞品ID")

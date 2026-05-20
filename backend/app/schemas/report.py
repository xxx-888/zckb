"""
报告相关 Schema
定义年度报告、周报等请求/响应数据结构
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class YearlyDataResponse(BaseModel):
    """年度数据响应"""

    year: int = Field(..., description="年份")
    total_reviews: int = Field(0, description="评论总数")
    average_rating: float = Field(0.0, description="平均评分")
    sentiment_distribution: dict = Field(default_factory=dict, description="情感分布")
    reply_stats: dict = Field(default_factory=dict, description="回复统计")
    monthly_data: list[dict] = Field(default_factory=list, description="月度数据")
    top_keywords: list[dict] = Field(default_factory=list, description="热门关键词")
    category_scores: dict = Field(default_factory=dict, description="分类评分")


class ReportInsightsResponse(BaseModel):
    """报告洞察响应"""

    year_over_year: dict = Field(default_factory=dict, description="同比数据")
    highlights: list[str] = Field(default_factory=list, description="亮点")
    improvements: list[str] = Field(default_factory=list, description="改进点")
    ai_summary: str = Field("", description="AI摘要")
    personality_type: Optional[str] = Field(None, description="店铺个性类型")
    recommendations: list[str] = Field(default_factory=list, description="建议")


class AnnualReportResponse(BaseModel):
    """年度报告响应"""

    id: UUID
    store_id: UUID
    year: int
    data: YearlyDataResponse
    insights: ReportInsightsResponse
    generated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class WeeklyBriefResponse(BaseModel):
    """周报响应"""

    id: UUID
    store_id: UUID
    week_start: datetime
    week_end: datetime
    total_reviews: int = Field(0, description="本周评论总数")
    positive_count: int = Field(0, description="正面评论数")
    negative_count: int = Field(0, description="负面评论数")
    neutral_count: int = Field(0, description="中性评论数")
    avg_rating: Optional[float] = Field(None, description="平均评分")
    top_issues: list[str] = Field(default_factory=list, description="主要问题列表")
    top_praises: list[str] = Field(default_factory=list, description="主要好评列表")
    dish_analysis: dict = Field(default_factory=dict, description="菜品分析")
    ai_summary: Optional[str] = Field(None, description="AI摘要")
    generated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class GenerateReportRequest(BaseModel):
    """生成报告请求"""

    store_id: UUID = Field(..., description="门店ID")
    year: int = Field(..., description="年份", ge=2000, le=2100)


class AllYearsDataResponse(BaseModel):
    """所有年份数据响应"""

    years: list[int] = Field(default_factory=list, description="有数据的年份列表")
    data: list[dict] = Field(default_factory=list, description="各年份简要数据")


class WeeklyBriefFilterParams(BaseModel):
    """周报筛选参数"""

    store_id: UUID = Field(..., description="门店ID")
    week_start: Optional[str] = Field(None, description="周开始日期(YYYY-MM-DD)")

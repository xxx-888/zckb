"""
经营看板 Schema
定义营业额、套餐核销、运营指标、分析意见的请求/响应数据结构
"""

from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ==================== 营业额记录 ====================

class RevenueRecordCreate(BaseModel):
    """创建营业额记录"""
    store_id: UUID = Field(..., description="门店ID")
    record_date: date = Field(..., description="记录日期")
    total_revenue: float = Field(0, description="总营业额")
    meituan_revenue: float = Field(0, description="美团营业额")
    douyin_revenue: float = Field(0, description="抖音营业额")
    other_revenue: float = Field(0, description="其他收入")
    visitor_count: int = Field(0, description="到店人数")
    table_count: int = Field(0, description="接待桌数")
    avg_people_per_table: float = Field(0, description="桌均人数")
    avg_per_capita: float = Field(0, description="人均消费")
    notes: Optional[str] = Field(None, description="备注")


class RevenueRecordUpdate(BaseModel):
    """更新营业额记录"""
    total_revenue: Optional[float] = None
    meituan_revenue: Optional[float] = None
    douyin_revenue: Optional[float] = None
    other_revenue: Optional[float] = None
    visitor_count: Optional[int] = None
    table_count: Optional[int] = None
    avg_people_per_table: Optional[float] = None
    avg_per_capita: Optional[float] = None
    notes: Optional[str] = None


class RevenueRecordResponse(BaseModel):
    """营业额记录响应"""
    id: UUID
    store_id: UUID
    record_date: date
    total_revenue: float
    meituan_revenue: float
    douyin_revenue: float
    other_revenue: float
    visitor_count: int
    table_count: int
    avg_people_per_table: float
    avg_per_capita: float
    notes: Optional[str] = None
    created_at: str

    model_config = {"from_attributes": True}


class RevenueBatchCreate(BaseModel):
    """批量创建营业额记录"""
    records: list[RevenueRecordCreate] = Field(..., description="营业额记录列表")


# ==================== 营业额聚合 ====================

class RevenueSummary(BaseModel):
    """营业额汇总（含环比）"""
    total_revenue: float
    meituan_revenue: float
    douyin_revenue: float
    other_revenue: float
    visitor_count: int
    table_count: int
    avg_people_per_table: float
    avg_per_capita: float
    # 环比
    mom_revenue_change: Optional[float] = Field(None, description="营业额环比变化率")
    mom_visitor_change: Optional[float] = Field(None, description="到店人数环比变化率")
    mom_table_change: Optional[float] = Field(None, description="桌数环比变化率")
    period_label: str
    compare_period_label: Optional[str] = None


class DailyRevenueRow(BaseModel):
    """日营业额趋势行"""
    date: str
    total_revenue: float
    meituan_revenue: float
    douyin_revenue: float
    other_revenue: float
    visitor_count: int
    table_count: int
    avg_people_per_table: float
    avg_per_capita: float


class RevenueTrendResponse(BaseModel):
    """营业额趋势响应"""
    daily: list[DailyRevenueRow]
    weekly: list[DailyRevenueRow]


# ==================== 套餐核销记录 ====================

class PackageRecordCreate(BaseModel):
    """创建套餐核销记录"""
    store_id: UUID = Field(..., description="门店ID")
    period_start: date = Field(..., description="周期开始日期")
    period_end: date = Field(..., description="周期结束日期")
    product_name: str = Field(..., description="商品名称")
    meituan_buy: int = Field(0, description="美团购买数")
    meituan_verify: int = Field(0, description="美团核销券数")
    douyin_buy: int = Field(0, description="抖音购买数")
    douyin_verify: int = Field(0, description="抖音核销券数")
    notes: Optional[str] = Field(None, description="备注")


class PackageRecordUpdate(BaseModel):
    """更新套餐核销记录"""
    product_name: Optional[str] = None
    meituan_buy: Optional[int] = None
    meituan_verify: Optional[int] = None
    douyin_buy: Optional[int] = None
    douyin_verify: Optional[int] = None
    notes: Optional[str] = None


class PackageRecordResponse(BaseModel):
    """套餐核销记录响应"""
    id: UUID
    store_id: UUID
    period_start: date
    period_end: date
    product_name: str
    meituan_buy: int
    meituan_verify: int
    douyin_buy: int
    douyin_verify: int
    notes: Optional[str] = None
    created_at: str

    model_config = {"from_attributes": True}


class PackageBatchCreate(BaseModel):
    """批量创建套餐核销记录"""
    records: list[PackageRecordCreate] = Field(..., description="套餐核销记录列表")


class PackageItem(BaseModel):
    """套餐汇总项"""
    product_name: str
    meituan_buy: int = 0
    meituan_verify: int = 0
    douyin_buy: int = 0
    douyin_verify: int = 0
    total_buy: int = 0
    total_verify: int = 0
    verify_rate: float = 0


class PackagePeriodSummary(BaseModel):
    """某周期套餐汇总"""
    period_start: date
    period_end: date
    period_label: str
    items: list[PackageItem]
    total_meituan_buy: int = 0
    total_meituan_verify: int = 0
    total_douyin_buy: int = 0
    total_douyin_verify: int = 0


class PackageComparisonResponse(BaseModel):
    """套餐双周期对比响应"""
    store_name: str
    current_period: PackagePeriodSummary
    compare_period: Optional[PackagePeriodSummary] = None


class PackageRankingResponse(BaseModel):
    """套餐排行响应"""
    top_ranking: list[PackageItem]
    bottom_ranking: list[PackageItem]
    overall_summary: dict


# ==================== 门店运营指标 ====================

class StoreMetricCreate(BaseModel):
    """创建门店运营指标"""
    store_id: UUID = Field(..., description="门店ID")
    metric_date: date = Field(..., description="指标日期")
    platform: str = Field(..., description="平台名称")
    ranking_name: Optional[str] = None
    ranking_position: Optional[str] = None
    prev_ranking_position: Optional[str] = None
    star_rating: Optional[float] = None
    prev_star_rating: Optional[float] = None
    impressions: Optional[int] = None
    visits: Optional[int] = None
    purchases: Optional[int] = None
    verifications: Optional[int] = None
    new_favorites: Optional[int] = None
    checkins: Optional[int] = None
    scan_count: Optional[int] = None
    product_impressions: Optional[int] = None
    product_visits: Optional[int] = None
    product_purchases: Optional[int] = None
    new_reviews: Optional[int] = None
    new_bad_reviews: Optional[int] = None
    bad_keywords: Optional[list[str]] = None
    notes: Optional[str] = None


class StoreMetricUpdate(BaseModel):
    """更新门店运营指标"""
    ranking_name: Optional[str] = None
    ranking_position: Optional[str] = None
    prev_ranking_position: Optional[str] = None
    star_rating: Optional[float] = None
    prev_star_rating: Optional[float] = None
    impressions: Optional[int] = None
    visits: Optional[int] = None
    purchases: Optional[int] = None
    verifications: Optional[int] = None
    new_favorites: Optional[int] = None
    checkins: Optional[int] = None
    scan_count: Optional[int] = None
    product_impressions: Optional[int] = None
    product_visits: Optional[int] = None
    product_purchases: Optional[int] = None
    new_reviews: Optional[int] = None
    new_bad_reviews: Optional[int] = None
    bad_keywords: Optional[list[str]] = None
    notes: Optional[str] = None


class StoreMetricResponse(BaseModel):
    """门店运营指标响应"""
    id: UUID
    store_id: UUID
    metric_date: date
    platform: str
    ranking_name: Optional[str] = None
    ranking_position: Optional[str] = None
    prev_ranking_position: Optional[str] = None
    star_rating: Optional[float] = None
    prev_star_rating: Optional[float] = None
    impressions: Optional[int] = None
    visits: Optional[int] = None
    purchases: Optional[int] = None
    verifications: Optional[int] = None
    new_favorites: Optional[int] = None
    checkins: Optional[int] = None
    scan_count: Optional[int] = None
    product_impressions: Optional[int] = None
    product_visits: Optional[int] = None
    product_purchases: Optional[int] = None
    new_reviews: Optional[int] = None
    new_bad_reviews: Optional[int] = None
    bad_keywords: Optional[list[str]] = None
    notes: Optional[str] = None
    created_at: str

    model_config = {"from_attributes": True}


class StoreMetricBatchCreate(BaseModel):
    """批量创建门店运营指标"""
    records: list[StoreMetricCreate] = Field(..., description="运营指标记录列表")


class MetricCompareItem(BaseModel):
    """指标对比项"""
    name: str
    current_value: str
    compare_value: Optional[str] = None
    mom_change: Optional[str] = None
    highlight: Optional[str] = None


class PlatformMetricsResponse(BaseModel):
    """平台指标聚合响应"""
    platform: str
    metrics: list[MetricCompareItem]


class StoreHealthResponse(BaseModel):
    """门店健康度响应"""
    funnels: list[dict]
    rankings: list[dict]
    reviews_summary: list[dict]
    daily_metrics: list[dict]


# ==================== 运营分析意见 ====================

class OperationAnalysisCreate(BaseModel):
    """创建运营分析"""
    store_id: UUID = Field(..., description="门店ID")
    period_start: date = Field(..., description="周期开始日期")
    period_end: date = Field(..., description="周期结束日期")
    analysis_opinion: str = Field("", description="分析意见")
    goals: list[str] = Field(default_factory=list, description="下周目标列表")


class OperationAnalysisUpdate(BaseModel):
    """更新运营分析"""
    analysis_opinion: Optional[str] = None
    goals: Optional[list[str]] = None


class OperationAnalysisResponse(BaseModel):
    """运营分析响应"""
    id: UUID
    store_id: UUID
    period_start: date
    period_end: date
    analysis_opinion: str
    goals: list[str]
    created_at: str

    model_config = {"from_attributes": True}


# ==================== 看板聚合 ====================

class DashboardOverviewResponse(BaseModel):
    """看板完整概览响应"""
    revenue: RevenueSummary
    business_metrics: dict
    package_comparison: Optional[PackageComparisonResponse] = None
    operation_analysis: Optional[OperationAnalysisResponse] = None
    operation_metrics: Optional[dict] = None

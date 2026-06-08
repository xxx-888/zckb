"""
经营看板 API 路由
提供营业额、套餐核销、运营指标、分析意见的CRUD接口和聚合查询
"""

from datetime import date, timedelta
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_active_user, require_valid_subscription
from app.core.response import error, paginated, success
from app.models.store import Store
from app.models.store_dashboard import (
    OperationAnalysis,
    PackageRecord,
    RevenueRecord,
    StoreMetric,
)
from app.models.user import User, UserStore
from app.schemas.store_dashboard import (
    DashboardOverviewResponse,
    OperationAnalysisCreate,
    OperationAnalysisResponse,
    OperationAnalysisUpdate,
    PackageBatchCreate,
    PackageComparisonResponse,
    PackageRankingResponse,
    PackageRecordCreate,
    PackageRecordResponse,
    PackageRecordUpdate,
    RevenueBatchCreate,
    RevenueRecordCreate,
    RevenueRecordResponse,
    RevenueRecordUpdate,
    RevenueSummary,
    RevenueTrendResponse,
    StoreHealthResponse,
    StoreMetricBatchCreate,
    StoreMetricCreate,
    StoreMetricResponse,
    StoreMetricUpdate,
)
from app.services import store_dashboard_service as svc

router = APIRouter(prefix="/store-dashboard", tags=["经营看板"])


# ==================== 工具依赖 ====================

async def _get_store_ids(
    user: User,
    db: AsyncSession,
    store_id: Optional[UUID] = None,
) -> list[UUID]:
    """获取用户可访问的门店ID列表"""
    all_ids = await svc._fetch_user_store_ids(db, user)
    if store_id:
        if store_id in all_ids:
            return [store_id]
        return []
    return all_ids if all_ids else []


def _parse_date(val: Optional[str]) -> Optional[date]:
    if not val:
        return None
    try:
        return date.fromisoformat(val)
    except (ValueError, TypeError):
        return None


def _record_to_dict(record) -> dict:
    """将 ORM 对象转换为字典"""
    d = {}
    for col in record.__table__.columns:
        val = getattr(record, col.name)
        if hasattr(val, "isoformat"):
            val = val.isoformat()
        d[col.name] = val
    return d


# ==================== 营业额接口 ====================

@router.post("/revenue")
async def create_revenue(
    data: RevenueRecordCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """创建营业额记录"""
    record = RevenueRecord(**data.model_dump(), created_by=user.id)
    result = await svc.create_revenue_record(db, record, user)
    return success(_record_to_dict(result), "创建成功")


@router.post("/revenue/batch")
async def batch_create_revenue(
    data: RevenueBatchCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """批量创建营业额记录"""
    records = [RevenueRecord(**r.model_dump(), created_by=user.id) for r in data.records]
    count = await svc.batch_create_revenue_records(db, records, user)
    return success({"count": count}, f"成功创建{count}条记录")


@router.get("/revenue")
async def list_revenue(
    store_id: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """查询营业额记录（分页）"""
    store_ids = await _get_store_ids(user, db, UUID(store_id) if store_id else None)
    if not store_ids:
        return success({"items": [], "total": 0})
    records, total = await svc.get_revenue_records(
        db, store_ids, _parse_date(start_date), _parse_date(end_date), page, page_size
    )
    items = [_record_to_dict(r) for r in records]
    return paginated(items, total, page, page_size)


@router.put("/revenue/{record_id}")
async def update_revenue(
    record_id: UUID,
    data: RevenueRecordUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """更新营业额记录"""
    record = await svc.update_revenue_record(db, record_id, user, **data.model_dump(exclude_unset=True))
    if not record:
        return error("记录不存在")
    return success(_record_to_dict(record), "更新成功")


@router.delete("/revenue/{record_id}")
async def delete_revenue(
    record_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """删除营业额记录"""
    ok = await svc.delete_revenue_record(db, record_id)
    if not ok:
        return error("记录不存在")
    return success(None, "删除成功")


@router.get("/revenue/summary")
async def revenue_summary(
    store_id: Optional[str] = Query(None),
    start_date: str = Query(..., description="当期开始日期 YYYY-MM-DD"),
    end_date: str = Query(..., description="当期结束日期 YYYY-MM-DD"),
    compare_start: Optional[str] = Query(None, description="对比期开始日期"),
    compare_end: Optional[str] = Query(None, description="对比期结束日期"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """营业额汇总（含环比）"""
    store_ids = await _get_store_ids(user, db, UUID(store_id) if store_id else None)
    if not store_ids:
        return success(None)
    result = await svc.get_revenue_summary(
        db, store_ids,
        date.fromisoformat(start_date), date.fromisoformat(end_date),
        _parse_date(compare_start), _parse_date(compare_end),
    )
    return success(result)


@router.get("/revenue/trend")
async def revenue_trend(
    store_id: Optional[str] = Query(None),
    start_date: str = Query(...),
    end_date: str = Query(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """营业额趋势（日+周）"""
    store_ids = await _get_store_ids(user, db, UUID(store_id) if store_id else None)
    if not store_ids:
        return success({"daily": [], "weekly": []})
    result = await svc.get_revenue_trend(
        db, store_ids,
        date.fromisoformat(start_date), date.fromisoformat(end_date),
    )
    return success(result)


# ==================== 套餐核销接口 ====================

@router.post("/packages")
async def create_package(
    data: PackageRecordCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """创建套餐核销记录"""
    record = PackageRecord(**data.model_dump(), created_by=user.id)
    result = await svc.create_package_record(db, record, user)
    return success(_record_to_dict(result), "创建成功")


@router.post("/packages/batch")
async def batch_create_packages(
    data: PackageBatchCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """批量创建套餐核销记录"""
    records = [PackageRecord(**r.model_dump(), created_by=user.id) for r in data.records]
    count = await svc.batch_create_package_records(db, records, user)
    return success({"count": count}, f"成功创建{count}条记录")


@router.get("/packages")
async def list_packages(
    store_id: Optional[str] = Query(None),
    period_start: Optional[str] = Query(None),
    period_end: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """查询套餐核销记录（分页）"""
    store_ids = await _get_store_ids(user, db, UUID(store_id) if store_id else None)
    if not store_ids:
        return success({"items": [], "total": 0})
    records, total = await svc.get_package_records(
        db, store_ids, _parse_date(period_start), _parse_date(period_end), page, page_size
    )
    items = [_record_to_dict(r) for r in records]
    return paginated(items, total, page, page_size)


@router.put("/packages/{record_id}")
async def update_package(
    record_id: UUID,
    data: PackageRecordUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """更新套餐核销记录"""
    record = await svc.update_package_record(db, record_id, **data.model_dump(exclude_unset=True))
    if not record:
        return error("记录不存在")
    return success(_record_to_dict(record), "更新成功")


@router.delete("/packages/{record_id}")
async def delete_package(
    record_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """删除套餐核销记录"""
    ok = await svc.delete_package_record(db, record_id)
    if not ok:
        return error("记录不存在")
    return success(None, "删除成功")


@router.get("/packages/comparison")
async def package_comparison(
    store_id: Optional[str] = Query(None),
    current_start: str = Query(..., description="当期开始"),
    current_end: str = Query(..., description="当期结束"),
    compare_start: Optional[str] = Query(None, description="对比期开始"),
    compare_end: Optional[str] = Query(None, description="对比期结束"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """套餐双周期对比"""
    store_ids = await _get_store_ids(user, db, UUID(store_id) if store_id else None)
    if not store_ids:
        return success(None)
    result = await svc.get_package_comparison(
        db, store_ids,
        date.fromisoformat(current_start), date.fromisoformat(current_end),
        _parse_date(compare_start), _parse_date(compare_end),
    )
    return success(result)


@router.get("/packages/ranking")
async def package_ranking(
    store_id: Optional[str] = Query(None),
    start_date: str = Query(...),
    end_date: str = Query(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """套餐排行（Top5+Bottom5）"""
    store_ids = await _get_store_ids(user, db, UUID(store_id) if store_id else None)
    if not store_ids:
        return success(None)
    result = await svc.get_package_ranking(
        db, store_ids,
        date.fromisoformat(start_date), date.fromisoformat(end_date),
    )
    return success(result)


# ==================== 门店运营指标接口 ====================

@router.post("/metrics")
async def create_metric(
    data: StoreMetricCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """创建门店运营指标"""
    metric = StoreMetric(**data.model_dump(), created_by=user.id)
    result = await svc.create_store_metric(db, metric, user)
    return success(_record_to_dict(result), "创建成功")


@router.post("/metrics/batch")
async def batch_create_metrics(
    data: StoreMetricBatchCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """批量创建门店运营指标"""
    metrics = [StoreMetric(**m.model_dump(), created_by=user.id) for m in data.records]
    count = await svc.batch_create_store_metrics(db, metrics, user)
    return success({"count": count}, f"成功创建{count}条记录")


@router.get("/metrics")
async def list_metrics(
    store_id: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    platform: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """查询门店运营指标（分页）"""
    store_ids = await _get_store_ids(user, db, UUID(store_id) if store_id else None)
    if not store_ids:
        return success({"items": [], "total": 0})
    records, total = await svc.get_store_metrics(
        db, store_ids, _parse_date(start_date), _parse_date(end_date), platform, page, page_size
    )
    items = [_record_to_dict(r) for r in records]
    return paginated(items, total, page, page_size)


@router.put("/metrics/{metric_id}")
async def update_metric(
    metric_id: UUID,
    data: StoreMetricUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """更新门店运营指标"""
    metric = await svc.update_store_metric(db, metric_id, **data.model_dump(exclude_unset=True))
    if not metric:
        return error("记录不存在")
    return success(_record_to_dict(metric), "更新成功")


@router.delete("/metrics/{metric_id}")
async def delete_metric(
    metric_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """删除门店运营指标"""
    ok = await svc.delete_store_metric(db, metric_id)
    if not ok:
        return error("记录不存在")
    return success(None, "删除成功")


@router.get("/metrics/health")
async def store_health(
    store_id: Optional[str] = Query(None),
    start_date: str = Query(...),
    end_date: str = Query(...),
    compare_start: Optional[str] = Query(None),
    compare_end: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """门店运营健康度"""
    store_ids = await _get_store_ids(user, db, UUID(store_id) if store_id else None)
    if not store_ids:
        return success(None)
    result = await svc.get_store_health(
        db, store_ids,
        date.fromisoformat(start_date), date.fromisoformat(end_date),
        _parse_date(compare_start), _parse_date(compare_end),
    )
    return success(result)


# ==================== 运营分析意见接口 ====================

@router.post("/analysis")
async def create_analysis(
    data: OperationAnalysisCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """创建运营分析"""
    analysis = OperationAnalysis(**data.model_dump(), created_by=user.id)
    result = await svc.create_operation_analysis(db, analysis, user)
    return success(_record_to_dict(result), "创建成功")


@router.get("/analysis")
async def list_analysis(
    store_id: Optional[str] = Query(None),
    period_start: Optional[str] = Query(None),
    period_end: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """查询运营分析意见"""
    store_ids = await _get_store_ids(user, db, UUID(store_id) if store_id else None)
    if not store_ids:
        return success([])
    records = await svc.get_operation_analyses(
        db, store_ids, _parse_date(period_start), _parse_date(period_end)
    )
    items = [_record_to_dict(r) for r in records]
    return success(items)


@router.put("/analysis/{analysis_id}")
async def update_analysis(
    analysis_id: UUID,
    data: OperationAnalysisUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """更新运营分析"""
    analysis = await svc.update_operation_analysis(
        db, analysis_id, **data.model_dump(exclude_unset=True)
    )
    if not analysis:
        return error("记录不存在")
    return success(_record_to_dict(analysis), "更新成功")


@router.delete("/analysis/{analysis_id}")
async def delete_analysis(
    analysis_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """删除运营分析"""
    ok = await svc.delete_operation_analysis(db, analysis_id)
    if not ok:
        return error("记录不存在")
    return success(None, "删除成功")


# ==================== 看板聚合接口 ====================

@router.get("/overview")
async def dashboard_overview(
    store_id: Optional[str] = Query(None),
    start_date: str = Query(..., description="当期开始"),
    end_date: str = Query(..., description="当期结束"),
    compare_start: Optional[str] = Query(None),
    compare_end: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """看板完整概览（并发聚合）"""
    store_ids = await _get_store_ids(user, db, UUID(store_id) if store_id else None)
    if not store_ids:
        return success(None)
    result = await svc.get_dashboard_overview(
        db, user, store_ids,
        date.fromisoformat(start_date), date.fromisoformat(end_date),
        _parse_date(compare_start), _parse_date(compare_end),
    )
    return success(result)

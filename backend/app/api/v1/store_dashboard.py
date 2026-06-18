"""
经营看板 API 路由
提供营业额、套餐核销、运营指标、分析意见的CRUD接口和聚合查询
"""

import logging

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
logger = logging.getLogger(__name__)


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


def _default_week_range():
    """默认本周一到今天"""
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    return monday, today


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
    start_date: Optional[str] = Query(None, description="当期开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="当期结束日期 YYYY-MM-DD"),
    compare_start: Optional[str] = Query(None, description="对比期开始日期"),
    compare_end: Optional[str] = Query(None, description="对比期结束日期"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """营业额汇总（含环比）"""
    store_ids = await _get_store_ids(user, db, UUID(store_id) if store_id else None)
    if not store_ids:
        return success(None)
    _s = _parse_date(start_date) or _default_week_range()[0]
    _e = _parse_date(end_date) or _default_week_range()[1]
    result = await svc.get_revenue_summary(
        db, store_ids, _s, _e,
        _parse_date(compare_start), _parse_date(compare_end),
    )
    return success(result)


@router.get("/revenue/trend")
async def revenue_trend(
    store_id: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """营业额趋势（日+周）"""
    store_ids = await _get_store_ids(user, db, UUID(store_id) if store_id else None)
    if not store_ids:
        return success({"daily": [], "weekly": []})
    _s = _parse_date(start_date) or _default_week_range()[0]
    _e = _parse_date(end_date) or _default_week_range()[1]
    result = await svc.get_revenue_trend(
        db, store_ids, _s, _e,
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
    current_start: Optional[str] = Query(None, description="当期开始"),
    current_end: Optional[str] = Query(None, description="当期结束"),
    compare_start: Optional[str] = Query(None, description="对比期开始"),
    compare_end: Optional[str] = Query(None, description="对比期结束"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """套餐双周期对比"""
    store_ids = await _get_store_ids(user, db, UUID(store_id) if store_id else None)
    if not store_ids:
        return success(None)
    _s = _parse_date(current_start) or _default_week_range()[0]
    _e = _parse_date(current_end) or _default_week_range()[1]
    result = await svc.get_package_comparison(
        db, store_ids, _s, _e,
        _parse_date(compare_start), _parse_date(compare_end),
    )
    return success(result)


@router.get("/packages/ranking")
async def package_ranking(
    store_id: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """套餐排行（Top5+Bottom5）"""
    store_ids = await _get_store_ids(user, db, UUID(store_id) if store_id else None)
    if not store_ids:
        return success(None)
    _s = _parse_date(start_date) or _default_week_range()[0]
    _e = _parse_date(end_date) or _default_week_range()[1]
    result = await svc.get_package_ranking(
        db, store_ids, _s, _e,
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
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    compare_start: Optional[str] = Query(None),
    compare_end: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """门店运营健康度"""
    store_ids = await _get_store_ids(user, db, UUID(store_id) if store_id else None)
    if not store_ids:
        return success(None)
    _s = _parse_date(start_date) or _default_week_range()[0]
    _e = _parse_date(end_date) or _default_week_range()[1]
    result = await svc.get_store_health(
        db, store_ids, _s, _e,
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
    start_date: Optional[str] = Query(None, description="当期开始(YYYY-MM-DD)，不传默认本周"),
    end_date: Optional[str] = Query(None, description="当期结束(YYYY-MM-DD)，不传默认本周"),
    compare_start: Optional[str] = Query(None),
    compare_end: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """看板完整概览（并发聚合）"""
    store_ids = await _get_store_ids(user, db, UUID(store_id) if store_id else None)
    if not store_ids:
        return success(None)
    # 默认本周一 ~ 今天
    _start = _parse_date(start_date)
    _end = _parse_date(end_date)
    if not _start or not _end:
        today = date.today()
        _start = today - timedelta(days=today.weekday())
        _end = today
    result = await svc.get_dashboard_overview(
        db, user, store_ids,
        _start, _end,
        _parse_date(compare_start), _parse_date(compare_end),
    )
    return success(result)


# ==================== 仪表盘数据同步接口 ====================

@router.post("/sync")
async def sync_dashboard(
    store_id: Optional[str] = Query(None, description="门店ID，不传则同步用户所有门店"),
    start_date: Optional[str] = Query(None, description="同步开始日期，不传默认本周一"),
    end_date: Optional[str] = Query(None, description="同步结束日期，不传默认今天"),
    platform: Optional[str] = Query(None, description="指定平台(meituan/douyin/all)，不传则同步所有已连接平台"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """
    同步平台仪表盘数据到经营看板

    根据用户已连接的平台账号，从美团开店宝/抖音来客拉取营业额、套餐核销、门店指标数据。
    同步后数据自动写入 RevenueRecord / StoreMetric / PackageRecord 表。

    注意：此接口使用 Playwright 浏览器环境调用平台 API，启动浏览器约需 10-30 秒，
    数据获取约需 30-120 秒，请设置足够的超时时间（建议 180 秒以上）。
    """
    from app.services.dashboard_sync_service import DashboardSyncService

    _start = _parse_date(start_date)
    _end = _parse_date(end_date)
    if not _start or not _end:
        today = date.today()
        _start = today - timedelta(days=today.weekday())
        _end = today

    sync_svc = DashboardSyncService(db)
    _store_id = UUID(store_id) if store_id else None

    logger.info(f"📊 [同步API] 收到同步请求 | platform={platform} | store_id={store_id} | {_start}~{_end}")
    print(f"\n{'='*60}", flush=True)
    print(f"📊 [同步API] 收到同步请求 | platform={platform or 'all'} | store_id={store_id or 'all'} | {_start}~{_end}", flush=True)
    print(f"{'='*60}", flush=True)

    if platform and platform != "all":
        # 同步指定平台
        from app.models.store import PlatformAccount

        stmt = select(PlatformAccount).where(
            PlatformAccount.user_id == user.id,
            PlatformAccount.platform == platform,
            PlatformAccount.cookies_status == "valid",
        )
        result = await db.execute(stmt)
        account = result.scalar_one_or_none()

        if not account:
            logger.warning(f"📊 [同步API] 未找到有效的 {platform} 平台账号")
            return error(f"未找到有效的 {platform} 平台账号，请先连接平台")

        if platform == "meituan":
            sync_result = await sync_svc.sync_meituan_dashboard(
                account.id, _start, _end, _store_id
            )
        elif platform == "douyin":
            sync_result = await sync_svc.sync_douyin_dashboard(
                account.id, _start, _end, _store_id
            )
        else:
            return error(f"不支持的平台: {platform}")

        return success(sync_result)
    else:
        # 同步所有已连接平台
        logger.info(f"📊 [同步API] 开始全平台同步")
        sync_result = await sync_svc.sync_all_platforms(
            user.id, _start, _end, _store_id
        )
        logger.info(f"📊 [同步API] 全平台同步完成: success={sync_result.get('success')}")
        print(f"\n📊 [同步API] 全平台同步完成: success={sync_result.get('success')}", flush=True)
        if sync_result.get("summary"):
            s = sync_result["summary"]
            print(f"  平台数={s.get('platforms_synced')}, 营业额={s.get('total_revenue_records')}, 指标={s.get('total_metric_records')}, 套餐={s.get('total_package_records')}", flush=True)
        return success(sync_result)


@router.post("/sync/{account_id}")
async def sync_account_dashboard(
    account_id: UUID,
    start_date: Optional[str] = Query(None, description="同步开始日期"),
    end_date: Optional[str] = Query(None, description="同步结束日期"),
    store_id: Optional[str] = Query(None, description="门店ID"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_valid_subscription),
):
    """
    按平台账号ID同步仪表盘数据

    适用于用户有多个同平台账号的情况，可精确指定同步哪个账号。
    """
    from app.services.dashboard_sync_service import DashboardSyncService
    from app.models.store import PlatformAccount

    _start = _parse_date(start_date)
    _end = _parse_date(end_date)
    if not _start or not _end:
        today = date.today()
        _start = today - timedelta(days=today.weekday())
        _end = today

    _store_id = UUID(store_id) if store_id else None

    # 验证账号属于当前用户
    stmt = select(PlatformAccount).where(
        PlatformAccount.id == account_id,
        PlatformAccount.user_id == user.id,
    )
    result = await db.execute(stmt)
    account = result.scalar_one_or_none()

    if not account:
        return error("平台账号不存在或不属于当前用户")

    sync_svc = DashboardSyncService(db)

    if account.platform in ("meituan", "dianping"):
        sync_result = await sync_svc.sync_meituan_dashboard(
            account_id, _start, _end, _store_id
        )
    elif account.platform == "douyin":
        sync_result = await sync_svc.sync_douyin_dashboard(
            account_id, _start, _end, _store_id
        )
    else:
        return error(f"不支持的平台: {account.platform}")

    return success(sync_result)

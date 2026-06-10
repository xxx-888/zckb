"""
后台经营数据管理 API
管理员可录入/编辑/删除所有门店的营业额、套餐核销、运营指标、分析意见
支持 Excel 周报文件一键导入
"""

from datetime import date
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, UploadFile, File
from sqlalchemy import select, func, delete as sa_delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import require_roles
from app.core.response import error, paginated, success
from app.models.store import Store
from app.models.store_dashboard import (
    OperationAnalysis,
    PackageRecord,
    RevenueRecord,
    StoreMetric,
)
from app.models.user import User
from app.schemas.store_dashboard import (
    OperationAnalysisCreate,
    OperationAnalysisUpdate,
    PackageBatchCreate,
    PackageRecordCreate,
    PackageRecordUpdate,
    RevenueBatchCreate,
    RevenueRecordCreate,
    RevenueRecordUpdate,
    StoreMetricBatchCreate,
    StoreMetricCreate,
    StoreMetricUpdate,
)
from app.services import store_dashboard_service as svc
from app.services.excel_parser import parse_excel
from app.services.store_name_utils import find_best_matching_store

router = APIRouter(prefix="/admin/store-dashboard", tags=["管理员-经营数据管理"])


# ==================== 辅助函数 ====================

async def _get_all_store_ids(db: AsyncSession, store_id: Optional[UUID] = None) -> list[UUID]:
    """管理员获取门店列表（不过滤用户绑定）"""
    if store_id:
        return [store_id]
    result = await db.execute(select(Store.id))
    return [row[0] for row in result.all()]


def _record_to_dict(record) -> dict:
    d = {}
    for col in record.__table__.columns:
        val = getattr(record, col.name)
        if hasattr(val, "isoformat"):
            val = val.isoformat()
        d[col.name] = val
    # 附加门店名称
    store = getattr(record, "_store_name", None)
    if store:
        d["store_name"] = store
    return d


async def _attach_store_names(db: AsyncSession, records: list) -> None:
    """批量附加门店名称到记录对象"""
    store_ids = list({r.store_id for r in records})
    if not store_ids:
        return
    result = await db.execute(select(Store.id, Store.name).where(Store.id.in_(store_ids)))
    name_map = {row[0]: row[1] for row in result.all()}
    for r in records:
        r._store_name = name_map.get(r.store_id, "未知门店")


# ==================== 门店列表 ====================

@router.get("/stores")
async def list_stores(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """获取所有门店（用于下拉选择）"""
    result = await db.execute(select(Store.id, Store.name).order_by(Store.name))
    items = [{"id": str(row[0]), "name": row[1]} for row in result.all()]
    return success(items)


# ==================== 营业额记录管理 ====================

@router.post("/revenue")
async def create_revenue(
    data: RevenueRecordCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """创建营业额记录"""
    record = RevenueRecord(**data.model_dump(), created_by=user.id)
    result = await svc.create_revenue_record(db, record, user)
    await _attach_store_names(db, [result])
    return success(_record_to_dict(result), "创建成功")


@router.post("/revenue/batch")
async def batch_create_revenue(
    data: RevenueBatchCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
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
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """查询营业额记录列表（分页）"""
    store_ids = await _get_all_store_ids(db, UUID(store_id) if store_id else None)
    q = select(RevenueRecord).where(RevenueRecord.store_id.in_(store_ids))
    if start_date:
        q = q.where(RevenueRecord.record_date >= date.fromisoformat(start_date))
    if end_date:
        q = q.where(RevenueRecord.record_date <= date.fromisoformat(end_date))
    q = q.order_by(RevenueRecord.record_date.desc())
    # 计数
    from sqlalchemy import func as sa_func
    count_q = select(sa_func.count()).select_from(q.subquery())
    total = (await db.execute(count_q)).scalar() or 0
    # 分页
    q = q.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(q)
    records = list(result.scalars().all())
    await _attach_store_names(db, records)
    items = [_record_to_dict(r) for r in records]
    return paginated(items, total, page, page_size)


@router.put("/revenue/{record_id}")
async def update_revenue(
    record_id: UUID,
    data: RevenueRecordUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """更新营业额记录"""
    result = await db.execute(select(RevenueRecord).where(RevenueRecord.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        return error("记录不存在")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(record, k, v)
    await db.commit()
    await db.refresh(record)
    await _attach_store_names(db, [record])
    return success(_record_to_dict(record), "更新成功")


@router.delete("/revenue/{record_id}")
async def delete_revenue(
    record_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """删除营业额记录"""
    await db.execute(sa_delete(RevenueRecord).where(RevenueRecord.id == record_id))
    await db.commit()
    return success(None, "删除成功")


# ==================== 套餐核销记录管理 ====================

@router.post("/packages")
async def create_package(
    data: PackageRecordCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """创建套餐核销记录"""
    record = PackageRecord(**data.model_dump(), created_by=user.id)
    result = await svc.create_package_record(db, record, user)
    await _attach_store_names(db, [result])
    return success(_record_to_dict(result), "创建成功")


@router.post("/packages/batch")
async def batch_create_packages(
    data: PackageBatchCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """批量创建套餐核销记录"""
    records = [PackageRecord(**r.model_dump(), created_by=user.id) for r in data.records]
    count = await svc.batch_create_package_records(db, records, user)
    return success({"count": count}, f"成功创建{count}条记录")


@router.get("/packages")
async def list_packages(
    store_id: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    product_name: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """查询套餐核销记录列表（分页）"""
    store_ids = await _get_all_store_ids(db, UUID(store_id) if store_id else None)
    q = select(PackageRecord).where(PackageRecord.store_id.in_(store_ids))
    if start_date:
        q = q.where(PackageRecord.period_start >= date.fromisoformat(start_date))
    if end_date:
        q = q.where(PackageRecord.period_end <= date.fromisoformat(end_date))
    if product_name:
        q = q.where(PackageRecord.product_name.contains(product_name))
    q = q.order_by(PackageRecord.period_start.desc(), PackageRecord.product_name)
    from sqlalchemy import func as sa_func
    count_q = select(sa_func.count()).select_from(q.subquery())
    total = (await db.execute(count_q)).scalar() or 0
    q = q.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(q)
    records = list(result.scalars().all())
    await _attach_store_names(db, records)
    items = [_record_to_dict(r) for r in records]
    return paginated(items, total, page, page_size)


@router.put("/packages/{record_id}")
async def update_package(
    record_id: UUID,
    data: PackageRecordUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """更新套餐核销记录"""
    result = await db.execute(select(PackageRecord).where(PackageRecord.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        return error("记录不存在")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(record, k, v)
    await db.commit()
    await db.refresh(record)
    await _attach_store_names(db, [record])
    return success(_record_to_dict(record), "更新成功")


@router.delete("/packages/{record_id}")
async def delete_package(
    record_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """删除套餐核销记录"""
    await db.execute(sa_delete(PackageRecord).where(PackageRecord.id == record_id))
    await db.commit()
    return success(None, "删除成功")


# ==================== 运营指标管理 ====================

@router.post("/metrics")
async def create_metric(
    data: StoreMetricCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """创建运营指标"""
    metric = StoreMetric(**data.model_dump(), created_by=user.id)
    result = await svc.create_store_metric(db, metric, user)
    await _attach_store_names(db, [result])
    return success(_record_to_dict(result), "创建成功")


@router.post("/metrics/batch")
async def batch_create_metrics(
    data: StoreMetricBatchCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """批量创建运营指标"""
    records = [StoreMetric(**r.model_dump(), created_by=user.id) for r in data.records]
    count = await svc.batch_create_store_metrics(db, records, user)
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
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """查询运营指标列表（分页）"""
    store_ids = await _get_all_store_ids(db, UUID(store_id) if store_id else None)
    q = select(StoreMetric).where(StoreMetric.store_id.in_(store_ids))
    if start_date:
        q = q.where(StoreMetric.metric_date >= date.fromisoformat(start_date))
    if end_date:
        q = q.where(StoreMetric.metric_date <= date.fromisoformat(end_date))
    if platform:
        q = q.where(StoreMetric.platform == platform)
    q = q.order_by(StoreMetric.metric_date.desc(), StoreMetric.platform)
    from sqlalchemy import func as sa_func
    count_q = select(sa_func.count()).select_from(q.subquery())
    total = (await db.execute(count_q)).scalar() or 0
    q = q.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(q)
    records = list(result.scalars().all())
    await _attach_store_names(db, records)
    items = [_record_to_dict(r) for r in records]
    return paginated(items, total, page, page_size)


@router.put("/metrics/{metric_id}")
async def update_metric(
    metric_id: UUID,
    data: StoreMetricUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """更新运营指标"""
    result = await db.execute(select(StoreMetric).where(StoreMetric.id == metric_id))
    record = result.scalar_one_or_none()
    if not record:
        return error("记录不存在")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(record, k, v)
    await db.commit()
    await db.refresh(record)
    await _attach_store_names(db, [record])
    return success(_record_to_dict(record), "更新成功")


@router.delete("/metrics/{metric_id}")
async def delete_metric(
    metric_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """删除运营指标"""
    await db.execute(sa_delete(StoreMetric).where(StoreMetric.id == metric_id))
    await db.commit()
    return success(None, "删除成功")


# ==================== 运营分析意见管理 ====================

@router.post("/analysis")
async def create_analysis(
    data: OperationAnalysisCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """创建运营分析意见"""
    record = OperationAnalysis(**data.model_dump(), created_by=user.id)
    result = await svc.create_operation_analysis(db, record, user)
    await _attach_store_names(db, [result])
    return success(_record_to_dict(result), "创建成功")


@router.get("/analysis")
async def list_analysis(
    store_id: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """查询运营分析列表（分页）"""
    store_ids = await _get_all_store_ids(db, UUID(store_id) if store_id else None)
    q = select(OperationAnalysis).where(OperationAnalysis.store_id.in_(store_ids))
    q = q.order_by(OperationAnalysis.period_start.desc())
    from sqlalchemy import func as sa_func
    count_q = select(sa_func.count()).select_from(q.subquery())
    total = (await db.execute(count_q)).scalar() or 0
    q = q.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(q)
    records = list(result.scalars().all())
    await _attach_store_names(db, records)
    items = [_record_to_dict(r) for r in records]
    return paginated(items, total, page, page_size)


@router.put("/analysis/{analysis_id}")
async def update_analysis(
    analysis_id: UUID,
    data: OperationAnalysisUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """更新运营分析意见"""
    result = await db.execute(select(OperationAnalysis).where(OperationAnalysis.id == analysis_id))
    record = result.scalar_one_or_none()
    if not record:
        return error("记录不存在")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(record, k, v)
    await db.commit()
    await db.refresh(record)
    await _attach_store_names(db, [record])
    return success(_record_to_dict(record), "更新成功")


@router.delete("/analysis/{analysis_id}")
async def delete_analysis(
    analysis_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """删除运营分析意见"""
    await db.execute(sa_delete(OperationAnalysis).where(OperationAnalysis.id == analysis_id))
    await db.commit()
    return success(None, "删除成功")


# ==================== Excel 导入 ====================

@router.post("/import-excel")
async def import_excel(
    file: UploadFile = File(...),
    store_id: Optional[str] = Query(None, description="可选：指定导入到某个门店（不传则自动匹配Excel中的门店名）"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_roles("HQ", "SUPER_ADMIN")),
):
    """
    上传周报 Excel 文件，一键导入营业额/套餐/运营指标/分析意见

    Excel 格式要求：
    - 必须包含 '营业额情况' sheet（营业额数据）
    - 必须包含 '套餐数据' sheet（套餐核销数据）
    - 门店 sheet（如 '大学城店'）为可选，包含运营指标和分析意见
    - 门店名称需与系统中的门店名匹配
    """
    if not file.filename or not file.filename.endswith(('.xlsx', '.xls')):
        return error("请上传 .xlsx 格式的 Excel 文件")

    file_bytes = await file.read()
    if len(file_bytes) < 100:
        return error("文件内容为空或太小")

    # 构建门店名 -> UUID 映射
    store_name_map: dict[str, UUID] = {}
    result = await db.execute(select(Store.id, Store.name))
    for row in result.all():
        store_name_map[row[1]] = row[0]

    if not store_name_map:
        return error("系统中没有门店数据，请先创建门店")

    # 解析 Excel
    parsed = parse_excel(file_bytes, store_name_map)

    # 批量写入数据库
    counts = {"revenue": 0, "package": 0, "metric": 0, "analysis": 0}

    # 营业额
    if parsed.revenues:
        records = [RevenueRecord(**r, created_by=user.id) for r in parsed.revenues]
        db.add_all(records)
        counts["revenue"] = len(records)

    # 套餐
    if parsed.packages:
        records = [PackageRecord(**r, created_by=user.id) for r in parsed.packages]
        db.add_all(records)
        counts["package"] = len(records)

    # 运营指标
    if parsed.metrics:
        records = [StoreMetric(**r, created_by=user.id) for r in parsed.metrics]
        db.add_all(records)
        counts["metric"] = len(records)

    # 分析意见
    if parsed.analyses:
        records = [OperationAnalysis(**r, created_by=user.id) for r in parsed.analyses]
        db.add_all(records)
        counts["analysis"] = len(records)

    await db.commit()

    total = sum(counts.values())
    return success({
        "imported": counts,
        "total": total,
        "errors": parsed.errors,
        "filename": file.filename,
    }, f"成功导入 {total} 条数据")

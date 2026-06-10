"""
经营看板服务层
处理营业额、套餐核销、运营指标、分析意见的CRUD和聚合统计
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store import Store
from app.models.store_dashboard import (
    OperationAnalysis,
    PackageRecord,
    RevenueRecord,
    StoreMetric,
)
from app.models.user import User, UserStore


# ==================== 工具函数 ====================

async def _fetch_user_store_ids(db: AsyncSession, user: User) -> list[UUID]:
    """预查询用户关联的门店ID列表（SUPER_ADMIN/HQ 可查看所有门店）"""
    from app.models.store import Store as StoreModel
    # SUPER_ADMIN 和 HQ 角色可访问所有门店
    if getattr(user, 'role', None) in ('SUPER_ADMIN', 'HQ'):
        result = await db.execute(select(StoreModel.id))
        return [row[0] for row in result.all()]
    result = await db.execute(
        select(UserStore.store_id).where(UserStore.user_id == user.id)
    )
    return [row[0] for row in result.all()]


def _calc_mom(current: float, previous: float) -> Optional[float]:
    """计算环比变化率（百分比）"""
    if previous == 0:
        return None
    return round((current - previous) / previous * 100, 1)


def _format_date_range(start: date, end: date) -> str:
    return f"{start.month}.{start.day}-{end.month}.{end.day}"


def _highlight_by_change(change: Optional[float], negative_threshold: float = -15.0) -> Optional[str]:
    """根据环比变化判断高亮类型"""
    if change is None:
        return "neutral"
    if change > 0:
        return "positive"
    if change < negative_threshold:
        return "negative"
    return "neutral"


# ==================== 营业额记录 ====================

async def create_revenue_record(
    db: AsyncSession, record: RevenueRecord, user: User
) -> RevenueRecord:
    """创建单条营业额记录"""
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


async def batch_create_revenue_records(
    db: AsyncSession, records: list[RevenueRecord], user: User
) -> int:
    """批量创建营业额记录"""
    db.add_all(records)
    await db.commit()
    return len(records)


async def get_revenue_records(
    db: AsyncSession,
    store_ids: list[UUID],
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[RevenueRecord], int]:
    """查询营业额记录（分页）"""
    query = select(RevenueRecord).where(RevenueRecord.store_id.in_(store_ids))
    if start_date:
        query = query.where(RevenueRecord.record_date >= start_date)
    if end_date:
        query = query.where(RevenueRecord.record_date <= end_date)
    query = query.order_by(RevenueRecord.record_date.desc())

    # 总数
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # 分页
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    result = await db.execute(query)
    return list(result.scalars().all()), total


async def update_revenue_record(
    db: AsyncSession, record_id: UUID, user: User, **kwargs
) -> Optional[RevenueRecord]:
    """更新营业额记录"""
    record = await db.get(RevenueRecord, record_id)
    if not record:
        return None
    for key, value in kwargs.items():
        if value is not None and hasattr(record, key):
            setattr(record, key, value)
    await db.commit()
    await db.refresh(record)
    return record


async def delete_revenue_record(
    db: AsyncSession, record_id: UUID
) -> bool:
    """删除营业额记录"""
    result = await db.execute(
        delete(RevenueRecord).where(RevenueRecord.id == record_id)
    )
    await db.commit()
    return result.rowcount > 0


async def get_revenue_summary(
    db: AsyncSession,
    store_ids: list[UUID],
    start_date: date,
    end_date: date,
    compare_start: Optional[date] = None,
    compare_end: Optional[date] = None,
) -> dict:
    """获取营业额汇总（含环比）"""
    # 当期汇总
    current = await _aggregate_revenue(db, store_ids, start_date, end_date)
    current_label = _format_date_range(start_date, end_date)

    result = {
        "total_revenue": current.get("total", 0),
        "meituan_revenue": current.get("meituan", 0),
        "douyin_revenue": current.get("douyin", 0),
        "other_revenue": current.get("other", 0),
        "visitor_count": current.get("visitors", 0),
        "table_count": current.get("tables", 0),
        "avg_people_per_table": current.get("avg_people", 0),
        "avg_per_capita": current.get("avg_capita", 0),
        "period_label": current_label,
        "mom_revenue_change": None,
        "mom_visitor_change": None,
        "mom_table_change": None,
        "compare_period_label": None,
    }

    # 环比
    if compare_start and compare_end:
        previous = await _aggregate_revenue(db, store_ids, compare_start, compare_end)
        result["compare_period_label"] = _format_date_range(compare_start, compare_end)
        result["mom_revenue_change"] = _calc_mom(current.get("total", 0), previous.get("total", 0))
        result["mom_visitor_change"] = _calc_mom(current.get("visitors", 0), previous.get("visitors", 0))
        result["mom_table_change"] = _calc_mom(current.get("tables", 0), previous.get("tables", 0))

    return result


async def get_revenue_trend(
    db: AsyncSession,
    store_ids: list[UUID],
    start_date: date,
    end_date: date,
) -> dict:
    """获取营业额趋势（日+周）"""
    query = (
        select(RevenueRecord)
        .where(
            RevenueRecord.store_id.in_(store_ids),
            RevenueRecord.record_date >= start_date,
            RevenueRecord.record_date <= end_date,
        )
        .order_by(RevenueRecord.record_date)
    )
    result = await db.execute(query)
    records = list(result.scalars().all())

    daily = []
    for r in records:
        daily.append({
            "date": f"{r.record_date.month}.{r.record_date.day}",
            "total_revenue": r.total_revenue,
            "meituan_revenue": r.meituan_revenue,
            "douyin_revenue": r.douyin_revenue,
            "other_revenue": r.other_revenue,
            "visitor_count": r.visitor_count,
            "table_count": r.table_count,
            "avg_people_per_table": r.avg_people_per_table,
            "avg_per_capita": r.avg_per_capita,
        })

    # 按周聚合
    weekly = _aggregate_weekly(records)

    return {"daily": daily, "weekly": weekly}


async def _aggregate_revenue(
    db: AsyncSession, store_ids: list[UUID], start: date, end: date
) -> dict:
    """聚合指定日期范围的营业额"""
    query = select(
        func.coalesce(func.sum(RevenueRecord.total_revenue), 0).label("total"),
        func.coalesce(func.sum(RevenueRecord.meituan_revenue), 0).label("meituan"),
        func.coalesce(func.sum(RevenueRecord.douyin_revenue), 0).label("douyin"),
        func.coalesce(func.sum(RevenueRecord.other_revenue), 0).label("other"),
        func.coalesce(func.sum(RevenueRecord.visitor_count), 0).label("visitors"),
        func.coalesce(func.sum(RevenueRecord.table_count), 0).label("tables"),
        func.coalesce(func.avg(RevenueRecord.avg_people_per_table), 0).label("avg_people"),
        func.coalesce(func.avg(RevenueRecord.avg_per_capita), 0).label("avg_capita"),
    ).where(
        RevenueRecord.store_id.in_(store_ids),
        RevenueRecord.record_date >= start,
        RevenueRecord.record_date <= end,
    )
    row = (await db.execute(query)).one()
    return {
        "total": float(row.total),
        "meituan": float(row.meituan),
        "douyin": float(row.douyin),
        "other": float(row.other),
        "visitors": int(row.visitors),
        "tables": int(row.tables),
        "avg_people": round(float(row.avg_people), 1),
        "avg_capita": round(float(row.avg_capita), 1),
    }


def _aggregate_weekly(records: list[RevenueRecord]) -> list[dict]:
    """将日记录按周聚合"""
    if not records:
        return []

    weekly_map: dict[str, dict] = {}
    for r in records:
        # ISO 周计算
        week_start = r.record_date - timedelta(days=r.record_date.weekday())
        key = week_start.isoformat()
        if key not in weekly_map:
            weekly_map[key] = {
                "week_label": f"{week_start.month}.{week_start.day}",
                "total_revenue": 0,
                "meituan_revenue": 0,
                "douyin_revenue": 0,
                "visitor_count": 0,
                "table_count": 0,
            }
        weekly_map[key]["total_revenue"] += r.total_revenue
        weekly_map[key]["meituan_revenue"] += r.meituan_revenue
        weekly_map[key]["douyin_revenue"] += r.douyin_revenue
        weekly_map[key]["visitor_count"] += r.visitor_count
        weekly_map[key]["table_count"] += r.table_count

    return sorted(weekly_map.values(), key=lambda x: x["week_label"])


# ==================== 套餐核销记录 ====================

async def create_package_record(
    db: AsyncSession, record: PackageRecord, user: User
) -> PackageRecord:
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


async def batch_create_package_records(
    db: AsyncSession, records: list[PackageRecord], user: User
) -> int:
    db.add_all(records)
    await db.commit()
    return len(records)


async def get_package_records(
    db: AsyncSession,
    store_ids: list[UUID],
    period_start: Optional[date] = None,
    period_end: Optional[date] = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[PackageRecord], int]:
    query = select(PackageRecord).where(PackageRecord.store_id.in_(store_ids))
    if period_start:
        query = query.where(PackageRecord.period_start >= period_start)
    if period_end:
        query = query.where(PackageRecord.period_end <= period_end)
    query = query.order_by(PackageRecord.period_start.desc(), PackageRecord.product_name)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    result = await db.execute(query)
    return list(result.scalars().all()), total


async def update_package_record(
    db: AsyncSession, record_id: UUID, **kwargs
) -> Optional[PackageRecord]:
    record = await db.get(PackageRecord, record_id)
    if not record:
        return None
    for key, value in kwargs.items():
        if value is not None and hasattr(record, key):
            setattr(record, key, value)
    await db.commit()
    await db.refresh(record)
    return record


async def delete_package_record(
    db: AsyncSession, record_id: UUID
) -> bool:
    result = await db.execute(
        delete(PackageRecord).where(PackageRecord.id == record_id)
    )
    await db.commit()
    return result.rowcount > 0


async def get_package_comparison(
    db: AsyncSession,
    store_ids: list[UUID],
    current_start: date,
    current_end: date,
    compare_start: Optional[date] = None,
    compare_end: Optional[date] = None,
) -> dict:
    """获取套餐双周期对比数据"""
    # 当期数据
    current_items = await _query_package_period(db, store_ids, current_start, current_end)
    current_summary = _summarize_package_items(current_items, current_start, current_end)

    result = {
        "store_name": "",  # 由API层填充
        "current_period": current_summary,
        "compare_period": None,
    }

    # 对比期
    if compare_start and compare_end:
        compare_items = await _query_package_period(db, store_ids, compare_start, compare_end)
        result["compare_period"] = _summarize_package_items(compare_items, compare_start, compare_end)

    return result


async def get_package_ranking(
    db: AsyncSession,
    store_ids: list[UUID],
    start_date: date,
    end_date: date,
) -> dict:
    """获取套餐排行（Top5 + Bottom5）"""
    items = await _query_package_period(db, store_ids, start_date, end_date)

    # 计算总核销和核销率
    ranking = []
    total_buy = 0
    total_verify = 0
    for item in items:
        tb = item.meituan_buy + item.douyin_buy
        tv = item.meituan_verify + item.douyin_verify
        total_buy += tb
        total_verify += tv
        vr = round(tv / tb * 100, 1) if tb > 0 else 0
        ranking.append({
            "product_name": item.product_name,
            "meituan_buy": item.meituan_buy,
            "meituan_verify": item.meituan_verify,
            "douyin_buy": item.douyin_buy,
            "douyin_verify": item.douyin_verify,
            "total_verify": tv,
            "verify_rate": vr,
        })

    ranking.sort(key=lambda x: x["total_verify"], reverse=True)

    return {
        "top_ranking": ranking[:5] if len(ranking) >= 5 else ranking,
        "bottom_ranking": ranking[-5:] if len(ranking) >= 5 else ranking,
        "overall_summary": {
            "total_buy": total_buy,
            "total_verify": total_verify,
            "avg_verify_rate": round(total_verify / total_buy * 100, 1) if total_buy > 0 else 0,
        },
    }


async def _query_package_period(
    db: AsyncSession, store_ids: list[UUID], start: date, end: date
) -> list[PackageRecord]:
    """查询与指定日期范围有交集的套餐记录"""
    query = (
        select(PackageRecord)
        .where(
            PackageRecord.store_id.in_(store_ids),
            PackageRecord.period_end >= start,
            PackageRecord.period_start <= end,
        )
        .order_by(PackageRecord.product_name)
    )
    result = await db.execute(query)
    return list(result.scalars().all())


def _summarize_package_items(
    items: list[PackageRecord], start: date, end: date
) -> dict:
    """汇总套餐数据"""
    summarized = []
    total_mt_buy = 0
    total_mt_verify = 0
    total_dy_buy = 0
    total_dy_verify = 0
    for item in items:
        summarized.append({
            "product_name": item.product_name,
            "meituan_buy": item.meituan_buy,
            "meituan_verify": item.meituan_verify,
            "douyin_buy": item.douyin_buy,
            "douyin_verify": item.douyin_verify,
        })
        total_mt_buy += item.meituan_buy
        total_mt_verify += item.meituan_verify
        total_dy_buy += item.douyin_buy
        total_dy_verify += item.douyin_verify

    return {
        "period_start": start.isoformat(),
        "period_end": end.isoformat(),
        "period_label": _format_date_range(start, end),
        "items": summarized,
        "total_meituan_buy": total_mt_buy,
        "total_meituan_verify": total_mt_verify,
        "total_douyin_buy": total_dy_buy,
        "total_douyin_verify": total_dy_verify,
    }


# ==================== 门店运营指标 ====================

async def create_store_metric(
    db: AsyncSession, metric: StoreMetric, user: User
) -> StoreMetric:
    db.add(metric)
    await db.commit()
    await db.refresh(metric)
    return metric


async def batch_create_store_metrics(
    db: AsyncSession, metrics: list[StoreMetric], user: User
) -> int:
    db.add_all(metrics)
    await db.commit()
    return len(metrics)


async def get_store_metrics(
    db: AsyncSession,
    store_ids: list[UUID],
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    platform: Optional[str] = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[StoreMetric], int]:
    query = select(StoreMetric).where(StoreMetric.store_id.in_(store_ids))
    if start_date:
        query = query.where(StoreMetric.metric_date >= start_date)
    if end_date:
        query = query.where(StoreMetric.metric_date <= end_date)
    if platform:
        query = query.where(StoreMetric.platform == platform)
    query = query.order_by(StoreMetric.metric_date.desc(), StoreMetric.platform)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    result = await db.execute(query)
    return list(result.scalars().all()), total


async def update_store_metric(
    db: AsyncSession, metric_id: UUID, **kwargs
) -> Optional[StoreMetric]:
    metric = await db.get(StoreMetric, metric_id)
    if not metric:
        return None
    for key, value in kwargs.items():
        if value is not None and hasattr(metric, key):
            setattr(metric, key, value)
    await db.commit()
    await db.refresh(metric)
    return metric


async def delete_store_metric(
    db: AsyncSession, metric_id: UUID
) -> bool:
    result = await db.execute(
        delete(StoreMetric).where(StoreMetric.id == metric_id)
    )
    await db.commit()
    return result.rowcount > 0


async def get_store_health(
    db: AsyncSession,
    store_ids: list[UUID],
    start_date: date,
    end_date: date,
    compare_start: Optional[date] = None,
    compare_end: Optional[date] = None,
) -> dict:
    """获取门店运营健康度数据（漏斗、榜单、评价）"""
    # 当期指标
    current_metrics = await _query_metrics_period(db, store_ids, start_date, end_date)
    compare_metrics = []
    if compare_start and compare_end:
        compare_metrics = await _query_metrics_period(db, store_ids, compare_start, compare_end)

    # 按平台聚合
    funnels = []
    rankings = []
    reviews_summary = []
    platform_metric_map: dict[str, list] = {}
    platform_compare_map: dict[str, list] = {}

    for m in current_metrics:
        platform_metric_map.setdefault(m.platform, []).append(m)
    for m in compare_metrics:
        platform_compare_map.setdefault(m.platform, []).append(m)

    for platform in ["meituan", "dianping", "douyin"]:
        cur = platform_metric_map.get(platform, [])
        prev = platform_compare_map.get(platform, [])

        # 漏斗聚合
        imp = sum(m.impressions or 0 for m in cur)
        vis = sum(m.visits or 0 for m in cur)
        pur = sum(m.purchases or 0 for m in cur)
        ver = sum(m.verifications or 0 for m in cur)
        funnels.append({
            "platform": platform,
            "impressions": imp,
            "visits": vis,
            "purchases": pur,
            "verifications": ver,
            "impression_to_visit": round(vis / imp * 100, 1) if imp > 0 else 0,
            "visit_to_purchase": round(pur / vis * 100, 1) if vis > 0 else 0,
        })

        # 榜单
        for m in cur:
            if m.ranking_name:
                rankings.append({
                    "platform": platform,
                    "ranking_name": m.ranking_name,
                    "current_rank": m.ranking_position or "-",
                    "prev_rank": m.prev_ranking_position or "-",
                    "rank_change": "持平",
                })

        # 评价
        new_reviews = sum(m.new_reviews or 0 for m in cur)
        bad_reviews = sum(m.new_bad_reviews or 0 for m in cur)
        star = None
        prev_star = None
        for m in cur:
            if m.star_rating is not None:
                star = m.star_rating
        for m in prev:
            if m.prev_star_rating is not None:
                prev_star = m.prev_star_rating
        keywords = []
        for m in cur:
            if m.bad_keywords:
                keywords.extend(m.bad_keywords)
        reviews_summary.append({
            "platform": platform,
            "star_rating": star or 0,
            "prev_star_rating": prev_star or 0,
            "new_reviews": new_reviews,
            "bad_reviews": bad_reviews,
            "bad_keywords": list(set(keywords)),
        })

    # 指标对比
    all_platforms_metrics = _build_platform_metrics(current_metrics, compare_metrics)

    return {
        "funnels": funnels,
        "rankings": rankings,
        "reviews_summary": reviews_summary,
        "daily_metrics": _build_daily_metrics(current_metrics),
        "platform_metrics": all_platforms_metrics,
    }


def _build_platform_metrics(
    current: list[StoreMetric], compare: list[StoreMetric]
) -> dict:
    """构建平台指标对比数据"""
    metric_defs = [
        ("美团人气榜榜单", "ranking_position", lambda m: m.ranking_position),
        ("美团星级", "star_rating", lambda m: str(m.star_rating) if m.star_rating else "-"),
        ("曝光次数", "impressions", lambda m: str(m.impressions or 0)),
        ("访问次数", "visits", lambda m: str(m.visits or 0)),
        ("曝光-访问转化率", "imp_to_vis", None),
        ("购买人数", "purchases", lambda m: str(m.purchases or 0)),
        ("访问-购买转化率", "vis_to_pur", None),
        ("新增收藏人数", "new_favorites", lambda m: str(m.new_favorites or 0)),
        ("打卡人数", "checkins", lambda m: str(m.checkins or 0)),
        ("扫码人数", "scan_count", lambda m: str(m.scan_count or 0)),
        ("商品曝光人数", "product_impressions", lambda m: str(m.product_impressions or 0)),
        ("商品访问人数", "product_visits", lambda m: str(m.product_visits or 0)),
        ("商品曝光-访问转化率", "prod_imp_to_vis", None),
        ("商品购买人数", "product_purchases", lambda m: str(m.product_purchases or 0)),
        ("商品访问-购买转化率", "prod_vis_to_pur", None),
        ("新评价数", "new_reviews", lambda m: str(m.new_reviews or 0)),
        ("新中差评数", "new_bad_reviews", lambda m: str(m.new_bad_reviews or 0)),
    ]

    result = {}
    for m in current:
        if m.platform not in result:
            result[m.platform] = {
                "metrics": [],
            }

    return result


def _build_daily_metrics(records: list[StoreMetric]) -> list[dict]:
    """构建日指标数据"""
    return [
        {
            "date": f"{m.metric_date.month}.{m.metric_date.day}",
            "platform": m.platform,
            "impressions": m.impressions or 0,
            "visits": m.visits or 0,
            "purchases": m.purchases or 0,
            "verifications": m.verifications or 0,
            "star_rating": m.star_rating or 0,
            "new_reviews": m.new_reviews or 0,
        }
        for m in records
    ]


async def _query_metrics_period(
    db: AsyncSession, store_ids: list[UUID], start: date, end: date
) -> list[StoreMetric]:
    query = (
        select(StoreMetric)
        .where(
            StoreMetric.store_id.in_(store_ids),
            StoreMetric.metric_date >= start,
            StoreMetric.metric_date <= end,
        )
        .order_by(StoreMetric.metric_date)
    )
    result = await db.execute(query)
    return list(result.scalars().all())


# ==================== 运营分析意见 ====================

async def create_operation_analysis(
    db: AsyncSession, analysis: OperationAnalysis, user: User
) -> OperationAnalysis:
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)
    return analysis


async def get_operation_analyses(
    db: AsyncSession,
    store_ids: list[UUID],
    period_start: Optional[date] = None,
    period_end: Optional[date] = None,
) -> list[OperationAnalysis]:
    """查询与指定日期范围有交集的运营分析记录"""
    query = select(OperationAnalysis).where(
        OperationAnalysis.store_id.in_(store_ids)
    )
    if period_start:
        query = query.where(OperationAnalysis.period_end >= period_start)
    if period_end:
        query = query.where(OperationAnalysis.period_start <= period_end)
    query = query.order_by(OperationAnalysis.period_start.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def update_operation_analysis(
    db: AsyncSession, analysis_id: UUID, **kwargs
) -> Optional[OperationAnalysis]:
    analysis = await db.get(OperationAnalysis, analysis_id)
    if not analysis:
        return None
    for key, value in kwargs.items():
        if value is not None and hasattr(analysis, key):
            setattr(analysis, key, value)
    await db.commit()
    await db.refresh(analysis)
    return analysis


async def delete_operation_analysis(
    db: AsyncSession, analysis_id: UUID
) -> bool:
    result = await db.execute(
        delete(OperationAnalysis).where(OperationAnalysis.id == analysis_id)
    )
    await db.commit()
    return result.rowcount > 0


# ==================== 看板聚合 ====================

async def get_dashboard_overview(
    db: AsyncSession,
    user: User,
    store_ids: list[UUID],
    start_date: date,
    end_date: date,
    compare_start: Optional[date] = None,
    compare_end: Optional[date] = None,
) -> dict:
    """获取看板完整概览（顺序查询各模块，避免共享session并发死锁）"""
    revenue_summary = await get_revenue_summary(db, store_ids, start_date, end_date, compare_start, compare_end)
    health = await get_store_health(db, store_ids, start_date, end_date, compare_start, compare_end)
    package_comparison = await get_package_comparison(db, store_ids, start_date, end_date, compare_start, compare_end)
    analyses = await get_operation_analyses(db, store_ids, start_date, end_date)

    # 门店名称
    store_name = ""
    if store_ids:
        store_result = await db.execute(
            select(Store.name).where(Store.id == store_ids[0])
        )
        store_name = store_result.scalar() or ""

    return {
        "revenue": revenue_summary,
        "business_metrics": {
            "visitor_count": revenue_summary["visitor_count"],
            "table_count": revenue_summary["table_count"],
            "avg_people_per_table": revenue_summary["avg_people_per_table"],
            "avg_per_capita": revenue_summary["avg_per_capita"],
            "mom_visitor_change": revenue_summary.get("mom_visitor_change"),
            "mom_table_change": revenue_summary.get("mom_table_change"),
        },
        "package_comparison": {**package_comparison, "store_name": store_name} if package_comparison else None,
        "operation_analysis": analyses[0] if analyses else None,
        "operation_metrics": health.get("platform_metrics"),
    }

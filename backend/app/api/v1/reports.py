"""
报告路由模块
处理年度报告、周报等接口
"""

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_valid_subscription, get_db
from app.core.response import success
from app.models.user import User
from app.schemas.report import (
    AllYearsDataResponse,
    AnnualReportResponse,
    GenerateReportRequest,
    WeeklyBriefResponse,
    YearlyDataResponse,
    ReportInsightsResponse,
)
from app.services import report_service

router = APIRouter(prefix="/reports", tags=["报告管理"])


@router.get("/annual", summary="获取年度报告")
async def get_annual_report(
    store_id: UUID = Query(..., description="门店ID"),
    year: int = Query(..., description="年份", ge=2000, le=2100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取指定门店的年度报告
    - 包含年度数据统计、洞察分析等
    """
    report = await report_service.get_annual_report(db, store_id, year)

    # 查询上一年报告用于同比计算
    prev_report = None
    try:
        prev_report = await report_service.get_annual_report(db, store_id, year - 1)
    except Exception:
        pass

    # 查询所有年份数据用于 historical_trends
    all_years_data = await report_service.get_all_years_data(db, store_id)

    # 计算 year_over_year（基于实际报告数据，不依赖AI）
    yoy = report.insights.get("year_over_year", {}) if report.insights else {}
    if prev_report:
        prev_total = prev_report.total_reviews
        curr_total = report.total_reviews
        if prev_total > 0:
            yoy["review_growth"] = round((curr_total - prev_total) / prev_total * 100, 1)

        prev_rating = prev_report.average_rating or 0
        curr_rating = report.average_rating or 0
        yoy["rating_change"] = round(curr_rating - prev_rating, 1)

        prev_reply_rate = (prev_report.reply_stats or {}).get("reply_rate", 0)
        curr_reply_rate = (report.reply_stats or {}).get("reply_rate", 0)
        yoy["reply_rate_change"] = round(curr_reply_rate - prev_reply_rate, 1)
    else:
        # 无上一年报告，若AI未给出有效值则补零
        yoy.setdefault("review_growth", 0)
        yoy.setdefault("rating_change", 0)
        yoy.setdefault("reply_rate_change", 0)

    # 计算 historical_trends
    total_3y = sum(d.get("total_reviews", 0) for d in all_years_data)
    avg_rating_3y = 0.0
    if all_years_data:
        avg_rating_3y = round(
            sum(d.get("average_rating", 0) for d in all_years_data) / len(all_years_data), 1
        )
    best_year = year
    worst_year = year
    if all_years_data:
        best_year = max(all_years_data, key=lambda x: x.get("average_rating", 0))["year"]
        worst_year = min(all_years_data, key=lambda x: x.get("average_rating", 0))["year"]

    historical_trends = {
        "best_year": best_year,
        "worst_year": worst_year,
        "average_rating_3_years": avg_rating_3y,
        "total_reviews_3_years": total_3y,
    }

    # 构建响应数据
    data = YearlyDataResponse(
        year=report.year,
        total_reviews=report.total_reviews,
        average_rating=report.average_rating or 0.0,
        sentiment_distribution=report.sentiment_distribution or {},
        reply_stats=report.reply_stats or {},
        monthly_data=report.monthly_data or [],
        top_keywords=report.top_keywords or [],
        category_scores=report.category_scores or {},
        rating_distribution=report.rating_distribution or {},
        platform_distribution=report.platform_distribution or {},
        reply_sentiment=report.reply_sentiment or {},
        peak_month=report.peak_month or {},
        active_days=report.active_days or 0,
        monthly_sentiment=report.monthly_sentiment or [],
    )

    insights = ReportInsightsResponse(
        year_over_year=yoy,
        highlights=report.insights.get("highlights", []) if report.insights else [],
        improvements=report.insights.get("improvements", []) if report.insights else [],
        ai_summary=report.insights.get("ai_summary", "") if report.insights else "",
        personality_type=report.insights.get("personality_type") if report.insights else None,
        recommendations=report.insights.get("recommendations", []) if report.insights else [],
    )

    response = AnnualReportResponse(
        id=report.id,
        store_id=report.store_id,
        year=report.year,
        data=data,
        insights=insights,
        generated_at=report.generated_at,
    )

    return success(data={
        **response.model_dump(mode="json"),
        "historical_trends": historical_trends,
    })


@router.get("/annual/all-years", summary="获取所有年份数据")
async def get_all_years_data(
    store_id: UUID = Query(..., description="门店ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取门店所有有数据的年份列表及简要数据
    """
    years_data = await report_service.get_all_years_data(db, store_id)

    years = [d["year"] for d in years_data]

    response = AllYearsDataResponse(
        years=years,
        data=years_data,
    )

    return success(data=response.model_dump(mode="json"))


@router.post("/annual/generate", summary="生成年度报告")
async def generate_annual_report(
    request: GenerateReportRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    生成指定门店的年度报告
    - 基于该年份的评论数据自动生成
    - 如果报告已存在则更新
    """
    report = await report_service.generate_annual_report(
        db, request.store_id, request.year
    )

    # 查询上一年报告用于同比计算
    prev_report = None
    try:
        prev_report = await report_service.get_annual_report(db, request.store_id, request.year - 1)
    except Exception:
        pass

    # 查询所有年份数据用于 historical_trends
    all_years_data = await report_service.get_all_years_data(db, request.store_id)

    # 计算 year_over_year（基于实际报告数据，不依赖AI）
    yoy = report.insights.get("year_over_year", {}) if report.insights else {}
    if prev_report:
        prev_total = prev_report.total_reviews
        curr_total = report.total_reviews
        if prev_total > 0:
            yoy["review_growth"] = round((curr_total - prev_total) / prev_total * 100, 1)

        prev_rating = prev_report.average_rating or 0
        curr_rating = report.average_rating or 0
        yoy["rating_change"] = round(curr_rating - prev_rating, 1)

        prev_reply_rate = (prev_report.reply_stats or {}).get("reply_rate", 0)
        curr_reply_rate = (report.reply_stats or {}).get("reply_rate", 0)
        yoy["reply_rate_change"] = round(curr_reply_rate - prev_reply_rate, 1)
    else:
        # 无上一年报告，若AI未给出有效值则补零
        yoy.setdefault("review_growth", 0)
        yoy.setdefault("rating_change", 0)
        yoy.setdefault("reply_rate_change", 0)

    # 计算 historical_trends
    total_3y = sum(d.get("total_reviews", 0) for d in all_years_data)
    avg_rating_3y = 0.0
    if all_years_data:
        avg_rating_3y = round(
            sum(d.get("average_rating", 0) for d in all_years_data) / len(all_years_data), 1
        )
    best_year = request.year
    worst_year = request.year
    if all_years_data:
        best_year = max(all_years_data, key=lambda x: x.get("average_rating", 0))["year"]
        worst_year = min(all_years_data, key=lambda x: x.get("average_rating", 0))["year"]

    historical_trends = {
        "best_year": best_year,
        "worst_year": worst_year,
        "average_rating_3_years": avg_rating_3y,
        "total_reviews_3_years": total_3y,
    }

    # 构建响应数据
    data = YearlyDataResponse(
        year=report.year,
        total_reviews=report.total_reviews,
        average_rating=report.average_rating or 0.0,
        sentiment_distribution=report.sentiment_distribution or {},
        reply_stats=report.reply_stats or {},
        monthly_data=report.monthly_data or [],
        top_keywords=report.top_keywords or [],
        category_scores=report.category_scores or {},
        rating_distribution=report.rating_distribution or {},
        platform_distribution=report.platform_distribution or {},
        reply_sentiment=report.reply_sentiment or {},
        peak_month=report.peak_month or {},
        active_days=report.active_days or 0,
        monthly_sentiment=report.monthly_sentiment or [],
    )

    insights = ReportInsightsResponse(
        year_over_year=yoy,
        highlights=report.insights.get("highlights", []) if report.insights else [],
        improvements=report.insights.get("improvements", []) if report.insights else [],
        ai_summary=report.insights.get("ai_summary", "") if report.insights else "",
        personality_type=report.insights.get("personality_type") if report.insights else None,
        recommendations=report.insights.get("recommendations", []) if report.insights else [],
    )

    response = AnnualReportResponse(
        id=report.id,
        store_id=report.store_id,
        year=report.year,
        data=data,
        insights=insights,
        generated_at=report.generated_at,
    )

    return success(
        data={
            **response.model_dump(mode="json"),
            "historical_trends": historical_trends,
        },
        message=f"{request.year}年度报告生成成功",
    )


@router.get("/weekly", summary="获取周报")
async def get_weekly_brief(
    store_id: UUID = Query(..., description="门店ID"),
    week_start: str | None = Query(None, description="周开始日期(YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取指定门店的周报
    - 如未指定周开始日期，则返回当前周的周报
    """
    week_start_dt = None
    if week_start:
        try:
            week_start_dt = datetime.strptime(week_start, "%Y-%m-%d")
        except ValueError:
            from app.core.exceptions import BusinessException
            raise BusinessException("日期格式错误，请使用YYYY-MM-DD格式")

    brief = await report_service.get_weekly_brief(db, store_id, week_start_dt)

    response = WeeklyBriefResponse(
        id=brief.id,
        store_id=brief.store_id,
        week_start=brief.week_start,
        week_end=brief.week_end,
        total_reviews=brief.total_reviews,
        positive_count=brief.positive_count,
        negative_count=brief.negative_count,
        neutral_count=brief.neutral_count,
        avg_rating=brief.avg_rating,
        top_issues=brief.top_issues or [],
        top_praises=brief.top_praises or [],
        dish_analysis=brief.dish_analysis or {},
        ai_summary=brief.ai_summary,
        generated_at=brief.generated_at,
    )

    return success(data=response.model_dump(mode="json"))


@router.post("/weekly/generate", summary="生成周报")
async def generate_weekly_brief(
    store_id: UUID = Query(..., description="门店ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    生成指定门店的周报
    - 基于本周的评论数据自动生成
    - 如果周报已存在则更新
    """
    brief = await report_service.generate_weekly_brief(db, store_id)

    response = WeeklyBriefResponse(
        id=brief.id,
        store_id=brief.store_id,
        week_start=brief.week_start,
        week_end=brief.week_end,
        total_reviews=brief.total_reviews,
        positive_count=brief.positive_count,
        negative_count=brief.negative_count,
        neutral_count=brief.neutral_count,
        avg_rating=brief.avg_rating,
        top_issues=brief.top_issues or [],
        top_praises=brief.top_praises or [],
        dish_analysis=brief.dish_analysis or {},
        ai_summary=brief.ai_summary,
        generated_at=brief.generated_at,
    )

    return success(
        data=response.model_dump(mode="json"),
        message="周报生成成功",
    )

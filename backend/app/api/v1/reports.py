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
    )

    insights = ReportInsightsResponse(
        year_over_year=report.insights.get("year_over_year", {}) if report.insights else {},
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

    return success(data=response.model_dump(mode="json"))


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
    )

    insights = ReportInsightsResponse(
        year_over_year=report.insights.get("year_over_year", {}) if report.insights else {},
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
        data=response.model_dump(mode="json"),
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

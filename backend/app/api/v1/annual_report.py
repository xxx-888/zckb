"""
年度报告 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from app.core.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.services.annual_report_service import (
    get_annual_report_data,
    get_all_yearly_data,
    get_report_insights,
    get_historical_trends,
)

router = APIRouter(prefix="/api/v1/annual-report", tags=["年度报告"])

@router.get("/{year}")
async def get_annual_report(
    year: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取指定年份的年度报告数据"""
    if year < 2020 or year > 2026:
        raise HTTPException(status_code=400, detail="年份无效")
    
    data = await get_annual_report_data(db, current_user, year)
    return {"code": 200, "message": "success", "data": data}


@router.get("/all")
async def get_all_yearly_data(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取所有年份数据"""
    data = await get_all_yearly_data(db, current_user)
    return {"code": 200, "message": "success", "data": data}


@router.get("/insights/{year}")
async def get_insights(
    year: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取年度报告洞察"""
    data = await get_report_insights(db, current_user, year)
    return {"code": 200, "message": "success", "data": data}


@router.get("/historical-trends")
async def get_historical_trends(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取历史趋势"""
    data = await get_historical_trends(db, current_user)
    return {"code": 200, "message": "success", "data": data}

"""
经营洞察路由模块
处理经营分析和洞察相关接口
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_valid_subscription, get_db
from app.core.response import success
from app.models.user import User
from app.schemas.insights import (
    CompetitorOpportunityResponse,
    DishEliminationResponse,
    DishResponse,
    ServiceCaseResponse,
    ThreeGoodThreeBadResponse,
)
from app.services import insights_service

router = APIRouter(prefix="/insights", tags=["经营洞察"])


@router.get("/top-dishes", summary="菜品口碑排行")
async def get_top_dishes(
    period: str = Query("30d", description="时间周期"),
    store_id: str | None = Query(None, description="门店ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取菜品口碑排行
    - 各菜品好评/差评统计
    - 推荐改进和淘汰建议
    """
    dishes = await insights_service.get_top_dishes(db, current_user, period, store_id)
    return success(
        data=[DishResponse(**dish).model_dump(mode="json") for dish in dishes]
    )


@router.get("/three-good-three-bad", summary="三好三差报告")
async def get_three_good_three_bad(
    period: str = Query("30d", description="时间周期"),
    store_id: str | None = Query(None, description="门店ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取三好三差报告
    - 三项最值得保持的优点
    - 三项最需要改进的不足
    """
    report = await insights_service.get_three_good_three_bad(db, current_user, period, store_id)
    return success(data=ThreeGoodThreeBadResponse(**report).model_dump(mode="json"))


@router.get("/dish-elimination", summary="末位淘汰建议")
async def get_dish_elimination(
    store_id: str | None = Query(None, description="门店ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取末位淘汰建议
    - 低评分菜品分析
    - 淘汰原因和改进建议
    """
    suggestions = await insights_service.get_dish_elimination(db, current_user, store_id)
    return success(
        data=[DishEliminationResponse(**item).model_dump(mode="json") for item in suggestions]
    )


@router.get("/service-cases", summary="服务案例库")
async def get_service_cases(
    case_type: str | None = Query(None, description="案例类型: complaint/praise/suggestion"),
    store_id: str | None = Query(None, description="门店ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取服务案例库
    - 投诉处理案例
    - 服务表扬案例
    - 改进建议案例
    """
    cases = await insights_service.get_service_cases(db, current_user, case_type, store_id)
    return success(
        data=[ServiceCaseResponse(**case).model_dump(mode="json") for case in cases]
    )


@router.get("/competitor-opportunities", summary="同行机会洞察")
async def get_competitor_opportunities(
    store_id: str | None = Query(None, description="门店ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取同行机会洞察
    - 市场空白分析
    - 竞争机会点
    - 行动建议
    """
    opportunities = await insights_service.get_competitor_opportunities(db, current_user, store_id)
    return success(
        data=[CompetitorOpportunityResponse(**item).model_dump(mode="json") for item in opportunities]
    )

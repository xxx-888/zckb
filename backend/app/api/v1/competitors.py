"""
竞对分析路由模块
处理竞品管理、分析任务、分析报告等接口
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_valid_subscription, get_db
from app.core.response import success, paginated
from app.models.user import User
from app.schemas.competitor import (
    CompetitorCreateRequest,
    CompetitorResponse,
    CompetitorPlanResponse,
    CompetitorTaskCreateRequest,
    CompetitorTaskResponse,
    CompetitorAnalysisResultResponse,
    GenerateReportRequest,
)
from app.services import competitor_service
from app.services.collection_pack_service import deduct_credits, get_user_balance

router = APIRouter(prefix="/competitors", tags=["竞对分析"])


# ==================== 竞品管理 ====================

@router.get("", summary="获取竞品列表")
async def get_competitors(
    store_id: UUID = Query(..., description="门店ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取指定门店的竞品列表
    """
    competitors = await competitor_service.get_competitors(db, store_id)

    items = []
    for competitor in competitors:
        items.append(CompetitorResponse.model_validate(competitor).model_dump(mode="json"))

    return success(data={"items": items, "total": len(items)})


@router.post("", summary="添加竞品")
async def create_competitor(
    request: CompetitorCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    添加新的竞品
    - 会自动尝试获取竞品的基础数据
    """
    competitor = await competitor_service.create_competitor(
        db, request.model_dump()
    )

    return success(
        data=CompetitorResponse.model_validate(competitor).model_dump(mode="json"),
        message="竞品添加成功",
    )


# ==================== 套餐 & 任务（必须在 /{competitor_id} 之前） ====================

@router.get("/plans", summary="获取套餐列表")
async def get_competitor_plans(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取竞对分析的套餐列表
    - 包含基础版、标准版、高级版
    """
    plans = await competitor_service.get_competitor_plans(db)

    items = []
    for plan in plans:
        items.append(CompetitorPlanResponse(**plan).model_dump(mode="json"))

    return success(data={"items": items, "total": len(items)})


@router.get("/tasks", summary="获取任务列表")
async def get_analysis_tasks(
    store_id: UUID | None = Query(None, description="门店ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取竞对分析任务列表
    - 可按门店筛选
    """
    tasks = await competitor_service.get_analysis_tasks(db, store_id)

    # 补充竞品名称
    items = []
    for task in tasks:
        from sqlalchemy import select as sa_select
        competitor_result = await db.execute(
            sa_select(competitor_service.Competitor).where(
                competitor_service.Competitor.id == task.competitor_id
            )
        )
        competitor = competitor_result.scalar_one_or_none()

        items.append({
            "id": str(task.id),
            "competitor_name": competitor.name if competitor else "",
            "platform": competitor.platform if competitor else "",
            "status": task.status,
            "payment_status": task.payment_status,
            "price": task.price,
            "result_data": task.result_data,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None,
        })

    return success(data={"items": items, "total": len(items)})


@router.post("/tasks", summary="创建分析任务（消耗采集积分）")
async def create_analysis_task(
    request: CompetitorTaskCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    创建竞对分析任务
    - 需要指定竞品ID和套餐ID
    - 从用户采集积分中扣除对应数量（套餐 price = 消耗积分）
    - 积分不足返回 402
    """
    from app.core.exceptions import CreditInsufficientException, NotFoundException

    # 查询套餐，确定消耗积分数量
    plan = await competitor_service.get_plan_by_id(db, request.plan_id)
    if not plan:
        raise NotFoundException("套餐不存在")
    credit_cost = int(plan.get("price", 0))

    # 检查并扣除积分
    balance = await get_user_balance(db, str(current_user.id))
    if balance.balance < credit_cost:
        raise CreditInsufficientException(
            message=f"采集积分不足，需要 {credit_cost} 积分，当前余额 {balance.balance}",
            code=402,
        )
    await deduct_credits(db, str(current_user.id), credit_cost)

    # 创建任务
    task = await competitor_service.create_analysis_task(
        db, request.model_dump()
    )

    # 获取竞品信息用于响应
    from sqlalchemy import select as sa_select
    competitor_result = await db.execute(
        sa_select(competitor_service.Competitor).where(
            competitor_service.Competitor.id == task.competitor_id
        )
    )
    competitor = competitor_result.scalar_one_or_none()

    response_data = {
        "id": str(task.id),
        "competitor_name": competitor.name if competitor else "",
        "platform": competitor.platform if competitor else "",
        "status": task.status,
        "payment_status": "paid",
        "price": credit_cost,
        "result_data": task.result_data,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "updated_at": task.updated_at.isoformat() if task.updated_at else None,
    }

    return success(
        data=response_data,
        message=f"分析任务创建成功，消耗 {credit_cost} 积分",
    )


@router.post("/tasks/{task_id}/pay", summary="支付分析任务（兼容旧接口）")
async def pay_analysis_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    支付竞对分析任务（兼容旧接口，新版本使用积分扣除）
    """
    from sqlalchemy import select as sa_select
    from app.core.exceptions import NotFoundException

    stmt = sa_select(competitor_service.CompetitorAnalysisTask).where(
        competitor_service.CompetitorAnalysisTask.id == task_id
    )
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()

    if not task:
        raise NotFoundException("任务不存在")

    task.payment_status = "paid"
    await db.flush()

    return success(message="支付成功")


@router.post("/tasks/{task_id}/generate", summary="生成任务报告")
async def generate_task_report(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    为已支付的任务生成分析报告
    """
    result = await competitor_service.generate_analysis_report(db, task_id)

    response = CompetitorAnalysisResultResponse(
        overview=result["overview"],
        rating_comparison=result["rating_comparison"],
        sentiment_comparison=result["sentiment_comparison"],
        keyword_analysis=result["keyword_analysis"],
        strength_weakness=result["strength_weakness"],
        recommendations=result["recommendations"],
    )

    return success(
        data=response.model_dump(mode="json"),
        message="分析报告生成成功",
    )


# ==================== 报告生成 ====================

@router.post("/generate-report", summary="生成分析报告")
async def generate_analysis_report(
    request: GenerateReportRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    生成竞对分析报告
    - 需要指定竞品ID
    - 需要先完成分析任务的支付
    """
    # 获取竞品信息
    detail = await competitor_service.get_competitor_detail(db, request.competitor_id)

    # 获取门店自身数据
    self_data = await competitor_service._get_self_store_data(db, detail["store_id"])

    # 构建竞品数据
    competitor_data = {
        "name": detail["name"],
        "platform": detail["platform"],
        "rating": detail["rating"],
        "positive_rate": detail["positive_rate"],
        "review_count": detail["review_count"],
        "trends_data": detail["trends_data"],
    }

    # 生成对比分析
    result = competitor_service._compare_with_self(self_data, competitor_data)

    response = CompetitorAnalysisResultResponse(
        overview=result["overview"],
        rating_comparison=result["rating_comparison"],
        sentiment_comparison=result["sentiment_comparison"],
        keyword_analysis=result["keyword_analysis"],
        strength_weakness=result["strength_weakness"],
        recommendations=result["recommendations"],
    )

    return success(
        data=response.model_dump(mode="json"),
        message="分析报告生成成功",
    )


# ==================== 竞品详情 & 操作（带路径参数的路由放最后） ====================

@router.delete("/{competitor_id}", summary="删除竞品")
async def delete_competitor(
    competitor_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    删除指定的竞品
    """
    await competitor_service.delete_competitor(db, competitor_id)

    return success(message="竞品已删除")


@router.get("/{competitor_id}", summary="获取竞品详情")
async def get_competitor_detail(
    competitor_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取竞品的详细信息
    - 包含基础数据、最近评论、分析历史等
    """
    detail = await competitor_service.get_competitor_detail(db, competitor_id)

    return success(data=detail)


@router.post("/{competitor_id}/sync", summary="同步竞品数据")
async def sync_competitor_data(
    competitor_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    同步竞品的最新数据
    - 从平台获取最新的评分、评论数等数据
    """
    competitor = await competitor_service.sync_competitor_data(db, competitor_id)

    return success(
        data=CompetitorResponse.model_validate(competitor).model_dump(mode="json"),
        message="数据同步成功",
    )

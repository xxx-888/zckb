"""
爬虫路由模块
处理爬虫平台管理、同步日志、任务管理等接口
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_valid_subscription, get_db
from app.core.response import paginated, success
from app.models.user import User
from app.schemas.spider import (
    SpiderPlatformCreateRequest,
    SpiderPlatformListResponse,
    SpiderPlatformResponse,
    SpiderPlatformUpdateRequest,
    SpiderSyncLogListResponse,
    SpiderSyncLogResponse,
    SpiderTaskCreateRequest,
    SpiderTaskListResponse,
    SpiderTaskResponse,
    SpiderTestConnectionResponse,
)
from app.services import spider_service

router = APIRouter(prefix="/spider", tags=["爬虫管理"])


@router.get("/platforms", summary="平台列表")
async def get_platforms(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取所有爬虫平台列表
    """
    platforms = await spider_service.get_platforms(db)
    return success(
        data=[
            SpiderPlatformResponse.model_validate(p).model_dump(mode="json")
            for p in platforms
        ]
    )


@router.post("/platforms", summary="新增平台")
async def create_platform(
    request: SpiderPlatformCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    创建新的爬虫平台
    """
    platform = await spider_service.create_platform(db, request)
    return success(
        data=SpiderPlatformResponse.model_validate(platform).model_dump(mode="json"),
        message="平台创建成功",
    )


@router.put("/platforms/{platform_id}", summary="更新平台")
async def update_platform(
    platform_id: UUID,
    request: SpiderPlatformUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    更新爬虫平台信息
    """
    platform = await spider_service.update_platform(db, platform_id, request)
    return success(
        data=SpiderPlatformResponse.model_validate(platform).model_dump(mode="json"),
        message="平台更新成功",
    )


@router.delete("/platforms/{platform_id}", summary="删除平台")
async def delete_platform(
    platform_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    删除爬虫平台
    """
    await spider_service.delete_platform(db, platform_id)
    return success(message="平台删除成功")


@router.post("/platforms/{platform_id}/sync", summary="同步单个平台")
async def sync_platform(
    platform_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    手动触发单个平台的数据同步
    """
    sync_log = await spider_service.sync_platform(db, platform_id)
    return success(
        data=SpiderSyncLogResponse.model_validate(sync_log).model_dump(mode="json"),
        message="同步任务已启动",
    )


@router.post("/sync-all", summary="同步所有平台")
async def sync_all_platforms(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    手动触发所有活跃平台的数据同步
    """
    sync_logs = await spider_service.sync_all_platforms(db)
    return success(
        data=[
            SpiderSyncLogResponse.model_validate(log).model_dump(mode="json")
            for log in sync_logs
        ],
        message=f"已启动 {len(sync_logs)} 个平台的同步任务",
    )


@router.get("/logs", summary="同步日志")
async def get_sync_logs(
    platform_id: Optional[UUID] = Query(None, description="平台ID筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取爬虫同步日志列表
    """
    logs, total = await spider_service.get_sync_logs(db, platform_id, page, page_size)
    return paginated(
        items=[
            SpiderSyncLogResponse.model_validate(log).model_dump(mode="json")
            for log in logs
        ],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/platforms/{platform_id}/test", summary="测试连接")
async def test_platform_connection(
    platform_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    测试爬虫平台连接
    """
    result = await spider_service.test_platform_connection(db, platform_id)
    return success(data=result)


@router.get("/tasks", summary="任务列表")
async def get_tasks(
    status: Optional[str] = Query(None, description="状态筛选: pending/running/success/failed"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取爬虫任务列表
    """
    tasks, total = await spider_service.get_tasks(db, status, page, page_size)
    return paginated(
        items=[
            SpiderTaskResponse.model_validate(task).model_dump(mode="json")
            for task in tasks
        ],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/tasks", summary="创建任务")
async def create_task(
    request: SpiderTaskCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    创建新的爬虫任务
    """
    task = await spider_service.create_task(db, request)
    return success(
        data=SpiderTaskResponse.model_validate(task).model_dump(mode="json"),
        message="任务创建成功",
    )


@router.post("/tasks/{task_id}/cancel", summary="取消任务")
async def cancel_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    取消待执行或运行中的爬虫任务
    """
    task = await spider_service.cancel_task(db, task_id)
    return success(
        data=SpiderTaskResponse.model_validate(task).model_dump(mode="json"),
        message="任务已取消",
    )

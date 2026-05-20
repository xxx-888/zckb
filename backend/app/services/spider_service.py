"""
爬虫服务模块
处理爬虫平台、同步日志、任务相关的业务逻辑
"""

import asyncio
import random
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException, NotFoundException
from app.models.spider import SpiderPlatform, SpiderSyncLog, SpiderTask
from app.schemas.spider import (
    SpiderPlatformCreateRequest,
    SpiderPlatformUpdateRequest,
    SpiderTaskCreateRequest,
)


async def get_platforms(db: AsyncSession) -> list[SpiderPlatform]:
    """
    获取所有爬虫平台列表

    Args:
        db: 数据库会话

    Returns:
        list[SpiderPlatform]: 平台列表
    """
    result = await db.execute(
        select(SpiderPlatform).order_by(SpiderPlatform.created_at.desc())
    )
    return list(result.scalars().all())


async def create_platform(
    db: AsyncSession,
    data: SpiderPlatformCreateRequest,
) -> SpiderPlatform:
    """
    创建爬虫平台

    Args:
        db: 数据库会话
        data: 创建请求数据

    Returns:
        SpiderPlatform: 创建成功的平台对象

    Raises:
        BusinessException: 平台名称已存在
    """
    # 检查平台名称是否已存在
    result = await db.execute(
        select(SpiderPlatform).where(SpiderPlatform.name == data.name)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise BusinessException(f"平台 '{data.name}' 已存在")

    platform = SpiderPlatform(
        name=data.name,
        display_name=data.display_name,
        status="active",
        reliability=1.0,
        config=data.config,
    )
    db.add(platform)
    await db.flush()
    await db.refresh(platform)

    return platform


async def update_platform(
    db: AsyncSession,
    platform_id: UUID,
    data: SpiderPlatformUpdateRequest,
) -> SpiderPlatform:
    """
    更新爬虫平台

    Args:
        db: 数据库会话
        platform_id: 平台ID
        data: 更新请求数据

    Returns:
        SpiderPlatform: 更新后的平台对象

    Raises:
        NotFoundException: 平台不存在
    """
    result = await db.execute(
        select(SpiderPlatform).where(SpiderPlatform.id == platform_id)
    )
    platform = result.scalar_one_or_none()

    if not platform:
        raise NotFoundException("爬虫平台不存在")

    if data.display_name is not None:
        platform.display_name = data.display_name
    if data.status is not None:
        platform.status = data.status
    if data.config is not None:
        platform.config = data.config

    await db.flush()
    await db.refresh(platform)

    return platform


async def delete_platform(db: AsyncSession, platform_id: UUID) -> None:
    """
    删除爬虫平台

    Args:
        db: 数据库会话
        platform_id: 平台ID

    Raises:
        NotFoundException: 平台不存在
    """
    result = await db.execute(
        select(SpiderPlatform).where(SpiderPlatform.id == platform_id)
    )
    platform = result.scalar_one_or_none()

    if not platform:
        raise NotFoundException("爬虫平台不存在")

    await db.delete(platform)
    await db.flush()


async def sync_platform(
    db: AsyncSession,
    platform_id: UUID,
    store_id: Optional[UUID] = None,
) -> SpiderSyncLog:
    """
    同步单个平台数据

    Args:
        db: 数据库会话
        platform_id: 平台ID
        store_id: 门店ID（可选）

    Returns:
        SpiderSyncLog: 同步日志记录

    Raises:
        NotFoundException: 平台不存在
    """
    result = await db.execute(
        select(SpiderPlatform).where(SpiderPlatform.id == platform_id)
    )
    platform = result.scalar_one_or_none()

    if not platform:
        raise NotFoundException("爬虫平台不存在")

    # 创建同步日志
    sync_log = SpiderSyncLog(
        platform_id=platform_id,
        store_id=store_id,
        status="running",
        records_synced=0,
        started_at=datetime.utcnow(),
    )
    db.add(sync_log)
    await db.flush()

    try:
        # 模拟爬虫同步过程
        sync_result = await _simulate_spider_sync(platform_id, store_id)

        sync_log.status = "success" if sync_result["success"] else "failed"
        sync_log.records_synced = sync_result.get("records_synced", 0)
        sync_log.error_message = sync_result.get("error_message")
        sync_log.duration_ms = sync_result.get("duration_ms")
        sync_log.finished_at = datetime.utcnow()

        # 更新平台最后同步时间
        platform.last_sync_at = datetime.utcnow()
        platform.status = "active"
        platform.error_log = None

    except Exception as e:
        sync_log.status = "failed"
        sync_log.error_message = str(e)
        sync_log.finished_at = datetime.utcnow()

        # 更新平台状态为异常
        platform.status = "error"
        platform.error_log = str(e)

    await db.flush()
    await db.refresh(sync_log)

    return sync_log


async def sync_all_platforms(db: AsyncSession) -> list[SpiderSyncLog]:
    """
    同步所有活跃平台

    Args:
        db: 数据库会话

    Returns:
        list[SpiderSyncLog]: 同步日志记录列表
    """
    result = await db.execute(
        select(SpiderPlatform).where(SpiderPlatform.status == "active")
    )
    platforms = list(result.scalars().all())

    sync_logs = []
    for platform in platforms:
        sync_log = await sync_platform(db, platform.id)
        sync_logs.append(sync_log)

    return sync_logs


async def get_sync_logs(
    db: AsyncSession,
    platform_id: Optional[UUID] = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[SpiderSyncLog], int]:
    """
    获取同步日志列表

    Args:
        db: 数据库会话
        platform_id: 平台ID筛选（可选）
        page: 页码
        page_size: 每页数量

    Returns:
        tuple: (日志列表, 总数)
    """
    conditions = []
    if platform_id:
        conditions.append(SpiderSyncLog.platform_id == platform_id)

    where_clause = and_(*conditions) if conditions else True

    # 查询总数
    count_stmt = select(func.count()).select_from(SpiderSyncLog).where(where_clause)
    total = (await db.execute(count_stmt)).scalar() or 0

    # 分页查询
    offset = (page - 1) * page_size
    stmt = (
        select(SpiderSyncLog)
        .where(where_clause)
        .order_by(SpiderSyncLog.started_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    logs = list(result.scalars().all())

    return logs, total


async def test_platform_connection(
    db: AsyncSession,
    platform_id: UUID,
) -> dict:
    """
    测试平台连接

    Args:
        db: 数据库会话
        platform_id: 平台ID

    Returns:
        dict: 测试结果

    Raises:
        NotFoundException: 平台不存在
    """
    result = await db.execute(
        select(SpiderPlatform).where(SpiderPlatform.id == platform_id)
    )
    platform = result.scalar_one_or_none()

    if not platform:
        raise NotFoundException("爬虫平台不存在")

    # 模拟连接测试
    start_time = datetime.utcnow()
    await asyncio.sleep(random.uniform(0.1, 0.5))  # 模拟网络延迟
    response_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)

    # 模拟成功率（95%成功率）
    success = random.random() < 0.95

    return {
        "success": success,
        "message": "连接成功" if success else "连接失败：无法访问平台API",
        "response_time_ms": response_time,
    }


async def create_task(
    db: AsyncSession,
    data: SpiderTaskCreateRequest,
) -> SpiderTask:
    """
    创建爬虫任务

    Args:
        db: 数据库会话
        data: 创建请求数据

    Returns:
        SpiderTask: 创建成功的任务对象

    Raises:
        NotFoundException: 平台不存在
    """
    # 验证平台存在
    result = await db.execute(
        select(SpiderPlatform).where(SpiderPlatform.id == data.platform_id)
    )
    platform = result.scalar_one_or_none()
    if not platform:
        raise NotFoundException("爬虫平台不存在")

    task = SpiderTask(
        platform_id=data.platform_id,
        store_id=data.store_id,
        task_type=data.task_type,
        status="pending",
        priority=data.priority,
        scheduled_at=data.scheduled_at or datetime.utcnow(),
    )
    db.add(task)
    await db.flush()
    await db.refresh(task)

    return task


async def get_tasks(
    db: AsyncSession,
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[SpiderTask], int]:
    """
    获取任务列表

    Args:
        db: 数据库会话
        status: 状态筛选（可选）
        page: 页码
        page_size: 每页数量

    Returns:
        tuple: (任务列表, 总数)
    """
    conditions = []
    if status:
        conditions.append(SpiderTask.status == status)

    where_clause = and_(*conditions) if conditions else True

    # 查询总数
    count_stmt = select(func.count()).select_from(SpiderTask).where(where_clause)
    total = (await db.execute(count_stmt)).scalar() or 0

    # 分页查询
    offset = (page - 1) * page_size
    stmt = (
        select(SpiderTask)
        .where(where_clause)
        .order_by(SpiderTask.priority.desc(), SpiderTask.scheduled_at.asc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    tasks = list(result.scalars().all())

    return tasks, total


async def get_task_by_id(
    db: AsyncSession,
    task_id: int,
) -> SpiderTask:
    """
    根据ID获取任务

    Args:
        db: 数据库会话
        task_id: 任务ID

    Returns:
        SpiderTask: 任务对象

    Raises:
        NotFoundException: 任务不存在
    """
    result = await db.execute(select(SpiderTask).where(SpiderTask.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise NotFoundException("爬虫任务不存在")

    return task


async def cancel_task(
    db: AsyncSession,
    task_id: int,
) -> SpiderTask:
    """
    取消爬虫任务

    Args:
        db: 数据库会话
        task_id: 任务ID

    Returns:
        SpiderTask: 更新后的任务对象

    Raises:
        NotFoundException: 任务不存在
        BusinessException: 任务状态不允许取消
    """
    task = await get_task_by_id(db, task_id)

    if task.status not in ("pending", "running"):
        raise BusinessException(f"任务状态为 '{task.status}'，无法取消")

    task.status = "failed"
    task.error_message = "任务已取消"
    task.finished_at = datetime.utcnow()

    await db.flush()
    await db.refresh(task)

    return task


async def _simulate_spider_sync(
    platform_id: UUID,
    store_id: Optional[UUID] = None,
) -> dict:
    """
    模拟爬虫同步过程

    Args:
        platform_id: 平台ID
        store_id: 门店ID（可选）

    Returns:
        dict: 同步结果
    """
    start_time = datetime.utcnow()

    # 模拟同步耗时（1-3秒）
    await asyncio.sleep(random.uniform(1.0, 3.0))

    # 模拟成功率（90%成功率）
    success = random.random() < 0.9

    duration_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)

    if success:
        return {
            "success": True,
            "records_synced": random.randint(10, 100),
            "duration_ms": duration_ms,
            "error_message": None,
        }
    else:
        return {
            "success": False,
            "records_synced": 0,
            "duration_ms": duration_ms,
            "error_message": "模拟同步失败：网络超时",
        }

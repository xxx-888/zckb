"""
FastAPI router for spider service API endpoints.
"""
from datetime import datetime
from typing import Any

from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.core.config import settings
from app.core.logger import get_logger
from app.spiders.factory import get_supported_platforms, is_platform_supported
from app.tasks.celery_app import celery
from app.tasks.spider_tasks import (
    monitor_reviews_task,
    reply_review_task,
    sync_reviews_task,
    sync_store_info_task,
)

logger = get_logger("api.router")
router = APIRouter(prefix="/api/v1", tags=["spider"])


# Pydantic models for request/response
class Credentials(BaseModel):
    """Platform credentials model."""
    username: str = Field(..., description="Platform username")
    password: str = Field(..., description="Platform password")
    cookies: dict[str, str] | None = Field(None, description="Optional cookies")
    token: str | None = Field(None, description="Optional access token")
    extra_data: dict[str, Any] = Field(default_factory=dict, description="Extra credential data")


class SyncReviewsRequest(BaseModel):
    """Request model for syncing reviews."""
    platform: str = Field(..., description="Platform name (meituan, douyin, taobao, jd)")
    store_id: str = Field(..., description="Store identifier")
    credentials: Credentials
    page: int = Field(1, ge=1, description="Page number")
    limit: int = Field(20, ge=1, le=100, description="Reviews per page")
    start_date: str | None = Field(None, description="Start date filter (ISO format)")
    end_date: str | None = Field(None, description="End date filter (ISO format)")


class SyncStoreRequest(BaseModel):
    """Request model for syncing store info."""
    platform: str = Field(..., description="Platform name")
    store_id: str = Field(..., description="Store identifier")
    credentials: Credentials


class ReplyReviewRequest(BaseModel):
    """Request model for replying to a review."""
    platform: str = Field(..., description="Platform name")
    review_id: str = Field(..., description="Review identifier")
    content: str = Field(..., min_length=1, max_length=1000, description="Reply content")
    credentials: Credentials
    store_id: str | None = Field(None, description="Optional store ID")


class MonitorReviewsRequest(BaseModel):
    """Request model for monitoring reviews."""
    platform: str = Field(..., description="Platform name")
    store_ids: list[str] = Field(..., min_length=1, description="List of store IDs to monitor")
    credentials: Credentials
    last_check_time: str | None = Field(None, description="Last check time (ISO format)")


class TaskResponse(BaseModel):
    """Response model for task submission."""
    task_id: str
    status: str
    message: str


class TaskStatusResponse(BaseModel):
    """Response model for task status."""
    task_id: str
    status: str
    result: dict[str, Any] | None = None
    traceback: str | None = None


class WorkerStatusResponse(BaseModel):
    """Response model for worker status."""
    active_workers: int
    registered_tasks: list[str]
    queues: list[str]
    broker_url: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: datetime
    version: str = "0.1.0"
    redis_connected: bool


# API Endpoints
@router.post(
    "/tasks/sync-reviews",
    response_model=TaskResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger review sync task",
    description="Start a background task to sync reviews from a platform",
)
async def sync_reviews(request: SyncReviewsRequest) -> TaskResponse:
    """Trigger a review sync task."""
    if not is_platform_supported(request.platform):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported platform: {request.platform}. "
            f"Supported: {get_supported_platforms()}",
        )

    task = sync_reviews_task.delay(
        platform=request.platform,
        store_id=request.store_id,
        credentials=request.credentials.model_dump(),
        page=request.page,
        limit=request.limit,
        start_date=request.start_date,
        end_date=request.end_date,
    )

    logger.info(f"Queued sync_reviews_task: {task.id}")
    return TaskResponse(
        task_id=task.id,
        status="queued",
        message="Review sync task has been queued",
    )


@router.post(
    "/tasks/sync-store",
    response_model=TaskResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger store info sync task",
    description="Start a background task to sync store information",
)
async def sync_store(request: SyncStoreRequest) -> TaskResponse:
    """Trigger a store info sync task."""
    if not is_platform_supported(request.platform):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported platform: {request.platform}",
        )

    task = sync_store_info_task.delay(
        platform=request.platform,
        store_id=request.store_id,
        credentials=request.credentials.model_dump(),
    )

    logger.info(f"Queued sync_store_info_task: {task.id}")
    return TaskResponse(
        task_id=task.id,
        status="queued",
        message="Store sync task has been queued",
    )


@router.post(
    "/tasks/reply-review",
    response_model=TaskResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger review reply task",
    description="Start a background task to reply to a review",
)
async def reply_review(request: ReplyReviewRequest) -> TaskResponse:
    """Trigger a review reply task."""
    if not is_platform_supported(request.platform):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported platform: {request.platform}",
        )

    task = reply_review_task.delay(
        platform=request.platform,
        review_id=request.review_id,
        content=request.content,
        credentials=request.credentials.model_dump(),
        store_id=request.store_id,
    )

    logger.info(f"Queued reply_review_task: {task.id}")
    return TaskResponse(
        task_id=task.id,
        status="queued",
        message="Reply task has been queued",
    )


@router.post(
    "/tasks/monitor-reviews",
    response_model=TaskResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger review monitoring task",
    description="Start a background task to monitor new reviews",
)
async def monitor_reviews(request: MonitorReviewsRequest) -> TaskResponse:
    """Trigger a review monitoring task."""
    if not is_platform_supported(request.platform):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported platform: {request.platform}",
        )

    task = monitor_reviews_task.delay(
        platform=request.platform,
        store_ids=request.store_ids,
        credentials=request.credentials.model_dump(),
        last_check_time=request.last_check_time,
    )

    logger.info(f"Queued monitor_reviews_task: {task.id}")
    return TaskResponse(
        task_id=task.id,
        status="queued",
        message="Monitor task has been queued",
    )


@router.get(
    "/tasks/{task_id}/status",
    response_model=TaskStatusResponse,
    summary="Get task status",
    description="Get the status and result of a task",
)
async def get_task_status(task_id: str) -> TaskStatusResponse:
    """Get the status of a Celery task."""
    task_result = AsyncResult(task_id, app=celery)

    result = None
    traceback = None
    if task_result.ready():
        try:
            result = task_result.get(timeout=1.0, propagate=False)
        except Exception as e:
            traceback = str(e)

    return TaskStatusResponse(
        task_id=task_id,
        status=task_result.status,
        result=result,
        traceback=traceback,
    )


@router.get(
    "/workers/status",
    response_model=WorkerStatusResponse,
    summary="Get worker status",
    description="Get status of Celery workers",
)
async def get_worker_status() -> WorkerStatusResponse:
    """Get Celery worker status."""
    try:
        # Get active workers
        inspector = celery.control.inspect()
        active = inspector.active() or {}
        registered = inspector.registered() or {}

        active_count = sum(len(tasks) for tasks in active.values())
        registered_tasks = list(set(
            task for tasks in registered.values() for task in tasks
        ))

        return WorkerStatusResponse(
            active_workers=active_count,
            registered_tasks=registered_tasks,
            queues=["spider", "monitor"],
            broker_url=str(settings.celery_broker_url),
        )
    except Exception as e:
        logger.error(f"Error getting worker status: {e}")
        return WorkerStatusResponse(
            active_workers=0,
            registered_tasks=[],
            queues=["spider", "monitor"],
            broker_url=str(settings.celery_broker_url),
        )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check service health status",
)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    redis_connected = False
    try:
        # Try to ping Redis
        from redis import Redis
        redis_client = Redis.from_url(str(settings.redis_url))
        redis_connected = redis_client.ping()
    except Exception:
        pass

    return HealthResponse(
        status="healthy" if redis_connected else "degraded",
        timestamp=datetime.now(),
        redis_connected=redis_connected,
    )


@router.get(
    "/platforms",
    summary="Get supported platforms",
    description="Get list of supported platforms",
)
async def get_platforms() -> dict[str, Any]:
    """Get supported platforms."""
    return {
        "platforms": get_supported_platforms(),
        "count": len(get_supported_platforms()),
    }

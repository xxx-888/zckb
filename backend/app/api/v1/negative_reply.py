"""
差评处理路由模块
处理差评自动回复审核相关接口
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.core.response import paginated, success
from app.models.user import User
from app.schemas.negative_reply import (
    ApproveRequest,
    NegativeReplyHistoryResponse,
    NegativeReplyTaskListResponse,
    NegativeReplyTaskResponse,
    RejectRequest,
)
from app.services import negative_reply_service

router = APIRouter(prefix="/negative-reply", tags=["差评处理"])


@router.get("/tasks", summary="差评任务列表")
async def get_tasks(
    status: str | None = Query(None, description="状态筛选: pending/approved/rejected/sent"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页大小"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取差评处理任务列表
    - 待审核的AI生成回复
    - 支持按状态筛选
    """
    tasks, total = await negative_reply_service.get_tasks(
        db, current_user, status, page, page_size
    )
    return paginated(
        items=[NegativeReplyTaskResponse(**task).model_dump(mode="json") for task in tasks],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/tasks/{task_id}/approve", summary="批准并发送")
async def approve_task(
    task_id: UUID,
    request: ApproveRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    批准并发送差评回复
    - 审核通过AI生成的回复
    - 自动发送到平台
    """
    audit = await negative_reply_service.approve_task(db, task_id, current_user)
    return success(
        data={"task_id": str(audit.id), "status": audit.status},
        message="已批准并发送",
    )


@router.post("/tasks/{task_id}/reject", summary="驳回")
async def reject_task(
    task_id: UUID,
    request: RejectRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    驳回差评回复任务
    - 拒绝AI生成的回复
    - 需要填写驳回原因
    """
    audit = await negative_reply_service.reject_task(
        db, task_id, current_user, request.reason
    )
    return success(
        data={"task_id": str(audit.id), "status": audit.status},
        message="已驳回",
    )


@router.post("/tasks/{task_id}/regenerate", summary="重新生成AI回复")
async def regenerate_reply(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    重新生成AI回复
    - 对不满意的回复重新生成
    - 返回新的回复内容
    """
    audit = await negative_reply_service.regenerate_reply(db, task_id)
    return success(
        data={
            "task_id": str(audit.id),
            "ai_draft": audit.ai_reply_content,
            "status": audit.status,
        },
        message="已重新生成",
    )


@router.get("/history", summary="已处理历史")
async def get_history(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页大小"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取已处理历史记录
    - 已批准/驳回/发送的任务
    - 包含最终回复内容
    """
    history, total = await negative_reply_service.get_history(
        db, current_user, page, page_size
    )
    return paginated(
        items=[NegativeReplyHistoryResponse(**item).model_dump(mode="json") for item in history],
        total=total,
        page=page,
        page_size=page_size,
    )

"""
审核路由模块
处理AI回复审核相关的接口
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_valid_subscription, get_db
from app.core.response import paginated, success
from app.models.user import User
from app.schemas.audit import (
    AuditActionResponse,
    AuditApproveRequest,
    AuditItemResponse,
    AuditListResponse,
    AuditRejectRequest,
    AuditRegenerateRequest,
    AuditStatsResponse,
)
from app.services import audit_service

router = APIRouter(prefix="/audit", tags=["回复审核"])


@router.get("/stats", summary="审核统计")
async def get_audit_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取审核统计数据
    - 待审核数量
    - 已通过数量
    - 已拒绝数量
    - 已发送数量
    - 平均处理时间
    """
    stats = await audit_service.get_audit_stats(db)
    return success(data=stats)


@router.get("/list", summary="审核列表")
async def get_audit_list(
    status: Optional[str] = Query(None, description="状态筛选: pending/approved/rejected/sent"),
    keyword: Optional[str] = Query(None, description="关键词搜索(评论内容/用户名/门店名)"),
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取AI回复审核列表
    - 支持按状态筛选
    - 支持关键词搜索（评论内容、用户名、门店名）
    - 关联查询 Review + Store + User 返回完整数据
    """
    items, total = await audit_service.get_audit_list(
        db, status, keyword, page, limit
    )
    return paginated(
        items=items,
        total=total,
        page=page,
        page_size=limit,
    )


@router.get("/{audit_id}", summary="审核详情")
async def get_audit_detail(
    audit_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取审核记录详情（关联查询评论、门店、审核人完整数据）
    """
    item = await audit_service.get_audit_by_id(db, audit_id)
    return success(data=item)


@router.post("/{audit_id}/approve", summary="审核通过")
async def approve_audit(
    audit_id: UUID,
    request: AuditApproveRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    审核通过AI回复
    - 将AI回复设为正式回复
    - 更新评论回复状态
    """
    audit = await audit_service.approve_audit(db, audit_id, current_user.id)
    return success(
        data={
            "id": str(audit.id),
            "status": audit.status,
            "reviewed_at": audit.reviewed_at.isoformat() if audit.reviewed_at else None,
        },
        message="审核已通过",
    )


@router.post("/{audit_id}/reject", summary="审核拒绝")
async def reject_audit(
    audit_id: UUID,
    request: AuditRejectRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    审核拒绝AI回复
    - 记录拒绝原因
    - 审核状态变为已拒绝
    """
    audit = await audit_service.reject_audit(
        db, audit_id, current_user.id, request.reason
    )
    return success(
        data={
            "id": str(audit.id),
            "status": audit.status,
            "reject_reason": audit.reject_reason,
            "reviewed_at": audit.reviewed_at.isoformat() if audit.reviewed_at else None,
        },
        message="审核已拒绝",
    )


@router.post("/{audit_id}/regenerate", summary="重新生成回复")
async def regenerate_reply(
    audit_id: UUID,
    request: AuditRegenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    重新生成AI回复
    - 调用真实 AI 服务重新生成回复
    - 重新计算风险等级
    - 状态重置为 pending
    """
    audit = await audit_service.regenerate_reply(db, audit_id)
    return success(
        data={
            "id": str(audit.id),
            "ai_reply": audit.ai_reply_content,
            "status": audit.status,
        },
        message="回复已重新生成",
    )

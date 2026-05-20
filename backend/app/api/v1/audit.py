"""
审核路由模块
处理AI回复审核相关的接口
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_active_user
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


@router.get("/list", summary="待审核列表")
async def get_audit_list(
    status: Optional[str] = Query(None, description="状态筛选: pending/approved/rejected/sent"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取AI回复审核列表
    - 支持按状态筛选
    - 支持关键词搜索（评论内容、用户名等）
    """
    audits, total = await audit_service.get_audit_list(
        db, status, keyword, page, limit
    )
    return paginated(
        items=[
            AuditItemResponse.model_validate(audit).model_dump(mode="json")
            for audit in audits
        ],
        total=total,
        page=page,
        page_size=limit,
    )


@router.get("/{audit_id}", summary="审核详情")
async def get_audit_detail(
    audit_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取审核记录详情
    """
    audit = await audit_service.get_audit_by_id(db, audit_id)
    return success(
        data=AuditItemResponse.model_validate(audit).model_dump(mode="json")
    )


@router.post("/{audit_id}/approve", summary="审核通过")
async def approve_audit(
    audit_id: UUID,
    request: AuditApproveRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    审核通过AI回复
    - 将AI回复设为正式回复
    - 更新评论回复状态
    """
    audit = await audit_service.approve_audit(db, audit_id, current_user.id)
    return success(
        data=AuditActionResponse.model_validate(audit).model_dump(mode="json"),
        message="审核已通过",
    )


@router.post("/{audit_id}/reject", summary="审核拒绝")
async def reject_audit(
    audit_id: UUID,
    request: AuditRejectRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
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
        data=AuditActionResponse.model_validate(audit).model_dump(mode="json"),
        message="审核已拒绝",
    )


@router.post("/{audit_id}/regenerate", summary="重新生成回复")
async def regenerate_reply(
    audit_id: UUID,
    request: AuditRegenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    重新生成AI回复
    - 基于评论内容生成新的AI回复
    - 重新计算风险等级和评分
    """
    audit = await audit_service.regenerate_reply(db, audit_id)
    return success(
        data=AuditActionResponse.model_validate(audit).model_dump(mode="json"),
        message="回复已重新生成",
    )


@router.get("/stats", summary="审核统计")
async def get_audit_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取审核统计数据
    - 待审核数量
    - 已通过数量
    - 已拒绝数量
    - 平均处理时间
    """
    stats = await audit_service.get_audit_stats(db)
    return success(data=stats)

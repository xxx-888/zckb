"""
审核服务模块
处理AI回复审核相关的业务逻辑
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import and_, desc, or_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from app.core.exceptions import BusinessException, NotFoundException
from app.models.review import ReplyAudit, Review
from app.models.store import Store
from app.models.user import User


async def get_audit_list(
    db: AsyncSession,
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[ReplyAudit], int]:
    """
    获取审核列表，使用 ORM 预加载关联数据

    Args:
        db: 数据库会话
        status: 状态筛选（可选）
        keyword: 关键词搜索（匹配评论内容/用户名/门店名）
        page: 页码
        page_size: 每页数量

    Returns:
        tuple: (审核列表 ORM 对象列表, 总数)
    """
    conditions = []

    if status:
        conditions.append(ReplyAudit.status == status)

    # 关键词搜索需要 join Review/Store 来过滤
    if keyword:
        search_pattern = f"%{keyword}%"
        conditions.append(
            or_(
                Review.content.ilike(search_pattern),
                Review.user_name.ilike(search_pattern),
                Store.name.ilike(search_pattern),
            )
        )

    where_clause = and_(*conditions) if conditions else True

    # 查询总数
    count_stmt = (
        select(func.count(ReplyAudit.id))
        .select_from(ReplyAudit)
        .join(ReplyAudit.review)
        .join(ReplyAudit.store, isouter=True)
        .where(where_clause)
    )
    total = (await db.execute(count_stmt)).scalar() or 0

    # 分页查询：selectinload 预加载 review + store + auditor
    offset = (page - 1) * page_size
    stmt = (
        select(ReplyAudit)
        .options(
            selectinload(ReplyAudit.review),
            selectinload(ReplyAudit.store),
            selectinload(ReplyAudit.auditor),
        )
        .join(ReplyAudit.review)
        .join(ReplyAudit.store, isouter=True)
        .where(where_clause)
        .order_by(ReplyAudit.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    audits = result.unique().scalars().all()

    return audits, total


async def get_audit_by_id(db: AsyncSession, audit_id: UUID) -> ReplyAudit:
    """
    根据ID获取审核记录，预加载关联数据

    Args:
        db: 数据库会话
        audit_id: 审核ID

    Returns:
        ReplyAudit: 审核记录 ORM 对象

    Raises:
        NotFoundException: 审核记录不存在
    """
    stmt = (
        select(ReplyAudit)
        .options(
            selectinload(ReplyAudit.review),
            selectinload(ReplyAudit.store),
            selectinload(ReplyAudit.auditor),
        )
        .where(ReplyAudit.id == audit_id)
    )
    result = await db.execute(stmt)
    audit = result.unique().scalar_one_or_none()

    if not audit:
        raise NotFoundException("审核记录不存在")

    return audit


async def approve_audit(
    db: AsyncSession,
    audit_id: UUID,
    auditor_id: UUID,
) -> ReplyAudit:
    """
    审核通过：将状态改为 approved，并将 AI 回复写入 Review.reply
    """
    audit = await _get_audit_record(db, audit_id)

    if audit.status != "pending":
        raise BusinessException(f"审核状态为 '{audit.status}'，无法执行通过操作")

    audit.status = "approved"
    audit.auditor_id = auditor_id
    audit.reviewed_at = datetime.utcnow()

    # 将 AI 回复写入 Review
    review = await _get_review_for_audit(db, audit)
    if review and audit.ai_reply_content:
        review.reply = audit.ai_reply_content
        review.reply_time = datetime.utcnow()
        review.ai_generated = True
        review.ai_reply_draft = None

    await db.flush()
    await db.refresh(audit)
    return audit


async def reject_audit(
    db: AsyncSession,
    audit_id: UUID,
    auditor_id: UUID,
    reason: str,
) -> ReplyAudit:
    """
    审核拒绝：将状态改为 rejected，记录拒绝原因
    """
    audit = await _get_audit_record(db, audit_id)

    if audit.status != "pending":
        raise BusinessException(f"审核状态为 '{audit.status}'，无法执行拒绝操作")

    audit.status = "rejected"
    audit.auditor_id = auditor_id
    audit.reject_reason = reason
    audit.reviewed_at = datetime.utcnow()

    await db.flush()
    await db.refresh(audit)
    return audit


async def regenerate_reply(
    db: AsyncSession,
    audit_id: UUID,
) -> ReplyAudit:
    """
    重新生成AI回复：使用真实的 AIService 生成新回复
    """
    from app.services.negative_reply_service import regenerate_reply as negative_regenerate

    audit = await _get_audit_record(db, audit_id)

    if audit.status not in ("pending", "rejected"):
        raise BusinessException(f"审核状态为 '{audit.status}'，无法重新生成回复")

    # 委托给 negative_reply_service 的 regenerate_reply，它使用真实 AI
    audit = await negative_regenerate(db, audit_id)

    # 重新计算风险等级
    review = await _get_review_for_audit(db, audit)
    if review:
        audit.risk_level = _calculate_risk_level(review)

    audit.status = "pending"
    audit.reject_reason = None

    await db.flush()
    await db.refresh(audit)
    return audit


async def get_audit_stats(db: AsyncSession) -> dict:
    """
    获取审核统计数据：各状态计数、平均处理时间
    """
    status_stmt = (
        select(ReplyAudit.status, func.count())
        .group_by(ReplyAudit.status)
    )
    status_result = await db.execute(status_stmt)
    status_map = dict(status_result.all())

    pending_count = status_map.get("pending", 0)
    approved_count = status_map.get("approved", 0)
    rejected_count = status_map.get("rejected", 0)
    sent_count = status_map.get("sent", 0)
    total_count = sum(status_map.values())

    avg_time_stmt = select(
        func.avg(
            func.extract(
                "epoch",
                ReplyAudit.reviewed_at - ReplyAudit.created_at
            )
        )
    ).where(ReplyAudit.reviewed_at.isnot(None))
    avg_time = (await db.execute(avg_time_stmt)).scalar()

    avg_processing_time = round(float(avg_time), 2) if avg_time else None

    return {
        "pending_count": pending_count,
        "approved_count": approved_count,
        "rejected_count": rejected_count,
        "sent_count": sent_count,
        "total_count": total_count,
        "avg_processing_time": avg_processing_time,
    }


# ---- 内部辅助函数 ----

async def _get_audit_record(db: AsyncSession, audit_id: UUID) -> ReplyAudit:
    """根据ID获取审核记录 ORM 对象"""
    result = await db.execute(
        select(ReplyAudit).where(ReplyAudit.id == audit_id)
    )
    audit = result.scalar_one_or_none()
    if not audit:
        raise NotFoundException("审核记录不存在")
    return audit


async def _get_review_for_audit(db: AsyncSession, audit: ReplyAudit) -> Optional[Review]:
    """获取审核记录对应的评论"""
    result = await db.execute(
        select(Review).where(Review.id == audit.review_id)
    )
    return result.scalar_one_or_none()


def _calculate_risk_level(review: Review) -> str:
    """根据评分计算风险等级"""
    if review.rating <= 2:
        return "high"
    elif review.rating == 3:
        return "medium"
    else:
        return "low"

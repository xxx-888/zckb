"""
后台管理服务模块
处理系统统计、管理员用户、角色权限等后台管理业务逻辑
"""

import csv
import io
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException, NotFoundException
from app.core.security import get_password_hash
from app.models.review import ReplyAudit, Review
from app.models.spider import SpiderPlatform
from app.models.store import Store
from app.models.user import User
from app.schemas.admin import (
    AdminUserCreateRequest,
    AdminUserUpdateRequest,
    RoleCreateRequest,
    RoleUpdateRequest,
)


async def get_system_stats(db: AsyncSession, period: str = "30d") -> dict:
    """
    获取系统统计数据

    Args:
        db: 数据库会话
        period: 统计周期 (7d/30d/90d/all)

    Returns:
        dict: 统计数据
    """
    # 计算时间范围
    now = datetime.utcnow()
    if period == "7d":
        start_date = now - timedelta(days=7)
    elif period == "30d":
        start_date = now - timedelta(days=30)
    elif period == "90d":
        start_date = now - timedelta(days=90)
    else:
        start_date = None

    # 用户总数
    users_stmt = select(func.count()).select_from(User)
    total_users = (await db.execute(users_stmt)).scalar() or 0

    # 门店总数
    stores_stmt = select(func.count()).select_from(Store)
    total_stores = (await db.execute(stores_stmt)).scalar() or 0

    # 评论总数（按时间筛选）
    reviews_conditions = [Review.status == "normal"]
    if start_date:
        reviews_conditions.append(Review.created_at >= start_date)
    reviews_stmt = select(func.count()).select_from(Review).where(*reviews_conditions)
    total_reviews = (await db.execute(reviews_stmt)).scalar() or 0

    # 回复总数
    replies_stmt = select(func.count()).select_from(Review).where(
        Review.reply.isnot(None),
        *reviews_conditions
    )
    total_replies = (await db.execute(replies_stmt)).scalar() or 0

    # 待审核数量
    pending_audits_stmt = select(func.count()).select_from(ReplyAudit).where(
        ReplyAudit.status == "pending"
    )
    pending_audits = (await db.execute(pending_audits_stmt)).scalar() or 0

    # 活跃平台数
    active_platforms_stmt = select(func.count()).select_from(SpiderPlatform).where(
        SpiderPlatform.status == "active"
    )
    active_platforms = (await db.execute(active_platforms_stmt)).scalar() or 0

    return {
        "total_users": total_users,
        "total_stores": total_stores,
        "total_reviews": total_reviews,
        "total_replies": total_replies,
        "pending_audits": pending_audits,
        "active_platforms": active_platforms,
        "period": period,
    }


async def get_system_health(db: AsyncSession) -> dict:
    """
    获取系统健康状态

    Args:
        db: 数据库会话

    Returns:
        dict: 健康状态数据
    """
    # 检查数据库连接
    try:
        await db.execute(select(1))
        database_status = "connected"
    except Exception:
        database_status = "disconnected"

    # 检查爬虫服务状态
    spider_services = {}
    try:
        result = await db.execute(select(SpiderPlatform))
        platforms = list(result.scalars().all())
        for platform in platforms:
            spider_services[platform.name] = {
                "status": platform.status,
                "last_sync": platform.last_sync_at.isoformat() if platform.last_sync_at else None,
                "reliability": platform.reliability,
            }
    except Exception as e:
        spider_services["error"] = str(e)

    # 确定整体状态
    if database_status == "disconnected":
        overall_status = "unhealthy"
    elif any(s.get("status") == "error" for s in spider_services.values() if isinstance(s, dict)):
        overall_status = "degraded"
    else:
        overall_status = "healthy"

    return {
        "status": overall_status,
        "database": database_status,
        "cache": "connected",  # 模拟缓存状态
        "spider_services": spider_services,
        "timestamp": datetime.utcnow(),
    }


async def export_report(
    db: AsyncSession,
    report_type: str,
    period: str = "30d",
) -> bytes:
    """
    导出系统报告

    Args:
        db: 数据库会话
        report_type: 报告类型 (reviews/audits/stats)
        period: 时间周期

    Returns:
        bytes: CSV格式的报告数据

    Raises:
        BusinessException: 不支持的报告类型
    """
    output = io.StringIO()
    writer = csv.writer(output)

    if report_type == "reviews":
        # 导出评论数据
        writer.writerow(["评论ID", "门店ID", "平台", "用户名", "评分", "内容", "回复", "创建时间"])

        result = await db.execute(
            select(Review).where(Review.status == "normal").order_by(Review.created_at.desc())
        )
        reviews = list(result.scalars().all())

        for review in reviews:
            writer.writerow([
                str(review.id),
                str(review.store_id),
                review.platform,
                review.user_name or "",
                review.rating,
                (review.content or "")[:100],
                (review.reply or "")[:100],
                review.created_at.isoformat() if review.created_at else "",
            ])

    elif report_type == "audits":
        # 导出审核数据
        writer.writerow(["审核ID", "评论ID", "AI回复", "状态", "风险等级", "审核时间"])

        result = await db.execute(
            select(ReplyAudit).order_by(ReplyAudit.created_at.desc())
        )
        audits = list(result.scalars().all())

        for audit in audits:
            writer.writerow([
                str(audit.id),
                str(audit.review_id),
                (audit.ai_reply_content or "")[:100],
                audit.status,
                audit.risk_level or "",
                audit.reviewed_at.isoformat() if audit.reviewed_at else "",
            ])

    elif report_type == "stats":
        # 导出统计数据
        stats = await get_system_stats(db, period)
        writer.writerow(["指标", "数值"])
        for key, value in stats.items():
            writer.writerow([key, value])

    else:
        raise BusinessException(f"不支持的报告类型: {report_type}")

    return output.getvalue().encode("utf-8-sig")


async def get_admin_users(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[User], int]:
    """
    获取管理员用户列表

    Args:
        db: 数据库会话
        page: 页码
        page_size: 每页数量

    Returns:
        tuple: (用户列表, 总数)
    """
    # 查询总数
    count_stmt = select(func.count()).select_from(User)
    total = (await db.execute(count_stmt)).scalar() or 0

    # 分页查询
    offset = (page - 1) * page_size
    stmt = (
        select(User)
        .order_by(User.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    users = list(result.scalars().all())

    return users, total


async def create_admin_user(
    db: AsyncSession,
    data: AdminUserCreateRequest,
) -> User:
    """
    创建管理员用户

    Args:
        db: 数据库会话
        data: 创建请求数据

    Returns:
        User: 创建成功的用户对象

    Raises:
        BusinessException: 手机号或邮箱已存在
    """
    # 检查手机号是否已存在
    if data.phone:
        result = await db.execute(select(User).where(User.phone == data.phone))
        if result.scalar_one_or_none():
            raise BusinessException("该手机号已注册")

    # 检查邮箱是否已存在
    if data.email:
        result = await db.execute(select(User).where(User.email == data.email))
        if result.scalar_one_or_none():
            raise BusinessException("该邮箱已注册")

    user = User(
        username=data.username,
        phone=data.phone,
        email=data.email,
        hashed_password=get_password_hash(data.password),
        role=data.role,
        status="active",
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    return user


async def update_admin_user(
    db: AsyncSession,
    user_id: UUID,
    data: AdminUserUpdateRequest,
) -> User:
    """
    更新管理员用户

    Args:
        db: 数据库会话
        user_id: 用户ID
        data: 更新请求数据

    Returns:
        User: 更新后的用户对象

    Raises:
        NotFoundException: 用户不存在
        BusinessException: 手机号或邮箱已存在
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise NotFoundException("用户不存在")

    # 检查手机号是否冲突
    if data.phone and data.phone != user.phone:
        existing = await db.execute(select(User).where(User.phone == data.phone))
        if existing.scalar_one_or_none():
            raise BusinessException("该手机号已被其他用户使用")
        user.phone = data.phone

    # 检查邮箱是否冲突
    if data.email and data.email != user.email:
        existing = await db.execute(select(User).where(User.email == data.email))
        if existing.scalar_one_or_none():
            raise BusinessException("该邮箱已被其他用户使用")
        user.email = data.email

    if data.username is not None:
        user.username = data.username
    if data.role is not None:
        user.role = data.role

    await db.flush()
    await db.refresh(user)

    return user


async def disable_admin_user(
    db: AsyncSession,
    user_id: UUID,
) -> User:
    """
    禁用管理员用户

    Args:
        db: 数据库会话
        user_id: 用户ID

    Returns:
        User: 更新后的用户对象

    Raises:
        NotFoundException: 用户不存在
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise NotFoundException("用户不存在")

    user.status = "disabled"
    await db.flush()
    await db.refresh(user)

    return user


# 模拟角色数据存储（实际项目中应该使用数据库表）
_roles_db = {}
_role_id_counter = 0


def _get_next_role_id() -> UUID:
    """生成下一个角色ID（模拟）"""
    global _role_id_counter
    _role_id_counter += 1
    return UUID(int=_role_id_counter)


async def get_roles(db: AsyncSession) -> list[dict]:
    """
    获取角色列表

    Args:
        db: 数据库会话

    Returns:
        list[dict]: 角色列表
    """
    # 返回预定义的系统角色 + 自定义角色
    system_roles = [
        {
            "id": UUID("00000000-0000-0000-0000-000000000001"),
            "name": "超级管理员",
            "permissions": ["*"],
            "description": "拥有所有权限",
            "created_at": datetime.utcnow(),
        },
        {
            "id": UUID("00000000-0000-0000-0000-000000000002"),
            "name": "运营管理员",
            "permissions": ["review:read", "review:reply", "audit:read", "audit:approve", "spider:read"],
            "description": "负责日常运营和审核",
            "created_at": datetime.utcnow(),
        },
        {
            "id": UUID("00000000-0000-0000-0000-000000000003"),
            "name": "门店管理员",
            "permissions": ["review:read", "review:reply", "store:read"],
            "description": "管理单个门店",
            "created_at": datetime.utcnow(),
        },
    ]

    custom_roles = list(_roles_db.values())
    return system_roles + custom_roles


async def create_role(
    db: AsyncSession,
    data: RoleCreateRequest,
) -> dict:
    """
    创建角色

    Args:
        db: 数据库会话
        data: 创建请求数据

    Returns:
        dict: 创建成功的角色
    """
    role_id = _get_next_role_id()
    role = {
        "id": role_id,
        "name": data.name,
        "permissions": data.permissions,
        "description": data.description,
        "created_at": datetime.utcnow(),
    }
    _roles_db[role_id] = role
    return role


async def update_role(
    db: AsyncSession,
    role_id: UUID,
    data: RoleUpdateRequest,
) -> dict:
    """
    更新角色

    Args:
        db: 数据库会话
        role_id: 角色ID
        data: 更新请求数据

    Returns:
        dict: 更新后的角色

    Raises:
        NotFoundException: 角色不存在
    """
    # 检查是否是系统角色（不允许修改）
    system_ids = [
        UUID("00000000-0000-0000-0000-000000000001"),
        UUID("00000000-0000-0000-0000-000000000002"),
        UUID("00000000-0000-0000-0000-000000000003"),
    ]
    if role_id in system_ids:
        raise BusinessException("系统角色不允许修改")

    role = _roles_db.get(role_id)
    if not role:
        raise NotFoundException("角色不存在")

    if data.name is not None:
        role["name"] = data.name
    if data.permissions is not None:
        role["permissions"] = data.permissions
    if data.description is not None:
        role["description"] = data.description

    return role


async def get_permissions_structure(db: AsyncSession) -> list[dict]:
    """
    获取权限组织架构

    Args:
        db: 数据库会话

    Returns:
        list[dict]: 权限模块列表
    """
    return [
        {
            "module": "review",
            "name": "评论管理",
            "permissions": [
                {"id": "review:read", "name": "查看评论", "description": "查看评论列表和详情"},
                {"id": "review:reply", "name": "回复评论", "description": "对评论进行回复"},
                {"id": "review:delete", "name": "删除评论", "description": "删除评论"},
            ],
        },
        {
            "module": "audit",
            "name": "审核管理",
            "permissions": [
                {"id": "audit:read", "name": "查看审核", "description": "查看审核列表和详情"},
                {"id": "audit:approve", "name": "审核通过", "description": "通过AI回复审核"},
                {"id": "audit:reject", "name": "审核拒绝", "description": "拒绝AI回复审核"},
            ],
        },
        {
            "module": "spider",
            "name": "爬虫管理",
            "permissions": [
                {"id": "spider:read", "name": "查看爬虫", "description": "查看爬虫平台和日志"},
                {"id": "spider:manage", "name": "管理爬虫", "description": "管理爬虫平台和任务"},
                {"id": "spider:sync", "name": "同步数据", "description": "触发数据同步"},
            ],
        },
        {
            "module": "store",
            "name": "门店管理",
            "permissions": [
                {"id": "store:read", "name": "查看门店", "description": "查看门店列表和详情"},
                {"id": "store:manage", "name": "管理门店", "description": "创建和编辑门店"},
            ],
        },
        {
            "module": "user",
            "name": "用户管理",
            "permissions": [
                {"id": "user:read", "name": "查看用户", "description": "查看用户列表和详情"},
                {"id": "user:manage", "name": "管理用户", "description": "创建和编辑用户"},
            ],
        },
        {
            "module": "system",
            "name": "系统管理",
            "permissions": [
                {"id": "system:read", "name": "查看系统", "description": "查看系统统计和健康状态"},
                {"id": "system:config", "name": "系统配置", "description": "修改系统配置"},
            ],
        },
    ]

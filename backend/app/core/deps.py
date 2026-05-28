"""
依赖注入模块
提供认证、权限校验、订阅有效性检查等公共依赖
"""

from functools import wraps
from typing import Callable

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import ForbiddenException, UnauthorizedException, SubscriptionRequiredException
from app.core.security import decode_token
from app.models.user import User


# OAuth2 密码流，token 从 /api/v1/auth/login 获取
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    获取当前认证用户
    从 JWT token 中解析用户 ID，查询数据库获取用户信息

    Args:
        token: JWT token
        db: 数据库会话

    Returns:
        User: 当前用户对象

    Raises:
        UnauthorizedException: token 无效或用户不存在
    """
    credentials_exception = UnauthorizedException("无法验证用户凭据")

    try:
        payload = decode_token(token)
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except (ValueError, Exception):
        raise credentials_exception

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    获取当前活跃用户
    校验用户状态是否为启用

    Args:
        current_user: 当前用户

    Returns:
        User: 状态正常的用户

    Raises:
        ForbiddenException: 用户已被禁用
    """
    if current_user.status != "active":
        raise ForbiddenException("用户已被禁用，请联系管理员")
    return current_user


def require_roles(*roles: str) -> Callable:
    """
    角色权限校验工厂函数
    返回一个依赖，用于校验当前用户是否拥有指定角色
    SUPER_ADMIN 和 HQ 始终拥有所有权限

    用法:
        @router.get("/admin-only")
        async def admin_route(
            user: User = Depends(require_roles("HQ", "SUPER_ADMIN"))
        ):
            ...

    Args:
        *roles: 允许访问的角色列表

    Returns:
        Callable: FastAPI 依赖函数
    """
    # 超级管理员角色列表
    super_roles = ["SUPER_ADMIN", "HQ"]

    async def role_checker(
        current_user: User = Depends(get_current_active_user),
    ) -> User:
        # 超级管理员始终有所有权限
        if current_user.role and current_user.role.upper() in [r.upper() for r in super_roles]:
            return current_user

        # 不区分大小写检查角色
        user_role_upper = current_user.role.upper() if current_user.role else ''
        allowed_roles_upper = [r.upper() for r in roles]
        if user_role_upper not in allowed_roles_upper:
            raise ForbiddenException(
                f"权限不足，需要以下角色之一: {', '.join(roles)}"
            )
        return current_user

    return role_checker


async def require_valid_subscription(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    订阅有效性检查依赖。
    检查当前登录用户的订阅是否有效（trial 或 active 状态）。
    SUPER_ADMIN / HQ 角色直接跳过订阅检查。
    无效时抛出 SubscriptionRequiredException (402)。
    """
    # 后台管理账号跳过订阅检查
    super_roles = ["SUPER_ADMIN", "HQ"]
    if current_user.role and current_user.role.upper() in [r.upper() for r in super_roles]:
        return current_user

    from app.models.subscription import UserSubscription

    result = await db.execute(
        select(UserSubscription).where(
            UserSubscription.user_id == str(current_user.id),
            UserSubscription.status.in_(["trial", "active"]),
        ).order_by(UserSubscription.created_at.desc()).limit(1)
    )
    subscription = result.scalar_one_or_none()

    if not subscription:
        raise SubscriptionRequiredException()

    return current_user

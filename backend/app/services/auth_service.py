"""
认证服务模块
处理用户认证相关的业务逻辑
"""

# 调试：打印当前文件路径
import inspect
print(f"✅ Loading auth_service.py from: {inspect.getfile(inspect.currentframe())}")

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException, ForbiddenException, UnauthorizedException
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import RegisterRequest


async def authenticate_user(
    db: AsyncSession,
    username_or_phone: str,
    password: str,
) -> User:
    """
    验证用户凭据（支持用户名或手机号）
    
    Args:
        db: 数据库会话
        username_or_phone: 用户名或手机号
        password: 明文密码

    Returns:
        User: 认证成功的用户对象

    Raises:
        UnauthorizedException: 用户名/手机号或密码错误
    """
    # 先尝试用手机号查询
    result = await db.execute(select(User).where(User.phone == username_or_phone))
    user = result.scalar_one_or_none()
    
    # 如果没找到，再尝试用用户名查询
    if not user:
        result = await db.execute(select(User).where(User.username == username_or_phone))
        user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        raise UnauthorizedException("用户名/手机号或密码错误")

    if user.status != "active":
        raise ForbiddenException("用户已被禁用，请联系管理员")

    return user


async def create_user(
    db: AsyncSession,
    user_data: RegisterRequest,
) -> User:
    """
    创建新用户
    
    Args:
        db: 数据库会话
        user_data: 注册请求数据

    Returns:
        User: 创建成功的用户对象

    Raises:
        BusinessException: 手机号已注册
    """
    # 检查手机号是否已注册
    result = await db.execute(select(User).where(User.phone == user_data.phone))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise BusinessException("该手机号已注册，请直接登录")

    # 检查用户名是否已存在
    if user_data.username:
        result = await db.execute(select(User).where(User.username == user_data.username))
        if result.scalar_one_or_none():
            raise BusinessException("该用户名已被使用，请换一个")

    # 创建用户 - 默认角色为 STORE
    user = User(
        phone=user_data.phone,
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        role="STORE",
        last_login_at=datetime.utcnow(),
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    return user


def create_token_for_user(user: User) -> str:
    """
    为用户生成 JWT token

    Args:
        user: 用户对象

    Returns:
        str: JWT token 字符串
    """
    token_data = {
        "sub": str(user.id),
        "phone": user.phone,
        "role": user.role,
    }
    return create_access_token(token_data)

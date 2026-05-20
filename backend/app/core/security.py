"""
安全工具模块
提供 JWT Token 生成/验证、密码哈希等功能
"""

from datetime import datetime, timedelta, timezone

import jwt
import bcrypt

from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证明文密码与哈希密码是否匹配

    Args:
        plain_password: 明文密码
        hashed_password: 哈希后的密码

    Returns:
        bool: 密码是否匹配
    """
    # 使用 bcrypt 直接验证
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def get_password_hash(password: str) -> str:
    """
    对密码进行哈希处理

    Args:
        password: 明文密码

    Returns:
        str: 哈希后的密码（bcrypt 生成）
    """
    # 使用 bcrypt 直接哈希（自动处理 72 字节限制）
    password_bytes = password.encode('utf-8')[:72]  # 截断到 72 字节
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    """
    创建 JWT 访问令牌

    Args:
        data: 要编码到 token 中的数据（通常包含 sub 字段）
        expires_delta: 过期时间增量，默认使用配置中的值

    Returns:
        str: 编码后的 JWT token
    """
    to_encode = data.copy()

    if expires_delta is not None:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def decode_token(token: str) -> dict:
    """
    解码并验证 JWT token

    Args:
        token: JWT token 字符串

    Returns:
        dict: 解码后的 payload 数据

    Raises:
        jwt.InvalidTokenError: token 无效或已过期
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token 已过期")
    except jwt.InvalidTokenError:
        raise ValueError("无效的 Token")

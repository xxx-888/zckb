"""
认证相关 Schema
定义登录、注册、Token 等请求/响应数据结构
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """登录请求 - 支持用户名或手机号"""

    username_or_phone: str = Field(..., description="用户名或手机号", min_length=2, max_length=50)
    password: str = Field(..., description="密码", min_length=6)


class RegisterRequest(BaseModel):
    """注册请求"""

    phone: str = Field(..., description="手机号", min_length=11, max_length=11)
    password: str = Field(..., description="密码", min_length=6)
    username: str = Field(..., description="用户名", min_length=2, max_length=50)
    verify_code: str = Field(..., description="验证码", min_length=4, max_length=6, alias="verifyCode")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    role: Optional[str] = Field("user", description="角色")

    model_config = {"populate_by_name": True, "by_alias": True}


class UserInfo(BaseModel):
    """用户信息"""

    id: UUID
    phone: Optional[str] = None
    email: Optional[str] = None
    username: str
    role: str
    avatar: Optional[str] = None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """Token 响应"""

    access_token: str
    token_type: str = "bearer"
    user: UserInfo


class ForgotPasswordRequest(BaseModel):
    """忘记密码 - 发送验证码请求"""

    phone: str = Field(..., description="手机号", min_length=11, max_length=11)


class ResetPasswordRequest(BaseModel):
    """重置密码请求"""

    phone: str = Field(..., description="手机号", min_length=11, max_length=11)
    code: str = Field(..., description="验证码", min_length=6, max_length=6)
    new_password: str = Field(..., description="新密码", min_length=6)


class VerifyCodeRequest(BaseModel):
    """验证验证码请求（忘记密码第一步）"""

    phone: str = Field(..., description="手机号", min_length=11, max_length=11)
    code: str = Field(..., description="验证码", min_length=6, max_length=6)


class RefreshTokenRequest(BaseModel):
    """刷新 Token 请求"""

    access_token: str = Field(..., description="当前 access_token")

"""
认证路由模块
处理用户登录、注册、Token 刷新等认证相关接口
"""

from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.core.response import success
from app.core.security import create_access_token, decode_token, get_password_hash
from app.models.user import User
from app.models.verification_code import VerificationCode
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserInfo,
    VerifyCodeRequest,
)
from app.services import auth_service
from sqlalchemy import select, update, delete
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["认证管理"])


@router.post("/login", summary="用户登录")
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    用户登录接口
    - 验证用户名/手机号和密码
    - 返回 JWT token 和用户信息
    """
    user = await auth_service.authenticate_user(db, request.username_or_phone, request.password)
    access_token = auth_service.create_token_for_user(user)

    return success(
        data=TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserInfo.model_validate(user),
        ).model_dump(mode="json"),
        message="登录成功",
    )


@router.post("/register", summary="用户注册")
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    用户注册接口
    - 验证验证码
    - 创建新用户
    - 自动生成 JWT token
    """
    from app.core.exceptions import BusinessException
    from sqlalchemy import select, update
    from datetime import datetime
    
    # 验证验证码 - 从数据库查询
    result = await db.execute(
        select(VerificationCode)
        .where(
            (VerificationCode.phone == request.phone) &
            (VerificationCode.purpose == "register") &
            (VerificationCode.is_used == False)
        )
        .order_by(VerificationCode.created_at.desc())
        .limit(1)
    )
    verification_code = result.scalar_one_or_none()
    
    if not verification_code:
        raise BusinessException("请先获取验证码")
    
    # 检查是否过期
    now = datetime.utcnow()
    if now > verification_code.expires_at:
        raise BusinessException("验证码已过期，请重新获取")
    
    # 检查验证码是否正确
    if request.verify_code != verification_code.code:
        raise BusinessException("验证码错误")
    
    # 标记为已使用
    verification_code.is_used = True
    await db.flush()
    
    # 创建用户
    user = await auth_service.create_user(db, request)
    access_token = auth_service.create_token_for_user(user)

    return success(
        data=TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserInfo.model_validate(user),
        ).model_dump(mode="json"),
        message="注册成功",
    )


@router.post("/logout", summary="用户退出")
async def logout(
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    用户退出接口
    - 前端清除本地存储的 token 即可
    - 后端可在此处做 token 黑名单处理（如需要）
    """
    return success(message="退出成功")


@router.get("/current", summary="获取当前用户信息")
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取当前登录用户的详细信息
    """
    return success(
        data=UserInfo.model_validate(current_user).model_dump(mode="json"),
    )


@router.post("/register/send-code", summary="注册发送验证码")
async def send_register_code(
    request: ForgotPasswordRequest,  # 复用，只需要 phone 字段
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    注册发送验证码
    - 检查手机号是否已注册，已注册则提示直接登录
    - 对接阿里云短信服务发送验证码
    """
    import random
    from datetime import timedelta
    
    # 检查手机号是否已注册
    from sqlalchemy import select
    result = await db.execute(select(User).where(User.phone == request.phone))
    if result.scalar_one_or_none():
        from app.core.exceptions import BusinessException
        raise BusinessException("该手机号已注册，请直接登录")
    
    # 生成随机6位验证码
    code = "".join([str(random.randint(0, 9)) for _ in range(6)])
    
    # 计算过期时间（5分钟后）
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    
    # 先删除该手机号的旧验证码（如果有）
    from sqlalchemy import delete
    await db.execute(
        delete(VerificationCode).where(
            (VerificationCode.phone == request.phone) & 
            (VerificationCode.purpose == "register")
        )
    )
    
    # 保存新验证码到数据库
    verification_code = VerificationCode(
        phone=request.phone,
        code=code,
        purpose="register",
        expires_at=expires_at,
        is_used=False,
    )
    db.add(verification_code)
    await db.flush()
    
    # 对接阿里云短信服务发送验证码
    try:
        from app.services.sms_service import send_verification_code
        await send_verification_code(request.phone, code, "register")
        return success(message="验证码已发送到您的手机，5分钟内有效")
    except Exception as e:
        # 短信发送失败，但验证码已保存（方便调试）
        print(f"⚠️ 短信发送失败: {str(e)}")
        print(f"⚠️ 手机号: {request.phone}, 验证码: {code}")
        return success(message="验证码已发送，请注意查收")


@router.post("/forgot-password/send-code", summary="发送验证码")
async def send_reset_code(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    发送密码重置验证码
    - 生成随机6位验证码并保存到数据库
    - 生产环境对接短信服务
    - 当前为模拟实现，后台打印日志
    """
    from sqlalchemy import select, delete
    from datetime import datetime, timedelta
    import random

    result = await db.execute(select(User).where(User.phone == request.phone))
    user = result.scalar_one_or_none()

    if not user:
        from app.core.exceptions import BusinessException

        raise BusinessException("该手机号未注册")

    # 生成随机6位验证码
    code = "".join([str(random.randint(0, 9)) for _ in range(6)])
    
    # 计算过期时间（5分钟后）
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    
    # 先删除该手机号的旧验证码（如果有）
    await db.execute(
        delete(VerificationCode).where(
            (VerificationCode.phone == request.phone) & 
            (VerificationCode.purpose == "forgot_password")
        )
    )
    
    # 保存新验证码到数据库
    verification_code = VerificationCode(
        phone=request.phone,
        code=code,
        purpose="forgot_password",
        expires_at=expires_at,
        is_used=False,
    )
    db.add(verification_code)
    await db.flush()

    # 对接阿里云短信服务发送验证码
    try:
        from app.services.sms_service import send_verification_code
        await send_verification_code(request.phone, code, "reset_password")
        return success(message="验证码已发送到您的手机，5分钟内有效")
    except Exception as e:
        # 短信发送失败，但验证码已保存（方便调试）
        print(f"⚠️ 短信发送失败: {str(e)}")
        print(f"⚠️ 手机号: {request.phone}, 验证码: {code}")
        return success(message="验证码已发送，请注意查收")


@router.post("/forgot-password/verify-code", summary="验证验证码")
async def verify_reset_code(
    request: VerifyCodeRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    验证密码重置验证码
    - 从数据库验证验证码是否正确
    - 用于忘记密码流程的第一步验证
    """
    from sqlalchemy import select
    from datetime import datetime
    from app.core.exceptions import BusinessException

    # 验证验证码 - 从数据库查询
    result = await db.execute(
        select(VerificationCode)
        .where(
            (VerificationCode.phone == request.phone) &
            (VerificationCode.purpose == "forgot_password") &
            (VerificationCode.is_used == False)
        )
        .order_by(VerificationCode.created_at.desc())
        .limit(1)
    )
    verification_code = result.scalar_one_or_none()
    
    if not verification_code:
        raise BusinessException("请先获取验证码")

    # 检查是否过期
    now = datetime.utcnow()
    if now > verification_code.expires_at:
        raise BusinessException("验证码已过期，请重新获取")

    # 检查验证码是否正确
    if request.code != verification_code.code:
        raise BusinessException("验证码错误")

    return success(message="验证码正确")


@router.post("/forgot-password/reset", summary="重置密码")
async def reset_password(
    request: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    重置密码
    - 从数据库验证验证码
    - 更新用户密码
    - 标记验证码为已使用
    """
    from sqlalchemy import select
    from datetime import datetime
    from app.core.exceptions import BusinessException

    # 验证验证码 - 从数据库查询
    result = await db.execute(
        select(VerificationCode)
        .where(
            (VerificationCode.phone == request.phone) &
            (VerificationCode.purpose == "forgot_password") &
            (VerificationCode.is_used == False)
        )
        .order_by(VerificationCode.created_at.desc())
        .limit(1)
    )
    verification_code = result.scalar_one_or_none()
    
    if not verification_code:
        raise BusinessException("请先获取验证码")

    # 检查是否过期
    now = datetime.utcnow()
    if now > verification_code.expires_at:
        raise BusinessException("验证码已过期，请重新获取")

    # 检查验证码是否正确
    if request.code != verification_code.code:
        raise BusinessException("验证码错误")

    # 查询用户
    result = await db.execute(select(User).where(User.phone == request.phone))
    user = result.scalar_one_or_none()

    if not user:
        raise BusinessException("该手机号未注册")

    # 更新密码
    user.hashed_password = get_password_hash(request.new_password)
    
    # 标记验证码为已使用
    verification_code.is_used = True
    
    await db.flush()

    return success(message="密码重置成功")


@router.post("/refresh", summary="刷新Token")
async def refresh_token(
    request: RefreshTokenRequest,
) -> dict:
    """
    刷新 JWT Token
    - 验证当前 token 有效性
    - 生成新的 token
    """
    try:
        payload = decode_token(request.access_token)
        user_id = payload.get("sub")
        if not user_id:
            from app.core.exceptions import UnauthorizedException

            raise UnauthorizedException("无效的 Token")
    except ValueError:
        from app.core.exceptions import UnauthorizedException

        raise UnauthorizedException("Token 已过期或无效")

    # 生成新 token
    new_token = create_access_token(
        data={"sub": user_id, "phone": payload.get("phone"), "role": payload.get("role")}
    )

    return success(
        data={"access_token": new_token, "token_type": "bearer"},
        message="Token 刷新成功",
    )

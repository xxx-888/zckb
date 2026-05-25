"""
设置服务模块
处理回复模板、自动回复配置、通知设置、用户信息等业务逻辑
"""

from typing import Optional
from uuid import UUID
from datetime import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException, NotFoundException
from app.models.settings import (
    AutoReplyConfig,
    ReplyTemplate,
    UserNotificationSetting,
)
from app.models.user import User
from app.schemas.settings import (
    AutoReplyConfigUpdateRequest,
    ReplyTemplateCreateRequest,
    ReplyTemplateUpdateRequest,
    UserNotificationSettingUpdateRequest,
    UserInfoUpdateRequest,
)


# ==================== 回复模板 ====================


async def get_reply_templates(
    db: AsyncSession,
    user: User,
    store_id: Optional[UUID] = None,
) -> list[ReplyTemplate]:
    """
    获取回复模板列表

    Args:
        db: 数据库会话
        user: 当前用户
        store_id: 门店ID（可选，筛选指定门店模板）

    Returns:
        list[ReplyTemplate]: 回复模板列表
    """
    query = select(ReplyTemplate).where(ReplyTemplate.user_id == user.id)
    if store_id:
        query = query.where(ReplyTemplate.store_id == store_id)
    query = query.order_by(ReplyTemplate.created_at.desc())

    result = await db.execute(query)
    return list(result.scalars().all())


async def create_reply_template(
    db: AsyncSession,
    user: User,
    data: ReplyTemplateCreateRequest,
) -> ReplyTemplate:
    """
    创建回复模板

    Args:
        db: 数据库会话
        user: 当前用户
        data: 创建请求数据

    Returns:
        ReplyTemplate: 创建成功的模板对象
    """
    template = ReplyTemplate(
        user_id=user.id,
        name=data.name,
        type=data.type,
        content=data.content,
    )
    db.add(template)
    await db.flush()
    await db.refresh(template)

    return template


async def update_reply_template(
    db: AsyncSession,
    template_id: UUID,
    user: User,
    data: ReplyTemplateUpdateRequest,
) -> ReplyTemplate:
    """
    更新回复模板

    Args:
        db: 数据库会话
        template_id: 模板ID
        user: 当前用户
        data: 更新请求数据

    Returns:
        ReplyTemplate: 更新后的模板对象

    Raises:
        NotFoundException: 模板不存在
        BusinessException: 无权操作该模板
    """
    result = await db.execute(
        select(ReplyTemplate).where(ReplyTemplate.id == template_id)
    )
    template = result.scalar_one_or_none()

    if not template:
        raise NotFoundException("回复模板不存在")
    if template.user_id != user.id:
        raise BusinessException("无权操作该模板")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(template, field, value)

    await db.flush()
    await db.refresh(template)

    return template


async def delete_reply_template(
    db: AsyncSession,
    template_id: UUID,
    user: User,
) -> None:
    """
    删除回复模板

    Args:
        db: 数据库会话
        template_id: 模板ID
        user: 当前用户

    Raises:
        NotFoundException: 模板不存在
        BusinessException: 无权操作该模板
    """
    result = await db.execute(
        select(ReplyTemplate).where(ReplyTemplate.id == template_id)
    )
    template = result.scalar_one_or_none()

    if not template:
        raise NotFoundException("回复模板不存在")
    if template.user_id != user.id:
        raise BusinessException("无权操作该模板")

    await db.delete(template)
    await db.flush()


# ==================== 自动回复配置 ====================


async def get_auto_reply_config(
    db: AsyncSession,
    store_id: UUID,
) -> AutoReplyConfig:
    """
    获取自动回复配置

    Args:
        db: 数据库会话
        store_id: 门店ID

    Returns:
        AutoReplyConfig: 自动回复配置对象

    Raises:
        NotFoundException: 配置不存在
    """
    result = await db.execute(
        select(AutoReplyConfig).where(AutoReplyConfig.store_id == store_id)
    )
    config = result.scalar_one_or_none()

    if not config:
        # 自动创建默认配置
        config = AutoReplyConfig(
            store_id=store_id,
            mode='smart',
            auto_reply_enabled=True,
            work_hours_only=False,
            work_start_time=time(9, 0),
            work_end_time=time(21, 0),
            keyword_reply_enabled=True,
            keywords={},
            ai_suggest_enabled=True,
        )
        db.add(config)
        await db.flush()
        await db.refresh(config)

    return config


async def update_auto_reply_config(
    db: AsyncSession,
    store_id: UUID,
    data: AutoReplyConfigUpdateRequest,
) -> AutoReplyConfig:
    """
    更新自动回复配置

    Args:
        db: 数据库会话
        store_id: 门店ID
        data: 更新请求数据

    Returns:
        AutoReplyConfig: 更新后的配置对象

    Raises:
        NotFoundException: 配置不存在
    """
    result = await db.execute(
        select(AutoReplyConfig).where(AutoReplyConfig.store_id == store_id)
    )
    config = result.scalar_one_or_none()

    if not config:
        # 自动创建默认配置
        config = AutoReplyConfig(
            store_id=store_id,
            mode='smart',
            auto_reply_enabled=True,
            work_hours_only=False,
            work_start_time=time(9, 0),
            work_end_time=time(21, 0),
            keyword_reply_enabled=True,
            keywords={},
            ai_suggest_enabled=True,
        )
        db.add(config)
        await db.flush()
        await db.refresh(config)

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(config, field, value)

    await db.flush()
    await db.refresh(config)

    return config


# ==================== 用户通知设置 ====================


async def get_notification_setting(
    db: AsyncSession,
    user_id: UUID,
) -> UserNotificationSetting:
    """
    获取用户通知设置

    Args:
        db: 数据库会话
        user_id: 用户ID

    Returns:
        UserNotificationSetting: 通知设置对象

    Raises:
        NotFoundException: 设置不存在
    """
    result = await db.execute(
        select(UserNotificationSetting).where(
            UserNotificationSetting.user_id == user_id
        )
    )
    setting = result.scalar_one_or_none()

    if not setting:
        # 自动创建默认通知设置
        setting = UserNotificationSetting(
            user_id=user_id,
            new_review_enabled=True,
            negative_alert_enabled=True,
            weekly_report_enabled=True,
            email_enabled=True,
            sms_enabled=False,
            push_enabled=True,
        )
        db.add(setting)
        await db.flush()
        await db.refresh(setting)

    return setting


async def update_notification_setting(
    db: AsyncSession,
    user_id: UUID,
    data: UserNotificationSettingUpdateRequest,
) -> UserNotificationSetting:
    """
    更新用户通知设置

    Args:
        db: 数据库会话
        user_id: 用户ID
        data: 更新请求数据

    Returns:
        UserNotificationSetting: 更新后的设置对象

    Raises:
        NotFoundException: 设置不存在
    """
    result = await db.execute(
        select(UserNotificationSetting).where(
            UserNotificationSetting.user_id == user_id
        )
    )
    setting = result.scalar_one_or_none()

    if not setting:
        # 自动创建默认通知设置
        setting = UserNotificationSetting(
            user_id=user_id,
            new_review_enabled=True,
            negative_alert_enabled=True,
            weekly_report_enabled=True,
            email_enabled=True,
            sms_enabled=False,
            push_enabled=True,
        )
        db.add(setting)
        await db.flush()
        await db.refresh(setting)

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(setting, field, value)

    await db.flush()
    await db.refresh(setting)

    return setting


# ==================== 用户信息 ====================


async def get_user_info(
    db: AsyncSession,
    user_id: UUID,
) -> User:
    """
    获取用户信息

    Args:
        db: 数据库会话
        user_id: 用户ID

    Returns:
        User: 用户对象

    Raises:
        NotFoundException: 用户不存在
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise NotFoundException("用户不存在")

    return user


async def update_user_info(
    db: AsyncSession,
    user_id: UUID,
    data: UserInfoUpdateRequest,
) -> User:
    """
    更新用户信息

    Args:
        db: 数据库会话
        user_id: 用户ID
        data: 更新请求数据

    Returns:
        User: 更新后的用户对象

    Raises:
        NotFoundException: 用户不存在
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise NotFoundException("用户不存在")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.flush()
    await db.refresh(user)

    return user

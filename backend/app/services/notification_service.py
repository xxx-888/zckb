"""
通知服务模块
处理通知渠道、规则、历史、模板等业务逻辑
"""

import asyncio
import time
from typing import Optional
from uuid import UUID

import httpx
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.notification import (
    NotificationChannel,
    NotificationHistory,
    NotificationRule,
    NotificationTemplate,
)
from app.schemas.notification import (
    NotificationChannelCreateRequest,
    NotificationChannelUpdateRequest,
    NotificationRuleCreateRequest,
    NotificationRuleUpdateRequest,
    NotificationTemplateCreateRequest,
    NotificationTemplateUpdateRequest,
)


# ==================== 通知渠道 ====================


async def get_channels(db: AsyncSession) -> list[NotificationChannel]:
    """
    获取所有通知渠道列表

    Args:
        db: 数据库会话

    Returns:
        list[NotificationChannel]: 通知渠道列表
    """
    result = await db.execute(
        select(NotificationChannel).order_by(NotificationChannel.created_at.desc())
    )
    return list(result.scalars().all())


async def create_channel(
    db: AsyncSession,
    data: NotificationChannelCreateRequest,
) -> NotificationChannel:
    """
    创建通知渠道

    Args:
        db: 数据库会话
        data: 创建请求数据

    Returns:
        NotificationChannel: 创建成功的渠道对象
    """
    channel = NotificationChannel(
        name=data.name,
        type=data.type,
        webhook_url=data.webhook_url,
        config=data.config or {},
    )
    db.add(channel)
    await db.flush()
    await db.refresh(channel)

    return channel


async def update_channel(
    db: AsyncSession,
    channel_id: UUID,
    data: NotificationChannelUpdateRequest,
) -> NotificationChannel:
    """
    更新通知渠道

    Args:
        db: 数据库会话
        channel_id: 渠道ID
        data: 更新请求数据

    Returns:
        NotificationChannel: 更新后的渠道对象

    Raises:
        NotFoundException: 渠道不存在
    """
    result = await db.execute(
        select(NotificationChannel).where(NotificationChannel.id == channel_id)
    )
    channel = result.scalar_one_or_none()

    if not channel:
        raise NotFoundException("通知渠道不存在")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(channel, field, value)

    await db.flush()
    await db.refresh(channel)

    return channel


async def delete_channel(db: AsyncSession, channel_id: UUID) -> None:
    """
    删除通知渠道

    Args:
        db: 数据库会话
        channel_id: 渠道ID

    Raises:
        NotFoundException: 渠道不存在
    """
    result = await db.execute(
        select(NotificationChannel).where(NotificationChannel.id == channel_id)
    )
    channel = result.scalar_one_or_none()

    if not channel:
        raise NotFoundException("通知渠道不存在")

    await db.delete(channel)
    await db.flush()


async def test_channel(db: AsyncSession, channel_id: UUID) -> dict:
    """
    测试通知渠道

    Args:
        db: 数据库会话
        channel_id: 渠道ID

    Returns:
        dict: 测试结果

    Raises:
        NotFoundException: 渠道不存在
    """
    result = await db.execute(
        select(NotificationChannel).where(NotificationChannel.id == channel_id)
    )
    channel = result.scalar_one_or_none()

    if not channel:
        raise NotFoundException("通知渠道不存在")

    # 发送测试消息
    test_title = "测试通知"
    test_content = f"这是一条来自 {channel.name} 的测试消息"

    success = await _send_webhook(channel, test_title, test_content)

    return {
        "success": success,
        "message": "测试消息发送成功" if success else "测试消息发送失败",
    }


# ==================== 通知规则 ====================


async def get_rules(db: AsyncSession) -> list[NotificationRule]:
    """
    获取所有通知规则列表

    Args:
        db: 数据库会话

    Returns:
        list[NotificationRule]: 通知规则列表
    """
    result = await db.execute(
        select(NotificationRule).order_by(NotificationRule.created_at.desc())
    )
    rules = list(result.scalars().all())

    # 加载渠道名称
    for rule in rules:
        if rule.channel:
            rule.channel_name = rule.channel.name

    return rules


async def create_rule(
    db: AsyncSession,
    data: NotificationRuleCreateRequest,
) -> NotificationRule:
    """
    创建通知规则

    Args:
        db: 数据库会话
        data: 创建请求数据

    Returns:
        NotificationRule: 创建成功的规则对象

    Raises:
        NotFoundException: 渠道不存在
    """
    # 验证渠道是否存在
    channel_result = await db.execute(
        select(NotificationChannel).where(NotificationChannel.id == data.channel_id)
    )
    channel = channel_result.scalar_one_or_none()
    if not channel:
        raise NotFoundException("通知渠道不存在")

    rule = NotificationRule(
        name=data.name,
        channel_id=data.channel_id,
        event_type=data.event_type,
        condition=data.condition or {},
        frequency=data.frequency or "realtime",
    )
    db.add(rule)
    await db.flush()
    await db.refresh(rule)

    # 设置渠道名称
    rule.channel_name = channel.name

    return rule


async def update_rule(
    db: AsyncSession,
    rule_id: UUID,
    data: NotificationRuleUpdateRequest,
) -> NotificationRule:
    """
    更新通知规则

    Args:
        db: 数据库会话
        rule_id: 规则ID
        data: 更新请求数据

    Returns:
        NotificationRule: 更新后的规则对象

    Raises:
        NotFoundException: 规则不存在或渠道不存在
    """
    result = await db.execute(
        select(NotificationRule).where(NotificationRule.id == rule_id)
    )
    rule = result.scalar_one_or_none()

    if not rule:
        raise NotFoundException("通知规则不存在")

    # 如果更新了渠道ID，验证渠道是否存在
    if data.channel_id:
        channel_result = await db.execute(
            select(NotificationChannel).where(NotificationChannel.id == data.channel_id)
        )
        channel = channel_result.scalar_one_or_none()
        if not channel:
            raise NotFoundException("通知渠道不存在")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(rule, field, value)

    await db.flush()
    await db.refresh(rule)

    # 更新渠道名称
    if rule.channel:
        rule.channel_name = rule.channel.name

    return rule


async def delete_rule(db: AsyncSession, rule_id: UUID) -> None:
    """
    删除通知规则

    Args:
        db: 数据库会话
        rule_id: 规则ID

    Raises:
        NotFoundException: 规则不存在
    """
    result = await db.execute(
        select(NotificationRule).where(NotificationRule.id == rule_id)
    )
    rule = result.scalar_one_or_none()

    if not rule:
        raise NotFoundException("通知规则不存在")

    await db.delete(rule)
    await db.flush()


# ==================== 通知历史 ====================


async def get_history(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[NotificationHistory], int]:
    """
    获取通知历史列表

    Args:
        db: 数据库会话
        page: 页码
        page_size: 每页大小

    Returns:
        tuple[list[NotificationHistory], int]: 历史记录列表和总数
    """
    # 查询总数
    count_result = await db.execute(
        select(func.count()).select_from(NotificationHistory)
    )
    total = count_result.scalar() or 0

    # 查询列表
    result = await db.execute(
        select(NotificationHistory)
        .order_by(desc(NotificationHistory.created_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    histories = list(result.scalars().all())

    # 加载规则名称和渠道名称
    for history in histories:
        if history.rule:
            history.rule_name = history.rule.name
        if history.channel:
            history.channel_name = history.channel.name

    return histories, total


# ==================== 通知模板 ====================


async def get_templates(db: AsyncSession) -> list[NotificationTemplate]:
    """
    获取所有通知模板列表

    Args:
        db: 数据库会话

    Returns:
        list[NotificationTemplate]: 通知模板列表
    """
    result = await db.execute(
        select(NotificationTemplate).order_by(NotificationTemplate.created_at.desc())
    )
    return list(result.scalars().all())


async def create_template(
    db: AsyncSession,
    data: NotificationTemplateCreateRequest,
) -> NotificationTemplate:
    """
    创建通知模板

    Args:
        db: 数据库会话
        data: 创建请求数据

    Returns:
        NotificationTemplate: 创建成功的模板对象
    """
    template = NotificationTemplate(
        name=data.name,
        event_type=data.event_type,
        template_text=data.template_text,
        variables=data.variables or [],
    )
    db.add(template)
    await db.flush()
    await db.refresh(template)

    return template


async def update_template(
    db: AsyncSession,
    template_id: UUID,
    data: NotificationTemplateUpdateRequest,
) -> NotificationTemplate:
    """
    更新通知模板

    Args:
        db: 数据库会话
        template_id: 模板ID
        data: 更新请求数据

    Returns:
        NotificationTemplate: 更新后的模板对象

    Raises:
        NotFoundException: 模板不存在
    """
    result = await db.execute(
        select(NotificationTemplate).where(NotificationTemplate.id == template_id)
    )
    template = result.scalar_one_or_none()

    if not template:
        raise NotFoundException("通知模板不存在")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(template, field, value)

    await db.flush()
    await db.refresh(template)

    return template


# ==================== 发送通知 ====================


async def send_notification(
    db: AsyncSession,
    event_type: str,
    context: dict,
) -> None:
    """
    发送通知
    根据事件类型查找匹配的规则并发送通知

    Args:
        db: 数据库会话
        event_type: 事件类型
        context: 上下文数据，用于渲染模板
    """
    # 查找匹配的规则
    result = await db.execute(
        select(NotificationRule)
        .where(NotificationRule.event_type == event_type)
        .where(NotificationRule.is_active == True)
    )
    rules = result.scalars().all()

    if not rules:
        return

    # 查找匹配的模板
    template_result = await db.execute(
        select(NotificationTemplate)
        .where(NotificationTemplate.event_type == event_type)
        .where(NotificationTemplate.is_active == True)
    )
    template = template_result.scalar_one_or_none()

    # 渲染消息内容
    if template:
        title = f"【{template.name}】"
        content = _render_template(template.template_text, context)
    else:
        title = "【系统通知】"
        content = str(context)

    # 发送通知
    for rule in rules:
        if not rule.channel or not rule.channel.is_active:
            continue

        # 检查条件
        if rule.condition and not _check_condition(rule.condition, context):
            continue

        # 创建历史记录
        history = NotificationHistory(
            rule_id=rule.id,
            channel_id=rule.channel_id,
            title=title,
            content=content,
            recipient=_get_recipient(rule.channel),
            status="pending",
        )
        db.add(history)
        await db.flush()

        # 异步发送
        asyncio.create_task(
            _send_notification_async(db, history.id, rule.channel, title, content)
        )


async def _send_notification_async(
    db: AsyncSession,
    history_id: UUID,
    channel: NotificationChannel,
    title: str,
    content: str,
) -> None:
    """
    异步发送通知

    Args:
        db: 数据库会话
        history_id: 历史记录ID
        channel: 通知渠道
        title: 标题
        content: 内容
    """
    start_time = time.time()

    try:
        success = await _send_webhook(channel, title, content)
        status = "sent" if success else "failed"
        error_message = None if success else "发送失败"
    except Exception as e:
        status = "failed"
        error_message = str(e)

    latency_ms = int((time.time() - start_time) * 1000)

    # 更新历史记录
    result = await db.execute(
        select(NotificationHistory).where(NotificationHistory.id == history_id)
    )
    history = result.scalar_one_or_none()

    if history:
        history.status = status
        history.error_message = error_message
        history.latency_ms = latency_ms
        await db.flush()


async def _send_webhook(
    channel: NotificationChannel,
    title: str,
    content: str,
) -> bool:
    """
    发送 Webhook 通知

    Args:
        channel: 通知渠道
        title: 标题
        content: 内容

    Returns:
        bool: 是否发送成功
    """
    if not channel.webhook_url:
        return False

    try:
        # 根据不同渠道类型构建不同的消息格式
        if channel.type == "dingtalk":
            payload = {
                "msgtype": "markdown",
                "markdown": {
                    "title": title,
                    "text": content,
                },
            }
        elif channel.type == "feishu":
            payload = {
                "msg_type": "text",
                "content": {
                    "text": f"{title}\n{content}",
                },
            }
        elif channel.type == "wechat":
            payload = {
                "msgtype": "markdown",
                "markdown": {
                    "content": f"**{title}**\n{content}",
                },
            }
        else:
            payload = {
                "title": title,
                "content": content,
            }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                channel.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            return response.status_code == 200

    except Exception:
        return False


def _render_template(template_text: str, context: dict) -> str:
    """
    渲染模板

    Args:
        template_text: 模板文本
        context: 上下文数据

    Returns:
        str: 渲染后的文本
    """
    try:
        return template_text.format(**context)
    except (KeyError, ValueError):
        return template_text


def _check_condition(condition: dict, context: dict) -> bool:
    """
    检查条件是否满足

    Args:
        condition: 条件配置
        context: 上下文数据

    Returns:
        bool: 条件是否满足
    """
    # 简单的条件检查实现
    # 支持: {"field": "rating", "operator": "lt", "value": 3}
    field = condition.get("field")
    operator = condition.get("operator")
    value = condition.get("value")

    if not field or not operator:
        return True

    context_value = context.get(field)
    if context_value is None:
        return True

    if operator == "eq":
        return context_value == value
    elif operator == "ne":
        return context_value != value
    elif operator == "gt":
        return context_value > value
    elif operator == "gte":
        return context_value >= value
    elif operator == "lt":
        return context_value < value
    elif operator == "lte":
        return context_value <= value
    elif operator == "in":
        return context_value in value
    elif operator == "contains":
        return value in str(context_value)

    return True


def _get_recipient(channel: NotificationChannel) -> str | None:
    """
    获取接收者信息

    Args:
        channel: 通知渠道

    Returns:
        str | None: 接收者信息
    """
    if channel.config and "recipient" in channel.config:
        return channel.config["recipient"]
    return channel.webhook_url

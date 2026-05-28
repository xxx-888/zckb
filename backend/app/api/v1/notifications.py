"""
通知路由模块
处理通知渠道、规则、历史、模板等相关接口
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_valid_subscription, get_db
from app.core.response import paginated, success
from app.models.user import User
from app.schemas.notification import (
    NotificationChannelCreateRequest,
    NotificationChannelResponse,
    NotificationChannelUpdateRequest,
    NotificationHistoryResponse,
    NotificationRuleCreateRequest,
    NotificationRuleResponse,
    NotificationRuleUpdateRequest,
    NotificationTemplateCreateRequest,
    NotificationTemplateResponse,
    NotificationTemplateUpdateRequest,
)
from app.services import notification_service

router = APIRouter(prefix="/notifications", tags=["通知管理"])


# ==================== 通知渠道 ====================


@router.get("/channels", summary="渠道列表")
async def get_channels(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取所有通知渠道列表
    """
    channels = await notification_service.get_channels(db)
    return success(
        data=[
            NotificationChannelResponse.model_validate(c).model_dump(mode="json")
            for c in channels
        ]
    )


@router.post("/channels", summary="新增渠道")
async def create_channel(
    request: NotificationChannelCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    创建新的通知渠道
    - name: 渠道名称
    - type: 渠道类型 (wechat/dingtalk/feishu/email/sms/push)
    - webhook_url: Webhook URL
    - config: 渠道配置（可选）
    """
    channel = await notification_service.create_channel(db, request)
    return success(
        data=NotificationChannelResponse.model_validate(channel).model_dump(mode="json"),
        message="创建成功",
    )


@router.put("/channels/{channel_id}", summary="更新渠道")
async def update_channel(
    channel_id: UUID,
    request: NotificationChannelUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    更新指定通知渠道
    """
    channel = await notification_service.update_channel(db, channel_id, request)
    return success(
        data=NotificationChannelResponse.model_validate(channel).model_dump(mode="json"),
        message="更新成功",
    )


@router.delete("/channels/{channel_id}", summary="删除渠道")
async def delete_channel(
    channel_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    删除指定通知渠道
    """
    await notification_service.delete_channel(db, channel_id)
    return success(message="删除成功")


@router.post("/channels/{channel_id}/test", summary="测试渠道")
async def test_channel(
    channel_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    测试通知渠道是否正常工作
    发送一条测试消息到指定渠道
    """
    result = await notification_service.test_channel(db, channel_id)
    return success(data=result)


# ==================== 通知规则 ====================


@router.get("/rules", summary="规则列表")
async def get_rules(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取所有通知规则列表
    """
    rules = await notification_service.get_rules(db)
    return success(
        data=[
            NotificationRuleResponse.model_validate(r).model_dump(mode="json")
            for r in rules
        ]
    )


@router.post("/rules", summary="新增规则")
async def create_rule(
    request: NotificationRuleCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    创建新的通知规则
    - name: 规则名称
    - channel_id: 渠道ID
    - event_type: 事件类型 (new_review/negative_alert/weekly_report/spider_status)
    - condition: 触发条件（可选）
    - frequency: 频率 (realtime/daily/weekly)
    """
    rule = await notification_service.create_rule(db, request)
    return success(
        data=NotificationRuleResponse.model_validate(rule).model_dump(mode="json"),
        message="创建成功",
    )


@router.put("/rules/{rule_id}", summary="更新规则")
async def update_rule(
    rule_id: UUID,
    request: NotificationRuleUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    更新指定通知规则
    """
    rule = await notification_service.update_rule(db, rule_id, request)
    return success(
        data=NotificationRuleResponse.model_validate(rule).model_dump(mode="json"),
        message="更新成功",
    )


@router.delete("/rules/{rule_id}", summary="删除规则")
async def delete_rule(
    rule_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    删除指定通知规则
    """
    await notification_service.delete_rule(db, rule_id)
    return success(message="删除成功")


# ==================== 通知历史 ====================


@router.get("/history", summary="推送历史")
async def get_history(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页大小"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取通知推送历史记录
    支持分页查询
    """
    histories, total = await notification_service.get_history(db, page, page_size)
    return paginated(
        items=[
            NotificationHistoryResponse.model_validate(h).model_dump(mode="json")
            for h in histories
        ],
        total=total,
        page=page,
        page_size=page_size,
    )


# ==================== 通知模板 ====================


@router.get("/templates", summary="模板列表")
async def get_templates(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取所有通知模板列表
    """
    templates = await notification_service.get_templates(db)
    return success(
        data=[
            NotificationTemplateResponse.model_validate(t).model_dump(mode="json")
            for t in templates
        ]
    )


@router.post("/templates", summary="新增模板")
async def create_template(
    request: NotificationTemplateCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    创建新的通知模板
    - name: 模板名称
    - event_type: 事件类型 (new_review/negative_alert/weekly_report/spider_status)
    - template_text: 模板文本
    - variables: 变量列表（可选）
    """
    template = await notification_service.create_template(db, request)
    return success(
        data=NotificationTemplateResponse.model_validate(template).model_dump(
            mode="json"
        ),
        message="创建成功",
    )


@router.put("/templates/{template_id}", summary="更新模板")
async def update_template(
    template_id: UUID,
    request: NotificationTemplateUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    更新指定通知模板
    """
    template = await notification_service.update_template(db, template_id, request)
    return success(
        data=NotificationTemplateResponse.model_validate(template).model_dump(
            mode="json"
        ),
        message="更新成功",
    )

"""
设置路由模块
处理回复模板、自动回复配置、通知设置等相关接口
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_valid_subscription, get_db
from app.core.response import success
from app.models.user import User
from app.schemas.settings import (
    AutoReplyConfigResponse,
    AutoReplyConfigUpdateRequest,
    ReplyTemplateCreateRequest,
    ReplyTemplateResponse,
    ReplyTemplateUpdateRequest,
    UserNotificationSettingResponse,
    UserNotificationSettingUpdateRequest,
)
from app.services import settings_service

router = APIRouter(prefix="/settings", tags=["设置管理"])


# ==================== 回复模板 ====================


@router.get("/reply-templates", summary="回复模板列表")
async def get_reply_templates(
    store_id: UUID | None = Query(None, description="门店ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取当前用户的回复模板列表
    - 支持按门店ID筛选
    """
    templates = await settings_service.get_reply_templates(
        db, current_user, store_id
    )
    return success(
        data=[
            ReplyTemplateResponse.model_validate(t).model_dump(mode="json")
            for t in templates
        ]
    )


@router.post("/reply-templates", summary="创建回复模板")
async def create_reply_template(
    request: ReplyTemplateCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    创建新的回复模板
    - name: 模板名称
    - type: 模板类型 (good/bad/neutral)
    - content: 模板内容
    """
    template = await settings_service.create_reply_template(
        db, current_user, request
    )
    return success(
        data=ReplyTemplateResponse.model_validate(template).model_dump(mode="json"),
        message="创建成功",
    )


@router.put("/reply-templates/{template_id}", summary="更新回复模板")
async def update_reply_template(
    template_id: UUID,
    request: ReplyTemplateUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    更新指定回复模板
    - 只能更新自己创建的模板
    """
    template = await settings_service.update_reply_template(
        db, template_id, current_user, request
    )
    return success(
        data=ReplyTemplateResponse.model_validate(template).model_dump(mode="json"),
        message="更新成功",
    )


@router.delete("/reply-templates/{template_id}", summary="删除回复模板")
async def delete_reply_template(
    template_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    删除指定回复模板
    - 只能删除自己创建的模板
    """
    await settings_service.delete_reply_template(db, template_id, current_user)
    return success(message="删除成功")


# ==================== 自动回复配置 ====================


@router.get("/auto-reply", summary="获取自动回复配置")
async def get_auto_reply_config(
    store_id: UUID = Query(..., description="门店ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取指定门店的自动回复配置
    """
    config = await settings_service.get_auto_reply_config(db, store_id)
    return success(
        data=AutoReplyConfigResponse.model_validate(config).model_dump(mode="json")
    )


@router.put("/auto-reply", summary="更新自动回复配置")
async def update_auto_reply_config(
    store_id: UUID = Query(..., description="门店ID"),
    request: AutoReplyConfigUpdateRequest = ...,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    更新指定门店的自动回复配置
    - mode: 模式 (smart/semi_auto/manual)
    - auto_reply_enabled: 是否启用自动回复
    - work_hours_only: 仅工作时间回复
    - work_start_time: 工作开始时间
    - work_end_time: 工作结束时间
    - keyword_reply_enabled: 是否启用关键词回复
    - keywords: 关键词配置
    - ai_suggest_enabled: 是否启用AI建议
    """
    config = await settings_service.update_auto_reply_config(db, store_id, request)
    return success(
        data=AutoReplyConfigResponse.model_validate(config).model_dump(mode="json"),
        message="更新成功",
    )


# ==================== 通知设置 ====================


@router.get("/notification", summary="获取通知设置")
async def get_notification_setting(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    获取当前用户的通知设置
    """
    setting = await settings_service.get_notification_setting(db, current_user.id)
    return success(
        data=UserNotificationSettingResponse.model_validate(setting).model_dump(
            mode="json"
        )
    )


@router.put("/notification", summary="更新通知设置")
async def update_notification_setting(
    request: UserNotificationSettingUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_valid_subscription),
) -> dict:
    """
    更新当前用户的通知设置
    - new_review_enabled: 新评论通知
    - negative_alert_enabled: 差评预警通知
    - weekly_report_enabled: 周报通知
    - email_enabled: 邮件通知
    - sms_enabled: 短信通知
    - push_enabled: 推送通知
    - quiet_hours_start: 免打扰开始时间
    - quiet_hours_end: 免打扰结束时间
    """
    setting = await settings_service.update_notification_setting(
        db, current_user.id, request
    )
    return success(
        data=UserNotificationSettingResponse.model_validate(setting).model_dump(
            mode="json"
        ),
        message="更新成功",
    )

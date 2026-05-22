"""
AI配置路由模块（后台管理）
处理AI模型配置、提示词配置、规则引擎等管理接口
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.core.response import success
from app.models.user import User
from app.schemas.ai_config import (
    AIModelConfigCreateRequest,
    AIModelConfigResponse,
    AIMonitoringResponse,
    AIPromptConfigCreateRequest,
    AIPromptConfigResponse,
    AIRuleEngineCreateRequest,
    AIRuleEngineResponse,
    AIEvaluationResponse,
)
from app.services import ai_config_service

router = APIRouter(prefix="/ai", tags=["AI配置管理"])


@router.get("/config", summary="获取AI配置")
async def get_ai_config(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取AI整体配置信息
    - 包含模型、提示词、规则引擎等配置概览
    """
    # 获取各类配置
    model_configs = await ai_config_service.get_model_configs(db)
    prompt_configs = await ai_config_service.get_prompt_configs(db)
    rule_engines = await ai_config_service.get_rule_engines(db)

    return success(
        data={
            "models": [AIModelConfigResponse.model_validate(m).model_dump(mode="json") for m in model_configs],
            "prompts": [AIPromptConfigResponse.model_validate(p).model_dump(mode="json") for p in prompt_configs],
            "rules": [AIRuleEngineResponse.model_validate(r).model_dump(mode="json") for r in rule_engines],
        }
    )


@router.get("/models", summary="获取模型配置列表")
async def get_model_configs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取AI模型配置列表
    - 支持多模型配置
    - 包含优先级、状态等信息
    """
    configs = await ai_config_service.get_model_configs(db)
    return success(
        data=[AIModelConfigResponse.model_validate(c).model_dump(mode="json") for c in configs]
    )


@router.post("/models", summary="新增模型配置")
async def create_model_config(
    request: AIModelConfigCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    新增AI模型配置
    - 支持OpenAI、智谱、文心、DeepSeek等多种模型
    """
    config = await ai_config_service.create_model_config(db, request)
    return success(
        data=AIModelConfigResponse.model_validate(config).model_dump(mode="json"),
        message="模型配置创建成功",
    )


@router.put("/models/{config_id}", summary="更新模型配置")
async def update_model_config(
    config_id: UUID,
    request: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    更新模型配置
    - 修改模型参数、API密钥等
    """
    config = await ai_config_service.update_model_config(db, config_id, request)
    return success(
        data=AIModelConfigResponse.model_validate(config).model_dump(mode="json"),
        message="模型配置更新成功",
    )


@router.delete("/models/{config_id}", summary="删除模型配置")
async def delete_model_config(
    config_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    删除模型配置
    """
    await ai_config_service.delete_model_config(db, config_id)
    return success(message="模型配置删除成功")


@router.post("/models/{config_id}/test", summary="测试模型连接")
async def test_model_config(
    config_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    测试模型连接
    - 验证API密钥和连接状态
    - 返回延迟测试结果
    """
    result = await ai_config_service.test_model_config(db, config_id)
    return success(data=result)


@router.get("/prompts", summary="获取提示词配置")
async def get_prompt_configs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取提示词模板配置
    - 好评/差评/中评回复模板
    - 申诉模板、周报模板等
    """
    configs = await ai_config_service.get_prompt_configs(db)
    return success(
        data=[AIPromptConfigResponse.model_validate(c).model_dump(mode="json") for c in configs]
    )


@router.post("/prompts", summary="新增提示词配置")
async def create_prompt_config(
    request: AIPromptConfigCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    新增提示词配置
    - 创建好评/差评/中评回复模板
    - 创建申诉模板、周报模板等
    """
    config = await ai_config_service.create_prompt_config(db, request)
    return success(
        data=AIPromptConfigResponse.model_validate(config).model_dump(mode="json"),
        message="提示词配置创建成功",
    )


@router.put("/prompts/{config_id}", summary="更新提示词配置")
async def update_prompt_config(
    config_id: UUID,
    request: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    更新提示词配置
    - 修改模板文本、变量、系统提示词等
    """
    config = await ai_config_service.update_prompt_config(db, config_id, request)
    return success(
        data=AIPromptConfigResponse.model_validate(config).model_dump(mode="json"),
        message="提示词配置更新成功",
    )


@router.get("/rules", summary="获取规则引擎")
async def get_rule_engines(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取AI规则引擎配置
    - 差评识别规则
    - 自动回复触发规则
    - 风险分级规则等
    """
    engines = await ai_config_service.get_rule_engines(db)
    return success(
        data=[AIRuleEngineResponse.model_validate(e).model_dump(mode="json") for e in engines]
    )


@router.post("/rules", summary="新增规则引擎")
async def create_rule_engine(
    request: AIRuleEngineCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    新增规则引擎
    - 差评识别规则
    - 自动回复触发规则
    - 风险分级规则等
    """
    engine = await ai_config_service.create_rule_engine(db, request)
    return success(
        data=AIRuleEngineResponse.model_validate(engine).model_dump(mode="json"),
        message="规则引擎创建成功",
    )


@router.put("/rules/{engine_id}", summary="更新规则引擎")
async def update_rule_engine(
    engine_id: UUID,
    request: dict,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    更新规则引擎配置
    - 修改规则定义、优先级等
    """
    engine = await ai_config_service.update_rule_engine(db, engine_id, request)
    return success(
        data=AIRuleEngineResponse.model_validate(engine).model_dump(mode="json"),
        message="规则引擎更新成功",
    )


@router.get("/monitoring", summary="实时监控数据")
async def get_monitoring_data(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取AI服务实时监控数据
    - 请求量、成功率、延迟等
    - 活跃模型数
    """
    data = await ai_config_service.get_monitoring_data(db)
    return success(data=AIMonitoringResponse(**data).model_dump(mode="json"))


@router.get("/evaluation", summary="效能评估")
async def get_evaluation_data(
    period: str = Query("7d", description="评估周期"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> dict:
    """
    获取AI效能评估数据
    - 评估周期内的整体表现
    - 改进建议
    """
    data = await ai_config_service.get_evaluation_data(db, period)
    return success(data=AIEvaluationResponse(**data).model_dump(mode="json"))

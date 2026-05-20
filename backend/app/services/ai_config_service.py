"""
AI配置服务模块
提供AI模型配置、提示词配置、规则引擎、监控数据等功能
"""

import random
from datetime import datetime
from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException, NotFoundException
from app.core.security import get_password_hash
from app.models.ai_config import AIModelConfig, AIPromptTemplate, AIRuleEngine
from app.schemas.ai_config import AIModelConfigCreateRequest


async def get_model_configs(db: AsyncSession) -> list[AIModelConfig]:
    """
    获取模型配置列表

    Args:
        db: 数据库会话

    Returns:
        list[AIModelConfig]: 模型配置列表
    """
    stmt = select(AIModelConfig).order_by(desc(AIModelConfig.priority))
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_model_config(
    db: AsyncSession, data: AIModelConfigCreateRequest
) -> AIModelConfig:
    """
    创建模型配置

    Args:
        db: 数据库会话
        data: 创建数据

    Returns:
        AIModelConfig: 创建的模型配置
    """
    # 加密API Key
    api_key_encrypted = get_password_hash(data.api_key) if data.api_key else None

    config = AIModelConfig(
        provider=data.provider,
        model_name=data.model_name,
        api_key_encrypted=api_key_encrypted,
        endpoint_url=data.endpoint_url,
        is_active=data.is_active if data.is_active is not None else True,
        priority=data.priority if data.priority is not None else 0,
        max_tokens=data.max_tokens if data.max_tokens is not None else 2048,
        temperature=data.temperature if data.temperature is not None else 0.7,
    )

    db.add(config)
    await db.flush()
    return config


async def update_model_config(
    db: AsyncSession, config_id: UUID, data: dict
) -> AIModelConfig:
    """
    更新模型配置

    Args:
        db: 数据库会话
        config_id: 配置ID
        data: 更新数据

    Returns:
        AIModelConfig: 更新后的模型配置
    """
    stmt = select(AIModelConfig).where(AIModelConfig.id == config_id)
    result = await db.execute(stmt)
    config = result.scalar_one_or_none()

    if not config:
        raise NotFoundException("模型配置不存在")

    # 更新字段
    for key, value in data.items():
        if key == "api_key" and value:
            config.api_key_encrypted = get_password_hash(value)
        elif hasattr(config, key) and key != "api_key":
            setattr(config, key, value)

    await db.flush()
    return config


async def delete_model_config(db: AsyncSession, config_id: UUID) -> None:
    """
    删除模型配置

    Args:
        db: 数据库会话
        config_id: 配置ID

    Returns:
        None
    """
    stmt = select(AIModelConfig).where(AIModelConfig.id == config_id)
    result = await db.execute(stmt)
    config = result.scalar_one_or_none()

    if not config:
        raise NotFoundException("模型配置不存在")

    await db.delete(config)
    await db.flush()


async def test_model_config(db: AsyncSession, config_id: UUID) -> dict:
    """
    测试模型连接

    Args:
        db: 数据库会话
        config_id: 配置ID

    Returns:
        dict: 测试结果
    """
    stmt = select(AIModelConfig).where(AIModelConfig.id == config_id)
    result = await db.execute(stmt)
    config = result.scalar_one_or_none()

    if not config:
        raise NotFoundException("模型配置不存在")

    # 模拟连接测试
    # 实际应用中应调用模型API进行测试
    success = random.random() > 0.2  # 80%成功率模拟

    if success:
        return {
            "success": True,
            "message": "连接成功",
            "latency_ms": random.randint(100, 500),
        }
    else:
        return {
            "success": False,
            "message": "连接失败：API密钥无效或网络错误",
            "latency_ms": 0,
        }


async def get_prompt_configs(db: AsyncSession) -> list[AIPromptTemplate]:
    """
    获取提示词配置列表

    Args:
        db: 数据库会话

    Returns:
        list[AIPromptTemplate]: 提示词配置列表
    """
    stmt = select(AIPromptTemplate).order_by(AIPromptTemplate.type)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def update_prompt_config(
    db: AsyncSession, config_id: UUID, data: dict
) -> AIPromptTemplate:
    """
    更新提示词配置

    Args:
        db: 数据库会话
        config_id: 配置ID
        data: 更新数据

    Returns:
        AIPromptTemplate: 更新后的提示词配置
    """
    stmt = select(AIPromptTemplate).where(AIPromptTemplate.id == config_id)
    result = await db.execute(stmt)
    config = result.scalar_one_or_none()

    if not config:
        raise NotFoundException("提示词配置不存在")

    # 更新字段
    for key, value in data.items():
        if hasattr(config, key):
            setattr(config, key, value)

    await db.flush()
    return config


async def get_rule_engines(db: AsyncSession) -> list[AIRuleEngine]:
    """
    获取规则引擎列表

    Args:
        db: 数据库会话

    Returns:
        list[AIRuleEngine]: 规则引擎列表
    """
    stmt = select(AIRuleEngine).order_by(desc(AIRuleEngine.priority))
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def update_rule_engine(
    db: AsyncSession, engine_id: UUID, data: dict
) -> AIRuleEngine:
    """
    更新规则引擎

    Args:
        db: 数据库会话
        engine_id: 引擎ID
        data: 更新数据

    Returns:
        AIRuleEngine: 更新后的规则引擎
    """
    stmt = select(AIRuleEngine).where(AIRuleEngine.id == engine_id)
    result = await db.execute(stmt)
    engine = result.scalar_one_or_none()

    if not engine:
        raise NotFoundException("规则引擎不存在")

    # 更新字段
    for key, value in data.items():
        if hasattr(engine, key):
            setattr(engine, key, value)

    await db.flush()
    return engine


async def get_monitoring_data(db: AsyncSession) -> dict:
    """
    获取AI监控数据

    Args:
        db: 数据库会话

    Returns:
        dict: 监控数据
    """
    # 获取活跃模型数
    stmt = select(AIModelConfig).where(AIModelConfig.is_active == True)
    result = await db.execute(stmt)
    active_models = len(result.scalars().all())

    # 模拟监控数据
    return {
        "timestamp": datetime.now(),
        "total_requests": random.randint(1000, 5000),
        "success_rate": round(random.uniform(0.92, 0.99), 3),
        "avg_latency": round(random.uniform(200, 800), 1),
        "active_models": active_models or 2,
    }


async def get_evaluation_data(db: AsyncSession, period: str = "7d") -> dict:
    """
    获取AI效能评估数据

    Args:
        db: 数据库会话
        period: 评估周期

    Returns:
        dict: 评估数据
    """
    # 模拟评估数据
    return {
        "period": period,
        "total_evaluations": random.randint(500, 2000),
        "avg_score": round(random.uniform(3.5, 4.8), 1),
        "improvement_areas": [
            "回复个性化程度有待提升",
            "多轮对话处理能力需加强",
            "特定场景识别准确率可优化",
        ],
    }

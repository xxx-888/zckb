"""
AI配置服务模块
提供AI模型配置、提示词配置、规则引擎、监控数据等功能
"""

import asyncio
import json
import random
import time
from datetime import datetime
from uuid import UUID

import aiohttp
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException, NotFoundException
from app.core.security import encrypt_api_key, decrypt_api_key
from app.models.ai_config import AIModelConfig, AIPromptTemplate, AIRuleEngine
from app.schemas.ai_config import AIModelConfigCreateRequest, AIPromptConfigCreateRequest, AIRuleEngineCreateRequest



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
    api_key_encrypted = encrypt_api_key(data.api_key) if data.api_key else None

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
            config.api_key_encrypted = encrypt_api_key(value)
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


# 各提供商的默认 endpoint
_PROVIDER_DEFAULT_ENDPOINTS = {
    "openai": "https://api.openai.com/v1/chat/completions",
    "deepseek": "https://api.deepseek.com/v1/chat/completions",
    "zhipu": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
    "tongyi": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    "hunyuan": "https://api.hunyuan.cloud.tencent.com/v1/chat/completions",
    "doubao": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    "kimi": "https://api.moonshot.cn/v1/chat/completions",
    "wenxin": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions",
    "local": "http://localhost:11434/v1/chat/completions",
}


async def test_model_config(
    db: AsyncSession,
    config_id: UUID,
    test_message: str | None = None,
    api_key_override: str | None = None,
) -> dict:
    """
    真实调用厂商 API 测试模型连接

    Args:
        db: 数据库会话
        config_id: 配置ID
        test_message: 可选的测试消息，默认为通用测试提示
        api_key_override: 可选的 API Key（用于旧版 bcrypt 加密的模型）

    Returns:
        dict: 包含 success, reply, latency_ms, model_name, provider
    """
    stmt = select(AIModelConfig).where(AIModelConfig.id == config_id)
    result = await db.execute(stmt)
    config = result.scalar_one_or_none()

    if not config:
        raise NotFoundException("模型配置不存在")

    # 获取 API Key：优先用用户手动输入 > 尝试解密存储的 key
    api_key = None
    if api_key_override:
        api_key = api_key_override
    elif config.api_key_encrypted:
        try:
            api_key = decrypt_api_key(config.api_key_encrypted)
        except Exception:
            pass  # 旧版 bcrypt，解密失败，继续看有没有 override

    if not api_key:
        return {
            "success": False,
            "message": "未配置有效的 API Key。请在下方输入 API Key 后重新测试（旧版加密不兼容，或尚未配置）",
            "reply": None,
            "latency_ms": 0,
            "model_name": config.model_name,
            "provider": config.provider,
        }

    # 构建 endpoint
    endpoint = config.endpoint_url or _PROVIDER_DEFAULT_ENDPOINTS.get(
        config.provider, "https://api.openai.com/v1/chat/completions"
    )

    # 构建测试消息
    message = test_message or "你好，请用一句话简单介绍一下你自己。"
    messages = [
        {"role": "system", "content": "你是一个AI助手，请简洁回答。"},
        {"role": "user", "content": message},
    ]

    payload = {
        "model": config.model_name,
        "messages": messages,
        "max_tokens": 1024,
        "temperature": config.temperature,
    }

    # ---- 文心一言特殊处理：URL 拼接 access_token ----
    if config.provider == "wenxin":
        # 文心接口格式: https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{model}?access_token={key}
        # 如果用户配了自定义 endpoint 则直接用，否则按模型名拼接
        if not config.endpoint_url:
            endpoint = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{config.model_name}?access_token={api_key}"
        else:
            separator = "&" if "?" in endpoint else "?"
            endpoint = f"{endpoint}{separator}access_token={api_key}"
        headers = {"Content-Type": "application/json"}
    else:
        # OpenAI 兼容格式：Bearer token
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    # 如果文心自定义 endpoint 且未拼 token，payload 需要调整（文心用 stream:false）
    if config.provider == "wenxin" and config.endpoint_url:
        payload["stream"] = False

    # Ollama 原生 /api/chat 接口需要 stream: false
    if "/api/chat" in endpoint and "ollama" in endpoint.lower() or "/api/chat" in endpoint and config.provider == "local":
        payload["stream"] = False

    start_time = time.time()
    # 打印请求日志
    print("=" * 60)
    print("[模型测试] 请求发送")
    print(f"  Provider:  {config.provider}")
    print(f"  Model:     {config.model_name}")
    print(f"  Endpoint:  {endpoint}")
    print(f"  Key 来源:  {'手动输入' if api_key_override else '数据库解密'}")
    print(f"  Auth:      {'access_token (URL)' if config.provider == 'wenxin' else 'Bearer Token'}")
    print(f"  Payload:   model={payload.get('model')}, max_tokens={payload.get('max_tokens')}, temperature={payload.get('temperature')}")
    try:
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(endpoint, headers=headers, json=payload) as response:
                latency_ms = int((time.time() - start_time) * 1000)
                content_type = response.headers.get("Content-Type", "")

                # 打印响应状态日志
                print(f"[模型测试] 收到响应")
                print(f"  HTTP 状态: {response.status}")
                print(f"  Content-Type: {content_type}")
                print(f"  耗时: {latency_ms}ms")

                if response.status != 200:
                    error_text = await response.text()
                    print(f"[模型测试] 请求失败")
                    print(f"  响应内容: {error_text[:500]}")
                    try:
                        error_json = json.loads(error_text)
                        # 兼容多种错误格式
                        if isinstance(error_json.get("error"), dict):
                            error_msg = error_json["error"].get("message", error_text)
                        elif error_json.get("error_msg"):
                            error_msg = error_json["error_msg"]
                        elif error_json.get("message"):
                            error_msg = error_json["message"]
                        else:
                            error_msg = error_text[:300]
                    except (json.JSONDecodeError, AttributeError):
                        error_msg = error_text[:300]
                    return {
                        "success": False,
                        "message": f"API 返回 HTTP {response.status}: {error_msg}",
                        "reply": None,
                        "latency_ms": latency_ms,
                        "model_name": config.model_name,
                        "provider": config.provider,
                    }

                # 解析响应（绕过 content-type 校验，兼容 ndjson 等）
                response_text = await response.text()
                print(f"  响应长度: {len(response_text)} 字符")
                print(f"  响应原文: {response_text[:500]}")
                try:
                    data = json.loads(response_text)
                except json.JSONDecodeError:
                    # Ollama /api/chat 返回多行 ndjson，取最后一行（done: true）
                    lines = [l.strip() for l in response_text.strip().split("\n") if l.strip()]
                    print(f"  JSON 解析失败(非标准JSON)，尝试 ndjson，共 {len(lines)} 行")
                    data = json.loads(lines[-1]) if lines else {}

                # 统一解析回复（兼容 OpenAI / 文心 / Ollama 格式）
                reply = ""
                usage = {}
                if "choices" in data:
                    reply = data["choices"][0].get("message", {}).get("content", "")
                    usage = data.get("usage", {})
                elif "result" in data:
                    reply = data["result"]  # 文心格式
                elif "message" in data:
                    # Ollama /api/chat 原生格式: {"message": {"content": "..."}, "done": true}
                    reply = data["message"].get("content", "")
                    usage = {
                        "prompt_tokens": data.get("prompt_eval_count", 0),
                        "completion_tokens": data.get("eval_count", 0),
                        "total_tokens": data.get("prompt_eval_count", 0) + data.get("eval_count", 0),
                    }

                print(f"[模型测试] 解析完成")
                print(f"  回复长度: {len(reply)} 字符")
                print(f"  回复预览: {reply[:200] if reply else '(空)'}")
                print(f"  Token: prompt={usage.get('prompt_tokens', 0)}, completion={usage.get('completion_tokens', 0)}, total={usage.get('total_tokens', 0)}")
                print("=" * 60)

                return {
                    "success": True,
                    "message": "连接成功",
                    "reply": reply,
                    "latency_ms": latency_ms,
                    "model_name": config.model_name,
                    "provider": config.provider,
                    "usage": {
                        "prompt_tokens": usage.get("prompt_tokens", 0),
                        "completion_tokens": usage.get("completion_tokens", 0),
                        "total_tokens": usage.get("total_tokens", 0),
                    },
                }
    except asyncio.TimeoutError:
        latency_ms = int((time.time() - start_time) * 1000)
        print(f"[模型测试] 请求超时 {latency_ms}ms, endpoint={endpoint}")
        print("=" * 60)
        return {
            "success": False,
            "message": f"请求超时（{latency_ms}ms），请检查网络或 endpoint 是否正确",
            "reply": None,
            "latency_ms": latency_ms,
            "model_name": config.model_name,
            "provider": config.provider,
        }
    except aiohttp.ClientConnectorError as e:
        latency_ms = int((time.time() - start_time) * 1000)
        print(f"[模型测试] 连接失败: {e}, endpoint={endpoint}")
        print("=" * 60)
        return {
            "success": False,
            "message": f"网络连接失败: {str(e)[:200]}",
            "reply": None,
            "latency_ms": latency_ms,
            "model_name": config.model_name,
            "provider": config.provider,
        }
    except Exception as e:
        latency_ms = int((time.time() - start_time) * 1000)
        print(f"[模型测试] 未知异常: {e}, endpoint={endpoint}")
        import traceback
        traceback.print_exc()
        print("=" * 60)
        latency_ms = int((time.time() - start_time) * 1000)
        return {
            "success": False,
            "message": f"测试异常: {str(e)[:300]}",
            "reply": None,
            "latency_ms": latency_ms,
            "model_name": config.model_name,
            "provider": config.provider,
        }


async def get_prompt_configs(db: AsyncSession) -> list[AIPromptTemplate]:
    """
    获取提示词配置列表
    """
    stmt = select(AIPromptTemplate).order_by(AIPromptTemplate.type)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_prompt_config(
    db: AsyncSession, data: AIPromptConfigCreateRequest
) -> AIPromptTemplate:
    """
    创建提示词配置
    """
    config = AIPromptTemplate(
        name=data.name,
        type=data.type,
        template_text=data.template_text,
        variables=data.variables if data.variables is not None else [],
        system_prompt=data.system_prompt,
        is_default=data.is_default if data.is_default is not None else False,
        is_active=data.is_active if data.is_active is not None else True,
    )

    db.add(config)
    await db.flush()
    return config


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
    """
    stmt = select(AIRuleEngine).order_by(desc(AIRuleEngine.priority))
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_rule_engine(
    db: AsyncSession, data: AIRuleEngineCreateRequest
) -> AIRuleEngine:
    """
    创建规则引擎
    """
    engine = AIRuleEngine(
        name=data.name,
        description=data.description,
        rules=data.rules,
        priority=data.priority if data.priority is not None else 0,
        is_active=data.is_active if data.is_active is not None else True,
    )

    db.add(engine)
    await db.flush()
    return engine


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


# ============================================================
# 深度指令测试 & 规则引擎测试
# ============================================================


async def _call_model_api(
    config: AIModelConfig,
    messages: list[dict],
    api_key_override: str | None = None,
    temperature: float | None = None,
    max_tokens: int = 1024,
) -> dict:
    """
    通用模型调用（复用 test_model_config 的逻辑）
    返回 {success, reply, latency_ms, usage, error}
    """
    # 获取 API Key
    api_key = None
    if api_key_override:
        api_key = api_key_override
    elif config.api_key_encrypted:
        try:
            api_key = decrypt_api_key(config.api_key_encrypted)
        except Exception:
            pass

    if not api_key:
        return {"success": False, "reply": None, "latency_ms": 0, "usage": {}, "error": "无可用 API Key"}

    endpoint = config.endpoint_url or _PROVIDER_DEFAULT_ENDPOINTS.get(
        config.provider, "https://api.openai.com/v1/chat/completions"
    )

    payload = {
        "model": config.model_name,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature if temperature is not None else config.temperature,
    }

    # 文心特殊处理
    if config.provider == "wenxin":
        if not config.endpoint_url:
            endpoint = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{config.model_name}?access_token={api_key}"
        else:
            sep = "&" if "?" in endpoint else "?"
            endpoint = f"{endpoint}{sep}access_token={api_key}"
        headers = {"Content-Type": "application/json"}
        if config.endpoint_url:
            payload["stream"] = False
    else:
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    # Ollama stream: false
    if "/api/chat" in endpoint and config.provider == "local":
        payload["stream"] = False

    start_time = time.time()
    try:
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(endpoint, headers=headers, json=payload) as response:
                latency_ms = int((time.time() - start_time) * 1000)

                if response.status != 200:
                    error_text = await response.text()
                    return {"success": False, "reply": None, "latency_ms": latency_ms, "usage": {}, "error": f"HTTP {response.status}: {error_text[:300]}"}

                response_text = await response.text()
                try:
                    data = json.loads(response_text)
                except json.JSONDecodeError:
                    lines = [l.strip() for l in response_text.strip().split("\n") if l.strip()]
                    data = json.loads(lines[-1]) if lines else {}

                reply = ""
                usage = {}
                if "choices" in data:
                    reply = data["choices"][0].get("message", {}).get("content", "")
                    usage = data.get("usage", {})
                elif "result" in data:
                    reply = data["result"]
                elif "message" in data:
                    reply = data["message"].get("content", "")
                    usage = {
                        "prompt_tokens": data.get("prompt_eval_count", 0),
                        "completion_tokens": data.get("eval_count", 0),
                        "total_tokens": data.get("prompt_eval_count", 0) + data.get("eval_count", 0),
                    }

                print(f"[指令测试] 模型响应: {reply[:200]}")
                return {"success": True, "reply": reply, "latency_ms": latency_ms, "usage": usage, "error": None}

    except Exception as e:
        latency_ms = int((time.time() - start_time) * 1000)
        return {"success": False, "reply": None, "latency_ms": latency_ms, "usage": {}, "error": str(e)[:300]}


async def test_prompt(db: AsyncSession, params: dict) -> dict:
    """
    测试深度指令：用指定模型 + 指令模板 + 变量 渲染后调用模型

    Args:
        params: {
            model_id, prompt_id?, system_prompt?, user_message,
            variables?, api_key?, temperature?, max_tokens?
        }
    """
    model_id = params.get("model_id")
    prompt_id = params.get("prompt_id")
    user_message = params.get("user_message", "")
    variables = params.get("variables") or {}
    api_key = params.get("api_key")
    temperature = params.get("temperature")
    max_tokens = params.get("max_tokens", 1024)

    if not model_id or not user_message:
        return {"success": False, "error": "model_id 和 user_message 为必填项"}

    # 获取模型配置
    stmt = select(AIModelConfig).where(AIModelConfig.id == model_id)
    result = await db.execute(stmt)
    config = result.scalar_one_or_none()
    if not config:
        return {"success": False, "error": "模型配置不存在"}

    # 获取指令模板（可选）
    system_prompt = params.get("system_prompt", "")
    template_text = user_message  # 默认直接用 user_message

    if prompt_id:
        stmt2 = select(AIPromptTemplate).where(AIPromptTemplate.id == prompt_id)
        result2 = await db.execute(stmt2)
        template = result2.scalar_one_or_none()
        if template:
            # 如果有模板，用模板的 system_prompt（除非用户覆盖）
            if not system_prompt:
                system_prompt = template.system_prompt or ""
            # 用模板的 template_text 替换变量
            try:
                template_text = template.template_text.format(**variables)
            except KeyError as e:
                return {"success": False, "error": f"模板变量缺失: {e}"}

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": template_text})

    print(f"[指令测试] 调用模型: {config.provider}/{config.model_name}")
    print(f"[指令测试] system_prompt: {system_prompt[:100]}")
    print(f"[指令测试] user_message: {template_text[:200]}")

    api_result = await _call_model_api(config, messages, api_key, temperature, max_tokens)

    return {
        "success": api_result["success"],
        "reply": api_result["reply"],
        "latency_ms": api_result["latency_ms"],
        "usage": api_result["usage"],
        "error": api_result["error"],
        "model_name": config.model_name,
        "provider": config.provider,
        "rendered_prompt": template_text,
        "system_prompt_used": system_prompt,
    }


async def test_rule(db: AsyncSession, params: dict) -> dict:
    """
    测试规则引擎：输入内容 → 规则匹配 → 模板匹配 → 模型调用

    Args:
        params: {
            model_id, rule_id, prompt_id?, test_input,
            test_rating?, api_key?
        }
    """
    model_id = params.get("model_id")
    rule_id = params.get("rule_id")
    test_input = params.get("test_input", "")
    test_rating = params.get("test_rating")
    api_key = params.get("api_key")

    if not model_id or not rule_id or not test_input:
        return {"success": False, "error": "model_id、rule_id、test_input 为必填项"}

    # 获取模型
    stmt = select(AIModelConfig).where(AIModelConfig.id == model_id)
    result = await db.execute(stmt)
    config = result.scalar_one_or_none()
    if not config:
        return {"success": False, "error": "模型配置不存在"}

    # 获取规则
    stmt2 = select(AIRuleEngine).where(AIRuleEngine.id == rule_id)
    result2 = await db.execute(stmt2)
    rule = result2.scalar_one_or_none()
    if not rule:
        return {"success": False, "error": "规则配置不存在"}

    rules_data = rule.rules or {}

    # ========== 规则匹配阶段 ==========
    match_results = []

    # 1. 评分匹配
    if test_rating is not None:
        min_rating = rules_data.get("min_rating")
        if min_rating is not None:
            triggered = test_rating <= min_rating
            match_results.append({
                "rule_key": "min_rating",
                "rule_desc": f"最低评分阈值 {min_rating}",
                "input": test_rating,
                "expected": f"评分 <= {min_rating}",
                "triggered": triggered,
            })

    # 2. 关键词匹配
    trigger_keywords = rules_data.get("trigger_keywords", [])
    if trigger_keywords and isinstance(trigger_keywords, list):
        matched_keywords = [kw for kw in trigger_keywords if kw in test_input]
        match_results.append({
            "rule_key": "trigger_keywords",
            "rule_desc": f"触发关键词 ({len(trigger_keywords)}个)",
            "input": test_input[:100],
            "matched": matched_keywords,
            "triggered": len(matched_keywords) > 0,
        })

    # 3. 敏感词检测
    blocked_words = rules_data.get("blocked_words", [])
    if blocked_words and isinstance(blocked_words, list):
        found_blocked = [w for w in blocked_words if w in test_input]
        match_results.append({
            "rule_key": "blocked_words",
            "rule_desc": f"敏感词列表 ({len(blocked_words)}个)",
            "found": found_blocked,
            "triggered": len(found_blocked) > 0,
        })

    # 4. 回复长度检查
    max_length = rules_data.get("max_reply_length")
    if max_length:
        match_results.append({
            "rule_key": "max_reply_length",
            "rule_desc": f"最大回复长度 {max_length}",
            "triggered": False,  # 后续在模型回复后检查
        })

    # 5. 自动回复检查
    auto_enabled = rules_data.get("auto_reply_enabled")
    if auto_enabled is not None:
        match_results.append({
            "rule_key": "auto_reply_enabled",
            "rule_desc": "自动回复开关",
            "value": auto_enabled,
            "triggered": auto_enabled,
        })

    any_triggered = any(r.get("triggered") for r in match_results)

    # ========== 模板匹配阶段 ==========
    template_info = None
    prompt_id = params.get("prompt_id")

    if not prompt_id:
        # 根据评分自动选择模板类型
        if test_rating is not None:
            if test_rating >= 4:
                target_type = "good_review"
            elif test_rating <= 2:
                target_type = "bad_review"
            else:
                target_type = "neutral_review"
            stmt3 = select(AIPromptTemplate).where(
                AIPromptTemplate.type == target_type,
                AIPromptTemplate.is_active == True,
            ).order_by(AIPromptTemplate.is_default.desc())
            result3 = await db.execute(stmt3)
            template = result3.scalar_one_or_none()
            if template:
                prompt_id = str(template.id)
                template_info = {"id": prompt_id, "name": template.name, "type": template.type}

    if prompt_id and not template_info:
        stmt4 = select(AIPromptTemplate).where(AIPromptTemplate.id == prompt_id)
        result4 = await db.execute(stmt4)
        tmpl = result4.scalar_one_or_none()
        if tmpl:
            template_info = {"id": str(tmpl.id), "name": tmpl.name, "type": tmpl.type}

    # ========== 模型调用阶段 ==========
    messages = []
    system_prompt = "你是一个专业的客服回复助手，请根据规则和上下文生成合适的回复。"

    if template_info:
        if prompt_id:
            stmt5 = select(AIPromptTemplate).where(AIPromptTemplate.id == prompt_id)
            result5 = await db.execute(stmt5)
            tmpl = result5.scalar_one_or_none()
            if tmpl and tmpl.system_prompt:
                system_prompt = tmpl.system_prompt

    messages.append({"role": "system", "content": system_prompt})

    # 构建用户消息，包含规则上下文
    rule_context = f"规则引擎「{rule.name}」已匹配结果:\n"
    for mr in match_results:
        if mr.get("triggered"):
            rule_context += f"  - {mr.get('rule_desc', '')}: 已触发\n"
    rule_context += f"\n用户输入: {test_input}"
    if test_rating is not None:
        rule_context += f"\n用户评分: {test_rating}/5"

    messages.append({"role": "user", "content": rule_context})

    print(f"[规则测试] 规则: {rule.name}, 模型: {config.provider}/{config.model_name}")
    print(f"[规则测试] 匹配结果: {match_results}")

    api_result = await _call_model_api(config, messages, api_key)

    # 检查回复长度
    if max_length and api_result.get("reply"):
        reply_len = len(api_result["reply"])
        for mr in match_results:
            if mr.get("rule_key") == "max_reply_length":
                mr["triggered"] = reply_len > max_length
                mr["actual_length"] = reply_len

    # 检查敏感词是否出现在回复中
    if blocked_words and api_result.get("reply"):
        for mr in match_results:
            if mr.get("rule_key") == "blocked_words":
                reply_blocked = [w for w in blocked_words if w in api_result["reply"]]
                if reply_blocked:
                    mr["reply_found"] = reply_blocked
                    mr["triggered"] = True

    return {
        "success": api_result["success"],
        "reply": api_result["reply"],
        "latency_ms": api_result["latency_ms"],
        "usage": api_result["usage"],
        "error": api_result["error"],
        "model_name": config.model_name,
        "provider": config.provider,
        "rule_name": rule.name,
        "rule_matched": any_triggered,
        "match_results": match_results,
        "template_used": template_info,
        "system_prompt_used": system_prompt,
    }

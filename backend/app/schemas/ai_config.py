"""
AI配置模块Schema定义
用于AI后台配置相关接口的请求和响应模型
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AIModelConfigResponse(BaseModel):
    """AI模型配置响应模型"""

    id: UUID = Field(..., description="配置ID")
    provider: str = Field(..., description="提供商: openai/zhipu/wenxin/deepseek/local")
    model_name: str = Field(..., description="模型名称")
    endpoint_url: Optional[str] = Field(None, description="API端点URL")
    is_active: bool = Field(..., description="是否启用")
    priority: int = Field(..., description="优先级")
    max_tokens: int = Field(..., description="最大token数")
    temperature: float = Field(..., description="温度参数")
    config: Optional[dict] = Field(None, description="额外配置")


class AIModelConfigCreateRequest(BaseModel):
    """AI模型配置创建请求模型"""

    provider: str = Field(..., description="提供商")
    model_name: str = Field(..., description="模型名称")
    api_key: str = Field(..., description="API密钥")
    endpoint_url: Optional[str] = Field(None, description="API端点URL")
    is_active: Optional[bool] = Field(True, description="是否启用")
    priority: Optional[int] = Field(0, description="优先级")
    max_tokens: Optional[int] = Field(2048, description="最大token数")
    temperature: Optional[float] = Field(0.7, description="温度参数")


class AIPromptConfigResponse(BaseModel):
    """AI提示词配置响应模型"""

    id: UUID = Field(..., description="配置ID")
    name: str = Field(..., description="模板名称")
    type: str = Field(..., description="类型: good_review/bad_review/neutral_review/appeal/weekly_report")
    template_text: str = Field(..., description="模板文本")
    variables: Optional[list[str]] = Field(None, description="变量列表")
    system_prompt: Optional[str] = Field(None, description="系统提示词")
    is_default: bool = Field(..., description="是否为默认模板")
    is_active: bool = Field(..., description="是否启用")


class AIRuleEngineResponse(BaseModel):
    """AI规则引擎响应模型"""

    id: UUID = Field(..., description="引擎ID")
    name: str = Field(..., description="规则名称")
    description: Optional[str] = Field(None, description="规则描述")
    rules: Optional[dict] = Field(None, description="规则定义")
    priority: int = Field(..., description="优先级")
    is_active: bool = Field(..., description="是否启用")


class AIMonitoringResponse(BaseModel):
    """AI监控数据响应模型"""

    timestamp: datetime = Field(..., description="时间戳")
    total_requests: int = Field(..., description="总请求数")
    success_rate: float = Field(..., description="成功率")
    avg_latency: float = Field(..., description="平均延迟(ms)")
    active_models: int = Field(..., description="活跃模型数")


class AIEvaluationResponse(BaseModel):
    """AI效能评估响应模型"""

    period: str = Field(..., description="评估周期")
    total_evaluations: int = Field(..., description="总评估数")
    avg_score: float = Field(..., description="平均得分")
    improvement_areas: list[str] = Field(..., description="改进领域")

"""
阿里云短信服务模块（使用官方 Tea SDK V3 签名）
文档：https://help.aliyun.com/document_detail/2674224.html
"""
import asyncio
import logging
from typing import Optional

from alibabacloud_dysmsapi20170525.client import Client as DysmsapiClient
from alibabacloud_dysmsapi20170525 import models as dysms_models
from alibabacloud_tea_openapi import models as openapi_models

from app.core.config import settings
from app.core.exceptions import BusinessException

logger = logging.getLogger(__name__)


def _create_client() -> DysmsapiClient:
    """
    创建阿里云短信客户端（使用 V3 签名）
    """
    access_key_id = settings.ALIYUN_ACCESS_KEY_ID
    access_key_secret = settings.ALIYUN_ACCESS_KEY_SECRET

    if not access_key_id or not access_key_secret:
        raise BusinessException("阿里云短信配置缺失：请配置 ALIYUN_ACCESS_KEY_ID 和 ALIYUN_ACCESS_KEY_SECRET")

    config = openapi_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint='dysmsapi.aliyuncs.com',
        # V3 签名（默认）
        protocol='https',
    )
    return DysmsapiClient(config)


async def send_sms(
    phone: str,
    sign_name: str,
    template_code: str,
    template_param: dict,
    access_key_id: str | None = None,
    access_key_secret: str | None = None,
) -> dict:
    """
    发送短信（使用官方 Tea SDK）
    
    Args:
        phone: 手机号（支持逗号分隔的多个手机号）
        sign_name: 短信签名
        template_code: 短信模板CODE
        template_param: 模板参数字典，例如 {"code": "123456"}
        access_key_id: 访问密钥ID（可选，默认从配置读取）
        access_key_secret: 访问密钥Secret（可选，默认从配置读取）
    
    Returns:
        dict: 阿里云响应结果
        
    Raises:
        BusinessException: 发送失败时抛出
    """
    if access_key_id and access_key_secret:
        # 使用临时密钥
        config = openapi_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            endpoint='dysmsapi.aliyuncs.com',
            protocol='https',
        )
        client = DysmsapiClient(config)
    else:
        client = _create_client()

    if not sign_name:
        raise BusinessException("短信签名不能为空")

    if not template_code:
        raise BusinessException("短信模板CODE不能为空")

    # 构建请求
    import json
    request = dysms_models.SendSmsRequest(
        phone_numbers=phone,
        sign_name=sign_name,
        template_code=template_code,
        template_param=json.dumps(template_param, ensure_ascii=False),  # 必须是 JSON 字符串
    )

    try:
        logger.info(f"发送短信: phone={phone}, sign={sign_name}, template={template_code}, param={template_param}")
        # 使用 asyncio.to_thread 包装同步 SDK 调用，避免阻塞事件循环
        response = await asyncio.to_thread(client.send_sms, request)
        
        # Tea SDK 响应处理（简化版）
        # 方法1：使用 to_map() 转为字典
        if hasattr(response.body, 'to_map'):
            body_dict = response.body.to_map()
        else:
            body_dict = response.body if isinstance(response.body, dict) else {}
        
        # 提取字段（兼容大写和小写键名）
        code = body_dict.get('Code') or body_dict.get('code', '')
        message = body_dict.get('Message') or body_dict.get('message', '')
        biz_id = body_dict.get('BizId') or body_dict.get('biz_id', '')
        request_id = body_dict.get('RequestId') or body_dict.get('request_id', '')
        
        response_dict = {
            'Code': code,
            'Message': message,
            'BizId': biz_id,
            'RequestId': request_id,
        }

        logger.info(f"阿里云短信发送响应: {response_dict}")

        # 检查发送结果
        if response_dict.get('Code') != 'OK':
            error_msg = response_dict.get('Message', '未知错误')
            logger.error(f"短信发送失败: {error_msg}, RequestId={response_dict.get('RequestId')}")
            raise BusinessException(f"短信发送失败: {error_msg}")

        return response_dict

    except BusinessException:
        raise
    except Exception as e:
        logger.error(f"短信发送异常: {str(e)}")
        raise BusinessException(f"短信发送异常: {str(e)}")


async def send_verification_code(phone: str, code: str, purpose: str = "register") -> dict:
    """
    发送验证码短信（根据用途选择模板）
    
    Args:
        phone: 手机号
        code: 验证码
        purpose: 用途（register/login/reset_password）
    
    Returns:
        dict: 发送结果
    """
    sign_name = settings.ALIYUN_SMS_SIGN_NAME

    if not sign_name:
        raise BusinessException("未配置短信签名（ALIYUN_SMS_SIGN_NAME）")

    # 根据用途选择模板CODE
    template_code_map = {
        "register": settings.ALIYUN_SMS_TEMPLATE_CODE_REGISTER,
        "login": settings.ALIYUN_SMS_TEMPLATE_CODE_LOGIN,
        "reset_password": settings.ALIYUN_SMS_TEMPLATE_CODE_RESET,
    }

    template_code = template_code_map.get(purpose, settings.ALIYUN_SMS_TEMPLATE_CODE_REGISTER)

    if not template_code:
        raise BusinessException(f"未配置短信模板CODE：{purpose}")

    # 模板参数（根据阿里云短信模板的变量名调整）
    # 你的模板变量是 ${code}，所以 key 必须是 "code"
    template_param = {
        "code": code
    }

    logger.info(f"发送验证码短信: phone={phone}, purpose={purpose}, template={template_code}")

    return await send_sms(
        phone=phone,
        sign_name=sign_name,
        template_code=template_code,
        template_param=template_param,
    )


def test_sms_connection() -> bool:
    """
    测试阿里云短信配置是否正确
    
    Returns:
        bool: 配置是否有效
    """
    try:
        if not settings.ALIYUN_ACCESS_KEY_ID or not settings.ALIYUN_ACCESS_KEY_SECRET:
            return False
        client = _create_client()
        # 不实际发送，只验证客户端创建成功
        return client is not None
    except Exception as e:
        logger.error(f"阿里云短信配置测试失败: {str(e)}")
        return False

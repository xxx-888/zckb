"""初始化数据脚本 - 创建系统默认数据。

使用方法:
    cd backend
    python -m scripts.init_data

或者通过 Poetry:
    poetry run python -m scripts.init_data
"""

import asyncio
import uuid
from datetime import date, datetime, time
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.models import (
    SubscriptionPlan,
    AIModelConfig,
    AIPromptTemplate,
    SpiderPlatform,
    NotificationTemplate,
    Region,
)


async def init_subscription_plans(session: AsyncSession) -> None:
    """初始化订阅套餐数据。

n    创建三个默认套餐:
    - 标准版: 适合小型商户
    - 旗舰版: 适合连锁品牌
    - 企业版: 适合大型集团
    """
    # 检查是否已存在数据
    result = await session.execute(select(SubscriptionPlan).limit(1))
    if result.scalar_one_or_none():
        print("[SKIP] 订阅套餐数据已存在，跳过初始化")
        return

    plans = [
        SubscriptionPlan(
            id=uuid.uuid4(),
            name="标准版",
            price_monthly=99.0,
            price_yearly=999.0,
            max_stores=3,
            max_reviews_per_month=1000,
            features={
                "ai_reply": True,
                "basic_analytics": True,
                "weekly_report": True,
                "annual_report": False,
                "competitor_analysis": False,
                "api_access": False,
                "priority_support": False,
                "features": [
                    "AI智能回复",
                    "基础数据分析",
                    "周报推送",
                    "多平台同步",
                    "邮件通知",
                ],
            },
            is_active=True,
        ),
        SubscriptionPlan(
            id=uuid.uuid4(),
            name="旗舰版",
            price_monthly=299.0,
            price_yearly=2999.0,
            max_stores=10,
            max_reviews_per_month=5000,
            features={
                "ai_reply": True,
                "advanced_analytics": True,
                "weekly_report": True,
                "annual_report": True,
                "competitor_analysis": True,
                "api_access": False,
                "priority_support": True,
                "features": [
                    "AI智能回复",
                    "高级数据分析",
                    "周报/年报推送",
                    "竞品分析",
                    "多平台同步",
                    "邮件+短信通知",
                    "优先客服支持",
                ],
            },
            is_active=True,
        ),
        SubscriptionPlan(
            id=uuid.uuid4(),
            name="企业版",
            price_monthly=999.0,
            price_yearly=9999.0,
            max_stores=50,
            max_reviews_per_month=None,  # 无限制
            features={
                "ai_reply": True,
                "advanced_analytics": True,
                "weekly_report": True,
                "annual_report": True,
                "competitor_analysis": True,
                "api_access": True,
                "priority_support": True,
                "custom_integration": True,
                "dedicated_manager": True,
                "features": [
                    "AI智能回复",
                    "企业级数据分析",
                    "周报/年报推送",
                    "竞品分析",
                    "多平台同步",
                    "全渠道通知",
                    "API接口访问",
                    "定制化集成",
                    "专属客户经理",
                    "SLA保障",
                ],
            },
            is_active=True,
        ),
    ]

    for plan in plans:
        session.add(plan)

    await session.commit()
    print(f"[OK] 成功创建 {len(plans)} 个订阅套餐")


async def init_ai_model_configs(session: AsyncSession) -> None:
    """初始化AI模型配置。

n    创建默认AI模型配置:
    - OpenAI GPT-4
    - 智谱AI GLM-4
    - DeepSeek V3
    """
    result = await session.execute(select(AIModelConfig).limit(1))
    if result.scalar_one_or_none():
        print("[SKIP] AI模型配置已存在，跳过初始化")
        return

    configs = [
        AIModelConfig(
            id=uuid.uuid4(),
            provider="openai",
            model_name="gpt-4",
            api_key_encrypted=None,  # 需要手动配置
            endpoint_url="https://api.openai.com/v1",
            is_active=False,  # 默认不启用，需要配置API Key
            priority=3,
            max_tokens=2048,
            temperature=0.7,
            config={
                "description": "OpenAI GPT-4 模型",
                "supports_streaming": True,
                "context_window": 8192,
            },
        ),
        AIModelConfig(
            id=uuid.uuid4(),
            provider="zhipu",
            model_name="glm-4",
            api_key_encrypted=None,
            endpoint_url="https://open.bigmodel.cn/api/paas/v4",
            is_active=False,
            priority=2,
            max_tokens=2048,
            temperature=0.7,
            config={
                "description": "智谱AI GLM-4 模型",
                "supports_streaming": True,
                "context_window": 8192,
            },
        ),
        AIModelConfig(
            id=uuid.uuid4(),
            provider="deepseek",
            model_name="deepseek-chat",
            api_key_encrypted=None,
            endpoint_url="https://api.deepseek.com/v1",
            is_active=False,
            priority=1,
            max_tokens=4096,
            temperature=0.7,
            config={
                "description": "DeepSeek V3 模型",
                "supports_streaming": True,
                "context_window": 16384,
            },
        ),
    ]

    for config in configs:
        session.add(config)

    await session.commit()
    print(f"[OK] 成功创建 {len(configs)} 个AI模型配置")


async def init_ai_prompt_templates(session: AsyncSession) -> None:
    """初始化AI提示词模板。

n    创建默认提示词模板:
    - 好评回复模板
    - 中评回复模板
    - 差评回复模板
    - 申诉模板
    """
    result = await session.execute(select(AIPromptTemplate).limit(1))
    if result.scalar_one_or_none():
        print("[SKIP] AI提示词模板已存在，跳过初始化")
        return

    templates = [
        AIPromptTemplate(
            id=uuid.uuid4(),
            name="好评回复模板",
            type="good_review",
            template_text="""感谢您选择我们的门店！

看到您的好评，我们整个团队都非常开心！{specific_praise}

{store_name}会继续努力，为您提供更优质的服务和体验。期待您的再次光临！

祝您生活愉快！""",
            variables=["specific_praise", "store_name", "user_name"],
            system_prompt="你是一个专业的客户服务代表，擅长撰写真诚、温暖的回复。回复要简洁友好，体现对顾客的感谢。",
            is_default=True,
            is_active=True,
        ),
        AIPromptTemplate(
            id=uuid.uuid4(),
            name="中评回复模板",
            type="neutral_review",
            template_text="""尊敬的顾客，您好！

感谢您抽出宝贵时间为我们留下评价。对于您提到的{issue_description}，我们深表歉意。

{improvement_action}

您的意见对我们非常重要，我们会认真改进。期待您再次光临，给我们一个弥补的机会！

如有任何问题，欢迎随时联系我们：{contact_info}""",
            variables=["issue_description", "improvement_action", "contact_info", "store_name"],
            system_prompt="你是一个专业的客户服务代表，擅长处理中评反馈。回复要诚恳、专业，体现改进的决心。",
            is_default=True,
            is_active=True,
        ),
        AIPromptTemplate(
            id=uuid.uuid4(),
            name="差评回复模板",
            type="bad_review",
            template_text="""尊敬的{user_name}，您好！

首先，对于给您带来的不好体验，我们深表歉意。

关于您反馈的{complaint_detail}，我们已经第一时间进行了调查和处理：
{resolution_steps}

为了表达我们的歉意，我们希望能为您提供{compensation_offer}。

您的反馈是我们改进的动力，我们会持续优化服务。恳请您给我们一个改正的机会！

店长联系方式：{manager_contact}

再次致歉，期待您的回复！""",
            variables=["user_name", "complaint_detail", "resolution_steps", "compensation_offer", "manager_contact", "store_name"],
            system_prompt="你是一个专业的客户服务经理，擅长处理差评和投诉。回复要诚恳道歉，提出具体的解决方案，体现专业和负责的态度。",
            is_default=True,
            is_active=True,
        ),
        AIPromptTemplate(
            id=uuid.uuid4(),
            name="申诉模板",
            type="appeal",
            template_text="""申诉理由：

1. 该评价存在以下问题：{issue_type}
   - 具体说明：{issue_detail}

2. 相关证据：
{evidence_list}

3. 我方立场：
{our_position}

4. 诉求：
{appeal_request}

请平台核实处理，谢谢！""",
            variables=["issue_type", "issue_detail", "evidence_list", "our_position", "appeal_request", "store_name", "platform"],
            system_prompt="你是一个专业的平台申诉专员，擅长撰写有理有据的申诉材料。申诉要逻辑清晰，证据充分，语气专业但坚定。",
            is_default=True,
            is_active=True,
        ),
    ]

    for template in templates:
        session.add(template)

    await session.commit()
    print(f"[OK] 成功创建 {len(templates)} 个AI提示词模板")


async def init_spider_platforms(session: AsyncSession) -> None:
    """初始化爬虫平台配置。

n    创建默认爬虫平台:
    - 美团
    - 抖音
    - 淘宝
    - 京东
    """
    result = await session.execute(select(SpiderPlatform).limit(1))
    if result.scalar_one_or_none():
        print("[SKIP] 爬虫平台配置已存在，跳过初始化")
        return

    platforms = [
        SpiderPlatform(
            id=uuid.uuid4(),
            name="meituan",
            display_name="美团",
            status="active",
            reliability=0.95,
            error_log=None,
            config={
                "base_url": "https://www.meituan.com",
                "api_version": "v1",
                "rate_limit": 100,
                "retry_policy": {
                    "max_retries": 3,
                    "backoff_factor": 2,
                },
            },
            last_sync_at=None,
        ),
        SpiderPlatform(
            id=uuid.uuid4(),
            name="dianping",
            display_name="大众点评",
            status="active",
            reliability=0.95,
            error_log=None,
            config={
                "base_url": "https://www.dianping.com",
                "api_version": "v1",
                "rate_limit": 100,
                "retry_policy": {
                    "max_retries": 3,
                    "backoff_factor": 2,
                },
            },
            last_sync_at=None,
        ),
        SpiderPlatform(
            id=uuid.uuid4(),
            name="douyin",
            display_name="抖音",
            status="active",
            reliability=0.90,
            error_log=None,
            config={
                "base_url": "https://www.douyin.com",
                "api_version": "v1",
                "rate_limit": 80,
                "retry_policy": {
                    "max_retries": 3,
                    "backoff_factor": 2,
                },
            },
            last_sync_at=None,
        ),
        SpiderPlatform(
            id=uuid.uuid4(),
            name="taobao",
            display_name="淘宝",
            status="active",
            reliability=0.92,
            error_log=None,
            config={
                "base_url": "https://www.taobao.com",
                "api_version": "v1",
                "rate_limit": 120,
                "retry_policy": {
                    "max_retries": 3,
                    "backoff_factor": 2,
                },
            },
            last_sync_at=None,
        ),
        SpiderPlatform(
            id=uuid.uuid4(),
            name="jd",
            display_name="京东",
            status="active",
            reliability=0.92,
            error_log=None,
            config={
                "base_url": "https://www.jd.com",
                "api_version": "v1",
                "rate_limit": 120,
                "retry_policy": {
                    "max_retries": 3,
                    "backoff_factor": 2,
                },
            },
            last_sync_at=None,
        ),
    ]

    for platform in platforms:
        session.add(platform)

    await session.commit()
    print(f"[OK] 成功创建 {len(platforms)} 个爬虫平台配置")


async def init_notification_templates(session: AsyncSession) -> None:
    """初始化通知模板。

n    创建默认通知模板:
    - 新评论通知
    - 差评预警
    - 周报通知
    - 爬虫状态通知
    """
    result = await session.execute(select(NotificationTemplate).limit(1))
    if result.scalar_one_or_none():
        print("[SKIP] 通知模板已存在，跳过初始化")
        return

    templates = [
        NotificationTemplate(
            id=uuid.uuid4(),
            name="新评论通知",
            event_type="new_review",
            template_text="""【新评论提醒】

门店：{store_name}
平台：{platform}
评分：{rating}星
内容：{review_content}

请及时查看并回复。""",
            variables=["store_name", "platform", "rating", "review_content"],
            is_active=True,
        ),
        NotificationTemplate(
            id=uuid.uuid4(),
            name="差评预警",
            event_type="negative_alert",
            template_text="""【差评预警】

门店：{store_name}
平台：{platform}
评分：{rating}星
内容：{review_content}

该评论被判定为差评，请重点关注并及时处理！""",
            variables=["store_name", "platform", "rating", "review_content", "risk_level"],
            is_active=True,
        ),
        NotificationTemplate(
            id=uuid.uuid4(),
            name="周报通知",
            event_type="weekly_report",
            template_text="""【周报】{store_name} - 第{week_number}周

本周数据概览：
- 新增评论：{new_reviews_count}
- 平均评分：{avg_rating}
- 好评率：{positive_rate}%

详细报告请登录系统查看。""",
            variables=["store_name", "week_number", "new_reviews_count", "avg_rating", "positive_rate"],
            is_active=True,
        ),
        NotificationTemplate(
            id=uuid.uuid4(),
            name="爬虫状态通知",
            event_type="spider_status",
            template_text="""【爬虫状态更新】

平台：{platform}
状态：{status}
同步记录数：{records_synced}
耗时：{duration}ms

{error_message if error_message else ""}""",
            variables=["platform", "status", "records_synced", "duration", "error_message"],
            is_active=True,
        ),
    ]

    for template in templates:
        session.add(template)

    await session.commit()
    print(f"[OK] 成功创建 {len(templates)} 个通知模板")


async def init_regions(session: AsyncSession) -> None:
    """初始化区域层级数据（示例数据）。

n    创建部分省市区示例数据，完整数据需要通过数据导入。
    """
    result = await session.execute(select(Region).limit(1))
    if result.scalar_one_or_none():
        print("[SKIP] 区域数据已存在，跳过初始化")
        return

    # 创建部分示例区域数据
    # 北京市
    beijing = Region(
        id=uuid.uuid4(),
        name="北京市",
        parent_id=None,
        level="province",
        code="110000",
    )
    session.add(beijing)
    await session.flush()  # 获取生成的ID

    beijing_city = Region(
        id=uuid.uuid4(),
        name="北京市",
        parent_id=beijing.id,
        level="city",
        code="110100",
    )
    session.add(beijing_city)
    await session.flush()

    # 北京市辖区
    districts = [
        ("东城区", "110101"),
        ("西城区", "110102"),
        ("朝阳区", "110105"),
        ("海淀区", "110108"),
    ]
    for name, code in districts:
        session.add(Region(
            id=uuid.uuid4(),
            name=name,
            parent_id=beijing_city.id,
            level="district",
            code=code,
        ))

    # 上海市
    shanghai = Region(
        id=uuid.uuid4(),
        name="上海市",
        parent_id=None,
        level="province",
        code="310000",
    )
    session.add(shanghai)
    await session.flush()

    shanghai_city = Region(
        id=uuid.uuid4(),
        name="上海市",
        parent_id=shanghai.id,
        level="city",
        code="310100",
    )
    session.add(shanghai_city)
    await session.flush()

    # 上海市辖区
    sh_districts = [
        ("黄浦区", "310101"),
        ("徐汇区", "310104"),
        ("长宁区", "310105"),
        ("静安区", "310106"),
    ]
    for name, code in sh_districts:
        session.add(Region(
            id=uuid.uuid4(),
            name=name,
            parent_id=shanghai_city.id,
            level="district",
            code=code,
        ))

    # 广东省
    guangdong = Region(
        id=uuid.uuid4(),
        name="广东省",
        parent_id=None,
        level="province",
        code="440000",
    )
    session.add(guangdong)
    await session.flush()

    # 广东城市
    cities = [
        ("广州市", "440100"),
        ("深圳市", "440300"),
    ]
    for name, code in cities:
        session.add(Region(
            id=uuid.uuid4(),
            name=name,
            parent_id=guangdong.id,
            level="city",
            code=code,
        ))

    await session.commit()
    print("[OK] 成功创建示例区域数据（北京、上海、广东部分城市）")
    print("[INFO] 如需完整区域数据，请导入完整的行政区划数据")


async def main() -> None:
    """执行所有初始化操作。"""
    print("=" * 60)
    print("开始初始化系统数据")
    print("=" * 60)

    async with AsyncSessionLocal() as session:
        try:
            # 初始化订阅套餐
            await init_subscription_plans(session)

            # 初始化AI模型配置
            await init_ai_model_configs(session)

            # 初始化AI提示词模板
            await init_ai_prompt_templates(session)

            # 初始化爬虫平台配置
            await init_spider_platforms(session)

            # 初始化通知模板
            await init_notification_templates(session)

            # 初始化区域数据
            await init_regions(session)

            print("=" * 60)
            print("数据初始化完成！")
            print("=" * 60)

        except Exception as e:
            await session.rollback()
            print(f"[ERROR] 初始化失败: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(main())

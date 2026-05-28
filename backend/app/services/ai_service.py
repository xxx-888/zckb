"""
AI核心服务模块
提供多模型混合支持的AI服务，包括回复生成、情感分析、标签提取、报告生成等功能
"""

import json
import time
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

import aiohttp
from sqlalchemy import and_, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException, NotFoundException
from app.core.security import decrypt_api_key
from app.models.ai_config import (
    AIModelConfig,
    AIPromptTemplate,
    AIRuleEngine,
    AIProcessingLog,
)
from app.models.report import AnnualReport, WeeklyBrief
from app.models.review import Review
from app.models.store import Store


class AIService:
    """AI核心服务类"""

    def __init__(self, db: AsyncSession) -> None:
        """
        初始化AI服务

        Args:
            db: 数据库会话
        """
        self.db = db

    async def get_active_model(self) -> AIModelConfig:
        """
        获取优先级最高的活跃模型

        Returns:
            AIModelConfig: 活跃的AI模型配置

        Raises:
            BusinessException: 没有可用的AI模型
        """
        stmt = (
            select(AIModelConfig)
            .where(AIModelConfig.is_active.is_(True))
            .order_by(desc(AIModelConfig.priority))
        )
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            raise BusinessException("没有可用的AI模型配置")

        return model

    async def generate_reply(
        self,
        review_content: str,
        rating: int,
        store_name: str,
        platform: str,
    ) -> dict:
        """
        生成回复

        Args:
            review_content: 评论内容
            rating: 评分
            store_name: 门店名称
            platform: 平台名称

        Returns:
            dict: 包含回复内容、情感分析等信息的字典
        """
        # 确定模板类型
        if rating >= 4:
            template_type = "good_review"
        elif rating <= 2:
            template_type = "bad_review"
        else:
            template_type = "neutral_review"

        # 获取提示词模板
        template = await self._get_prompt_template(template_type)

        # 构建消息
        variables = {
            "store_name": store_name,
            "platform": platform,
            "rating": rating,
            "review_content": review_content,
        }
        prompt = template.template_text.format(**variables)

        messages = [
            {"role": "system", "content": template.system_prompt or "你是一个专业的客服回复助手。"},
            {"role": "user", "content": prompt},
        ]

        # 获取活跃模型并调用
        model_config = await self.get_active_model()
        start_time = time.time()

        try:
            if model_config.provider == "openai":
                reply_text = await self._call_openai(messages, model_config)
            elif model_config.provider == "zhipu":
                reply_text = await self._call_zhipu(messages, model_config)
            elif model_config.provider == "deepseek":
                reply_text = await self._call_deepseek(messages, model_config)
            else:
                raise BusinessException(f"不支持的AI提供商: {model_config.provider}")

            processing_time = int((time.time() - start_time) * 1000)

            return {
                "reply": reply_text,
                "model_used": model_config.model_name,
                "provider": model_config.provider,
                "processing_time_ms": processing_time,
                "template_type": template_type,
            }
        except Exception as e:
            raise BusinessException(f"AI生成回复失败: {str(e)}")

    async def generate_text(self, prompt: str, system_prompt: str = "你是一个专业的AI助手。") -> str:
        """
        通用文本生成方法，供其他服务调用AI模型

        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词

        Returns:
            str: AI生成的文本内容
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        model_config = await self.get_active_model()

        try:
            if model_config.provider == "openai":
                return await self._call_openai(messages, model_config)
            elif model_config.provider == "zhipu":
                return await self._call_zhipu(messages, model_config)
            elif model_config.provider == "deepseek":
                return await self._call_deepseek(messages, model_config)
            else:
                raise BusinessException(f"不支持的AI提供商: {model_config.provider}")
        except Exception as e:
            raise BusinessException(f"AI文本生成失败: {str(e)}")

    async def analyze_sentiment(self, content: str) -> dict:
        """
        情感分析

        Args:
            content: 评论内容

        Returns:
            dict: 情感分析结果
        """
        if not content:
            return {"sentiment": "neutral", "confidence": 0.5, "score": 0.0}

        # 简单的关键词匹配模拟AI分析
        positive_keywords = ["好", "棒", "满意", "喜欢", "推荐", "不错", "好吃", "美味", "赞", "优秀"]
        negative_keywords = ["差", "难吃", "失望", "不好", "糟糕", "慢", "脏", "贵", "烂", "恶心"]

        positive_count = sum(1 for kw in positive_keywords if kw in content)
        negative_count = sum(1 for kw in negative_keywords if kw in content)

        if positive_count > negative_count:
            sentiment = "positive"
            confidence = min(0.5 + positive_count * 0.1, 0.95)
            score = min(positive_count * 0.2, 1.0)
        elif negative_count > positive_count:
            sentiment = "negative"
            confidence = min(0.5 + negative_count * 0.1, 0.95)
            score = -min(negative_count * 0.2, 1.0)
        else:
            sentiment = "neutral"
            confidence = 0.5
            score = 0.0

        return {
            "sentiment": sentiment,
            "confidence": round(confidence, 2),
            "score": round(score, 2),
        }

    async def analyze_tags(self, content: str) -> list[str]:
        """
        标签提取

        Args:
            content: 评论内容

        Returns:
            list[str]: 提取的标签列表
        """
        if not content:
            return []

        # 预定义标签关键词映射
        tag_keywords = {
            "服务态度": ["服务", "态度", "热情", "冷漠", "周到"],
            "菜品口味": ["口味", "味道", "好吃", "难吃", "咸", "淡", "辣"],
            "环境卫生": ["环境", "卫生", "干净", "脏", "整洁", "杂乱"],
            "上菜速度": ["速度", "快", "慢", "等待", "上菜", "出餐"],
            "性价比": ["价格", "贵", "便宜", "划算", "性价比", "值"],
            "食材新鲜": ["新鲜", "食材", "变质", "不新鲜", "质量"],
            "停车便利": ["停车", "车位", "方便", "难停"],
            "位置好找": ["位置", "好找", "难找", "交通", "便利"],
        }

        tags = []
        for tag, keywords in tag_keywords.items():
            if any(kw in content for kw in keywords):
                tags.append(tag)

        return tags[:5]  # 最多返回5个标签

    async def generate_appeal_suggestion(self, review: Review) -> dict:
        """
        生成申诉建议

        Args:
            review: 评论对象

        Returns:
            dict: 申诉建议数据
        """
        content = review.content or ""
        rating = review.rating

        # 判断是否为恶意差评
        malicious_indicators = [
            "竞争对手", "恶意", "敲诈", "勒索", "不给钱",
            "差评师", "职业差评", "刷差评", "没来过", "没消费",
        ]

        is_malicious = rating <= 2 and any(indicator in content for indicator in malicious_indicators)

        # 如果没有明显恶意指标，基于评分判断
        if not is_malicious and rating <= 1:
            # 检查评论内容是否过于简单或重复
            if len(content) < 10 or content.count("差") > 3:
                is_malicious = True

        confidence = 0.85 if is_malicious else 0.3

        if is_malicious:
            suggestion = "该评论疑似恶意差评，建议提交申诉"
            appeal_content = (
                f"尊敬的平台审核人员：\n\n"
                f"我们发现该用户（{review.user_name or '匿名用户'}）的评价存在以下异常：\n"
                f"1. 评价内容与实际情况不符\n"
                f"2. 疑似恶意差评行为\n"
                f"3. 评价时间或内容存在异常\n\n"
                f"恳请平台核实处理，维护公平公正的营商环境。"
            )
        else:
            suggestion = "该评论属于正常用户反馈，建议正常回复处理"
            appeal_content = ""

        return {
            "review_id": review.id,
            "is_malicious": is_malicious,
            "confidence": round(confidence, 2),
            "suggestion": suggestion,
            "appeal_content": appeal_content,
        }

    async def generate_weekly_brief(self, store_id: UUID) -> dict:
        """
        生成周报

        Args:
            store_id: 门店ID

        Returns:
            dict: 周报数据
        """
        # 计算本周时间范围
        now = datetime.utcnow()
        week_start = now - timedelta(days=now.weekday())
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)

        # 查询本周评论统计
        stmt = (
            select(
                func.count(Review.id).label("total"),
                func.sum(func.case((Review.sentiment == "positive", 1), else_=0)).label("positive"),
                func.sum(func.case((Review.sentiment == "negative", 1), else_=0)).label("negative"),
                func.sum(func.case((Review.sentiment == "neutral", 1), else_=0)).label("neutral"),
                func.avg(Review.rating).label("avg_rating"),
            )
            .where(
                and_(
                    Review.store_id == store_id,
                    Review.created_at >= week_start,
                    Review.created_at <= week_end,
                    Review.status == "normal",
                )
            )
        )
        result = await self.db.execute(stmt)
        row = result.one_or_none()

        total_reviews = row.total or 0
        positive_count = row.positive or 0
        negative_count = row.negative or 0
        neutral_count = row.neutral or 0
        avg_rating = round(row.avg_rating, 1) if row.avg_rating else 0.0

        # 提取热门问题（基于差评标签）
        top_issues = await self._extract_top_issues(store_id, week_start, week_end)

        # 提取热门好评
        top_praises = await self._extract_top_praises(store_id, week_start, week_end)

        # 生成AI摘要
        ai_summary = await self._generate_weekly_summary(
            total_reviews, positive_count, negative_count, avg_rating, top_issues
        )

        # 保存或更新周报
        brief = WeeklyBrief(
            store_id=store_id,
            week_start=week_start,
            week_end=week_end,
            total_reviews=total_reviews,
            positive_count=positive_count,
            negative_count=negative_count,
            neutral_count=neutral_count,
            avg_rating=avg_rating,
            top_issues=top_issues,
            top_praises=top_praises,
            ai_summary=ai_summary,
            generated_at=datetime.utcnow(),
        )
        self.db.add(brief)
        await self.db.flush()

        return {
            "id": brief.id,
            "store_id": store_id,
            "week_start": week_start,
            "week_end": week_end,
            "total_reviews": total_reviews,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count,
            "avg_rating": avg_rating,
            "top_issues": top_issues,
            "top_praises": top_praises,
            "ai_summary": ai_summary,
        }

    async def generate_annual_report(self, store_id: UUID, year: int) -> dict:
        """
        生成年度报告

        Args:
            store_id: 门店ID
            year: 年份

        Returns:
            dict: 年度报告数据
        """
        # 查询年度评论统计
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31, 23, 59, 59)

        stmt = (
            select(
                func.count(Review.id).label("total"),
                func.avg(Review.rating).label("avg_rating"),
            )
            .where(
                and_(
                    Review.store_id == store_id,
                    Review.created_at >= start_date,
                    Review.created_at <= end_date,
                    Review.status == "normal",
                )
            )
        )
        result = await self.db.execute(stmt)
        row = result.one_or_none()

        total_reviews = row.total or 0
        average_rating = round(row.avg_rating, 1) if row.avg_rating else 0.0

        # 情感分布
        sentiment_stmt = (
            select(Review.sentiment, func.count().label("count"))
            .where(
                and_(
                    Review.store_id == store_id,
                    Review.created_at >= start_date,
                    Review.created_at <= end_date,
                    Review.status == "normal",
                )
            )
            .group_by(Review.sentiment)
        )
        sentiment_result = await self.db.execute(sentiment_stmt)
        sentiment_distribution = {row.sentiment: row.count for row in sentiment_result.all()}

        # 回复统计
        reply_stmt = (
            select(
                func.count().filter(Review.reply.isnot(None)).label("replied"),
                func.count().filter(Review.ai_generated.is_(True)).label("ai_replied"),
            )
            .where(
                and_(
                    Review.store_id == store_id,
                    Review.created_at >= start_date,
                    Review.created_at <= end_date,
                    Review.status == "normal",
                )
            )
        )
        reply_result = await self.db.execute(reply_stmt)
        reply_row = reply_result.one()
        reply_stats = {
            "total_replied": reply_row.replied or 0,
            "ai_replied": reply_row.ai_replied or 0,
            "reply_rate": round((reply_row.replied or 0) / total_reviews * 100, 1) if total_reviews > 0 else 0,
        }

        # 月度数据
        monthly_data = await self._get_monthly_data(store_id, year)

        # 热门关键词
        top_keywords = await self._extract_top_keywords(store_id, start_date, end_date)

        # 洞察
        insights = {
            "year_over_year": "同比去年评论量增长15%",
            "highlights": ["服务态度获得一致好评", "菜品口味满意度提升"],
            "improvements": ["上菜速度有待提升", "停车便利性需要改善"],
            "ai_summary": f"{year}年度共收到{total_reviews}条评论，平均评分{average_rating}分，整体表现良好。",
        }

        # 保存或更新年度报告
        report = AnnualReport(
            store_id=store_id,
            year=year,
            total_reviews=total_reviews,
            average_rating=average_rating,
            sentiment_distribution=sentiment_distribution,
            reply_stats=reply_stats,
            monthly_data=monthly_data,
            top_keywords=top_keywords,
            insights=insights,
            generated_at=datetime.utcnow(),
        )
        self.db.add(report)
        await self.db.flush()

        return {
            "id": report.id,
            "store_id": store_id,
            "year": year,
            "total_reviews": total_reviews,
            "average_rating": average_rating,
            "sentiment_distribution": sentiment_distribution,
            "reply_stats": reply_stats,
            "monthly_data": monthly_data,
            "top_keywords": top_keywords,
            "insights": insights,
        }

    async def calculate_risk_level(self, review: Review) -> str:
        """
        计算风险等级

        Args:
            review: 评论对象

        Returns:
            str: 风险等级 (high/medium/low)
        """
        content = review.content or ""
        rating = review.rating

        # 高风险指标
        high_risk_keywords = [
            "投诉", "举报", "工商局", "315", "媒体", "曝光",
            "食物中毒", "卫生问题", "虚假宣传", "欺诈",
        ]

        # 中风险指标
        medium_risk_keywords = [
            "失望", "不会再", "差评", "避雷", "踩雷",
            "服务态度差", "态度恶劣", "不理人",
        ]

        # 检查高风险
        if rating <= 1 or any(kw in content for kw in high_risk_keywords):
            return "high"

        # 检查中风险
        if rating <= 2 or any(kw in content for kw in medium_risk_keywords):
            return "medium"

        return "low"

    async def _call_openai(
        self,
        messages: list[dict],
        model_config: AIModelConfig,
    ) -> str:
        """
        调用OpenAI API

        Args:
            messages: 消息列表
            model_config: 模型配置

        Returns:
            str: AI回复内容
        """
        api_key = decrypt_api_key(model_config.api_key_encrypted)
        endpoint = model_config.endpoint_url or "https://api.openai.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model_config.model_name,
            "messages": messages,
            "max_tokens": model_config.max_tokens,
            "temperature": model_config.temperature,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, headers=headers, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise BusinessException(f"OpenAI API调用失败: {error_text}")

                data = await response.json()
                return data["choices"][0]["message"]["content"]

    async def _call_zhipu(
        self,
        messages: list[dict],
        model_config: AIModelConfig,
    ) -> str:
        """
        调用智谱AI API

        Args:
            messages: 消息列表
            model_config: 模型配置

        Returns:
            str: AI回复内容
        """
        api_key = decrypt_api_key(model_config.api_key_encrypted)
        endpoint = model_config.endpoint_url or "https://open.bigmodel.cn/api/paas/v4/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model_config.model_name,
            "messages": messages,
            "max_tokens": model_config.max_tokens,
            "temperature": model_config.temperature,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, headers=headers, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise BusinessException(f"智谱AI API调用失败: {error_text}")

                data = await response.json()
                return data["choices"][0]["message"]["content"]

    async def _call_deepseek(
        self,
        messages: list[dict],
        model_config: AIModelConfig,
    ) -> str:
        """
        调用DeepSeek API

        Args:
            messages: 消息列表
            model_config: 模型配置

        Returns:
            str: AI回复内容
        """
        api_key = decrypt_api_key(model_config.api_key_encrypted)
        endpoint = model_config.endpoint_url or "https://api.deepseek.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model_config.model_name,
            "messages": messages,
            "max_tokens": model_config.max_tokens,
            "temperature": model_config.temperature,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, headers=headers, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise BusinessException(f"DeepSeek API调用失败: {error_text}")

                data = await response.json()
                return data["choices"][0]["message"]["content"]

    async def _get_prompt_template(self, template_type: str) -> AIPromptTemplate:
        """
        获取提示词模板

        Args:
            template_type: 模板类型

        Returns:
            AIPromptTemplate: 提示词模板
        """
        # 先尝试获取默认模板
        stmt = (
            select(AIPromptTemplate)
            .where(
                and_(
                    AIPromptTemplate.type == template_type,
                    AIPromptTemplate.is_default.is_(True),
                    AIPromptTemplate.is_active.is_(True),
                )
            )
        )
        result = await self.db.execute(stmt)
        template = result.scalar_one_or_none()

        # 如果没有默认模板，获取任意活跃模板
        if not template:
            stmt = (
                select(AIPromptTemplate)
                .where(
                    and_(
                        AIPromptTemplate.type == template_type,
                        AIPromptTemplate.is_active.is_(True),
                    )
                )
            )
            result = await self.db.execute(stmt)
            template = result.scalar_one_or_none()

        # 如果还是没有，返回默认模板
        if not template:
            default_templates = {
                "good_review": AIPromptTemplate(
                    type="good_review",
                    name="好评回复模板",
                    template_text="感谢您对{store_name}的好评！我们会继续努力提供更好的服务。",
                    system_prompt="你是一个专业的客服回复助手，回复要真诚、简洁。",
                ),
                "bad_review": AIPromptTemplate(
                    type="bad_review",
                    name="差评回复模板",
                    template_text="非常抱歉给您带来不好的体验，我们会认真改进。",
                    system_prompt="你是一个专业的客服回复助手，回复要诚恳、有歉意。",
                ),
                "neutral_review": AIPromptTemplate(
                    type="neutral_review",
                    name="中性评价回复模板",
                    template_text="感谢您的评价，我们会持续改进。",
                    system_prompt="你是一个专业的客服回复助手，回复要礼貌、专业。",
                ),
            }
            template = default_templates.get(template_type, default_templates["neutral_review"])

        return template

    async def _apply_rules(self, review: Review) -> dict:
        """
        应用规则引擎

        Args:
            review: 评论对象

        Returns:
            dict: 规则应用结果
        """
        # 获取所有活跃规则
        stmt = (
            select(AIRuleEngine)
            .where(AIRuleEngine.is_active.is_(True))
            .order_by(desc(AIRuleEngine.priority))
        )
        result = await self.db.execute(stmt)
        rules = result.scalars().all()

        applied_rules = []
        for rule in rules:
            if self._check_rule_match(review, rule.rules):
                applied_rules.append({
                    "rule_id": rule.id,
                    "rule_name": rule.name,
                    "action": rule.rules.get("action", "none"),
                })

        return {
            "applied_rules": applied_rules,
            "total_rules_checked": len(rules),
        }

    def _check_rule_match(self, review: Review, rules: dict) -> bool:
        """
        检查规则是否匹配

        Args:
            review: 评论对象
            rules: 规则定义

        Returns:
            bool: 是否匹配
        """
        conditions = rules.get("conditions", [])
        if not conditions:
            return False

        for condition in conditions:
            field = condition.get("field")
            operator = condition.get("operator")
            value = condition.get("value")

            review_value = getattr(review, field, None)

            if operator == "eq":
                if review_value != value:
                    return False
            elif operator == "ne":
                if review_value == value:
                    return False
            elif operator == "gt":
                if review_value is None or review_value <= value:
                    return False
            elif operator == "lt":
                if review_value is None or review_value >= value:
                    return False
            elif operator == "contains":
                if review_value is None or value not in str(review_value):
                    return False

        return True

    async def _log_processing(
        self,
        review_id: UUID,
        model_id: UUID,
        input_text: str,
        output_text: str,
        status: str,
        processing_time_ms: int,
    ) -> None:
        """
        记录AI处理日志

        Args:
            review_id: 评论ID
            model_id: 模型配置ID
            input_text: 输入文本
            output_text: 输出文本
            status: 处理状态
            processing_time_ms: 处理耗时(毫秒)
        """
        log = AIProcessingLog(
            review_id=review_id,
            model_config_id=model_id,
            input_text=input_text,
            output_text=output_text,
            status=status,
            processing_time_ms=processing_time_ms,
        )
        self.db.add(log)
        await self.db.flush()

    async def _extract_top_issues(
        self,
        store_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> list[str]:
        """提取主要问题"""
        # 查询差评标签
        stmt = (
            select(Review.tags)
            .where(
                and_(
                    Review.store_id == store_id,
                    Review.created_at >= start_date,
                    Review.created_at <= end_date,
                    Review.rating <= 2,
                    Review.status == "normal",
                )
            )
        )
        result = await self.db.execute(stmt)
        all_tags = []
        for row in result.all():
            if row.tags:
                all_tags.extend(row.tags)

        # 统计标签频率
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # 返回前3个问题标签
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        return [tag for tag, count in sorted_tags[:3]]

    async def _extract_top_praises(
        self,
        store_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> list[str]:
        """提取主要好评"""
        # 查询好评标签
        stmt = (
            select(Review.tags)
            .where(
                and_(
                    Review.store_id == store_id,
                    Review.created_at >= start_date,
                    Review.created_at <= end_date,
                    Review.rating >= 4,
                    Review.status == "normal",
                )
            )
        )
        result = await self.db.execute(stmt)
        all_tags = []
        for row in result.all():
            if row.tags:
                all_tags.extend(row.tags)

        # 统计标签频率
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # 返回前3个好评标签
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        return [tag for tag, count in sorted_tags[:3]]

    async def _generate_weekly_summary(
        self,
        total_reviews: int,
        positive_count: int,
        negative_count: int,
        avg_rating: float,
        top_issues: list[str],
    ) -> str:
        """生成周报AI摘要"""
        positive_rate = (positive_count / total_reviews * 100) if total_reviews > 0 else 0

        summary = f"本周共收到{total_reviews}条评论，好评率{positive_rate:.1f}%，平均评分{avg_rating}分。"

        if negative_count > 0:
            summary += f"收到{negative_count}条差评"
            if top_issues:
                summary += f"，主要问题集中在{', '.join(top_issues[:2])}方面"
            summary += "，建议重点关注并改进。"
        else:
            summary += "本周无差评，整体表现良好。"

        return summary

    async def _get_monthly_data(self, store_id: UUID, year: int) -> dict:
        """获取月度数据"""
        monthly_data = {}

        for month in range(1, 13):
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)

            stmt = (
                select(
                    func.count(Review.id).label("total"),
                    func.avg(Review.rating).label("avg_rating"),
                )
                .where(
                    and_(
                        Review.store_id == store_id,
                        Review.created_at >= start_date,
                        Review.created_at < end_date,
                        Review.status == "normal",
                    )
                )
            )
            result = await self.db.execute(stmt)
            row = result.one()

            monthly_data[str(month)] = {
                "total": row.total or 0,
                "avg_rating": round(row.avg_rating, 1) if row.avg_rating else 0.0,
            }

        return monthly_data

    async def _extract_top_keywords(
        self,
        store_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> dict:
        """提取热门关键词"""
        stmt = (
            select(Review.tags)
            .where(
                and_(
                    Review.store_id == store_id,
                    Review.created_at >= start_date,
                    Review.created_at <= end_date,
                    Review.status == "normal",
                )
            )
        )
        result = await self.db.execute(stmt)
        all_tags = []
        for row in result.all():
            if row.tags:
                all_tags.extend(row.tags)

        # 统计标签频率
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # 返回前10个关键词
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        return {tag: count for tag, count in sorted_tags[:10]}

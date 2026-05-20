"""
自动回复服务模块
处理自动回复相关的业务逻辑，包括新评论处理、自动回复判断、审核队列管理等
"""

from datetime import datetime, time
from uuid import UUID

from sqlalchemy import and_, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException, NotFoundException
from app.models.review import ReplyAudit, Review
from app.models.settings import AutoReplyConfig
from app.models.store import Store, StorePlatform
from app.services.ai_service import AIService


class AutoReplyService:
    """自动回复服务类"""

    def __init__(self, db: AsyncSession, ai_service: AIService) -> None:
        """
        初始化自动回复服务

        Args:
            db: 数据库会话
            ai_service: AI服务实例
        """
        self.db = db
        self.ai_service = ai_service

    async def process_new_review(self, review_id: UUID) -> dict:
        """
        处理新评论

        Args:
            review_id: 评论ID

        Returns:
            dict: 处理结果
        """
        # 获取评论
        stmt = select(Review).where(Review.id == review_id)
        result = await self.db.execute(stmt)
        review = result.scalar_one_or_none()

        if not review:
            raise NotFoundException("评论不存在")

        # 获取门店自动回复配置
        stmt = select(AutoReplyConfig).where(AutoReplyConfig.store_id == review.store_id)
        result = await self.db.execute(stmt)
        config = result.scalar_one_or_none()

        if not config:
            return {
                "review_id": review_id,
                "processed": False,
                "reason": "未配置自动回复",
            }

        # 判断是否自动回复
        should_reply = await self.should_auto_reply(review, config)

        if not should_reply:
            return {
                "review_id": review_id,
                "processed": False,
                "reason": "不符合自动回复条件",
            }

        # 生成AI回复
        store_stmt = select(Store).where(Store.id == review.store_id)
        store_result = await self.db.execute(store_stmt)
        store = store_result.scalar_one_or_none()
        store_name = store.name if store else "本店"

        ai_result = await self.ai_service.generate_reply(
            review_content=review.content or "",
            rating=review.rating,
            store_name=store_name,
            platform=review.platform,
        )

        ai_reply = ai_result.get("reply", "")

        # 根据模式处理
        if config.mode == "smart":
            # 智能模式：直接发送
            review.ai_reply_draft = ai_reply
            review.ai_generated = True

            # 创建审核记录（已批准）
            audit = await self.create_reply_audit(review, ai_reply, "smart")
            audit.status = "approved"
            audit.reviewed_at = datetime.utcnow()

            # 发送回复
            sent = await self.send_reply(review, ai_reply)

            if sent:
                review.reply = ai_reply
                review.reply_time = datetime.utcnow()
                audit.status = "sent"

            await self.db.flush()

            return {
                "review_id": review_id,
                "processed": True,
                "mode": "smart",
                "reply": ai_reply,
                "sent": sent,
            }

        elif config.mode == "semi_auto":
            # 半自动模式：进入待审核
            review.ai_reply_draft = ai_reply
            review.ai_generated = True

            audit = await self.create_reply_audit(review, ai_reply, "semi_auto")

            await self.db.flush()

            return {
                "review_id": review_id,
                "processed": True,
                "mode": "semi_auto",
                "reply": ai_reply,
                "audit_id": audit.id,
                "status": "pending_audit",
            }

        else:
            # 手动模式：仅生成建议
            review.ai_reply_draft = ai_reply
            review.ai_generated = False

            await self.db.flush()

            return {
                "review_id": review_id,
                "processed": True,
                "mode": "manual",
                "reply": ai_reply,
                "status": "suggestion_only",
            }

    async def should_auto_reply(self, review: Review, config: AutoReplyConfig) -> bool:
        """
        判断是否自动回复

        Args:
            review: 评论对象
            config: 自动回复配置

        Returns:
            bool: 是否自动回复
        """
        # 检查是否启用自动回复
        if not config.auto_reply_enabled:
            return False

        # 检查是否已回复
        if review.reply:
            return False

        # 检查工作时间
        if config.work_hours_only:
            if not await self.is_work_hours(config):
                return False

        # 检查关键词匹配
        if config.keyword_reply_enabled and config.keywords:
            if not await self.check_keywords(review.content or "", config.keywords):
                return False

        # 检查评分（默认不自动回复1-2分差评，除非配置允许）
        if review.rating <= 2:
            # 检查是否有差评自动回复配置
            keyword_config = config.keywords or {}
            if not keyword_config.get("auto_reply_negative", False):
                return False

        return True

    async def is_work_hours(self, config: AutoReplyConfig) -> bool:
        """
        判断是否工作时间

        Args:
            config: 自动回复配置

        Returns:
            bool: 是否工作时间
        """
        if not config.work_start_time or not config.work_end_time:
            # 未配置工作时间，默认全天
            return True

        now = datetime.now().time()

        # 处理跨午夜的情况
        if config.work_start_time <= config.work_end_time:
            return config.work_start_time <= now <= config.work_end_time
        else:
            # 跨午夜，如 22:00 - 08:00
            return now >= config.work_start_time or now <= config.work_end_time

    async def check_keywords(self, review_content: str, keywords: dict) -> bool:
        """
        检查关键词匹配

        Args:
            review_content: 评论内容
            keywords: 关键词配置

        Returns:
            bool: 是否匹配
        """
        if not keywords:
            return True

        # 检查排除关键词（如果包含则跳过）
        exclude_keywords = keywords.get("exclude", [])
        for kw in exclude_keywords:
            if kw in review_content:
                return False

        # 检查必须包含关键词（如果配置）
        include_keywords = keywords.get("include", [])
        if include_keywords:
            for kw in include_keywords:
                if kw in review_content:
                    return True
            # 配置了必须包含关键词但都不匹配
            return False

        # 检查自动回复关键词
        auto_reply_keywords = keywords.get("auto_reply", [])
        if auto_reply_keywords:
            for kw in auto_reply_keywords:
                if kw in review_content:
                    return True
            # 配置了自动回复关键词但都不匹配
            return False

        return True

    async def create_reply_audit(
        self,
        review: Review,
        ai_reply: str,
        mode: str,
    ) -> ReplyAudit:
        """
        创建回复审核记录

        Args:
            review: 评论对象
            ai_reply: AI回复内容
            mode: 自动回复模式

        Returns:
            ReplyAudit: 审核记录
        """
        # 计算风险等级
        risk_level = await self.ai_service.calculate_risk_level(review)

        audit = ReplyAudit(
            review_id=review.id,
            store_id=review.store_id,
            ai_reply_content=ai_reply,
            status="pending",
            risk_level=risk_level,
        )
        self.db.add(audit)
        await self.db.flush()
        await self.db.refresh(audit)

        return audit

    async def send_reply(self, review: Review, reply_content: str) -> bool:
        """
        发送回复到平台

        Args:
            review: 评论对象
            reply_content: 回复内容

        Returns:
            bool: 是否发送成功
        """
        # 获取平台关联信息
        stmt = (
            select(StorePlatform)
            .where(
                and_(
                    StorePlatform.store_id == review.store_id,
                    StorePlatform.platform == review.platform,
                    StorePlatform.connected.is_(True),
                )
            )
        )
        result = await self.db.execute(stmt)
        platform_store = result.scalar_one_or_none()

        if not platform_store:
            # 未关联平台，仅本地保存
            return False

        # TODO: 调用平台API发送回复
        # 这里需要根据平台类型调用不同的API
        # - 美团：调用美团开放平台API
        # - 大众点评：调用点评API
        # - 抖音：调用抖音生活服务API

        # 模拟发送成功
        return True

    async def process_pending_audits(self) -> None:
        """
        处理待审核队列
        定时任务调用，处理超时未审核的自动回复
        """
        # 查询超时未审核的记录（超过24小时）
        timeout = datetime.utcnow() - func.interval("24 hours")

        stmt = (
            select(ReplyAudit)
            .where(
                and_(
                    ReplyAudit.status == "pending",
                    ReplyAudit.created_at < timeout,
                )
            )
        )
        result = await self.db.execute(stmt)
        pending_audits = result.scalars().all()

        for audit in pending_audits:
            # 获取评论
            stmt = select(Review).where(Review.id == audit.review_id)
            result = await self.db.execute(stmt)
            review = result.scalar_one_or_none()

            if not review:
                continue

            # 自动批准并发送
            audit.status = "approved"
            audit.reviewed_at = datetime.utcnow()

            # 发送回复
            sent = await self.send_reply(review, audit.ai_reply_content)

            if sent:
                review.reply = audit.ai_reply_content
                review.reply_time = datetime.utcnow()
                audit.status = "sent"

        await self.db.flush()

    async def approve_audit(self, audit_id: UUID, user_id: UUID) -> ReplyAudit:
        """
        审核通过

        Args:
            audit_id: 审核记录ID
            user_id: 审核人ID

        Returns:
            ReplyAudit: 审核记录
        """
        stmt = select(ReplyAudit).where(ReplyAudit.id == audit_id)
        result = await self.db.execute(stmt)
        audit = result.scalar_one_or_none()

        if not audit:
            raise NotFoundException("审核记录不存在")

        if audit.status != "pending":
            raise BusinessException("该审核记录已处理")

        # 获取评论
        stmt = select(Review).where(Review.id == audit.review_id)
        result = await self.db.execute(stmt)
        review = result.scalar_one_or_none()

        if not review:
            raise NotFoundException("评论不存在")

        # 更新审核记录
        audit.status = "approved"
        audit.auditor_id = user_id
        audit.reviewed_at = datetime.utcnow()

        # 发送回复
        sent = await self.send_reply(review, audit.ai_reply_content)

        if sent:
            review.reply = audit.ai_reply_content
            review.reply_time = datetime.utcnow()
            review.ai_generated = True
            audit.status = "sent"

        await self.db.flush()
        await self.db.refresh(audit)

        return audit

    async def reject_audit(
        self,
        audit_id: UUID,
        user_id: UUID,
        reject_reason: str,
    ) -> ReplyAudit:
        """
        拒绝审核

        Args:
            audit_id: 审核记录ID
            user_id: 审核人ID
            reject_reason: 拒绝原因

        Returns:
            ReplyAudit: 审核记录
        """
        stmt = select(ReplyAudit).where(ReplyAudit.id == audit_id)
        result = await self.db.execute(stmt)
        audit = result.scalar_one_or_none()

        if not audit:
            raise NotFoundException("审核记录不存在")

        if audit.status != "pending":
            raise BusinessException("该审核记录已处理")

        # 更新审核记录
        audit.status = "rejected"
        audit.auditor_id = user_id
        audit.reviewed_at = datetime.utcnow()
        audit.reject_reason = reject_reason

        # 清除评论的AI草稿
        stmt = select(Review).where(Review.id == audit.review_id)
        result = await self.db.execute(stmt)
        review = result.scalar_one_or_none()

        if review:
            review.ai_reply_draft = None

        await self.db.flush()
        await self.db.refresh(audit)

        return audit

    async def get_pending_audits(
        self,
        store_id: UUID | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[ReplyAudit], int]:
        """
        获取待审核列表

        Args:
            store_id: 门店ID（可选）
            page: 页码
            page_size: 每页大小

        Returns:
            tuple[list[ReplyAudit], int]: (审核列表, 总数)
        """
        conditions = [ReplyAudit.status == "pending"]

        if store_id:
            conditions.append(ReplyAudit.store_id == store_id)

        # 查询总数
        count_stmt = select(func.count()).select_from(ReplyAudit).where(and_(*conditions))
        total = (await self.db.execute(count_stmt)).scalar() or 0

        # 查询数据
        stmt = (
            select(ReplyAudit)
            .where(and_(*conditions))
            .order_by(desc(ReplyAudit.created_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self.db.execute(stmt)
        audits = list(result.scalars().all())

        return audits, total

    async def get_audit_stats(self, store_id: UUID | None = None) -> dict:
        """
        获取审核统计

        Args:
            store_id: 门店ID（可选）

        Returns:
            dict: 统计数据
        """
        conditions = []
        if store_id:
            conditions.append(ReplyAudit.store_id == store_id)

        # 各状态统计
        stmt = (
            select(ReplyAudit.status, func.count().label("count"))
            .where(and_(*conditions) if conditions else True)
            .group_by(ReplyAudit.status)
        )
        result = await self.db.execute(stmt)
        status_counts = {row.status: row.count for row in result.all()}

        # 风险等级统计
        risk_stmt = (
            select(ReplyAudit.risk_level, func.count().label("count"))
            .where(and_(*conditions) if conditions else True)
            .group_by(ReplyAudit.risk_level)
        )
        risk_result = await self.db.execute(risk_stmt)
        risk_counts = {row.risk_level or "unknown": row.count for row in risk_result.all()}

        return {
            "pending": status_counts.get("pending", 0),
            "approved": status_counts.get("approved", 0),
            "rejected": status_counts.get("rejected", 0),
            "sent": status_counts.get("sent", 0),
            "high_risk": risk_counts.get("high", 0),
            "medium_risk": risk_counts.get("medium", 0),
            "low_risk": risk_counts.get("low", 0),
        }

"""
平台关联服务模块
处理平台账号连接、店铺绑定、数据同步等业务逻辑
"""

import base64
import json
import logging
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import and_, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BusinessException, NotFoundException
from app.models.review import Review
from app.models.spider import SpiderTask
from app.models.store import Store, StorePlatform, PlatformAccount
from app.models.user import User, UserStore

logger = logging.getLogger(__name__)


class PlatformService:
    """平台关联服务类"""

    def __init__(self, db: AsyncSession) -> None:
        """
        初始化平台服务

        Args:
            db: 数据库会话
        """
        self.db = db

    async def connect_platform(
        self,
        user_id: UUID,
        platform: str,
        credentials: dict,
    ) -> dict:
        """
        连接平台账号

        Args:
            user_id: 用户ID
            platform: 平台名称
            credentials: 登录凭证

        Returns:
            dict: 连接结果
        """
        # 验证平台类型
        valid_platforms = ["meituan", "dianping", "douyin", "taobao", "jd"]
        if platform not in valid_platforms:
            raise BusinessException(f"不支持的平台类型: {platform}")

        # 加密存储账号凭证（不实际登录，只保存信息）
        encrypted_credentials = await self._encrypt_credentials(credentials)

        # 写入 platform_accounts 表
        stmt = select(PlatformAccount).where(
            PlatformAccount.user_id == user_id,
            PlatformAccount.platform == platform,
        )
        result = await self.db.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            existing.platform_username = credentials.get("username", "")
            existing.cookies_status = "pending"
            existing.last_sync_at = datetime.utcnow()
            existing.error_msg = None
            account = existing
        else:
            account = PlatformAccount(
                user_id=user_id,
                platform=platform,
                platform_username=credentials.get("username", ""),
                cookies_encrypted=encrypted_credentials,
                cookies_status="pending",
                last_sync_at=datetime.utcnow(),
            )
            self.db.add(account)

        await self.db.flush()
        await self.db.refresh(account)

        # 返回模拟店铺列表（用于前端展示并绑定门店）
        mock_stores = await self.get_platform_stores(platform, credentials)

        return {
            "success": True,
            "message": "平台账号已保存，待爬虫服务处理",
            "account_id": str(account.id),
            "platform": platform,
            "stores": mock_stores,
        }

    async def get_platform_stores(
        self,
        platform: str,
        credentials: dict,
    ) -> list[dict]:
        """
        获取平台店铺列表

        Args:
            platform: 平台名称
            credentials: 登录凭证

        Returns:
            list[dict]: 平台店铺列表
        """
        # TODO: 实际应调用平台API获取店铺列表
        # 这里返回模拟数据

        mock_stores = {
            "meituan": [
                {
                    "platform_store_id": "mt_123456",
                    "platform_store_name": "测试门店-美团",
                    "platform": "meituan",
                    "rating": 4.5,
                    "review_count": 1280,
                },
                {
                    "platform_store_id": "mt_789012",
                    "platform_store_name": "测试分店-美团",
                    "platform": "meituan",
                    "rating": 4.3,
                    "review_count": 856,
                },
            ],
            "dianping": [
                {
                    "platform_store_id": "dp_123456",
                    "platform_store_name": "测试门店-点评",
                    "platform": "dianping",
                    "rating": 4.6,
                    "review_count": 2100,
                },
            ],
            "douyin": [
                {
                    "platform_store_id": "dy_123456",
                    "platform_store_name": "测试门店-抖音",
                    "platform": "douyin",
                    "rating": 4.4,
                    "review_count": 567,
                },
            ],
            "taobao": [
                {
                    "platform_store_id": "tb_123456",
                    "platform_store_name": "测试店铺-淘宝",
                    "platform": "taobao",
                    "rating": 4.7,
                    "review_count": 3200,
                },
            ],
            "jd": [
                {
                    "platform_store_id": "jd_123456",
                    "platform_store_name": "测试店铺-京东",
                    "platform": "jd",
                    "rating": 4.5,
                    "review_count": 1890,
                },
            ],
        }

        return mock_stores.get(platform, [])

    async def bind_platform_store(
        self,
        store_id: UUID,
        platform: str,
        platform_store_id: str,
        platform_store_name: str,
        account_id: UUID | None = None,
    ) -> StorePlatform:
        """
        绑定平台店铺

        Args:
            store_id: 系统门店ID
            platform: 平台名称
            platform_store_id: 平台侧门店ID
            platform_store_name: 平台侧门店名称
            account_id: 平台账号ID（可选）

        Returns:
            StorePlatform: 平台店铺关联对象
        """
        # 检查门店是否存在
        stmt = select(Store).where(Store.id == store_id)
        result = await self.db.execute(stmt)
        store = result.scalar_one_or_none()

        if not store:
            raise NotFoundException("门店不存在")

        # 检查是否已绑定
        stmt = (
            select(StorePlatform)
            .where(
                and_(
                    StorePlatform.store_id == store_id,
                    StorePlatform.platform == platform,
                )
            )
        )
        result = await self.db.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            # 更新现有绑定
            existing.platform_store_id = platform_store_id
            existing.platform_store_name = platform_store_name
            existing.account_id = account_id
            existing.connected = True
            existing.last_sync_at = None
            existing.sync_status = "pending"
            await self.db.flush()
            await self.db.refresh(existing)
            return existing

        # 创建新绑定
        store_platform = StorePlatform(
            store_id=store_id,
            platform=platform,
            platform_store_id=platform_store_id,
            platform_store_name=platform_store_name,
            account_id=account_id,
            connected=True,
            sync_status="pending",
        )
        self.db.add(store_platform)

        # 更新门店平台计数
        store.platform_count += 1

        await self.db.flush()
        await self.db.refresh(store_platform)

        return store_platform

    async def unbind_platform_store(self, store_platform_id: UUID) -> None:
        """
        解绑平台店铺

        Args:
            store_platform_id: 平台店铺关联ID
        """
        stmt = select(StorePlatform).where(StorePlatform.id == store_platform_id)
        result = await self.db.execute(stmt)
        store_platform = result.scalar_one_or_none()

        if not store_platform:
            raise NotFoundException("平台店铺关联不存在")

        # 获取门店
        stmt = select(Store).where(Store.id == store_platform.store_id)
        result = await self.db.execute(stmt)
        store = result.scalar_one_or_none()

        # 删除关联
        await self.db.delete(store_platform)

        # 更新门店平台计数
        if store and store.platform_count > 0:
            store.platform_count -= 1

        await self.db.flush()

    async def sync_platform_data(
        self,
        store_id: UUID,
        platform: str,
        full_sync: bool = False,
    ) -> dict:
        """
        同步平台数据

        Args:
            store_id: 门店ID
            platform: 平台名称
            full_sync: 是否全量同步

        Returns:
            dict: 同步任务信息
        """
        # 检查平台关联
        stmt = (
            select(StorePlatform)
            .where(
                and_(
                    StorePlatform.store_id == store_id,
                    StorePlatform.platform == platform,
                    StorePlatform.connected.is_(True),
                )
            )
        )
        result = await self.db.execute(stmt)
        store_platform = result.scalar_one_or_none()

        if not store_platform:
            raise BusinessException("该门店未绑定此平台")

        # 创建同步任务
        task_type = "full" if full_sync else "incremental"
        task = SpiderTask(
            store_platform_id=store_platform.id,
            platform=platform,
            platform_store_id=store_platform.platform_store_id,
            task_type=task_type,
            status="pending",
        )
        self.db.add(task)
        await self.db.flush()
        await self.db.refresh(task)

        # 更新同步状态
        store_platform.sync_status = "syncing"
        store_platform.last_sync_at = datetime.utcnow()

        await self.db.flush()

        # TODO: 触发爬虫任务
        # 这里应该调用爬虫服务或消息队列

        return {
            "task_id": task.id,
            "status": "pending",
            "message": "同步任务已创建",
            "platform": platform,
            "store_id": store_id,
            "full_sync": full_sync,
        }

    async def trigger_spider_sync(
        self,
        store_platform_id: UUID,
        task_type: str = "incremental",
    ) -> dict:
        """
        触发爬虫同步

        Args:
            store_platform_id: 平台店铺关联ID
            task_type: 任务类型 (full/incremental)

        Returns:
            dict: 任务信息
        """
        stmt = select(StorePlatform).where(StorePlatform.id == store_platform_id)
        result = await self.db.execute(stmt)
        store_platform = result.scalar_one_or_none()

        if not store_platform:
            raise NotFoundException("平台店铺关联不存在")

        if not store_platform.connected:
            raise BusinessException("平台店铺未连接")

        # 创建爬虫任务
        task = SpiderTask(
            store_platform_id=store_platform_id,
            platform=store_platform.platform,
            platform_store_id=store_platform.platform_store_id,
            task_type=task_type,
            status="pending",
        )
        self.db.add(task)
        await self.db.flush()
        await self.db.refresh(task)

        # 更新同步状态
        store_platform.sync_status = "syncing"

        await self.db.flush()

        return {
            "task_id": task.id,
            "status": "pending",
            "message": "爬虫任务已触发",
            "task_type": task_type,
        }

    async def get_sync_status(self, store_platform_id: UUID) -> dict:
        """
        获取同步状态

        Args:
            store_platform_id: 平台店铺关联ID

        Returns:
            dict: 同步状态
        """
        stmt = select(StorePlatform).where(StorePlatform.id == store_platform_id)
        result = await self.db.execute(stmt)
        store_platform = result.scalar_one_or_none()

        if not store_platform:
            raise NotFoundException("平台店铺关联不存在")

        # 查询最近任务
        stmt = (
            select(SpiderTask)
            .where(SpiderTask.store_platform_id == store_platform_id)
            .order_by(desc(SpiderTask.created_at))
            .limit(1)
        )
        result = await self.db.execute(stmt)
        latest_task = result.scalar_one_or_none()

        # 计算下次同步时间
        next_sync_at = None
        if store_platform.last_sync_at:
            next_sync_at = store_platform.last_sync_at + timedelta(hours=1)

        return {
            "store_platform_id": store_platform_id,
            "status": store_platform.sync_status or "idle",
            "connected": store_platform.connected,
            "last_sync_at": store_platform.last_sync_at,
            "next_sync_at": next_sync_at,
            "latest_task": {
                "id": latest_task.id if latest_task else None,
                "status": latest_task.status if latest_task else None,
                "created_at": latest_task.created_at if latest_task else None,
            } if latest_task else None,
        }

    async def reply_on_platform(
        self,
        store_platform_id: UUID,
        review_id: UUID,
        content: str,
    ) -> bool:
        """
        在平台上回复评论

        Args:
            store_platform_id: 平台店铺关联ID
            review_id: 评论ID
            content: 回复内容

        Returns:
            bool: 是否发送成功
        """
        # 获取平台关联
        stmt = select(StorePlatform).where(StorePlatform.id == store_platform_id)
        result = await self.db.execute(stmt)
        store_platform = result.scalar_one_or_none()

        if not store_platform:
            raise NotFoundException("平台店铺关联不存在")

        if not store_platform.connected:
            raise BusinessException("平台店铺未连接")

        # 获取评论
        stmt = select(Review).where(Review.id == review_id)
        result = await self.db.execute(stmt)
        review = result.scalar_one_or_none()

        if not review:
            raise NotFoundException("评论不存在")

        # TODO: 调用平台API发送回复
        # 根据平台类型调用不同的API
        platform = store_platform.platform

        try:
            # 模拟API调用
            if platform == "meituan":
                # 调用美团开放平台API
                pass
            elif platform == "dianping":
                # 调用点评API
                pass
            elif platform == "douyin":
                # 调用抖音生活服务API
                pass
            elif platform == "taobao":
                # 调用淘宝开放平台API
                pass
            elif platform == "jd":
                # 调用京东开放平台API
                pass

            # 更新评论回复状态
            review.reply = content
            review.reply_time = datetime.utcnow()
            await self.db.flush()

            return True
        except Exception as e:
            raise BusinessException(f"平台回复失败: {str(e)}")

    async def get_connected_platforms(self, user: User) -> list[dict]:
        """
        获取用户已连接的平台账号列表

        Args:
            user: 当前用户

        Returns:
            list[dict]: 平台账号列表
        """
        stmt = (
            select(PlatformAccount)
            .where(PlatformAccount.user_id == user.id)
            .order_by(desc(PlatformAccount.created_at))
        )
        result = await self.db.execute(stmt)
        accounts = result.scalars().all()

        platforms = []
        for acc in accounts:
            platforms.append({
                "id": acc.id,
                "platform": acc.platform,
                "platform_username": acc.platform_username,
                "connected": acc.cookies_status == "valid",
                "cookies_status": acc.cookies_status,
                "last_sync_at": acc.last_sync_at,
                "error_msg": acc.error_msg,
            })

        return platforms

    async def update_account(
        self,
        account_id: UUID,
        username: str | None = None,
        password: str | None = None,
    ) -> PlatformAccount:
        """
        更新平台账号的用户名/密码

        Args:
            account_id: 平台账号ID
            username: 新用户名（可选）
            password: 新密码（可选，会加密存储）

        Returns:
            PlatformAccount: 更新后的账号对象
        """
        stmt = select(PlatformAccount).where(PlatformAccount.id == account_id)
        result = await self.db.execute(stmt)
        account = result.scalar_one_or_none()

        if not account:
            raise NotFoundException("平台账号不存在")

        if username is not None:
            account.platform_username = username

        if password is not None and password != "":
            # 复用 _encrypt_credentials 加密新密码
            encrypted = await self._encrypt_credentials({
                "username": account.platform_username,
                "password": password,
            })
            account.cookies_encrypted = encrypted
            account.cookies_status = "pending"
            account.error_msg = None

        await self.db.flush()
        await self.db.refresh(account)
        return account

    async def get_account_by_id(self, account_id: UUID) -> PlatformAccount | None:
        """
        根据ID获取平台账号

        Args:
            account_id: 平台账号ID

        Returns:
            PlatformAccount | None
        """
        stmt = select(PlatformAccount).where(PlatformAccount.id == account_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_platform_store_details(self, store_platform_id: UUID) -> dict:
        """
        获取平台店铺详情

        Args:
            store_platform_id: 平台店铺关联ID

        Returns:
            dict: 店铺详情
        """
        stmt = (
            select(
                StorePlatform,
                Store.name.label("store_name"),
            )
            .join(Store, StorePlatform.store_id == Store.id)
            .where(StorePlatform.id == store_platform_id)
        )
        result = await self.db.execute(stmt)
        row = result.one_or_none()

        if not row:
            raise NotFoundException("平台店铺关联不存在")

        store_platform, store_name = row

        # 统计平台评论数
        review_stmt = (
            select(func.count(Review.id))
            .where(
                and_(
                    Review.store_id == store_platform.store_id,
                    Review.platform == store_platform.platform,
                    Review.status == "normal",
                )
            )
        )
        review_result = await self.db.execute(review_stmt)
        review_count = review_result.scalar() or 0

        return {
            "id": store_platform.id,
            "store_id": store_platform.store_id,
            "store_name": store_name,
            "platform": store_platform.platform,
            "platform_store_id": store_platform.platform_store_id,
            "platform_store_name": store_platform.platform_store_name,
            "connected": store_platform.connected,
            "last_sync_at": store_platform.last_sync_at,
            "sync_status": store_platform.sync_status,
            "review_count": review_count,
        }

    async def _encrypt_credentials(self, credentials: dict) -> str:
        """
        加密凭证

        Args:
            credentials: 凭证字典

        Returns:
            str: 加密后的凭证字符串
        """
        # TODO: 使用更安全的加密方式，如AES加密
        # 这里使用简单的base64编码作为示例
        json_str = json.dumps(credentials)
        encrypted = base64.b64encode(json_str.encode()).decode()
        return encrypted

    async def _decrypt_credentials(self, encrypted: str) -> dict:
        """
        解密凭证

        Args:
            encrypted: 加密后的凭证字符串

        Returns:
            dict: 凭证字典
        """
        # TODO: 使用对应的解密方式
        json_str = base64.b64decode(encrypted.encode()).decode()
        return json.loads(json_str)

    async def validate_platform_connection(
        self,
        platform: str,
        credentials: dict,
    ) -> bool:
        """
        验证平台连接

        Args:
            platform: 平台名称
            credentials: 登录凭证

        Returns:
            bool: 是否验证成功
        """
        # TODO: 实际应调用平台API验证
        # 这里模拟验证
        return True

    async def refresh_platform_token(
        self,
        store_platform_id: UUID,
    ) -> dict:
        """
        刷新平台Token

        Args:
            store_platform_id: 平台店铺关联ID

        Returns:
            dict: 刷新结果
        """
        stmt = select(StorePlatform).where(StorePlatform.id == store_platform_id)
        result = await self.db.execute(stmt)
        store_platform = result.scalar_one_or_none()

        if not store_platform:
            raise NotFoundException("平台店铺关联不存在")

        # TODO: 调用平台API刷新Token
        # 这里模拟刷新成功

        return {
            "success": True,
            "message": "Token刷新成功",
            "platform": store_platform.platform,
        }

    async def get_platform_statistics(self, store_id: UUID | None = None) -> dict:
        """
        获取平台统计信息

        Args:
            store_id: 门店ID（可选）

        Returns:
            dict: 统计数据
        """
        conditions = [StorePlatform.connected.is_(True)]
        if store_id:
            conditions.append(StorePlatform.store_id == store_id)

        # 各平台数量统计
        stmt = (
            select(StorePlatform.platform, func.count().label("count"))
            .where(and_(*conditions))
            .group_by(StorePlatform.platform)
        )
        result = await self.db.execute(stmt)
        platform_counts = {row.platform: row.count for row in result.all()}

        # 总连接数
        total_stmt = select(func.count()).select_from(StorePlatform).where(and_(*conditions))
        total = (await self.db.execute(total_stmt)).scalar() or 0

        # 最近同步统计
        recent_stmt = (
            select(func.count())
            .select_from(StorePlatform)
            .where(
                and_(
                    *conditions,
                    StorePlatform.last_sync_at >= datetime.utcnow() - timedelta(days=1),
                )
            )
        )
        recent_sync = (await self.db.execute(recent_stmt)).scalar() or 0

        return {
            "total_connections": total,
            "platform_distribution": platform_counts,
            "recent_sync_24h": recent_sync,
        }

"""数据库模型包 - 导入所有模型以确保 Alembic 能正确发现。"""

from .base import Base, BaseModel, TimestampMixin, UUIDPrimaryKeyMixin
from .user import User, UserStore, Region
from .store import Store, StorePlatform
from .review import Review, ReplyAudit
from .ai_config import AIModelConfig, AIPromptTemplate, AIRuleEngine, AIProcessingLog
from .notification import (
    NotificationChannel,
    NotificationRule,
    NotificationHistory,
    NotificationTemplate,
)
from .subscription import SubscriptionPlan, UserSubscription
from .spider import SpiderPlatform, SpiderSyncLog, SpiderTask
from .report import AnnualReport, WeeklyBrief, Competitor, CompetitorAnalysisTask
from .settings import ReplyTemplate, AutoReplyConfig, UserNotificationSetting
from .verification_code import VerificationCode

__all__ = [
    # Base
    "Base",
    "BaseModel",
    "TimestampMixin",
    "UUIDPrimaryKeyMixin",
    # User
    "User",
    "UserStore",
    "Region",
    # Store
    "Store",
    "StorePlatform",
    # Review
    "Review",
    "ReplyAudit",
    # AI Config
    "AIModelConfig",
    "AIPromptTemplate",
    "AIRuleEngine",
    "AIProcessingLog",
    # Notification
    "NotificationChannel",
    "NotificationRule",
    "NotificationHistory",
    "NotificationTemplate",
    # Subscription
    "SubscriptionPlan",
    "UserSubscription",
    # Spider
    "SpiderPlatform",
    "SpiderSyncLog",
    "SpiderTask",
    # Report
    "AnnualReport",
    "WeeklyBrief",
    "Competitor",
    "CompetitorAnalysisTask",
    # Settings
    "ReplyTemplate",
    "AutoReplyConfig",
    "UserNotificationSetting",
    # Verification Code
    "VerificationCode",
]

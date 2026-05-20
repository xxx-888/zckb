""""""爬虫基类模块。"""
"""爬虫基类模块。"""

from __future__ import annotations

import"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(Sp"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(Sp"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(Spider"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None ="""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str,"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            """"爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            """"爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time":"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform:"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] |"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None ="""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in ="""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。""""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright()."""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            """"爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_m"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.play"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width":"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server":"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in ="""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。""""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies","""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding=""""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) ->"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            """"爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Apple"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537."""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self,"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials:"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", """"爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id:"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id:"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name:"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError(""""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved:"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = """"爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
            state: 等待状态
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
            state: 等待状态
            
        Returns:
            元素定位器
        """
        if not"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
            state: 等待状态
            
        Returns:
            元素定位器
        """
        if not self.page:
            raise SpiderError("Browser"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
            state: 等待状态
            
        Returns:
            元素定位器
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        timeout ="""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
            state: 等待状态
            
        Returns:
            元素定位器
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        timeout = timeout or settings.browser_timeout
        locator = self"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
            state: 等待状态
            
        Returns:
            元素定位器
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        timeout = timeout or settings.browser_timeout
        locator = self.page.locator(selector)
        await locator.wait_for(state=state, timeout=timeout)
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
            state: 等待状态
            
        Returns:
            元素定位器
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        timeout = timeout or settings.browser_timeout
        locator = self.page.locator(selector)
        await locator.wait_for(state=state, timeout=timeout)
        return locator
    
    async def"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
            state: 等待状态
            
        Returns:
            元素定位器
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        timeout = timeout or settings.browser_timeout
        locator = self.page.locator(selector)
        await locator.wait_for(state=state, timeout=timeout)
        return locator
    
    async def safe_click(self, selector: str, timeout:"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
            state: 等待状态
            
        Returns:
            元素定位器
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        timeout = timeout or settings.browser_timeout
        locator = self.page.locator(selector)
        await locator.wait_for(state=state, timeout=timeout)
        return locator
    
    async def safe_click(self, selector: str, timeout: int | None = None) -> None:
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
            state: 等待状态
            
        Returns:
            元素定位器
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        timeout = timeout or settings.browser_timeout
        locator = self.page.locator(selector)
        await locator.wait_for(state=state, timeout=timeout)
        return locator
    
    async def safe_click(self, selector: str, timeout: int | None = None) -> None:
        """安全点击元素。
        
        Args:
            selector: CSS"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
            state: 等待状态
            
        Returns:
            元素定位器
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        timeout = timeout or settings.browser_timeout
        locator = self.page.locator(selector)
        await locator.wait_for(state=state, timeout=timeout)
        return locator
    
    async def safe_click(self, selector: str, timeout: int | None = None) -> None:
        """安全点击元素。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
            state: 等待状态
            
        Returns:
            元素定位器
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        timeout = timeout or settings.browser_timeout
        locator = self.page.locator(selector)
        await locator.wait_for(state=state, timeout=timeout)
        return locator
    
    async def safe_click(self, selector: str, timeout: int | None = None) -> None:
        """安全点击元素。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
        """
        locator ="""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
            state: 等待状态
            
        Returns:
            元素定位器
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        timeout = timeout or settings.browser_timeout
        locator = self.page.locator(selector)
        await locator.wait_for(state=state, timeout=timeout)
        return locator
    
    async def safe_click(self, selector: str, timeout: int | None = None) -> None:
        """安全点击元素。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
        """
        locator = await self.wait_for_selector(selector, timeout)
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
            state: 等待状态
            
        Returns:
            元素定位器
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        timeout = timeout or settings.browser_timeout
        locator = self.page.locator(selector)
        await locator.wait_for(state=state, timeout=timeout)
        return locator
    
    async def safe_click(self, selector: str, timeout: int | None = None) -> None:
        """安全点击元素。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
        """
        locator = await self.wait_for_selector(selector, timeout)
        await locator.click()
    
    async def safe_fill(
        self,
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
            state: 等待状态
            
        Returns:
            元素定位器
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        timeout = timeout or settings.browser_timeout
        locator = self.page.locator(selector)
        await locator.wait_for(state=state, timeout=timeout)
        return locator
    
    async def safe_click(self, selector: str, timeout: int | None = None) -> None:
        """安全点击元素。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
        """
        locator = await self.wait_for_selector(selector, timeout)
        await locator.click()
    
    async def safe_fill(
        self,
        selector: str,
        value: str"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
            state: 等待状态
            
        Returns:
            元素定位器
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        timeout = timeout or settings.browser_timeout
        locator = self.page.locator(selector)
        await locator.wait_for(state=state, timeout=timeout)
        return locator
    
    async def safe_click(self, selector: str, timeout: int | None = None) -> None:
        """安全点击元素。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
        """
        locator = await self.wait_for_selector(selector, timeout)
        await locator.click()
    
    async def safe_fill(
        self,
        selector: str,
        value: str,
        timeout: int | None = None"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
            state: 等待状态
            
        Returns:
            元素定位器
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        timeout = timeout or settings.browser_timeout
        locator = self.page.locator(selector)
        await locator.wait_for(state=state, timeout=timeout)
        return locator
    
    async def safe_click(self, selector: str, timeout: int | None = None) -> None:
        """安全点击元素。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
        """
        locator = await self.wait_for_selector(selector, timeout)
        await locator.click()
    
    async def safe_fill(
        self,
        selector: str,
        value: str,
        timeout: int | None = None,
    ) -> None:
        """""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
            state: 等待状态
            
        Returns:
            元素定位器
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        timeout = timeout or settings.browser_timeout
        locator = self.page.locator(selector)
        await locator.wait_for(state=state, timeout=timeout)
        return locator
    
    async def safe_click(self, selector: str, timeout: int | None = None) -> None:
        """安全点击元素。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
        """
        locator = await self.wait_for_selector(selector, timeout)
        await locator.click()
    
    async def safe_fill(
        self,
        selector: str,
        value: str,
        timeout: int | None = None,
    ) -> None:
        """安全填充输入框。
        
"""爬虫基类模块。"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from playwright.async_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
    async_playwright,
)
from playwright_stealth import stealth_async
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class SpiderError(Exception):
    """爬虫基础异常。"""
    pass


class LoginError(SpiderError):
    """登录异常。"""
    pass


class FetchError(SpiderError):
    """数据获取异常。"""
    pass


class ReplyError(SpiderError):
    """回复发布异常。"""
    pass


class ReviewData:
    """评论数据模型。"""
    
    def __init__(
        self,
        platform_review_id: str,
        user_name: str | None = None,
        user_avatar: str | None = None,
        rating: int = 5,
        content: str | None = None,
        images: list[str] | None = None,
        platform_created_at: datetime | None = None,
        reply: str | None = None,
        reply_time: datetime | None = None,
        raw_data: dict | None = None,
    ):
        self.platform_review_id = platform_review_id
        self.user_name = user_name
        self.user_avatar = user_avatar
        self.rating = rating
        self.content = content
        self.images = images or []
        self.platform_created_at = platform_created_at
        self.reply = reply
        self.reply_time = reply_time
        self.raw_data = raw_data
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典。"""
        return {
            "platform_review_id": self.platform_review_id,
            "user_name": self.user_name,
            "user_avatar": self.user_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "platform_created_at": self.platform_created_at.isoformat() if self.platform_created_at else None,
            "reply": self.reply,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "raw_data": self.raw_data,
        }


class BaseSpider(ABC):
    """爬虫基类。
    
    所有平台爬虫的抽象基类，定义了通用的爬虫接口。
    """
    
    def __init__(self, platform: str, config: dict[str, Any] | None = None) -> None:
        """初始化爬虫。
        
        Args:
            platform: 平台名称
            config: 平台特定配置
        """
        self.platform = platform
        self.config = config or settings.get_platform_config(platform)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self._is_logged_in = False
        self._cookies_path = Path(f".cookies/{platform}_cookies.json")
        
        # 确保cookies目录存在
        self._cookies_path.parent.mkdir(parents=True, exist_ok=True)
    
    async def start(self) -> None:
        """启动爬虫，初始化浏览器。"""
        logger.info(f"Starting {self.platform} spider...")
        
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = {
            "headless": settings.browser_headless,
            "slow_mo": settings.browser_slow_mo,
        }
        
        if settings.browser_executable_path:
            browser_args["executable_path"] = settings.browser_executable_path
        
        self.browser = await self.playwright.chromium.launch(**browser_args)
        
        # 创建浏览器上下文
        context_args: dict[str, Any] = {
            "viewport": {
                "width": settings.browser_viewport_width,
                "height": settings.browser_viewport_height,
            },
            "user_agent": settings.browser_user_agent or self._get_default_user_agent(),
        }
        
        # 加载已有cookies
        if self._cookies_path.exists():
            cookies = json.loads(self._cookies_path.read_text(encoding="utf-8"))
            context_args["storage_state"] = {"cookies": cookies}
            logger.debug(f"Loaded cookies from {self._cookies_path}")
        
        # 代理配置
        if settings.proxy_enabled and settings.proxy_url:
            context_args["proxy"] = {"server": settings.proxy_url}
        
        self.context = await self.browser.new_context(**context_args)
        
        # 创建新页面
        self.page = await self.context.new_page()
        
        # 应用stealth模式
        await stealth_async(self.page)
        
        # 设置默认超时
        self.page.set_default_timeout(settings.browser_timeout)
        
        logger.info(f"{self.platform} spider started successfully")
    
    async def stop(self) -> None:
        """停止爬虫，关闭浏览器。"""
        logger.info(f"Stopping {self.platform} spider...")
        
        # 保存cookies
        if self.context and self._is_logged_in:
            await self._save_cookies()
        
        if self.context:
            await self.context.close()
        
        if self.browser:
            await self.browser.close()
        
        if self.playwright:
            await self.playwright.stop()
        
        self._is_logged_in = False
        logger.info(f"{self.platform} spider stopped")
    
    async def _save_cookies(self) -> None:
        """保存cookies到文件。"""
        if not self.context:
            return
        
        try:
            storage_state = await self.context.storage_state()
            cookies = storage_state.get("cookies", [])
            self._cookies_path.write_text(
                json.dumps(cookies, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Cookies saved to {self._cookies_path}")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
    
    def _get_default_user_agent(self) -> str:
        """获取默认User-Agent。"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    
    @abstractmethod
    async def login(self, credentials: dict[str, Any]) -> bool:
        """登录平台。
        
        Args:
            credentials: 登录凭证，如 {"username": "...", "password": "..."}
            
        Returns:
            是否登录成功
        """
        pass
    
    @abstractmethod
    async def check_login_status(self) -> bool:
        """检查登录状态。
        
        Returns:
            是否已登录
        """
        pass
    
    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str | UUID,
        **kwargs: Any,
    ) -> list[ReviewData]:
        """获取评论列表。
        
        Args:
            store_id: 门店ID
            **kwargs: 其他参数，如分页、时间范围等
            
        Returns:
            评论数据列表
        """
        pass
    
    @abstractmethod
    async def post_reply(
        self,
        review_id: str,
        content: str,
    ) -> bool:
        """发布回复。
        
        Args:
            review_id: 评论ID
            content: 回复内容
            
        Returns:
            是否发布成功
        """
        pass
    
    async def take_screenshot(self, name: str | None = None) -> str:
        """截取屏幕截图。
        
        Args:
            name: 截图文件名
            
        Returns:
            截图文件路径
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.platform}_{name or 'screenshot'}_{timestamp}.png"
        filepath = screenshot_dir / filename
        
        await self.page.screenshot(path=str(filepath), full_page=True)
        logger.debug(f"Screenshot saved: {filepath}")
        
        return str(filepath)
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: int | None = None,
        state: str = "visible",
    ) -> Locator:
        """等待元素出现。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
            state: 等待状态
            
        Returns:
            元素定位器
        """
        if not self.page:
            raise SpiderError("Browser not started")
        
        timeout = timeout or settings.browser_timeout
        locator = self.page.locator(selector)
        await locator.wait_for(state=state, timeout=timeout)
        return locator
    
    async def safe_click(self, selector: str, timeout: int | None = None) -> None:
        """安全点击元素。
        
        Args:
            selector: CSS选择器
            timeout: 超时时间（毫秒）
        """
        locator = await self.wait_for_selector(selector, timeout)
        await locator.click()
    
    async def safe_fill(
        self,
        selector: str,
        value: str,
        timeout: int | None = None,
    ) -> None:
        """安全填充输入框。
        
        Args:
            selector: CSS选择器
            value: 填充值
            timeout
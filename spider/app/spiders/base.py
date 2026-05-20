"""
Base spider class for all platform spiders.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from playwright.async_api import Browser, BrowserContext, Page, async_playwright

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("spiders.base")


@dataclass
class Review:
    """Review data model."""

    review_id: str
    platform: str
    store_id: str
    author_name: str
    author_avatar: Optional[str] = None
    rating: int = 5  # 1-5
    content: str = ""
    images: list[str] = field(default_factory=list)
    reply_content: Optional[str] = None
    reply_time: Optional[datetime] = None
    review_time: Optional[datetime] = None
    order_info: Optional[str] = None  # Order details if available
    tags: list[str] = field(default_factory=list)
    helpful_count: int = 0
    is_anonymous: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, Any]:
        """Convert review to dictionary."""
        return {
            "review_id": self.review_id,
            "platform": self.platform,
            "store_id": self.store_id,
            "author_name": self.author_name,
            "author_avatar": self.author_avatar,
            "rating": self.rating,
            "content": self.content,
            "images": self.images,
            "reply_content": self.reply_content,
            "reply_time": self.reply_time.isoformat() if self.reply_time else None,
            "review_time": self.review_time.isoformat() if self.review_time else None,
            "order_info": self.order_info,
            "tags": self.tags,
            "helpful_count": self.helpful_count,
            "is_anonymous": self.is_anonymous,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class StoreInfo:
    """Store information data model."""

    store_id: str
    platform: str
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    rating: Optional[float] = None
    review_count: int = 0
    monthly_sales: Optional[int] = None
    business_hours: Optional[str] = None
    categories: list[str] = field(default_factory=list)
    logo: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: str = "active"  # active, closed, etc.

    def to_dict(self) -> dict[str, Any]:
        """Convert store info to dictionary."""
        return {
            "store_id": self.store_id,
            "platform": self.platform,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "rating": self.rating,
            "review_count": self.review_count,
            "monthly_sales": self.monthly_sales,
            "business_hours": self.business_hours,
            "categories": self.categories,
            "logo": self.logo,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "status": self.status,
        }


@dataclass
class Credentials:
    """Platform credentials."""

    username: str
    password: str
    cookies: Optional[dict[str, str]] = None
    token: Optional[str] = None
    extra_data: dict[str, Any] = field(default_factory=dict)


class BaseSpider(ABC):
    """Abstract base class for all platform spiders."""

    def __init__(self, platform_name: str, credentials: Credentials) -> None:
        """
        Initialize the spider.

        Args:
            platform_name: Name of the platform (e.g., 'meituan', 'douyin')
            credentials: Login credentials for the platform
        """
        self.platform_name = platform_name
        self.credentials = credentials
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.playwright = None
        self.is_logged_in = False

    async def _init_browser(self) -> None:
        """Initialize Playwright browser."""
        logger.info(f"Initializing browser for {self.platform_name}")
        self.playwright = await async_playwright().start()

        browser_type = getattr(self.playwright, settings.playwright_browser_type)
        self.browser = await browser_type.launch(
            headless=settings.playwright_headless,
            slow_mo=settings.playwright_slow_mo,
        )

        self.context = await self.browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        )

        # Load cookies if available
        if self.credentials.cookies:
            await self.context.add_cookies(
                [
                    {"name": k, "value": v, "domain": self._get_cookie_domain(), "path": "/"}
                    for k, v in self.credentials.cookies.items()
                ]
            )

        self.page = await self.context.new_page()
        logger.info(f"Browser initialized for {self.platform_name}")

    def _get_cookie_domain(self) -> str:
        """Get cookie domain for the platform. Override in subclass."""
        return ".example.com"

    @abstractmethod
    async def login(self) -> bool:
        """
        Login to the platform.

        Returns:
            True if login successful, False otherwise
        """
        pass

    @abstractmethod
    async def fetch_reviews(
        self,
        store_id: str,
        page: int = 1,
        limit: int = 20,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> list[Review]:
        """
        Fetch reviews for a store.

        Args:
            store_id: Store identifier
            page: Page number (1-based)
            limit: Number of reviews per page
            start_date: Filter reviews from this date
            end_date: Filter reviews until this date

        Returns:
            List of Review objects
        """
        pass

    @abstractmethod
    async def fetch_store_info(self, store_id: str) -> Optional[StoreInfo]:
        """
        Fetch store information.

        Args:
            store_id: Store identifier

        Returns:
            StoreInfo object or None if not found
        """
        pass

    @abstractmethod
    async def reply_review(self, review_id: str, content: str) -> bool:
        """
        Reply to a review.

        Args:
            review_id: Review identifier
            content: Reply content

        Returns:
            True if reply successful, False otherwise
        """
        pass

    async def check_new_reviews(
        self, store_id: str, last_check_time: datetime
    ) -> list[Review]:
        """
        Check for new reviews since last check.

        Args:
            store_id: Store identifier
            last_check_time: Last check timestamp

        Returns:
            List of new Review objects
        """
        reviews = await self.fetch_reviews(store_id, page=1, limit=50)
        return [r for r in reviews if r.review_time and r.review_time > last_check_time]

    async def save_cookies(self) -> dict[str, str]:
        """Save current cookies for reuse."""
        if not self.context:
            return {}
        cookies = await self.context.cookies()
        return {c["name"]: c["value"] for c in cookies if c.get("domain") == self._get_cookie_domain()}

    async def take_screenshot(self, path: str) -> None:
        """Take a screenshot of the current page."""
        if self.page:
            await self.page.screenshot(path=path, full_page=True)
            logger.info(f"Screenshot saved to {path}")

    async def close(self) -> None:
        """Close browser and cleanup resources."""
        logger.info(f"Closing browser for {self.platform_name}")
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        self.is_logged_in = False
        logger.info(f"Browser closed for {self.platform_name}")

    async def __aenter__(self) -> "BaseSpider":
        """Async context manager entry."""
        await self._init_browser()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()

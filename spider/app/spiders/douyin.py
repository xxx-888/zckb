"""
Douyin (抖音来客) spider implementation.
"""
from datetime import datetime
from typing import Any, Optional

from playwright.async_api import TimeoutError as PlaywrightTimeout

from app.core.logger import get_logger
from app.spiders.base import BaseSpider, Credentials, Review, StoreInfo

logger = get_logger("spiders.douyin")


class DouyinSpider(BaseSpider):
    """Spider for Douyin platform (抖音来客)."""

    BASE_URL = "https://life.douyin.com"
    LOGIN_URL = "https://life.douyin.com/login"
    REVIEW_URL_TEMPLATE = "https://life.douyin.com/comment/list"

    def __init__(self, credentials: Credentials) -> None:
        """Initialize Douyin spider."""
        super().__init__("douyin", credentials)

    def _get_cookie_domain(self) -> str:
        """Get cookie domain for Douyin."""
        return ".douyin.com"

    async def login(self) -> bool:
        """
        Login to Douyin merchant platform.

        Returns:
            True if login successful
        """
        logger.info("Attempting to login to Douyin")

        try:
            await self.page.goto(self.LOGIN_URL, wait_until="networkidle")
            await self.page.wait_for_load_state("domcontentloaded")

            # Check if already logged in
            if await self._is_logged_in():
                logger.info("Already logged in to Douyin")
                self.is_logged_in = True
                return True

            # Douyin typically uses QR code or SMS login
            # Try to handle different login methods
            try:
                # Try phone number login
                phone_input = await self.page.wait_for_selector(
                    "input[placeholder*='手机号'], input[type='tel']",
                    timeout=5000,
                )
                if phone_input:
                    await phone_input.fill(self.credentials.username)

                    # Get SMS code button
                    code_btn = await self.page.wait_for_selector(
                        "button:has-text('获取验证码'), .get-code-btn",
                        timeout=3000,
                    )
                    if code_btn:
                        await code_btn.click()
                        logger.info("SMS code requested, waiting for manual input...")
                        # In production, this should be handled differently
                        # Wait for manual SMS code entry
                        await self.page.wait_for_timeout(30000)

                else:
                    # Handle QR code login
                    logger.info("QR code login detected, please scan with Douyin app")
                    await self.page.wait_for_timeout(60000)  # Wait for QR scan

            except PlaywrightTimeout:
                logger.warning("Standard login form not found")

            # Verify login
            if await self._is_logged_in():
                self.is_logged_in = True
                self.credentials.cookies = await self.save_cookies()
                logger.info("Successfully logged in to Douyin")
                return True

            logger.error("Failed to login to Douyin")
            return False

        except Exception as e:
            logger.error(f"Error during Douyin login: {e}")
            return False

    async def _is_logged_in(self) -> bool:
        """Check if currently logged in."""
        try:
            indicator = await self.page.wait_for_selector(
                ".merchant-name, .user-avatar, .dashboard-header",
                timeout=3000,
            )
            return indicator is not None
        except PlaywrightTimeout:
            return False

    async def fetch_reviews(
        self,
        store_id: str,
        page: int = 1,
        limit: int = 20,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> list[Review]:
        """
        Fetch reviews from Douyin.

        Args:
            store_id: Douyin store ID
            page: Page number
            limit: Reviews per page
            start_date: Filter start date
            end_date: Filter end date

        Returns:
            List of Review objects
        """
        logger.info(f"Fetching reviews for store {store_id}, page {page}")

        if not self.is_logged_in:
            if not await self.login():
                return []

        reviews: list[Review] = []

        try:
            # Navigate to review page
            await self.page.goto(
                f"{self.REVIEW_URL_TEMPLATE}?shopId={store_id}",
                wait_until="networkidle",
            )

            # Wait for review list
            await self.page.wait_for_selector(".comment-list, .review-list", timeout=10000)

            # Apply filters
            if start_date or end_date:
                await self._apply_date_filter(start_date, end_date)

            # Navigate to specific page if needed
            if page > 1:
                await self._navigate_to_page(page)

            # Extract reviews
            review_elements = await self.page.query_selector_all(
                ".comment-item, .review-item"
            )

            for element in review_elements[:limit]:
                try:
                    review = await self._parse_review_element(element, store_id)
                    if review:
                        reviews.append(review)
                except Exception as e:
                    logger.warning(f"Failed to parse review element: {e}")

            logger.info(f"Fetched {len(reviews)} reviews from Douyin")
            return reviews

        except Exception as e:
            logger.error(f"Error fetching reviews from Douyin: {e}")
            return []

    async def _apply_date_filter(
        self, start_date: Optional[datetime], end_date: Optional[datetime]
    ) -> None:
        """Apply date filter."""
        try:
            filter_btn = await self.page.wait_for_selector(
                ".date-filter, .time-filter",
                timeout=5000,
            )
            if filter_btn:
                await filter_btn.click()

                if start_date:
                    start_input = await self.page.wait_for_selector(
                        ".start-date input",
                        timeout=3000,
                    )
                    if start_input:
                        await start_input.fill(start_date.strftime("%Y-%m-%d"))

                if end_date:
                    end_input = await self.page.wait_for_selector(
                        ".end-date input",
                        timeout=3000,
                    )
                    if end_input:
                        await end_input.fill(end_date.strftime("%Y-%m-%d"))

                confirm_btn = await self.page.wait_for_selector(
                    "button:has-text('确定'), .confirm-btn",
                    timeout=3000,
                )
                if confirm_btn:
                    await confirm_btn.click()
                    await self.page.wait_for_load_state("networkidle")

        except Exception as e:
            logger.warning(f"Failed to apply date filter: {e}")

    async def _navigate_to_page(self, page: int) -> None:
        """Navigate to specific page."""
        try:
            page_input = await self.page.wait_for_selector(
                ".pagination input, .page-input",
                timeout=3000,
            )
            if page_input:
                await page_input.fill(str(page))
                await page_input.press("Enter")
                await self.page.wait_for_load_state("networkidle")
            else:
                # Click next page multiple times
                for _ in range(page - 1):
                    next_btn = await self.page.wait_for_selector(
                        ".next-page, .pagination-next",
                        timeout=3000,
                    )
                    if next_btn:
                        await next_btn.click()
                        await self.page.wait_for_load_state("networkidle")

        except Exception as e:
            logger.warning(f"Failed to navigate to page {page}: {e}")

    async def _parse_review_element(self, element: Any, store_id: str) -> Optional[Review]:
        """Parse review element."""
        try:
            # Extract review ID
            review_id = await element.get_attribute("data-id") or ""
            if not review_id:
                review_id = f"dy_{datetime.now().timestamp()}"

            # Author info
            author_elem = await element.query_selector(".user-name, .author")
            author_name = "Anonymous"
            if author_elem:
                author_name = await author_elem.text_content() or "Anonymous"

            # Rating
            rating = 5  # Douyin may not have explicit ratings
            rating_elem = await element.query_selector(".rating, .star")
            if rating_elem:
                rating_text = await rating_elem.text_content()
                if rating_text:
                    try:
                        rating = int(float(rating_text))
                    except ValueError:
                        pass

            # Content
            content_elem = await element.query_selector(".content, .comment-text")
            content = ""
            if content_elem:
                content = await content_elem.text_content() or ""

            # Review time
            time_elem = await element.query_selector(".time, .date")
            review_time: Optional[datetime] = None
            if time_elem:
                time_text = await time_elem.text_content()
                if time_text:
                    review_time = self._parse_datetime(time_text.strip())

            # Reply
            reply_elem = await element.query_selector(".reply, .merchant-reply")
            reply_content = None
            if reply_elem:
                reply_content = await reply_elem.text_content()

            # Images
            images: list[str] = []
            img_elems = await element.query_selector_all(".image img, .media img")
            for img in img_elems:
                src = await img.get_attribute("src")
                if src:
                    images.append(src)

            return Review(
                review_id=review_id,
                platform="douyin",
                store_id=store_id,
                author_name=author_name.strip(),
                rating=rating,
                content=content.strip(),
                images=images,
                reply_content=reply_content.strip() if reply_content else None,
                review_time=review_time,
            )

        except Exception as e:
            logger.warning(f"Error parsing review element: {e}")
            return None

    def _parse_datetime(self, text: str) -> Optional[datetime]:
        """Parse datetime string."""
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d",
            "%m-%d %H:%M",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                continue
        return None

    async def fetch_store_info(self, store_id: str) -> Optional[StoreInfo]:
        """
        Fetch store information from Douyin.

        Args:
            store_id: Douyin store ID

        Returns:
            StoreInfo object
        """
        logger.info(f"Fetching store info for {store_id}")

        if not self.is_logged_in:
            if not await self.login():
                return None

        try:
            await self.page.goto(
                f"{self.BASE_URL}/shop/detail?shopId={store_id}",
                wait_until="networkidle",
            )

            await self.page.wait_for_selector(".shop-info, .store-detail", timeout=10000)

            name_elem = await self.page.query_selector(".shop-name, .store-name")
            name = "Unknown"
            if name_elem:
                name = await name_elem.text_content() or "Unknown"

            address_elem = await self.page.query_selector(".shop-address, .address")
            address = None
            if address_elem:
                address = await address_elem.text_content()

            phone_elem = await self.page.query_selector(".shop-phone, .contact-phone")
            phone = None
            if phone_elem:
                phone = await phone_elem.text_content()

            rating_elem = await self.page.query_selector(".shop-score, .rating")
            rating = None
            if rating_elem:
                rating_text = await rating_elem.text_content()
                if rating_text:
                    try:
                        rating = float(rating_text.strip())
                    except ValueError:
                        pass

            return StoreInfo(
                store_id=store_id,
                platform="douyin",
                name=name.strip(),
                address=address.strip() if address else None,
                phone=phone.strip() if phone else None,
                rating=rating,
            )

        except Exception as e:
            logger.error(f"Error fetching store info from Douyin: {e}")
            return None

    async def reply_review(self, review_id: str, content: str) -> bool:
        """
        Reply to a review on Douyin.

        Args:
            review_id: Review ID
            content: Reply content

        Returns:
            True if reply successful
        """
        logger.info(f"Replying to review {review_id}")

        if not self.is_logged_in:
            if not await self.login():
                return False

        try:
            # Find the review and click reply
            reply_btn = await self.page.wait_for_selector(
                f"[data-id='{review_id}'] .reply-btn, .reply-button",
                timeout=5000,
            )
            if not reply_btn:
                return False

            await reply_btn.click()

            reply_input = await self.page.wait_for_selector(
                "textarea.reply-input, .reply-textarea",
                timeout=5000,
            )
            if not reply_input:
                return False

            await reply_input.fill(content)

            submit_btn = await self.page.wait_for_selector(
                "button:has-text('提交'), button:has-text('回复'), .submit-reply",
                timeout=5000,
            )
            if not submit_btn:
                return False

            await submit_btn.click()

            # Wait for success
            await self.page.wait_for_selector(
                ".reply-success, .success-message",
                timeout=5000,
            )

            logger.info(f"Successfully replied to review {review_id}")
            return True

        except Exception as e:
            logger.error(f"Error replying to review on Douyin: {e}")
            return False

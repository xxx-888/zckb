"""
Meituan (美团开店宝) spider implementation.
"""
from datetime import datetime
from typing import Any, Optional

from playwright.async_api import TimeoutError as PlaywrightTimeout

from app.core.logger import get_logger
from app.spiders.base import BaseSpider, Credentials, Review, StoreInfo

logger = get_logger("spiders.meituan")


class MeituanSpider(BaseSpider):
    """Spider for Meituan platform (美团开店宝)."""

    BASE_URL = "https://e.waimai.meituan.com"
    LOGIN_URL = "https://e.waimai.meituan.com/#/login"
    REVIEW_URL_TEMPLATE = "https://e.waimai.meituan.com/#/comment/commentList"

    def __init__(self, credentials: Credentials) -> None:
        """Initialize Meituan spider."""
        super().__init__("meituan", credentials)
        self.store_name: Optional[str] = None

    def _get_cookie_domain(self) -> str:
        """Get cookie domain for Meituan."""
        return ".meituan.com"

    async def login(self) -> bool:
        """
        Login to Meituan merchant platform.

        Returns:
            True if login successful
        """
        logger.info("Attempting to login to Meituan")

        try:
            # Navigate to login page
            await self.page.goto(self.LOGIN_URL, wait_until="networkidle")
            await self.page.wait_for_load_state("domcontentloaded")

            # Check if already logged in
            if await self._is_logged_in():
                logger.info("Already logged in to Meituan")
                self.is_logged_in = True
                return True

            # Fill login form
            # Note: Meituan may have different login methods (password, SMS, QR code)
            # This implementation assumes password login
            try:
                # Try to find username/password fields
                username_input = await self.page.wait_for_selector(
                    "input[placeholder*='手机号'], input[placeholder*='用户名']",
                    timeout=5000,
                )
                password_input = await self.page.wait_for_selector(
                    "input[type='password']",
                    timeout=5000,
                )

                if username_input and password_input:
                    await username_input.fill(self.credentials.username)
                    await password_input.fill(self.credentials.password)

                    # Click login button
                    login_btn = await self.page.wait_for_selector(
                        "button:has-text('登录'), button[type='submit']",
                        timeout=5000,
                    )
                    if login_btn:
                        await login_btn.click()

            except PlaywrightTimeout:
                logger.warning("Standard login form not found, trying alternative methods")
                # Handle QR code login or other methods
                # This is a placeholder for alternative login flows
                pass

            # Wait for navigation after login
            await self.page.wait_for_load_state("networkidle")

            # Verify login success
            if await self._is_logged_in():
                self.is_logged_in = True
                # Save cookies for future use
                self.credentials.cookies = await self.save_cookies()
                logger.info("Successfully logged in to Meituan")
                return True

            logger.error("Failed to login to Meituan")
            return False

        except Exception as e:
            logger.error(f"Error during Meituan login: {e}")
            return False

    async def _is_logged_in(self) -> bool:
        """Check if currently logged in."""
        try:
            # Check for login indicator (e.g., user avatar, dashboard element)
            indicator = await self.page.wait_for_selector(
                ".user-info, .merchant-name, .dashboard",
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
        Fetch reviews from Meituan.

        Args:
            store_id: Meituan store ID (POI ID)
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
                logger.error("Not logged in, cannot fetch reviews")
                return []

        reviews: list[Review] = []

        try:
            # Navigate to review management page
            await self.page.goto(
                f"{self.REVIEW_URL_TEMPLATE}?poiId={store_id}",
                wait_until="networkidle",
            )

            # Wait for review list to load
            await self.page.wait_for_selector(".comment-list, .review-list", timeout=10000)

            # Apply date filters if provided
            if start_date or end_date:
                await self._apply_date_filter(start_date, end_date)

            # Extract reviews from current page
            review_elements = await self.page.query_selector_all(
                ".comment-item, .review-item"
            )

            for idx, element in enumerate(review_elements[:limit]):
                try:
                    review = await self._parse_review_element(element, store_id)
                    if review:
                        reviews.append(review)
                except Exception as e:
                    logger.warning(f"Failed to parse review element {idx}: {e}")

            logger.info(f"Fetched {len(reviews)} reviews from Meituan")
            return reviews

        except Exception as e:
            logger.error(f"Error fetching reviews from Meituan: {e}")
            return []

    async def _apply_date_filter(
        self, start_date: Optional[datetime], end_date: Optional[datetime]
    ) -> None:
        """Apply date filter to review list."""
        try:
            # Open date picker
            date_picker = await self.page.wait_for_selector(
                ".date-picker, .time-filter",
                timeout=5000,
            )
            if date_picker:
                await date_picker.click()

                # Set start date
                if start_date:
                    start_input = await self.page.wait_for_selector(
                        "input[placeholder*='开始'], .start-date",
                        timeout=3000,
                    )
                    if start_input:
                        await start_input.fill(start_date.strftime("%Y-%m-%d"))

                # Set end date
                if end_date:
                    end_input = await self.page.wait_for_selector(
                        "input[placeholder*='结束'], .end-date",
                        timeout=3000,
                    )
                    if end_input:
                        await end_input.fill(end_date.strftime("%Y-%m-%d"))

                # Apply filter
                apply_btn = await self.page.wait_for_selector(
                    "button:has-text('确定'), button:has-text('查询')",
                    timeout=3000,
                )
                if apply_btn:
                    await apply_btn.click()
                    await self.page.wait_for_load_state("networkidle")

        except Exception as e:
            logger.warning(f"Failed to apply date filter: {e}")

    async def _parse_review_element(self, element: Any, store_id: str) -> Optional[Review]:
        """Parse a review element into Review object."""
        try:
            # Extract review ID
            review_id_elem = await element.query_selector("[data-review-id], .review-id")
            review_id = ""
            if review_id_elem:
                review_id = await review_id_elem.get_attribute("data-review-id") or ""
            if not review_id:
                review_id = f"mt_{datetime.now().timestamp()}"

            # Extract author info
            author_elem = await element.query_selector(".user-name, .author-name")
            author_name = "Anonymous"
            if author_elem:
                author_name = await author_elem.text_content() or "Anonymous"

            # Extract rating
            rating_elem = await element.query_selector(".star-rating, .rating")
            rating = 5
            if rating_elem:
                rating_text = await rating_elem.get_attribute("data-rating")
                if rating_text:
                    rating = int(float(rating_text))

            # Extract content
            content_elem = await element.query_selector(".comment-content, .review-content")
            content = ""
            if content_elem:
                content = await content_elem.text_content() or ""

            # Extract review time
            time_elem = await element.query_selector(".comment-time, .review-time")
            review_time: Optional[datetime] = None
            if time_elem:
                time_text = await time_elem.text_content()
                if time_text:
                    review_time = self._parse_datetime(time_text.strip())

            # Extract reply info
            reply_elem = await element.query_selector(".merchant-reply, .reply-content")
            reply_content = None
            reply_time = None
            if reply_elem:
                reply_content = await reply_elem.text_content()
                reply_time_elem = await element.query_selector(".reply-time")
                if reply_time_elem:
                    reply_time_text = await reply_time_elem.text_content()
                    if reply_time_text:
                        reply_time = self._parse_datetime(reply_time_text.strip())

            # Extract images
            image_elems = await element.query_selector_all(".comment-img, .review-img")
            images: list[str] = []
            for img in image_elems:
                src = await img.get_attribute("src")
                if src:
                    images.append(src)

            return Review(
                review_id=review_id,
                platform="meituan",
                store_id=store_id,
                author_name=author_name.strip(),
                rating=rating,
                content=content.strip(),
                images=images,
                reply_content=reply_content.strip() if reply_content else None,
                reply_time=reply_time,
                review_time=review_time,
            )

        except Exception as e:
            logger.warning(f"Error parsing review element: {e}")
            return None

    def _parse_datetime(self, text: str) -> Optional[datetime]:
        """Parse datetime string from Meituan format."""
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
        Fetch store information from Meituan.

        Args:
            store_id: Meituan store ID

        Returns:
            StoreInfo object
        """
        logger.info(f"Fetching store info for {store_id}")

        if not self.is_logged_in:
            if not await self.login():
                return None

        try:
            # Navigate to store info page
            await self.page.goto(
                f"{self.BASE_URL}/#/shop/shopInfo?poiId={store_id}",
                wait_until="networkidle",
            )

            # Wait for store info to load
            await self.page.wait_for_selector(".shop-info, .store-info", timeout=10000)

            # Extract store information
            name_elem = await self.page.query_selector(".shop-name, .store-name")
            name = "Unknown"
            if name_elem:
                name = await name_elem.text_content() or "Unknown"

            address_elem = await self.page.query_selector(".shop-address, .address")
            address = None
            if address_elem:
                address = await address_elem.text_content()

            phone_elem = await self.page.query_selector(".shop-phone, .phone")
            phone = None
            if phone_elem:
                phone = await phone_elem.text_content()

            rating_elem = await self.page.query_selector(".shop-rating, .rating-score")
            rating = None
            if rating_elem:
                rating_text = await rating_elem.text_content()
                if rating_text:
                    try:
                        rating = float(rating_text.strip())
                    except ValueError:
                        pass

            review_count_elem = await self.page.query_selector(".review-count, .comment-count")
            review_count = 0
            if review_count_elem:
                count_text = await review_count_elem.text_content()
                if count_text:
                    try:
                        review_count = int("".join(filter(str.isdigit, count_text)))
                    except ValueError:
                        pass

            return StoreInfo(
                store_id=store_id,
                platform="meituan",
                name=name.strip(),
                address=address.strip() if address else None,
                phone=phone.strip() if phone else None,
                rating=rating,
                review_count=review_count,
            )

        except Exception as e:
            logger.error(f"Error fetching store info from Meituan: {e}")
            return None

    async def reply_review(self, review_id: str, content: str) -> bool:
        """
        Reply to a review on Meituan.

        Args:
            review_id: Review ID to reply to
            content: Reply content

        Returns:
            True if reply successful
        """
        logger.info(f"Replying to review {review_id}")

        if not self.is_logged_in:
            if not await self.login():
                return False

        try:
            # Navigate to review page
            await self.page.goto(
                f"{self.REVIEW_URL_TEMPLATE}?reviewId={review_id}",
                wait_until="networkidle",
            )

            # Find reply button
            reply_btn = await self.page.wait_for_selector(
                f"[data-review-id='{review_id}'] .reply-btn, .reply-button",
                timeout=5000,
            )
            if not reply_btn:
                logger.error(f"Reply button not found for review {review_id}")
                return False

            await reply_btn.click()

            # Fill reply content
            reply_input = await self.page.wait_for_selector(
                "textarea.reply-input, .reply-textarea",
                timeout=5000,
            )
            if not reply_input:
                logger.error("Reply input not found")
                return False

            await reply_input.fill(content)

            # Submit reply
            submit_btn = await self.page.wait_for_selector(
                "button:has-text('提交'), button:has-text('回复'), .submit-reply",
                timeout=5000,
            )
            if not submit_btn:
                logger.error("Submit button not found")
                return False

            await submit_btn.click()

            # Wait for success indicator
            await self.page.wait_for_selector(
                ".reply-success, .success-message",
                timeout=5000,
            )

            logger.info(f"Successfully replied to review {review_id}")
            return True

        except Exception as e:
            logger.error(f"Error replying to review on Meituan: {e}")
            return False

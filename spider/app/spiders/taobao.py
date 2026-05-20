"""
Taobao (淘宝闪购) spider implementation.
"""
from datetime import datetime
from typing import Any, Optional

from playwright.async_api import TimeoutError as PlaywrightTimeout

from app.core.logger import get_logger
from app.spiders.base import BaseSpider, Credentials, Review, StoreInfo

logger = get_logger("spiders.taobao")


class TaobaoSpider(BaseSpider):
    """Spider for Taobao Flash Purchase platform (淘宝闪购)."""

    BASE_URL = "https://seller.taobao.com"
    LOGIN_URL = "https://login.taobao.com/member/login.jhtml"
    REVIEW_URL_TEMPLATE = "https://rate.taobao.com/myRate.htm"

    def __init__(self, credentials: Credentials) -> None:
        """Initialize Taobao spider."""
        super().__init__("taobao", credentials)

    def _get_cookie_domain(self) -> str:
        """Get cookie domain for Taobao."""
        return ".taobao.com"

    async def login(self) -> bool:
        """
        Login to Taobao seller platform.

        Returns:
            True if login successful
        """
        logger.info("Attempting to login to Taobao")

        try:
            await self.page.goto(self.LOGIN_URL, wait_until="networkidle")
            await self.page.wait_for_load_state("domcontentloaded")

            # Check if already logged in
            if await self._is_logged_in():
                logger.info("Already logged in to Taobao")
                self.is_logged_in = True
                return True

            # Taobao uses various login methods
            try:
                # Try password login
                username_input = await self.page.wait_for_selector(
                    "#fm-login-id, input[name='fm-login-id'], input[placeholder*='手机号']",
                    timeout=5000,
                )
                password_input = await self.page.wait_for_selector(
                    "#fm-login-password, input[name='fm-login-password']",
                    timeout=5000,
                )

                if username_input and password_input:
                    await username_input.fill(self.credentials.username)
                    await password_input.fill(self.credentials.password)

                    # Handle slider verification if present
                    slider = await self.page.query_selector(".nc_wrapper, .slide-verify")
                    if slider:
                        logger.warning("Slider verification detected, manual intervention needed")
                        await self.page.wait_for_timeout(30000)

                    # Click login button
                    login_btn = await self.page.wait_for_selector(
                        ".password-login-btn, button[type='submit']",
                        timeout=5000,
                    )
                    if login_btn:
                        await login_btn.click()

            except PlaywrightTimeout:
                logger.warning("Standard login form not found, trying QR code")
                # QR code login fallback
                await self.page.wait_for_timeout(60000)

            # Wait for navigation
            await self.page.wait_for_load_state("networkidle")

            if await self._is_logged_in():
                self.is_logged_in = True
                self.credentials.cookies = await self.save_cookies()
                logger.info("Successfully logged in to Taobao")
                return True

            logger.error("Failed to login to Taobao")
            return False

        except Exception as e:
            logger.error(f"Error during Taobao login: {e}")
            return False

    async def _is_logged_in(self) -> bool:
        """Check if currently logged in."""
        try:
            indicator = await self.page.wait_for_selector(
                ".site-nav-user, .seller-name, .user-info",
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
        Fetch reviews from Taobao.

        Args:
            store_id: Taobao store ID
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
            # Navigate to rate management page
            await self.page.goto(
                f"{self.REVIEW_URL_TEMPLATE}?sellerId={store_id}&currentPage={page}",
                wait_until="networkidle",
            )

            await self.page.wait_for_selector(".rate-list, .review-list", timeout=10000)

            # Apply date filters
            if start_date or end_date:
                await self._apply_date_filter(start_date, end_date)

            # Extract reviews
            review_elements = await self.page.query_selector_all(
                ".rate-item, .review-item"
            )

            for element in review_elements[:limit]:
                try:
                    review = await self._parse_review_element(element, store_id)
                    if review:
                        reviews.append(review)
                except Exception as e:
                    logger.warning(f"Failed to parse review element: {e}")

            logger.info(f"Fetched {len(reviews)} reviews from Taobao")
            return reviews

        except Exception as e:
            logger.error(f"Error fetching reviews from Taobao: {e}")
            return []

    async def _apply_date_filter(
        self, start_date: Optional[datetime], end_date: Optional[datetime]
    ) -> None:
        """Apply date filter."""
        try:
            if start_date:
                start_input = await self.page.wait_for_selector(
                    "#startDate, .start-date",
                    timeout=3000,
                )
                if start_input:
                    await start_input.fill(start_date.strftime("%Y-%m-%d"))

            if end_date:
                end_input = await self.page.wait_for_selector(
                    "#endDate, .end-date",
                    timeout=3000,
                )
                if end_input:
                    await end_input.fill(end_date.strftime("%Y-%m-%d"))

            search_btn = await self.page.wait_for_selector(
                "button:has-text('搜索'), .search-btn",
                timeout=3000,
            )
            if search_btn:
                await search_btn.click()
                await self.page.wait_for_load_state("networkidle")

        except Exception as e:
            logger.warning(f"Failed to apply date filter: {e}")

    async def _parse_review_element(self, element: Any, store_id: str) -> Optional[Review]:
        """Parse review element."""
        try:
            review_id = await element.get_attribute("data-rateid") or ""
            if not review_id:
                review_id = f"tb_{datetime.now().timestamp()}"

            # Author
            author_elem = await element.query_selector(".buyer-name, .user-name")
            author_name = "Anonymous"
            if author_elem:
                author_name = await author_elem.text_content() or "Anonymous"

            # Rating
            rating = 5
            rating_elem = await element.query_selector(".star-level, .rate-star")
            if rating_elem:
                rating_class = await rating_elem.get_attribute("class")
                if rating_class:
                    # Extract rating from class like "star5" or "rate-star-5"
                    import re
                    match = re.search(r'(\d)', rating_class)
                    if match:
                        rating = int(match.group(1))

            # Content
            content_elem = await element.query_selector(".rate-content, .review-content")
            content = ""
            if content_elem:
                content = await content_elem.text_content() or ""

            # Review time
            time_elem = await element.query_selector(".rate-date, .review-time")
            review_time: Optional[datetime] = None
            if time_elem:
                time_text = await time_elem.text_content()
                if time_text:
                    review_time = self._parse_datetime(time_text.strip())

            # Reply
            reply_elem = await element.query_selector(".reply-content, .seller-reply")
            reply_content = None
            if reply_elem:
                reply_content = await reply_elem.text_content()

            # Images
            images: list[str] = []
            img_elems = await element.query_selector_all(".photo-view img, .rate-img")
            for img in img_elems:
                src = await img.get_attribute("src")
                if src:
                    images.append(src)

            return Review(
                review_id=review_id,
                platform="taobao",
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
            "%Y年%m月%d日",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                continue
        return None

    async def fetch_store_info(self, store_id: str) -> Optional[StoreInfo]:
        """Fetch store information from Taobao."""
        logger.info(f"Fetching store info for {store_id}")

        if not self.is_logged_in:
            if not await self.login():
                return None

        try:
            await self.page.goto(
                f"https://store.taobao.com/shop/view_shop.htm?user_number_id={store_id}",
                wait_until="networkidle",
            )

            await self.page.wait_for_selector(".shop-info, .shop-header", timeout=10000)

            name_elem = await self.page.query_selector(".shop-name a, .shop-title")
            name = "Unknown"
            if name_elem:
                name = await name_elem.text_content() or "Unknown"

            rating_elem = await self.page.query_selector(".shop-score, .dsr-info")
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
                platform="taobao",
                name=name.strip(),
                rating=rating,
            )

        except Exception as e:
            logger.error(f"Error fetching store info from Taobao: {e}")
            return None

    async def reply_review(self, review_id: str, content: str) -> bool:
        """Reply to a review on Taobao."""
        logger.info(f"Replying to review {review_id}")

        if not self.is_logged_in:
            if not await self.login():
                return False

        try:
            reply_btn = await self.page.wait_for_selector(
                f"[data-rateid='{review_id}'] .reply-btn",
                timeout=5000,
            )
            if not reply_btn:
                return False

            await reply_btn.click()

            reply_input = await self.page.wait_for_selector(
                "textarea.reply-input",
                timeout=5000,
            )
            if not reply_input:
                return False

            await reply_input.fill(content)

            submit_btn = await self.page.wait_for_selector(
                "button:has-text('提交'), .submit-reply",
                timeout=5000,
            )
            if not submit_btn:
                return False

            await submit_btn.click()

            await self.page.wait_for_selector(".reply-success", timeout=5000)

            logger.info(f"Successfully replied to review {review_id}")
            return True

        except Exception as e:
            logger.error(f"Error replying to review on Taobao: {e}")
            return False

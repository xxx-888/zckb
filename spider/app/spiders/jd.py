"""
JD (京东秒送) spider implementation.
"""
from datetime import datetime
from typing import Any, Optional

from playwright.async_api import TimeoutError as PlaywrightTimeout

from app.core.logger import get_logger
from app.spiders.base import BaseSpider, Credentials, Review, StoreInfo

logger = get_logger("spiders.jd")


class JDSpider(BaseSpider):
    """Spider for JD platform (京东秒送)."""

    BASE_URL = "https://shop.jd.com"
    LOGIN_URL = "https://passport.jd.com/new/login.aspx"
    REVIEW_URL_TEMPLATE = "https://shop.jd.com/comment/commentList.action"

    def __init__(self, credentials: Credentials) -> None:
        """Initialize JD spider."""
        super().__init__("jd", credentials)

    def _get_cookie_domain(self) -> str:
        """Get cookie domain for JD."""
        return ".jd.com"

    async def login(self) -> bool:
        """
        Login to JD merchant platform.

        Returns:
            True if login successful
        """
        logger.info("Attempting to login to JD")

        try:
            await self.page.goto(self.LOGIN_URL, wait_until="networkidle")
            await self.page.wait_for_load_state("domcontentloaded")

            # Check if already logged in
            if await self._is_logged_in():
                logger.info("Already logged in to JD")
                self.is_logged_in = True
                return True

            try:
                # JD typically uses account/password or QR code login
                # Try account login first
                login_tab = await self.page.wait_for_selector(
                    ".login-tab-r, .login-tab:nth-child(2)",
                    timeout=5000,
                )
                if login_tab:
                    await login_tab.click()  # Switch to account login

                username_input = await self.page.wait_for_selector(
                    "#loginname, input[name='loginname']",
                    timeout=5000,
                )
                password_input = await self.page.wait_for_selector(
                    "#nloginpwd, input[name='nloginpwd']",
                    timeout=5000,
                )

                if username_input and password_input:
                    await username_input.fill(self.credentials.username)
                    await password_input.fill(self.credentials.password)

                    # Handle captcha if present
                    captcha = await self.page.query_selector(".JD_Verification, .verify-code")
                    if captcha:
                        logger.warning("Captcha detected, manual intervention needed")
                        await self.page.wait_for_timeout(30000)

                    # Click login
                    login_btn = await self.page.wait_for_selector(
                        ".login-btn, .btn-entry",
                        timeout=5000,
                    )
                    if login_btn:
                        await login_btn.click()

            except PlaywrightTimeout:
                logger.warning("Account login not available, trying QR code")
                await self.page.wait_for_timeout(60000)

            # Wait for login to complete
            await self.page.wait_for_load_state("networkidle")

            if await self._is_logged_in():
                self.is_logged_in = True
                self.credentials.cookies = await self.save_cookies()
                logger.info("Successfully logged in to JD")
                return True

            logger.error("Failed to login to JD")
            return False

        except Exception as e:
            logger.error(f"Error during JD login: {e}")
            return False

    async def _is_logged_in(self) -> bool:
        """Check if currently logged in."""
        try:
            indicator = await self.page.wait_for_selector(
                ".user-name, .seller-name, .shop-name",
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
        Fetch reviews from JD.

        Args:
            store_id: JD store ID
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
            # Navigate to comment management
            await self.page.goto(
                f"{self.REVIEW_URL_TEMPLATE}?shopId={store_id}&page={page}",
                wait_until="networkidle",
            )

            await self.page.wait_for_selector(".comment-list, .rate-list", timeout=10000)

            # Apply filters
            if start_date or end_date:
                await self._apply_date_filter(start_date, end_date)

            # Extract reviews
            review_elements = await self.page.query_selector_all(
                ".comment-item, .rate-item"
            )

            for element in review_elements[:limit]:
                try:
                    review = await self._parse_review_element(element, store_id)
                    if review:
                        reviews.append(review)
                except Exception as e:
                    logger.warning(f"Failed to parse review element: {e}")

            logger.info(f"Fetched {len(reviews)} reviews from JD")
            return reviews

        except Exception as e:
            logger.error(f"Error fetching reviews from JD: {e}")
            return []

    async def _apply_date_filter(
        self, start_date: Optional[datetime], end_date: Optional[datetime]
    ) -> None:
        """Apply date filter."""
        try:
            filter_section = await self.page.wait_for_selector(
                ".filter-section, .date-filter",
                timeout=5000,
            )
            if filter_section:
                await filter_section.click()

                if start_date:
                    start_input = await self.page.wait_for_selector(
                        "input[placeholder*='开始'], .start-date",
                        timeout=3000,
                    )
                    if start_input:
                        await start_input.fill(start_date.strftime("%Y-%m-%d"))

                if end_date:
                    end_input = await self.page.wait_for_selector(
                        "input[placeholder*='结束'], .end-date",
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

    async def _parse_review_element(self, element: Any, store_id: str) -> Optional[Review]:
        """Parse review element."""
        try:
            review_id = await element.get_attribute("data-id") or ""
            if not review_id:
                review_id = f"jd_{datetime.now().timestamp()}"

            # Author
            author_elem = await element.query_selector(".user-info .name, .buyer-name")
            author_name = "Anonymous"
            if author_elem:
                author_name = await author_elem.text_content() or "Anonymous"

            # Rating - JD uses star icons
            rating = 5
            star_elems = await element.query_selector_all(".star-filled, .icon-star")
            if star_elems:
                rating = len(star_elems)

            # Content
            content_elem = await element.query_selector(".comment-content, .rate-content")
            content = ""
            if content_elem:
                content = await content_elem.text_content() or ""

            # Review time
            time_elem = await element.query_selector(".comment-time, .rate-date")
            review_time: Optional[datetime] = None
            if time_elem:
                time_text = await time_elem.text_content()
                if time_text:
                    review_time = self._parse_datetime(time_text.strip())

            # Reply
            reply_elem = await element.query_selector(".reply-content, .seller-reply")
            reply_content = None
            reply_time = None
            if reply_elem:
                reply_content = await reply_elem.text_content()
                reply_time_elem = await element.query_selector(".reply-time")
                if reply_time_elem:
                    reply_time_text = await reply_time_elem.text_content()
                    if reply_time_text:
                        reply_time = self._parse_datetime(reply_time_text.strip())

            # Images
            images: list[str] = []
            img_elems = await element.query_selector_all(".pic-list img, .comment-img")
            for img in img_elems:
                src = await img.get_attribute("src")
                if src:
                    images.append(src)

            # Order info
            order_elem = await element.query_selector(".order-info, .product-name")
            order_info = None
            if order_elem:
                order_info = await order_elem.text_content()

            return Review(
                review_id=review_id,
                platform="jd",
                store_id=store_id,
                author_name=author_name.strip(),
                rating=rating,
                content=content.strip(),
                images=images,
                reply_content=reply_content.strip() if reply_content else None,
                reply_time=reply_time,
                review_time=review_time,
                order_info=order_info.strip() if order_info else None,
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
            "%Y/%m/%d %H:%M:%S",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                continue
        return None

    async def fetch_store_info(self, store_id: str) -> Optional[StoreInfo]:
        """Fetch store information from JD."""
        logger.info(f"Fetching store info for {store_id}")

        if not self.is_logged_in:
            if not await self.login():
                return None

        try:
            await self.page.goto(
                f"https://shop.jd.com/shopInfo.action?shopId={store_id}",
                wait_until="networkidle",
            )

            await self.page.wait_for_selector(".shop-intro, .shop-info", timeout=10000)

            name_elem = await self.page.query_selector(".shop-name, .shop-title")
            name = "Unknown"
            if name_elem:
                name = await name_elem.text_content() or "Unknown"

            address_elem = await self.page.query_selector(".shop-address")
            address = None
            if address_elem:
                address = await address_elem.text_content()

            rating_elem = await self.page.query_selector(".shop-score")
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
                platform="jd",
                name=name.strip(),
                address=address.strip() if address else None,
                rating=rating,
            )

        except Exception as e:
            logger.error(f"Error fetching store info from JD: {e}")
            return None

    async def reply_review(self, review_id: str, content: str) -> bool:
        """Reply to a review on JD."""
        logger.info(f"Replying to review {review_id}")

        if not self.is_logged_in:
            if not await self.login():
                return False

        try:
            reply_btn = await self.page.wait_for_selector(
                f"[data-id='{review_id}'] .reply-btn, .btn-reply",
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
                "button:has-text('提交'), .btn-submit",
                timeout=5000,
            )
            if not submit_btn:
                return False

            await submit_btn.click()

            await self.page.wait_for_selector(".reply-success", timeout=5000)

            logger.info(f"Successfully replied to review {review_id}")
            return True

        except Exception as e:
            logger.error(f"Error replying to review on JD: {e}")
            return False

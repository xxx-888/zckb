"""
Celery tasks for spider operations.
"""
from datetime import datetime
from typing import Any

from celery import Task
from celery.exceptions import MaxRetriesExceededError, SoftTimeLimitExceeded

from app.core.config import settings
from app.core.logger import get_logger
from app.spiders.base import Credentials
from app.spiders.factory import create_spider
from app.tasks.api_client import APIClient
from app.tasks.celery_app import celery

logger = get_logger("tasks.spider")


class SpiderTask(Task):
    """Base task class with spider-specific error handling."""

    autoretry_for = (Exception,)
    retry_backoff = True
    retry_backoff_max = 600  # Max 10 minutes between retries
    retry_kwargs = {"max_retries": 3}
    soft_time_limit = settings.task_timeout
    time_limit = settings.task_timeout * 2

    def on_failure(self, exc: Exception, task_id: str, args: Any, kwargs: Any, einfo: Any) -> None:
        """Handle task failure."""
        logger.error(f"Task {task_id} failed: {exc}")
        # Update sync status in main backend
        try:
            if len(args) >= 2:
                platform = args[0]
                store_id = args[1]
                client = APIClient(settings.api_base_url, settings.api_key)
                import asyncio
                asyncio.run(client.update_sync_status(
                    store_id=store_id,
                    status="failed",
                    message=str(exc),
                    platform=platform,
                ))
        except Exception as e:
            logger.error(f"Failed to update sync status: {e}")


@celery.task(bind=True, base=SpiderTask)
def sync_reviews_task(
    self: SpiderTask,
    platform: str,
    store_id: str,
    credentials: dict[str, Any],
    page: int = 1,
    limit: int = 20,
    start_date: str | None = None,
    end_date: str | None = None,
) -> dict[str, Any]:
    """
    Celery task to sync reviews from a platform.

    Args:
        platform: Platform name (meituan, douyin, taobao, jd)
        store_id: Store identifier
        credentials: Platform credentials dict with username, password, etc.
        page: Page number to fetch
        limit: Number of reviews per page
        start_date: Optional start date filter (ISO format)
        end_date: Optional end date filter (ISO format)

    Returns:
        Task result with reviews data
    """
    logger.info(f"Starting review sync for {platform} store {store_id}")

    async def _sync() -> dict[str, Any]:
        creds = Credentials(
            username=credentials.get("username", ""),
            password=credentials.get("password", ""),
            cookies=credentials.get("cookies"),
            token=credentials.get("token"),
            extra_data=credentials.get("extra_data", {}),
        )

        client = APIClient(settings.api_base_url, settings.api_key)

        # Update status to in_progress
        await client.update_sync_status(
            store_id=store_id,
            status="in_progress",
            message="Starting review sync",
            platform=platform,
        )

        reviews = []
        spider = None

        try:
            spider = create_spider(platform, creds)

            async with spider:
                # Parse date filters
                start_dt = datetime.fromisoformat(start_date) if start_date else None
                end_dt = datetime.fromisoformat(end_date) if end_date else None

                # Fetch reviews
                reviews = await spider.fetch_reviews(
                    store_id=store_id,
                    page=page,
                    limit=limit,
                    start_date=start_dt,
                    end_date=end_dt,
                )

                # Submit to main backend
                if reviews:
                    review_dicts = [r.to_dict() for r in reviews]
                    await client.submit_reviews(store_id, review_dicts)

                # Update status to completed
                await client.update_sync_status(
                    store_id=store_id,
                    status="completed",
                    message=f"Successfully synced {len(reviews)} reviews",
                    platform=platform,
                    synced_count=len(reviews),
                )

                logger.info(f"Synced {len(reviews)} reviews for {platform} store {store_id}")

                return {
                    "success": True,
                    "platform": platform,
                    "store_id": store_id,
                    "reviews_count": len(reviews),
                    "page": page,
                }

        except SoftTimeLimitExceeded:
            logger.error(f"Task timed out for {platform} store {store_id}")
            await client.update_sync_status(
                store_id=store_id,
                status="failed",
                message="Task timeout",
                platform=platform,
            )
            raise

        except Exception as e:
            logger.error(f"Error syncing reviews: {e}")
            await client.update_sync_status(
                store_id=store_id,
                status="failed",
                message=str(e),
                platform=platform,
            )
            raise self.retry(exc=e)

    import asyncio
    return asyncio.run(_sync())


@celery.task(bind=True, base=SpiderTask)
def sync_store_info_task(
    self: SpiderTask,
    platform: str,
    store_id: str,
    credentials: dict[str, Any],
) -> dict[str, Any]:
    """
    Celery task to sync store information from a platform.

    Args:
        platform: Platform name
        store_id: Store identifier
        credentials: Platform credentials

    Returns:
        Task result with store info
    """
    logger.info(f"Starting store info sync for {platform} store {store_id}")

    async def _sync() -> dict[str, Any]:
        creds = Credentials(
            username=credentials.get("username", ""),
            password=credentials.get("password", ""),
            cookies=credentials.get("cookies"),
            token=credentials.get("token"),
            extra_data=credentials.get("extra_data", {}),
        )

        client = APIClient(settings.api_base_url, settings.api_key)
        spider = None

        try:
            spider = create_spider(platform, creds)

            async with spider:
                store_info = await spider.fetch_store_info(store_id)

                if store_info:
                    await client.submit_store_info(store_id, store_info.to_dict())
                    logger.info(f"Synced store info for {platform} store {store_id}")
                    return {
                        "success": True,
                        "platform": platform,
                        "store_id": store_id,
                        "store_name": store_info.name,
                    }
                else:
                    return {
                        "success": False,
                        "error": "Store not found",
                        "platform": platform,
                        "store_id": store_id,
                    }

        except Exception as e:
            logger.error(f"Error syncing store info: {e}")
            raise self.retry(exc=e)

    import asyncio
    return asyncio.run(_sync())


@celery.task(bind=True, base=SpiderTask)
def reply_review_task(
    self: SpiderTask,
    platform: str,
    review_id: str,
    content: str,
    credentials: dict[str, Any],
    store_id: str | None = None,
) -> dict[str, Any]:
    """
    Celery task to reply to a review.

    Args:
        platform: Platform name
        review_id: Review identifier
        content: Reply content
        credentials: Platform credentials
        store_id: Optional store ID for context

    Returns:
        Task result
    """
    logger.info(f"Starting reply to {platform} review {review_id}")

    async def _reply() -> dict[str, Any]:
        creds = Credentials(
            username=credentials.get("username", ""),
            password=credentials.get("password", ""),
            cookies=credentials.get("cookies"),
            token=credentials.get("token"),
            extra_data=credentials.get("extra_data", {}),
        )

        client = APIClient(settings.api_base_url, settings.api_key)
        spider = None

        try:
            spider = create_spider(platform, creds)

            async with spider:
                success = await spider.reply_review(review_id, content)

                if success:
                    # Notify main backend of successful reply
                    await client.update_sync_status(
                        store_id=store_id or review_id,
                        status="reply_sent",
                        message=f"Reply sent to review {review_id}",
                        platform=platform,
                    )

                logger.info(f"Reply to {platform} review {review_id}: {'success' if success else 'failed'}")
                return {
                    "success": success,
                    "platform": platform,
                    "review_id": review_id,
                }

        except Exception as e:
            logger.error(f"Error replying to review: {e}")
            raise self.retry(exc=e)

    import asyncio
    return asyncio.run(_reply())


@celery.task(bind=True, base=SpiderTask)
def monitor_reviews_task(
    self: SpiderTask,
    platform: str,
    store_ids: list[str],
    credentials: dict[str, Any],
    last_check_time: str | None = None,
) -> dict[str, Any]:
    """
    Celery task to monitor new reviews for multiple stores.

    Args:
        platform: Platform name
        store_ids: List of store identifiers to monitor
        credentials: Platform credentials
        last_check_time: ISO format datetime of last check

    Returns:
        Task result with new reviews count
    """
    logger.info(f"Starting review monitoring for {platform} stores: {store_ids}")

    async def _monitor() -> dict[str, Any]:
        creds = Credentials(
            username=credentials.get("username", ""),
            password=credentials.get("password", ""),
            cookies=credentials.get("cookies"),
            token=credentials.get("token"),
            extra_data=credentials.get("extra_data", {}),
        )

        client = APIClient(settings.api_base_url, settings.api_key)
        spider = None
        total_new_reviews = 0

        try:
            spider = create_spider(platform, creds)

            async with spider:
                last_check = datetime.fromisoformat(last_check_time) if last_check_time else None

                for store_id in store_ids:
                    try:
                        if last_check:
                            new_reviews = await spider.check_new_reviews(store_id, last_check)
                        else:
                            # First run - get recent reviews
                            new_reviews = await spider.fetch_reviews(store_id, page=1, limit=10)

                        if new_reviews:
                            review_dicts = [r.to_dict() for r in new_reviews]
                            await client.submit_reviews(store_id, review_dicts)
                            total_new_reviews += len(new_reviews)

                            logger.info(f"Found {len(new_reviews)} new reviews for {store_id}")

                    except Exception as e:
                        logger.error(f"Error monitoring store {store_id}: {e}")
                        continue

                return {
                    "success": True,
                    "platform": platform,
                    "stores_checked": len(store_ids),
                    "new_reviews_count": total_new_reviews,
                }

        except Exception as e:
            logger.error(f"Error in monitor task: {e}")
            raise self.retry(exc=e)

    import asyncio
    return asyncio.run(_monitor())


@celery.task(bind=True)
def monitor_all_stores_task(self: Task) -> dict[str, Any]:
    """
    Periodic task to monitor all configured stores.
    Fetches pending tasks from main backend and schedules monitoring.
    """
    logger.info("Starting scheduled monitoring of all stores")

    async def _monitor_all() -> dict[str, Any]:
        client = APIClient(settings.api_base_url, settings.api_key)

        try:
            # Get pending monitoring tasks from main backend
            pending_tasks = await client.get_pending_tasks()

            task_count = 0
            for task in pending_tasks:
                platform = task.get("platform")
                store_ids = task.get("store_ids", [])
                credentials = task.get("credentials", {})
                last_check = task.get("last_check_time")

                if platform and store_ids and credentials:
                    # Schedule monitor task
                    monitor_reviews_task.delay(
                        platform=platform,
                        store_ids=store_ids,
                        credentials=credentials,
                        last_check_time=last_check,
                    )
                    task_count += 1

            logger.info(f"Scheduled {task_count} monitoring tasks")
            return {
                "success": True,
                "tasks_scheduled": task_count,
            }

        except Exception as e:
            logger.error(f"Error in monitor all task: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    import asyncio
    return asyncio.run(_monitor_all())

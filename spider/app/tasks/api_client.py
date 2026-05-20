"""
API client for communicating with the main backend.
"""
from typing import Any

import httpx

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("tasks.api_client")


class APIClient:
    """Client for main backend API communication."""

    def __init__(self, base_url: str, api_key: str) -> None:
        """
        Initialize API client.

        Args:
            base_url: Base URL of the main backend API
            api_key: API key for authentication
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def submit_reviews(self, store_id: str, reviews: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Submit reviews to the main backend.

        Args:
            store_id: Store identifier
            reviews: List of review dictionaries

        Returns:
            API response
        """
        url = f"{self.base_url}/reviews/batch"
        payload = {
            "store_id": store_id,
            "reviews": reviews,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self.headers,
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Submitted {len(reviews)} reviews for store {store_id}")
                return result

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error submitting reviews: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Error submitting reviews: {e}")
                raise

    async def submit_store_info(self, store_id: str, info: dict[str, Any]) -> dict[str, Any]:
        """
        Submit store information to the main backend.

        Args:
            store_id: Store identifier
            info: Store information dictionary

        Returns:
            API response
        """
        url = f"{self.base_url}/stores/{store_id}"

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.put(
                    url,
                    json=info,
                    headers=self.headers,
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Submitted store info for {store_id}")
                return result

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error submitting store info: {e.response.status_code}")
                raise
            except Exception as e:
                logger.error(f"Error submitting store info: {e}")
                raise

    async def update_sync_status(
        self,
        store_id: str,
        status: str,
        message: str,
        platform: str,
        synced_count: int | None = None,
    ) -> dict[str, Any]:
        """
        Update sync status in the main backend.

        Args:
            store_id: Store identifier
            status: Sync status (in_progress, completed, failed)
            message: Status message
            platform: Platform name
            synced_count: Number of synced items (optional)

        Returns:
            API response
        """
        url = f"{self.base_url}/sync-status"
        payload = {
            "store_id": store_id,
            "platform": platform,
            "status": status,
            "message": message,
            "synced_count": synced_count,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self.headers,
                )
                response.raise_for_status()
                result = response.json()
                logger.debug(f"Updated sync status for {store_id}: {status}")
                return result

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error updating sync status: {e.response.status_code}")
                raise
            except Exception as e:
                logger.error(f"Error updating sync status: {e}")
                raise

    async def get_pending_tasks(self) -> list[dict[str, Any]]:
        """
        Get pending monitoring tasks from the main backend.

        Returns:
            List of pending task configurations
        """
        url = f"{self.base_url}/tasks/pending"

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(
                    url,
                    headers=self.headers,
                )
                response.raise_for_status()
                result = response.json()
                tasks = result.get("tasks", [])
                logger.info(f"Retrieved {len(tasks)} pending tasks")
                return tasks

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error getting pending tasks: {e.response.status_code}")
                return []
            except Exception as e:
                logger.error(f"Error getting pending tasks: {e}")
                return []

    async def get_store_credentials(self, store_id: str, platform: str) -> dict[str, Any] | None:
        """
        Get credentials for a store from the main backend.

        Args:
            store_id: Store identifier
            platform: Platform name

        Returns:
            Credentials dictionary or None
        """
        url = f"{self.base_url}/stores/{store_id}/credentials"

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(
                    url,
                    headers=self.headers,
                    params={"platform": platform},
                )
                response.raise_for_status()
                result = response.json()
                return result.get("credentials")

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    logger.warning(f"Credentials not found for {store_id}")
                    return None
                logger.error(f"HTTP error getting credentials: {e.response.status_code}")
                raise
            except Exception as e:
                logger.error(f"Error getting credentials: {e}")
                raise

    async def notify_new_reviews(
        self,
        store_id: str,
        platform: str,
        review_count: int,
        reviews: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Notify main backend of new reviews.

        Args:
            store_id: Store identifier
            platform: Platform name
            review_count: Number of new reviews
            reviews: Optional list of new review data

        Returns:
            API response
        """
        url = f"{self.base_url}/notifications/new-reviews"
        payload = {
            "store_id": store_id,
            "platform": platform,
            "review_count": review_count,
            "reviews": reviews or [],
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self.headers,
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Notified new reviews for {store_id}: {review_count}")
                return result

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error notifying new reviews: {e.response.status_code}")
                raise
            except Exception as e:
                logger.error(f"Error notifying new reviews: {e}")
                raise

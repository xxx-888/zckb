"""
Celery Worker startup script.
Usage: python worker.py
"""
import sys

from app.core.config import settings
from app.core.logger import get_logger
from app.tasks.celery_app import celery

logger = get_logger("worker")


def main() -> int:
    """Main entry point for Celery worker."""
    logger.info("Starting Celery worker")

    # Start Celery worker
    argv = [
        "worker",
        "--loglevel=info",
        f"--concurrency={settings.max_concurrent_tasks}",
        "--queues=spider,monitor",
        "--hostname=spider-worker@%h",
    ]

    try:
        celery.worker_main(argv)
        return 0
    except Exception as e:
        logger.error(f"Worker failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

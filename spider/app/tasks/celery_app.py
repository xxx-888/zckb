"""
Celery application configuration for distributed task processing.
"""
from celery import Celery

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("tasks.celery")

# Create Celery application
celery = Celery("spider_tasks")

# Configure from settings
celery.config_from_object(settings.celery_config)

# Define task routes and queues
celery.conf.task_routes = {
    "app.tasks.spider_tasks.sync_reviews_task": {"queue": "spider"},
    "app.tasks.spider_tasks.sync_store_info_task": {"queue": "spider"},
    "app.tasks.spider_tasks.reply_review_task": {"queue": "spider"},
    "app.tasks.spider_tasks.monitor_reviews_task": {"queue": "monitor"},
}

# Define default queue
celery.conf.task_default_queue = "spider"
celery.conf.task_queues = {
    "spider": {
        "exchange": "spider",
        "routing_key": "spider",
    },
    "monitor": {
        "exchange": "monitor",
        "routing_key": "monitor",
    },
}

# Beat schedule for periodic tasks
celery.conf.beat_schedule = {
    "monitor-all-stores": {
        "task": "app.tasks.spider_tasks.monitor_all_stores_task",
        "schedule": 300.0,  # Run every 5 minutes
    },
}

logger.info("Celery application initialized")


def get_celery_app() -> Celery:
    """Get the Celery application instance."""
    return celery

"""
Spider factory for creating platform-specific spider instances.
"""
from typing import Type

from app.core.logger import get_logger
from app.spiders.base import BaseSpider, Credentials
from app.spiders.douyin import DouyinSpider
from app.spiders.jd import JDSpider
from app.spiders.meituan import MeituanSpider
from app.spiders.taobao import TaobaoSpider

logger = get_logger("spiders.factory")

# Map of platform names to spider classes
SPIDER_MAP: dict[str, Type[BaseSpider]] = {
    "meituan": MeituanSpider,
    "douyin": DouyinSpider,
    "taobao": TaobaoSpider,
    "jd": JDSpider,
    # Aliases
    "美团": MeituanSpider,
    "抖音": DouyinSpider,
    "淘宝": TaobaoSpider,
    "京东": JDSpider,
}


def create_spider(platform: str, credentials: Credentials) -> BaseSpider:
    """
    Create a spider instance for the specified platform.

    Args:
        platform: Platform name (e.g., 'meituan', 'douyin', 'taobao', 'jd')
        credentials: Platform credentials

    Returns:
        Spider instance

    Raises:
        ValueError: If platform is not supported
    """
    platform_lower = platform.lower()

    if platform_lower not in SPIDER_MAP:
        supported = ", ".join(SPIDER_MAP.keys())
        raise ValueError(
            f"Unsupported platform: {platform}. "
            f"Supported platforms: {supported}"
        )

    spider_class = SPIDER_MAP[platform_lower]
    spider = spider_class(credentials)

    logger.info(f"Created {spider_class.__name__} for platform: {platform}")
    return spider


def get_supported_platforms() -> list[str]:
    """
    Get list of supported platform names.

    Returns:
        List of platform identifiers
    """
    # Return only English identifiers (filter out Chinese aliases)
    return [p for p in SPIDER_MAP.keys() if p.isascii()]


def is_platform_supported(platform: str) -> bool:
    """
    Check if a platform is supported.

    Args:
        platform: Platform name to check

    Returns:
        True if platform is supported
    """
    return platform.lower() in SPIDER_MAP

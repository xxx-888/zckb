"""
二维码登录服务
管理 Playwright 浏览器实例，处理平台扫码登录的完整生命周期
"""
import asyncio
import base64
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
from urllib.parse import quote, urlencode
from uuid import UUID, uuid4

from playwright.async_api import Browser, BrowserContext, Page, async_playwright

logger = logging.getLogger(__name__)


def _get_meituan_login_url() -> str:
    """构造美团开店宝登录 URL（含 epassportParams，支持二维码登录）"""
    ts = int(time.time() * 1000)
    passport_params = {
        "bg_source": "1",
        "service": "com.sankuai.meishi.fe.ecom",
        "part_type": "0",
        "feconfig": "bssoify",
        "biz_line": "1",
        "continue": (
            f"https://ecom.meituan.com/bizaccount/biz-choice.html?"
            f"redirect_uri=https%3A%2F%2Fecom.meituan.com%2Fmeishi%2F"
            f"&_t={ts}"
            f"&target=https%3A%2F%2Fecom.meituan.com%2Fmeishi%2F"
            f"&leftBottomLink="
            f"&signUpTarget=self"
        ),
    }
    return (
        f"https://ecom.meituan.com/bizaccount/login.html"
        f"?loginByPhoneNumber=true&isProduction=true"
        f"&epassportParams={quote(urlencode(passport_params), safe='')}"
    )


# 反检测 JS（隐藏 Playwright 自动化特征）
STEALTH_JS = """
// 1. 隐藏 webdriver 标记（最关键）
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

// 2. 伪装 Chrome 对象
if (!window.chrome) window.chrome = {};
window.chrome.runtime = { connect: function(){}, sendMessage: function(){} };

// 3. 覆盖 permissions query
const originalQuery = window.navigator.permissions.query;
window.navigator.permissions.query = (parameters) =>
    parameters.name === 'notifications'
        ? Promise.resolve({ state: Notification.permission })
        : originalQuery(parameters);

// 4. 伪装 plugins
Object.defineProperty(navigator, 'plugins', {
    get: () => {
        const plugins = [
            { name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer', description: 'Portable Document Format' },
            { name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai', description: '' },
            { name: 'Native Client', filename: 'internal-nacl-plugin', description: '' },
        ];
        plugins.length = 3;
        return plugins;
    },
});

// 5. 伪装 languages
Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en'] });

// 6. 修复 platform（Playwright 有时会暴露 Linux）
Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });

// 7. 隐藏 Playwright 特有属性
delete window.__playwright;
delete window.__pw_manual;
"""


# 平台登录页配置
PLATFORM_CONFIG = {
    "meituan": {
        "login_url": _get_meituan_login_url,  # 动态生成（含时间戳）
        "qr_selector": ".qrcode-img img, .qr-code img, canvas, [class*='qrcode'], img[src*='qrcode']",
        "success_url_pattern": "ecom.meituan.com",
        "check_logged_in": ".user-info, .merchant-name, [class*='header'] [class*='name']",
        "cookie_domain": ".meituan.com",
        "viewport": {"width": 1280, "height": 800},
    },
    "douyin": {
        "login_url": "https://life.douyin.com/p/login",
        "qr_selector": ".qrcode-img img, .qr-code img, canvas, [class*='qrcode'], img[src*='qrcode']",
        "success_url_pattern": "life.douyin.com",
        "check_logged_in": ".merchant-name, .user-avatar, [class*='header'] [class*='name']",
        "cookie_domain": ".douyin.com",
        "viewport": {"width": 1280, "height": 800},
    },
}

# 最大超时时间（秒）
QR_LOGIN_TIMEOUT = 120


@dataclass
class QRLoginTask:
    """二维码登录任务"""

    task_id: str = field(default_factory=lambda: str(uuid4()))
    user_id: str = ""
    platform: str = ""
    status: str = "pending"  # pending, waiting_scan, scanning, success, failed, expired, cancelled
    qr_image_base64: str = ""
    cookies: dict = field(default_factory=dict)
    platform_username: str = ""
    error_message: str = ""
    created_at: float = field(default_factory=time.time)
    expires_at: float = 0
    browser: Optional[Browser] = None
    context: Optional[BrowserContext] = None
    page: Optional[Page] = None
    playwright_instance: Any = None
    _lock: Optional[asyncio.Lock] = None

    def __post_init__(self):
        self.expires_at = self.created_at + QR_LOGIN_TIMEOUT
        self._lock = asyncio.Lock()


class QRLoginService:
    """
    二维码登录服务（单例）
    管理所有活跃的二维码登录任务
    """

    _instance = None
    _tasks: dict[str, QRLoginTask] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tasks = {}
        return cls._instance

    @classmethod
    def get_instance(cls) -> "QRLoginService":
        return cls()

    def _cleanup_expired(self):
        """清理过期任务"""
        now = time.time()
        expired = [tid for tid, task in self._tasks.items() if task.expires_at < now]
        for tid in expired:
            asyncio.create_task(self._cancel_task(tid))

    async def start_login(self, user_id: str, platform: str) -> dict:
        """
        启动二维码登录流程

        Args:
            user_id: 用户ID
            platform: 平台名称 (meituan / douyin)

        Returns:
            dict: {task_id, qr_image, status}
        """
        self._cleanup_expired()

        if platform not in PLATFORM_CONFIG:
            return {"success": False, "error": f"不支持的平台: {platform}"}

        task = QRLoginTask(user_id=user_id, platform=platform)
        config = PLATFORM_CONFIG[platform]

        try:
            task.playwright_instance = await async_playwright().start()

            config = PLATFORM_CONFIG[platform]
            # 登录 URL：支持动态生成（如美团的 epassportParams）
            login_url = config["login_url"]() if callable(config["login_url"]) else config["login_url"]

            # 使用 Chrome channel，带反检测启动参数
            browser_type = task.playwright_instance.chromium
            task.browser = await browser_type.launch(
                headless=True,
                channel="chrome",
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-infobars",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--disable-extensions",
                    "--disable-component-extensions-with-background-pages",
                    "--disable-default-apps",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--lang=zh-CN",
                ],
            )

            task.context = await task.browser.new_context(
                viewport=config["viewport"],
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/131.0.0.0 Safari/537.36"
                ),
                locale="zh-CN",
                timezone_id="Asia/Shanghai",
                extra_http_headers={
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                },
            )

            # 注入反检测脚本（对所有新页面生效）
            await task.context.add_init_script(STEALTH_JS)

            task.page = await task.context.new_page()

            # 打开登录页
            logger.info(f"[QR Login] Opening {platform} login page: {login_url}")
            await task.page.goto(login_url, wait_until="domcontentloaded", timeout=30000)

            # 等待二维码等动态内容加载
            await asyncio.sleep(2)

            # 尝试多种选择器找到二维码
            qr_image = await self._capture_qr_code(task.page, config["qr_selector"])

            if not qr_image:
                # 兜底：截取整个登录页面区域
                qr_image = await self._capture_login_area(task.page)

            task.qr_image_base64 = qr_image
            task.status = "waiting_scan"
            self._tasks[task.task_id] = task

            # 启动后台轮询检测登录状态
            asyncio.create_task(self._poll_login_status(task))

            logger.info(f"[QR Login] Task {task.task_id} started for {platform}")

            return {
                "success": True,
                "task_id": task.task_id,
                "qr_image": task.qr_image_base64,
                "status": "waiting_scan",
                "expires_in": QR_LOGIN_TIMEOUT,
            }

        except Exception as e:
            logger.error(f"[QR Login] Failed to start: {e}")
            await self._cleanup_task_resources(task)
            return {"success": False, "error": f"启动登录失败: {str(e)}"}

    async def get_status(self, task_id: str) -> dict:
        """
        查询登录状态（供前端轮询）

        Returns:
            dict: {status, cookies, platform_username, error_message}
        """
        task = self._tasks.get(task_id)
        if not task:
            return {"status": "not_found", "error": "任务不存在或已过期"}

        result = {
            "status": task.status,
            "task_id": task.task_id,
            "platform": task.platform,
            "remaining_seconds": max(0, int(task.expires_at - time.time())),
        }

        if task.status == "success":
            result["cookies"] = task.cookies
            result["platform_username"] = task.platform_username
            # 登录成功后清理资源，但保留任务供前端查询
            await self._cleanup_task_resources(task)

        elif task.status == "failed":
            result["error_message"] = task.error_message
            await self._cleanup_task_resources(task)

        elif task.status == "expired":
            await self._cleanup_task_resources(task)

        return result

    async def cancel_login(self, task_id: str) -> dict:
        """取消登录任务"""
        task = self._tasks.get(task_id)
        if not task:
            return {"success": False, "error": "任务不存在"}

        await self._cancel_task(task_id)
        return {"success": True, "message": "已取消"}

    async def _poll_login_status(self, task: QRLoginTask):
        """
        后台轮询检测登录状态
        每隔 2 秒检查一次，最多轮询 QR_LOGIN_TIMEOUT / 2 次
        """
        config = PLATFORM_CONFIG[task.platform]
        check_interval = 2
        max_checks = QR_LOGIN_TIMEOUT // check_interval

        for i in range(max_checks):
            if task.status in ("success", "failed", "cancelled", "expired"):
                return

            try:
                if not task.page or task.page.is_closed():
                    task.status = "failed"
                    task.error_message = "浏览器页面已关闭"
                    return

                current_url = task.page.url

                # 检查是否登录成功（URL 变化或出现登录成功标识）
                logged_in = False

                # 方式1：检查 URL 是否跳转到主页面
                if config["success_url_pattern"] in current_url:
                    logged_in = True

                # 方式2：检查页面是否出现已登录标识
                if not logged_in:
                    try:
                        indicator = await task.page.wait_for_selector(
                            config["check_logged_in"], timeout=1000
                        )
                        if indicator:
                            logged_in = True
                    except Exception:
                        pass

                if logged_in:
                    logger.info(f"[QR Login] Task {task.task_id} login detected!")

                    # 等待页面完全加载，确保 cookie 完整
                    await asyncio.sleep(3)

                    # 使用 storage_state 导出完整登录态（与 CPA export_auth_state 一致）
                    storage_state = await task.context.storage_state(indexed_db=True)
                    cookies_list = storage_state.get("cookies", [])

                    task.cookies = {
                        c["name"]: c["value"]
                        for c in cookies_list
                        if config["cookie_domain"] in c.get("domain", "")
                    }

                    # 同时保存完整 storage_state 到 cookies 字段的 _storage_state 键（供爬虫使用）
                    task.cookies["_storage_state"] = storage_state

                    if task.cookies:
                        # 尝试提取用户名
                        task.platform_username = await self._extract_username(task.page)
                        task.status = "success"
                        logger.info(
                            f"[QR Login] Task {task.task_id} success! "
                            f"Got {len(task.cookies)} cookies, username: {task.platform_username}"
                        )
                    else:
                        task.status = "failed"
                        task.error_message = "登录成功但未获取到 cookies"
                        logger.warning(f"[QR Login] Task {task.task_id} no cookies captured")
                    return

                # 检查是否超时
                if time.time() > task.expires_at:
                    task.status = "expired"
                    task.error_message = "二维码已过期"
                    logger.info(f"[QR Login] Task {task.task_id} expired")
                    await self._cleanup_task_resources(task)
                    return

            except Exception as e:
                logger.warning(f"[QR Login] Poll error for {task.task_id}: {e}")
                if i % 10 == 0:
                    # 每 20 秒尝试恢复
                    try:
                        if task.page and not task.page.is_closed():
                            await task.page.reload(timeout=15000)
                    except Exception:
                        task.status = "failed"
                        task.error_message = "浏览器连接异常"
                        return

            await asyncio.sleep(check_interval)

        # 超过最大轮询次数
        task.status = "expired"
        task.error_message = "二维码已过期，请重新获取"
        await self._cleanup_task_resources(task)

    async def _capture_qr_code(self, page: Page, selectors: str) -> str:
        """
        尝试多种选择器截取二维码图片

        Returns:
            base64 编码的图片字符串（不含 data: 前缀）
        """
        selector_list = [s.strip() for s in selectors.split(",")]

        for selector in selector_list:
            try:
                element = await page.wait_for_selector(selector, timeout=5000)
                if element:
                    # 优先尝试直接获取 img src
                    tag_name = await element.evaluate("el => el.tagName.toLowerCase()")

                    if tag_name == "img":
                        src = await element.get_attribute("src")
                        if src:
                            if src.startswith("data:image"):
                                return src.split(",", 1)[1] if "," in src else src
                            # 如果是 URL，截图元素
                            screenshot = await element.screenshot(type="png")
                            return base64.b64encode(screenshot).decode()

                    if tag_name == "canvas":
                        # Canvas 元素，获取 data URL
                        data_url = await element.evaluate(
                            "el => el.toDataURL('image/png')"
                        )
                        if data_url and "," in data_url:
                            return data_url.split(",", 1)[1]

                    # 其他元素，直接截图
                    screenshot = await element.screenshot(type="png")
                    return base64.b64encode(screenshot).decode()

            except Exception:
                continue

        return ""

    async def _capture_login_area(self, page: Page) -> str:
        """
        兜底方案：截取登录页面的主要区域作为二维码展示
        """
        try:
            # 等待页面主体加载
            await page.wait_for_load_state("domcontentloaded")
            await asyncio.sleep(1)

            # 截取整个可见页面
            screenshot = await page.screenshot(type="png", full_page=False)
            return base64.b64encode(screenshot).decode()

        except Exception as e:
            logger.error(f"Failed to capture login area: {e}")
            return ""

    async def _extract_username(self, page: Page) -> str:
        """尝试从页面提取用户名"""
        selectors = [
            ".user-name", ".merchant-name", ".nickname",
            "[class*='user'] [class*='name']", ".header-name",
        ]
        for sel in selectors:
            try:
                element = await page.wait_for_selector(sel, timeout=2000)
                if element:
                    text = (await element.text_content() or "").strip()
                    if text:
                        return text[:50]
            except Exception:
                continue
        return ""

    async def _cancel_task(self, task_id: str):
        """取消并清理任务"""
        task = self._tasks.pop(task_id, None)
        if task:
            task.status = "cancelled"
            await self._cleanup_task_resources(task)

    async def _cleanup_task_resources(self, task: QRLoginTask):
        """清理任务资源（浏览器等）"""
        try:
            if task.context:
                await task.context.close()
            if task.browser:
                await task.browser.close()
            if task.playwright_instance:
                await task.playwright_instance.stop()
        except Exception as e:
            logger.warning(f"Error cleaning up task {task.task_id}: {e}")

        task.context = None
        task.browser = None
        task.playwright_instance = None
        task.page = None

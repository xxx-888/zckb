"""
二维码登录服务
管理 Playwright 浏览器实例，处理平台扫码登录的完整生命周期

关键：Windows 下 uvicorn 的事件循环可能不支持 subprocess，
Playwright 需要创建子进程启动浏览器，因此所有 Playwright 操作
都在独立线程的专属事件循环中执行（通过 _PlaywrightBridge 桥接）。
"""
import asyncio
import base64
import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
from urllib.parse import quote, urlencode
from uuid import UUID, uuid4

from playwright.async_api import Browser, BrowserContext, Page, async_playwright

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# Playwright 跨线程桥接（解决 Windows subprocess NotImplementedError）
# ═══════════════════════════════════════════════════════════════

class _PlaywrightBridge:
    """
    在独立线程中运行一个专属 asyncio 事件循环，
    所有 Playwright 子进程 I/O 都在这个循环上完成。
    主线程通过 run_coroutine_threadsafe + wrap_future 桥接。
    """

    _loop: Optional[asyncio.AbstractEventLoop] = None
    _thread: Optional[threading.Thread] = None
    _ready = threading.Event()

    # ── 生命周期 ──

    @classmethod
    def ensure(cls):
        """确保后台线程已启动"""
        if cls._thread is not None and cls._thread.is_alive():
            return
        cls._ready.clear()
        cls._thread = threading.Thread(target=cls._run, daemon=True, name="pw-bridge")
        cls._thread.start()
        cls._ready.wait(timeout=10)

    @classmethod
    def _run(cls):
        cls._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls._loop)
        cls._ready.set()
        cls._loop.run_forever()

    @classmethod
    def stop(cls):
        if cls._loop and cls._loop.is_running():
            cls._loop.call_soon_threadsafe(cls._loop.stop)
        if cls._thread:
            cls._thread.join(timeout=5)
        cls._loop = None
        cls._thread = None

    # ── 调用接口 ──

    @classmethod
    async def call(cls, coro):
        """
        在 Playwright 线程上执行协程，返回结果。
        用法:  await _PlaywrightBridge.call(page.goto(url, ...))
        """
        cls.ensure()
        future = asyncio.run_coroutine_threadsafe(coro, cls._loop)
        return await asyncio.wrap_future(future)

    @classmethod
    def call_later(cls, coro):
        """在 Playwright 线程上调度协程（fire-and-forget，用于后台轮询）"""
        cls.ensure()
        asyncio.run_coroutine_threadsafe(coro, cls._loop)


# ═══════════════════════════════════════════════════════════════
# 平台配置
# ═══════════════════════════════════════════════════════════════

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


# 反检测 JS（隐藏 Playwright 自动化特征，与 CPA export_auth_state 一致）
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

QR_LOGIN_TIMEOUT = 120


# ═══════════════════════════════════════════════════════════════
# 数据类
# ═══════════════════════════════════════════════════════════════

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

    def __post_init__(self):
        self.expires_at = self.created_at + QR_LOGIN_TIMEOUT


# ═══════════════════════════════════════════════════════════════
# 核心服务
# ═══════════════════════════════════════════════════════════════

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
            self._schedule_cancel(tid)

    def _schedule_cancel(self, task_id: str):
        """在主线程调度取消任务（后台轮询也需要从主线程发起到 pw 线程）"""
        asyncio.create_task(self._cancel_task(task_id))

    # ── 公开接口 ──

    async def start_login(self, user_id: str, platform: str) -> dict:
        """
        启动二维码登录流程。
        所有 Playwright 操作通过 _PlaywrightBridge 在独立线程执行。
        """
        self._cleanup_expired()

        if platform not in PLATFORM_CONFIG:
            return {"success": False, "error": f"不支持的平台: {platform}"}

        task = QRLoginTask(user_id=user_id, platform=platform)
        config = PLATFORM_CONFIG[platform]

        try:
            # ── 所有 Playwright I/O 通过 bridge 执行 ──
            task.playwright_instance = await _PlaywrightBridge.call(
                async_playwright().start()
            )

            login_url = config["login_url"]() if callable(config["login_url"]) else config["login_url"]

            browser_type = task.playwright_instance.chromium
            task.browser = await _PlaywrightBridge.call(
                browser_type.launch(
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
            )

            task.context = await _PlaywrightBridge.call(
                task.browser.new_context(
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
            )

            await _PlaywrightBridge.call(task.context.add_init_script(STEALTH_JS))
            task.page = await _PlaywrightBridge.call(task.context.new_page())

            logger.info(f"[QR Login] Opening {platform} login page: {login_url}")
            await _PlaywrightBridge.call(
                task.page.goto(login_url, wait_until="domcontentloaded", timeout=30000)
            )

            # 等待二维码等动态内容加载
            await asyncio.sleep(2)

            # 截取二维码
            qr_image = await _PlaywrightBridge.call(
                self._capture_qr_code(task.page, config["qr_selector"])
            )
            if not qr_image:
                qr_image = await _PlaywrightBridge.call(
                    self._capture_login_area(task.page)
                )

            task.qr_image_base64 = qr_image
            task.status = "waiting_scan"
            self._tasks[task.task_id] = task

            # 启动后台轮询（在 pw 线程上执行，避免跨线程 Playwright 调用）
            _PlaywrightBridge.call_later(self._poll_login_status(task))

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
        """查询登录状态（供前端轮询）"""
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
            await self._cleanup_task_resources(task)
        elif task.status in ("failed", "expired"):
            result["error_message"] = task.error_message
            await self._cleanup_task_resources(task)

        return result

    async def cancel_login(self, task_id: str) -> dict:
        """取消登录任务"""
        task = self._tasks.get(task_id)
        if not task:
            return {"success": False, "error": "任务不存在"}
        await self._cancel_task(task_id)
        return {"success": True, "message": "已取消"}

    # ── 后台轮询（在 Playwright 线程的事件循环中执行）──

    async def _poll_login_status(self, task: QRLoginTask):
        """后台轮询检测登录状态，运行在 pw 线程"""
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

                logged_in = False

                # 方式1：URL 跳转检测
                if config["success_url_pattern"] in current_url:
                    logged_in = True

                # 方式2：DOM 元素检测
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
                    await asyncio.sleep(3)  # 等待 cookie 完整加载

                    # 导出 storage_state
                    storage_state = await task.context.storage_state(indexed_db=True)
                    cookies_list = storage_state.get("cookies", [])

                    task.cookies = {
                        c["name"]: c["value"]
                        for c in cookies_list
                        if config["cookie_domain"] in c.get("domain", "")
                    }
                    task.cookies["_storage_state"] = storage_state

                    if task.cookies:
                        task.platform_username = await self._extract_username(task.page)
                        task.status = "success"
                        logger.info(
                            f"[QR Login] Task {task.task_id} success! "
                            f"Got {len(task.cookies)} cookies, username: {task.platform_username}"
                        )
                    else:
                        task.status = "failed"
                        task.error_message = "登录成功但未获取到 cookies"
                    return

                # 超时检查
                if time.time() > task.expires_at:
                    task.status = "expired"
                    task.error_message = "二维码已过期"
                    logger.info(f"[QR Login] Task {task.task_id} expired")
                    await self._cleanup_task_resources(task)
                    return

            except Exception as e:
                logger.warning(f"[QR Login] Poll error for {task.task_id}: {e}")
                if i % 10 == 0:
                    try:
                        if task.page and not task.page.is_closed():
                            await task.page.reload(timeout=15000)
                    except Exception:
                        task.status = "failed"
                        task.error_message = "浏览器连接异常"
                        return

            await asyncio.sleep(check_interval)

        task.status = "expired"
        task.error_message = "二维码已过期，请重新获取"
        await self._cleanup_task_resources(task)

    # ── Playwright 辅助方法（也在 pw 线程上下文中调用）──

    async def _capture_qr_code(self, page: Page, selectors: str) -> str:
        """尝试多种选择器截取二维码图片"""
        selector_list = [s.strip() for s in selectors.split(",")]

        for selector in selector_list:
            try:
                element = await page.wait_for_selector(selector, timeout=5000)
                if element:
                    tag_name = await element.evaluate("el => el.tagName.toLowerCase()")

                    if tag_name == "img":
                        src = await element.get_attribute("src")
                        if src:
                            if src.startswith("data:image"):
                                return src.split(",", 1)[1] if "," in src else src
                            screenshot = await element.screenshot(type="png")
                            return base64.b64encode(screenshot).decode()

                    if tag_name == "canvas":
                        data_url = await element.evaluate("el => el.toDataURL('image/png')")
                        if data_url and "," in data_url:
                            return data_url.split(",", 1)[1]

                    screenshot = await element.screenshot(type="png")
                    return base64.b64encode(screenshot).decode()

            except Exception:
                continue

        return ""

    async def _capture_login_area(self, page: Page) -> str:
        """兜底：截取整个登录页面"""
        try:
            await page.wait_for_load_state("domcontentloaded")
            await asyncio.sleep(1)
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

    # ── 资源清理 ──

    async def _cancel_task(self, task_id: str):
        """取消并清理任务"""
        task = self._tasks.pop(task_id, None)
        if task:
            task.status = "cancelled"
            await self._cleanup_task_resources(task)

    async def _cleanup_task_resources(self, task: QRLoginTask):
        """清理浏览器资源（通过 bridge 在 pw 线程执行）"""
        try:
            if task.context:
                await _PlaywrightBridge.call(task.context.close())
            if task.browser:
                await _PlaywrightBridge.call(task.browser.close())
            if task.playwright_instance:
                await _PlaywrightBridge.call(task.playwright_instance.stop())
        except Exception as e:
            logger.warning(f"Error cleaning up task {task.task_id}: {e}")

        task.context = None
        task.browser = None
        task.playwright_instance = None
        task.page = None

"""
二维码登录服务
使用 sync_playwright 在独立线程中运行，避免 Windows 下
uvicorn asyncio 事件循环不支持 subprocess 的问题。

架构：
  asyncio.to_thread → _sync_start_login（启动浏览器+截图，立即返回）
                   → threading.Thread → _sync_poll_login（后台轮询，阻塞）
"""
import asyncio
import base64
import logging
import os
import threading
import time
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import quote, urlencode
from uuid import uuid4

from playwright.sync_api import (
    Browser, BrowserContext, Page, sync_playwright,
)

logger = logging.getLogger(__name__)

# 是否 headless（设环境变量 HEADLESS=false 可弹出浏览器调试）
HEADLESS = os.getenv("QR_HEADLESS", "true").lower() in ("true", "1", "yes")


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


STEALTH_JS = """
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
if (!window.chrome) window.chrome = {};
window.chrome.runtime = { connect: function(){}, sendMessage: function(){} };
const originalQuery = window.navigator.permissions.query;
window.navigator.permissions.query = (parameters) =>
    parameters.name === 'notifications'
        ? Promise.resolve({ state: Notification.permission })
        : originalQuery(parameters);
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
Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en'] });
Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
delete window.__playwright;
delete window.__pw_manual;
"""

PLATFORM_CONFIG = {
    "meituan": {
        "login_url": _get_meituan_login_url,
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
    status: str = "pending"
    qr_image_base64: str = ""
    cookies: dict = field(default_factory=dict)
    platform_username: str = ""
    error_message: str = ""
    created_at: float = field(default_factory=time.time)
    expires_at: float = 0

    def __post_init__(self):
        self.expires_at = self.created_at + QR_LOGIN_TIMEOUT


# ═══════════════════════════════════════════════════════════════
# 核心服务
# ═══════════════════════════════════════════════════════════════

class QRLoginService:
    """二维码登录服务（单例）"""

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
        now = time.time()
        expired = [tid for tid, t in self._tasks.items() if t.expires_at < now]
        for tid in expired:
            task = self._tasks.pop(tid, None)
            if task:
                task.status = "expired"
                task.error_message = "二维码已过期"

    # ── 公开接口（async，内部用 to_thread 调用 sync） ──

    async def start_login(self, user_id: str, platform: str) -> dict:
        self._cleanup_expired()

        if platform not in PLATFORM_CONFIG:
            return {"success": False, "error": f"不支持的平台: {platform}"}

        task = QRLoginTask(user_id=user_id, platform=platform)
        self._tasks[task.task_id] = task

        try:
            # 第一步：在线程中启动浏览器+截图（阻塞但快速，约 10-15 秒）
            result = await asyncio.to_thread(
                self._sync_start_login, task, platform
            )
            if not result.get("success"):
                self._tasks.pop(task.task_id, None)
                return result

            # 第二步：截图成功后，启动后台线程轮询登录状态（不阻塞当前请求）
            poll_thread = threading.Thread(
                target=self._sync_poll_login,
                args=(task,),
                daemon=True,
                name=f"qr-poll-{task.task_id[:8]}",
            )
            task._poll_thread = poll_thread  # type: ignore
            poll_thread.start()

            return result

        except Exception as e:
            logger.error(f"[QR Login] start_login error: {e}")
            self._tasks.pop(task.task_id, None)
            return {"success": False, "error": str(e)}

    async def get_status(self, task_id: str) -> dict:
        task = self._tasks.get(task_id)
        if not task:
            return {"status": "not_found", "error": "任务不存在或已过期"}

        result = {
            "status": task.status,
            "platform": task.platform,
            "remaining_seconds": max(0, int(task.expires_at - time.time())),
        }

        if task.status == "success":
            result["cookies"] = task.cookies
            result["platform_username"] = task.platform_username
            self._tasks.pop(task_id, None)
        elif task.status in ("failed", "expired"):
            result["error_message"] = task.error_message
            self._tasks.pop(task_id, None)

        return result

    async def cancel_login(self, task_id: str) -> dict:
        task = self._tasks.pop(task_id, None)
        if task:
            task.status = "cancelled"
            task._stop_event = True  # type: ignore
        return {"success": True, "message": "已取消"}

    # ── Sync Playwright 实现（在线程池中运行） ──

    def _sync_start_login(self, task: QRLoginTask, platform: str) -> dict:
        """在独立线程中用 sync_playwright 启动浏览器并截取二维码"""
        # 添加停止事件供 cancel 使用
        task._stop_event = False  # type: ignore
        task._browser = None  # type: ignore
        task._context = None  # type: ignore
        task._page = None  # type: ignore

        try:
            pw = sync_playwright().start()

            config = PLATFORM_CONFIG[platform]
            login_url = config["login_url"]() if callable(config["login_url"]) else config["login_url"]

            logger.info(f"[QR Login] Launching browser (headless={HEADLESS}) for {platform}")

            # 尝试使用系统 Chrome，失败则回退到 Chromium
            browser = None
            try:
                browser = pw.chromium.launch(
                    headless=HEADLESS,
                    channel="chrome",
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--disable-infobars",
                        "--no-first-run",
                        "--no-default-browser-check",
                        "--disable-extensions",
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-gpu",
                        "--lang=zh-CN",
                    ],
                )
                logger.info("[QR Login] Using system Chrome")
            except Exception as e:
                logger.warning(f"[QR Login] Chrome channel failed ({e}), falling back to Chromium")
                browser = pw.chromium.launch(
                    headless=HEADLESS,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--disable-infobars",
                        "--no-first-run",
                        "--no-default-browser-check",
                        "--disable-extensions",
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-gpu",
                        "--lang=zh-CN",
                    ],
                )

            context = browser.new_context(
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
            context.add_init_script(STEALTH_JS)

            page = context.new_page()

            # 保存引用供 cancel 清理
            task._browser = browser  # type: ignore
            task._context = context  # type: ignore
            task._page = page  # type: ignore
            task._pw = pw  # type: ignore

            logger.info(f"[QR Login] Opening {platform}: {login_url[:80]}...")
            page.goto(login_url, wait_until="domcontentloaded", timeout=30000)

            # 等待页面加载
            page.wait_for_timeout(3000)

            # 截取二维码
            qr_image = self._sync_capture_qr_code(page, config["qr_selector"])
            if not qr_image:
                logger.info("[QR Login] No QR element found, capturing full page")
                qr_image = self._sync_capture_login_area(page)

            task.qr_image_base64 = qr_image
            task.status = "waiting_scan"

            logger.info(f"[QR Login] Task {task.task_id} waiting for scan, qr_image len={len(qr_image)}")

            # 注意：不在这里调 _sync_poll_login！轮询由 start_login 启动的独立线程执行
            return {
                "success": True,
                "task_id": task.task_id,
                "qr_image": task.qr_image_base64,
                "status": task.status,
                "expires_in": QR_LOGIN_TIMEOUT,
            }

        except Exception as e:
            logger.error(f"[QR Login] _sync_start_login error: {e}")
            self._sync_cleanup(task)
            return {"success": False, "error": str(e)}

    def _sync_poll_login(self, task: QRLoginTask):
        """Sync 轮询登录状态（阻塞在线程中，配合 to_thread）"""
        config = PLATFORM_CONFIG[task.platform]
        check_interval = 3
        max_checks = QR_LOGIN_TIMEOUT // check_interval

        page = getattr(task, '_page', None)
        context = getattr(task, '_context', None)

        for i in range(max_checks):
            # 检查取消
            if getattr(task, '_stop_event', False):
                return

            try:
                if not page or page.is_closed():
                    task.status = "failed"
                    task.error_message = "浏览器页面已关闭"
                    return

                current_url = page.url
                logged_in = False

                # URL 跳转检测
                if config["success_url_pattern"] in current_url and "login" not in current_url:
                    logged_in = True

                # DOM 元素检测
                if not logged_in:
                    try:
                        indicator = page.wait_for_selector(
                            config["check_logged_in"], timeout=1000
                        )
                        if indicator:
                            logged_in = True
                    except Exception:
                        pass

                if logged_in:
                    logger.info(f"[QR Login] Task {task.task_id} login detected!")
                    page.wait_for_timeout(3000)

                    # 导出 storage_state
                    storage_state = context.storage_state(indexed_db=True)
                    cookies_list = storage_state.get("cookies", [])

                    task.cookies = {
                        c["name"]: c["value"]
                        for c in cookies_list
                        if config["cookie_domain"] in c.get("domain", "")
                    }
                    task.cookies["_storage_state"] = storage_state

                    if task.cookies:
                        task.platform_username = self._sync_extract_username(page)
                        task.status = "success"
                        logger.info(
                            f"[QR Login] Task {task.task_id} success! "
                            f"Cookies: {len(task.cookies)}, user: {task.platform_username}"
                        )
                    else:
                        task.status = "failed"
                        task.error_message = "登录成功但未获取到 cookies"
                    return

                if time.time() > task.expires_at:
                    task.status = "expired"
                    task.error_message = "二维码已过期"
                    logger.info(f"[QR Login] Task {task.task_id} expired")
                    return

            except Exception as e:
                logger.warning(f"[QR Login] Poll error: {e}")
                if i % 10 == 0 and page and not page.is_closed():
                    try:
                        page.reload(timeout=15000)
                    except Exception:
                        task.status = "failed"
                        task.error_message = "浏览器连接异常"
                        return

            time.sleep(check_interval)

        task.status = "expired"
        task.error_message = "二维码已过期"

    def _sync_capture_qr_code(self, page: Page, selectors: str) -> str:
        """尝试多种选择器截取二维码"""
        for selector in [s.strip() for s in selectors.split(",")]:
            try:
                element = page.wait_for_selector(selector, timeout=5000)
                if element:
                    tag_name = element.evaluate("el => el.tagName.toLowerCase()")

                    if tag_name == "img":
                        src = element.get_attribute("src")
                        if src:
                            if src.startswith("data:image"):
                                return src.split(",", 1)[1] if "," in src else src
                            screenshot = element.screenshot(type="png")
                            return base64.b64encode(screenshot).decode()

                    if tag_name == "canvas":
                        data_url = element.evaluate("el => el.toDataURL('image/png')")
                        if data_url and "," in data_url:
                            return data_url.split(",", 1)[1]

                    screenshot = element.screenshot(type="png")
                    return base64.b64encode(screenshot).decode()
            except Exception:
                continue
        return ""

    def _sync_capture_login_area(self, page: Page) -> str:
        """兜底：截取整个登录页面"""
        try:
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(1000)
            screenshot = page.screenshot(type="png", full_page=False)
            return base64.b64encode(screenshot).decode()
        except Exception as e:
            logger.error(f"[QR Login] capture_login_area error: {e}")
            return ""

    def _sync_extract_username(self, page: Page) -> str:
        """尝试从页面提取用户名"""
        selectors = [
            ".user-name", ".merchant-name", ".nickname",
            "[class*='user'] [class*='name']", ".header-name",
        ]
        for sel in selectors:
            try:
                element = page.wait_for_selector(sel, timeout=2000)
                if element:
                    text = (element.text_content() or "").strip()
                    if text:
                        return text[:50]
            except Exception:
                continue
        return ""

    def _sync_cleanup(self, task: QRLoginTask):
        """清理浏览器资源"""
        try:
            page = getattr(task, '_page', None)
            context = getattr(task, '_context', None)
            browser = getattr(task, '_browser', None)
            pw = getattr(task, '_pw', None)
            if page and not page.is_closed():
                page.close()
            if context:
                context.close()
            if browser:
                browser.close()
            if pw:
                pw.stop()
        except Exception as e:
            logger.warning(f"[QR Login] cleanup error: {e}")

        task._page = None  # type: ignore
        task._context = None  # type: ignore
        task._browser = None  # type: ignore
        task._pw = None  # type: ignore

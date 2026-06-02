"""
二维码登录服务
使用 multiprocessing 在独立进程中运行 Playwright，
彻底避免 Windows 下 asyncio 事件循环与 sync API 的冲突。

架构:
  主进程 (uvicorn asyncio)             独立进程 (Playwright sync API)
  ┌────────────────────────┐          ┌────────────────────────────┐
  │ POST /qr-login/start  │──spawn──▶│ _worker_main               │
  │   轮询 {task}_qr.json │          │   1. launch browser        │
  │   返回二维码给前端     │          │   2. 截取QR → {id}_qr.json │
  ├────────────────────────┤          │   3. 轮询登录(120s)       │
  │ GET /qr-login/status   │          │   4. 成功 → {id}_done.json│
  │   读取 {task}_done.json│          │   5. 关闭浏览器           │
  └────────────────────────┘          └────────────────────────────┘
  通信方式: JSON 文件（简单可靠，跨进程）
"""
import asyncio
import base64
import json
import logging
import multiprocessing
import os
import time
from typing import Optional
from urllib.parse import quote, urlencode
from uuid import uuid4

logger = logging.getLogger(__name__)

# 是否 headless（设环境变量 QR_HEADLESS=false 可弹出浏览器调试）
HEADLESS = os.getenv("QR_HEADLESS", "true").lower() in ("true", "1", "yes")
QR_LOGIN_TIMEOUT = 120

# IPC 目录：主进程和 worker 进程通过此目录下的 JSON 文件通信
_RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".qr_results")


# ═══════════════════════════════════════════════════════════════
# 平台配置（纯数据，无 Playwright 依赖）
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


# ═══════════════════════════════════════════════════════════════
# Worker 函数（在独立进程中运行，不依赖 asyncio）
# ═══════════════════════════════════════════════════════════════

def _worker_main(task_id: str, platform: str, headless: bool, results_dir: str):
    """
    在独立 OS 进程中运行 Playwright sync API。
    通过 JSON 文件与主进程通信：
      - {task_id}_qr.json   → 二维码截图结果
      - {task_id}_done.json → 最终结果（成功/超时/失败）
      - {task_id}_cancel    → 取消信号文件（主进程创建）
    """
    # 注意：playwright 必须在子进程内部 import，不能在主进程 import
    from playwright.sync_api import sync_playwright  # noqa: E402

    qr_file = os.path.join(results_dir, f"{task_id}_qr.json")
    done_file = os.path.join(results_dir, f"{task_id}_done.json")
    cancel_file = os.path.join(results_dir, f"{task_id}_cancel")

    config = PLATFORM_CONFIG[platform]
    login_url = config["login_url"]() if callable(config["login_url"]) else config["login_url"]

    pw = None
    browser = None
    context = None
    page = None

    try:
        pw = sync_playwright().start()

        # 尝试 Chrome，失败回退 Chromium
        try:
            browser = pw.chromium.launch(
                headless=headless,
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
        except Exception:
            browser = pw.chromium.launch(
                headless=headless,
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
        page.goto(login_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)

        # ── 截取二维码 ──
        qr_image = _capture_qr_code(page, config["qr_selector"])
        if not qr_image:
            qr_image = _capture_login_area(page)

        # 写入二维码结果（主进程会轮询此文件）
        with open(qr_file, "w", encoding="utf-8") as f:
            json.dump({
                "task_id": task_id,
                "qr_image": qr_image,
                "status": "waiting_scan",
                "expires_in": QR_LOGIN_TIMEOUT,
            }, f)

        # ── 轮询登录状态 ──
        start_time = time.time()
        check_interval = 3

        while time.time() - start_time < QR_LOGIN_TIMEOUT:
            # 检查取消信号
            if os.path.exists(cancel_file):
                _write_result(done_file, {"status": "cancelled", "platform": platform})
                return

            if not page or page.is_closed():
                _write_result(done_file, {"status": "failed", "platform": platform,
                                          "error": "浏览器页面已关闭"})
                return

            current_url = page.url
            logged_in = False

            # URL 跳转检测
            if config["success_url_pattern"] in current_url and "login" not in current_url:
                logged_in = True

            # DOM 元素检测
            if not logged_in:
                try:
                    indicator = page.wait_for_selector(config["check_logged_in"], timeout=1000)
                    if indicator:
                        logged_in = True
                except Exception:
                    pass

            if logged_in:
                page.wait_for_timeout(3000)

                # 导出完整登录态
                storage_state = context.storage_state(indexed_db=True)
                cookies_list = storage_state.get("cookies", [])

                cookies = {
                    c["name"]: c["value"]
                    for c in cookies_list
                    if config["cookie_domain"] in c.get("domain", "")
                }
                cookies["_storage_state"] = storage_state

                # 提取用户名
                username = _extract_username(page)

                _write_result(done_file, {
                    "status": "success",
                    "platform": platform,
                    "platform_username": username,
                    "cookies": cookies,
                })
                return

            time.sleep(check_interval)

        # 超时
        _write_result(done_file, {"status": "expired", "platform": platform})

    except Exception as e:
        logger.error(f"[QR Worker] {task_id} error: {e}", exc_info=True)
        # 如果还没写入 qr_file，直接写 error 到 done_file
        _write_result(done_file, {
            "status": "failed",
            "platform": platform,
            "error": str(e),
        })

    finally:
        # 清理浏览器
        try:
            if page and not page.is_closed():
                page.close()
            if context:
                context.close()
            if browser:
                browser.close()
            if pw:
                pw.stop()
        except Exception:
            pass


def _write_result(filepath: str, data: dict):
    """安全写入 JSON 结果文件"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception as e:
        logger.error(f"[QR Worker] Failed to write result to {filepath}: {e}")


def _capture_qr_code(page, selectors: str) -> str:
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


def _capture_login_area(page) -> str:
    """兜底：截取整个登录页面"""
    try:
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(1000)
        screenshot = page.screenshot(type="png", full_page=False)
        return base64.b64encode(screenshot).decode()
    except Exception:
        return ""


def _extract_username(page) -> str:
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


# ═══════════════════════════════════════════════════════════════
# 服务类（在主进程中运行，async 接口）
# ═══════════════════════════════════════════════════════════════

class QRLoginService:
    """二维码登录服务（单例）—— 通过 multiprocessing 调度 Playwright worker"""

    _instance: Optional["QRLoginService"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    @classmethod
    def get_instance(cls) -> "QRLoginService":
        return cls()

    def _ensure_init(self):
        if self._initialized:
            return
        os.makedirs(_RESULTS_DIR, exist_ok=True)
        self._processes: dict[str, multiprocessing.Process] = {}
        self._initialized = True
        self._cleanup_stale()

    def _cleanup_stale(self):
        """清理上次运行的残留文件（超过 1 小时的）"""
        now = time.time()
        try:
            for filename in os.listdir(_RESULTS_DIR):
                filepath = os.path.join(_RESULTS_DIR, filename)
                if os.path.isfile(filepath) and now - os.path.getmtime(filepath) > 3600:
                    os.remove(filepath)
        except Exception:
            pass

    def _task_file(self, task_id: str, suffix: str) -> str:
        return os.path.join(_RESULTS_DIR, f"{task_id}{suffix}")

    def _read_json(self, filepath: str) -> Optional[dict]:
        try:
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return None

    # ── 公开 async 接口 ──

    async def start_login(self, user_id: str, platform: str) -> dict:
        self._ensure_init()

        if platform not in PLATFORM_CONFIG:
            return {"success": False, "error": f"不支持的平台: {platform}"}

        task_id = str(uuid4())

        # 清除可能存在的旧文件
        for suffix in ["_qr.json", "_done.json", "_cancel"]:
            fp = self._task_file(task_id, suffix)
            if os.path.exists(fp):
                os.remove(fp)

        # 启动 worker 进程
        process = multiprocessing.Process(
            target=_worker_main,
            args=(task_id, platform, HEADLESS, _RESULTS_DIR),
            daemon=True,
            name=f"qr-{task_id[:8]}",
        )
        process.start()
        self._processes[task_id] = process
        logger.info(f"[QR Login] Started worker process pid={process.pid} for {platform}")

        # 轮询等待二维码文件（最多 30 秒）
        qr_file = self._task_file(task_id, "_qr.json")
        for _ in range(30):
            await asyncio.sleep(1)

            # 检查是否立即失败（done.json 会出现比 qr.json 更早的情况）
            done_data = self._read_json(self._task_file(task_id, "_done.json"))
            if done_data and done_data.get("status") in ("failed",):
                self._cleanup_task(task_id)
                return {"success": False, "error": done_data.get("error", "启动失败")}

            # 二维码就绪
            qr_data = self._read_json(qr_file)
            if qr_data and qr_data.get("qr_image"):
                return {"success": True, **qr_data}

        # 超时：30 秒内没拿到二维码
        self._cleanup_task(task_id)
        return {"success": False, "error": "获取二维码超时，请重试"}

    async def get_status(self, task_id: str) -> dict:
        self._ensure_init()

        # 检查最终结果
        done_data = self._read_json(self._task_file(task_id, "_done.json"))
        if done_data:
            status = done_data.get("status", "unknown")
            if status == "success":
                # 成功：返回 cookies 信息，然后清理
                self._cleanup_task(task_id)
            elif status in ("expired", "failed", "cancelled"):
                self._cleanup_task(task_id)
            return done_data

        # 检查是否还在等待扫码
        qr_data = self._read_json(self._task_file(task_id, "_qr.json"))
        if qr_data:
            elapsed = time.time() - os.path.getmtime(self._task_file(task_id, "_qr.json"))
            remaining = max(0, int(QR_LOGIN_TIMEOUT - elapsed))
            return {
                "status": "waiting_scan",
                "remaining_seconds": remaining,
            }

        return {"status": "not_found", "error": "任务不存在或已过期"}

    async def cancel_login(self, task_id: str) -> dict:
        self._ensure_init()

        # 写取消信号文件
        cancel_file = self._task_file(task_id, "_cancel")
        try:
            with open(cancel_file, "w") as f:
                f.write(str(time.time()))
        except Exception:
            pass

        # 终止进程
        self._cleanup_task(task_id)
        return {"success": True}

    def _cleanup_task(self, task_id: str):
        """终止进程并清理文件"""
        process = self._processes.pop(task_id, None)
        if process and process.is_alive():
            try:
                process.terminate()
                process.join(timeout=5)
                if process.is_alive():
                    process.kill()
            except Exception:
                pass

        for suffix in ["_qr.json", "_done.json", "_cancel"]:
            fp = self._task_file(task_id, suffix)
            if os.path.exists(fp):
                try:
                    os.remove(fp)
                except Exception:
                    pass

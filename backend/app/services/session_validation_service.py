"""
会话验证服务

验证已保存的 storage_state 是否仍然有效（会话是否过期）。
使用 multiprocessing 在独立进程中运行 Playwright，避免 asyncio 冲突。

用法:
    result = await SessionValidationService.validate(platform, storage_state_dict)
    # result: {"valid": True/False, "username": "...", "storage_state": {...}}
"""
import asyncio
import json
import logging
import multiprocessing
import os
import time
from typing import Optional

logger = logging.getLogger(__name__)

# 验证超时（秒）
_VALIDATE_TIMEOUT = 30

# IPC 目录（复用 qr_login_service 的目录）
_RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".qr_results")

# 平台验证配置
PLATFORM_VALIDATE_CONFIG = {
        "meituan": {
        # 访问需要登录的页面来验证
        "validate_url": "https://ecom.meituan.com/meishi/",
        # DOM 分析发现：用户名在 [class*='nav_infoLabel']，用户信息区在 [class*='nav_info']
        # CSS module 类名带 hash 后缀，使用 [class*='xxx'] 前缀匹配
        "check_logged_in": "[class*='nav_infoLabel'], [class*='nav_info']",
        "username_selector": "[class*='nav_infoLabel']",
        "success_url_contains": "ecom.meituan.com",
        "redirect_to_login_sign": "epassport.meituan.com",
    },
    "dianping": {
        "validate_url": "https://e.dianping.com/",
        "check_logged_in": ".user-info, .merchant-name, [class*='header'] [class*='name']",
        "success_url_contains": "e.dianping.com",
        "redirect_to_login_sign": "passport.dianping.com",
    },
    "douyin": {
        "validate_url": "https://life.douyin.com/",
        "check_logged_in": ".merchant-name, .user-avatar",
        "success_url_contains": "life.douyin.com",
        "redirect_to_login_sign": "sso.douyin.com",
    },
}

STEALTH_JS = """
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
if (!window.chrome) window.chrome = {};
window.chrome.runtime = { connect: function(){}, sendMessage: function(){} };
delete window.__playwright;
delete window.__pw_manual;
"""


# ═══════════════════════════════════════════════════════════════
# Worker 函数（独立进程）
# ═══════════════════════════════════════════════════════════════

def _validate_worker(task_id: str, platform: str, storage_state: dict, results_dir: str):
    """
    在独立进程中用 storage_state 创建浏览器 context，验证会话是否有效。

    流程:
    1. 用 storage_state 创建新 context
    2. 导航到平台需要登录的页面
    3. 检查是否被重定向到登录页（说明 session 过期）
    4. 检查页面是否存在已登录标识元素
    5. 如果有效，导出最新的 storage_state（可能包含刷新后的 cookie）
    6. 将结果写入 JSON 文件
    """
    from playwright.sync_api import sync_playwright  # noqa: E402

    done_file = os.path.join(results_dir, f"{task_id}_validate.json")

    config = PLATFORM_VALIDATE_CONFIG.get(platform)
    if not config:
        _write_validate_result(done_file, {
            "valid": False,
            "error": f"不支持的平台: {platform}",
        })
        return

    pw = None
    browser = None
    context = None
    page = None

    try:
        pw = sync_playwright().start()

        try:
            browser = pw.chromium.launch(
                headless=True,
                channel="chrome",
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--lang=zh-CN",
                ],
            )
        except Exception:
            browser = pw.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--lang=zh-CN",
                ],
            )

        # 用 storage_state 创建 context —— 这是关键步骤
        context = browser.new_context(
            storage_state=storage_state,
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
        )
        context.add_init_script(STEALTH_JS)

        page = context.new_page()

        logger.info(f"[Validate Worker] {task_id} navigating to {config['validate_url']}")
        page.goto(config["validate_url"], wait_until="domcontentloaded", timeout=20000)
        page.wait_for_timeout(3000)

        current_url = page.url
        logger.info(f"[Validate Worker] {task_id} current URL: {current_url}")

        # 检查 1: 是否被重定向到登录页
        if config["redirect_to_login_sign"] in current_url:
            logger.info(f"[Validate Worker] {task_id} redirected to login page, session expired")
            _write_validate_result(done_file, {
                "valid": False,
                "error": "会话已过期，被重定向到登录页",
                "current_url": current_url,
            })
            return

        # 检查 2: 页面是否有已登录标识元素
        logged_in = False
        for selector in config["check_logged_in"].split(","):
            selector = selector.strip()
            try:
                el = page.wait_for_selector(selector, timeout=3000)
                if el and el.is_visible():
                    logged_in = True
                    break
            except Exception:
                continue

        if not logged_in:
            # 即使没有找到登录标识，如果 URL 没被重定向到登录页，也可能有效
            # 再宽松检查：URL 包含目标域名且不含 login
            if config["success_url_contains"] in current_url and "login" not in current_url.lower():
                logged_in = True
                logger.info(f"[Validate Worker] {task_id} no login indicator found, but URL is valid")

        if not logged_in:
            logger.info(f"[Validate Worker] {task_id} no login indicator, session expired")
            _write_validate_result(done_file, {
                "valid": False,
                "error": "页面未检测到登录状态",
                "current_url": current_url,
            })
            return

        # 登录有效！提取用户名
        username = ""
        # 优先使用平台配置中的专用 username_selector
        username_selectors = []
        if config.get("username_selector"):
            username_selectors.insert(0, config["username_selector"])
        # 通用兜底选择器
        username_selectors.extend([
            ".user-name", ".merchant-name", ".nickname",
            "[class*='user'] [class*='name']", ".header-name",
        ])
        for sel in username_selectors:
            try:
                el = page.wait_for_selector(sel, timeout=2000)
                if el:
                    text = (el.text_content() or "").strip()
                    if text:
                        username = text[:50]
                        break
            except Exception:
                continue

        # 导出最新的 storage_state（可能包含刷新后的 cookie）
        try:
            new_storage_state = context.storage_state(indexed_db=True)
        except Exception as e:
            logger.warning(f"[Validate Worker] {task_id} failed to export storage_state: {e}")
            new_storage_state = storage_state

        logger.info(f"[Validate Worker] {task_id} session VALID, username={username}")
        _write_validate_result(done_file, {
            "valid": True,
            "username": username,
            "current_url": current_url,
            "storage_state": new_storage_state,
        })

    except Exception as e:
        logger.error(f"[Validate Worker] {task_id} error: {e}", exc_info=True)
        _write_validate_result(done_file, {
            "valid": False,
            "error": str(e),
        })

    finally:
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


def _write_validate_result(filepath: str, data: dict):
    """写入验证结果 JSON"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception as e:
        logger.error(f"[Validate Worker] Failed to write result: {e}")


# ═══════════════════════════════════════════════════════════════
# 服务类（主进程 async 接口）
# ═══════════════════════════════════════════════════════════════

class SessionValidationService:
    """会话验证服务（单例）"""

    _instance: Optional["SessionValidationService"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    @classmethod
    def get_instance(cls) -> "SessionValidationService":
        return cls()

    def _ensure_init(self):
        if self._initialized:
            return
        os.makedirs(_RESULTS_DIR, exist_ok=True)
        self._processes: dict = {}
        self._initialized = True

    def _read_json(self, filepath: str) -> Optional[dict]:
        try:
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return None

    async def validate(self, platform: str, storage_state: dict) -> dict:
        """
        验证 storage_state 对应的会话是否仍然有效。

        Args:
            platform: 平台名称
            storage_state: Playwright storage_state dict

        Returns:
            dict: {
                "valid": True/False,
                "username": "..." (optional),
                "storage_state": {...} (optional, 仅 valid=True 时返回最新状态),
                "error": "..." (optional, 仅 valid=False 时)
            }
        """
        self._ensure_init()

        if platform not in PLATFORM_VALIDATE_CONFIG:
            return {"valid": False, "error": f"不支持的平台: {platform}"}

        task_id = f"val_{int(time.time() * 1000)}"
        done_file = os.path.join(_RESULTS_DIR, f"{task_id}_validate.json")

        # 清除可能存在的旧结果
        if os.path.exists(done_file):
            os.remove(done_file)

        # 启动验证 worker 进程
        process = multiprocessing.Process(
            target=_validate_worker,
            args=(task_id, platform, storage_state, _RESULTS_DIR),
            daemon=True,
            name=f"validate-{task_id[:8]}",
        )
        process.start()
        self._processes[task_id] = process
        logger.info(f"[Session Validate] started worker pid={process.pid} for {platform}")

        # 轮询等待结果
        for _ in range(_VALIDATE_TIMEOUT):
            await asyncio.sleep(1)

            result = self._read_json(done_file)
            if result:
                self._cleanup(task_id, done_file)
                return result

        # 超时
        self._cleanup(task_id, done_file)
        return {"valid": False, "error": "验证超时"}

    def _cleanup(self, task_id: str, done_file: str):
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

        if os.path.exists(done_file):
            try:
                os.remove(done_file)
            except Exception:
                pass

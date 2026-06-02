"""
短信验证码登录服务
用于抖音来客等平台通过手机号+验证码方式获取登录态。
复用 multiprocessing + JSON IPC 模式，与 qr_login_service 架构一致。

流程:
  1. sms_start: 启动浏览器 → 打开登录页 → 填入手机号 → 点击"发送验证码" → 返回 task_id
  2. sms_verify: 填入验证码 → 点击"登录/确认" → 等待跳转 → 导出 storage_state → 返回结果
"""
import asyncio
import base64
import json
import logging
import multiprocessing
import os
import time
from typing import Optional
from uuid import uuid4

logger = logging.getLogger(__name__)

# IPC 目录（复用 qr_login_service 的目录）
_RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".qr_results")

STEALTH_JS = """
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
if (!window.chrome) window.chrome = {};
window.chrome.runtime = { connect: function(){}, sendMessage: function(){} };
delete window.__playwright;
delete window.__pw_manual;
"""


# ═══════════════════════════════════════════════════════════════
# 平台 SMS 登录配置
# ═══════════════════════════════════════════════════════════════

PLATFORM_SMS_CONFIG = {
    "douyin": {
        "login_url": "https://life.douyin.com/login",
        "phone_input_selector": "input[type='tel'], input[placeholder*='手机号'], input[placeholder*='手机'], [class*='phone'] input, [class*='mobile'] input",
        "send_code_selector": "button, [class*='code'], [class*='send'], text=获取验证码, text=发送验证码, text=获取验证码",
        "code_input_selector": "input[type='text'], input[placeholder*='验证码'], input[placeholder*='code'], [class*='code'] input, [class*='verify'] input",
        "login_button_selector": "button[type='submit'], button:has-text('登录'), button:has-text('确认'), [class*='login'] button",
        "success_url_pattern": "life.douyin.com",
        "check_logged_in": ".merchant-name, .user-avatar, [class*='header'] [class*='name']",
        "cookie_domain": ".douyin.com",
        "viewport": {"width": 1280, "height": 800},
        "sms_timeout": 300,  # 验证码等待超时（5分钟）
    },
}


# ═══════════════════════════════════════════════════════════════
# Worker 函数（独立进程）
# ═══════════════════════════════════════════════════════════════

def _sms_start_worker(task_id: str, platform: str, phone: str, results_dir: str):
    """
    在独立进程中：打开登录页 → 填入手机号 → 点击发送验证码。
    浏览器保持打开，等待后续 sms_verify 来填入验证码。
    """
    from playwright.sync_api import sync_playwright

    done_file = os.path.join(results_dir, f"{task_id}_sms_start.json")
    config = PLATFORM_SMS_CONFIG.get(platform)

    if not config:
        _write_result(done_file, {"status": "failed", "error": f"不支持的平台: {platform}"})
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

        login_url = config["login_url"]
        logger.info(f"[SMS Start Worker] {task_id} navigating to {login_url}")
        page.goto(login_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)

        # 填入手机号
        phone_filled = False
        for selector in config["phone_input_selector"].split(","):
            selector = selector.strip()
            try:
                el = page.wait_for_selector(selector, timeout=5000)
                if el:
                    el.click()
                    el.fill(phone)
                    phone_filled = True
                    logger.info(f"[SMS Start Worker] {task_id} phone filled via: {selector}")
                    break
            except Exception:
                continue

        if not phone_filled:
            _write_result(done_file, {"status": "failed", "error": "找不到手机号输入框"})
            return

        page.wait_for_timeout(1000)

        # 点击"发送验证码"按钮
        code_sent = False
        for selector in config["send_code_selector"].split(","):
            selector = selector.strip()
            try:
                # 用 page.locator 方式更灵活
                locators = [
                    page.locator(selector).first,
                ]
                for loc in locators:
                    try:
                        if loc.count() > 0 and loc.is_visible(timeout=3000):
                            loc.click()
                            code_sent = True
                            logger.info(f"[SMS Start Worker] {task_id} send code clicked via: {selector}")
                            break
                    except Exception:
                        continue
                if code_sent:
                    break
            except Exception:
                continue

        if not code_sent:
            logger.warning(f"[SMS Start Worker] {task_id} could not find send code button, phone filled only")
            # 不算失败，前端可能手动操作

        page.wait_for_timeout(2000)

        # 导出当前 context 的临时状态供 sms_verify 使用
        # 通过保存 cookies + localStorage（不含 IndexedDB，因为还没登录）
        current_state = context.storage_state()

        _write_result(done_file, {
            "status": "ready",
            "phone_filled": phone_filled,
            "code_sent": code_sent,
            "current_url": page.url,
            "storage_state": current_state,  # 传递当前状态
        })

        # 浏览器保持打开，等 sms_verify 来接管
        # 但 multiprocessing 进程需要保持存活 — 通过写 heartbeat 文件
        heartbeat_file = os.path.join(results_dir, f"{task_id}_heartbeat")
        start = time.time()
        timeout = config.get("sms_timeout", 300)
        while time.time() - start < timeout:
            # 检查取消信号
            cancel_file = os.path.join(results_dir, f"{task_id}_cancel")
            if os.path.exists(cancel_file):
                logger.info(f"[SMS Start Worker] {task_id} cancelled")
                break
            # 写心跳
            try:
                with open(heartbeat_file, "w") as f:
                    f.write(str(time.time()))
            except Exception:
                pass
            time.sleep(2)

        logger.info(f"[SMS Start Worker] {task_id} timeout, closing browser")

    except Exception as e:
        logger.error(f"[SMS Start Worker] {task_id} error: {e}", exc_info=True)
        _write_result(done_file, {"status": "failed", "error": str(e)})

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


def _sms_verify_worker(task_id: str, platform: str, verify_code: str, results_dir: str):
    """
    在独立进程中：用之前保存的 storage_state 创建 context → 填入验证码 → 点击登录 → 导出完整登录态。
    这是一个全新的浏览器进程，通过复用之前的 state 来保持页面状态。
    """
    from playwright.sync_api import sync_playwright

    done_file = os.path.join(results_dir, f"{task_id}_sms_verify.json")
    config = PLATFORM_SMS_CONFIG.get(platform)

    if not config:
        _write_result(done_file, {"status": "failed", "error": f"不支持的平台: {platform}"})
        return

    # 读取之前的 start 结果获取 storage_state
    start_file = os.path.join(results_dir, f"{task_id}_sms_start.json")
    start_data = None
    if os.path.exists(start_file):
        try:
            with open(start_file, "r", encoding="utf-8") as f:
                start_data = json.load(f)
        except Exception:
            pass

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

        # 如果有之前的 state，恢复
        init_state = None
        if start_data and start_data.get("storage_state"):
            init_state = start_data["storage_state"]

        context = browser.new_context(
            storage_state=init_state,
            viewport=config["viewport"],
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

        # 如果是全新的 context，需要先导航到登录页并填入手机号
        if init_state:
            # 恢复状态，需要重新导航到登录页
            login_url = config["login_url"]
            page.goto(login_url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)
        else:
            login_url = config["login_url"]
            logger.info(f"[SMS Verify Worker] {task_id} navigating to {login_url}")
            page.goto(login_url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)

        # 填入验证码
        code_filled = False
        for selector in config["code_input_selector"].split(","):
            selector = selector.strip()
            try:
                el = page.wait_for_selector(selector, timeout=5000)
                if el:
                    el.click()
                    el.fill(verify_code)
                    code_filled = True
                    logger.info(f"[SMS Verify Worker] {task_id} code filled via: {selector}")
                    break
            except Exception:
                continue

        if not code_filled:
            _write_result(done_file, {"status": "failed", "error": "找不到验证码输入框"})
            return

        page.wait_for_timeout(1000)

        # 点击登录按钮
        login_clicked = False
        for selector in config["login_button_selector"].split(","):
            selector = selector.strip()
            try:
                loc = page.locator(selector).first
                if loc.count() > 0 and loc.is_visible(timeout=3000):
                    loc.click()
                    login_clicked = True
                    logger.info(f"[SMS Verify Worker] {task_id} login clicked via: {selector}")
                    break
            except Exception:
                continue

        if not login_clicked:
            logger.warning(f"[SMS Verify Worker] {task_id} login button not found")

        # 等待登录跳转
        start_time = time.time()
        timeout = 30
        logged_in = False

        while time.time() - start_time < timeout:
            current_url = page.url

            # URL 跳转检测
            if config["success_url_pattern"] in current_url and "login" not in current_url:
                logged_in = True
                break

            # DOM 检测
            try:
                indicator = page.wait_for_selector(config["check_logged_in"], timeout=1000)
                if indicator:
                    logged_in = True
                    break
            except Exception:
                pass

            time.sleep(2)

        if not logged_in:
            # 截图调试
            try:
                debug_path = os.path.join(results_dir, f"_debug_{platform}_sms_verify.png")
                page.screenshot(path=debug_path)
            except Exception:
                pass
            _write_result(done_file, {
                "status": "failed",
                "error": "验证码登录失败，请检查验证码是否正确",
                "current_url": page.url,
            })
            return

        # 登录成功！等待页面完全加载
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

        logger.info(f"[SMS Verify Worker] {task_id} login SUCCESS, {len(cookies_list)} cookies saved")

        _write_result(done_file, {
            "status": "success",
            "platform": platform,
            "cookies": cookies,
        })

    except Exception as e:
        logger.error(f"[SMS Verify Worker] {task_id} error: {e}", exc_info=True)
        _write_result(done_file, {"status": "failed", "error": str(e)})

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


def _write_result(filepath: str, data: dict):
    """安全写入 JSON 结果文件"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception as e:
        logger.error(f"[SMS Worker] Failed to write result to {filepath}: {e}")


# ═══════════════════════════════════════════════════════════════
# 服务类（主进程 async 接口）
# ═══════════════════════════════════════════════════════════════

class SMSLoginService:
    """短信验证码登录服务（单例）"""

    _instance: Optional["SMSLoginService"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    @classmethod
    def get_instance(cls) -> "SMSLoginService":
        return cls()

    def _ensure_init(self):
        if self._initialized:
            return
        os.makedirs(_RESULTS_DIR, exist_ok=True)
        self._processes: dict = {}
        self._initialized = True

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

    async def start_sms_login(self, platform: str, phone: str) -> dict:
        """
        第一步：启动浏览器，填入手机号，触发发送验证码。

        Returns:
            {"success": True, "task_id": "...", "status": "ready", "code_sent": True}
        """
        self._ensure_init()

        if platform not in PLATFORM_SMS_CONFIG:
            return {"success": False, "error": f"不支持短信登录的平台: {platform}"}

        task_id = f"sms_{str(uuid4())[:8]}_{int(time.time() * 1000)}"

        # 清除旧文件
        for suffix in ["_sms_start.json", "_sms_verify.json", "_cancel", "_heartbeat"]:
            fp = self._task_file(task_id, suffix)
            if os.path.exists(fp):
                os.remove(fp)

        # 启动 worker 进程
        process = multiprocessing.Process(
            target=_sms_start_worker,
            args=(task_id, platform, phone, _RESULTS_DIR),
            daemon=True,
            name=f"sms-start-{task_id[:8]}",
        )
        process.start()
        self._processes[task_id] = process
        logger.info(f"[SMS Login] started worker pid={process.pid} for {platform}")

        # 轮询等待 start 结果
        start_file = self._task_file(task_id, "_sms_start.json")
        for _ in range(30):
            await asyncio.sleep(1)

            result = self._read_json(start_file)
            if result:
                if result.get("status") == "ready":
                    return {
                        "success": True,
                        "task_id": task_id,
                        "status": "ready",
                        "code_sent": result.get("code_sent", False),
                    }
                elif result.get("status") == "failed":
                    self._cleanup_task(task_id)
                    return {"success": False, "error": result.get("error", "启动失败")}

        self._cleanup_task(task_id)
        return {"success": False, "error": "初始化超时，请重试"}

    async def verify_sms_code(self, task_id: str, platform: str, verify_code: str) -> dict:
        """
        第二步：用户提交验证码，填入并完成登录。

        Returns:
            {"status": "success", "platform": "...", "cookies": {...}}
            {"status": "failed", "error": "..."}
        """
        self._ensure_init()

        verify_file = self._task_file(task_id, "_sms_verify.json")

        # 清除旧的 verify 结果
        if os.path.exists(verify_file):
            os.remove(verify_file)

        # 启动 verify worker 进程
        process = multiprocessing.Process(
            target=_sms_verify_worker,
            args=(task_id, platform, verify_code, _RESULTS_DIR),
            daemon=True,
            name=f"sms-verify-{task_id[:8]}",
        )
        process.start()
        self._processes[f"{task_id}_verify"] = process
        logger.info(f"[SMS Login] verify worker pid={process.pid} for {task_id}")

        # 轮询等待 verify 结果
        for _ in range(45):
            await asyncio.sleep(1)

            result = self._read_json(verify_file)
            if result:
                self._cleanup_task(task_id)
                return result

        self._cleanup_task(task_id)
        return {"status": "failed", "error": "验证超时，请重试"}

    async def cancel_sms_login(self, task_id: str) -> dict:
        """取消短信登录流程"""
        cancel_file = self._task_file(task_id, "_cancel")
        try:
            with open(cancel_file, "w") as f:
                f.write(str(time.time()))
        except Exception:
            pass

        self._cleanup_task(task_id)
        return {"success": True}

    def _cleanup_task(self, task_id: str):
        """终止进程并清理文件"""
        for key in [task_id, f"{task_id}_verify"]:
            process = self._processes.pop(key, None)
            if process and process.is_alive():
                try:
                    process.terminate()
                    process.join(timeout=5)
                    if process.is_alive():
                        process.kill()
                except Exception:
                    pass

        for suffix in ["_sms_start.json", "_sms_verify.json", "_cancel", "_heartbeat"]:
            fp = self._task_file(task_id, suffix)
            if os.path.exists(fp):
                try:
                    os.remove(fp)
                except Exception:
                    pass

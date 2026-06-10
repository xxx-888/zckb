"""
短信验证码登录服务
用于抖音来客等平台通过手机号+验证码方式获取登录态。
复用 multiprocessing + JSON IPC 模式，与 qr_login_service 架构一致。

流程:
  1. sms_start: 启动浏览器 → 打开登录页 → 填入手机号 → 点击"发送验证码" → 返回 task_id
  2. sms_verify: 恢复页面 → 填入手机号+验证码 → 勾选协议 → 点击"立即入驻" → 等待跳转 → 导出 storage_state

抖音来客登录页 DOM 结构（2025-06 实测）:
  - 登录地址: https://life.douyin.com/p/login
  - 手机号输入框: <input placeholder="手机号码" class="life-core-input life-core-input-size-md">
  - 发送验证码: <span class="src-pages-Login-components-Phone-FieldCodeInput-index-module__btn-send-code--AT_Wx--212e2">发送验证码</span>
  - 验证码输入框: <input placeholder="验证码" class="life-core-input life-core-input-size-md">
  - 用户协议勾选: <span class="life-core-checkbox-icon">
  - 登录按钮: <button type="submit" class="life-core-btn ...">立即入驻</button>
"""
import asyncio
import json
import logging
import multiprocessing
import os
import re
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
        # 抖音来客登录页地址
        "login_url": "https://life.douyin.com/p/login",

        # 手机号输入框 — 抖音来客使用 placeholder="手机号码" + life-core-input class
        # 同时兼容可能的 type="tel" 变体
        "phone_input_selectors": [
            'input.life-core-input[placeholder="手机号码"]',
            'input[placeholder="手机号码"]',
            'input[placeholder="请输入手机号"]',
            'input.life-core-input[placeholder*="手机"]',
        ],

        # 发送验证码按钮 — 抖音来客的 class 名含 CSS module hash，不稳定
        # 优先用文本匹配 "发送验证码"，再用 class 部分匹配
        "send_code_selectors": [
            'text="发送验证码"',
            'text="获取验证码"',
            'span:has-text("发送验证码"):not(:has(span))',
            'button:has-text("发送验证码")',
            '[class*="btn-send-code"]',
            '[class*="sendCode"]',
            '[class*="send-code"]',
        ],

        # 验证码输入框
        "code_input_selectors": [
            'input.life-core-input[placeholder="验证码"]',
            'input[placeholder="验证码"]',
            'input[placeholder="请输入验证码"]',
            'input.life-core-input[placeholder*="验证码"]',
        ],

        # 用户协议勾选框 — 需要点击来勾选（如果未勾选）
        "agreement_checkbox_selectors": [
            'span.life-core-checkbox-icon',
            '[class*="checkbox-icon"]',
            '[class*="agreement"] [class*="checkbox"]',
        ],

        # 登录/入驻按钮
        "login_button_selectors": [
            'button.life-core-btn[type="submit"]',
            'button[type="submit"]:has-text("立即入驻")',
            'button:has-text("立即入驻")',
            'button:has-text("登录")',
            'button.life-core-btn[type="submit"]',
        ],

        # 登录成功检测
        "success_url_pattern": "life.douyin.com",
        "success_url_exclude": "login",
        "check_logged_in": ".merchant-name, .user-avatar, [class*='header'] [class*='name'], [class*='merchant-info']",

        # Cookie 过滤域名
        "cookie_domain": ".douyin.com",

        # 浏览器视口
        "viewport": {"width": 1280, "height": 800},

        # 验证码等待超时（5分钟）
        "sms_timeout": 300,
    },
}


def _launch_browser(pw):
    """启动浏览器（优先 Chrome channel，回退 Chromium）- 有头模式便于调试"""
    try:
        browser = pw.chromium.launch(
            headless=False,
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
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--lang=zh-CN",
            ],
        )
    return browser


def _try_selectors(page, selectors, action="click", timeout=5000):
    """
    按优先级尝试多个选择器执行操作。
    action: "click" | "fill" | "check"
    返回 (成功, 使用的选择器, 元素)
    """
    for selector in selectors:
        selector = selector.strip()
        if not selector:
            continue
        try:
            # 文本选择器（text="xxx"）用 locator
            if selector.startswith('text=') or selector.startswith('button:has-text') or selector.startswith('span:has-text'):
                loc = page.locator(selector).first
                if loc.count() > 0:
                    loc.wait_for(state="visible", timeout=timeout)
                    if action == "click":
                        loc.click()
                    elif action == "fill":
                        pass  # 文本选择器一般不用于 fill
                    return True, selector, loc
            else:
                el = page.wait_for_selector(selector, timeout=timeout, state="visible")
                if el:
                    if action == "click":
                        el.click()
                    elif action == "fill":
                        pass  # fill 需要外部调用
                    elif action == "check":
                        el.click()  # checkbox 用 click 切换
                    return True, selector, el
        except Exception:
            continue
    return False, None, None


def _fill_input(page, selectors, value, timeout=5000):
    """尝试多个选择器填入值"""
    for selector in selectors:
        selector = selector.strip()
        if not selector:
            continue
        try:
            el = page.wait_for_selector(selector, timeout=timeout, state="visible")
            if el:
                el.click()
                page.wait_for_timeout(200)
                # 使用 fill 而不是 type，避免逐字符触发事件导致问题
                el.fill("")
                el.fill(value)
                page.wait_for_timeout(300)
                # 验证值已填入
                filled_value = el.input_value()
                if filled_value == value:
                    return True, selector
                # fill 可能被框架拦截，尝试 type
                el.fill("")
                el.type(value, delay=50)
                page.wait_for_timeout(200)
                return True, selector
        except Exception:
            continue
    return False, None


def _is_checkbox_checked(page, selectors):
    """检查 checkbox 是否已勾选"""
    for selector in selectors:
        selector = selector.strip()
        if not selector:
            continue
        try:
            # 检查父元素的 aria-checked 或 class 是否含 checked
            loc = page.locator(selector).first
            if loc.count() > 0:
                # 尝试获取父级容器的 class 或 aria-checked
                parent = loc.locator("xpath=ancestor::*[@class][1]").first
                if parent.count() > 0:
                    cls = parent.get_attribute("class") or ""
                    aria = parent.get_attribute("aria-checked") or ""
                    if "checked" in cls.lower() or aria == "true":
                        return True
                # 检查 checkbox-icon 本身是否有 checked class
                cls = loc.get_attribute("class") or ""
                if "checked" in cls.lower():
                    return True
        except Exception:
            continue
    return False


# ═══════════════════════════════════════════════════════════════
# Worker 函数（独立进程）
# ═══════════════════════════════════════════════════════════════

def _sms_start_worker(task_id: str, platform: str, phone: str, results_dir: str):
    """
    第一步（独立进程）：
    1. 启动浏览器 → 打开抖音来客登录页
    2. 等待页面加载 → 填入手机号
    3. 点击「发送验证码」
    4. 保存当前 storage_state（含 cookies + localStorage）
    5. 返回 task_id + status=ready，保持进程存活等待 verify
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
        logger.info(f"[SMS Start] {task_id} Playwright started")

        browser = _launch_browser(pw)
        logger.info(f"[SMS Start] {task_id} Browser launched")

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
        logger.info(f"[SMS Start] {task_id} Context created, viewport={config['viewport']}, stealth JS injected")

        page = context.new_page()

        # ---- Step 1: 打开登录页 ----
        login_url = config["login_url"]
        logger.info(f"[SMS Start] {task_id} ═══ Step 1: Navigating to login page: {login_url}")
        page.goto(login_url, wait_until="domcontentloaded", timeout=30000)
        logger.info(f"[SMS Start] {task_id} Page loaded, current_url={page.url[:80]}")

        # 抖音来客是 SPA，需要等待 JS 渲染完成
        logger.info(f"[SMS Start] {task_id} Waiting for SPA to render (phone input)...")
        phone_filled = False
        for attempt in range(3):
            phone_filled, phone_sel = _fill_input(
                page, config["phone_input_selectors"], phone, timeout=8000
            )
            if phone_filled:
                logger.info(f"[SMS Start] {task_id} ✓ Phone filled OK via selector: {phone_sel}")
                break
            # 可能页面还在加载，等一下再试
            logger.warning(f"[SMS Start] {task_id} ✗ Phone input not found (attempt {attempt + 1}/3), retrying in 3s...")
            page.wait_for_timeout(3000)

        if not phone_filled:
            logger.error(f"[SMS Start] {task_id} ✗ FAILED: Could not find phone input after 3 attempts")
            _write_result(done_file, {"status": "failed", "error": "找不到手机号输入框，页面可能未正确加载"})
            return

        page.wait_for_timeout(1000)

        # ---- Step 2: 点击「发送验证码」 ----
        logger.info(f"[SMS Start] {task_id} ═══ Step 2: Clicking 'Send Verification Code' button...")
        code_sent = False
        code_sent, code_sel, _ = _try_selectors(
            page, config["send_code_selectors"], action="click", timeout=5000
        )
        if code_sent:
            logger.info(f"[SMS Start] {task_id} ✓ Send code clicked OK via selector: {code_sel}")
        else:
            logger.warning(f"[SMS Start] {task_id} ✗ Send code button not found (phone was filled, not critical)")

        # 等待发送验证码请求完成
        logger.info(f"[SMS Start] {task_id} Waiting 3s for SMS request to complete...")
        page.wait_for_timeout(3000)

        # ---- Step 3: 保存当前状态 ----
        logger.info(f"[SMS Start] {task_id} ═══ Step 3: Saving browser state (storage_state)...")
        current_state = context.storage_state()
        state_cookies = len(current_state.get("cookies", []))
        logger.info(f"[SMS Start] {task_id} ✓ State saved, {state_cookies} cookies in storage_state")

        _write_result(done_file, {
            "status": "ready",
            "phone_filled": True,
            "code_sent": code_sent,
            "current_url": page.url,
            "storage_state": current_state,
            "phone": phone,  # 保存手机号供 verify 阶段使用
        })

        logger.info(f"[SMS Start] {task_id} ═══ Result written to done_file: status=ready, phone={phone[-4:]}, code_sent={code_sent}")
        logger.info(f"[SMS Start] {task_id} ═══ Keeping process alive, waiting for verify (timeout={config.get('sms_timeout', 300)}s)...")

        # ---- 保持进程存活（等待 verify 或超时）----
        heartbeat_file = os.path.join(results_dir, f"{task_id}_heartbeat")
        start = time.time()
        timeout = config.get("sms_timeout", 300)
        while time.time() - start < timeout:
            cancel_file = os.path.join(results_dir, f"{task_id}_cancel")
            if os.path.exists(cancel_file):
                logger.info(f"[SMS Start] {task_id} cancelled")
                break
            try:
                with open(heartbeat_file, "w") as f:
                    f.write(str(time.time()))
            except Exception:
                pass
            time.sleep(2)

        logger.info(f"[SMS Start] {task_id} timeout, closing browser")

    except Exception as e:
        logger.error(f"[SMS Start] {task_id} error: {e}", exc_info=True)
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
    第二步（独立进程）：
    1. 用之前保存的 storage_state 创建新 context
    2. 导航到登录页 → 填入手机号（因为新 context 需要重新填）
    3. 填入验证码
    4. 勾选用户协议
    5. 点击「立即入驻」
    6. 等待登录成功跳转
    7. 导出完整 storage_state（含 indexed_db）→ 加密保存
    """
    from playwright.sync_api import sync_playwright

    done_file = os.path.join(results_dir, f"{task_id}_sms_verify.json")
    config = PLATFORM_SMS_CONFIG.get(platform)

    if not config:
        _write_result(done_file, {"status": "failed", "error": f"不支持的平台: {platform}"})
        return

    # 读取之前的 start 结果
    start_file = os.path.join(results_dir, f"{task_id}_sms_start.json")
    start_data = None
    if os.path.exists(start_file):
        try:
            with open(start_file, "r", encoding="utf-8") as f:
                start_data = json.load(f)
        except Exception:
            pass

    # 终止 start 进程（verify 会开新的浏览器）
    cancel_file = os.path.join(results_dir, f"{task_id}_cancel")
    try:
        with open(cancel_file, "w") as f:
            f.write(str(time.time()))
    except Exception:
        pass

    pw = None
    browser = None
    context = None
    page = None

    try:
        pw = sync_playwright().start()
        logger.info(f"[SMS Verify] {task_id} Playwright started")

        browser = _launch_browser(pw)
        logger.info(f"[SMS Verify] {task_id} Browser launched")

        # 恢复之前的 storage_state（含 cookies）
        init_state = None
        if start_data and start_data.get("storage_state"):
            init_state = start_data["storage_state"]
            restored_cookies = len(init_state.get("cookies", []))
            logger.info(f"[SMS Verify] {task_id} Restoring storage_state from start phase ({restored_cookies} cookies)")
        else:
            logger.warning(f"[SMS Verify] {task_id} No storage_state found from start phase, creating fresh context")

        # 保存手机号供重填
        saved_phone = start_data.get("phone", "") if start_data else ""
        logger.info(f"[SMS Verify] {task_id} Saved phone from start phase: {saved_phone[:3]}****{saved_phone[-4:]}")

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
        logger.info(f"[SMS Verify] {task_id} Context created (with restored state), stealth JS injected")
        page = context.new_page()

        # ---- Step 1: 导航到登录页 ----
        login_url = config["login_url"]
        logger.info(f"[SMS Verify] {task_id} ═══ Step 1: Navigating to login page: {login_url}")
        page.goto(login_url, wait_until="domcontentloaded", timeout=30000)
        logger.info(f"[SMS Verify] {task_id} Page loaded, current_url={page.url[:80]}, waiting 3s for SPA...")
        page.wait_for_timeout(3000)

        # ---- Step 2: 重新填入手机号（新 context 需要重新填）----
        logger.info(f"[SMS Verify] {task_id} ═══ Step 2: Re-filling phone number (new context requires re-fill)...")
        if saved_phone:
            phone_filled, phone_sel = _fill_input(
                page, config["phone_input_selectors"], saved_phone, timeout=8000
            )
            if phone_filled:
                logger.info(f"[SMS Verify] {task_id} ✓ Phone re-filled OK via selector: {phone_sel}")
            else:
                logger.warning(f"[SMS Verify] {task_id} ✗ Phone re-fill failed")
            page.wait_for_timeout(1000)

            # 重新点击「发送验证码」（因为新 context 可能需要）
            # 注意：如果验证码是之前发的，这里不需要再发
            # 但抖音来客可能要求重新发，先尝试不发，如果后续填验证码失败再考虑

        # ---- Step 3: 填入验证码 ----
        logger.info(f"[SMS Verify] {task_id} ═══ Step 3: Filling verification code: {verify_code[:2]}{'*' * (len(verify_code) - 2)}")
        code_filled = False
        for attempt in range(2):
            code_filled, code_sel = _fill_input(
                page, config["code_input_selectors"], verify_code, timeout=5000
            )
            if code_filled:
                logger.info(f"[SMS Verify] {task_id} ✓ Code filled OK via selector: {code_sel}")
                break
            logger.warning(f"[SMS Verify] {task_id} ✗ Code input not found (attempt {attempt + 1}/2), retrying in 2s...")
            page.wait_for_timeout(2000)

        if not code_filled:
            # 截图调试
            try:
                debug_path = os.path.join(results_dir, f"_debug_{platform}_sms_verify.png")
                page.screenshot(path=debug_path)
                logger.info(f"[SMS Verify] {task_id} Debug screenshot saved to {debug_path}")
            except Exception:
                pass
            logger.error(f"[SMS Verify] {task_id} ✗ FAILED: Code input not found after 2 attempts")
            _write_result(done_file, {"status": "failed", "error": "找不到验证码输入框"})
            return

        page.wait_for_timeout(1000)

        # ---- Step 4: 勾选用户协议 ----
        logger.info(f"[SMS Verify] {task_id} ═══ Step 4: Checking agreement checkbox...")
        try:
            already_checked = _is_checkbox_checked(page, config["agreement_checkbox_selectors"])
            if not already_checked:
                clicked, chk_sel, _ = _try_selectors(
                    page, config["agreement_checkbox_selectors"], action="click", timeout=3000
                )
                if clicked:
                    logger.info(f"[SMS Verify] {task_id} ✓ Agreement checkbox checked via: {chk_sel}")
                else:
                    logger.warning(f"[SMS Verify] {task_id} ✗ Agreement checkbox not found, proceeding anyway")
            else:
                logger.info(f"[SMS Verify] {task_id} ✓ Agreement already checked, skipping")
        except Exception as e:
            logger.warning(f"[SMS Verify] {task_id} ✗ Agreement checkbox error: {e}")

        page.wait_for_timeout(500)

        # ---- Step 5: 点击「立即入驻」按钮 ----
        logger.info(f"[SMS Verify] {task_id} ═══ Step 5: Clicking login button ('立即入驻')...")
        login_clicked = False
        for selector in config["login_button_selectors"]:
            selector = selector.strip()
            try:
                if selector.startswith('button:has-text') or selector.startswith('text='):
                    loc = page.locator(selector).first
                    if loc.count() > 0 and loc.is_visible(timeout=3000):
                        loc.click()
                        login_clicked = True
                        logger.info(f"[SMS Verify] {task_id} login clicked via: {selector}")
                        break
                else:
                    el = page.wait_for_selector(selector, timeout=3000, state="visible")
                    if el:
                        el.click()
                        login_clicked = True
                        logger.info(f"[SMS Verify] {task_id} login clicked via: {selector}")
                        break
            except Exception:
                continue

        if not login_clicked:
            logger.warning(f"[SMS Verify] {task_id} ✗ Login button not found!")

        # ---- Step 6: 等待登录跳转 ----
        login_timeout = 30
        logger.info(f"[SMS Verify] {task_id} ═══ Step 6: Waiting for login redirect (timeout={login_timeout}s)...")
        start_time = time.time()
        logged_in = False
        success_pattern = config["success_url_pattern"]
        exclude_pattern = config.get("success_url_exclude", "login")

        while time.time() - start_time < login_timeout:
            current_url = page.url

            # URL 跳转检测 — 登录成功后跳转到 life.douyin.com（不含 login）
            if success_pattern in current_url and exclude_pattern not in current_url.lower():
                logged_in = True
                logger.info(f"[SMS Verify] {task_id} ✓ Login SUCCESS! URL redirected to: {current_url}")
                break

            # DOM 检测
            try:
                indicator = page.wait_for_selector(config["check_logged_in"], timeout=1000)
                if indicator:
                    logged_in = True
                    logger.info(f"[SMS Verify] {task_id} ✓ Login SUCCESS! DOM indicator detected")
                    break
            except Exception:
                pass

            elapsed = int(time.time() - start_time)
            if elapsed % 6 == 0:
                logger.info(f"[SMS Verify] {task_id} ... still waiting for redirect ({elapsed}s/{login_timeout}s), current_url={current_url[:60]}")

            time.sleep(2)

        if not logged_in:
            # 截图调试
            try:
                debug_path = os.path.join(results_dir, f"_debug_{platform}_sms_verify_fail.png")
                page.screenshot(path=debug_path)
                logger.info(f"[SMS Verify] {task_id} Fail screenshot saved to {debug_path}")
            except Exception:
                pass
            logger.error(f"[SMS Verify] {task_id} ✗ FAILED: Login redirect not detected within timeout, current_url={page.url[:80]}")
            _write_result(done_file, {
                "status": "failed",
                "error": "验证码登录失败，请检查验证码是否正确",
                "current_url": page.url,
            })
            return

        # ---- Step 7: 登录成功！提取用户信息 ----
        logger.info(f"[SMS Verify] {task_id} ═══ Step 7: Login confirmed, extracting user profile info...")
        page.wait_for_timeout(3000)

        # 额外导航一次确保 cookies 完整
        try:
            logger.info(f"[SMS Verify] {task_id} Navigating to life.douyin.com to ensure full cookies...")
            page.goto("https://life.douyin.com/", wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(5000)
            logger.info(f"[SMS Verify] {task_id} Extra navigation done, current_url={page.url[:80]}")
        except Exception as e:
            logger.warning(f"[SMS Verify] {task_id} Extra navigation failed: {e}")

        # ---- Step 7a: 提取用户信息 ----
        # 抖音来客用户信息在右上角头像区域的 UserCard 弹出面板中
        # DOM 结构（2025-06 实测）:
        #   头像区域: div.box-profile（点击展开 UserCard）
        #   用户昵称: div.user-name → "商户7649231745585399859"
        #   账户ID:   div.account-id-row → "7649231745585399859"
        #   手机号:   div.phone-number → "153******65"
        #   角色:     div.role-name → "超级管理员"

        platform_username = ""
        platform_account_id = ""
        platform_phone = ""
        platform_role = ""

        # 点击头像区域展开 UserCard（默认是隐藏状态，class 含 __hide）
        profile_clicked = False
        profile_selectors = [
            '[class*="box-profile"]',
            '[class*="Profile"] [class*="avatar-content"]',
            '[class*="Profile"] [class*="avatar"]',
        ]
        for sel in profile_selectors:
            try:
                el = page.wait_for_selector(sel, timeout=5000, state="visible")
                if el:
                    el.click()
                    profile_clicked = True
                    logger.info(f"[SMS Verify] {task_id} ✓ Profile avatar clicked via: {sel}")
                    page.wait_for_timeout(1500)  # 等待 UserCard 动画展开
                    break
            except Exception:
                continue

        if not profile_clicked:
            logger.warning(f"[SMS Verify] {task_id} ✗ Could not find/click profile avatar, trying to read header title directly")

        # 提取用户昵称 — UserCard 展开后读取 user-name
        username_selectors = [
            '[class*="user-name"]',          # UserCard 内的用户名
            '[class*="title"] [class*="Profile"]',  # 顶部 header title（备选）
            '.merchant-name',
            '[class*="merchant-name"]',
            '[class*="header"] [class*="name"]',
        ]
        for sel in username_selectors:
            try:
                el = page.wait_for_selector(sel, timeout=3000)
                if el:
                    text = el.text_content() or ""
                    text = text.strip()
                    if text:
                        platform_username = text
                        logger.info(f"[SMS Verify] {task_id} ✓ Username extracted via '{sel}': {platform_username}")
                        break
            except Exception:
                continue

        # 提取账户 ID — UserCard 展开后读取 account-id-row
        account_id_selectors = [
            '[class*="account-id-row"]',
            '[class*="account-id"] [class*="row"]',
        ]
        for sel in account_id_selectors:
            try:
                el = page.wait_for_selector(sel, timeout=3000)
                if el:
                    text = el.text_content() or ""
                    # 文本包含 ID + "复制" + 分隔符，需要提取纯数字部分
                    # 实际文本如: "7649231745585399859复制" 或 "7649231745585399859 | 复制"
                    text = text.strip()
                    # 提取第一个连续数字串作为 ID
                    id_match = re.search(r'\d{10,}', text)
                    if id_match:
                        platform_account_id = id_match.group(0)
                        logger.info(f"[SMS Verify] {task_id} ✓ Account ID extracted: {platform_account_id}")
                        break
            except Exception:
                continue

        # 提取手机号
        phone_selectors = [
            '[class*="phone-number"]',
            '[class*="phone"] [class*="number"]',
        ]
        for sel in phone_selectors:
            try:
                el = page.wait_for_selector(sel, timeout=2000)
                if el:
                    text = el.text_content() or ""
                    text = text.strip()
                    # 去掉 "管理"、"换绑" 等额外文字
                    phone_match = re.match(r'[\d\*]+\s*\d{3}\*{4}\d{2}', text)
                    if phone_match:
                        platform_phone = phone_match.group(0).strip()
                    elif text:
                        platform_phone = text.split('\n')[0].strip()
                    if platform_phone:
                        logger.info(f"[SMS Verify] {task_id} ✓ Phone extracted: {platform_phone}")
                        break
            except Exception:
                continue

        # 提取角色信息
        role_selectors = [
            '[class*="role-name"]',
            '[class*="role"] [class*="name"]',
        ]
        for sel in role_selectors:
            try:
                el = page.wait_for_selector(sel, timeout=2000)
                if el:
                    text = el.text_content() or ""
                    text = text.strip()
                    if text:
                        platform_role = text
                        logger.info(f"[SMS Verify] {task_id} ✓ Role extracted: {platform_role}")
                        break
            except Exception:
                continue

        # 点击其他区域关闭 UserCard（避免遮挡后续操作）
        if profile_clicked:
            try:
                page.locator("body").click(position={"x": 100, "y": 100})
                page.wait_for_timeout(500)
            except Exception:
                pass

        # 如果从 UserCard 提取不到用户名，尝试从 header 直接读取
        if not platform_username:
            try:
                header_title_selectors = [
                    '[class*="Profile"] [class*="title--"]',
                    '[class*="box-profile"] [class*="title"]',
                ]
                for sel in header_title_selectors:
                    try:
                        el = page.wait_for_selector(sel, timeout=2000)
                        if el:
                            text = el.text_content() or ""
                            text = text.strip()
                            if text:
                                platform_username = text
                                logger.info(f"[SMS Verify] {task_id} ✓ Username extracted from header: {platform_username}")
                                break
                    except Exception:
                        continue
            except Exception:
                pass

        logger.info(f"[SMS Verify] {task_id} ═══════════════════════════════════════════════")
        logger.info(f"[SMS Verify] {task_id} ═══ USER PROFILE: username={platform_username}, account_id={platform_account_id}, phone={platform_phone}, role={platform_role}")
        logger.info(f"[SMS Verify] {task_id} ═══════════════════════════════════════════════")

        # ---- Step 7b: 导出 storage_state ----
        logger.info(f"[SMS Verify] {task_id} Exporting cookies and storage_state...")
        storage_state = context.storage_state(indexed_db=True)
        cookies_list = storage_state.get("cookies", [])

        # 过滤抖音域名 cookies
        cookies = {
            c["name"]: c["value"]
            for c in cookies_list
            if config["cookie_domain"] in c.get("domain", "")
        }
        cookies["_storage_state"] = storage_state
        logger.info(f"[SMS Verify] {task_id} ✓ Exported {len(cookies_list)} total cookies, {len(cookies) - 1} matched domain '{config['cookie_domain']}'")

        _write_result(done_file, {
            "status": "success",
            "platform": platform,
            "cookies": cookies,
            "platform_username": platform_username,
            "platform_account_id": platform_account_id,
            "platform_phone": platform_phone,
            "platform_role": platform_role,
        })

    except Exception as e:
        logger.error(f"[SMS Verify] {task_id} error: {e}", exc_info=True)
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
        logger.info(f"[SMS Login] ═══════════════════════════════════════════════")
        logger.info(f"[SMS Login] START: platform={platform}, phone={phone[:3]}****{phone[-4:]}, task_id={task_id}")
        logger.info(f"[SMS Login] ═══════════════════════════════════════════════")

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
        logger.info(f"[SMS Login] Worker process started, pid={process.pid}")

        # 轮询等待 start 结果（最多 40 秒，给 SPA 渲染留足时间）
        logger.info(f"[SMS Login] Polling for start result (timeout 40s)...")
        start_file = self._task_file(task_id, "_sms_start.json")
        for _ in range(40):
            await asyncio.sleep(1)

            result = self._read_json(start_file)
            if result:
                if result.get("status") == "ready":
                    logger.info(f"[SMS Login] ✓ Start phase complete: code_sent={result.get('code_sent')}")
                    return {
                        "success": True,
                        "task_id": task_id,
                        "status": "ready",
                        "code_sent": result.get("code_sent", False),
                    }
                elif result.get("status") == "failed":
                    logger.error(f"[SMS Login] ✗ Start phase failed: {result.get('error')}")
                    self._cleanup_task(task_id)
                    return {"success": False, "error": result.get("error", "启动失败")}

        logger.error(f"[SMS Login] ✗ Start phase timed out after 40s")
        self._cleanup_task(task_id)
        return {"success": False, "error": "初始化超时，请重试"}

    async def verify_sms_code(self, task_id: str, platform: str, verify_code: str) -> dict:
        """
        第二步：用户提交验证码，填入并完成登录。

        Returns:
            {"status": "success", "platform": "...", "cookies": {...}, "platform_username": "..."}
            {"status": "failed", "error": "..."}
        """
        self._ensure_init()
        logger.info(f"[SMS Login] ═══════════════════════════════════════════════")
        logger.info(f"[SMS Login] VERIFY: task_id={task_id}, code={verify_code[:2]}{'*' * (len(verify_code) - 2)}, platform={platform}")
        logger.info(f"[SMS Login] ═══════════════════════════════════════════════")

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
        logger.info(f"[SMS Login] Verify worker process started, pid={process.pid}")

        # 轮询等待 verify 结果（最多 50 秒）
        logger.info(f"[SMS Login] Polling for verify result (timeout 50s)...")
        for _ in range(50):
            await asyncio.sleep(1)

            result = self._read_json(verify_file)
            if result:
                status = result.get("status")
                if status == "success":
                    logger.info(f"[SMS Login] ✓ Verify phase complete: status=success, username={result.get('platform_username', '')}")
                else:
                    logger.error(f"[SMS Login] ✗ Verify phase failed: {result.get('error')}")
                self._cleanup_task(task_id)
                return result

        logger.error(f"[SMS Login] ✗ Verify phase timed out after 50s")
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

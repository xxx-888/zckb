"""
Playwright 平台登录引擎
统一管理各平台的登录流程，获取并序列化 cookies
支持：美团开店宝、抖音来客、淘宝闪购
"""

import json
import logging
from typing import Optional

from playwright.async_api import async_playwright, BrowserContext, Page, Cookie

logger = logging.getLogger(__name__)


# 各平台登录 URL
LOGIN_URLS = {
    "meituan": "https://ecommerce.meituan.com/",
    "douyin": "https://lifestyle.douyin.com/",
    "taobao": "https://login.taobao.com/",
}


class PlatformLoginEngine:
    """平台登录引擎，使用 Playwright 模拟登录获取 cookies"""

    def __init__(self, headless: bool = True):
        self.headless = headless

    async def login(
        self,
        platform: str,
        credentials: dict,
    ) -> dict:
        """
        登录指定平台，返回 { "success": True/False, "cookies": "...", "message": "..." }
        内部自动管理浏览器生命周期，调用方无需使用 async with。
        """
        if platform not in LOGIN_URLS:
            return {"success": False, "message": f"不支持的平台: {platform}"}

        username = credentials.get("username", "")
        password = credentials.get("password", "")

        playwright = None
        browser = None
        context: Optional[BrowserContext] = None
        try:
            playwright = await async_playwright().start()
            browser = await playwright.chromium.launch(
                headless=self.headless,
                args=["--no-sandbox", "--disable-setuid-sandbox"],
            )
            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            )
            page: Page = await context.new_page()

            if platform == "meituan":
                cookies = await self._login_meituan(page, username, password)
            elif platform == "dianping":
                cookies = await self._login_dianping(page, username, password)
            elif platform == "douyin":
                cookies = await self._login_douyin(page, username, password)
            elif platform == "taobao":
                cookies = await self._login_taobao(page, username, password)
            elif platform == "jd":
                cookies = await self._login_jd(page, username, password)
            else:
                return {"success": False, "message": f"未实现的平台: {platform}"}

            await context.close()
            await browser.close()
            await playwright.stop()
            return {"success": True, "cookies": cookies}

        except Exception as e:
            logger.error(f"平台登录失败 [{platform}]: {e}")
            try:
                if context:
                    await context.close()
            except Exception:
                pass
            try:
                if browser:
                    await browser.close()
            except Exception:
                pass
            try:
                if playwright:
                    await playwright.stop()
            except Exception:
                pass
            return {"success": False, "message": str(e)}

    async def _login_meituan(self, page: Page, username: str, password: str) -> dict:
        """美团开店宝登录"""
        await page.goto("https://ecommerce.meituan.com/", timeout=30000)
        await page.wait_for_load_state("networkidle")
        await page.fill('input[type="text"], input[name="username"], input#username', username)
        await page.fill('input[type="password"], input[name="password"], input#password', password)
        await page.click('button[type="submit"], button:has-text("登录")')
        try:
            await page.wait_for_url("**/home**", timeout=15000)
        except Exception:
            await page.wait_for_selector('[class*="logout"], [class*="user-info"]', timeout=15000)
        return await self._extract_cookies(page.context)

    async def _login_dianping(self, page: Page, username: str, password: str) -> dict:
        """大众点评商家中心登录"""
        await page.goto("https://e.dianping.com/", timeout=30000)
        await page.wait_for_load_state("networkidle")
        await page.fill('input[type="text"], input[name="username"]', username)
        await page.fill('input[type="password"]', password)
        await page.click('button[type="submit"], .login-btn')
        try:
            await page.wait_for_url("**/home**", timeout=15000)
        except Exception:
            await page.wait_for_selector('[class*="user"], [class*="logout"]', timeout=15000)
        return await self._extract_cookies(page.context)

    async def _login_douyin(self, page: Page, username: str, password: str) -> dict:
        """抖音来客登录"""
        await page.goto("https://lifestyle.douyin.com/", timeout=30000)
        await page.wait_for_load_state("networkidle")
        await page.fill('input[type="text"], input[name="account"]', username)
        await page.fill('input[type="password"]', password)
        await page.click('button[type="submit"], .login-btn')
        try:
            await page.wait_for_url("**/home**", timeout=15000)
        except Exception:
            await page.wait_for_selector('[class*="user"], [class*="logout"]', timeout=15000)
        return await self._extract_cookies(page.context)

    async def _login_taobao(self, page: Page, username: str, password: str) -> dict:
        """淘宝商家中心登录"""
        await page.goto("https://login.taobao.com/", timeout=30000)
        await page.wait_for_load_state("networkidle")
        await page.fill('input[name="fm-login-id"]', username)
        await page.fill('input[name="fm-login-password"]', password)
        await page.click('button[type="submit"], .fm-submit')
        try:
            await page.wait_for_url("**/seller**", timeout=15000)
        except Exception:
            await page.wait_for_selector('[class*="user"], [class*="seller"]', timeout=15000)
        return await self._extract_cookies(page.context)

    async def _login_jd(self, page: Page, username: str, password: str) -> dict:
        """京东商家中心登录"""
        await page.goto("https://shop.jd.com/", timeout=30000)
        await page.wait_for_load_state("networkidle")
        await page.fill('input[type="text"], input[name="loginName"]', username)
        await page.fill('input[type="password"]', password)
        await page.click('button[type="submit"], .btn-login')
        try:
            await page.wait_for_url("**/home**", timeout=15000)
        except Exception:
            await page.wait_for_selector('[class*="user"], [class*="logout"]', timeout=15000)
        return await self._extract_cookies(page.context)

    async def _extract_cookies(self, context: BrowserContext) -> dict:
        """从 Playwright context 提取 cookies，转为 { name: value } 格式"""
        cookies: list[Cookie] = await context.cookies()
        return {c["name"]: c["value"] for c in cookies}

    @staticmethod
    def serialize_cookies(cookies: dict) -> str:
        """将 cookies 字典序列化为存储用的 JSON 字符串"""
        return json.dumps(cookies, ensure_ascii=False)

    @staticmethod
    def deserialize_cookies(cookies_str: str) -> dict:
        """从存储的 JSON 字符串反序列化为 cookies 字典"""
        if not cookies_str:
            return {}
        return json.loads(cookies_str)


async def test_login(platform: str, username: str, password: str):
    """测试登录（手动调试用，非 headless 模式）"""
    engine = PlatformLoginEngine(headless=False)
    result = await engine.login(platform, {"username": username, "password": password})
    if result["success"]:
        print(f"登录成功！cookies 共 {len(result['cookies'])} 个")
        serialized = PlatformLoginEngine.serialize_cookies(result["cookies"])
        print(f"序列化长度: {len(serialized)}")
        return result["cookies"]
    else:
        print(f"登录失败: {result['message']}")
        return None


if __name__ == "__main__":
    import asyncio, sys
    if len(sys.argv) >= 4:
        asyncio.run(test_login(sys.argv[1], sys.argv[2], sys.argv[3]))
    else:
        print("用法: python -m app.services.spider_engine <platform> <username> <password>")

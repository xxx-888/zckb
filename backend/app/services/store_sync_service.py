"""
店铺同步服务
登录成功后自动从平台商家后台抓取店铺列表（platform_store_id + platform_store_name），
同步到 store_platforms 表。

使用 multiprocessing 在独立进程中运行 Playwright（与 qr_login_service 一致）。
"""
import asyncio
import json
import logging
import multiprocessing
import os
import threading
import time
from typing import Optional
from uuid import uuid4

logger = logging.getLogger(__name__)

HEADLESS = os.getenv("QR_HEADLESS", "true").lower() in ("true", "1", "yes")
SYNC_TIMEOUT = 30  # 店铺同步超时（秒）

_RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".qr_results")

STEALTH_JS = """
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
if (!window.chrome) window.chrome = {};
window.chrome.runtime = { connect: function(){}, sendMessage: function(){} };
delete window.__playwright;
delete window.__pw_manual;
"""

# 平台店铺列表页面配置
PLATFORM_STORE_CONFIG = {
    "meituan": {
        # 美团开店宝 - 资质管理页面（会加载 pagePoiQualificationForMerchant 接口）
        "store_list_url": "https://ecom.meituan.com/settle/poi-ecom/poi-qualification",
        # 店铺列表表格行的选择器（通过 JS 提取数据更可靠）
        "cookie_domain": ".meituan.com",
        # JS 脚本：从页面 DOM 中提取店铺列表（匹配 mtd-prime-table 结构）
        "extract_script": """
        () => {
            const stores = [];
            // 美团开店宝使用 mtd-prime-table 组件
            const rows = document.querySelectorAll(
                '[data-row-key], tr.mtd-prime-table-row, table tbody tr'
            );

            rows.forEach(row => {
                try {
                    // 优先从 data-row-key 获取 poiId
                    const rowKey = row.getAttribute('data-row-key');
                    // 从单元格提取店铺名（第一个 td 中的主标题）
                    const nameEl = row.querySelector(
                        '.lWO5kd6T1Ugig0NqkqvT, ' +
                        '[class*="poiName"], [class*="shopName"], [class*="storeName"], ' +
                        'td:nth-child(1) a, a[class*="poi"], a[class*="shop"]'
                    );

                    const name = nameEl ? nameEl.textContent.trim() : '';
                    // poiId 可能作为子文本出现（如 "门店ID: 890106175"）
                    let id = rowKey || '';
                    if (!id) {
                        const idEl = row.querySelector(
                            '.lVRaQtkpm0j46fWn4m48, ' +
                            '[class*="poiId"], [class*="storeId"]'
                        );
                        if (idEl) {
                            const match = idEl.textContent.match(/\\d+/);
                            if (match) id = match[0];
                        }
                    }

                    if (name && id) {
                        stores.push({
                            platform_store_id: id,
                            platform_store_name: name,
                        });
                    }
                } catch(e) {}
            });

            return { stores, method: 'dom', url: window.location.href };
        }
        """,
        # 通过资质管理 API 获取店铺列表（最可靠）
        # 注意: accountId 通过 page.evaluate 第二个参数注入
        "api_extract_script": """
        async (accountId) => {
            try {
                const requestBody = accountId
                    ? { request: { accountId: parseInt(accountId), keyword: '', pageNo: 1, pageSize: 10 } }
                    : {};

                const res = await fetch(
                    'https://ecom.meituan.com/gw/nibcus/poiQualification/pagePoiQualificationForMerchant',
                    {
                        method: 'POST',
                        headers: {
                            'accept': 'application/json, text/plain, */*',
                            'content-type': 'application/json',
                            'is-api-upgrade': '1',
                        },
                        body: JSON.stringify(requestBody),
                        credentials: 'include'
                    }
                );
                const status = res.status;
                const text = await res.text();

                console.log('[API Extract] Status:', status, 'AccountId:', accountId);
                console.log('[API Extract] Response (first 500):', text.substring(0, 500));

                if (status !== 200) {
                    return { stores: [], method: 'api_error', error: `HTTP ${status}`, body: text.substring(0, 500) };
                }

                let json;
                try { json = JSON.parse(text); } catch(e) {
                    return { stores: [], method: 'api_error', error: 'Invalid JSON', body: text.substring(0, 500) };
                }

                // 响应结构: { data: { total, code, data: [{ poiName, poiId, ... }] } }
                const respData = json?.data?.data || json?.data || [];
                const poiList = Array.isArray(respData) ? respData : [];

                const stores = poiList.map(poi => ({
                    platform_store_id: String(poi.poiId || poi.id || ''),
                    platform_store_name: poi.poiName || poi.name || '',
                })).filter(s => s.platform_store_id && s.platform_store_name);

                return { stores, method: 'api', total: poiList.length, raw_keys: poiList.length > 0 ? Object.keys(poiList[0]) : [] };
            } catch(e) {
                return { stores: [], method: 'api_error', error: e.message };
            }
        }
        """,
    },
    "douyin": {
        # 抖音来客 - 门店管理页面，页面会自动调用 poiAccountList 接口
        "store_list_url": "https://life.douyin.com/p/poi-manage/home",
        "cookie_domain": ".douyin.com",
        # 拦截的 API URL 关键字（用于 page.on("response") 匹配）
        "api_url_pattern": "poiAccountList",
        "extract_script": None,
        "api_extract_script": None,
    },
}


def _sync_worker(task_id: str, platform: str, storage_state: dict, headless: bool, results_dir: str, platform_account_id: str = ""):
    """
    在独立进程中运行店铺同步：
    1. 启动浏览器，加载 storage_state
    2. 通过 httpx 直接调用平台 API 获取店铺列表
    3. 兜底通过页面 DOM 提取
    4. 写入结果文件
    """
    # 配置子进程日志输出到 stderr（否则 multiprocessing 子进程日志不可见）
    import sys
    _handler = logging.StreamHandler(sys.stderr)
    _handler.setFormatter(logging.Formatter("[%(name)s] %(message)s"))
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)
    from playwright.sync_api import sync_playwright  # noqa: E402

    done_file = os.path.join(results_dir, f"{task_id}_sync_done.json")

    config = PLATFORM_STORE_CONFIG.get(platform)
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
                headless=headless,
                channel="chrome",
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox", "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage", "--disable-gpu",
                    "--lang=zh-CN",
                ],
            )
        except Exception:
            browser = pw.chromium.launch(
                headless=headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox", "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage", "--disable-gpu",
                    "--lang=zh-CN",
                ],
            )

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
        # 捕获浏览器 console.log 输出到 Python logger
        page.on("console", lambda msg: logger.info(f"[Browser Console] {msg.type}: {msg.text}"))

        # ═══════════════════════════════════════════════
        # 抖音来客特殊处理: 注册 response 监听器在导航之前
        # poiAccountList 请求会在页面加载过程中发出，必须在 goto 前注册
        # ═══════════════════════════════════════════════
        douyin_captured_stores = []
        douyin_capture_event = None

        if platform == "douyin":
            douyin_capture_event = threading.Event()
            api_pattern = config.get("api_url_pattern", "poiAccountList")

            def _on_response(response):
                """监听 poiAccountList API 响应"""
                try:
                    url = response.url
                    if api_pattern in url:
                        logger.info(f"[StoreSync] ✓ Response captured: status={response.status}, url={url[:120]}")
                        if response.status == 200:
                            try:
                                body = response.json()
                            except Exception as json_err:
                                logger.warning(f"[StoreSync] Failed to parse response JSON: {json_err}")
                                # 尝试用 text() 手动解析
                                try:
                                    text_body = response.text()
                                    body = json.loads(text_body)
                                    logger.info(f"[StoreSync] Fallback text() parse succeeded")
                                except Exception as e2:
                                    logger.error(f"[StoreSync] All parse attempts failed: {e2}")
                                    return
                            status_code = body.get("status_code")
                            logger.info(f"[StoreSync] poiAccountList response: status_code={status_code}")
                            store_list = body.get("data", {}).get("list", [])
                            pagination = body.get("data", {}).get("pagination", {})
                            logger.info(f"[StoreSync] poiAccountList: {len(store_list)} accounts, pagination={pagination}")
                            for item in store_list:
                                poi_id = str(item.get("poi_id") or "")
                                account_name = item.get("account_name") or item.get("detail", {}).get("life_account_name") or ""
                                account_id = str(item.get("account_id") or "")
                                status = item.get("status")
                                logger.info(f"[StoreSync]   → account_name={account_name}, poi_id={poi_id}, status={status}")
                                # 过滤无效门店：poi_id 为 "0" 或空
                                if not poi_id or poi_id == "0":
                                    logger.info(f"[StoreSync]   ✗ Skipping invalid store (poi_id=0 or empty)")
                                    continue
                                douyin_captured_stores.append({
                                    "platform_store_id": poi_id,
                                    "platform_store_name": account_name,
                                    "platform_account_id": account_id,
                                    "status": status,
                                })
                            douyin_capture_event.set()
                        else:
                            logger.warning(f"[StoreSync] poiAccountList HTTP status={response.status}")
                except Exception as e:
                    logger.warning(f"[StoreSync] Response handler error: {e}")

            page.on("response", _on_response)
            logger.info(f"[StoreSync] Response listener registered for pattern: '{api_pattern}' (BEFORE navigation)")

        # 导航到店铺列表页面（抖音用 domcontentloaded 因为 SPA 有持续监控请求，美团用 networkidle）
        store_url = config["store_list_url"]
        wait_mode = "domcontentloaded" if platform == "douyin" else "networkidle"
        logger.info(f"[StoreSync Worker] Navigating to {store_url} (wait_until={wait_mode})")
        page.goto(store_url, wait_until=wait_mode, timeout=30000)

        # 等待页面和接口响应充分完成
        page.wait_for_timeout(3000)

        # 检查是否被重定向到登录页
        current_url = page.url
        if "login" in current_url.lower() or "passport" in current_url.lower():
            _write_result(done_file, {
                "status": "failed",
                "error": "登录态已失效，被重定向到登录页面",
                "current_url": current_url,
            })
            return

        stores = []
        extract_method = "none"

        # ═══════════════════════════════════════════════
        # 策略1: page.evaluate(fetch) — 在浏览器上下文内发请求
        # 浏览器会自动携带所有 cookie（含 CSRF token）和正确的 header
        # 比 httpx 直接请求更可靠，因为美团 gw 网关会校验请求来源
        # ═══════════════════════════════════════════════
        if not stores and config.get("api_extract_script"):
            try:
                api_result = page.evaluate(config["api_extract_script"], platform_account_id)
                logger.info(f"[StoreSync Worker] page.evaluate API raw result (accountId={platform_account_id}): {api_result}")
                if api_result and api_result.get("stores"):
                    stores = api_result["stores"]
                    extract_method = api_result.get("method", "api")
                    logger.info(f"[StoreSync Worker] page.evaluate API extraction: {len(stores)} stores found")
            except Exception as e:
                logger.warning(f"[StoreSync Worker] page.evaluate API extraction failed: {e}")

        # ═══════════════════════════════════════════════
        # 策略2: DOM 提取 — 从页面表格中解析店铺数据
        # ═══════════════════════════════════════════════
        if not stores and config.get("extract_script"):
            try:
                # 先截图辅助调试
                screenshot_path = os.path.join(results_dir, f"{task_id}_page.png")
                page.screenshot(path=screenshot_path, full_page=True)
                logger.info(f"[StoreSync Worker] Page screenshot saved to {screenshot_path}")
                # 获取页面 HTML 片段辅助调试
                html_snippet = page.evaluate("() => document.body?.innerHTML?.substring(0, 2000) || ''")
                logger.info(f"[StoreSync Worker] Page HTML snippet (first 2000 chars): {html_snippet[:1000]}")

                dom_result = page.evaluate(config["extract_script"])
                logger.info(f"[StoreSync Worker] DOM extraction raw result: {dom_result}")
                if dom_result and dom_result.get("stores"):
                    stores = dom_result["stores"]
                    extract_method = dom_result.get("method", "dom")
                    logger.info(f"[StoreSync Worker] DOM extraction: {len(stores)} stores found")
            except Exception as e:
                logger.warning(f"[StoreSync Worker] DOM extraction failed: {e}")

        # ═══════════════════════════════════════════════
        # 策略3: 抖音来客 — 使用预注册的 poiAccountList API 响应数据
        # 监听器在 page.goto() 之前已注册，这里检查捕获结果
        # ═══════════════════════════════════════════════
        if not stores and platform == "douyin" and douyin_capture_event is not None:
            try:
                # 等待 API 响应被捕获（最多 15 秒）
                captured = douyin_capture_event.wait(timeout=15)
                # 额外等待 3 秒，给 SPA 分页请求留出时间
                page.wait_for_timeout(3000)

                # 如果首次未捕获到，尝试 reload 触发（SPA 可能因路由未变化而不重新请求）
                if not captured:
                    logger.info(f"[StoreSync] First pass no capture, reloading page to re-trigger API...")
                    # reload 前重置 event，以便捕获新的响应
                    douyin_capture_event.clear()
                    page.reload(wait_until="domcontentloaded", timeout=30000)
                    captured = douyin_capture_event.wait(timeout=15)
                    page.wait_for_timeout(3000)  # 同样给分页请求留时间

                if douyin_captured_stores:
                    stores = douyin_captured_stores
                    extract_method = "api_intercept"
                    logger.info(f"[StoreSync] ✓ Douyin API intercept: {len(stores)} valid stores captured")
                    # 打印所有捕获的店铺名
                    for s in stores:
                        logger.info(f"[StoreSync]   ✓ {s.get('platform_store_name', '')} (poi_id={s.get('platform_store_id', '')})")
                else:
                    logger.warning(f"[StoreSync] ✗ Douyin API intercept: no stores captured (captured={captured})")
                    logger.warning(f"[StoreSync] Current page URL: {page.url}")

            except Exception as e:
                logger.error(f"[StoreSync] Douyin API intercept error: {e}", exc_info=True)

            # 移除监听器
            try:
                page.remove_listener("response", _on_response)
            except Exception:
                pass

        # ═══════════════════════════════════════════════
        # 策略4: 拦截页面请求 — 用 route 拦截 API 响应获取数据（美团）
        # 当页面本身会调用 pagePoiQualificationForMerchant 时，直接拿响应
        # ═══════════════════════════════════════════════
        if not stores and platform == "meituan":
            try:
                # 重新加载页面，同时拦截 API 响应
                intercept_stores = []

                def handle_response(route):
                    try:
                        resp = route.fetch()
                        body = resp.text()
                        route.fulfill(response=resp)
                        # 尝试解析响应
                        try:
                            data = json.loads(body)
                            inner = data.get("data", {})
                            if isinstance(inner, dict):
                                poi_list = inner.get("data", [])
                            elif isinstance(inner, list):
                                poi_list = inner
                            else:
                                poi_list = []
                            if poi_list and isinstance(poi_list, list):
                                for poi in poi_list:
                                    poi_id = str(poi.get("poiId") or poi.get("id") or "")
                                    poi_name = poi.get("poiName") or poi.get("name") or ""
                                    if poi_id and poi_name:
                                        intercept_stores.append({
                                            "platform_store_id": poi_id,
                                            "platform_store_name": poi_name,
                                        })
                                logger.info(f"[StoreSync Worker] Route intercept caught {len(intercept_stores)} stores")
                        except Exception:
                            pass
                    except Exception as e:
                        logger.warning(f"[StoreSync Worker] Route intercept error: {e}")
                        route.continue_()

                page.route(
                    "**/gw/nibcus/poiQualification/pagePoiQualificationForMerchant",
                    handle_response,
                )
                page.reload(wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(2000)

                if intercept_stores:
                    stores = intercept_stores
                    extract_method = "route_intercept"
                    logger.info(f"[StoreSync Worker] Route intercept: {len(stores)} stores found")
                # 清除 route
                page.unroute("**/gw/nibcus/poiQualification/pagePoiQualificationForMerchant")
            except Exception as e:
                logger.warning(f"[StoreSync Worker] Route intercept failed: {e}")

        # 去重（按 platform_store_id）
        seen = set()
        unique_stores = []
        for s in stores:
            sid = s["platform_store_id"]
            if sid and sid not in seen:
                seen.add(sid)
                unique_stores.append(s)

        _write_result(done_file, {
            "status": "success",
            "platform": platform,
            "stores": unique_stores,
            "store_count": len(unique_stores),
            "method": extract_method,
        })
        logger.info(f"[StoreSync Worker] Sync complete: {len(unique_stores)} stores for {platform}")

    except Exception as e:
        logger.error(f"[StoreSync Worker] Error: {e}", exc_info=True)
        _write_result(done_file, {
            "status": "failed",
            "platform": platform,
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


def _write_result(filepath: str, data: dict):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception as e:
        logger.error(f"[StoreSync] Failed to write result: {e}")


class StoreSyncService:
    """店铺同步服务（单例）"""

    _instance: Optional["StoreSyncService"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    @classmethod
    def get_instance(cls) -> "StoreSyncService":
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

    async def sync_stores(self, platform: str, storage_state: dict, platform_account_id: str = "") -> dict:
        """
        同步平台店铺列表。

        Args:
            platform: 平台名称
            storage_state: Playwright storage_state
            platform_account_id: 平台原始账号ID（如美团accountId）

        Returns:
            {"status": "success", "stores": [...], "store_count": N}
            或 {"status": "failed", "error": "..."}
        """
        self._ensure_init()

        if platform not in PLATFORM_STORE_CONFIG:
            return {"status": "failed", "error": f"不支持的平台: {platform}"}

        task_id = str(uuid4())

        # 清理旧文件
        for suffix in ["_sync_done.json"]:
            fp = self._task_file(task_id, suffix)
            if os.path.exists(fp):
                os.remove(fp)

        # 启动 worker 进程
        process = multiprocessing.Process(
            target=_sync_worker,
            args=(task_id, platform, storage_state, HEADLESS, _RESULTS_DIR, platform_account_id),
            daemon=True,
            name=f"sync-{task_id[:8]}",
        )
        process.start()
        self._processes[task_id] = process
        logger.info(f"[StoreSync] Started sync process pid={process.pid} for {platform}")

        # 轮询等待结果（最多 30 秒）
        done_file = self._task_file(task_id, "_sync_done.json")
        for _ in range(60):  # 60 * 0.5s = 30s
            await asyncio.sleep(0.5)
            result = self._read_json(done_file)
            if result:
                self._cleanup_task(task_id)
                return result

        # 超时
        self._cleanup_task(task_id)
        return {"status": "failed", "error": "店铺同步超时"}

    def _cleanup_task(self, task_id: str):
        process = self._processes.pop(task_id, None)
        if process and process.is_alive():
            try:
                process.terminate()
                process.join(timeout=5)
                if process.is_alive():
                    process.kill()
            except Exception:
                pass

        for suffix in ["_sync_done.json"]:
            fp = self._task_file(task_id, suffix)
            if os.path.exists(fp):
                try:
                    os.remove(fp)
                except Exception:
                    pass

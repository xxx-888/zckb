"""
评论同步服务

通过 Playwright 在浏览器上下文中调用平台评论 API，抓取评论数据。
子进程负责 Playwright 抓取，主进程负责 DB 入库。

使用 multiprocessing 在独立进程中运行 Playwright（与 store_sync_service 一致）。
"""
import asyncio
import json
import logging
import multiprocessing
import os
import time
from typing import Optional
from uuid import uuid4

logger = logging.getLogger(__name__)

HEADLESS = os.getenv("QR_HEADLESS", "true").lower() in ("true", "1", "yes")
REVIEW_SYNC_TIMEOUT = 600  # 评论同步超时（秒）— 部分店铺评论量大，需要更长时间

_RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".qr_results")

STEALTH_JS = """
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
if (!window.chrome) window.chrome = {};
window.chrome.runtime = { connect: function(){}, sendMessage: function(){} };
delete window.__playwright;
delete window.__pw_manual;
"""

# 平台评论 API 配置
PLATFORM_REVIEW_CONFIG = {
    "meituan": {
        "api_url": "https://ecom.meituan.com/emis/gw/rpc/TFeedbackListNewService/queryMTFeedbackPCNew",
        "entry_url": "https://ecom.meituan.com/emis/evaluation/poi",
        "page_size": 50,
        "max_pages": 1000,
    },
    "dianping": {
        "api_url": "https://ecom.meituan.com/emis/gw/rpc/TFeedbackListNewService/queryDPFeedbackPCNew",
        "entry_url": "https://ecom.meituan.com/emis/evaluation/poi",
        "page_size": 50,
        "max_pages": 1000,
    },
}

# 评论 API 请求 JS — 在浏览器上下文中执行 fetch
REVIEW_FETCH_JS = """
async (args) => {
    try {
        const res = await fetch(args.apiUrl, {
            method: "POST",
            headers: { "content-type": "application/json" },
            body: JSON.stringify({
                pageNo: args.pageNo,
                pageSize: args.pageSize,
                poiId: String(args.poiId),
                startTime: -1,
                endTime: -1,
                replyType: "全部",
                starType: "全部",
                sourceType: "全部",
                userType: "全部",
                timeType: args.timeType
            }),
            credentials: "include"
        });
        const text = await res.text();
        let json;
        try { json = JSON.parse(text); } catch(e) { json = { error: text.substring(0, 500) }; }
        json._status = res.status;
        return json;
    } catch(e) {
        return { error: e.message, _status: 0 };
    }
}
"""


def _review_sync_worker(
    task_id: str,
    platform: str,  # 单个平台，如 "meituan" 或 "dianping"
    storage_state: dict,
    headless: bool,
    results_dir: str,
    stores: list,
    time_type: str = "近30天",
):
    """
    在独立进程中运行评论同步：
    1. 启动浏览器，加载 storage_state
    2. 调用指定平台的评论 API
    3. 收集评论原始数据，写入结果文件
    """
    import sys
    _handler = logging.StreamHandler(sys.stderr)
    _handler.setFormatter(logging.Formatter("[%(name)s] %(message)s"))
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)
    from playwright.sync_api import sync_playwright

    done_file = os.path.join(results_dir, f"{task_id}_review_done.json")

    # 校验平台
    if platform not in PLATFORM_REVIEW_CONFIG:
        _write_result(done_file, {"status": "failed", "error": f"不支持的平台: {platform}"})
        return

    config = PLATFORM_REVIEW_CONFIG[platform]
    logger.info(f"[ReviewSync Worker] platform={platform}, stores={len(stores)}, timeType={time_type}")

    pw = None
    browser = None
    context = None
    page = None

    try:
        pw = sync_playwright().start()

        # storage_state 直接可用（解密 cookies_encrypted 即得）
        if not storage_state or not storage_state.get("cookies"):
            _write_result(done_file, {"status": "failed", "error": "storage_state 为空，请重新扫码登录"})
            return

        # 兼容：如果 cookies 是 dict {name: value}，转换成 Playwright 列表格式
        _cookies = storage_state.get("cookies")
        if isinstance(_cookies, dict):
            domain = ".meituan.com"  # 美团和大众点评评论 API 都在 ecom.meituan.com 域下
            pw_cookies = []
            for name, value in _cookies.items():
                if str(name).startswith("_"):
                    continue
                pw_cookies.append({
                    "name": str(name),
                    "value": str(value),
                    "domain": domain,
                    "path": "/",
                    "expires": -1,
                    "httpOnly": False,
                    "secure": True,
                    "sameSite": "Lax",
                })
            storage_state["cookies"] = pw_cookies
            logger.info(f"[ReviewSync Worker] Converted cookies dict → list: {len(pw_cookies)} cookies")
        elif isinstance(_cookies, list):
            # 已经是正确格式，无需转换
            pass
        else:
            _write_result(done_file, {"status": "failed", "error": f"storage_state.cookies 格式异常: {type(_cookies)}"})
            return

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
        page.on("console", lambda msg: logger.info(f"[Browser Console] {msg.type}: {msg.text}"))

        # 先访问评论管理页面，建立完整登录态
        entry_url = config["entry_url"]
        logger.info(f"[ReviewSync Worker] Navigating to {entry_url}")
        page.goto(entry_url, wait_until="networkidle", timeout=30000)
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

        all_reviews = []
        page_size = config["page_size"]
        max_pages = config["max_pages"]

        for store_idx, store_info in enumerate(stores):
            poi_id = store_info["platform_store_id"]
            store_name = store_info.get("platform_store_name", poi_id)
            store_db_id = store_info.get("store_id", "")

            logger.info(f"[ReviewSync Worker] [{store_idx+1}/{len(stores)}] 抓取: {store_name} (poi_id={poi_id})")

            try:
                store_reviews = []
                api_total = None

                for page_no in range(1, max_pages + 1):
                    result = page.evaluate(REVIEW_FETCH_JS, {
                        "apiUrl": config["api_url"],
                        "poiId": poi_id,
                        "pageNo": page_no,
                        "pageSize": page_size,
                        "timeType": time_type,
                    })

                    if not result or result.get("error"):
                        error_msg = result.get("error", "Unknown error") if result else "Empty result"
                        logger.warning(f"[ReviewSync Worker] API error for {store_name} page {page_no}: {error_msg[:200]}")
                        if page_no == 1:
                            break  # 首页就失败，跳过此店铺
                        break  # 后续页失败，停止翻页

                    http_status = result.get("_status", 0)
                    data_outer = result.get("data") or {}
                    data_inner = (data_outer.get("data") or {}) if data_outer else {}
                    feedbacks = data_inner.get("feedbacks", []) or []

                    if page_no == 1:
                        code = data_outer.get("code", "?") if data_outer else "?"
                        msg = data_outer.get("msg", "") if data_outer else ""
                        api_total = (data_inner or {}).get("total")
                        logger.info(
                            f"[ReviewSync Worker] {store_name}: code={code}, msg={msg}, "
                            f"http={http_status}, total={api_total}, page_feedbacks={len(feedbacks)}"
                        )

                    for item in feedbacks:
                        review = _convert_raw_review(item, store_db_id, platform, poi_id)
                        if review:
                            store_reviews.append(review)

                    # 判断末页
                    if len(feedbacks) < page_size:
                        break
                    if api_total is not None and len(store_reviews) >= api_total:
                        break

                    # 翻页间隔
                    time.sleep(0.5)

                logger.info(f"[ReviewSync Worker] {store_name}: 共抓取 {len(store_reviews)} 条评论")
                all_reviews.extend(store_reviews)

            except Exception as e:
                logger.error(f"[ReviewSync Worker] {store_name} 异常: {e}", exc_info=True)
                continue

        # 去重（按 store_id + platform + platform_review_id）
        seen = set()
        unique_reviews = []
        for r in all_reviews:
            key = (r.get("store_id", ""), r["platform"], r["platform_review_id"])
            if r["platform_review_id"] and key not in seen:
                seen.add(key)
                unique_reviews.append(r)

        _write_result(done_file, {
            "status": "success",
            "platform": platform,
            "reviews": unique_reviews,
            "review_count": len(unique_reviews),
            "store_count": len(stores),
        })
        logger.info(
            f"[ReviewSync Worker] Sync complete: {len(unique_reviews)} reviews "
            f"from {len(stores)} stores for {platform}"
        )

    except Exception as e:
        logger.error(f"[ReviewSync Worker] Error: {e}", exc_info=True)
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


def _convert_raw_review(raw_item: dict, store_db_id: str, platform: str, poi_id: str) -> Optional[dict]:
    """将平台原始评论转换为标准格式"""
    try:
        from datetime import datetime, timezone, timedelta

        _TZ = timezone(timedelta(hours=8))

        # 评论时间
        comment_time = None
        add_time_ts = raw_item.get("addTime")
        if add_time_ts and isinstance(add_time_ts, (int, float)) and add_time_ts > 0:
            comment_time = datetime.fromtimestamp(add_time_ts / 1000, tz=_TZ)
        else:
            raw_time = raw_item.get("commentTime") or raw_item.get("commentTimeStr")
            if raw_time:
                for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y/%m/%d"):
                    try:
                        dt = datetime.strptime(str(raw_time)[:19], fmt)
                        comment_time = dt.replace(tzinfo=_TZ)
                        break
                    except ValueError:
                        continue

        # 图片（API 返回的图片可能是 dict 对象，需提取 url 字段）
        images_raw = raw_item.get("pictures") or raw_item.get("images") or raw_item.get("imgs") or []
        images_list = []
        if isinstance(images_raw, list):
            for img in images_raw:
                if isinstance(img, str):
                    images_list.append(img)
                elif isinstance(img, dict):
                    # 优先取 url/originUrl/bigUrl，降级取 thumbUrl
                    url = img.get("url") or img.get("originUrl") or img.get("bigUrl") or img.get("thumbUrl") or ""
                    if url:
                        images_list.append(url)
        if not images_list:
            images_list = None

        # 情感：基于评分自动判断
        score = raw_item.get("score") or raw_item.get("star") or 0
        if score >= 4:
            sentiment = "positive"
        elif score <= 2:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {
            "store_id": store_db_id,
            "platform": platform,
            "platform_store_id": poi_id,
            "platform_review_id": str(raw_item.get("feedbackId") or raw_item.get("id") or ""),
            "user_name": (raw_item.get("userName") or raw_item.get("userNickName") or "")[:100] or None,
            "user_avatar": (raw_item.get("userAvatar") or "")[:500] or None,
            "content": raw_item.get("content") or raw_item.get("commentText") or None,
            "rating": int(score) if score else 3,
            "images": images_list if images_list else None,
            "sentiment": sentiment,
            "platform_created_at": comment_time.isoformat() if comment_time else None,
            "raw_json": raw_item,
        }
    except Exception as e:
        logger.warning(f"[ReviewSync Worker] 评论转换失败: {e}")
        return None


def _write_result(filepath: str, data: dict):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, default=str)
    except Exception as e:
        logger.error(f"[ReviewSync] Failed to write result: {e}")


class ReviewSyncService:
    """评论同步服务（单例）"""

    _instance: Optional["ReviewSyncService"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    @classmethod
    def get_instance(cls) -> "ReviewSyncService":
        return cls()

    def _ensure_init(self):
        if self._initialized:
            return
        os.makedirs(_RESULTS_DIR, exist_ok=True)
        self._processes: dict = {}
        self._task_meta: dict = {}  # task_id → {"account_id", "platforms", "status", "result", "error", "started_at"}
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

    async def sync_reviews(
        self,
        platform: str,   # 单个平台，如 "meituan" 或 "dianping"
        storage_state: dict,  # Playwright storage_state（直接可用）
        stores: list,       # 该平台下的店铺列表
        time_type: str = "近30天",
    ) -> dict:
        """
        同步指定平台的评论。

        Args:
            platform: 平台名称（"meituan" 或 "dianping"）
            storage_state: Playwright storage_state
            stores: 该平台下的店铺列表 [{"platform_store_id", "platform_store_name", "store_id"}]
            time_type: 时间范围 "近7天"/"近30天"/"全部"

        Returns:
            {"status": "success", "reviews": [...], "review_count": N, "store_count": M}
        """
        print(f"[PRINT][sync_reviews] ENTRY: platform={platform}, stores={len(stores)}", flush=True)
        logger.info(f"[TRACE][sync_reviews] ENTRY: platform={platform}")
        self._ensure_init()

        if platform not in PLATFORM_REVIEW_CONFIG:
            return {"status": "failed", "error": f"不支持的平台: {platform}"}

        task_id = str(uuid4())

        # 清理旧文件
        fp = self._task_file(task_id, "_review_done.json")
        if os.path.exists(fp):
            os.remove(fp)

        # 启动 worker 进程（传单个 platform）
        process = multiprocessing.Process(
            target=_review_sync_worker,
            args=(task_id, platform, storage_state, HEADLESS, _RESULTS_DIR, stores, time_type),
            daemon=True,
            name=f"review-sync-{task_id[:8]}",
        )
        process.start()
        self._processes[task_id] = process
        logger.info(f"[ReviewSync] Started process pid={process.pid} for {platform}, {len(stores)} stores")

        # 轮询等待结果（最多 REVIEW_SYNC_TIMEOUT 秒）
        done_file = self._task_file(task_id, "_review_done.json")
        max_polls = int(REVIEW_SYNC_TIMEOUT * 2)  # 1200 * 0.5s = 600s
        for _ in range(max_polls):
            await asyncio.sleep(0.5)
            result = self._read_json(done_file)
            if result:
                self._cleanup_task(task_id)
                return result

        # 超时
        self._cleanup_task(task_id)
        self._task_meta[task_id] = {
            **self._task_meta.get(task_id, {}),
            "status": "failed",
            "error": f"评论同步超时（{REVIEW_SYNC_TIMEOUT}秒）",
        }
        return {"status": "failed", "error": f"评论同步超时（{REVIEW_SYNC_TIMEOUT}秒）"}

    async def start_sync_reviews_async(
        self,
        account_id: str,
        storage_state: dict,
        stores_by_platform: dict,  # {"meituan": [...], "dianping": [...]}
        time_type: str = "近30天",
    ) -> str:
        """
        非阻塞启动评论同步任务，返回 task_id。
        前端通过 get_sync_reviews_status(task_id) 轮询进度。
        """
        import asyncio as _asyncio

        self._ensure_init()
        task_id = str(uuid4())
        platforms_list = list(stores_by_platform.keys())

        self._task_meta[task_id] = {
            "account_id": account_id,
            "platforms": platforms_list,
            "status": "running",
            "result": None,
            "error": None,
            "started_at": time.time(),
            "current_platform": platforms_list[0] if platforms_list else "",
            "progress": f"0/{len(platforms_list)} 平台",
        }

        # 后台协程执行同步 + 入库
        async def _background_sync():
            from app.core.database import async_session_factory
            from app.models.review import Review

            try:
                all_reviews = []
                all_store_count = 0
                errors = []

                for idx, plt in enumerate(platforms_list):
                    plt_stores = stores_by_platform[plt]
                    self._task_meta[task_id]["current_platform"] = plt
                    self._task_meta[task_id]["progress"] = f"{idx}/{len(platforms_list)} 平台 ({plt})"

                    sync_result = await self.sync_reviews(
                        platform=plt,
                        storage_state=storage_state,
                        stores=plt_stores,
                        time_type=time_type,
                    )

                    if sync_result.get("status") == "success":
                        all_reviews.extend(sync_result.get("reviews", []))
                        all_store_count += sync_result.get("store_count", 0)
                    else:
                        err = sync_result.get("error", f"{plt} 同步失败")
                        errors.append(err)
                        logger.warning(f"[sync_reviews_bg] {plt} failed: {err}")

                # 直接在后台入库（避免 result 接口超时）
                created_count = 0
                skipped_count = 0

                if all_reviews:
                    # 去重
                    seen = set()
                    unique_reviews = []
                    for r in all_reviews:
                        key = (r.get("store_id", ""), r["platform"], r["platform_review_id"])
                        if r["platform_review_id"] and key not in seen:
                            seen.add(key)
                            unique_reviews.append(r)

                    from itertools import groupby as _groupby
                    from sqlalchemy import select as _select

                    async with async_session_factory() as db_session:
                        try:
                            existing_keys = set()
                            sorted_reviews = sorted(unique_reviews, key=lambda r: (r["platform"], r["platform_review_id"]))
                            for plat, grp in _groupby(sorted_reviews, key=lambda r: r["platform"]):
                                review_ids = [r["platform_review_id"] for r in list(grp)]
                                if review_ids:
                                    exist_stmt = _select(Review.platform_review_id).where(
                                        Review.platform == plat,
                                        Review.platform_review_id.in_(review_ids),
                                    )
                                    exist_result = await db_session.execute(exist_stmt)
                                    existing_keys.update((plat, row[0]) for row in exist_result.all())

                            from datetime import datetime
                            for item in unique_reviews:
                                key = (item["platform"], item["platform_review_id"])
                                if key in existing_keys or not item["platform_review_id"]:
                                    skipped_count += 1
                                    continue
                                platform_time = None
                                if item.get("platform_created_at"):
                                    try:
                                        platform_time = datetime.fromisoformat(item["platform_created_at"].replace("Z", "+00:00"))
                                        platform_time = platform_time.replace(tzinfo=None)
                                    except Exception:
                                        pass
                                review = Review(
                                    store_id=item["store_id"],
                                    platform=item["platform"],
                                    platform_review_id=item["platform_review_id"],
                                    user_name=item.get("user_name"),
                                    user_avatar=item.get("user_avatar"),
                                    rating=item.get("rating", 3),
                                    content=item.get("content"),
                                    images=item.get("images"),
                                    sentiment=item.get("sentiment"),
                                    raw_json=item.get("raw_json"),
                                    platform_created_at=platform_time,
                                    status="normal",
                                )
                                db_session.add(review)
                                created_count += 1
                            await db_session.commit()
                        except Exception as db_err:
                            logger.exception(f"[sync_reviews_bg] 入库异常: {db_err}")
                            await db_session.rollback()
                            errors.append(f"入库失败: {str(db_err)}")

                # 入库完成后，不再存储原始评论数据（只保留统计），释放内存
                self._task_meta[task_id].update({
                    "status": "success" if created_count > 0 or (not errors) else "failed",
                    "result": {
                        "review_count": len(all_reviews),
                        "created": created_count,
                        "skipped": skipped_count,
                        "store_count": all_store_count,
                        "errors": errors,
                    },
                    "error": "; ".join(errors) if errors else None,
                    "current_platform": "",
                    "progress": f"{len(platforms_list)}/{len(platforms_list)} 平台 - 入库完成",
                })
            except Exception as e:
                logger.exception(f"[sync_reviews_bg] task {task_id} exception")
                self._task_meta[task_id].update({
                    "status": "failed",
                    "error": str(e),
                })

        _asyncio.create_task(_background_sync())
        return task_id

    def get_sync_reviews_status(self, task_id: str) -> dict:
        """查询评论同步任务状态，供前端轮询。"""
        self._ensure_init()
        meta = self._task_meta.get(task_id)
        if not meta:
            return {"status": "not_found", "error": "任务不存在"}
        return {
            "status": meta["status"],  # running / success / failed
            "current_platform": meta.get("current_platform", ""),
            "progress": meta.get("progress", ""),
            "result": meta.get("result"),
            "error": meta.get("error"),
        }

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

        fp = self._task_file(task_id, "_review_done.json")
        if os.path.exists(fp):
            try:
                os.remove(fp)
            except Exception:
                pass

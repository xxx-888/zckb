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
        "api_type": "post",  # POST + JSON body
    },
    "dianping": {
        "api_url": "https://ecom.meituan.com/emis/gw/rpc/TFeedbackListNewService/queryDPFeedbackPCNew",
        "entry_url": "https://ecom.meituan.com/emis/evaluation/poi",
        "page_size": 50,
        "max_pages": 1000,
        "api_type": "post",
    },
    "douyin": {
        "api_url": "https://life.douyin.com/life/infra/v1/review/get_review_list/",
        "entry_url": "https://life.douyin.com/p/life_comment/management",
        "page_size": 20,
        "max_pages": 2000,
        "api_type": "get",  # GET + query params
        "cookie_domain": ".life.douyin.com",
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


# 抖音评论 API 请求 JS — GET + query params（在浏览器上下文中执行 fetch）
# 按账号获取所有店铺评论，poi_id=0 表示不筛选具体店铺
# 只需最小必要 headers，参考实际浏览器抓包
DOUYIN_REVIEW_FETCH_JS = """
async (args) => {
    try {
        const params = new URLSearchParams();
        params.set('poi_id', '0');
        params.set('tags', '1,2,3,9,5,4,10,8,7,50,');
        params.set('sort_by', '2');
        params.set('life_account_id', args.lifeAccountId);
        params.set('count', String(args.count));
        params.set('cursor', String(args.cursor));
        params.set('top_rate_ids', '');
        params.set('reply_display_by_level', '1');
        params.set('root_life_account_id', args.lifeAccountId);
        params.set('store_type', '1');
        params.set('source', '1');
        params.set('all_selected_params', JSON.stringify({
            "SearchAllAccountPoiType": 0,
            "ExpandToPoiAccount": true,
            "SearchAllAccountPoiStatus": 0,
            "RelationTypes": [1, 10],
            "SettleStatusBeforeClaim": [],
            "Selections": [],
            "TagIDList": [],
            "MainCategoryList": {},
            "SubCategoryList": {},
            "PermissionKeyList": ["hermes.shop.evaluation_manage_CloudBusiness"],
            "StoreBizTagList": [],
            "SxtSolutionStatusList": [],
            "SxtSolutionPunishStatusList": []
        }));
        if (args.searchAfter) {
            params.set('search_after', JSON.stringify(args.searchAfter));
        }

        const url = args.apiUrl + '?' + params.toString();
        const res = await fetch(url, {
            method: "GET",
            headers: {
                "ac-tag": "smb_m",
                "accept": "application/json, text/plain, */*",
                "agw-js-conv": "str",
                "priority": "u=1, i",
                "rpc-persist-life-biz-view-id": "0",
                "rpc-persist-life-merchant-switch-role": "1",
                "rpc-persist-life-platform": "pc",
                "rpc-persist-lite-app-id": "100007",
                "rpc-persist-terminal-type": "1",
                "sec-ch-ua": '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-tt-trace-log": "01",
            },
            credentials: "include",
            mode: "cors",
        });
        const text = await res.text();
        let json;
        try { json = JSON.parse(text); } catch(e) { json = { error: text.substring(0, 500) }; }
        json._status = res.status;
        json._raw_keys = Object.keys(json);
        json._url = url.substring(0, 200);
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
        cookie_domain = config.get("cookie_domain", ".meituan.com")
        if isinstance(_cookies, dict):
            pw_cookies = []
            for name, value in _cookies.items():
                if str(name).startswith("_"):
                    continue
                pw_cookies.append({
                    "name": str(name),
                    "value": str(value),
                    "domain": cookie_domain,
                    "path": "/",
                    "expires": -1,
                    "httpOnly": False,
                    "secure": True,
                    "sameSite": "Lax",
                })
            storage_state["cookies"] = pw_cookies
            logger.info(f"[ReviewSync Worker] Converted cookies dict → list: {len(pw_cookies)} cookies (domain={cookie_domain})")
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

        is_douyin = platform == "douyin"

        # 抖音页面较重，使用 domcontentloaded 而非 networkidle 避免超时
        wait_strategy = "domcontentloaded" if is_douyin else "networkidle"
        goto_timeout = 60000 if is_douyin else 30000
        try:
            page.goto(entry_url, wait_until=wait_strategy, timeout=goto_timeout)
        except Exception as e:
            # 导航超时不一定失败，页面可能已加载，尝试继续
            logger.warning(f"[ReviewSync Worker] page.goto warning: {e}, continuing anyway")
        page.wait_for_timeout(3000 if not is_douyin else 5000)

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
        api_type = config.get("api_type", "post")

        # 抖音增量同步截止时间（30天前的 Unix 时间戳）
        import datetime as _dt
        _cutoff_ts = 0
        if is_douyin and time_type != "全部":
            _cutoff_dt = _dt.datetime.now(_dt.timezone(_dt.timedelta(hours=8))) - _dt.timedelta(days=30)
            _cutoff_ts = int(_cutoff_dt.timestamp())
            logger.info(f"[ReviewSync Worker] 抖音增量同步截止时间戳: {_cutoff_ts} ({_cutoff_dt.strftime('%Y-%m-%d %H:%M:%S')})")

        if is_douyin:
            # ========== 抖音：一次性拉取账号下所有评论，按 poi_id 匹配店铺 ==========
            # 构建 poi_id → store 映射
            poi_store_map = {}
            for s in stores:
                pid = s.get("platform_store_id", "")
                if pid:
                    poi_store_map[str(pid)] = s

            # life_account_id 从第一个店铺的 account_id 字段取
            life_account_id = ""
            for s in stores:
                lid = s.get("account_id", "")
                if lid:
                    life_account_id = lid
                    break

            if not life_account_id:
                _write_result(done_file, {"status": "failed", "error": "抖音账号缺少 life_account_id"})
                return

            logger.info(f"[ReviewSync Worker] 抖音: 使用 life_account_id={life_account_id}, 已绑定 {len(poi_store_map)} 个店铺")

            cursor = 0
            search_after = None
            douyin_reviews = []

            for page_no in range(1, max_pages + 1):
                result = page.evaluate(DOUYIN_REVIEW_FETCH_JS, {
                    "apiUrl": config["api_url"],
                    "lifeAccountId": life_account_id,
                    "count": page_size,
                    "cursor": cursor,
                    "searchAfter": search_after,
                })

                if not result or result.get("error"):
                    error_msg = result.get("error", "Unknown error") if result else "Empty result"
                    logger.warning(f"[ReviewSync Worker] 抖音 API error page {page_no}: {error_msg[:200]}")
                    break

                http_status = result.get("_status", 0)
                raw_keys = result.get("_raw_keys", [])

                # 尝试多种字段名获取评论列表（抖音数据在 data 层内）
                outer_data = result.get("data") or {}
                reviews_data = outer_data.get("reviews") or result.get("reviews") or result.get("review_list", []) or []
                has_more = outer_data.get("has_more", False) or result.get("has_more", False)
                filtered_count = outer_data.get("filtered_count") or result.get("filtered_count", "?")

                # 每页都输出进度和评论概要
                logger.info(
                    f"[ReviewSync Worker] 抖音 第{page_no}页: http={http_status}, "
                    f"filtered_count={filtered_count}, has_more={has_more}, "
                    f"本页={len(reviews_data)}, 已累计={len(douyin_reviews) + len(reviews_data)}"
                )

                # 每页输出评论简要信息（时间+评分+内容前30字）
                for idx, item in enumerate(reviews_data):
                    pub_ts = item.get("publiced_time", 0)
                    import datetime as _dt2
                    pub_str = _dt2.datetime.fromtimestamp(int(pub_ts), tz=_dt2.timezone(_dt2.timedelta(hours=8))).strftime("%m-%d %H:%M") if pub_ts else "?"
                    score = _extract_douyin_score(item.get("score_tags", []))
                    poi = str(item.get("poi_id", ""))[:10]
                    content = (item.get("review_content") or "")[:30]
                    logger.info(f"  [{idx+1}] {pub_str} ★{score} poi={poi}... {content}")

                for item in reviews_data:
                    # 根据评论中的 poi_id 匹配绑定的店铺
                    review_poi_id = str(item.get("poi_id", ""))
                    matched_store = poi_store_map.get(review_poi_id)
                    store_db_id = matched_store["store_id"] if matched_store else ""
                    poi_id = matched_store["platform_store_id"] if matched_store else review_poi_id

                    review = _convert_douyin_review(item, store_db_id, poi_id)
                    if review:
                        douyin_reviews.append(review)

                # 增量同步：遇到超过30天的评论则停止
                if _cutoff_ts > 0 and reviews_data:
                    last_ts = int(reviews_data[-1].get("publiced_time", 0))
                    if last_ts > 0 and last_ts < _cutoff_ts:
                        logger.info(f"[ReviewSync Worker] 抖音: 已到达30天前截止，停止翻页")
                        break

                if not has_more or len(reviews_data) < page_size:
                    break

                # 下一页：用最后一条评论的时间戳作为 search_after，cursor 始终为 0
                if reviews_data:
                    last_ts = int(reviews_data[-1].get("publiced_time", 0))
                    if last_ts > 0:
                        search_after = [1, last_ts]
                time.sleep(0.5)

            logger.info(f"[ReviewSync Worker] 抖音: 共抓取 {len(douyin_reviews)} 条评论")
            all_reviews.extend(douyin_reviews)

        else:
            # ========== 美团/大众点评：按店铺逐个查询 ==========
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
                            break

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

                        if len(feedbacks) < page_size:
                            break
                        if api_total is not None and len(store_reviews) >= api_total:
                            break

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


def _convert_douyin_review(raw_item: dict, store_db_id: str, poi_id: str) -> Optional[dict]:
    """将抖音评论转换为标准格式（与 meituan/dianping 格式对齐）"""
    try:
        from datetime import datetime, timezone, timedelta

        _TZ = timezone(timedelta(hours=8))

        # 评论时间（publiced_time 是 Unix 秒级时间戳）
        comment_time = None
        pub_ts = raw_item.get("publiced_time")
        if pub_ts and isinstance(pub_ts, (int, float, str)):
            try:
                comment_time = datetime.fromtimestamp(int(pub_ts), tz=_TZ)
            except (OSError, ValueError, OverflowError):
                pass

        # 评分：从 score_tags 中提取（type==20 的 sub_type 映射）
        score = _extract_douyin_score(raw_item.get("score_tags", []))

        # 情感判断
        if score >= 4:
            sentiment = "positive"
        elif score <= 2:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        # 图片（review_images 中的 url_list）
        images_list = []
        for img in (raw_item.get("review_images") or []):
            url_list = img.get("url_list") if isinstance(img, dict) else None
            if url_list and isinstance(url_list, list) and len(url_list) > 0:
                images_list.append(url_list[0])  # 取第一张 URL
        if not images_list:
            images_list = None

        # 回复
        reply_text = None
        replies = raw_item.get("replies") or []
        if replies and isinstance(replies, list) and len(replies) > 0:
            reply_text = replies[0].get("content", "")

        # 关联的产品名称
        spu_name = raw_item.get("spu_name") or ""

        return {
            "store_id": store_db_id,
            "platform": "douyin",
            "platform_store_id": raw_item.get("poi_id") or poi_id,
            "platform_review_id": str(raw_item.get("review_id") or ""),
            "user_name": (raw_item.get("cust_nick_name") or "")[:100] or None,
            "user_avatar": (raw_item.get("avatar_uri") or "")[:500] or None,
            "content": raw_item.get("review_content") or None,
            "rating": score,
            "images": images_list,
            "sentiment": sentiment,
            "platform_created_at": comment_time.isoformat() if comment_time else None,
            "raw_json": {
                "spu_name": spu_name,
                "reply": reply_text,
                "exposure_cnt": raw_item.get("exposure_cnt"),
                "thumb_ups": raw_item.get("thumb_ups"),
                "user_level": raw_item.get("user_level"),
                "review_source": raw_item.get("review_source"),
                **raw_item,
            },
        }
    except Exception as e:
        logger.warning(f"[ReviewSync Worker] 抖音评论转换失败: {e}")
        return None


def _extract_douyin_score(score_tags: list) -> int:
    """从抖音 score_tags 提取评分（1-5）"""
    if not score_tags or not isinstance(score_tags, list):
        return 3  # 默认中评
    for tag in score_tags:
        if not isinstance(tag, dict):
            continue
        if tag.get("type") == 20:
            sub = tag.get("sub_type", "")
            # sub_type 映射：10=超赞(5), 8=好评(4), 6=中评(3), 4=差评(2), 2=很差(1)
            score_map = {"10": 5, "8": 4, "6": 3, "4": 2, "2": 1}
            return score_map.get(str(sub), 3)
    # 没有 score_tags 时根据 attitude 字段判断
    return 3


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

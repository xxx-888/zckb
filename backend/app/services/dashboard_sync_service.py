"""
仪表盘数据同步服务

通过 Playwright 在浏览器上下文中调用平台仪表盘 API，抓取营业额、套餐、门店指标数据。
架构与 review_sync_service 一致：子进程运行 Playwright，主进程负责 DB 入库。

关键点：
- 美团开店宝 API 要求 startTime 和 endTime 必须同一天（error 605），需逐天查询
- 抖音来客 API 有签名验证，后端 httpx 无法直接调用，必须在浏览器环境中 fetch
- 两个平台的 fetch 请求都必须在浏览器页面上下文中执行（credentials: "include"）
"""

from __future__ import annotations

import asyncio
import json
import logging
import multiprocessing
import os
import time
from datetime import date, datetime, timedelta, timezone
from typing import Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store import PlatformAccount, Store, StorePlatform
from app.models.store_dashboard import PackageRecord, RevenueRecord, StoreMetric
from app.services.platform_service import PlatformService

logger = logging.getLogger(__name__)

HEADLESS = os.getenv("QR_HEADLESS", "true").lower() in ("true", "1", "yes")
DASHBOARD_SYNC_TIMEOUT = 300  # 仪表盘同步超时（秒）

_RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".qr_results")

STEALTH_JS = """
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
if (!window.chrome) window.chrome = {};
window.chrome.runtime = { connect: function(){}, sendMessage: function(){} };
delete window.__playwright;
delete window.__pw_manual;
"""

# ==================== 美团开店宝 fetch JS ====================
# 逐天查询，startTime 和 endTime 必须同一天
MEITUAN_DASHBOARD_FETCH_JS = """
async (args) => {
    try {
        const startTime = args.startTime;
        const endTime = args.endTime;
        const res = await fetch("https://ecom.meituan.com/emis/gw/TPcTradeAnalysisService/getCoreMetric?yodaReady", {
            method: "POST",
            headers: {
                "accept": "application/json, text/plain, */*",
                "content-type": "application/json;charset=UTF-8",
                "sec-ch-ua": '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-requested-with": "XMLHttpRequest"
            },
            body: JSON.stringify({
                startTime: startTime,
                endTime: endTime,
                granularity: "DAY",
                condition: {
                    poiId: "-1",
                    platform: 2,
                    tab: "6",
                    locationType: 1,
                    subType: "",
                    cmpType: "POP"
                }
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

# ==================== 抖音来客 fetch JS ====================
# 完整匹配浏览器抓包格式，包含 biz_params 和 life-account-id headers
DOUYIN_DASHBOARD_FETCH_JS = """
async (args) => {
    try {
        const res = await fetch("https://www.life-data.cn/api/dito/query", {
            method: "POST",
            headers: {
                "accept": "application/json, text/plain, */*",
                "content-type": "application/json",
                "life-account-id": String(args.lifeAccountId),
                "root-life-account-id": String(args.lifeAccountId),
                "priority": "u=1, i",
                "sec-ch-ua": '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-tt-trace-log": "01"
            },
            body: JSON.stringify({
                biz_params: {
                    path: "/dito/pc/home",
                    query: {},
                    first_render: false,
                    common_params: {
                        __partialAccountInfo: { isRootChainMerchant: false },
                        start_date: args.startDate,
                        end_date: args.endDate,
                        date_type: args.dateType
                    },
                    module_params: {
                        HomepageRealtimeProductRank: {
                            order_field: "pay_gmv",
                            order_type: "desc"
                        },
                        HomepageLivingRoomList: {},
                        HomepagePotentialTopic: {},
                        TradeAndProductSingle: {
                            start_date: args.startDate,
                            end_date: args.endDate
                        },
                        TradeAndProductPoiRank: {
                            start_date: args.startDate,
                            end_date: args.endDate
                        },
                        TradeAndProductRegionRank: {},
                        TradeAndProductProductRank: {
                            start_date: args.startDate,
                            end_date: args.endDate
                        },
                        FlowTranslateIndicatorAndFlowSource: {},
                        FlowTranslateIndicatorAndFlowSourceDSS: {},
                        FlowTranslatePaySource: {},
                        DateRangeSizer: {}
                    }
                },
                dito_params: {
                    is_event: true,
                    node_update_map: [
                        { type: "refresh", node: "DailyRealTimeProductRank_1" },
                        { type: "refresh", node: "LivingRoomAndPotentialTopic_1" },
                        { type: "refresh", node: "BusinessAndProductContainer" },
                        { type: "refresh", node: "TrafficAndConversionContainer" },
                        { type: "refresh", node: "TabComponent_1" }
                    ]
                }
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


# ==================== Playwright Worker ====================

def _write_result(filepath: str, data: dict):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, default=str)
        print(f"[DashboardSync] ✅ 结果写入: {os.path.basename(filepath)} status={data.get('status', '?')}", flush=True)
    except Exception as e:
        print(f"[DashboardSync] ❌ 写入结果失败: {e}", flush=True)


def _dashboard_sync_worker(
    task_id: str,
    platform: str,
    storage_state: dict,
    start_date: str,  # YYYY-MM-DD
    end_date: str,     # YYYY-MM-DD
    headless: bool,
    results_dir: str,
    life_account_id: str = "",  # 抖音需要
):
    """
    仪表盘同步 Worker — 在子进程中运行 Playwright

    流程:
    1. 启动浏览器 + 加载 storage_state
    2. 导航到平台页面建立登录态
    3. 使用 page.evaluate() 执行 fetch JS
    4. 解析返回数据，写入结果文件
    """
    from playwright.sync_api import sync_playwright

    print(f"\n{'='*60}", flush=True)
    print(f"[DashboardSync Worker] 🚀 启动 | 平台={platform} | 日期={start_date}~{end_date}", flush=True)
    print(f"[DashboardSync Worker] task_id={task_id} | headless={headless}", flush=True)
    print(f"{'='*60}", flush=True)

    done_file = os.path.join(results_dir, f"{task_id}_dashboard_done.json")

    # 平台配置
    if platform == "meituan":
        entry_url = "https://ecom.meituan.com/bizguide/trade-analysis/overview"
        cookie_domain = ".meituan.com"
    elif platform == "douyin":
        # 抖音来客仪表盘数据在 life-data.cn，但登录态在 life.douyin.com
        # 需要先访问 life.douyin.com 建立 SSO 登录态，再跳转到 life-data.cn 自动获得认证
        # 用户提供的正确跳转路径：
        #   1. 先访问 https://life.douyin.com/p/home
        #   2. 再跳转到 https://www.life-data.cn/?channel_id=laike_data_first_menu&groupid=...
        douyin_home_url = "https://life.douyin.com/p/home"
        douyin_dashboard_url = (
            f"https://www.life-data.cn/?channel_id=laike_data_first_menu&groupid={life_account_id}"
            if life_account_id
            else "https://www.life-data.cn/?channel_id=laike_data_first_menu"
        )
        entry_url = douyin_home_url  # 先到抖音主站建立登录态
        dashboard_url = douyin_dashboard_url  # 再跳转到仪表盘
        cookie_domain = ".life.douyin.com"
    else:
        _write_result(done_file, {"status": "failed", "error": f"不支持的平台: {platform}"})
        return

    browser = None
    context = None
    page = None
    pw = None

    try:
        pw = sync_playwright().start()

        # 验证 storage_state
        if not storage_state or not storage_state.get("cookies"):
            print(f"[DashboardSync Worker] ❌ storage_state 为空!", flush=True)
            _write_result(done_file, {"status": "failed", "error": "storage_state 为空，请重新登录"})
            return

        # 兼容：如果 cookies 是 dict {name: value}，转换成 Playwright 列表格式
        _cookies = storage_state.get("cookies")
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
            print(f"[DashboardSync Worker] 🔄 转换 cookies dict → list: {len(pw_cookies)} cookies", flush=True)
        else:
            print(f"[DashboardSync Worker] 📦 storage_state cookies 数量: {len(_cookies)}", flush=True)
            # 打印关键 cookie 名称（不打印值）
            cookie_names = [c.get("name", "?") if isinstance(c, dict) else str(c) for c in _cookies[:10]]
            print(f"[DashboardSync Worker] 📋 Cookie 名称(前10): {cookie_names}", flush=True)

        # 启动浏览器
        print(f"[DashboardSync Worker] 🌐 启动浏览器 (headless={headless})...", flush=True)
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
            print(f"[DashboardSync Worker] ⚠️ Chrome channel 启动失败，使用默认 Chromium", flush=True)
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
        page.on("console", lambda msg: print(f"[Browser Console] {msg.type}: {msg.text}", flush=True))

        # 导航到平台页面建立登录态
        is_douyin = platform == "douyin"
        wait_strategy = "domcontentloaded" if is_douyin else "networkidle"
        goto_timeout = 60000 if is_douyin else 30000

        # 第一步：导航到入口 URL（美团直接到目标页，抖音先到 life.douyin.com 建立 SSO）
        print(f"[DashboardSync Worker] 🔗 第一步：导航到 {entry_url}...", flush=True)
        try:
            page.goto(entry_url, wait_until=wait_strategy, timeout=goto_timeout)
            print(f"[DashboardSync Worker] ✅ 第一步页面加载完成: {page.url}", flush=True)
        except Exception as e:
            print(f"[DashboardSync Worker] ⚠️ page.goto 警告: {e}, 继续执行", flush=True)

        page.wait_for_timeout(3000 if not is_douyin else 5000)

        # 检查是否被重定向到登录页（第一步）
        current_url = page.url
        print(f"[DashboardSync Worker] 📍 第一步后当前页面URL: {current_url}", flush=True)
        if "login" in current_url.lower() or "passport" in current_url.lower():
            print(f"[DashboardSync Worker] ❌ 登录态已失效! 被重定向到: {current_url}", flush=True)
            _write_result(done_file, {
                "status": "failed",
                "error": "登录态已失效，被重定向到登录页面",
                "current_url": current_url,
            })
            return

        # 抖音专属：第二步跳转到 life-data.cn 触发 SSO 自动登录
        if is_douyin and dashboard_url:
            print(f"\n[DashboardSync Worker] 🔗 第二步（抖音SSO）：跳转到 {dashboard_url}...", flush=True)
            try:
                page.goto(dashboard_url, wait_until="domcontentloaded", timeout=60000)
                print(f"[DashboardSync Worker] ✅ 第二步页面加载完成: {page.url}", flush=True)
            except Exception as e:
                print(f"[DashboardSync Worker] ⚠️ 第二步跳转警告: {e}, 继续执行", flush=True)

            # 等待 SSO 完成（关键！）
            print(f"[DashboardSync Worker] ⏳ 等待 SSO 登录完成...", flush=True)
            page.wait_for_timeout(8000)  # 等待 8 秒让 SSO 完成

            # 检查跳转后是否被重定向到登录页
            current_url = page.url
            print(f"[DashboardSync Worker] 📍 第二步后当前页面URL: {current_url}", flush=True)
            if "login" in current_url.lower() or "passport" in current_url.lower():
                print(f"[DashboardSync Worker] ❌ SSO 跳转失败! 被重定向到: {current_url}", flush=True)
                print(f"[DashboardSync Worker] 💡 提示: 请确认 life_account_id={life_account_id} 是否正确", flush=True)
                _write_result(done_file, {
                    "status": "failed",
                    "error": "SSO 跳转失败，请重新登录抖音来客并保存 cookie",
                    "current_url": current_url,
                })
                return

            print(f"[DashboardSync Worker] ✅ SSO 登录成功! 当前页面: {current_url}", flush=True)

        # ==================== 执行同步 ====================

        print(f"[DashboardSync Worker] 🔍 开始执行 {platform} 仪表盘数据同步...", flush=True)

        if platform == "meituan":
            result = _sync_meituan_in_browser(page, start_date, end_date)
        elif platform == "douyin":
            result = _sync_douyin_in_browser(page, start_date, end_date, life_account_id)
        else:
            result = {"status": "failed", "error": f"不支持的平台: {platform}"}

        print(f"\n[DashboardSync Worker] 📊 同步结果: status={result.get('status')}", flush=True)
        if result.get("status") == "success":
            if platform == "meituan":
                print(f"  营业额数据点: {len(result.get('revenue_data', []))}", flush=True)
                print(f"  门店指标日期数: {len(result.get('metrics_data', {}))}", flush=True)
                # 打印前3天的营业额样本
                for item in result.get("revenue_data", [])[:3]:
                    print(f"    {item.get('date')}: ¥{item.get('yNumber')}", flush=True)
            elif platform == "douyin":
                print(f"  原始数据 keys: {list(result.get('raw_data', {}).keys())[:5]}", flush=True)
        else:
            print(f"  ❌ 错误: {result.get('error', '未知')}", flush=True)

        _write_result(done_file, result)

    except Exception as e:
        print(f"[DashboardSync Worker] ❌ 异常: {e}", flush=True)
        import traceback
        traceback.print_exc()
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


def _sync_meituan_in_browser(page, start_date: str, end_date: str) -> dict:
    """
    在浏览器中逐天同步美团开店宝仪表盘数据

    美团 API 要求 startTime 和 endTime 必须同一天
    """
    from datetime import datetime, timedelta as _td

    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()

    all_revenue_data = []  # [{date: "YYYY/MM/DD", yNumber: float}]
    all_metrics_data = {}   # {date_str: {metric_name: metric_value}}

    total_days = (end - start).days + 1
    print(f"\n[美团] 📅 查询范围: {start_date} ~ {end_date} (共 {total_days} 天)", flush=True)

    current = start
    day_idx = 0
    while current <= end:
        day_idx += 1
        # 同一天的 00:00:00 ~ 23:59:59
        day_start = datetime.combine(current, datetime.min.time())
        day_end = datetime.combine(current, datetime.max.time())

        start_ts = int(day_start.timestamp() * 1000)
        end_ts = int(day_end.timestamp() * 1000)

        print(f"[美团] [{day_idx}/{total_days}] 查询 {current.strftime('%Y-%m-%d')} (startTime={start_ts}, endTime={end_ts})", flush=True)

        try:
            result = page.evaluate(MEITUAN_DASHBOARD_FETCH_JS, {
                "startTime": start_ts,
                "endTime": end_ts,
            })

            if not result:
                print(f"[美团] ⚠️ {current}: 返回为空!", flush=True)
                current += _td(days=1)
                continue

            http_status = result.get("_status", 0)
            error_info = result.get("error")

            # 打印原始响应摘要
            top_keys = [k for k in result.keys() if k != "_status"][:5]
            print(f"[美团] {current}: HTTP={http_status}, 顶级keys={top_keys}", flush=True)

            # 检查 API 错误
            if error_info:
                print(f"[美团] ⚠️ {current}: fetch错误 {str(error_info)[:200]}", flush=True)
                current += _td(days=1)
                continue

            # 检查业务错误
            api_error = result.get("error", {})
            if isinstance(api_error, dict) and api_error.get("code"):
                print(
                    f"[美团] ⚠️ {current}: API业务错误 code={api_error.get('code')}, "
                    f"message={api_error.get('message', '')[:200]}",
                    flush=True
                )
                current += _td(days=1)
                continue

            # 解析营业额数据
            data = result.get("data", result)
            sub = data.get("subBaseModule", {}) if isinstance(data, dict) else {}
            summaries = sub.get("summariesMethod", [])

            day_revenue_count = 0
            for summary in summaries:
                line_cards = summary.get("lineCardList", [])
                for card in line_cards:
                    graphs = card.get("lineGraphs", [])
                    for graph in graphs:
                        title = graph.get("title", "")
                        if title != "当前汇总":
                            continue
                        points = graph.get("points", [])
                        for point in points:
                            x_val = point.get("x", "")
                            y_number = point.get("yNumber", 0)
                            if x_val and y_number is not None:
                                all_revenue_data.append({
                                    "date": x_val,
                                    "yNumber": y_number,
                                })
                                day_revenue_count += 1

            # 解析门店指标
            summary_rows = sub.get("summaries", [])
            date_str = current.strftime("%Y/%m/%d")
            day_metrics_count = 0
            for summary in summary_rows:
                rows = summary.get("rows", [])
                for row_group in rows:
                    for item in row_group:
                        name = item.get("name", "")
                        value = item.get("value", "0")
                        if name and date_str not in all_metrics_data:
                            all_metrics_data[date_str] = {}
                        if name:
                            try:
                                all_metrics_data.setdefault(date_str, {})[name] = float(value)
                                day_metrics_count += 1
                            except (ValueError, TypeError):
                                pass

            print(
                f"[美团] ✅ {current}: HTTP={http_status}, "
                f"营业额点数={day_revenue_count}, 指标数={day_metrics_count}",
                flush=True
            )

            # 打印当天的营业额数据样本
            if day_revenue_count > 0:
                latest = all_revenue_data[-1]
                print(f"[美团]   💰 营业额: {latest.get('date')} = ¥{latest.get('yNumber')}", flush=True)

        except Exception as e:
            print(f"[美团] ❌ {current}: 异常 {e}", flush=True)
            import traceback
            traceback.print_exc()
            current += _td(days=1)
            continue

        # 避免请求过快
        time.sleep(0.3)
        current += _td(days=1)

    # 汇总统计
    print(f"\n[美团] 📊 同步完成!", flush=True)
    print(f"  总营业额数据点: {len(all_revenue_data)}", flush=True)
    print(f"  总门店指标日期: {len(all_metrics_data)}", flush=True)

    if all_revenue_data:
        total_amount = sum(item.get("yNumber", 0) for item in all_revenue_data)
        print(f"  总营业额合计: ¥{total_amount:,.2f}", flush=True)

    return {
        "status": "success",
        "platform": "meituan",
        "revenue_data": all_revenue_data,
        "metrics_data": all_metrics_data,
    }


def _sync_douyin_in_browser(page, start_date: str, end_date: str, life_account_id: str) -> dict:
    """
    在浏览器中同步抖音来客仪表盘数据

    使用正确的 biz_params 格式和 life-account-id headers
    """
    print(f"\n[抖音] 🎬 开始同步抖音来客数据", flush=True)
    print(f"[抖音] life_account_id={life_account_id}", flush=True)

    if not life_account_id:
        print(f"[抖音] ❌ 缺少 life_account_id!", flush=True)
        return {"status": "failed", "error": "抖音账号缺少 life_account_id，请先同步店铺"}

    # 计算日期类型
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()
    days_diff = (end - start).days

    if days_diff <= 1:
        date_type = "last_one_days"
    elif days_diff <= 6:
        date_type = "last_seven_days"
    elif days_diff <= 13:
        date_type = "last_fourteen_days"
    elif days_diff <= 29:
        date_type = "last_thirty_days"
    else:
        date_type = "nature_month"

    print(
        f"[抖音] 📅 查询 {start_date} ~ {end_date} "
        f"(共{days_diff + 1}天, date_type={date_type})",
        flush=True
    )

    try:
        result = page.evaluate(DOUIN_DASHBOARD_FETCH_JS, {
            "lifeAccountId": life_account_id,
            "startDate": start_date,
            "endDate": end_date,
            "dateType": date_type,
        })

        if not result:
            print(f"[抖音] ❌ API 返回为空!", flush=True)
            return {"status": "failed", "error": "抖音来客 API 返回为空"}

        http_status = result.get("_status", 0)
        error_info = result.get("error")
        code = result.get("code")

        # 打印原始响应摘要
        top_keys = [k for k in result.keys() if k not in ("_status",)][:8]
        print(f"[抖音] HTTP={http_status}, code={code}, 顶级keys={top_keys}", flush=True)

        if error_info:
            print(f"[抖音] ❌ fetch 错误: {str(error_info)[:200]}", flush=True)
            return {"status": "failed", "error": f"抖音来客 fetch 错误: {str(error_info)[:200]}"}

        if http_status == 401:
            print(f"[抖音] ❌ 登录态已失效(401)!", flush=True)
            return {"status": "failed", "error": "抖音来客登录态已失效(401)，请重新登录"}

        # 检查业务返回码
        if code and code != 0:
            print(f"[抖音] ❌ API 业务错误: code={code}", flush=True)
            return {"status": "failed", "error": f"抖音来客 API 错误: code={code}"}

        # 解析数据结构
        data = result.get("data", result)
        if isinstance(data, dict):
            layout = data.get("layout", [])
            print(f"[抖音] 📊 layout 层数: {len(layout)}", flush=True)

            # 递归查找关键模块类型
            def _find_modules(nodes, depth=0):
                found = []
                if not isinstance(nodes, list):
                    return found
                for node in nodes:
                    if not isinstance(node, dict):
                        continue
                    sub_type = node.get("subType", "")
                    if sub_type:
                        found.append(sub_type)
                    children = node.get("children", [])
                    if children:
                        found.extend(_find_modules(children, depth + 1))
                return found

            modules = _find_modules(layout)
            print(f"[抖音] 📋 发现的模块类型: {modules[:15]}", flush=True)

            # 递归搜索 layout 结构中指定 key 的数据（内联版本，不依赖类方法）
            def _find_in_layout_inline(obj, key):
                results = []
                if not isinstance(obj, dict):
                    return results
                if key in obj:
                    val = obj[key]
                    if isinstance(val, dict) and val.get("code") is not None:
                        results.append(val)
                    elif isinstance(val, list):
                        for item in val:
                            if isinstance(item, dict):
                                results.append(item)
                for sub_key in ["children", "data", "layout"]:
                    sub = obj.get(sub_key)
                    if isinstance(sub, list):
                        for item in sub:
                            results.extend(_find_in_layout_inline(item, key))
                    elif isinstance(sub, dict):
                        results.extend(_find_in_layout_inline(sub, key))
                return results

            # 查找 hourTrends 数据
            hour_trends = _find_in_layout_inline(data, "hourTrends")
            if hour_trends:
                for ht in hour_trends:
                    hours = ht.get("data", [])
                    if hours:
                        print(f"[抖音] ⏰ 小时趋势数据: {len(hours)} 个小时", flush=True)
                        for h in hours[:2]:
                            print(f"  {h.get('hour')}: 成交{h.get('pay_gmv', 0)}元/{h.get('pay_cert_cnt', 0)}券", flush=True)

            # 查找实时指标
            realtime = _find_in_layout_inline(data, "realtimeIndicator")
            print(f"[抖音] 📈 实时指标数据: {len(realtime)} 个", flush=True)

            # 查找商品排行
            product_rank = _find_in_layout_inline(data, "DailyRealTimeProductRank")
            print(f"[抖音] 🏆 商品排行数据: {len(product_rank)} 个", flush=True)

        print(f"[抖音] ✅ 数据获取成功!", flush=True)

        return {
            "status": "success",
            "platform": "douyin",
            "raw_data": result.get("data", result),
        }

    except Exception as e:
        print(f"[抖音] ❌ 异常: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return {"status": "failed", "error": str(e)}


# ==================== 数据解析与存储 ====================

class DashboardSyncService:
    """仪表盘数据同步服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ==================== 同步入口 ====================

    async def sync_meituan_dashboard(
        self,
        account_id: UUID,
        start_date: date,
        end_date: date,
        store_id: Optional[UUID] = None,
    ) -> dict:
        """同步美团开店宝仪表盘数据"""
        logger.info(f"[美团] 🚀 开始同步美团开店宝 | account_id={account_id} | {start_date}~{end_date}")

        account = await self._get_account(account_id)
        if not account:
            logger.error(f"[美团] ❌ 平台账号不存在: {account_id}")
            return {"success": False, "error": "平台账号不存在"}

        storage_state = await self._get_storage_state(account)
        if not storage_state:
            logger.error(f"[美团] ❌ storage_state 为空，登录态已失效")
            return {"success": False, "error": "美团登录态已失效，请重新扫码登录"}

        logger.info(f"[美团] ✅ storage_state 获取成功, cookies数={len(storage_state.get('cookies', []))}")

        target_store_id = store_id or await self._get_first_store_for_account(account_id)
        if not target_store_id:
            logger.error(f"[美团] ❌ 未找到关联门店")
            return {"success": False, "error": "未找到关联门店，请先绑定门店"}

        logger.info(f"[美团] 📍 目标门店: {target_store_id}")

        try:
            # 启动 Playwright worker 进程
            result = await self._run_playwright_sync(
                platform="meituan",
                storage_state=storage_state,
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
            )

            if result.get("status") != "success":
                return {"success": False, "error": result.get("error", "同步失败")}

            # 解析并存储营业额数据
            revenue_count = await self._store_meituan_revenue(
                result.get("revenue_data", []),
                target_store_id,
                start_date,
                end_date,
            )
            logger.info(f"[美团] 💰 营业额记录入库: {revenue_count} 条")

            # 解析并存储门店指标
            metric_count = await self._store_meituan_metrics(
                result.get("metrics_data", {}),
                target_store_id,
                start_date,
                end_date,
            )
            logger.info(f"[美团] 📊 门店指标入库: {metric_count} 条")

            # 更新同步时间
            account.last_sync_at = datetime.utcnow()
            await self.db.commit()

            logger.info(f"[美团] ✅ 同步完成! revenue={revenue_count}, metric={metric_count}")

            return {
                "success": True,
                "platform": "meituan",
                "revenue_records": revenue_count,
                "metric_records": metric_count,
            }

        except Exception as e:
            logger.error(f"同步美团开店宝数据失败: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def sync_douyin_dashboard(
        self,
        account_id: UUID,
        start_date: date,
        end_date: date,
        store_id: Optional[UUID] = None,
    ) -> dict:
        """同步抖音来客仪表盘数据"""
        logger.info(f"[抖音] 🚀 开始同步抖音来客 | account_id={account_id} | {start_date}~{end_date}")

        account = await self._get_account(account_id)
        if not account:
            logger.error(f"[抖音] ❌ 平台账号不存在: {account_id}")
            return {"success": False, "error": "平台账号不存在"}

        storage_state = await self._get_storage_state(account)
        if not storage_state:
            logger.error(f"[抖音] ❌ storage_state 为空，登录态已失效")
            return {"success": False, "error": "抖音来客登录态已失效，请重新登录"}

        logger.info(f"[抖音] ✅ storage_state 获取成功, cookies数={len(storage_state.get('cookies', []))}")

        target_store_id = store_id or await self._get_first_store_for_account(account_id)
        if not target_store_id:
            logger.error(f"[抖音] ❌ 未找到关联门店")
            return {"success": False, "error": "未找到关联门店，请先绑定门店"}

        # 获取 life_account_id
        life_account_id = account.platform_account_id or ""
        logger.info(f"[抖音] 📱 platform_account_id={life_account_id}")
        if not life_account_id:
            # 尝试从绑定的店铺中获取
            life_account_id = await self._get_douyin_life_account_id(account_id)
            logger.info(f"[抖音] 📱 从 StorePlatform 获取 life_account_id={life_account_id}")

        if not life_account_id:
            logger.error(f"[抖音] ❌ 缺少 life_account_id!")
            return {"success": False, "error": "抖音账号缺少 life_account_id，请先同步店铺数据"}

        logger.info(f"[抖音] 📍 目标门店: {target_store_id}, life_account_id: {life_account_id}")

        try:
            # 启动 Playwright worker 进程
            result = await self._run_playwright_sync(
                platform="douyin",
                storage_state=storage_state,
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
                life_account_id=life_account_id,
            )

            if result.get("status") != "success":
                return {"success": False, "error": result.get("error", "同步失败")}

            # 解析并存储抖音数据
            raw_data = result.get("raw_data", {})
            logger.info(f"[抖音] 📦 开始解析原始数据, keys={list(raw_data.keys())[:5] if isinstance(raw_data, dict) else 'N/A'}")

            metric_count = await self._store_douyin_realtime(raw_data, target_store_id, end_date)
            logger.info(f"[抖音] 📊 实时指标入库: {metric_count} 条")

            revenue_count = await self._store_douyin_hourly(raw_data, target_store_id, end_date)
            logger.info(f"[抖音] 💰 小时趋势入库: {revenue_count} 条")

            package_count = await self._store_douyin_products(raw_data, target_store_id, start_date, end_date)
            logger.info(f"[抖音] 🏆 商品排行入库: {package_count} 条")

            # 更新同步时间
            account.last_sync_at = datetime.utcnow()
            await self.db.commit()

            logger.info(f"[抖音] ✅ 同步完成! revenue={revenue_count}, metric={metric_count}, package={package_count}")

            return {
                "success": True,
                "platform": "douyin",
                "revenue_records": revenue_count,
                "metric_records": metric_count,
                "package_records": package_count,
            }

        except Exception as e:
            logger.error(f"同步抖音来客数据失败: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def sync_all_platforms(
        self,
        user_id: UUID,
        start_date: date,
        end_date: date,
        store_id: Optional[UUID] = None,
    ) -> dict:
        """同步用户所有已连接平台的仪表盘数据"""
        logger.info(f"[DashboardSync] 🚀 开始全平台同步 | user_id={user_id} | {start_date}~{end_date}")
        results = []

        # 获取用户所有有效平台账号
        stmt = select(PlatformAccount).where(
            PlatformAccount.user_id == user_id,
            PlatformAccount.cookies_status == "valid",
        )
        db_result = await self.db.execute(stmt)
        accounts = list(db_result.scalars().all())

        if not accounts:
            logger.warning(f"[DashboardSync] ⚠️ 无有效的平台账号")
            return {
                "success": False,
                "error": "无有效的平台账号，请先连接平台",
                "results": [],
            }

        logger.info(f"[DashboardSync] 📱 发现 {len(accounts)} 个有效平台账号")
        for acc in accounts:
            logger.info(f"  - {acc.platform} (id={acc.id}, status={acc.cookies_status})")

        for account in accounts:
            if account.platform == "meituan":
                result = await self.sync_meituan_dashboard(
                    account.id, start_date, end_date, store_id
                )
                results.append(result)
            elif account.platform == "douyin":
                result = await self.sync_douyin_dashboard(
                    account.id, start_date, end_date, store_id
                )
                results.append(result)
            elif account.platform == "dianping":
                # 大众点评复用美团的API（同属美团体系）
                result = await self.sync_meituan_dashboard(
                    account.id, start_date, end_date, store_id
                )
                result["platform"] = "dianping"
                results.append(result)

        total_revenue = sum(r.get("revenue_records", 0) for r in results if r.get("success"))
        total_metric = sum(r.get("metric_records", 0) for r in results if r.get("success"))
        total_package = sum(r.get("package_records", 0) for r in results if r.get("success"))

        return {
            "success": True,
            "results": results,
            "summary": {
                "platforms_synced": len([r for r in results if r.get("success")]),
                "total_revenue_records": total_revenue,
                "total_metric_records": total_metric,
                "total_package_records": total_package,
            },
        }

    # ==================== Playwright 执行 ====================

    async def _run_playwright_sync(
        self,
        platform: str,
        storage_state: dict,
        start_date: str,
        end_date: str,
        life_account_id: str = "",
    ) -> dict:
        """启动 Playwright 子进程并等待结果"""
        os.makedirs(_RESULTS_DIR, exist_ok=True)

        task_id = str(uuid4())
        done_file = os.path.join(_RESULTS_DIR, f"{task_id}_dashboard_done.json")

        # 清理旧文件
        if os.path.exists(done_file):
            os.remove(done_file)

        logger.info(f"[DashboardSync] 🚀 启动 Playwright 同步 | 平台={platform} | 日期={start_date}~{end_date}")

        # 启动 worker 进程
        process = multiprocessing.Process(
            target=_dashboard_sync_worker,
            args=(task_id, platform, storage_state, start_date, end_date, HEADLESS, _RESULTS_DIR, life_account_id),
            daemon=True,
            name=f"dashboard-sync-{task_id[:8]}",
        )
        process.start()
        logger.info(f"[DashboardSync] 子进程已启动 pid={process.pid} for {platform}")

        # 轮询等待结果
        max_polls = int(DASHBOARD_SYNC_TIMEOUT * 2)
        poll_count = 0
        for _ in range(max_polls):
            await asyncio.sleep(0.5)
            poll_count += 1

            # 每 10 秒打印一次等待状态
            if poll_count % 20 == 0:
                elapsed = poll_count * 0.5
                logger.info(f"[DashboardSync] ⏳ 等待子进程完成... 已等 {elapsed:.0f}秒 (pid={process.pid})")

            if os.path.exists(done_file):
                try:
                    with open(done_file, "r", encoding="utf-8") as f:
                        result = json.load(f)
                    # 清理临时文件
                    try:
                        os.remove(done_file)
                    except Exception:
                        pass
                    logger.info(f"[DashboardSync] ✅ 子进程完成! status={result.get('status')}")
                    return result
                except Exception as e:
                    logger.error(f"[DashboardSync] 读取结果文件失败: {e}")

        # 超时
        logger.error(f"[DashboardSync] ❌ 同步超时 ({DASHBOARD_SYNC_TIMEOUT}秒)!")
        try:
            if process.is_alive():
                process.terminate()
        except Exception:
            pass

        return {"status": "failed", "error": f"仪表盘同步超时（{DASHBOARD_SYNC_TIMEOUT}秒）"}

    # ==================== 数据存储 ====================

    async def _store_meituan_revenue(
        self,
        revenue_data: list,
        store_id: UUID,
        start_date: date,
        end_date: date,
    ) -> int:
        """存储美团营业额数据到 RevenueRecord"""
        count = 0
        for item in revenue_data:
            x_val = item.get("date", "")
            y_number = item.get("yNumber", 0)

            if not x_val or y_number is None:
                continue

            try:
                record_date = datetime.strptime(x_val, "%Y/%m/%d").date()
            except ValueError:
                continue

            if record_date < start_date or record_date > end_date:
                continue

            existing = await self._find_revenue_record(store_id, record_date)

            if existing:
                existing.meituan_revenue = y_number
                existing.total_revenue = (
                    existing.meituan_revenue
                    + existing.douyin_revenue
                    + existing.other_revenue
                )
            else:
                record = RevenueRecord(
                    store_id=store_id,
                    record_date=record_date,
                    total_revenue=y_number,
                    meituan_revenue=y_number,
                    douyin_revenue=0,
                    other_revenue=0,
                    visitor_count=0,
                    table_count=0,
                    avg_people_per_table=0,
                    avg_per_capita=0,
                    notes="美团开店宝自动同步",
                )
                self.db.add(record)

            count += 1

        if count > 0:
            await self.db.flush()

        return count

    async def _store_meituan_metrics(
        self,
        metrics_data: dict,
        store_id: UUID,
        start_date: date,
        end_date: date,
    ) -> int:
        """存储美团门店指标到 StoreMetric"""
        count = 0
        for date_str, metrics in metrics_data.items():
            try:
                record_date = datetime.strptime(date_str, "%Y/%m/%d").date()
            except ValueError:
                continue

            if record_date < start_date or record_date > end_date:
                continue

            existing = await self._find_store_metric(store_id, record_date, "meituan")

            notes_parts = []
            for metric_name, metric_value in metrics.items():
                if existing:
                    if "营业门店数" in metric_name:
                        existing.new_favorites = int(metric_value)
                    elif "在线门店数" in metric_name or "交易在线门店数" in metric_name:
                        existing.scan_count = int(metric_value)
                    elif "动销门店数" in metric_name:
                        existing.checkins = int(metric_value)
                notes_parts.append(f"{metric_name}={metric_value}")

            if not existing:
                metric = StoreMetric(
                    store_id=store_id,
                    metric_date=record_date,
                    platform="meituan",
                    notes="美团开店宝同步: " + ", ".join(notes_parts[:3]),
                )
                for metric_name, metric_value in metrics.items():
                    if "营业门店数" in metric_name:
                        metric.new_favorites = int(metric_value)
                    elif "在线门店数" in metric_name or "交易在线门店数" in metric_name:
                        metric.scan_count = int(metric_value)
                    elif "动销门店数" in metric_name:
                        metric.checkins = int(metric_value)

                self.db.add(metric)
                count += 1

        if count > 0:
            await self.db.flush()

        return count

    async def _store_douyin_realtime(
        self,
        data: dict,
        store_id: UUID,
        record_date: date,
    ) -> int:
        """存储抖音来客实时指标"""
        count = 0
        try:
            indicators = self._find_in_layout(data, "realtimeIndicator")
            if not indicators:
                # 也搜索 hourTrends 中的汇总数据
                hour_trends = self._find_in_layout(data, "hourTrends")
                if hour_trends:
                    for trend in hour_trends:
                        hours = trend.get("data", [])
                        if not hours:
                            continue
                        # 汇总所有小时的数据
                        total_pay_gmv = sum(h.get("pay_gmv", 0) or 0 for h in hours)
                        total_pay_cert = sum(h.get("pay_cert_cnt", 0) or 0 for h in hours)
                        total_verify_gmv = sum(h.get("verify_gmv", 0) or 0 for h in hours)
                        total_verify_cert = sum(h.get("verify_cert_cnt", 0) or 0 for h in hours)
                        total_refund_gmv = sum(h.get("refund_gmv", 0) or 0 for h in hours)
                        total_refund_cert = sum(h.get("refund_cert_cnt", 0) or 0 for h in hours)
                        total_product_uv = sum(h.get("project_detail_product_show_uv", 0) or 0 for h in hours)

                        # 抖音数据中 gmv 单位是分，需要转换为元
                        pay_gmv_yuan = round(total_pay_gmv / 100, 2) if total_pay_gmv > 100 else total_pay_gmv
                        verify_gmv_yuan = round(total_verify_gmv / 100, 2) if total_verify_gmv > 100 else total_verify_gmv

                        # 更新 RevenueRecord
                        rev_existing = await self._find_revenue_record(store_id, record_date)
                        if rev_existing:
                            rev_existing.douyin_revenue = pay_gmv_yuan
                            rev_existing.total_revenue = (
                                rev_existing.meituan_revenue
                                + rev_existing.douyin_revenue
                                + rev_existing.other_revenue
                            )
                        else:
                            record = RevenueRecord(
                                store_id=store_id,
                                record_date=record_date,
                                total_revenue=pay_gmv_yuan,
                                meituan_revenue=0,
                                douyin_revenue=pay_gmv_yuan,
                                other_revenue=0,
                                visitor_count=0,
                                table_count=0,
                                avg_people_per_table=0,
                                avg_per_capita=0,
                                notes="抖音来客自动同步",
                            )
                            self.db.add(record)
                            count += 1

                        # 更新 StoreMetric
                        metric_existing = await self._find_store_metric(store_id, record_date, "douyin")
                        if metric_existing:
                            metric_existing.purchases = total_pay_cert
                            metric_existing.verifications = total_verify_cert
                            metric_existing.product_impressions = total_product_uv
                        else:
                            metric = StoreMetric(
                                store_id=store_id,
                                metric_date=record_date,
                                platform="douyin",
                                purchases=total_pay_cert,
                                verifications=total_verify_cert,
                                product_impressions=total_product_uv,
                                notes=f"抖音来客同步: 成交{pay_gmv_yuan}元/{total_pay_cert}券, 核销{verify_gmv_yuan}元/{total_verify_cert}券",
                            )
                            self.db.add(metric)
                            count += 1

                if count > 0:
                    await self.db.flush()
                return count

            for indicator_data in indicators:
                rows = indicator_data.get("data", [])
                if not rows:
                    continue

                for row in rows:
                    pay_gmv = row.get("pay_gmv", 0) or 0
                    pay_cert_cnt = row.get("pay_cert_cnt", 0) or 0
                    verify_gmv = row.get("verify_gmv", 0) or 0
                    verify_cert_cnt = row.get("verify_cert_cnt", 0) or 0
                    product_uv = row.get("project_detail_product_show_uv", 0) or 0

                    # 判断 gmv 单位：如果大于10000则认为是分，否则是元
                    pay_gmv_yuan = round(pay_gmv / 100, 2) if pay_gmv > 10000 else pay_gmv

                    # 更新 RevenueRecord
                    rev_existing = await self._find_revenue_record(store_id, record_date)
                    if rev_existing:
                        rev_existing.douyin_revenue = pay_gmv_yuan
                        rev_existing.total_revenue = (
                            rev_existing.meituan_revenue
                            + rev_existing.douyin_revenue
                            + rev_existing.other_revenue
                        )
                    else:
                        record = RevenueRecord(
                            store_id=store_id,
                            record_date=record_date,
                            total_revenue=pay_gmv_yuan,
                            meituan_revenue=0,
                            douyin_revenue=pay_gmv_yuan,
                            other_revenue=0,
                            visitor_count=0,
                            table_count=0,
                            avg_people_per_table=0,
                            avg_per_capita=0,
                            notes="抖音来客自动同步",
                        )
                        self.db.add(record)

                    # 更新 StoreMetric
                    metric_existing = await self._find_store_metric(store_id, record_date, "douyin")
                    if metric_existing:
                        metric_existing.purchases = pay_cert_cnt
                        metric_existing.verifications = verify_cert_cnt
                        metric_existing.product_impressions = product_uv
                    else:
                        metric = StoreMetric(
                            store_id=store_id,
                            metric_date=record_date,
                            platform="douyin",
                            purchases=pay_cert_cnt,
                            verifications=verify_cert_cnt,
                            product_impressions=product_uv,
                            notes=f"抖音来客同步: 成交{pay_gmv_yuan}元/{pay_cert_cnt}券, 核销券数={verify_cert_cnt}",
                        )
                        self.db.add(metric)
                        count += 1

            if count > 0:
                await self.db.flush()

        except Exception as e:
            logger.error(f"存储抖音实时指标失败: {e}", exc_info=True)

        return count

    async def _store_douyin_hourly(
        self,
        data: dict,
        store_id: UUID,
        record_date: date,
    ) -> int:
        """存储抖音来客小时趋势数据"""
        count = 0
        try:
            hour_trends = self._find_in_layout(data, "hourTrends")
            if not hour_trends:
                return 0

            for trend_data in hour_trends:
                hours = trend_data.get("data", [])
                total_gmv = 0  # 分

                for hour_item in hours:
                    pay_gmv = hour_item.get("pay_gmv", 0) or 0
                    total_gmv += pay_gmv

                # 如果 gmv 大于 10000，则认为是分；否则是元
                total_gmv_yuan = round(total_gmv / 100, 2) if total_gmv > 10000 else total_gmv

                rev_existing = await self._find_revenue_record(store_id, record_date)
                if rev_existing:
                    # 取小时汇总和实时指标中较大的值
                    rev_existing.douyin_revenue = max(
                        rev_existing.douyin_revenue, total_gmv_yuan
                    )
                    rev_existing.total_revenue = (
                        rev_existing.meituan_revenue
                        + rev_existing.douyin_revenue
                        + rev_existing.other_revenue
                    )
                    count += 1

            if count > 0:
                await self.db.flush()

        except Exception as e:
            logger.error(f"存储抖音小时趋势数据失败: {e}", exc_info=True)

        return count

    async def _store_douyin_products(
        self,
        data: dict,
        store_id: UUID,
        start_date: date,
        end_date: date,
    ) -> int:
        """存储抖音来客商品排行到 PackageRecord"""
        count = 0
        try:
            product_ranks = self._find_in_layout(data, "productRank")
            if not product_ranks:
                product_ranks = self._find_in_layout(data, "DailyRealTimeProductRank")

            if not product_ranks:
                return 0

            for rank_data in product_ranks:
                products = rank_data.get("data", rank_data.get("productRank", []))
                if isinstance(products, dict):
                    products = products.get("list", [])

                for product in products:
                    product_name = product.get("product_name", product.get("name", ""))
                    if not product_name:
                        continue

                    pay_cnt = product.get("pay_cert_cnt", product.get("pay_cnt", 0)) or 0
                    verify_cnt = product.get("verify_cert_cnt", product.get("verify_cnt", 0)) or 0

                    existing = await self._find_package_record(
                        store_id, product_name, start_date, end_date
                    )

                    if existing:
                        existing.douyin_buy = (existing.douyin_buy or 0) + pay_cnt
                        existing.douyin_verify = (existing.douyin_verify or 0) + verify_cnt
                    else:
                        record = PackageRecord(
                            store_id=store_id,
                            period_start=start_date,
                            period_end=end_date,
                            product_name=product_name,
                            meituan_buy=0,
                            meituan_verify=0,
                            douyin_buy=pay_cnt,
                            douyin_verify=verify_cnt,
                            notes="抖音来客自动同步",
                        )
                        self.db.add(record)
                        count += 1

            if count > 0:
                await self.db.flush()

        except Exception as e:
            logger.error(f"存储抖音商品排行数据失败: {e}", exc_info=True)

        return count

    # ==================== 工具方法 ====================

    async def _get_account(self, account_id: UUID) -> Optional[PlatformAccount]:
        """获取平台账号"""
        stmt = select(PlatformAccount).where(PlatformAccount.id == account_id).limit(1)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def _get_storage_state(self, account: PlatformAccount) -> Optional[dict]:
        """
        获取平台账号的 storage_state（Playwright 格式）

        cookies_encrypted 存储的是 base64 编码的 JSON，
        解密后可能包含 _storage_state 字段（Playwright 格式）
        """
        if not account.cookies_encrypted:
            logger.warning(f"[DashboardSync] ⚠️ account {account.id} cookies_encrypted 为空")
            return None

        try:
            platform_svc = PlatformService(self.db)
            credentials = await platform_svc._decrypt_credentials(account.cookies_encrypted)

            logger.info(f"[DashboardSync] 🔓 解密 credentials 成功, type={type(credentials).__name__}")

            # 尝试多种格式
            if isinstance(credentials, dict):
                # 格式1: 直接是 storage_state
                if credentials.get("cookies"):
                    logger.info(f"[DashboardSync] ✅ 格式1: 直接 storage_state, cookies数={len(credentials.get('cookies', []))}")
                    return credentials

                # 格式2: 包含 _storage_state 字段
                storage_state = credentials.get("_storage_state")
                if storage_state and isinstance(storage_state, dict):
                    logger.info(f"[DashboardSync] ✅ 格式2: _storage_state, cookies数={len(storage_state.get('cookies', []))}")
                    return storage_state

                # 格式3: 包含 cookies 字段，里面有 _storage_state
                cookies_data = credentials.get("cookies", {})
                if isinstance(cookies_data, dict):
                    storage_state = cookies_data.get("_storage_state")
                    if storage_state and isinstance(storage_state, dict):
                        logger.info(f"[DashboardSync] ✅ 格式3: cookies._storage_state, cookies数={len(storage_state.get('cookies', []))}")
                        return storage_state

                # 格式4: cookies 是 dict {name: value} 格式
                if isinstance(cookies_data, dict) and len(cookies_data) > 0:
                    logger.info(f"[DashboardSync] ✅ 格式4: cookies dict, keys数={len(cookies_data)}, 样本keys={list(cookies_data.keys())[:5]}")
                    # 转换为 Playwright 格式
                    pw_cookies = []
                    cookie_domain = ".meituan.com" if account.platform == "meituan" else ".life-data.cn"
                    for name, value in cookies_data.items():
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
                    if pw_cookies:
                        result = {"cookies": pw_cookies}
                        logger.info(f"[DashboardSync] ✅ 格式4 转换成功, cookies数={len(pw_cookies)}")
                        return result

                # 格式5: credentials 本身就是 cookie dict
                if len(credentials) > 0 and all(isinstance(v, str) for v in credentials.values() if v is not None):
                    logger.info(f"[DashboardSync] ✅ 格式5: credentials 本身是 cookie dict, keys数={len(credentials)}")
                    cookie_domain = ".meituan.com" if account.platform == "meituan" else ".life-data.cn"
                    pw_cookies = []
                    for name, value in credentials.items():
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
                    if pw_cookies:
                        result = {"cookies": pw_cookies}
                        logger.info(f"[DashboardSync] ✅ 格式5 转换成功, cookies数={len(pw_cookies)}")
                        return result

                logger.warning(f"[DashboardSync] ⚠️ 无法识别 credentials 格式, keys={list(credentials.keys())[:10]}")
            else:
                logger.warning(f"[DashboardSync] ⚠️ credentials 不是 dict, type={type(credentials).__name__}")

            return None
        except Exception as e:
            logger.error(f"[DashboardSync] ❌ 获取 storage_state 失败: {e}", exc_info=True)
            return None

    async def _get_first_store_for_account(self, account_id: UUID) -> Optional[UUID]:
        """获取账号关联的第一个门店"""
        stmt = (
            select(StorePlatform.store_id)
            .where(StorePlatform.account_id == account_id)
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def _get_douyin_life_account_id(self, account_id: UUID) -> str:
        """获取抖音账号的 life_account_id"""
        # 先从 PlatformAccount.platform_account_id 取
        account = await self._get_account(account_id)
        if account and account.platform_account_id:
            return account.platform_account_id

        # 从绑定的店铺中取 account_id
        stmt = (
            select(StorePlatform)
            .where(StorePlatform.account_id == account_id)
            .limit(1)
        )
        result = await self.db.execute(stmt)
        sp = result.scalars().first()
        if sp and hasattr(sp, 'account_id') and sp.account_id:
            return str(sp.account_id)

        return ""

    async def _find_revenue_record(
        self, store_id: UUID, record_date: date
    ) -> Optional[RevenueRecord]:
        """查找指定门店+日期的营业额记录（可能存在重复行，取第一条）"""
        stmt = (
            select(RevenueRecord)
            .where(
                RevenueRecord.store_id == store_id,
                RevenueRecord.record_date == record_date,
            )
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def _find_store_metric(
        self, store_id: UUID, metric_date: date, platform: str
    ) -> Optional[StoreMetric]:
        """查找指定门店+日期+平台的门店指标（可能存在重复行，取第一条）"""
        stmt = (
            select(StoreMetric)
            .where(
                StoreMetric.store_id == store_id,
                StoreMetric.metric_date == metric_date,
                StoreMetric.platform == platform,
            )
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def _find_package_record(
        self, store_id: UUID, product_name: str, period_start: date, period_end: date
    ) -> Optional[PackageRecord]:
        """查找指定门店+商品名+周期的套餐记录（可能存在重复行，取第一条）"""
        stmt = (
            select(PackageRecord)
            .where(
                PackageRecord.store_id == store_id,
                PackageRecord.product_name == product_name,
                PackageRecord.period_start == period_start,
                PackageRecord.period_end == period_end,
            )
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    def _find_in_layout(self, data: dict, key: str) -> list:
        """递归搜索 layout 结构中指定 key 的数据"""
        results = []

        if not isinstance(data, dict):
            return results

        # 直接匹配
        if key in data:
            val = data[key]
            if isinstance(val, dict) and val.get("code") is not None:
                results.append(val)
            elif isinstance(val, list):
                for item in val:
                    if isinstance(item, dict):
                        results.append(item)

        # 递归搜索 children 和 data
        for sub_key in ["children", "data", "layout"]:
            sub = data.get(sub_key)
            if isinstance(sub, list):
                for item in sub:
                    results.extend(self._find_in_layout(item, key))
            elif isinstance(sub, dict):
                results.extend(self._find_in_layout(sub, key))

        return results

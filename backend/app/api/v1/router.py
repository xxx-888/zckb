"""
API v1 总路由模块
聚合所有子路由，统一注册到 FastAPI 应用
"""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.stores import router as stores_router
from app.api.v1.subscription import router as subscription_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.reviews import router as reviews_router

# 创建 v1 总路由
api_router = APIRouter()

# ---- 已实现的子路由 ----
api_router.include_router(auth_router)
api_router.include_router(stores_router)
api_router.include_router(subscription_router)
api_router.include_router(dashboard_router)
api_router.include_router(reviews_router)

# settings - 系统设置
from app.api.v1.settings import router as settings_router

api_router.include_router(settings_router)

# notifications - 通知管理
from app.api.v1.notifications import router as notifications_router

api_router.include_router(notifications_router)

# ---- AI模块子路由 ----
# ai_analysis - AI 分析
from app.api.v1.ai_analysis import router as ai_analysis_router

api_router.include_router(ai_analysis_router)

# negative_reply - 差评回复
from app.api.v1.negative_reply import router as negative_reply_router

api_router.include_router(negative_reply_router)

# positive_activation - 好评激活
from app.api.v1.positive_activation import router as positive_activation_router

api_router.include_router(positive_activation_router)

# insights - 洞察分析
from app.api.v1.insights import router as insights_router

api_router.include_router(insights_router)

# ---- 后台管理子路由 ----
# admin/ai_config - AI配置管理
from app.api.v1.admin.ai_config import router as admin_ai_config_router

api_router.include_router(admin_ai_config_router)

# audit - 审计日志
from app.api.v1.audit import router as audit_router

api_router.include_router(audit_router)

# spider - 爬虫管理
from app.api.v1.spider import router as spider_router

api_router.include_router(spider_router)

# admin - 后台管理
from app.api.v1.admin.admin import router as admin_router

api_router.include_router(admin_router)

# competitors - 竞品分析
from app.api.v1.competitors import router as competitors_router

api_router.include_router(competitors_router)

# reports - 报表管理
from app.api.v1.reports import router as reports_router

api_router.include_router(reports_router)

# platforms - 平台关联
from app.api.v1.platforms import router as platforms_router

api_router.include_router(platforms_router)

# annual_report - 年度报告
from app.api.v1.annual_report import router as annual_report_router

api_router.include_router(annual_report_router)

# admin/subscription - 订阅管理
from app.api.v1.admin.subscription import router as admin_subscription_router

api_router.include_router(admin_subscription_router)

# admin/regions - 区域管理
from app.api.v1.admin.region import router as admin_region_router

api_router.include_router(admin_region_router)

# collection_pack - 采集套餐（用户端）
from app.api.v1.collection_pack import router as collection_pack_router

api_router.include_router(collection_pack_router)

# admin/collection_pack - 采集套餐管理（后台）
from app.api.v1.admin.collection_pack import router as admin_collection_pack_router

api_router.include_router(admin_collection_pack_router)

# store_dashboard - 经营看板
from app.api.v1.store_dashboard import router as store_dashboard_router

api_router.include_router(store_dashboard_router)

# admin/store_dashboard - 后台经营数据管理
from app.api.v1.admin.store_dashboard import router as admin_store_dashboard_router

api_router.include_router(admin_store_dashboard_router)

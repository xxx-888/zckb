# CPA评价管理系统 - API接口清单

> 本文档列出所有后端API接口，供前端开发人员对接参考。
> 
> **Base URL**: `http://localhost:8000/api/v1`
> **API文档**: `http://localhost:8000/docs` (Swagger UI)

---

## 目录

1. [认证模块](#1-认证模块)
2. [用户模块](#2-用户模块)
3. [门店模块](#3-门店模块)
4. [评论模块](#4-评论模块)
5. [Dashboard模块](#5-dashboard模块)
6. [AI分析模块](#6-ai分析模块)
7. [差评处理模块](#7-差评处理模块)
8. [好评激活模块](#8-好评激活模块)
9. [经营洞察模块](#9-经营洞察模块)
10. [设置模块](#10-设置模块)
11. [通知模块](#11-通知模块)
12. [订阅模块](#12-订阅模块)
13. [平台关联模块](#13-平台关联模块)
14. [报告模块](#14-报告模块)
15. [竞对分析模块](#15-竞对分析模块)
16. [审核模块](#16-审核模块)
17. [爬虫模块](#17-爬虫模块)
18. [后台管理模块](#18-后台管理模块)

---

## 统一响应格式

### 成功响应
```json
{
  "code": 200,
  "message": "success",
  "data": { ... }
}
```

### 分页响应
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [ ... ],
    "total": 100,
    "page": 1,
    "pageSize": 20
  }
}
```

### 错误响应
```json
{
  "code": 400,
  "message": "错误描述",
  "data": null
}
```

---

## 1. 认证模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/auth/login` | 用户登录 | 否 |
| POST | `/auth/register` | 用户注册 | 否 |
| POST | `/auth/logout` | 退出登录 | 是 |
| GET | `/auth/current` | 获取当前用户信息 | 是 |
| POST | `/auth/forgot-password/send-code` | 发送验证码 | 否 |
| POST | `/auth/forgot-password/reset` | 重置密码 | 否 |
| POST | `/auth/refresh` | 刷新Token | 是 |

### 登录请求
```json
POST /auth/login
{
  "phone": "13800138000",
  "password": "password123"
}
```

### 登录响应
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "user": {
      "id": "uuid",
      "phone": "13800138000",
      "email": "user@example.com",
      "username": "用户名",
      "role": "HQ",
      "avatar": "https://...",
      "status": "active"
    }
  }
}
```

---

## 2. 用户模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/users/me` | 获取用户信息 | 是 |
| PUT | `/users/me` | 更新用户信息 | 是 |

---

## 3. 门店模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/stores` | 门店列表 | 是 |
| GET | `/stores/stats` | 门店汇总统计 | 是 |
| GET | `/stores/{store_id}` | 门店详情 | 是 |
| POST | `/stores` | 新增门店 | 是 |
| PUT | `/stores/{store_id}` | 更新门店 | 是 |
| DELETE | `/stores/{store_id}` | 删除门店 | 是 |
| POST | `/stores/{store_id}/activate` | 激活门店 | 是 |
| GET | `/stores/{store_id}/review-stats` | 门店评价统计 | 是 |
| GET | `/stores/{store_id}/monthly-stats` | 门店月度统计 | 是 |
| GET | `/stores/{store_id}/recent-reviews` | 门店最近评论 | 是 |

### 门店列表查询参数
```
GET /stores?page=1&page_size=20&type=restaurant&status=active&keyword=关键词
```

---

## 4. 评论模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/reviews` | 评价列表 | 是 |
| GET | `/reviews/stats` | 评价统计 | 是 |
| GET | `/reviews/{review_id}` | 评价详情 | 是 |
| GET | `/reviews/{review_id}/similar` | 相似评论 | 是 |
| POST | `/reviews` | 新增评价 | 是 |
| PUT | `/reviews/{review_id}` | 更新评价 | 是 |
| DELETE | `/reviews/{review_id}` | 删除评价 | 是 |
| POST | `/reviews/batch-delete` | 批量删除 | 是 |
| POST | `/reviews/{review_id}/like` | 赞同评论 | 是 |
| POST | `/reviews/{review_id}/reply` | 快速回复 | 是 |
| POST | `/reviews/{review_id}/approve-reply` | 审核通过并发送回复 | 是 |

### 评论列表查询参数
```
GET /reviews?page=1&page_size=20&sentiment=negative&keyword=关键词&store_id=uuid&platform=meituan&rating_min=1&rating_max=3&has_reply=false&has_image=true&start_date=2024-01-01&end_date=2024-12-31
```

---

## 5. Dashboard模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/dashboard/core-stats?period=7d` | 核心统计 | 是 |
| GET | `/dashboard/platform-distribution` | 平台分布 | 是 |
| GET | `/dashboard/recent-reviews?limit=10` | 最新评论 | 是 |
| GET | `/dashboard/store-rankings?limit=10` | 门店排行 | 是 |
| GET | `/dashboard/health-status` | 数据源健康 | 是 |
| GET | `/dashboard/alert` | 异常警告 | 是 |
| GET | `/dashboard/store-health` | 门店健康值 | 是 |

### 统计周期参数
- `period`: `7d` (7天), `30d` (30天), `90d` (90天), `all` (全部)

---

## 6. AI分析模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/ai-analysis/topics` | 语义分析主题 | 是 |
| GET | `/ai-analysis/tag-clustering` | 差评标签聚类 | 是 |
| GET | `/ai-analysis/sentiment-summary` | 情感指数 | 是 |
| GET | `/ai-analysis/risk-levels` | 风险分级 | 是 |
| GET | `/ai-analysis/reply-history` | 自动回复历史 | 是 |
| GET | `/ai-analysis/reply-stats` | 回复统计 | 是 |
| GET | `/ai-analysis/appeal-suggestions/{review_id}` | 申诉建议 | 是 |

---

## 7. 差评处理模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/negative-reply/tasks?status=pending` | 差评任务列表 | 是 |
| POST | `/negative-reply/tasks/{task_id}/approve` | 批准并发送 | 是 |
| POST | `/negative-reply/tasks/{task_id}/reject` | 驳回 | 是 |
| POST | `/negative-reply/tasks/{task_id}/regenerate` | 重新生成AI回复 | 是 |
| GET | `/negative-reply/history` | 已处理历史 | 是 |

---

## 8. 好评激活模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/positive-activation/high-quality-reviews` | 优质好评列表 | 是 |
| GET | `/positive-activation/brand-scripts` | 品牌话术库 | 是 |
| POST | `/positive-activation/copy-script/{script_id}` | 记录话术复制 | 是 |
| POST | `/positive-activation/send-authorization/{review_id}` | 发送授权请求 | 是 |
| POST | `/positive-activation/generate-content` | 生成种草内容 | 是 |

---

## 9. 经营洞察模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/insights/top-dishes?period=30d` | 菜品口碑排行 | 是 |
| GET | `/insights/three-good-three-bad?period=30d` | 三好三差报告 | 是 |
| GET | `/insights/dish-elimination` | 末位淘汰建议 | 是 |
| GET | `/insights/service-cases?type=golden` | 服务案例库 | 是 |
| GET | `/insights/competitor-opportunities` | 同行机会洞察 | 是 |

---

## 10. 设置模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/settings/reply-templates` | 回复模板列表 | 是 |
| POST | `/settings/reply-templates` | 创建回复模板 | 是 |
| PUT | `/settings/reply-templates/{template_id}` | 更新回复模板 | 是 |
| DELETE | `/settings/reply-templates/{template_id}` | 删除回复模板 | 是 |
| GET | `/settings/auto-reply` | 获取自动回复配置 | 是 |
| PUT | `/settings/auto-reply` | 更新自动回复配置 | 是 |
| GET | `/settings/notification` | 获取通知设置 | 是 |
| PUT | `/settings/notification` | 更新通知设置 | 是 |

### 自动回复配置请求
```json
PUT /settings/auto-reply
{
  "mode": "smart",
  "auto_reply_enabled": true,
  "work_hours_only": true,
  "work_start_time": "09:00",
  "work_end_time": "18:00",
  "keyword_reply_enabled": true,
  "keywords": {
    "退款": "感谢您的反馈，我们会尽快处理退款事宜...",
    "投诉": "非常抱歉给您带来不好的体验..."
  },
  "ai_suggest_enabled": true
}
```

---

## 11. 通知模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/notifications/channels` | 渠道列表 | 是 |
| POST | `/notifications/channels` | 新增渠道 | 是 |
| PUT | `/notifications/channels/{channel_id}` | 更新渠道 | 是 |
| DELETE | `/notifications/channels/{channel_id}` | 删除渠道 | 是 |
| POST | `/notifications/channels/{channel_id}/test` | 测试渠道 | 是 |
| GET | `/notifications/rules` | 规则列表 | 是 |
| POST | `/notifications/rules` | 新增规则 | 是 |
| PUT | `/notifications/rules/{rule_id}` | 更新规则 | 是 |
| DELETE | `/notifications/rules/{rule_id}` | 删除规则 | 是 |
| GET | `/notifications/history` | 推送历史 | 是 |
| GET | `/notifications/templates` | 模板列表 | 是 |
| POST | `/notifications/templates` | 新增模板 | 是 |
| PUT | `/notifications/templates/{template_id}` | 更新模板 | 是 |

---

## 12. 订阅模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/subscription/plans` | 获取所有订阅计划 | 是 |
| GET | `/subscription/current` | 获取当前用户订阅 | 是 |
| POST | `/subscription/upgrade` | 升级订阅 | 是 |
| POST | `/subscription/cancel` | 取消订阅 | 是 |

---

## 13. 平台关联模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/platforms/connect` | 连接平台账号 | 是 |
| GET | `/platforms/{platform}/stores` | 获取平台店铺列表 | 是 |
| POST | `/platforms/bind` | 绑定平台店铺 | 是 |
| DELETE | `/platforms/{store_platform_id}` | 解绑平台店铺 | 是 |
| POST | `/platforms/sync` | 同步平台数据 | 是 |
| GET | `/platforms/sync-status/{store_platform_id}` | 获取同步状态 | 是 |
| POST | `/platforms/{store_platform_id}/reply` | 在平台上回复评论 | 是 |
| GET | `/platforms/accounts` | 获取已连接的平台账号列表 | 是 |

### 连接平台请求
```json
POST /platforms/connect
{
  "platform": "meituan",
  "username": "手机号",
  "password": "密码",
  "verify_code": "验证码"
}
```

---

## 14. 报告模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/reports/annual?store_id={store_id}&year=2024` | 年度报告 | 是 |
| GET | `/reports/annual/all-years?store_id={store_id}` | 所有年份数据 | 是 |
| POST | `/reports/annual/generate` | 生成年度报告 | 是 |
| GET | `/reports/weekly?store_id={store_id}&week_start=2024-01-01` | 周报 | 是 |
| POST | `/reports/weekly/generate` | 生成周报 | 是 |

---

## 15. 竞对分析模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/competitors?store_id={store_id}` | 竞品列表 | 是 |
| POST | `/competitors` | 添加竞品 | 是 |
| DELETE | `/competitors/{competitor_id}` | 删除竞品 | 是 |
| GET | `/competitors/{competitor_id}` | 竞品详情 | 是 |
| POST | `/competitors/generate-report` | 生成分析报告 | 是 |
| GET | `/competitors/plans` | 套餐列表 | 是 |
| POST | `/competitors/tasks` | 创建分析任务 | 是 |
| GET | `/competitors/tasks` | 任务列表 | 是 |
| POST | `/competitors/tasks/{task_id}/pay` | 支付任务 | 是 |
| POST | `/competitors/tasks/{task_id}/generate` | 生成任务报告 | 是 |
| POST | `/competitors/{competitor_id}/sync` | 同步竞品数据 | 是 |

---

## 16. 审核模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/audit/list?status=pending&keyword=关键词&page=1&limit=20` | 待审核列表 | 是 |
| GET | `/audit/{audit_id}` | 审核详情 | 是 |
| POST | `/audit/{audit_id}/approve` | 审核通过 | 是 |
| POST | `/audit/{audit_id}/reject` | 审核拒绝 | 是 |
| POST | `/audit/{audit_id}/regenerate` | 重新生成回复 | 是 |
| GET | `/audit/stats` | 审核统计 | 是 |

---

## 17. 爬虫模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/spider/platforms` | 平台列表 | 是 |
| POST | `/spider/platforms` | 新增平台 | 是 |
| PUT | `/spider/platforms/{platform_id}` | 更新平台 | 是 |
| DELETE | `/spider/platforms/{platform_id}` | 删除平台 | 是 |
| POST | `/spider/platforms/{platform_id}/sync` | 同步单个平台 | 是 |
| POST | `/spider/sync-all` | 同步所有平台 | 是 |
| GET | `/spider/logs?platform_id={platform_id}` | 同步日志 | 是 |
| POST | `/spider/platforms/{platform_id}/test` | 测试连接 | 是 |
| GET | `/spider/tasks` | 任务列表 | 是 |
| POST | `/spider/tasks` | 创建任务 | 是 |
| POST | `/spider/tasks/{task_id}/cancel` | 取消任务 | 是 |

---

## 18. 后台管理模块

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/admin/dashboard/stats?period=7d` | 系统统计数据 | 是 |
| GET | `/admin/system/health` | 系统健康状态 | 是 |
| POST | `/admin/system/export-report` | 导出系统报告 | 是 |
| GET | `/admin/permissions/admins` | 管理员列表 | 是 |
| POST | `/admin/permissions/admins` | 新增管理员 | 是 |
| PUT | `/admin/permissions/admins/{user_id}` | 更新管理员 | 是 |
| POST | `/admin/permissions/admins/{user_id}/disable` | 禁用管理员 | 是 |
| GET | `/admin/permissions/roles` | 角色列表 | 是 |
| POST | `/admin/permissions/roles` | 新增角色 | 是 |
| PUT | `/admin/permissions/roles/{role_id}` | 更新角色 | 是 |
| GET | `/admin/permissions/structure` | 组织架构 | 是 |

---

## AI配置模块（后台管理）

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/ai/config` | 获取AI配置 | 是 |
| GET | `/ai/models` | 获取模型配置列表 | 是 |
| POST | `/ai/models` | 新增模型配置 | 是 |
| PUT | `/ai/models/{config_id}` | 更新模型配置 | 是 |
| DELETE | `/ai/models/{config_id}` | 删除模型配置 | 是 |
| POST | `/ai/models/{config_id}/test` | 测试模型连接 | 是 |
| GET | `/ai/prompts` | 获取提示词配置 | 是 |
| PUT | `/ai/prompts/{config_id}` | 更新提示词配置 | 是 |
| GET | `/ai/rules` | 获取规则引擎 | 是 |
| PUT | `/ai/rules/{engine_id}` | 更新规则引擎 | 是 |
| GET | `/ai/monitoring` | 实时监控数据 | 是 |
| GET | `/ai/evaluation` | 效能评估 | 是 |

---

## 认证方式

所有需要认证的接口都需要在请求头中携带JWT Token：

```
Authorization: Bearer {access_token}
```

---

## 枚举值定义

### 用户角色 (role)
- `HQ` - 总部
- `OPERATOR` - 运营商
- `STORE` - 店长

### 门店类型 (store_type)
- `restaurant` - 餐饮
- `hotel` - 酒店
- `beverage` - 饮品

### 平台类型 (platform)
- `meituan` - 美团
- `dianping` - 大众点评
- `douyin` - 抖音
- `taobao` - 淘宝闪购
- `jd` - 京东秒送

### 评论情感 (sentiment)
- `positive` - 正面
- `negative` - 负面
- `neutral` - 中性

### 风险等级 (risk_level)
- `high` - 高
- `medium` - 中
- `low` - 低

### 回复模式 (reply_mode)
- `smart` - 智能模式
- `semi_auto` - 半自动模式
- `manual` - 手动模式

### 订阅状态 (subscription_status)
- `trial` - 试用
- `active` - 活跃
- `expired` - 过期
- `cancelled` - 已取消

---

## 前端对接注意事项

1. **Base URL配置**: 在 `.env` 文件中设置 `VITE_API_BASE_URL=http://localhost:8000`

2. **请求拦截器**: 自动从 localStorage 获取 token 并添加到请求头

3. **错误处理**: 统一处理 401 未授权错误，自动跳转到登录页

4. **分页处理**: 列表接口都支持 `page` 和 `page_size` 参数，返回数据包含 `total` 总数

5. **角色权限**: 根据用户角色控制页面访问权限和数据可见性
   - HQ: 查看所有数据
   - OPERATOR: 查看关联门店数据
   - STORE: 仅查看自己门店数据

# API 接口文档

评论管理平台后端 API 接口文档。

## 目录

- [统一响应格式](#统一响应格式)
- [错误码说明](#错误码说明)
- [认证模块](#认证模块)
- [用户模块](#用户模块)
- [门店模块](#门店模块)
- [评论模块](#评论模块)
- [Dashboard 模块](#dashboard-模块)
- [AI 分析模块](#ai-分析模块)
- [设置模块](#设置模块)
- [通知模块](#通知模块)
- [订阅模块](#订阅模块)
- [爬虫模块](#爬虫模块)
- [后台管理模块](#后台管理模块)

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
    "page_size": 20,
    "pages": 5
  }
}
```

### 错误响应

```json
{
  "code": 400,
  "message": "请求参数错误",
  "detail": "phone 字段不能为空"
}
```

---

## 错误码说明

| 错误码 | 说明 | HTTP 状态码 |
|--------|------|-------------|
| 200 | 成功 | 200 |
| 400 | 请求参数错误 | 400 |
| 401 | 未认证 | 401 |
| 403 | 无权限 | 403 |
| 404 | 资源不存在 | 404 |
| 409 | 资源冲突 | 409 |
| 422 | 验证错误 | 422 |
| 429 | 请求过于频繁 | 429 |
| 500 | 服务器内部错误 | 500 |
| 502 | 外部服务错误 | 502 |
| 503 | 服务不可用 | 503 |

---

## 认证模块

### 基础路径

`/api/v1/auth`

### 接口列表

#### 1. 用户注册

- **URL**: `POST /auth/register`
- **描述**: 新用户注册
- **请求体**:

```json
{
  "phone": "13800138000",
  "password": "password123",
  "username": "张三",
  "role": "STORE"
}
```

- **响应**:

```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "id": "uuid",
    "phone": "13800138000",
    "username": "张三",
    "role": "STORE",
    "created_at": "2025-01-01T00:00:00Z"
  }
}
```

#### 2. 用户登录

- **URL**: `POST /auth/login`
- **描述**: 用户登录，支持手机号或邮箱
- **请求体**:

```json
{
  "phone": "13800138000",
  "password": "password123"
}
```

- **响应**:

```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "expires_in": 3600,
    "user": {
      "id": "uuid",
      "phone": "13800138000",
      "username": "张三",
      "role": "STORE",
      "avatar": "https://..."
    }
  }
}
```

#### 3. 刷新 Token

- **URL**: `POST /auth/refresh`
- **描述**: 使用 refresh_token 获取新的 access_token
- **请求体**:

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

- **响应**: 同登录响应

#### 4. 登出

- **URL**: `POST /auth/logout`
- **描述**: 用户登出，使当前 token 失效
- **请求头**: `Authorization: Bearer {token}`
- **响应**:

```json
{
  "code": 200,
  "message": "登出成功"
}
```

#### 5. 获取当前用户信息

- **URL**: `GET /auth/me`
- **描述**: 获取当前登录用户信息
- **请求头**: `Authorization: Bearer {token}`
- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": "uuid",
    "phone": "13800138000",
    "email": "user@example.com",
    "username": "张三",
    "role": "STORE",
    "avatar": "https://...",
    "status": "active",
    "last_login_at": "2025-01-01T00:00:00Z",
    "created_at": "2025-01-01T00:00:00Z"
  }
}
```

#### 6. 修改密码

- **URL**: `PUT /auth/password`
- **描述**: 修改当前用户密码
- **请求头**: `Authorization: Bearer {token}`
- **请求体**:

```json
{
  "old_password": "oldpassword123",
  "new_password": "newpassword123"
}
```

---

## 用户模块

### 基础路径

`/api/v1/users`

### 接口列表

#### 1. 获取用户列表

- **URL**: `GET /users`
- **描述**: 获取用户列表（管理员权限）
- **权限**: HQ, OPERATOR
- **查询参数**:
  - `page`: 页码，默认 1
  - `page_size`: 每页数量，默认 20
  - `role`: 按角色筛选
  - `status`: 按状态筛选
  - `keyword`: 搜索关键词（用户名/手机号）

- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "uuid",
        "phone": "13800138000",
        "username": "张三",
        "role": "STORE",
        "status": "active",
        "created_at": "2025-01-01T00:00:00Z"
      }
    ],
    "total": 100,
    "page": 1,
    "page_size": 20,
    "pages": 5
  }
}
```

#### 2. 获取用户详情

- **URL**: `GET /users/{user_id}`
- **描述**: 获取指定用户详情
- **权限**: 本人或管理员

#### 3. 创建用户

- **URL**: `POST /users`
- **描述**: 创建新用户（管理员权限）
- **权限**: HQ, OPERATOR
- **请求体**:

```json
{
  "phone": "13800138000",
  "password": "password123",
  "username": "张三",
  "role": "STORE",
  "store_ids": ["store-uuid-1", "store-uuid-2"]
}
```

#### 4. 更新用户

- **URL**: `PUT /users/{user_id}`
- **描述**: 更新用户信息
- **权限**: 本人或管理员
- **请求体**:

```json
{
  "username": "张三",
  "email": "user@example.com",
  "avatar": "https://...",
  "status": "active"
}
```

#### 5. 删除用户

- **URL**: `DELETE /users/{user_id}`
- **描述**: 删除用户（软删除）
- **权限**: HQ

#### 6. 分配门店

- **URL**: `POST /users/{user_id}/stores`
- **描述**: 为用户分配门店
- **权限**: HQ, OPERATOR
- **请求体**:

```json
{
  "store_ids": ["store-uuid-1", "store-uuid-2"],
  "role_in_store": "manager"
}
```

---

## 门店模块

### 基础路径

`/api/v1/stores`

### 接口列表

#### 1. 获取门店列表

- **URL**: `GET /stores`
- **描述**: 获取当前用户有权限的门店列表
- **查询参数**:
  - `page`: 页码
  - `page_size`: 每页数量
  - `type`: 门店类型筛选
  - `status`: 状态筛选
  - `region_id`: 区域筛选
  - `keyword`: 搜索关键词

- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "uuid",
        "name": "某某餐厅",
        "type": "restaurant",
        "address": "北京市朝阳区...",
        "status": "active",
        "health_score": 4.5,
        "platform_count": 3,
        "review_count": 128,
        "region": {
          "id": "uuid",
          "name": "朝阳区",
          "level": "district"
        },
        "platforms": [
          {
            "platform": "meituan",
            "platform_store_name": "某某餐厅（美团）",
            "connected": true
          }
        ]
      }
    ],
    "total": 50,
    "page": 1,
    "page_size": 20,
    "pages": 3
  }
}
```

#### 2. 获取门店详情

- **URL**: `GET /stores/{store_id}`
- **描述**: 获取门店详细信息

#### 3. 创建门店

- **URL**: `POST /stores`
- **描述**: 创建新门店
- **权限**: HQ, OPERATOR
- **请求体**:

```json
{
  "name": "某某餐厅",
  "type": "restaurant",
  "address": "北京市朝阳区...",
  "owner_name": "李四",
  "phone": "13800138000",
  "region_id": "region-uuid"
}
```

#### 4. 更新门店

- **URL**: `PUT /stores/{store_id}`
- **描述**: 更新门店信息
- **请求体**: 同创建门店

#### 5. 删除门店

- **URL**: `DELETE /stores/{store_id}`
- **描述**: 删除门店
- **权限**: HQ

#### 6. 绑定平台账号

- **URL**: `POST /stores/{store_id}/platforms`
- **描述**: 绑定第三方平台账号
- **请求体**:

```json
{
  "platform": "meituan",
  "platform_store_id": "123456",
  "platform_store_name": "某某餐厅（美团）",
  "config": {
    "cookies": "...",
    "token": "..."
  }
}
```

#### 7. 解绑平台账号

- **URL**: `DELETE /stores/{store_id}/platforms/{platform_id}`
- **描述**: 解绑第三方平台账号

#### 8. 同步平台数据

- **URL**: `POST /stores/{store_id}/sync`
- **描述**: 手动触发平台数据同步
- **请求体**:

```json
{
  "platform": "meituan",
  "sync_type": "incremental"
}
```

---

## 评论模块

### 基础路径

`/api/v1/reviews`

### 接口列表

#### 1. 获取评论列表

- **URL**: `GET /reviews`
- **描述**: 获取评论列表
- **查询参数**:
  - `page`: 页码
  - `page_size`: 每页数量
  - `store_id`: 门店筛选
  - `platform`: 平台筛选
  - `rating`: 评分筛选
  - `sentiment`: 情感筛选 (positive/negative/neutral)
  - `status`: 状态筛选
  - `start_date`: 开始日期
  - `end_date`: 结束日期
  - `keyword`: 关键词搜索
  - `has_reply`: 是否已回复

- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "uuid",
        "store_id": "store-uuid",
        "platform": "meituan",
        "platform_review_id": "review-123",
        "user_name": "用户昵称",
        "user_avatar": "https://...",
        "rating": 5,
        "content": "味道很好，服务也不错！",
        "images": ["https://..."],
        "sentiment": "positive",
        "tags": ["味道好", "服务好"],
        "reply": "感谢您的评价！",
        "reply_time": "2025-01-01T00:00:00Z",
        "ai_generated": true,
        "risk_level": "low",
        "status": "normal",
        "platform_created_at": "2025-01-01T00:00:00Z",
        "created_at": "2025-01-01T00:00:00Z"
      }
    ],
    "total": 1000,
    "page": 1,
    "page_size": 20,
    "pages": 50
  }
}
```

#### 2. 获取评论详情

- **URL**: `GET /reviews/{review_id}`
- **描述**: 获取评论详细信息

#### 3. 回复评论

- **URL**: `POST /reviews/{review_id}/reply`
- **描述**: 回复评论
- **请求体**:

```json
{
  "content": "感谢您的评价！",
  "ai_generated": false
}
```

#### 4. 生成 AI 回复

- **URL**: `POST /reviews/{review_id}/ai-reply`
- **描述**: 使用 AI 生成回复建议
- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "reply": "感谢您的五星好评！...",
    "confidence": 0.95,
    "processing_time_ms": 1200
  }
}
```

#### 5. 批量回复

- **URL**: `POST /reviews/batch-reply`
- **描述**: 批量回复评论
- **请求体**:

```json
{
  "review_ids": ["uuid-1", "uuid-2"],
  "content": "统一回复内容",
  "ai_generated": false
}
```

#### 6. 申诉评论

- **URL**: `POST /reviews/{review_id}/appeal`
- **描述**: 对评论发起申诉
- **请求体**:

```json
{
  "reason": "恶意差评",
  "evidence": "相关证据描述"
}
```

#### 7. 获取评论统计

- **URL**: `GET /reviews/statistics`
- **描述**: 获取评论统计数据
- **查询参数**:
  - `store_id`: 门店ID
  - `start_date`: 开始日期
  - `end_date`: 结束日期

- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total_reviews": 1000,
    "average_rating": 4.5,
    "reply_rate": 0.85,
    "sentiment_distribution": {
      "positive": 700,
      "neutral": 200,
      "negative": 100
    },
    "rating_distribution": {
      "5": 600,
      "4": 200,
      "3": 150,
      "2": 30,
      "1": 20
    },
    "platform_distribution": {
      "meituan": 400,
      "dianping": 300,
      "douyin": 200,
      "taobao": 100
    }
  }
}
```

---

## Dashboard 模块

### 基础路径

`/api/v1/dashboard`

### 接口列表

#### 1. 获取概览数据

- **URL**: `GET /dashboard/overview`
- **描述**: 获取仪表盘概览数据
- **查询参数**:
  - `store_id`: 门店ID（可选，不传则返回所有有权限门店的汇总）

- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total_reviews": 1280,
    "new_reviews_today": 45,
    "average_rating": 4.6,
    "reply_rate": 0.88,
    "pending_reviews": 12,
    "negative_reviews_today": 3,
    "store_count": 5,
    "platform_count": 4
  }
}
```

#### 2. 获取趋势数据

- **URL**: `GET /dashboard/trends`
- **描述**: 获取评论趋势数据
- **查询参数**:
  - `store_id`: 门店ID
  - `period`: 周期 (7d/30d/90d/1y)
  - `metric`: 指标 (reviews/rating/sentiment)

- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "period": "30d",
    "labels": ["2025-01-01", "2025-01-02", ...],
    "datasets": [
      {
        "label": "评论数",
        "data": [10, 15, 12, ...]
      },
      {
        "label": "平均评分",
        "data": [4.5, 4.6, 4.4, ...]
      }
    ]
  }
}
```

#### 3. 获取热门关键词

- **URL**: `GET /dashboard/keywords`
- **描述**: 获取评论中的热门关键词
- **查询参数**:
  - `store_id`: 门店ID
  - `period`: 周期
  - `sentiment`: 情感类型 (positive/negative)
  - `limit`: 返回数量

- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "positive": [
      {"keyword": "味道好", "count": 150, "sentiment": "positive"},
      {"keyword": "服务好", "count": 120, "sentiment": "positive"}
    ],
    "negative": [
      {"keyword": "上菜慢", "count": 30, "sentiment": "negative"},
      {"keyword": "环境吵", "count": 20, "sentiment": "negative"}
    ]
  }
}
```

#### 4. 获取门店对比

- **URL**: `GET /dashboard/store-comparison`
- **描述**: 获取多门店对比数据
- **查询参数**:
  - `store_ids`: 门店ID列表
  - `period`: 周期

- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "stores": [
      {
        "id": "uuid",
        "name": "门店A",
        "total_reviews": 500,
        "average_rating": 4.7,
        "reply_rate": 0.90
      },
      {
        "id": "uuid",
        "name": "门店B",
        "total_reviews": 400,
        "average_rating": 4.5,
        "reply_rate": 0.85
      }
    ]
  }
}
```

---

## AI 分析模块

### 基础路径

`/api/v1/ai`

### 接口列表

#### 1. 生成回复

- **URL**: `POST /ai/generate-reply`
- **描述**: 为评论生成 AI 回复
- **请求体**:

```json
{
  "review_id": "review-uuid",
  "template_id": "template-uuid",
  "custom_prompt": "额外提示（可选）"
}
```

- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "reply": "生成的回复内容...",
    "confidence": 0.92,
    "model_used": "gpt-4",
    "processing_time_ms": 1500,
    "tokens_used": 256
  }
}
```

#### 2. 情感分析

- **URL**: `POST /ai/sentiment-analysis`
- **描述**: 对评论进行情感分析
- **请求体**:

```json
{
  "content": "评论内容"
}
```

- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "sentiment": "positive",
    "confidence": 0.95,
    "scores": {
      "positive": 0.85,
      "neutral": 0.10,
      "negative": 0.05
    }
  }
}
```

#### 3. 提取关键词

- **URL**: `POST /ai/extract-keywords`
- **描述**: 从评论中提取关键词
- **请求体**:

```json
{
  "content": "评论内容",
  "limit": 10
}
```

- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "keywords": [
      {"word": "味道", "weight": 0.9},
      {"word": "服务", "weight": 0.8}
    ]
  }
}
```

#### 4. 生成周报摘要

- **URL**: `POST /ai/weekly-summary`
- **描述**: 生成周报 AI 摘要
- **请求体**:

```json
{
  "store_id": "store-uuid",
  "week_start": "2025-01-01",
  "week_end": "2025-01-07"
}
```

- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "summary": "本周共收到评论 120 条...",
    "highlights": ["好评亮点1", "好评亮点2"],
    "suggestions": ["改进建议1", "改进建议2"]
  }
}
```

#### 5. 获取 AI 模型配置

- **URL**: `GET /ai/models`
- **描述**: 获取 AI 模型配置列表
- **权限**: HQ

#### 6. 更新 AI 模型配置

- **URL**: `PUT /ai/models/{model_id}`
- **描述**: 更新 AI 模型配置
- **权限**: HQ
- **请求体**:

```json
{
  "api_key": "new-api-key",
  "is_active": true,
  "priority": 1,
  "temperature": 0.7
}
```

#### 7. 获取提示词模板

- **URL**: `GET /ai/prompt-templates`
- **描述**: 获取提示词模板列表
- **权限**: HQ, OPERATOR

#### 8. 更新提示词模板

- **URL**: `PUT /ai/prompt-templates/{template_id}`
- **描述**: 更新提示词模板
- **权限**: HQ, OPERATOR

---

## 设置模块

### 基础路径

`/api/v1/settings`

### 接口列表

#### 1. 获取自动回复配置

- **URL**: `GET /settings/auto-reply`
- **描述**: 获取门店自动回复配置
- **查询参数**:
  - `store_id`: 门店ID

- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "store_id": "store-uuid",
    "mode": "semi_auto",
    "auto_reply_enabled": true,
    "work_hours_only": true,
    "work_start_time": "09:00",
    "work_end_time": "22:00",
    "keyword_reply_enabled": true,
    "keywords": {
      "好评": "感谢您的五星好评！",
      "差评": "非常抱歉给您带来不好的体验..."
    },
    "ai_suggest_enabled": true
  }
}
```

#### 2. 更新自动回复配置

- **URL**: `PUT /settings/auto-reply`
- **描述**: 更新自动回复配置
- **请求体**: 同获取配置

#### 3. 获取回复模板列表

- **URL**: `GET /settings/reply-templates`
- **描述**: 获取回复模板列表
- **查询参数**:
  - `store_id`: 门店ID
  - `type`: 模板类型

#### 4. 创建回复模板

- **URL**: `POST /settings/reply-templates`
- **描述**: 创建回复模板
- **请求体**:

```json
{
  "name": "好评模板",
  "type": "good",
  "content": "感谢您的五星好评！",
  "store_id": "store-uuid",
  "variables": ["user_name"]
}
```

#### 5. 更新回复模板

- **URL**: `PUT /settings/reply-templates/{template_id}`
- **描述**: 更新回复模板

#### 6. 删除回复模板

- **URL**: `DELETE /settings/reply-templates/{template_id}`
- **描述**: 删除回复模板

#### 7. 获取用户通知设置

- **URL**: `GET /settings/notifications`
- **描述**: 获取当前用户通知设置

- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "new_review_enabled": true,
    "negative_alert_enabled": true,
    "weekly_report_enabled": true,
    "email_enabled": false,
    "sms_enabled": false,
    "push_enabled": true,
    "quiet_hours_start": "22:00",
    "quiet_hours_end": "08:00"
  }
}
```

#### 8. 更新用户通知设置

- **URL**: `PUT /settings/notifications`
- **描述**: 更新用户通知设置
- **请求体**: 同获取设置

---

## 通知模块

### 基础路径

`/api/v1/notifications`

### 接口列表

#### 1. 获取通知渠道列表

- **URL**: `GET /notifications/channels`
- **描述**: 获取通知渠道列表
- **权限**: HQ

#### 2. 创建通知渠道

- **URL**: `POST /notifications/channels`
- **描述**: 创建通知渠道
- **权限**: HQ
- **请求体**:

```json
{
  "name": "企业微信",
  "type": "wechat",
  "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
  "config": {
    "mention_all": false
  }
}
```

#### 3. 获取通知规则列表

- **URL**: `GET /notifications/rules`
- **描述**: 获取通知规则列表

#### 4. 创建通知规则

- **URL**: `POST /notifications/rules`
- **描述**: 创建通知规则
- **请求体**:

```json
{
  "name": "差评预警",
  "channel_id": "channel-uuid",
  "event_type": "negative_alert",
  "condition": {
    "rating_threshold": 3,
    "sentiment": "negative"
  },
  "frequency": "realtime"
}
```

#### 5. 获取通知历史

- **URL**: `GET /notifications/history`
- **描述**: 获取通知发送历史
- **查询参数**:
  - `page`: 页码
  - `page_size`: 每页数量
  - `status`: 状态筛选
  - `start_date`: 开始日期
  - `end_date`: 结束日期

#### 6. 测试通知渠道

- **URL**: `POST /notifications/channels/{channel_id}/test`
- **描述**: 测试通知渠道是否正常

---

## 订阅模块

### 基础路径

`/api/v1/subscriptions`

### 接口列表

#### 1. 获取订阅套餐列表

- **URL**: `GET /subscriptions/plans`
- **描述**: 获取所有订阅套餐

- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": "uuid",
      "name": "标准版",
      "price_monthly": 99.0,
      "price_yearly": 999.0,
      "max_stores": 3,
      "features": {
        "ai_reply": true,
        "basic_analytics": true,
        "features": ["AI智能回复", "基础数据分析"]
      }
    },
    {
      "id": "uuid",
      "name": "旗舰版",
      "price_monthly": 299.0,
      "price_yearly": 2999.0,
      "max_stores": 10,
      "features": {
        "ai_reply": true,
        "advanced_analytics": true,
        "competitor_analysis": true,
        "features": ["AI智能回复", "高级数据分析", "竞品分析"]
      }
    }
  ]
}
```

#### 2. 获取当前订阅

- **URL**: `GET /subscriptions/current`
- **描述**: 获取当前用户订阅信息

- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": "uuid",
    "plan": {
      "id": "uuid",
      "name": "旗舰版"
    },
    "status": "active",
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "auto_renew": true,
    "days_remaining": 300
  }
}
```

#### 3. 创建订阅

- **URL**: `POST /subscriptions`
- **描述**: 创建新订阅
- **请求体**:

```json
{
  "plan_id": "plan-uuid",
  "period": "yearly",
  "auto_renew": true
}
```

#### 4. 取消订阅

- **URL**: `POST /subscriptions/{subscription_id}/cancel`
- **描述**: 取消自动续费

#### 5. 获取账单历史

- **URL**: `GET /subscriptions/bills`
- **描述**: 获取账单历史

---

## 爬虫模块

### 基础路径

`/api/v1/spider`

### 接口列表

#### 1. 获取平台列表

- **URL**: `GET /spider/platforms`
- **描述**: 获取爬虫平台列表

- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": "uuid",
      "name": "meituan",
      "display_name": "美团",
      "status": "active",
      "reliability": 0.95,
      "last_sync_at": "2025-01-01T00:00:00Z"
    }
  ]
}
```

#### 2. 获取同步日志

- **URL**: `GET /spider/sync-logs`
- **描述**: 获取同步日志
- **查询参数**:
  - `platform_id`: 平台ID
  - `store_id`: 门店ID
  - `status`: 状态筛选
  - `page`: 页码

#### 3. 创建同步任务

- **URL**: `POST /spider/tasks`
- **描述**: 创建爬虫同步任务
- **请求体**:

```json
{
  "platform_id": "platform-uuid",
  "store_id": "store-uuid",
  "task_type": "full_sync",
  "priority": 1
}
```

#### 4. 获取任务列表

- **URL**: `GET /spider/tasks`
- **描述**: 获取爬虫任务列表

#### 5. 获取任务详情

- **URL**: `GET /spider/tasks/{task_id}`
- **描述**: 获取任务详情

#### 6. 取消任务

- **URL**: `POST /spider/tasks/{task_id}/cancel`
- **描述**: 取消正在执行的任务

---

## 后台管理模块

### 基础路径

`/api/v1/admin`

### 接口列表

#### 1. 获取系统统计

- **URL**: `GET /admin/statistics`
- **描述**: 获取系统统计数据
- **权限**: HQ

- **响应**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total_users": 100,
    "total_stores": 50,
    "total_reviews": 10000,
    "active_subscriptions": 80,
    "today_new_reviews": 120,
    "system_health": {
      "database": "healthy",
      "redis": "healthy",
      "spider": "healthy"
    }
  }
}
```

#### 2. 获取用户管理列表

- **URL**: `GET /admin/users`
- **描述**: 获取用户管理列表
- **权限**: HQ

#### 3. 禁用用户

- **URL**: `POST /admin/users/{user_id}/disable`
- **描述**: 禁用用户账号
- **权限**: HQ

#### 4. 启用用户

- **URL**: `POST /admin/users/{user_id}/enable`
- **描述**: 启用用户账号
- **权限**: HQ

#### 5. 获取系统日志

- **URL**: `GET /admin/logs`
- **描述**: 获取系统操作日志
- **权限**: HQ

#### 6. 获取 AI 处理日志

- **URL**: `GET /admin/ai-logs`
- **描述**: 获取 AI 处理日志
- **权限**: HQ

#### 7. 系统配置管理

- **URL**: `GET /admin/config`
- **描述**: 获取系统配置
- **权限**: HQ

- **URL**: `PUT /admin/config`
- **描述**: 更新系统配置
- **权限**: HQ

---

## 附录

### 枚举值定义

#### 用户角色 (UserRole)

- `HQ`: 总部管理员
- `OPERATOR`: 运营人员
- `STORE`: 门店用户

#### 门店类型 (StoreType)

- `restaurant`: 餐饮
- `hotel`: 酒店
- `beverage`: 饮品

#### 门店状态 (StoreStatus)

- `active`: 活跃
- `pending`: 待审核
- `inactive`: 停用

#### 评论情感 (ReviewSentiment)

- `positive`: 正面
- `negative`: 负面
- `neutral`: 中性

#### 评论状态 (ReviewStatus)

- `normal`: 正常
- `appealed`: 申诉中
- `deleted`: 已删除

#### 平台名称 (Platform)

- `meituan`: 美团
- `dianping`: 大众点评
- `douyin`: 抖音
- `taobao`: 淘宝
- `jd`: 京东

#### 订阅状态 (SubscriptionStatus)

- `trial`: 试用
- `active`: 活跃
- `expired`: 已过期
- `cancelled`: 已取消

### 分页参数说明

所有列表接口都支持以下分页参数：

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `page` | integer | 页码 | 1 |
| `page_size` | integer | 每页数量 | 20 |
| `sort_by` | string | 排序字段 | created_at |
| `sort_order` | string | 排序方向 (asc/desc) | desc |

### 日期格式

所有日期时间字段使用 ISO 8601 格式：

- 日期: `YYYY-MM-DD` (例: 2025-01-01)
- 日期时间: `YYYY-MM-DDTHH:mm:ssZ` (例: 2025-01-01T12:00:00Z)

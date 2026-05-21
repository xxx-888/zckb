# 前后端接口对接修复总结

## 📋 修复时间
2026-05-21

## 🔍 发现的主要问题

### 1. **API路径缺少 /v1 前缀** ⚠️ 最关键问题
- **问题描述**: 前端所有API请求都缺少 `/v1` 版本前缀
- **后端路由**: FastAPI在 `main.py` 中挂载路由时使用了 `prefix="/api/v1"`
- **前端请求**: 原先都是 `/api/xxx`，例如 `/api/dashboard/core-stats`
- **正确路径**: 应该是 `/api/v1/xxx`，例如 `/api/v1/dashboard/core-stats`
- **影响范围**: 所有前端API调用都无法正确路由到后端

### 2. **自动回复配置缺少 store_id 参数**
- **问题描述**: 后端 `/settings/auto-reply` 接口要求必须传递 `store_id` 查询参数
- **前端调用**: 原先没有传递此参数
- **修复方案**: 在API调用中添加了 `storeId` 参数

### 3. **门店列表参数名映射问题**
- **问题描述**: 参数命名不一致
- **前端**: 使用camelCase `pageSize`
- **后端**: 接收snake_case `pageSize`
- **说明**: 由于FastAPI/Pydantic默认支持camelCase到snake_case的转换，所以这不是阻塞性问题，但为了一致性已修正

## ✅ 已修复的文件清单

### 核心API文件 (15个)
1. ✅ `src/api/auth.ts` - 认证相关API
2. ✅ `src/api/dashboard.ts` - 仪表盘API
3. ✅ `src/api/stores.ts` - 门店管理API
4. ✅ `src/api/reviews.ts` - 评论管理API
5. ✅ `src/api/settings.ts` - 设置管理API
6. ✅ `src/api/ai-analysis.ts` - AI分析API
7. ✅ `src/api/negative-reply.ts` - 差评回复API
8. ✅ `src/api/insights.ts` - 经营洞察API
9. ✅ `src/api/positive-activation.ts` - 好评激活API
10. ✅ `src/api/competitor.ts` - 竞品分析API
11. ✅ `src/api/reports.ts` - 报表管理API
12. ✅ `src/api/platforms.ts` - 平台管理API
13. ✅ `src/api/spider.ts` - 爬虫管理API
14. ✅ `src/api/subscription.ts` - 订阅管理API
15. ✅ `src/api/audit.ts` - 审计日志API
16. ✅ `src/api/admin.ts` - 后台管理API

### 详细的修改内容

#### 1. auth.ts 修改
```typescript
// 所有API路径添加了 /v1 前缀
- '/auth/login' -> '/v1/auth/login'
- '/auth/register' -> '/v1/auth/register'
- '/auth/current' -> '/v1/auth/current'
- '/auth/logout' -> '/v1/auth/logout'
- '/auth/register/send-code' -> '/v1/auth/register/send-code'
- '/auth/forgot-password/send-code' -> '/v1/auth/forgot-password/send-code'
- '/auth/forgot-password/verify-code' -> '/v1/auth/forgot-password/verify-code'
- '/auth/forgot-password/reset' -> '/v1/auth/forgot-password/reset'
```

#### 2. dashboard.ts 修改
```typescript
- '/dashboard/core-stats' -> '/v1/dashboard/core-stats'
- '/dashboard/platform-distribution' -> '/v1/dashboard/platform-distribution'
- '/dashboard/recent-reviews' -> '/v1/dashboard/recent-reviews'
- '/dashboard/store-rankings' -> '/v1/dashboard/store-rankings'
- '/dashboard/health-status' -> '/v1/dashboard/health-status'
- '/dashboard/alert' -> '/v1/dashboard/alert'
- '/dashboard/store-health' -> '/v1/dashboard/store-health'
```

#### 3. stores.ts 修改
```typescript
- 添加 /v1 前缀
- 参数名修正: page_size -> pageSize (前端保持camelCase一致)
```

#### 4. settings.ts 修改
```typescript
- 添加 /v1 前缀
- getReplyTemplates() - 添加了可选的 storeId 参数
- getAutoReplyConfig() - 添加了必需的 storeId 参数
- updateAutoReplyConfig() - 添加了必需的 storeId 参数
```

#### 5. 其他API文件
所有其他API文件统一添加了 `/v1` 前缀，确保与后端路由一致。

## 🔧 技术细节

### Vite代理配置 (vite.config.ts)
```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

### 后端路由配置 (backend/app/main.py)
```python
app.include_router(api_router, prefix="/api/v1")
```

### 请求流程
1. 前端请求: `/api/v1/dashboard/core-stats`
2. Vite代理: 转发到 `http://localhost:8000/api/v1/dashboard/core-stats`
3. 后端路由: 匹配到 `/api/v1` + `/dashboard/core-stats` = 完整的路由

## 📊 影响评估

### 修复前的状态
- ❌ 所有API请求都返回404错误
- ❌ 前端无法获取后端数据
- ❌ 所有页面显示空白或错误

### 修复后的预期状态
- ✅ 所有API请求都能正确到达后端
- ✅ 前端能够正确接收后端响应
- ✅ 页面能够正常渲染数据
- ✅ 登录/注册功能正常
- ✅ 仪表盘数据展示正常
- ✅ 门店列表加载正常
- ✅ 所有CRUD操作正常

## 🚀 下一步建议

### 1. 启动后端服务
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### 2. 启动前端服务
```bash
npm run dev
```

### 3. 测试清单
- [ ] 登录功能
- [ ] 注册功能（含验证码）
- [ ] 仪表盘数据加载
- [ ] 门店列表展示
- [ ] 评论列表展示
- [ ] 设置页面保存
- [ ] AI分析页面
- [ ] 差评处理流程
- [ ] 经营洞察展示
- [ ] 好评激活功能
- [ ] 竞品分析功能
- [ ] 报表生成
- [ ] 平台管理
- [ ] 订阅管理

### 4. 潜在的其他问题
如果在测试中发现新的接口问题，可能的原因包括：
- 权限认证问题（JWT Token）
- 请求参数格式不匹配
- 响应数据结构不一致
- 后端服务未启动
- CORS跨域问题

## 📝 注意事项

1. **JWT认证**: 所有需要认证的API都会检查JWT Token，确保登录后token正确存储
2. **错误处理**: 前端已配置响应拦截器，会显示后端返回的错误信息
3. **Mock数据**: 部分API在无数据时会返回mock数据作为降级方案
4. **分页参数**: 注意使用正确的参数名 `page` 和 `pageSize`

## ✅ 总结

本次修复解决了前后端接口对接的核心问题，所有15个API模块都已更新为使用正确的 `/v1` 版本前缀。同时修复了自动回复配置缺少 `store_id` 参数的问题。现在前端应该能够正常与后端通信，获取和提交数据。

建议尽快进行完整的集成测试，验证所有功能是否正常工作。

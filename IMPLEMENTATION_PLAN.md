# 功能实施计划

## 📋 需求概述

### 1. 首页多渠道详情页链接优化
**目标**：Dashboard 页面各渠道卡片点击后直接进入详情分析页

**实施步骤**：
1. 修改 `AdminDashboard.tsx`，为渠道卡片添加链接
2. 创建 `ChannelDetail.tsx` 页面（多渠道详情）
3. 添加路由配置
4. 实现数据传递（渠道类型、筛选条件）

**工作量**：1-2 天
**优先级**：高（快速见效）

---

### 2. 评价数据知识库 + 年度报告
**目标**：存储历史评价数据，生成个性化年度报告（数字资产）

**后端实施**：
1. 数据库迁移（增强 `reviews` 表，创建 `knowledge_base` 和 `annual_reports` 表）
2. 创建 API 端点：
   - `POST /api/v1/reviews/extract-topics`（提取话题和关键词）
   - `GET /api/v1/stores/:id/annual-report?year=:year`（获取年度报告）
   - `POST /api/v1/stores/:id/annual-report/generate`（生成年度报告）
3. 实现 AI 分析服务（`AnnualReportGenerator`）
4. 数据存储优化（添加 `topics`, `keywords`, `sentiment_score` 字段）

**前端实施**：
1. 创建 `AnnualReport.tsx` 页面
2. 实现年度报告展示（总览、趋势图、AI 洞察、话题云）
3. 添加知识库管理页面
4. 实现数据导出功能

**工作量**：1-2 周
**优先级**：中（核心功能）

---

### 3. 竞对分析付费功能 + 小红书数据采集
**目标**：竞对分析需要先付费，然后系统自动采集和分析

**后端实施**：
1. 数据库迁移（创建 `orders` 和 `competitor_tasks` 表）
2. 实现支付系统：
   - `POST /api/v1/payments/create-order`（创建订单）
   - `POST /api/v1/payments/callback`（支付回调）
3. 实现爬虫服务：
   - 美团/大众点评爬虫（已有，优化）
   - 小红书爬虫（新增，使用 Selenium）
4. 实现 "三好三差" 分析报告生成
5. 任务队列管理（Celery 或 RQ）

**前端实施**：
1. 创建 `CompetitorPayment.tsx`（付费页面）
2. 创建 `CompetitorTaskStatus.tsx`（任务状态查询）
3. 创建 `CompetitorReport.tsx`（报告展示）
4. 实现支付流程（支付宝/微信支付集成）

**工作量**：2-3 周
**优先级**：低（复杂功能，可后续迭代）

---

## 🗓️ 实施时间表

### Week 1（本周）
- [ ] 完成功能 1：首页多渠道详情页链接
- [ ] 设计功能 2 的数据库结构
- [ ] 创建数据库迁移文件

### Week 2
- [ ] 实现功能 2 的后端 API
- [ ] 实现 AI 年度报告生成服务
- [ ] 创建前端年度报告页面

### Week 3
- [ ] 实现功能 3 的支付系统
- [ ] 实现小红书爬虫
- [ ] 实现 "三好三差" 报告生成

### Week 4
- [ ] 前端付费页面和支付流程
- [ ] 任务队列和状态管理
- [ ] 测试和优化

---

## 🛠️ 技术栈

### 后端
- **FastAPI**：API 框架
- **SQLAlchemy**：ORM
- **Alembic**：数据库迁移
- **Celery + Redis**：任务队列
- **Selenium**：网页爬虫
- **OpenAI API / 本地 LLM**：AI 分析

### 前端
- **React + TypeScript**：前端框架
- **Vite**：构建工具
- **Tailwind CSS**：样式
- **Recharts / Echarts**：数据可视化
- **React Router**：路由管理

---

## 📂 文件结构

```
zc/
├── backend/
│   ├── alembic/versions/
│   │   └── add_knowledge_base_and_payment.py  # 数据库迁移
│   ├── models/
│   │   ├── review.py
│   │   ├── knowledge_base.py
│   │   ├── annual_report.py
│   │   ├── order.py
│   │   └── competitor_task.py
│   ├── services/
│   │   ├── annual_report_generator.py  # AI 报告生成
│   │   ├── payment_service.py        # 支付系统
│   │   └── report_generator.py       # 三好三差报告
│   ├── crawlers/
│   │   ├── meituan_crawler.py
│   │   ├── dianping_crawler.py
│   │   └── xiaohongshu_crawler.py
│   └── api/
│       ├── reviews.py
│       ├── annual_reports.py
│       ├── payments.py
│       └── competitor_analysis.py
│
├── frontend/src/
│   ├── pages/admin/
│   │   ├── AnnualReport.tsx         # 年度报告页面
│   │   ├── KnowledgeBase.tsx        # 知识库管理
│   │   ├── CompetitorPayment.tsx   # 竞对付费页面
│   │   ├── CompetitorTaskStatus.tsx # 任务状态
│   │   └── CompetitorReport.tsx    # 报告展示
│   └── components/annual-report/
│       ├── StatsOverview.tsx
│       ├── SentimentTrendChart.tsx
│       ├── AIInsights.tsx
│       └── TopicCloud.tsx
│
└── nginx-ip-only.conf  # Nginx 配置（已完成）
```

---

## ✅ 验收标准

### 功能 1：首页多渠道详情页链接
- [ ] 点击 Dashboard 渠道卡片能跳转到详情页
- [ ] 详情页展示该渠道的评价数据
- [ ] 支持时间范围筛选
- [ ] 响应式设计（移动端适配）

### 功能 2：评价数据知识库 + 年度报告
- [ ] 所有历史评价数据存储到知识库
- [ ] 能生成指定年份的年度报告
- [ ] 报告包含：总览、趋势图、AI 洞察、话题云
- [ ] 支持报告导出（PDF/Excel）

### 功能 3：竞对分析付费 + 小红书采集
- [ ] 用户可以选择竞对和平台，创建付费订单
- [ ] 支付成功后，系统自动开始采集
- [ ] 采集完成后生成 "三好三差" 分析报告
- [ ] 用户可以在前端查看任务状态和报告

---

## 🚨 风险和注意事项

1. **小红书爬虫可能被反爬虫机制阻止**
   - 解决方案：使用代理 IP、随机 User-Agent、验证码识别服务

2. **AI 分析成本**
   - 解决方案：使用本地 LLM（如 ChatGLM、Qwen）降低成本

3. **支付安全**
   - 解决方案：使用支付宝/微信官方 SDK，验证签名

4. **数据量过大**
   - 解决方案：分页查询、数据归档、缓存策略

---

## 📝 下一步行动

**立即开始**：
1. 实现功能 1（首页链接优化）
2. 创建数据库迁移文件
3. 实现后端 API（功能 2）

**需要确认**：
- 你希望我先做哪个功能？
- 支付系统集成哪个平台（支付宝/微信/Stripe）？
- AI 分析使用哪个模型（GPT-4/Claude/本地 LLM）？

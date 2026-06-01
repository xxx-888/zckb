# 智策口碑管理系统 (ZCKB)

餐饮商家全渠道评价管理与 AI 智能运营平台。支持美团、大众点评、抖音、淘宝、京东等多平台评价自动采集，结合 AI 进行情感分析、智能回复、经营洞察与竞品对比。

## 系统架构

```
                    ┌──────────────┐
                    │   Nginx     │
                    │  (HTTPS)    │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │                         │
     ┌────────▼────────┐      ┌────────▼────────┐
     │   React 前端     │      │  FastAPI 后端    │
     │   (静态资源)     │      │  (API 服务)      │
     └─────────────────┘      └────────┬────────┘
                                       │
                          ┌────────────┼────────────┐
                          │            │            │
                 ┌────────▼───┐ ┌─────▼─────┐ ┌────▼──────┐
                 │ PostgreSQL │ │   Redis   │ │  AI 服务   │
                 │  (数据库)   │ │ (缓存/队列) │ │(OpenAI等) │
                 └────────────┘ └─────┬─────┘ └───────────┘
                                     │
                            ┌────────▼────────┐
                            │  Celery Worker  │
                            │  (爬虫引擎)     │
                            │  + Playwright   │
                            └─────────────────┘
```

## 技术栈

### 前端
- React 18 + TypeScript
- Vite 8 (构建工具)
- React Router 6 (路由)
- Tailwind CSS + Radix UI (样式 & 组件)
- Recharts (图表)
- Axios (HTTP 请求)
- Lucide React (图标)

### 后端
- Python 3.13 + FastAPI
- SQLAlchemy 2.0 (异步 ORM)
- PostgreSQL / SQLite
- Redis + Celery (任务队列)
- PyJWT (认证)
- Pydantic 2.7 (数据校验)

### 爬虫服务
- FastAPI + Celery Worker
- Playwright (浏览器自动化)
- 支持平台：美团、抖音、淘宝、京东

### AI 集成
- OpenAI / 智谱 AI (GLM) / DeepSeek

## 核心功能

### 评价采集
- 多平台自动采集评论（美团、大众点评、抖音、淘宝、京东）
- Playwright 浏览器自动化登录与数据抓取
- 评论批量导入/导出（Excel / CSV）
- 定时监控新评论

### AI 智能分析
- 情感分析与情感指数
- 语义主题提取
- 差评标签聚类
- 风险等级自动分级
- AI 智能回复生成（人工审核后一键发布）
- 种草内容生成（小红书 / 抖音 / 微博）

### 经营洞察
- 菜品口碑排行
- 三好三差分析报告
- 末位淘汰建议
- 服务案例库
- 同行机会洞察
- 竞品对比分析

### 报告系统
- AI 年度报告（含同比分析、历史趋势）
- AI 周报
- 月度门店统计

### 通知系统
- 多渠道推送：微信 / 钉钉 / 飞书 / 邮箱 / 短信
- 自定义通知规则与模板
- 推送历史记录

### 订阅与付费
- 多级订阅套餐（标准版 / 旗舰版 / 企业版）
- 采集积分按量付费
- 支付订单管理

### 权限管理
- 多角色体系：总部(HQ) / 运营(OPERATOR) / 门店(STORE) / 超管(SUPER_ADMIN)
- 区域管理与门店分配
- 用户-门店多对多关联

## 项目结构

```
zc/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── api/v1/          # API 路由（130+ 接口）
│   │   ├── core/            # 配置、数据库、认证、异常处理
│   │   ├── models/          # SQLAlchemy 数据模型（20+ 表）
│   │   ├── schemas/         # Pydantic 请求/响应模型
│   │   ├── services/        # 业务逻辑层（25+ 服务）
│   │   └── main.py          # 应用入口
│   ├── migrations/          # 数据库迁移
│   └── .env.example         # 环境变量模板
│
├── src/                     # React 前端
│   ├── api/                 # API 请求封装（19 个模块）
│   ├── components/          # 通用组件
│   │   └── ui/              # 基础 UI 组件
│   ├── context/             # React Context
│   ├── hooks/               # 自定义 Hooks
│   ├── pages/
│   │   ├── mobile/          # 移动端页面（26 个）
│   │   └── admin/           # 后台管理页面（22 个）
│   └── lib/                 # 工具函数
│
├── spider/                  # 爬虫服务
│   ├── app/
│   │   ├── spiders/         # 各平台爬虫实现
│   │   ├── tasks/           # Celery 任务
│   │   └── main.py          # 爬虫 API 入口
│   ├── worker.py            # Celery Worker 入口
│   └── pyproject.toml
│
├── public/                  # 静态资源
├── dist/                    # 构建产物
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
└── package.json
```

## API 模块

| 模块 | 路径前缀 | 说明 |
|------|---------|------|
| 认证 | `/api/v1/auth` | 登录、注册、验证码、密码重置、Token 刷新 |
| 门店 | `/api/v1/stores` | 门店 CRUD、统计、月度数据 |
| 评论 | `/api/v1/reviews` | 评论 CRUD、导入导出、筛选、快速回复 |
| 仪表盘 | `/api/v1/dashboard` | 核心统计、平台分布、门店排行 |
| AI 分析 | `/api/v1/ai-analysis` | 情感分析、主题提取、标签聚类 |
| 差评处理 | `/api/v1/negative-reply` | AI 回复任务审批流 |
| 好评激活 | `/api/v1/positive-activation` | 优质评论、品牌话术、种草生成 |
| 经营洞察 | `/api/v1/insights` | 菜品排行、三好三差、淘汰建议 |
| 竞品分析 | `/api/v1/competitors` | 竞品管理、分析任务、报告生成 |
| 报告 | `/api/v1/reports` | 年度报告、周报生成 |
| 平台关联 | `/api/v1/platforms` | 账号连接、店铺绑定、数据同步 |
| 爬虫 | `/api/v1/spider` | 平台管理、同步任务、日志 |
| 审核管理 | `/api/v1/audit` | AI 回复审核 |
| 设置 | `/api/v1/settings` | 回复模板、自动回复、通知设置 |
| 通知 | `/api/v1/notifications` | 渠道/规则/模板/推送历史 |
| 订阅 | `/api/v1/subscription` | 套餐、支付、积分 |
| AI 配置 | `/api/v1/ai` | 模型管理、提示词、规则引擎、监控 |
| 后台管理 | `/api/v1/admin` | 系统统计、权限、区域、采集套餐 |

## 快速开始

### 环境要求
- Node.js >= 18
- Python >= 3.10
- PostgreSQL 15+
- Redis

### 后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install fastapi uvicorn[standard] sqlalchemy[asyncio] asyncpg redis celery pydantic pydantic-settings python-jose passlib[bcrypt] python-multipart PyJWT openpyxl aiohttp httpx python-dotenv alibabacloud-dysmsapi20170525

# 配置环境变量
cp .env.example .env
# 编辑 .env 填写数据库、Redis、JWT 密钥等配置

# 启动
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 前端

```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 生产构建
npm run build
# 构建产物在 dist/ 目录
```

### 爬虫服务

```bash
cd spider

# 安装依赖
pip install -e .

# 安装浏览器引擎
playwright install chromium

# 启动 API 服务（端口 8001）
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001

# 启动 Celery Worker
celery -A worker worker --loglevel=info
```

### 生产部署（Nginx 反向代理）

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # 前端静态文件
    root /opt/zcweb;
    index index.html;

    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, max-age=31536000, immutable";
        access_log off;
    }

    # API 反向代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # SPA 路由 fallback
    location / {
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }
}
```

## 前端页面

### 移动端（26 个页面）

| 页面 | 路由 | 功能 |
|------|------|------|
| 登录 | `/mobile/login` | 手机号 + 密码登录 |
| 注册 | `/mobile/register` | 验证码注册 |
| 首页 | `/mobile` | 数据概览仪表盘 |
| 门店列表 | `/mobile/store-list` | 门店管理 |
| AI 分析 | `/mobile/ai-analysis` | 情感/主题/标签/风险 |
| 经营洞察 | `/mobile/insights` | 菜品排行/三好三差 |
| 评论流 | `/mobile/review-stream` | 实时评论列表 |
| 差评处理 | `/mobile/negative-reply` | AI 回复审批 |
| 好评激活 | `/mobile/positive-activation` | 话术/种草生成 |
| 平台连接 | `/mobile/platform-connection` | 平台账号绑定 |
| 年度报告 | `/mobile/annual-report` | AI 年度报告 |
| 竞品分析 | `/mobile/competitor-analysis` | 竞品对比 |
| 订阅管理 | `/mobile/subscription` | 套餐/支付 |
| 设置中心 | `/mobile/settings` | 回复模板/通知/自动回复 |

### 后台管理（22 个页面）

| 页面 | 路由 | 功能 |
|------|------|------|
| 仪表盘 | `/admin/dashboard` | 系统数据概览 |
| 门店管理 | `/admin/store-management` | 门店 CRUD |
| 评论管理 | `/admin/review-management` | 评论审核/操作 |
| 爬虫管理 | `/admin/spider-management` | 采集任务监控 |
| AI 配置 | `/admin/ai-config/*` | 模型/提示词/规则/监控/评估 |
| 回复审核 | `/admin/reply-audit` | AI 回复质量审核 |
| 竞品分析 | `/admin/competitor-analysis` | 竞品管理 |
| 通知配置 | `/admin/notification-config` | 渠道/规则/模板 |
| 权限管理 | `/admin/permission-management` | 角色/管理员 |
| 订阅管理 | `/admin/subscription-management` | 套餐/支付记录 |
| 区域管理 | `/admin/region-management` | 区域树形结构 |
| 采集套餐 | `/admin/collection-pack-management` | 积分套餐/订单 |

## 数据库模型

| 模型 | 说明 |
|------|------|
| User | 用户（手机号/邮箱/角色/状态） |
| Store | 门店（名称/类型/地址/健康分） |
| PlatformAccount | 平台账号（登录凭证/Cookies） |
| StorePlatform | 门店-平台关联 |
| Review | 评论（平台/评分/情感/标签/风险） |
| ReplyAudit | AI 回复审核记录 |
| AIModelConfig | AI 模型配置 |
| AIPromptTemplate | AI 提示词模板 |
| SubscriptionPlan | 订阅套餐 |
| UserSubscription | 用户订阅 |
| PaymentRecord | 支付记录 |
| CollectionPack | 采集积分套餐 |
| SpiderPlatform | 爬虫平台 |
| SpiderTask | 爬虫任务 |
| NotificationChannel | 通知渠道 |
| NotificationRule | 通知规则 |
| AnnualReport | 年度报告 |
| Competitor | 竞品 |
| Region | 区域 |

## 环境变量

### 后端 (.env)
```env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/zckb
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=your-secret-key
CORS_ORIGINS=["https://your-domain.com"]
OPENAI_API_KEY=
ZHIPU_API_KEY=
DEEPSEEK_API_KEY=
ALIYUN_ACCESS_KEY_ID=
ALIYUN_ACCESS_KEY_SECRET=
```

### 前端 (.env.production)
```env
VITE_API_BASE_URL=/api
```

## License

MIT

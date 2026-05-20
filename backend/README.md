# 评论管理平台后端

基于 FastAPI + SQLAlchemy 2.0 + PostgreSQL 的异步评论管理后端服务。

## 项目简介

评论管理平台是一个面向餐饮、酒店等连锁品牌的全渠道评论管理解决方案，主要功能包括：

- **多平台评论聚合**：支持美团、大众点评、抖音、淘宝、京东等平台
- **AI 智能回复**：基于大语言模型的自动回复生成
- **评论数据分析**：情感分析、关键词提取、趋势分析
- **竞品分析**：监控竞品动态，对比分析
- **自动周报/年报**：定期生成数据报告
- **实时通知**：差评预警、新评论提醒

## 技术栈

- **Web 框架**: FastAPI (异步)
- **ORM**: SQLAlchemy 2.0 (异步)
- **数据库**: PostgreSQL 14+
- **缓存**: Redis 6+
- **任务队列**: Celery + Redis
- **数据库迁移**: Alembic
- **认证**: JWT (python-jose)
- **密码哈希**: Passlib (bcrypt)
- **HTTP 客户端**: httpx
- **数据验证**: Pydantic V2

## 项目结构

```
backend/
├── alembic/                    # 数据库迁移
│   ├── versions/               # 迁移脚本
│   ├── env.py                  # 迁移环境配置
│   └── script.py.mako          # 迁移模板
├── app/                        # 应用代码
│   ├── api/                    # API 路由
│   │   ├── deps.py             # 依赖注入
│   │   └── v1/                 # API v1 版本
│   │       ├── auth.py         # 认证接口
│   │       ├── users.py        # 用户接口
│   │       ├── stores.py       # 门店接口
│   │       ├── reviews.py      # 评论接口
│   │       ├── dashboard.py    # 仪表盘接口
│   │       ├── ai.py           # AI 分析接口
│   │       ├── settings.py     # 设置接口
│   │       ├── notifications.py # 通知接口
│   │       ├── subscriptions.py # 订阅接口
│   │       ├── spider.py       # 爬虫接口
│   │       └── admin.py        # 后台管理接口
│   ├── core/                   # 核心配置
│   │   ├── config.py           # 应用配置
│   │   ├── security.py         # 安全工具
│   │   ├── database.py         # 数据库连接
│   │   └── exceptions.py       # 异常定义
│   ├── models/                 # 数据模型
│   │   ├── base.py             # 基类定义
│   │   ├── user.py             # 用户模型
│   │   ├── store.py            # 门店模型
│   │   ├── review.py           # 评论模型
│   │   ├── ai_config.py        # AI 配置模型
│   │   ├── notification.py     # 通知模型
│   │   ├── subscription.py     # 订阅模型
│   │   ├── spider.py           # 爬虫模型
│   │   ├── report.py           # 报告模型
│   │   └── settings.py         # 设置模型
│   ├── schemas/                # Pydantic 模式
│   ├── services/               # 业务逻辑
│   ├── utils/                  # 工具函数
│   └── main.py                 # 应用入口
├── scripts/                    # 脚本工具
│   └── init_data.py            # 初始化数据
├── tests/                      # 测试代码
├── alembic.ini                 # Alembic 配置
├── pyproject.toml              # Poetry 配置
└── README.md                   # 项目说明
```

## 安装部署

### 环境要求

- Python 3.11+
- PostgreSQL 14+
- Redis 6+

### 本地开发环境

1. **克隆仓库**

```bash
cd backend
```

2. **安装 Poetry**（如果尚未安装）

```bash
pip install poetry
```

3. **安装依赖**

```bash
poetry install
```

4. **配置环境变量**

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 应用配置
APP_NAME="评论管理平台"
APP_ENV=development
DEBUG=true
SECRET_KEY=your-secret-key-here

# 数据库配置
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/review_platform_db

# Redis 配置
REDIS_URL=redis://localhost:6379/0

# AI 配置（可选）
OPENAI_API_KEY=your-openai-key
ZHIPU_API_KEY=your-zhipu-key
DEEPSEEK_API_KEY=your-deepseek-key
```

5. **创建数据库**

```bash
# 使用 psql 创建数据库
psql -U postgres -c "CREATE DATABASE review_platform_db;"
```

6. **执行数据库迁移**

```bash
# 使用 Poetry
poetry run alembic upgrade head

# 或使用 Python
python -m alembic upgrade head
```

7. **初始化系统数据**

```bash
poetry run python -m scripts.init_data
```

8. **启动开发服务器**

```bash
# 使用 Poetry
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或使用 Python
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

服务启动后访问：
- API 文档: http://localhost:8000/docs
- ReDoc 文档: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health

## 数据库迁移

### 创建新迁移

```bash
# 自动生成迁移（基于模型变化）
poetry run alembic revision --autogenerate -m "描述信息"

# 手动创建迁移
poetry run alembic revision -m "描述信息"
```

### 执行迁移

```bash
# 升级到最新版本
poetry run alembic upgrade head

# 升级到指定版本
poetry run alembic upgrade <revision>

# 降级到指定版本
poetry run alembic downgrade <revision>

# 降级到上一个版本
poetry run alembic downgrade -1

# 查看当前版本
poetry run alembic current

# 查看历史版本
poetry run alembic history
```

### 离线模式（生成 SQL）

```bash
# 生成升级 SQL
poetry run alembic upgrade head --sql > upgrade.sql

# 生成降级 SQL
poetry run alembic downgrade -1 --sql > downgrade.sql
```

## API 文档

### 在线文档

启动服务后，可以通过以下地址访问 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### 接口模块

| 模块 | 路径前缀 | 说明 |
|------|----------|------|
| 认证 | `/api/v1/auth` | 登录、注册、刷新 Token |
| 用户 | `/api/v1/users` | 用户管理 |
| 门店 | `/api/v1/stores` | 门店 CRUD、平台绑定 |
| 评论 | `/api/v1/reviews` | 评论管理、回复 |
| 仪表盘 | `/api/v1/dashboard` | 数据统计、趋势分析 |
| AI 分析 | `/api/v1/ai` | AI 回复生成、分析 |
| 设置 | `/api/v1/settings` | 自动回复、模板配置 |
| 通知 | `/api/v1/notifications` | 通知规则、历史记录 |
| 订阅 | `/api/v1/subscriptions` | 套餐、订阅管理 |
| 爬虫 | `/api/v1/spider` | 同步任务、日志 |
| 后台管理 | `/api/v1/admin` | 系统管理 |

详细 API 文档请参考 [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)。

## 环境变量说明

### 核心配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `APP_NAME` | 应用名称 | 评论管理平台 |
| `APP_ENV` | 运行环境 | development |
| `DEBUG` | 调试模式 | true |
| `SECRET_KEY` | JWT 密钥 | - |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token 有效期 | 60 |

### 数据库配置

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `DATABASE_URL` | 数据库连接 URL | postgresql+asyncpg://user:pass@host:port/db |

### Redis 配置

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `REDIS_URL` | Redis 连接 URL | redis://localhost:6379/0 |

### AI 配置

| 变量名 | 说明 |
|--------|------|
| `OPENAI_API_KEY` | OpenAI API Key |
| `ZHIPU_API_KEY` | 智谱 AI API Key |
| `DEEPSEEK_API_KEY` | DeepSeek API Key |

### 邮件配置

| 变量名 | 说明 |
|--------|------|
| `SMTP_HOST` | SMTP 服务器地址 |
| `SMTP_PORT` | SMTP 端口 |
| `SMTP_USER` | SMTP 用户名 |
| `SMTP_PASSWORD` | SMTP 密码 |

### 对象存储配置

| 变量名 | 说明 |
|--------|------|
| `OSS_ACCESS_KEY` | OSS Access Key |
| `OSS_SECRET_KEY` | OSS Secret Key |
| `OSS_BUCKET` | OSS Bucket 名称 |
| `OSS_ENDPOINT` | OSS 端点 |

## 测试

```bash
# 运行所有测试
poetry run pytest

# 运行指定测试文件
poetry run pytest tests/test_auth.py

# 运行并生成覆盖率报告
poetry run pytest --cov=app --cov-report=html

# 持续测试模式
poetry run pytest -f
```

## 代码质量

```bash
# 代码格式化
poetry run black app tests
poetry run isort app tests

# 代码检查
poetry run flake8 app tests
poetry run mypy app

# 运行所有检查
poetry run pre-commit run --all-files
```

## 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

[MIT](LICENSE)

## 联系方式

如有问题或建议，请提交 Issue 或联系开发团队。

# Review Spider Service

分布式爬虫服务，支持多平台评论数据采集、监控和回复。

## 功能特性

- **分布式架构**：基于 Celery + Redis 支持多节点部署
- **多平台支持**：美团开店宝、抖音来客、淘宝闪购、京东秒送
- **评论采集**：支持分页获取、日期过滤、增量同步
- **评论监控**：定时监控新评论，支持 webhook 通知
- **评价回复**：自动/手动回复评论
- **数据入库**：通过 API 对接主后端系统

## 技术栈

- **Web 框架**: FastAPI + Uvicorn
- **任务队列**: Celery + Redis
- **爬虫引擎**: Playwright (支持 Chromium/Firefox/WebKit)
- **数据验证**: Pydantic v2
- **HTTP 客户端**: httpx
- **数据库**: SQLAlchemy + asyncpg (可选)

## 项目结构

```
spider/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── router.py          # FastAPI 路由
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # 配置管理
│   │   └── logger.py          # 日志配置
│   ├── spiders/
│   │   ├── __init__.py
│   │   ├── base.py            # 爬虫基类
│   │   ├── meituan.py         # 美团开店宝
│   │   ├── douyin.py          # 抖音来客
│   │   ├── taobao.py          # 淘宝闪购
│   │   ├── jd.py              # 京东秒送
│   │   └── factory.py         # 爬虫工厂
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── celery_app.py      # Celery 应用
│   │   ├── spider_tasks.py    # 爬虫任务
│   │   └── api_client.py      # 主后端 API 客户端
│   └── main.py                # FastAPI 入口
├── pyproject.toml             # 项目依赖
├── .env                       # 环境变量
├── .env.example               # 环境变量模板
├── .gitignore
├── run.py                     # API 服务启动脚本
└── worker.py                  # Celery Worker 启动脚本
```

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -e ".[dev]"

# 安装 Playwright 浏览器
playwright install chromium
```

### 2. 配置环境变量

复制 `.env.example` 到 `.env` 并修改配置：

```bash
cp .env.example .env
```

主要配置项：

```env
# Redis 配置
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# 主后端 API 配置
API_BASE_URL=http://localhost:8000/api/v1
API_KEY=your-api-key

# Playwright 配置
PLAYWRIGHT_HEADLESS=false  # 开发环境设为 false 方便调试
PLAYWRIGHT_SLOW_MO=100

# 任务配置
MAX_CONCURRENT_TASKS=5
TASK_TIMEOUT=300
```

### 3. 启动服务

#### 启动 Redis

```bash
# Docker
docker run -d -p 6379:6379 redis:latest

# 或本地安装
redis-server
```

#### 启动 API 服务

```bash
python run.py
# 或
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

#### 启动 Celery Worker

```bash
# 单节点
python worker.py

# 或使用 celery 命令
celery -A app.tasks.celery_app worker -l info -Q spider,monitor

# 多节点部署（不同服务器）
celery -A app.tasks.celery_app worker -l info -Q spider -n spider-worker@%h
celery -A app.tasks.celery_app worker -l info -Q monitor -n monitor-worker@%h
```

#### 启动 Celery Beat（定时任务）

```bash
celery -A app.tasks.celery_app beat -l info
```

## API 接口

### 基础信息

- 基础 URL: `http://localhost:8001/api/v1`
- 文档: `http://localhost:8001/docs`

### 接口列表

#### 1. 同步评论

```http
POST /api/v1/tasks/sync-reviews
Content-Type: application/json

{
  "platform": "meituan",
  "store_id": "123456",
  "credentials": {
    "username": "your_username",
    "password": "your_password"
  },
  "page": 1,
  "limit": 20,
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```

响应：

```json
{
  "task_id": "abc-123-def",
  "status": "queued",
  "message": "Review sync task has been queued"
}
```

#### 2. 同步店铺信息

```http
POST /api/v1/tasks/sync-store
Content-Type: application/json

{
  "platform": "meituan",
  "store_id": "123456",
  "credentials": {
    "username": "your_username",
    "password": "your_password"
  }
}
```

#### 3. 回复评论

```http
POST /api/v1/tasks/reply-review
Content-Type: application/json

{
  "platform": "meituan",
  "review_id": "review_123",
  "content": "感谢您的评价，我们会继续努力！",
  "credentials": {
    "username": "your_username",
    "password": "your_password"
  },
  "store_id": "123456"
}
```

#### 4. 监控评论

```http
POST /api/v1/tasks/monitor-reviews
Content-Type: application/json

{
  "platform": "meituan",
  "store_ids": ["123456", "789012"],
  "credentials": {
    "username": "your_username",
    "password": "your_password"
  },
  "last_check_time": "2024-01-15T10:00:00"
}
```

#### 5. 查询任务状态

```http
GET /api/v1/tasks/{task_id}/status
```

响应：

```json
{
  "task_id": "abc-123-def",
  "status": "SUCCESS",
  "result": {
    "success": true,
    "reviews_count": 20
  },
  "traceback": null
}
```

#### 6. Worker 状态

```http
GET /api/v1/workers/status
```

#### 7. 健康检查

```http
GET /api/v1/health
```

#### 8. 支持的平台

```http
GET /api/v1/platforms
```

## 爬虫开发指南

### 添加新平台

1. 在 `app/spiders/` 目录下创建新的爬虫文件，继承 `BaseSpider`：

```python
from app.spiders.base import BaseSpider, Credentials, Review, StoreInfo

class NewPlatformSpider(BaseSpider):
    BASE_URL = "https://example.com"
    LOGIN_URL = "https://example.com/login"

    def __init__(self, credentials: Credentials) -> None:
        super().__init__("new_platform", credentials)

    async def login(self) -> bool:
        # 实现登录逻辑
        pass

    async def fetch_reviews(self, store_id: str, page: int = 1, limit: int = 20):
        # 实现评论获取逻辑
        pass

    async def fetch_store_info(self, store_id: str):
        # 实现店铺信息获取逻辑
        pass

    async def reply_review(self, review_id: str, content: str) -> bool:
        # 实现回复逻辑
        pass
```

2. 在 `app/spiders/factory.py` 中注册新爬虫：

```python
from app.spiders.new_platform import NewPlatformSpider

SPIDER_MAP = {
    # ... 现有平台
    "new_platform": NewPlatformSpider,
}
```

## 部署指南

### Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY pyproject.toml .
RUN pip install -e "."

# 安装 Playwright
RUN playwright install chromium

COPY . .

EXPOSE 8001

CMD ["python", "run.py"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  api:
    build: .
    ports:
      - "8001:8001"
    environment:
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/1
      - CELERY_RESULT_BACKEND=redis://redis:6379/2
    depends_on:
      - redis

  worker:
    build: .
    command: python worker.py
    environment:
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/1
      - CELERY_RESULT_BACKEND=redis://redis:6379/2
    depends_on:
      - redis
    deploy:
      replicas: 2  # 多 Worker 节点

  beat:
    build: .
    command: celery -A app.tasks.celery_app beat -l info
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/1
    depends_on:
      - redis
```

## 注意事项

1. **登录安全**：各平台可能有验证码、滑块验证等反爬机制，需要根据实际情况处理
2. **频率控制**：建议设置合理的请求间隔，避免被封禁
3. **Cookie 管理**：登录成功后保存 Cookie，减少重复登录
4. **异常处理**：网络不稳定时需要重试机制
5. **数据隐私**：妥善保管平台账号密码

## 许可证

MIT License

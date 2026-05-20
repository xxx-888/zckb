# 部署文档

评论管理平台后端生产环境部署指南。

## 目录

- [环境要求](#环境要求)
- [生产环境部署](#生产环境部署)
- [Docker 部署](#docker-部署)
- [Nginx 反向代理配置](#nginx-反向代理配置)
- [数据库配置](#数据库配置)
- [Redis 配置](#redis-配置)
- [日志配置](#日志配置)
- [监控告警](#监控告警)

---

## 环境要求

### 服务器配置

| 组件 | 最低配置 | 推荐配置 |
|------|----------|----------|
| CPU | 2 核 | 4 核+ |
| 内存 | 4 GB | 8 GB+ |
| 磁盘 | 50 GB SSD | 100 GB SSD+ |
| 带宽 | 5 Mbps | 10 Mbps+ |

### 软件版本

| 软件 | 版本要求 |
|------|----------|
| Python | 3.11+ |
| PostgreSQL | 14+ |
| Redis | 6+ |
| Nginx | 1.20+ |
| Docker | 20.10+ (可选) |
| Docker Compose | 2.0+ (可选) |

### 操作系统

- Ubuntu 22.04 LTS (推荐)
- CentOS 8/Rocky Linux 8
- Debian 11

---

## 生产环境部署

### 1. 系统初始化

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装基础工具
sudo apt install -y build-essential curl wget git vim htop net-tools

# 安装 Python 3.11
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-dev python3.11-venv

# 安装 Poetry
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 验证安装
poetry --version
```

### 2. 安装 PostgreSQL

```bash
# 安装 PostgreSQL 14
sudo apt install -y postgresql-14 postgresql-client-14 postgresql-contrib-14

# 启动服务
sudo systemctl enable postgresql
sudo systemctl start postgresql

# 创建数据库和用户
sudo -u postgres psql << EOF
CREATE DATABASE review_platform_db;
CREATE USER review_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE review_platform_db TO review_user;
\c review_platform_db
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOF

# 配置 PostgreSQL 监听
sudo vim /etc/postgresql/14/main/postgresql.conf
# 修改: listen_addresses = '*'

# 配置访问权限
sudo vim /etc/postgresql/14/main/pg_hba.conf
# 添加: host all all 0.0.0.0/0 md5

# 重启服务
sudo systemctl restart postgresql
```

### 3. 安装 Redis

```bash
# 安装 Redis
sudo apt install -y redis-server

# 配置 Redis
sudo vim /etc/redis/redis.conf
```

修改以下配置：

```conf
# 绑定地址（生产环境建议绑定内网IP）
bind 127.0.0.1

# 启用密码认证
requirepass your_redis_password

# 持久化配置
save 900 1
save 300 10
save 60 10000

# 内存限制（根据服务器配置调整）
maxmemory 512mb
maxmemory-policy allkeys-lru
```

```bash
# 启动服务
sudo systemctl enable redis-server
sudo systemctl restart redis-server

# 验证
redis-cli ping
```

### 4. 部署应用

```bash
# 创建应用目录
sudo mkdir -p /opt/review-platform
cd /opt/review-platform

# 克隆代码（或上传代码）
git clone https://your-repo-url.git backend
cd backend

# 安装依赖
poetry install --no-dev

# 创建日志目录
mkdir -p logs

# 创建环境变量文件
sudo vim /opt/review-platform/backend/.env
```

生产环境 `.env` 配置：

```env
# 应用配置
APP_NAME="评论管理平台"
APP_ENV=production
DEBUG=false
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# 数据库配置
DATABASE_URL=postgresql+asyncpg://review_user:your_secure_password@localhost:5432/review_platform_db

# Redis 配置
REDIS_URL=redis://:your_redis_password@localhost:6379/0

# AI 配置（生产环境必须配置）
OPENAI_API_KEY=your-openai-api-key
ZHIPU_API_KEY=your-zhipu-api-key
DEEPSEEK_API_KEY=your-deepseek-api-key

# 邮件配置
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=noreply@example.com
SMTP_PASSWORD=your-smtp-password

# 对象存储配置（阿里云OSS/腾讯云COS/AWS S3）
OSS_ACCESS_KEY=your-access-key
OSS_SECRET_KEY=your-secret-key
OSS_BUCKET=review-platform
OSS_ENDPOINT=oss-cn-beijing.aliyuncs.com
OSS_CUSTOM_DOMAIN=https://cdn.example.com

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=/opt/review-platform/backend/logs/app.log

# CORS 配置（前端域名）
CORS_ORIGINS=["https://your-frontend-domain.com"]

# 爬虫配置
SPIDER_CONCURRENT_LIMIT=5
SPIDER_REQUEST_TIMEOUT=30

# 通知配置
NOTIFICATION_RATE_LIMIT=100
```

### 5. 执行数据库迁移

```bash
cd /opt/review-platform/backend
poetry run alembic upgrade head
```

### 6. 初始化数据

```bash
cd /opt/review-platform/backend
poetry run python -m scripts.init_data
```

### 7. 配置 Systemd 服务

创建服务文件：

```bash
sudo vim /etc/systemd/system/review-platform.service
```

```ini
[Unit]
Description=Review Platform Backend
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/review-platform/backend
Environment=PATH=/opt/review-platform/backend/.venv/bin
Environment=PYTHONPATH=/opt/review-platform/backend
ExecStart=/opt/review-platform/backend/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=5

# 日志配置
StandardOutput=append:/var/log/review-platform/app.log
StandardError=append:/var/log/review-platform/error.log

[Install]
WantedBy=multi-user.target
```

```bash
# 创建日志目录
sudo mkdir -p /var/log/review-platform
sudo chown -R www-data:www-data /var/log/review-platform

# 设置权限
sudo chown -R www-data:www-data /opt/review-platform

# 重载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl enable review-platform
sudo systemctl start review-platform

# 查看状态
sudo systemctl status review-platform
sudo journalctl -u review-platform -f
```

---

## Docker 部署

### 使用 Docker Compose

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: review-platform-app
    restart: always
    ports:
      - "8000:8000"
    environment:
      - APP_ENV=production
      - DEBUG=false
      - DATABASE_URL=postgresql+asyncpg://review_user:${DB_PASSWORD}@db:5432/review_platform_db
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    env_file:
      - .env
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
      - ./uploads:/app/uploads
    networks:
      - review-platform-network

  db:
    image: postgres:14-alpine
    container_name: review-platform-db
    restart: always
    environment:
      - POSTGRES_DB=review_platform_db
      - POSTGRES_USER=review_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - review-platform-network

  redis:
    image: redis:7-alpine
    container_name: review-platform-redis
    restart: always
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - review-platform-network

  nginx:
    image: nginx:alpine
    container_name: review-platform-nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - ./logs/nginx:/var/log/nginx
    depends_on:
      - app
    networks:
      - review-platform-network

volumes:
  postgres_data:
  redis_data:

networks:
  review-platform-network:
    driver: bridge
```

创建 `Dockerfile`：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 Poetry
RUN pip install poetry

# 复制项目文件
COPY pyproject.toml poetry.lock ./
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./
COPY scripts ./scripts

# 安装依赖
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

部署命令：

```bash
# 创建环境变量文件
cp .env.example .env
# 编辑 .env 文件配置

# 启动服务
docker-compose up -d

# 执行迁移
docker-compose exec app poetry run alembic upgrade head

# 初始化数据
docker-compose exec app poetry run python -m scripts.init_data

# 查看日志
docker-compose logs -f app
```

---

## Nginx 反向代理配置

### 基础配置

```bash
sudo vim /etc/nginx/sites-available/review-platform
```

```nginx
upstream review_platform {
    server 127.0.0.1:8000;
    keepalive 64;
}

server {
    listen 80;
    server_name api.your-domain.com;

    # 重定向到 HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.your-domain.com;

    # SSL 证书配置
    ssl_certificate /etc/nginx/ssl/your-domain.crt;
    ssl_certificate_key /etc/nginx/ssl/your-domain.key;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # 日志配置
    access_log /var/log/nginx/review-platform-access.log;
    error_log /var/log/nginx/review-platform-error.log;

    # 客户端上传限制
    client_max_body_size 50M;

    # 超时配置
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;

    location / {
        proxy_pass http://review_platform;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # 静态文件（如果有）
    location /static {
        alias /opt/review-platform/backend/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # 上传文件
    location /uploads {
        alias /opt/review-platform/backend/uploads;
        expires 7d;
        add_header Cache-Control "public";
    }

    # 健康检查
    location /health {
        proxy_pass http://review_platform;
        access_log off;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/review-platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 高级配置（含限流）

```nginx
# 限流配置
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/m;

server {
    # ... 基础配置

    # API 限流
    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        proxy_pass http://review_platform;
        # ... 其他配置
    }

    # 认证接口更严格限流
    location /api/v1/auth/ {
        limit_req zone=auth_limit burst=5 nodelay;
        proxy_pass http://review_platform;
        # ... 其他配置
    }
}
```

---

## 数据库配置

### PostgreSQL 性能优化

编辑 `/etc/postgresql/14/main/postgresql.conf`：

```conf
# 连接配置
max_connections = 200

# 内存配置（根据服务器内存调整）
shared_buffers = 2GB
effective_cache_size = 6GB
work_mem = 20MB
maintenance_work_mem = 512MB

# WAL 配置
wal_buffers = 16MB
min_wal_size = 1GB
max_wal_size = 4GB
checkpoint_completion_target = 0.9

# 查询优化
random_page_cost = 1.1
effective_io_concurrency = 200

# 日志配置
log_destination = 'stderr'
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_rotation_age = 1d
log_rotation_size = 100MB
log_min_duration_statement = 1000
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '
log_statement = 'ddl'
```

### 定期备份

创建备份脚本 `/opt/backup/backup.sh`：

```bash
#!/bin/bash

BACKUP_DIR="/opt/backup/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="review_platform_db"
DB_USER="review_user"
RETENTION_DAYS=30

# 创建备份目录
mkdir -p $BACKUP_DIR

# 执行备份
pg_dump -U $DB_USER -h localhost $DB_NAME | gzip > $BACKUP_DIR/${DB_NAME}_${DATE}.sql.gz

# 删除旧备份
find $BACKUP_DIR -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete

# 上传到对象存储（可选）
# aws s3 cp $BACKUP_DIR/${DB_NAME}_${DATE}.sql.gz s3://your-backup-bucket/

echo "Backup completed: ${DB_NAME}_${DATE}.sql.gz"
```

```bash
# 添加定时任务
chmod +x /opt/backup/backup.sh
sudo crontab -e

# 每天凌晨 2 点执行备份
0 2 * * * /opt/backup/backup.sh >> /var/log/backup.log 2>&1
```

---

## Redis 配置

### 生产环境配置

```conf
# 绑定配置（仅允许本地访问，如需远程访问请配置防火墙）
bind 127.0.0.1
protected-mode yes

# 端口
port 6379

# 密码认证
requirepass your_strong_password_here

# 持久化
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# RDB 持久化
save 900 1
save 300 10
save 60 10000

# 内存管理
maxmemory 1gb
maxmemory-policy allkeys-lru

# 慢查询日志
slowlog-log-slower-than 10000
slowlog-max-len 128

# 客户端超时
timeout 300
tcp-keepalive 60

# 日志
loglevel notice
logfile /var/log/redis/redis-server.log
```

---

## 日志配置

### 应用日志

配置日志轮转 `/etc/logrotate.d/review-platform`：

```
/opt/review-platform/backend/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 www-data www-data
    sharedscripts
    postrotate
        systemctl reload review-platform
    endscript
}
```

### 结构化日志配置

在 `.env` 中配置：

```env
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=/opt/review-platform/backend/logs/app.log
```

### 日志收集（可选）

使用 Filebeat + ELK 或 Fluentd 收集日志：

```yaml
# filebeat.yml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /opt/review-platform/backend/logs/*.log
  json.keys_under_root: true
  json.add_error_key: true

output.elasticsearch:
  hosts: ["localhost:9200"]
  index: "review-platform-%{+yyyy.MM.dd}"
```

---

## 监控告警

### 使用 Prometheus + Grafana

创建 `docker-compose.monitoring.yml`：

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: always
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: always
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    restart: always
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro

  postgres-exporter:
    image: prometheuscommunity/postgres-exporter:latest
    container_name: postgres-exporter
    restart: always
    ports:
      - "9187:9187"
    environment:
      - DATA_SOURCE_NAME=postgresql://review_user:password@db:5432/review_platform_db?sslmode=disable

  redis-exporter:
    image: oliver006/redis_exporter:latest
    container_name: redis-exporter
    restart: always
    ports:
      - "9121:9121"
    environment:
      - REDIS_ADDR=redis://redis:6379
      - REDIS_PASSWORD=your_redis_password

volumes:
  prometheus_data:
  grafana_data:
```

### 健康检查端点

应用提供以下健康检查端点：

- `GET /health` - 基础健康检查
- `GET /health/db` - 数据库连接检查
- `GET /health/redis` - Redis 连接检查

### 告警规则示例

```yaml
# alerting.rules.yml
groups:
- name: review-platform
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High error rate detected"

  - alert: DatabaseDown
    expr: pg_up == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Database is down"

  - alert: RedisDown
    expr: redis_up == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Redis is down"

  - alert: HighMemoryUsage
    expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes > 0.85
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High memory usage"
```

---

## 安全建议

1. **使用 HTTPS**: 生产环境必须启用 SSL/TLS
2. **定期更新**: 及时更新系统和依赖包的安全补丁
3. **防火墙配置**: 仅开放必要的端口（80, 443, 22）
4. **强密码策略**: 使用复杂密码并定期更换
5. **访问控制**: 限制数据库和 Redis 的访问来源
6. **日志审计**: 定期审查访问日志和错误日志
7. **备份策略**: 定期备份数据并测试恢复流程

---

## 故障排查

### 常见问题

1. **服务无法启动**
   - 检查日志：`sudo journalctl -u review-platform -n 100`
   - 检查配置：`poetry run python -c "from app.core.config import settings; print(settings)"`

2. **数据库连接失败**
   - 检查 PostgreSQL 状态：`sudo systemctl status postgresql`
   - 检查连接配置：`.env` 中的 `DATABASE_URL`
   - 检查防火墙规则

3. **内存不足**
   - 调整 worker 数量：`--workers 2`
   - 增加服务器内存
   - 优化 PostgreSQL 配置

4. **502 Bad Gateway**
   - 检查后端服务是否运行
   - 检查 Nginx 配置
   - 检查端口是否被占用

---

## 更新部署

```bash
# 1. 拉取最新代码
cd /opt/review-platform/backend
git pull

# 2. 安装新依赖
poetry install --no-dev

# 3. 执行数据库迁移
poetry run alembic upgrade head

# 4. 重启服务
sudo systemctl restart review-platform

# 5. 验证服务状态
sudo systemctl status review-platform
curl http://localhost:8000/health
```

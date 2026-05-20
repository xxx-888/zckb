"""Initial migration - Create all 27 tables

Revision ID: 001
Revises:
Create Date: 2025-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """创建所有27张数据表。"""

    # ==================== 1. 枚举类型定义 ====================

    # 用户角色枚举
    op.execute("CREATE TYPE user_role AS ENUM ('HQ', 'OPERATOR', 'STORE')")
    # 用户状态枚举
    op.execute("CREATE TYPE user_status AS ENUM ('active', 'disabled')")
    # 区域层级枚举
    op.execute("CREATE TYPE region_level AS ENUM ('province', 'city', 'district')")
    # 门店类型枚举
    op.execute("CREATE TYPE store_type AS ENUM ('restaurant', 'hotel', 'beverage')")
    # 门店状态枚举
    op.execute("CREATE TYPE store_status AS ENUM ('active', 'pending', 'inactive')")
    # 平台名称枚举
    op.execute("CREATE TYPE store_platform_name AS ENUM ('meituan', 'dianping', 'douyin', 'taobao', 'jd')")
    # 评论情感枚举
    op.execute("CREATE TYPE review_sentiment AS ENUM ('positive', 'negative', 'neutral')")
    # 评论风险等级枚举
    op.execute("CREATE TYPE review_risk_level AS ENUM ('high', 'medium', 'low')")
    # 评论状态枚举
    op.execute("CREATE TYPE review_status AS ENUM ('normal', 'appealed', 'deleted')")
    # 回复审核状态枚举
    op.execute("CREATE TYPE reply_audit_status AS ENUM ('pending', 'approved', 'rejected', 'sent')")
    # 审核风险等级枚举
    op.execute("CREATE TYPE audit_risk_level AS ENUM ('high', 'medium', 'low')")
    # AI提供商枚举
    op.execute("CREATE TYPE ai_provider AS ENUM ('openai', 'zhipu', 'wenxin', 'deepseek', 'local')")
    # 提示词模板类型枚举
    op.execute("CREATE TYPE prompt_template_type AS ENUM ('good_review', 'bad_review', 'neutral_review', 'appeal', 'weekly_report')")
    # AI处理状态枚举
    op.execute("CREATE TYPE ai_processing_status AS ENUM ('success', 'failed')")
    # 通知渠道类型枚举
    op.execute("CREATE TYPE notification_channel_type AS ENUM ('wechat', 'dingtalk', 'feishu', 'email', 'sms', 'push')")
    # 通知事件类型枚举
    op.execute("CREATE TYPE notification_event_type AS ENUM ('new_review', 'negative_alert', 'weekly_report', 'spider_status')")
    # 通知频率枚举
    op.execute("CREATE TYPE notification_frequency AS ENUM ('realtime', 'daily', 'weekly')")
    # 通知历史状态枚举
    op.execute("CREATE TYPE notification_history_status AS ENUM ('pending', 'sent', 'failed')")
    # 通知模板事件类型枚举
    op.execute("CREATE TYPE notification_template_event_type AS ENUM ('new_review', 'negative_alert', 'weekly_report', 'spider_status')")
    # 订阅状态枚举
    op.execute("CREATE TYPE subscription_status AS ENUM ('trial', 'active', 'expired', 'cancelled')")
    # 爬虫平台状态枚举
    op.execute("CREATE TYPE spider_platform_status AS ENUM ('active', 'paused', 'error')")
    # 爬虫平台名称枚举
    op.execute("CREATE TYPE spider_platform_name AS ENUM ('meituan', 'dianping', 'douyin', 'taobao', 'jd')")
    # 爬虫同步状态枚举
    op.execute("CREATE TYPE spider_sync_status AS ENUM ('running', 'success', 'failed')")
    # 爬虫任务类型枚举
    op.execute("CREATE TYPE spider_task_type AS ENUM ('full_sync', 'incremental', 'reply')")
    # 爬虫任务状态枚举
    op.execute("CREATE TYPE spider_task_status AS ENUM ('pending', 'running', 'success', 'failed')")
    # 竞品分析状态枚举
    op.execute("CREATE TYPE competitor_analysis_status AS ENUM ('pending', 'collecting', 'analyzing', 'completed', 'failed')")
    # 竞品支付状态枚举
    op.execute("CREATE TYPE competitor_payment_status AS ENUM ('unpaid', 'paid')")
    # 回复模板类型枚举
    op.execute("CREATE TYPE reply_template_type AS ENUM ('good', 'bad', 'neutral')")
    # 自动回复模式枚举
    op.execute("CREATE TYPE auto_reply_mode AS ENUM ('smart', 'semi_auto', 'manual')")

    # ==================== 2. 用户相关表 ====================

    # users 表
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('phone', sa.String(length=20), nullable=True, comment='手机号'),
        sa.Column('email', sa.String(length=255), nullable=True, comment='邮箱'),
        sa.Column('username', sa.String(length=100), nullable=False, comment='用户名'),
        sa.Column('hashed_password', sa.String(length=255), nullable=False, comment='加密密码'),
        sa.Column('avatar', sa.String(length=500), nullable=True, comment='头像URL'),
        sa.Column('role', sa.Enum('HQ', 'OPERATOR', 'STORE', name='user_role'), nullable=False, comment='角色: HQ-总部, OPERATOR-运营, STORE-门店'),
        sa.Column('status', sa.Enum('active', 'disabled', name='user_status'), nullable=False, comment='状态: active-启用, disabled-禁用'),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True, comment='最后登录时间'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.PrimaryKeyConstraint('id'),
        comment='用户表'
    )
    op.create_index('ix_users_phone', 'users', ['phone'], unique=True)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # regions 表
    op.create_table(
        'regions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('name', sa.String(length=100), nullable=False, comment='区域名称'),
        sa.Column('parent_id', postgresql.UUID(as_uuid=True), nullable=True, comment='父级区域ID'),
        sa.Column('level', sa.Enum('province', 'city', 'district', name='region_level'), nullable=False, comment='层级: province-省, city-市, district-区'),
        sa.Column('code', sa.String(length=20), nullable=True, comment='行政区划代码'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['parent_id'], ['regions.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        comment='区域层级表（省/市/区）'
    )
    op.create_index('ix_regions_parent_id', 'regions', ['parent_id'])
    op.create_index('ix_regions_code', 'regions', ['code'])

    # ==================== 3. 门店相关表 ====================

    # stores 表
    op.create_table(
        'stores',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('name', sa.String(length=255), nullable=False, comment='门店名称'),
        sa.Column('type', sa.Enum('restaurant', 'hotel', 'beverage', name='store_type'), nullable=False, comment='门店类型: restaurant-餐饮, hotel-酒店, beverage-饮品'),
        sa.Column('address', sa.String(length=500), nullable=True, comment='门店地址'),
        sa.Column('owner_name', sa.String(length=100), nullable=True, comment='店主姓名'),
        sa.Column('phone', sa.String(length=20), nullable=True, comment='联系电话'),
        sa.Column('status', sa.Enum('active', 'pending', 'inactive', name='store_status'), nullable=False, comment='状态: active-活跃, pending-待审核, inactive-停用'),
        sa.Column('health_score', sa.Float(), nullable=True, comment='健康评分'),
        sa.Column('platform_count', sa.Integer(), nullable=False, default=0, comment='关联平台数量'),
        sa.Column('review_count', sa.Integer(), nullable=False, default=0, comment='评论总数'),
        sa.Column('region_id', postgresql.UUID(as_uuid=True), nullable=True, comment='区域ID'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['region_id'], ['regions.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        comment='门店表'
    )
    op.create_index('ix_stores_region_id', 'stores', ['region_id'])

    # store_platforms 表
    op.create_table(
        'store_platforms',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=False, comment='门店ID'),
        sa.Column('platform', sa.Enum('meituan', 'dianping', 'douyin', 'taobao', 'jd', name='store_platform_name'), nullable=False, comment='平台名称'),
        sa.Column('platform_store_id', sa.String(length=100), nullable=True, comment='平台侧门店ID'),
        sa.Column('platform_store_name', sa.String(length=255), nullable=True, comment='平台侧门店名称'),
        sa.Column('connected', sa.Boolean(), nullable=False, default=False, comment='是否已连接'),
        sa.Column('last_sync_at', sa.DateTime(timezone=True), nullable=True, comment='最后同步时间'),
        sa.Column('sync_status', sa.String(length=50), nullable=True, comment='同步状态'),
        sa.Column('config', postgresql.JSONB(), nullable=True, comment='平台配置(JSONB)'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        comment='门店-平台关联表'
    )
    op.create_index('ix_store_platforms_store_id', 'store_platforms', ['store_id'])

    # user_stores 表（多对多关联）
    op.create_table(
        'user_stores',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False, comment='用户ID'),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=False, comment='门店ID'),
        sa.Column('role_in_store', sa.String(length=50), nullable=True, comment='门店内角色'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'store_id'),
        comment='用户-门店关联表（多对多）'
    )

    # ==================== 4. 评论相关表 ====================

    # reviews 表
    op.create_table(
        'reviews',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=False, comment='门店ID'),
        sa.Column('platform', sa.Enum('meituan', 'dianping', 'douyin', 'taobao', 'jd', name='store_platform_name'), nullable=False, comment='来源平台'),
        sa.Column('platform_review_id', sa.String(length=100), nullable=False, comment='平台侧评论ID'),
        sa.Column('user_name', sa.String(length=100), nullable=True, comment='评论者昵称'),
        sa.Column('user_avatar', sa.String(length=500), nullable=True, comment='评论者头像URL'),
        sa.Column('rating', sa.Integer(), nullable=False, comment='评分(1-5)'),
        sa.Column('content', sa.Text(), nullable=True, comment='评论内容'),
        sa.Column('images', postgresql.ARRAY(sa.Text()), nullable=True, comment='评论图片URL列表'),
        sa.Column('sentiment', sa.Enum('positive', 'negative', 'neutral', name='review_sentiment'), nullable=True, comment='情感分析: positive-正面, negative-负面, neutral-中性'),
        sa.Column('tags', postgresql.ARRAY(sa.Text()), nullable=True, comment='标签列表'),
        sa.Column('raw_json', postgresql.JSONB(), nullable=True, comment='原始爬虫数据(JSONB)'),
        sa.Column('reply', sa.Text(), nullable=True, comment='商家回复内容'),
        sa.Column('reply_time', sa.DateTime(timezone=True), nullable=True, comment='回复时间'),
        sa.Column('ai_generated', sa.Boolean(), nullable=False, default=False, comment='是否AI生成回复'),
        sa.Column('ai_reply_draft', sa.Text(), nullable=True, comment='AI回复草稿'),
        sa.Column('risk_level', sa.Enum('high', 'medium', 'low', name='review_risk_level'), nullable=True, comment='风险等级: high-高, medium-中, low-低'),
        sa.Column('status', sa.Enum('normal', 'appealed', 'deleted', name='review_status'), nullable=False, default='normal', comment='状态: normal-正常, appealed-申诉中, deleted-已删除'),
        sa.Column('platform_created_at', sa.DateTime(timezone=True), nullable=True, comment='平台侧评论时间'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        comment='评论表'
    )
    op.create_index('ix_reviews_store_id', 'reviews', ['store_id'])

    # reply_audits 表
    op.create_table(
        'reply_audits',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('review_id', postgresql.UUID(as_uuid=True), nullable=False, comment='评论ID'),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=False, comment='门店ID'),
        sa.Column('ai_reply_content', sa.Text(), nullable=True, comment='AI回复内容'),
        sa.Column('status', sa.Enum('pending', 'approved', 'rejected', 'sent', name='reply_audit_status'), nullable=False, default='pending', comment='审核状态: pending-待审核, approved-已通过, rejected-已拒绝, sent-已发送'),
        sa.Column('risk_level', sa.Enum('high', 'medium', 'low', name='audit_risk_level'), nullable=True, comment='风险等级'),
        sa.Column('scores', postgresql.JSONB(), nullable=True, comment='评分(JSONB): realism/empathy/concreteness/consistency'),
        sa.Column('reject_reason', sa.Text(), nullable=True, comment='拒绝原因'),
        sa.Column('auditor_id', postgresql.UUID(as_uuid=True), nullable=True, comment='审核人ID'),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True, comment='审核时间'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['review_id'], ['reviews.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['auditor_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        comment='回复审核表'
    )
    op.create_index('ix_reply_audits_review_id', 'reply_audits', ['review_id'])
    op.create_index('ix_reply_audits_store_id', 'reply_audits', ['store_id'])

    # ==================== 5. AI配置相关表 ====================

    # ai_model_configs 表
    op.create_table(
        'ai_model_configs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('provider', sa.Enum('openai', 'zhipu', 'wenxin', 'deepseek', 'local', name='ai_provider'), nullable=False, comment='提供商: openai/zhipu/wenxin/deepseek/local'),
        sa.Column('model_name', sa.String(length=100), nullable=False, comment='模型名称'),
        sa.Column('api_key_encrypted', sa.String(length=500), nullable=True, comment='加密后的API Key'),
        sa.Column('endpoint_url', sa.String(length=500), nullable=True, comment='API端点URL'),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True, comment='是否启用'),
        sa.Column('priority', sa.Integer(), nullable=False, default=0, comment='优先级(数值越大优先级越高)'),
        sa.Column('max_tokens', sa.Integer(), nullable=False, default=2048, comment='最大token数'),
        sa.Column('temperature', sa.Float(), nullable=False, default=0.7, comment='温度参数'),
        sa.Column('config', postgresql.JSONB(), nullable=True, comment='额外配置(JSONB)'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.PrimaryKeyConstraint('id'),
        comment='AI 模型配置表'
    )

    # ai_prompt_templates 表
    op.create_table(
        'ai_prompt_templates',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('name', sa.String(length=100), nullable=False, comment='模板名称'),
        sa.Column('type', sa.Enum('good_review', 'bad_review', 'neutral_review', 'appeal', 'weekly_report', name='prompt_template_type'), nullable=False, comment='模板类型'),
        sa.Column('template_text', sa.Text(), nullable=False, comment='模板文本'),
        sa.Column('variables', postgresql.ARRAY(sa.Text()), nullable=True, comment='变量列表'),
        sa.Column('system_prompt', sa.Text(), nullable=True, comment='系统提示词'),
        sa.Column('is_default', sa.Boolean(), nullable=False, default=False, comment='是否为默认模板'),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True, comment='是否启用'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.PrimaryKeyConstraint('id'),
        comment='AI 提示词模板表'
    )

    # ai_rule_engines 表
    op.create_table(
        'ai_rule_engines',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('name', sa.String(length=100), nullable=False, comment='规则名称'),
        sa.Column('description', sa.Text(), nullable=True, comment='规则描述'),
        sa.Column('rules', postgresql.JSONB(), nullable=True, comment='规则定义(JSONB)'),
        sa.Column('priority', sa.Integer(), nullable=False, default=0, comment='优先级'),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True, comment='是否启用'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.PrimaryKeyConstraint('id'),
        comment='AI 规则引擎表'
    )

    # ai_processing_logs 表
    op.create_table(
        'ai_processing_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('review_id', postgresql.UUID(as_uuid=True), nullable=True, comment='关联评论ID'),
        sa.Column('model_config_id', postgresql.UUID(as_uuid=True), nullable=True, comment='模型配置ID'),
        sa.Column('input_tokens', sa.Integer(), nullable=True, comment='输入token数'),
        sa.Column('output_tokens', sa.Integer(), nullable=True, comment='输出token数'),
        sa.Column('processing_time_ms', sa.Integer(), nullable=True, comment='处理耗时(毫秒)'),
        sa.Column('status', sa.Enum('success', 'failed', name='ai_processing_status'), nullable=False, comment='处理状态: success-成功, failed-失败'),
        sa.Column('error_message', sa.Text(), nullable=True, comment='错误信息'),
        sa.Column('input_text', sa.Text(), nullable=True, comment='输入文本'),
        sa.Column('output_text', sa.Text(), nullable=True, comment='输出文本'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['review_id'], ['reviews.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['model_config_id'], ['ai_model_configs.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        comment='AI 处理日志表'
    )
    op.create_index('ix_ai_processing_logs_review_id', 'ai_processing_logs', ['review_id'])
    op.create_index('ix_ai_processing_logs_model_config_id', 'ai_processing_logs', ['model_config_id'])

    # ==================== 6. 通知相关表 ====================

    # notification_channels 表
    op.create_table(
        'notification_channels',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('name', sa.String(length=100), nullable=False, comment='渠道名称'),
        sa.Column('type', sa.Enum('wechat', 'dingtalk', 'feishu', 'email', 'sms', 'push', name='notification_channel_type'), nullable=False, comment='渠道类型: wechat/dingtalk/feishu/email/sms/push'),
        sa.Column('webhook_url', sa.String(length=500), nullable=True, comment='Webhook URL'),
        sa.Column('config', postgresql.JSONB(), nullable=True, comment='渠道配置(JSONB)'),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True, comment='是否启用'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.PrimaryKeyConstraint('id'),
        comment='通知渠道表'
    )

    # notification_rules 表
    op.create_table(
        'notification_rules',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('name', sa.String(length=100), nullable=False, comment='规则名称'),
        sa.Column('channel_id', postgresql.UUID(as_uuid=True), nullable=False, comment='渠道ID'),
        sa.Column('event_type', sa.Enum('new_review', 'negative_alert', 'weekly_report', 'spider_status', name='notification_event_type'), nullable=False, comment='事件类型: new_review/negative_alert/weekly_report/spider_status'),
        sa.Column('condition', postgresql.JSONB(), nullable=True, comment='触发条件(JSONB)'),
        sa.Column('frequency', sa.Enum('realtime', 'daily', 'weekly', name='notification_frequency'), nullable=False, default='realtime', comment='频率: realtime-实时, daily-每日, weekly-每周'),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True, comment='是否启用'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['channel_id'], ['notification_channels.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        comment='通知规则表'
    )
    op.create_index('ix_notification_rules_channel_id', 'notification_rules', ['channel_id'])

    # notification_histories 表
    op.create_table(
        'notification_histories',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('rule_id', postgresql.UUID(as_uuid=True), nullable=True, comment='规则ID'),
        sa.Column('channel_id', postgresql.UUID(as_uuid=True), nullable=False, comment='渠道ID'),
        sa.Column('title', sa.String(length=255), nullable=True, comment='通知标题'),
        sa.Column('content', sa.Text(), nullable=True, comment='通知内容'),
        sa.Column('recipient', sa.String(length=255), nullable=True, comment='接收者'),
        sa.Column('status', sa.Enum('pending', 'sent', 'failed', name='notification_history_status'), nullable=False, default='pending', comment='状态: pending-待发送, sent-已发送, failed-发送失败'),
        sa.Column('error_message', sa.Text(), nullable=True, comment='错误信息'),
        sa.Column('latency_ms', sa.Integer(), nullable=True, comment='发送延迟(毫秒)'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['rule_id'], ['notification_rules.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['channel_id'], ['notification_channels.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        comment='通知历史记录表'
    )
    op.create_index('ix_notification_histories_rule_id', 'notification_histories', ['rule_id'])
    op.create_index('ix_notification_histories_channel_id', 'notification_histories', ['channel_id'])

    # notification_templates 表
    op.create_table(
        'notification_templates',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('name', sa.String(length=100), nullable=False, comment='模板名称'),
        sa.Column('event_type', sa.Enum('new_review', 'negative_alert', 'weekly_report', 'spider_status', name='notification_template_event_type'), nullable=False, comment='事件类型'),
        sa.Column('template_text', sa.Text(), nullable=False, comment='模板文本'),
        sa.Column('variables', postgresql.ARRAY(sa.Text()), nullable=True, comment='变量列表'),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True, comment='是否启用'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.PrimaryKeyConstraint('id'),
        comment='通知模板表'
    )

    # ==================== 7. 订阅相关表 ====================

    # subscription_plans 表
    op.create_table(
        'subscription_plans',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('name', sa.String(length=100), nullable=False, comment='套餐名称(标准版/旗舰版/企业版)'),
        sa.Column('price_monthly', sa.Float(), nullable=False, default=0.0, comment='月价格'),
        sa.Column('price_yearly', sa.Float(), nullable=False, default=0.0, comment='年价格'),
        sa.Column('features', postgresql.JSONB(), nullable=True, comment='功能特性列表(JSONB)'),
        sa.Column('max_stores', sa.Integer(), nullable=False, default=1, comment='最大门店数'),
        sa.Column('max_reviews_per_month', sa.Integer(), nullable=True, comment='每月最大评论数'),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True, comment='是否启用'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.PrimaryKeyConstraint('id'),
        comment='订阅套餐表'
    )

    # user_subscriptions 表
    op.create_table(
        'user_subscriptions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False, comment='用户ID'),
        sa.Column('plan_id', postgresql.UUID(as_uuid=True), nullable=False, comment='套餐ID'),
        sa.Column('status', sa.Enum('trial', 'active', 'expired', 'cancelled', name='subscription_status'), nullable=False, default='trial', comment='状态: trial-试用, active-活跃, expired-已过期, cancelled-已取消'),
        sa.Column('start_date', sa.Date(), nullable=False, comment='开始日期'),
        sa.Column('end_date', sa.Date(), nullable=True, comment='结束日期'),
        sa.Column('auto_renew', sa.Boolean(), nullable=False, default=True, comment='是否自动续费'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['plan_id'], ['subscription_plans.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        comment='用户订阅表'
    )
    op.create_index('ix_user_subscriptions_user_id', 'user_subscriptions', ['user_id'])
    op.create_index('ix_user_subscriptions_plan_id', 'user_subscriptions', ['plan_id'])

    # ==================== 8. 爬虫相关表 ====================

    # spider_platforms 表
    op.create_table(
        'spider_platforms',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('name', sa.Enum('meituan', 'dianping', 'douyin', 'taobao', 'jd', name='spider_platform_name'), nullable=False, unique=True, comment='平台名称: meituan/dianping/douyin/taobao/jd'),
        sa.Column('display_name', sa.String(length=100), nullable=False, comment='显示名称'),
        sa.Column('status', sa.Enum('active', 'paused', 'error', name='spider_platform_status'), nullable=False, default='active', comment='状态: active-活跃, paused-暂停, error-异常'),
        sa.Column('reliability', sa.Float(), nullable=False, default=1.0, comment='可靠性评分'),
        sa.Column('error_log', sa.Text(), nullable=True, comment='错误日志'),
        sa.Column('config', postgresql.JSONB(), nullable=True, comment='配置(JSONB，含cookies等)'),
        sa.Column('last_sync_at', sa.DateTime(timezone=True), nullable=True, comment='最后同步时间'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.PrimaryKeyConstraint('id'),
        comment='爬虫平台表'
    )

    # spider_sync_logs 表
    op.create_table(
        'spider_sync_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('platform_id', postgresql.UUID(as_uuid=True), nullable=False, comment='平台ID'),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=True, comment='门店ID'),
        sa.Column('status', sa.Enum('running', 'success', 'failed', name='spider_sync_status'), nullable=False, comment='状态: running-运行中, success-成功, failed-失败'),
        sa.Column('records_synced', sa.Integer(), nullable=False, default=0, comment='同步记录数'),
        sa.Column('error_message', sa.Text(), nullable=True, comment='错误信息'),
        sa.Column('duration_ms', sa.Integer(), nullable=True, comment='耗时(毫秒)'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True, comment='开始时间'),
        sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True, comment='结束时间'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['platform_id'], ['spider_platforms.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        comment='爬虫同步日志表'
    )
    op.create_index('ix_spider_sync_logs_platform_id', 'spider_sync_logs', ['platform_id'])
    op.create_index('ix_spider_sync_logs_store_id', 'spider_sync_logs', ['store_id'])

    # spider_tasks 表（使用 BigInteger 自增ID）
    op.create_table(
        'spider_tasks',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='任务ID(自增)'),
        sa.Column('platform_id', postgresql.UUID(as_uuid=True), nullable=False, comment='平台ID'),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=True, comment='门店ID'),
        sa.Column('task_type', sa.Enum('full_sync', 'incremental', 'reply', name='spider_task_type'), nullable=False, comment='任务类型: full_sync-全量同步, incremental-增量同步, reply-回复同步'),
        sa.Column('status', sa.Enum('pending', 'running', 'success', 'failed', name='spider_task_status'), nullable=False, default='pending', comment='状态: pending-待执行, running-运行中, success-成功, failed-失败'),
        sa.Column('priority', sa.Integer(), nullable=False, default=0, comment='优先级'),
        sa.Column('result', postgresql.JSONB(), nullable=True, comment='任务结果(JSONB)'),
        sa.Column('error_message', sa.Text(), nullable=True, comment='错误信息'),
        sa.Column('scheduled_at', sa.DateTime(timezone=True), nullable=True, comment='计划执行时间'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True, comment='开始执行时间'),
        sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True, comment='执行完成时间'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['platform_id'], ['spider_platforms.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        comment='爬虫任务表'
    )
    op.create_index('ix_spider_tasks_platform_id', 'spider_tasks', ['platform_id'])
    op.create_index('ix_spider_tasks_store_id', 'spider_tasks', ['store_id'])

    # ==================== 9. 报告相关表 ====================

    # annual_reports 表
    op.create_table(
        'annual_reports',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=False, comment='门店ID'),
        sa.Column('year', sa.Integer(), nullable=False, comment='年份'),
        sa.Column('total_reviews', sa.Integer(), nullable=False, default=0, comment='评论总数'),
        sa.Column('average_rating', sa.Float(), nullable=True, comment='平均评分'),
        sa.Column('sentiment_distribution', postgresql.JSONB(), nullable=True, comment='情感分布(JSONB)'),
        sa.Column('reply_stats', postgresql.JSONB(), nullable=True, comment='回复统计(JSONB)'),
        sa.Column('monthly_data', postgresql.JSONB(), nullable=True, comment='月度数据(JSONB)'),
        sa.Column('top_keywords', postgresql.JSONB(), nullable=True, comment='热门关键词(JSONB)'),
        sa.Column('category_scores', postgresql.JSONB(), nullable=True, comment='分类评分(JSONB)'),
        sa.Column('insights', postgresql.JSONB(), nullable=True, comment='洞察(JSONB): year_over_year/highlights/improvements/ai_summary'),
        sa.Column('generated_at', sa.DateTime(timezone=True), nullable=True, comment='生成时间'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        comment='年度报告表'
    )
    op.create_index('ix_annual_reports_store_id', 'annual_reports', ['store_id'])

    # weekly_briefs 表
    op.create_table(
        'weekly_briefs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=False, comment='门店ID'),
        sa.Column('week_start', sa.DateTime(timezone=True), nullable=False, comment='周开始日期'),
        sa.Column('week_end', sa.DateTime(timezone=True), nullable=False, comment='周结束日期'),
        sa.Column('total_reviews', sa.Integer(), nullable=False, default=0, comment='本周评论总数'),
        sa.Column('positive_count', sa.Integer(), nullable=False, default=0, comment='正面评论数'),
        sa.Column('negative_count', sa.Integer(), nullable=False, default=0, comment='负面评论数'),
        sa.Column('neutral_count', sa.Integer(), nullable=False, default=0, comment='中性评论数'),
        sa.Column('avg_rating', sa.Float(), nullable=True, comment='平均评分'),
        sa.Column('top_issues', postgresql.ARRAY(sa.Text()), nullable=True, comment='主要问题列表'),
        sa.Column('top_praises', postgresql.ARRAY(sa.Text()), nullable=True, comment='主要好评列表'),
        sa.Column('dish_analysis', postgresql.JSONB(), nullable=True, comment='菜品分析(JSONB)'),
        sa.Column('ai_summary', sa.Text(), nullable=True, comment='AI 摘要'),
        sa.Column('generated_at', sa.DateTime(timezone=True), nullable=True, comment='生成时间'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        comment='周报简报表'
    )
    op.create_index('ix_weekly_briefs_store_id', 'weekly_briefs', ['store_id'])

    # competitors 表
    op.create_table(
        'competitors',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=False, comment='门店ID'),
        sa.Column('name', sa.String(length=255), nullable=False, comment='竞品名称'),
        sa.Column('platform', sa.Enum('meituan', 'dianping', 'douyin', 'taobao', 'jd', name='competitor_platform'), nullable=False, comment='平台'),
        sa.Column('platform_store_id', sa.String(length=100), nullable=True, comment='平台侧门店ID'),
        sa.Column('rating', sa.Float(), nullable=True, comment='评分'),
        sa.Column('positive_rate', sa.Float(), nullable=True, comment='好评率'),
        sa.Column('review_count', sa.Integer(), nullable=False, default=0, comment='评论数'),
        sa.Column('trends_data', postgresql.JSONB(), nullable=True, comment='趋势数据(JSONB)'),
        sa.Column('bad_tags', postgresql.ARRAY(sa.Text()), nullable=True, comment='差评标签列表'),
        sa.Column('last_synced_at', sa.DateTime(timezone=True), nullable=True, comment='最后同步时间'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        comment='竞品表'
    )
    op.create_index('ix_competitors_store_id', 'competitors', ['store_id'])

    # competitor_analysis_tasks 表
    op.create_table(
        'competitor_analysis_tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('competitor_id', postgresql.UUID(as_uuid=True), nullable=False, comment='竞品ID'),
        sa.Column('status', sa.Enum('pending', 'collecting', 'analyzing', 'completed', 'failed', name='competitor_analysis_status'), nullable=False, default='pending', comment='状态: pending-待处理, collecting-采集中, analyzing-分析中, completed-已完成, failed-失败'),
        sa.Column('payment_status', sa.Enum('unpaid', 'paid', name='competitor_payment_status'), nullable=False, default='unpaid', comment='支付状态: unpaid-未支付, paid-已支付'),
        sa.Column('price', sa.Float(), nullable=False, default=0.0, comment='价格'),
        sa.Column('result_data', postgresql.JSONB(), nullable=True, comment='分析结果数据(JSONB)'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['competitor_id'], ['competitors.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        comment='竞品分析任务表'
    )
    op.create_index('ix_competitor_analysis_tasks_competitor_id', 'competitor_analysis_tasks', ['competitor_id'])

    # ==================== 10. 设置相关表 ====================

    # reply_templates 表
    op.create_table(
        'reply_templates',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True, comment='创建用户ID'),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=True, comment='门店ID'),
        sa.Column('name', sa.String(length=100), nullable=False, comment='模板名称'),
        sa.Column('type', sa.Enum('good', 'bad', 'neutral', name='reply_template_type'), nullable=False, comment='模板类型: good-好评, bad-差评, neutral-中性'),
        sa.Column('content', sa.String(length=2000), nullable=False, comment='模板内容'),
        sa.Column('variables', postgresql.ARRAY(sa.String()), nullable=True, comment='变量列表'),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True, comment='是否启用'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        comment='回复模板表'
    )
    op.create_index('ix_reply_templates_user_id', 'reply_templates', ['user_id'])
    op.create_index('ix_reply_templates_store_id', 'reply_templates', ['store_id'])

    # auto_reply_configs 表
    op.create_table(
        'auto_reply_configs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=False, comment='门店ID'),
        sa.Column('mode', sa.Enum('smart', 'semi_auto', 'manual', name='auto_reply_mode'), nullable=False, default='semi_auto', comment='模式: smart-智能, semi_auto-半自动, manual-手动'),
        sa.Column('auto_reply_enabled', sa.Boolean(), nullable=False, default=False, comment='是否启用自动回复'),
        sa.Column('work_hours_only', sa.Boolean(), nullable=False, default=True, comment='仅工作时间回复'),
        sa.Column('work_start_time', sa.Time(), nullable=True, comment='工作开始时间'),
        sa.Column('work_end_time', sa.Time(), nullable=True, comment='工作结束时间'),
        sa.Column('keyword_reply_enabled', sa.Boolean(), nullable=False, default=False, comment='是否启用关键词回复'),
        sa.Column('keywords', postgresql.JSONB(), nullable=True, comment='关键词配置(JSONB)'),
        sa.Column('ai_suggest_enabled', sa.Boolean(), nullable=False, default=True, comment='是否启用AI建议'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('store_id'),
        comment='自动回复配置表'
    )
    op.create_index('ix_auto_reply_configs_store_id', 'auto_reply_configs', ['store_id'])

    # user_notification_settings 表
    op.create_table(
        'user_notification_settings',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='主键ID'),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False, comment='用户ID'),
        sa.Column('new_review_enabled', sa.Boolean(), nullable=False, default=True, comment='新评论通知'),
        sa.Column('negative_alert_enabled', sa.Boolean(), nullable=False, default=True, comment='差评预警通知'),
        sa.Column('weekly_report_enabled', sa.Boolean(), nullable=False, default=True, comment='周报通知'),
        sa.Column('email_enabled', sa.Boolean(), nullable=False, default=False, comment='邮件通知'),
        sa.Column('sms_enabled', sa.Boolean(), nullable=False, default=False, comment='短信通知'),
        sa.Column('push_enabled', sa.Boolean(), nullable=False, default=True, comment='推送通知'),
        sa.Column('quiet_hours_start', sa.Time(), nullable=True, comment='免打扰开始时间'),
        sa.Column('quiet_hours_end', sa.Time(), nullable=True, comment='免打扰结束时间'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新时间'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id'),
        comment='用户通知设置表'
    )
    op.create_index('ix_user_notification_settings_user_id', 'user_notification_settings', ['user_id'])


def downgrade() -> None:
    """回滚所有表结构。"""

    # ==================== 10. 设置相关表 ====================
    op.drop_index('ix_user_notification_settings_user_id', table_name='user_notification_settings')
    op.drop_table('user_notification_settings')
    op.drop_index('ix_auto_reply_configs_store_id', table_name='auto_reply_configs')
    op.drop_table('auto_reply_configs')
    op.drop_index('ix_reply_templates_store_id', table_name='reply_templates')
    op.drop_index('ix_reply_templates_user_id', table_name='reply_templates')
    op.drop_table('reply_templates')

    # ==================== 9. 报告相关表 ====================
    op.drop_index('ix_competitor_analysis_tasks_competitor_id', table_name='competitor_analysis_tasks')
    op.drop_table('competitor_analysis_tasks')
    op.drop_index('ix_competitors_store_id', table_name='competitors')
    op.drop_table('competitors')
    op.drop_index('ix_weekly_briefs_store_id', table_name='weekly_briefs')
    op.drop_table('weekly_briefs')
    op.drop_index('ix_annual_reports_store_id', table_name='annual_reports')
    op.drop_table('annual_reports')

    # ==================== 8. 爬虫相关表 ====================
    op.drop_index('ix_spider_tasks_store_id', table_name='spider_tasks')
    op.drop_index('ix_spider_tasks_platform_id', table_name='spider_tasks')
    op.drop_table('spider_tasks')
    op.drop_index('ix_spider_sync_logs_store_id', table_name='spider_sync_logs')
    op.drop_index('ix_spider_sync_logs_platform_id', table_name='spider_sync_logs')
    op.drop_table('spider_sync_logs')
    op.drop_table('spider_platforms')

    # ==================== 7. 订阅相关表 ====================
    op.drop_index('ix_user_subscriptions_plan_id', table_name='user_subscriptions')
    op.drop_index('ix_user_subscriptions_user_id', table_name='user_subscriptions')
    op.drop_table('user_subscriptions')
    op.drop_table('subscription_plans')

    # ==================== 6. 通知相关表 ====================
    op.drop_table('notification_templates')
    op.drop_index('ix_notification_histories_channel_id', table_name='notification_histories')
    op.drop_index('ix_notification_histories_rule_id', table_name='notification_histories')
    op.drop_table('notification_histories')
    op.drop_index('ix_notification_rules_channel_id', table_name='notification_rules')
    op.drop_table('notification_rules')
    op.drop_table('notification_channels')

    # ==================== 5. AI配置相关表 ====================
    op.drop_index('ix_ai_processing_logs_model_config_id', table_name='ai_processing_logs')
    op.drop_index('ix_ai_processing_logs_review_id', table_name='ai_processing_logs')
    op.drop_table('ai_processing_logs')
    op.drop_table('ai_rule_engines')
    op.drop_table('ai_prompt_templates')
    op.drop_table('ai_model_configs')

    # ==================== 4. 评论相关表 ====================
    op.drop_index('ix_reply_audits_store_id', table_name='reply_audits')
    op.drop_index('ix_reply_audits_review_id', table_name='reply_audits')
    op.drop_table('reply_audits')
    op.drop_index('ix_reviews_store_id', table_name='reviews')
    op.drop_table('reviews')

    # ==================== 3. 门店相关表 ====================
    op.drop_table('user_stores')
    op.drop_index('ix_store_platforms_store_id', table_name='store_platforms')
    op.drop_table('store_platforms')
    op.drop_index('ix_stores_region_id', table_name='stores')
    op.drop_table('stores')

    # ==================== 2. 用户相关表 ====================
    op.drop_index('ix_regions_code', table_name='regions')
    op.drop_index('ix_regions_parent_id', table_name='regions')
    op.drop_table('regions')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_phone', table_name='users')
    op.drop_table('users')

    # ==================== 1. 删除枚举类型 ====================
    op.execute("DROP TYPE IF EXISTS user_role")
    op.execute("DROP TYPE IF EXISTS user_status")
    op.execute("DROP TYPE IF EXISTS region_level")
    op.execute("DROP TYPE IF EXISTS store_type")
    op.execute("DROP TYPE IF EXISTS store_status")
    op.execute("DROP TYPE IF EXISTS store_platform_name")
    op.execute("DROP TYPE IF EXISTS review_sentiment")
    op.execute("DROP TYPE IF EXISTS review_risk_level")
    op.execute("DROP TYPE IF EXISTS review_status")
    op.execute("DROP TYPE IF EXISTS reply_audit_status")
    op.execute("DROP TYPE IF EXISTS audit_risk_level")
    op.execute("DROP TYPE IF EXISTS ai_provider")
    op.execute("DROP TYPE IF EXISTS prompt_template_type")
    op.execute("DROP TYPE IF EXISTS ai_processing_status")
    op.execute("DROP TYPE IF EXISTS notification_channel_type")
    op.execute("DROP TYPE IF EXISTS notification_event_type")
    op.execute("DROP TYPE IF EXISTS notification_frequency")
    op.execute("DROP TYPE IF EXISTS notification_history_status")
    op.execute("DROP TYPE IF EXISTS notification_template_event_type")
    op.execute("DROP TYPE IF EXISTS subscription_status")
    op.execute("DROP TYPE IF EXISTS spider_platform_status")
    op.execute("DROP TYPE IF EXISTS spider_platform_name")
    op.execute("DROP TYPE IF EXISTS spider_sync_status")
    op.execute("DROP TYPE IF EXISTS spider_task_type")
    op.execute("DROP TYPE IF EXISTS spider_task_status")
    op.execute("DROP TYPE IF EXISTS competitor_analysis_status")
    op.execute("DROP TYPE IF EXISTS competitor_payment_status")
    op.execute("DROP TYPE IF EXISTS competitor_platform")
    op.execute("DROP TYPE IF EXISTS reply_template_type")
    op.execute("DROP TYPE IF EXISTS auto_reply_mode")

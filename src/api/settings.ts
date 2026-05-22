import { api } from '@/lib/api';

// 类型定义
export interface ReplyTemplate {
  id: string;
  name: string;
  type: 'good' | 'bad' | 'neutral';
  content: string;
  variables?: string[];
  is_active: boolean;
  created_at: string;
}

export interface AutoReplyConfig {
  id: string;
  mode: 'smart' | 'semi_auto' | 'manual';
  auto_reply_enabled: boolean;
  work_hours_only: boolean;
  work_start_time?: string;
  work_end_time?: string;
  keyword_reply_enabled: boolean;
  keywords?: Record<string, string>;
  ai_suggest_enabled: boolean;
}

export interface UserNotificationSetting {
  id: string;
  new_review_enabled: boolean;
  negative_alert_enabled: boolean;
  weekly_report_enabled: boolean;
  email_enabled: boolean;
  sms_enabled: boolean;
  push_enabled: boolean;
  quiet_hours_start?: string;
  quiet_hours_end?: string;
}

export interface NotificationChannel {
  id: string;
  name: string;
  type: 'wechat' | 'dingtalk' | 'feishu' | 'email' | 'sms' | 'push';
  webhook_url?: string;
  config?: any;
  is_active: boolean;
  created_at: string;
}

export interface NotificationRule {
  id: string;
  name: string;
  channel_id: string;
  channel_name?: string;
  event_type: 'new_review' | 'negative_alert' | 'weekly_report' | 'spider_status';
  condition?: any;
  frequency: 'realtime' | 'daily' | 'weekly';
  is_active: boolean;
}

// API 函数
export const settingsApi = {
  // 回复模板
  getReplyTemplates: async (): Promise<ReplyTemplate[]> => {
    const response = await api.get<any>('/v1/settings/reply-templates');
    return response.data || response;
  },

  createReplyTemplate: async (data: Partial<ReplyTemplate>): Promise<ReplyTemplate> => {
    const response = await api.post<any, any>('/v1/settings/reply-templates', data);
    return response.data || response;
  },

  updateReplyTemplate: async (id: string, data: Partial<ReplyTemplate>): Promise<ReplyTemplate> => {
    const response = await api.put<any, any>(`/v1/settings/reply-templates/${id}`, data);
    return response.data || response;
  },

  deleteReplyTemplate: async (id: string): Promise<void> => {
    const response = await api.delete(`/v1/settings/reply-templates/${id}`);
    return response.data;
  },

  // 自动回复配置
  getAutoReplyConfig: async (): Promise<AutoReplyConfig> => {
    const response = await api.get<any>('/v1/settings/auto-reply');
    return response.data || response;
  },

  updateAutoReplyConfig: async (data: Partial<AutoReplyConfig>): Promise<AutoReplyConfig> => {
    const response = await api.put<any, any>('/v1/settings/auto-reply', data);
    return response.data || response;
  },

  // 用户通知设置
  getNotificationSetting: async (): Promise<UserNotificationSetting> => {
    const response = await api.get<any>('/v1/settings/notification');
    return response.data || response;
  },

  updateNotificationSetting: async (data: Partial<UserNotificationSetting>): Promise<UserNotificationSetting> => {
    const response = await api.put<any, any>('/v1/settings/notification', data);
    return response.data || response;
  },

  // 通知渠道
  getNotificationChannels: async (): Promise<NotificationChannel[]> => {
    const response = await api.get<any>('/v1/notifications/channels');
    return response.data || response;
  },

  createNotificationChannel: async (data: Partial<NotificationChannel>): Promise<NotificationChannel> => {
    const response = await api.post<any, any>('/v1/notifications/channels', data);
    return response.data || response;
  },

  updateNotificationChannel: async (id: string, data: Partial<NotificationChannel>): Promise<NotificationChannel> => {
    const response = await api.put<any, any>(`/v1/notifications/channels/${id}`, data);
    return response.data || response;
  },

  deleteNotificationChannel: async (id: string): Promise<void> => {
    const response = await api.delete(`/v1/notifications/channels/${id}`);
    return response.data;
  },

  testNotificationChannel: async (id: string): Promise<void> => {
    const response = await api.post(`/v1/notifications/channels/${id}/test`);
    return response.data;
  },

  // 通知规则
  getNotificationRules: async (): Promise<NotificationRule[]> => {
    const response = await api.get<any>('/v1/notifications/rules');
    return response.data || response;
  },

  createNotificationRule: async (data: Partial<NotificationRule>): Promise<NotificationRule> => {
    const response = await api.post<any, any>('/v1/notifications/rules', data);
    return response.data || response;
  },

  updateNotificationRule: async (id: string, data: Partial<NotificationRule>): Promise<NotificationRule> => {
    const response = await api.put<any, any>(`/v1/notifications/rules/${id}`, data);
    return response.data || response;
  },

  deleteNotificationRule: async (id: string): Promise<void> => {
    const response = await api.delete(`/v1/notifications/rules/${id}`);
    return response.data;
  },
};

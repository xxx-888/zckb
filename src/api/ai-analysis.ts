import { api } from '@/lib/api';

// 类型定义
export interface Topic {
  label: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  count: number;
  trend: 'up' | 'down' | 'stable';
}

export interface TagCluster {
  category: string;
  items: string[];
  percentage: number;
  color: string;
}

export interface SentimentSummary {
  score: number;
  trend: string;
  positive: number;
  negative: number;
  aiAccuracy?: number;
  ai_accuracy?: number;
}

export interface RiskLevels {
  high: { count: number; desc: string };
  medium: { count: number; desc: string };
  low: { count: number; desc: string };
}

export interface ReplyRecord {
  id: string;
  user: string;
  rating: number;
  time: string;
  content: string;
  reply: string;
  status: string;
}

export interface ReplyStats {
  todayCount: number;
  autoBlocked: number;
  avgTime: string;
  total?: number;
  ai_generated?: number;
  manual?: number;
  success_rate?: number;
}

export interface AppealSuggestion {
  id?: string;
  review_id: string;
  user?: string;
  platform?: string;
  date?: string;
  content: string;
  draft?: string;
  is_malicious?: boolean;
  confidence?: number;
  suggestion?: string;
  appeal_content?: string;
}

// ========== API 调用 ==========

export const fetchTopics = async (period?: string): Promise<Topic[]> => {
  const url = period ? `/v1/ai-analysis/topics?period=${period}` : '/v1/ai-analysis/topics';
  const response = await api.get<any>(url);
  return response.data || [];
};

export const fetchTagClustering = async (period?: string): Promise<TagCluster[]> => {
  const url = period ? `/v1/ai-analysis/tag-clustering?period=${period}` : '/v1/ai-analysis/tag-clustering';
  const response = await api.get<any>(url);
  return response.data || [];
};

export const fetchSentimentSummary = async (): Promise<SentimentSummary> => {
  const response = await api.get<any>('/v1/ai-analysis/sentiment-summary');
  const data = response.data || response;
  return {
    score: data.score ?? 0,
    trend: data.trend ?? '-',
    positive: data.positive ?? 0,
    negative: data.negative ?? 0,
    aiAccuracy: data.aiAccuracy ?? data.ai_accuracy ?? 0,
  };
};

export const fetchRiskLevels = async (): Promise<RiskLevels> => {
  const response = await api.get<any>('/v1/ai-analysis/risk-levels');
  const data = response.data || response;
  return {
    high: { count: data.high_count ?? 0, desc: data.high_desc ?? '需立即处理' },
    medium: { count: data.medium_count ?? 0, desc: data.medium_desc ?? '建议24小时内回复' },
    low: { count: data.low_count ?? 0, desc: data.low_desc ?? '常规回复即可' },
  };
};

export const fetchReplyHistory = async (page = 1, pageSize = 20): Promise<ReplyRecord[]> => {
  const response = await api.get<any>(`/v1/ai-analysis/reply-history?page=${page}&page_size=${pageSize}`);
  const items = response.items || response.data || [];
  return items.map((item: any) => ({
    id: item.id || item.review_id || '',
    user: item.user_name || item.user || '',
    rating: item.rating || 0,
    time: item.created_at || item.time || '',
    content: item.content || '',
    reply: item.reply || item.ai_reply_content || '',
    status: item.status === 'completed' || item.status === 'sent' ? '自动已发' : item.status === 'approved' ? '已审核' : '待发送',
  }));
};

export const fetchReplyStats = async (): Promise<ReplyStats> => {
  const response = await api.get<any>('/v1/ai-analysis/reply-stats');
  const data = response.data || response;
  return {
    todayCount: data.total ?? 0,
    autoBlocked: data.ai_generated ?? 0,
    avgTime: '-',
    total: data.total ?? 0,
    ai_generated: data.ai_generated ?? 0,
    manual: data.manual ?? 0,
    success_rate: data.success_rate ?? 0,
  };
};

export const fetchAppealSuggestions = async (): Promise<AppealSuggestion[]> => {
  const response = await api.get<any>('/v1/ai-analysis/appeal-suggestions');
  const data = response.data || [];
  return Array.isArray(data) ? data : [];
};

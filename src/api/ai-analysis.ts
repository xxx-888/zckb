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

export const aiAnalysisApi = {
  getTopics: async (period?: string): Promise<Topic[]> => {
    const url = period ? `/ai-analysis/topics?period=${period}` : '/ai-analysis/topics';
    const response = await api.get<any>(url);
    return response.data || response;
  },

  getTagClustering: async (period?: string): Promise<TagCluster[]> => {
    const url = period ? `/ai-analysis/tag-clustering?period=${period}` : '/ai-analysis/tag-clustering';
    const response = await api.get<any>(url);
    return response.data || response;
  },

  getSentimentSummary: async (): Promise<SentimentSummary> => {
    const response = await api.get<any>('/ai-analysis/sentiment-summary');
    const data = response.data || response;
    return {
      score: data.score,
      trend: data.trend,
      positive: data.positive,
      negative: data.negative,
      aiAccuracy: data.aiAccuracy ?? data.ai_accuracy ?? 92.5,
    };
  },

  getRiskLevels: async (): Promise<RiskLevels> => {
    const response = await api.get<any>('/ai-analysis/risk-levels');
    const data = response.data || response;
    // 后端返回扁平结构，转换为前端期望的嵌套结构
    return {
      high: { count: data.high_count ?? 0, desc: data.high_desc ?? '' },
      medium: { count: data.medium_count ?? 0, desc: data.medium_desc ?? '' },
      low: { count: data.low_count ?? 0, desc: data.low_desc ?? '' },
    };
  },

  getReplyHistory: async (page: number = 1, pageSize: number = 20): Promise<any> => {
    const response = await api.get<any>(`/ai-analysis/reply-history?page=${page}&page_size=${pageSize}`);
    return response.data || response;
  },

  getReplyStats: async (): Promise<ReplyStats> => {
    const response = await api.get<any>('/ai-analysis/reply-stats');
    return response.data || response;
  },

  getAppealSuggestion: async (reviewId: string): Promise<AppealSuggestion> => {
    const response = await api.get<any>(`/ai-analysis/appeal-suggestion/${reviewId}`);
    return response.data || response;
  },
};

// 兼容旧函数名的别名
// ============ 测试数据生成函数 ============
const mockTopics: Topic[] = [
  { label: '服务态度', sentiment: 'positive', count: 156, trend: 'up' },
  { label: '菜品口味', sentiment: 'positive', count: 142, trend: 'stable' },
  { label: '环境卫生', sentiment: 'neutral', count: 89, trend: 'down' },
  { label: '上菜速度', sentiment: 'negative', count: 45, trend: 'up' },
  { label: '性价比', sentiment: 'positive', count: 123, trend: 'up' },
  { label: '停车便利', sentiment: 'negative', count: 34, trend: 'stable' },
];

const mockTagClustering: TagCluster[] = [
  { category: '服务质量', items: ['服务态度差', '响应慢', '不理人'], percentage: 35.5, color: '#FF6B6B' },
  { category: '菜品问题', items: ['口味不佳', '食材不新鲜', '分量少'], percentage: 28.3, color: '#FFA94D' },
  { category: '环境卫生', items: ['桌面不干净', '地面湿滑', '有异味'], percentage: 18.7, color: '#FFD43B' },
  { category: '等待时间', items: ['上菜慢', '排队久', '出餐慢'], percentage: 17.5, color: '#69DB7C' },
];

const mockReplyHistory: ReplyRecord[] = Array.from({ length: 5 }, (_, i) => ({
  id: `mock-review-${i + 1}`,
  user: `用户${i + 1}`,
  rating: Math.floor(Math.random() * 2) + 1,
  time: new Date(Date.now() - i * 3600000).toISOString(),
  content: ['菜品口味一般，服务态度有待提升。', '上菜太慢了，等了半小时'][i % 2],
  reply: ['非常抱歉给您带来不好的体验，我们会认真改进。', '感谢您的反馈，已安排专人跟进处理。'][i % 2],
  status: ['自动已发', '待发送'][i % 2] as '自动已发' | '待发送',
}));

const mockAppealSuggestions: AppealSuggestion[] = [
  {
    review_id: 'mock-review-1',
    content: '这家店太差了，再也不会来了！',
    is_malicious: true,
    confidence: 0.87,
    suggestion: '该评论疑似恶意差评，建议提交申诉',
    appeal_content: '尊敬的平台审核人员：我们发现该用户的评价存在以下异常：1. 评价内容与实际情况不符；2. 疑似竞争对手恶意抹黑。恳请平台核实处理。',
  },
];

// ============ 导出 fetch 函数（接口无数据时自动插入测试数据）============
export const fetchTopics = async (period?: string): Promise<Topic[]> => {
  const data = await aiAnalysisApi.getTopics(period);
  return (data && data.length > 0) ? data : mockTopics;
};

export const fetchTagClustering = async (period?: string): Promise<TagCluster[]> => {
  const data = await aiAnalysisApi.getTagClustering(period);
  return (data && data.length > 0) ? data : mockTagClustering;
};

export const fetchSentimentSummary = async (): Promise<SentimentSummary> => {
  const data = await aiAnalysisApi.getSentimentSummary();
  return data ?? {
    score: 84.5,
    trend: 'up',
    positive: 84,
    negative: 16,
    aiAccuracy: 92.5,
  };
};

export const fetchRiskLevels = async (): Promise<RiskLevels> => {
  const data = await aiAnalysisApi.getRiskLevels();
  return data ?? {
    high: { count: 12, desc: '需立即处理，可能影响门店评分' },
    medium: { count: 28, desc: '建议24小时内回复处理' },
    low: { count: 156, desc: '常规回复即可' },
  };
};

export const fetchReplyHistory = async (page = 1, pageSize = 20): Promise<ReplyRecord[]> => {
  const response = await aiAnalysisApi.getReplyHistory(page, pageSize);
  const items = response.items || response || [];
  if (items.length > 0) {
    return items.map((item: any) => ({
      id: item.id || item.review_id,
      user: item.user_name || item.user,
      rating: item.rating,
      time: item.created_at || item.time,
      content: item.content,
      reply: item.reply || item.ai_reply_draft || '',
      status: item.status === 'completed' ? '自动已发' : '待发送',
    }));
  }
  return mockReplyHistory;
};

export const fetchReplyStats = async (): Promise<ReplyStats> => {
  const response = await aiAnalysisApi.getReplyStats();
  const hasData = response && (response.total > 0 || response.success_rate > 0);
  if (hasData) {
    return {
      todayCount: response.total || 0,
      autoBlocked: Math.floor((response.ai_generated || 0) * 0.1),
      avgTime: '3分钟',
      total: response.total || 0,
      ai_generated: response.ai_generated || 0,
      manual: response.manual || 0,
      success_rate: response.success_rate || 0,
    };
  }
  const todayCount = Math.floor(Math.random() * 20) + 5;
  return {
    todayCount,
    autoBlocked: Math.floor(todayCount * 0.3),
    avgTime: '3分钟',
    total: 156,
    ai_generated: 133,
    manual: 23,
    success_rate: 94.2,
  };
};

export const fetchAppealSuggestions = async (reviewId?: string): Promise<AppealSuggestion[]> => {
  if (reviewId) {
    const response = await api.get<any>(`/ai-analysis/appeal-suggestion/${reviewId}`);
    const items = response.data || response;
    return Array.isArray(items) ? items : [items];
  }
  // 无 reviewId 时返回测试数据，使申诉 tab 可展示
  return mockAppealSuggestions;
};

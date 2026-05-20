import { api } from '@/lib/api';

// 类型定义
export interface CoreStats {
  total_reviews: number;
  review_trend: string;
  avg_rating: number;
  rating_trend: string;
  positive_rate: string;
  positive_trend: string;
  ai_reply_rate: string;
  reply_trend: string;
}

export interface PlatformData {
  platform: string;
  count: number;
  percentage: number;
  color: string;
  icon: string;
}

export interface Review {
  id: string;
  store_name: string;
  user_name: string;
  content: string;
  rating: number;
  sentiment: 'positive' | 'negative' | 'neutral';
  platform: string;
  time: string;
  avatar?: string;
  tags?: string[];
  hasImage?: boolean;
  store_id?: string;
  platform_review_id?: string;
}

export interface StoreRanking {
  name: string;
  score: number;
  reviews: number;
  trend: 'up' | 'down' | 'stable';
  health: number;
}

export interface HealthStatus {
  platform: string;
  status: 'normal' | 'warning';
  time: string;
}

export interface AlertData {
  id: string;
  title: string;
  description: string;
  severity: 'high' | 'medium' | 'low';
}

// API 函数
export const dashboardApi = {
  // 获取核心统计
  getCoreStats: async (period: string = '7d'): Promise<CoreStats> => {
    const response = await api.get<any>(`/dashboard/core-stats?period=${period}`);
    return response.data || response;
  },

  // 获取平台分布
  getPlatformDistribution: async (): Promise<PlatformData[]> => {
    const response = await api.get<any>('/dashboard/platform-distribution');
    return response.data || response;
  },

  // 获取最新评论
  getRecentReviews: async (limit: number = 10): Promise<Review[]> => {
    const response = await api.get<any>(`/dashboard/recent-reviews?limit=${limit}`);
    return response.data || response;
  },

  // 获取门店排行
  getStoreRankings: async (limit: number = 10): Promise<StoreRanking[]> => {
    const response = await api.get<any>(`/dashboard/store-rankings?limit=${limit}`);
    return response.data || response;
  },

  // 获取数据源健康状态
  getHealthStatus: async (): Promise<HealthStatus[]> => {
    const response = await api.get<any>('/dashboard/health-status');
    return response.data || response;
  },

  // 获取警告信息
  getAlerts: async (): Promise<AlertData[]> => {
    const response = await api.get<any>('/dashboard/alert');
    return response.data || response;
  },

  // 获取门店健康值
  getStoreHealth: async (): Promise<any[]> => {
    const response = await api.get<any>('/dashboard/store-health');
    return response.data || response;
  },
};

// 兼容旧函数名的别名
export const fetchCoreStats = dashboardApi.getCoreStats;
export const fetchPlatformData = dashboardApi.getPlatformDistribution;
export const fetchRecentReviews = dashboardApi.getRecentReviews;
export const fetchStoreRankings = dashboardApi.getStoreRankings;
export const fetchHealthStatus = dashboardApi.getHealthStatus;
export const fetchAlert = dashboardApi.getAlerts;
export const fetchStoreHealth = dashboardApi.getStoreHealth;

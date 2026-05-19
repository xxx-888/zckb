/**
 * 首页数据 API 接口
 * 
 * 所有函数通过 HTTP 请求获取数据
 * 本地开发时由 json-server 提供 Mock 数据（npm run mock）
 * 生产环境对接真实后端 API
 */

// ==================== 类型定义 ====================

export interface CoreStats {
  totalReviews: number;
  reviewTrend: string;
  avgRating: number;
  ratingTrend: string;
  positiveRate: string;
  positiveTrend: string;
  aiReplyRate: string;
  replyTrend: string;
}

export interface PlatformData {
  platform: string;
  count: number;
  percentage: number;
  color: string;
  icon: string;
}

export interface Review {
  id: number;
  user: string;
  content: string;
  rating: number;
  platform: string;
  time: string;
  sentiment: 'positive' | 'negative' | 'neutral';
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
  type: 'anomaly' | 'negative_spike' | 'competitor';
  title: string;
  description: string;
  severity: 'critical' | 'warning' | 'info';
  timestamp: string;
}

export interface DashboardData {
  coreStats: CoreStats;
  platformData: PlatformData[];
  recentReviews: Review[];
  storeRankings: StoreRanking[];
  healthStats: HealthStatus[];
  alert: AlertData | null;
}

// ==================== HTTP 请求封装 ====================

const BASE_URL = '/api';

async function fetchAPI<T>(endpoint: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${endpoint}`);
  if (!res.ok) throw new Error(`API 请求失败: ${res.status} ${res.statusText}`);
  return res.json();
}

// ==================== API 函数 ====================

/**
 * 获取核心统计数据
 * GET /api/v1/dashboard/core-stats?period=:period
 */
export async function fetchCoreStats(
  timePeriod: 'today' | 'yesterday' | '7days' | '30days' | 'custom'
): Promise<CoreStats> {
  const data = await fetchAPI<any>(`/dashboard_overview/${timePeriod}`);
  return {
    totalReviews: data.totalReviews,
    reviewTrend: data.reviewTrend,
    avgRating: data.avgRating,
    ratingTrend: data.ratingTrend,
    positiveRate: data.positiveRate,
    positiveTrend: data.positiveTrend,
    aiReplyRate: data.aiReplyRate,
    replyTrend: data.replyTrend,
  };
}

/**
 * 获取平台分布数据
 * GET /api/v1/dashboard/platform-distribution
 */
export async function fetchPlatformData(): Promise<PlatformData[]> {
  const data = await fetchAPI<any>(`/dashboard_overview/7days`);
  return data.platformData || [];
}

/**
 * 获取最新评论动态
 * GET /api/v1/dashboard/recent-reviews?limit=:limit
 */
export async function fetchRecentReviews(limit: number = 5): Promise<Review[]> {
  const data = await fetchAPI<any>(`/dashboard_overview/7days`);
  const reviews = data.recentReviews || [];
  return reviews.slice(0, limit);
}

/**
 * 获取门店排行榜（HQ/运营商视图）
 * GET /api/v1/dashboard/store-rankings?limit=:limit
 */
export async function fetchStoreRankings(limit: number = 5): Promise<StoreRanking[]> {
  const data = await fetchAPI<any>(`/dashboard_overview/7days`);
  const rankings = data.storeRankings || [];
  return rankings.slice(0, limit);
}

/**
 * 获取数据源健康状态
 * GET /api/v1/dashboard/health-status
 */
export async function fetchHealthStatus(): Promise<HealthStatus[]> {
  const data = await fetchAPI<any>(`/dashboard_overview/7days`);
  return data.healthStats || [];
}

/**
 * 获取异常警告
 * GET /api/v1/dashboard/alert
 */
export async function fetchAlert(): Promise<AlertData | null> {
  const data = await fetchAPI<any>(`/dashboard_overview/7days`);
  return data.alert || null;
}

/**
 * 获取商户视图的口碑健康值
 * GET /api/v1/dashboard/store-health
 */
export async function fetchStoreHealth(): Promise<{
  healthScore: number;
  rankPercentile: number;
  suggestion: string;
}> {
  return fetchAPI<any>(`/store_health`);
}

/**
 * 获取所有首页数据（批量接口）
 * GET /api/v1/dashboard/overview?period=:period
 */
export async function fetchDashboardData(
  timePeriod: 'today' | 'yesterday' | '7days' | '30days' | 'custom'
): Promise<DashboardData> {
  const data = await fetchAPI<any>(`/dashboard_overview/${timePeriod}`);
  return {
    coreStats: {
      totalReviews: data.totalReviews,
      reviewTrend: data.reviewTrend,
      avgRating: data.avgRating,
      ratingTrend: data.ratingTrend,
      positiveRate: data.positiveRate,
      positiveTrend: data.positiveTrend,
      aiReplyRate: data.aiReplyRate,
      replyTrend: data.replyTrend,
    },
    platformData: data.platformData || [],
    recentReviews: data.recentReviews || [],
    storeRankings: data.storeRankings || [],
    healthStats: data.healthStats || [],
    alert: data.alert || null,
  };
}

// ==================== React Hook ====================

import { useState, useEffect } from 'react';

/**
 * 使用首页数据的 Hook
 * 
 * @example
 * const { data, loading, error, refetch } = useDashboardData('7days');
 */
export function useDashboardData(timePeriod: 'today' | 'yesterday' | '7days' | '30days' | 'custom') {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await fetchDashboardData(timePeriod);
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [timePeriod]);

  return { data, loading, error, refetch: fetchData };
}

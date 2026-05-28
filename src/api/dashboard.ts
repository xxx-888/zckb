import { api } from '@/lib/api';

// ==================== 类型定义 ====================
export interface CoreStats {
  total_reviews: number;
  review_trend: number;
  avg_rating: number;
  rating_trend: number;
  positive_rate: number;
  positive_trend: number;
  ai_reply_rate: number;
  reply_trend: number;
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
  health_score?: number;
}

export interface HealthStatus {
  platform: string;
  status: 'normal' | 'warning' | 'error';
  time: string | null;
}

export interface AlertData {
  id: string;
  title: string;
  description: string;
  severity: 'high' | 'medium' | 'low';
}

// ==================== 工具函数 ====================

/** 将前端 timePeriod 映射为后端期望的 period 格式 */
function mapPeriod(timePeriod: string): string {
  const mapping: Record<string, string> = {
    'today': '1d',
    'yesterday': '1d',
    '7days': '7d',
    '30days': '30d',
    '90days': '90d',
    'custom': '7d',
  };
  return mapping[timePeriod] || '7d';
}

/**
 * 构建查询参数字符串（自动处理 ? 和 & 的连接）
 */
function buildPeriodParam(period?: string): string {
  if (!period) return '';
  return `?period=${mapPeriod(period)}`;
}

/** 通用 API 调用封装 */
async function fetchAPI<T>(url: string): Promise<T> {
  const response = await api.get<any>(url);
  if (response.code !== undefined && response.data !== undefined) {
    if (response.code === 0 || response.code === 200) {
      return response.data as T;
    }
    throw new Error(response.message || `API ${url} 执行失败`);
  }
  return response as T;
}

// ==================== API 函数 ====================

/** 获取核心统计 */
export async function fetchCoreStats(timePeriod: string): Promise<CoreStats> {
  const period = mapPeriod(timePeriod);
  return fetchAPI<CoreStats>(`/v1/dashboard/core-stats?period=${period}`);
}

/** 获取平台分布 */
export async function fetchPlatformData(timePeriod?: string): Promise<PlatformData[]> {
  const q = timePeriod ? `?period=${mapPeriod(timePeriod)}` : '';
  return fetchAPI<PlatformData[]>(`/v1/dashboard/platform-distribution${q}`);
}

/** 获取最新评论列表 */
export async function fetchRecentReviews(limit: number = 10, timePeriod?: string): Promise<Review[]> {
  let q = `?limit=${limit}`;
  if (timePeriod) q += `&period=${mapPeriod(timePeriod)}`;
  return fetchAPI<Review[]>(`/v1/dashboard/recent-reviews${q}`);
}

/** 获取门店排行榜（HQ/OPERATOR 视图） */
export async function fetchStoreRankings(limit: number = 10, timePeriod?: string): Promise<StoreRanking[]> {
  let q = `?limit=${limit}`;
  if (timePeriod) q += `&period=${mapPeriod(timePeriod)}`;
  return fetchAPI<StoreRanking[]>(`/v1/dashboard/store-rankings${q}`);
}

/** 获取数据源健康状态 */
export async function fetchHealthStatus(timePeriod?: string): Promise<HealthStatus[]> {
  const q = timePeriod ? `?period=${mapPeriod(timePeriod)}` : '';
  return fetchAPI<HealthStatus[]>(`/v1/dashboard/health-status${q}`);
}

/** 获取异常警告 */
export async function fetchAlert(timePeriod?: string): Promise<AlertData | null> {
  const q = timePeriod ? `?period=${mapPeriod(timePeriod)}` : '';
  const alerts = await fetchAPI<AlertData[]>(`/v1/dashboard/alert${q}`);
  if (alerts && alerts.length > 0) {
    const priority: Record<string, number> = { high: 3, medium: 2, low: 1 };
    alerts.sort((a, b) => (priority[a.severity] || 0) - (priority[b.severity] || 0));
    return alerts[alerts.length - 1];
  }
  return null;
}

/** 获取当前用户所辖门店的健康值列表（商户视图用） */
export async function fetchStoreHealth(timePeriod?: string): Promise<any[]> {
  const q = timePeriod ? `?period=${mapPeriod(timePeriod)}` : '';
  return fetchAPI<any[]>(`/v1/dashboard/store-health${q}`);
}

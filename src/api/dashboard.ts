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

/**
 * 将前端 timePeriod 映射为后端期望的 period 格式
 * 前端: 'today' | 'yesterday' | '7days' | '30days' | '90days' | 'custom'
 * 后端: '1d' | '7d' | '30d' | '90d'
 */
function mapPeriod(timePeriod: string): string {
  const mapping: Record<string, string> = {
    'today': '1d',
    'yesterday': '1d',   // 后端统一按1天处理，service层会区分今天/昨天
    '7days': '7d',
    '30days': '30d',
    '90days': '90d',
    'custom': '7d',       // 自定义暂不支持，降级为7天
  };
  return mapping[timePeriod] || '7d';
}

/**
 * 通用 API 调用封装
 * 注意：api.ts 的响应拦截器已经返回了 response.data，所以这里直接使用 response
 */
async function fetchAPI<T>(url: string): Promise<T> {
  const response = await api.get<any>(url);
  // 如果后端返回的格式是 { code: 0, data: {...} }，需要解包
  // 如果后端返回的格式是 { items: [...], total: ... }，直接使用
  if (response.code !== undefined && response.data !== undefined) {
    // 后端返回了 { code, data, message } 格式
    if (response.code === 0 || response.code === 200) {
      return response.data as T;
    }
    throw new Error(response.message || `API ${url} 执行失败`);
  }
  // 后端直接返回了数据（比如 { items: [...], total: ... }）
  return response as T;
}

// ==================== API 函数 ====================

/** 获取核心统计（评论总数、平均评分、好评率、AI回复率及趋势） */
export async function fetchCoreStats(timePeriod: string): Promise<CoreStats> {
  const period = mapPeriod(timePeriod);
  return fetchAPI<CoreStats>(`/v1/dashboard/core-stats?period=${period}`);
}

/** 获取平台分布（各平台评论数量及占比） */
export async function fetchPlatformData(): Promise<PlatformData[]> {
  return fetchAPI<PlatformData[]>(`/v1/dashboard/platform-distribution`);
}

/** 获取最新评论列表 */
export async function fetchRecentReviews(limit: number = 10): Promise<Review[]> {
  return fetchAPI<Review[]>(`/v1/dashboard/recent-reviews?limit=${limit}`);
}

/** 获取门店排行榜（HQ/OPERATOR 视图） */
export async function fetchStoreRankings(limit: number = 10): Promise<StoreRanking[]> {
  return fetchAPI<StoreRanking[]>(`/v1/dashboard/store-rankings?limit=${limit}`);
}

/** 获取数据源健康状态（各平台最后同步时间） */
export async function fetchHealthStatus(): Promise<HealthStatus[]> {
  return fetchAPI<HealthStatus[]>(`/v1/dashboard/health-status`);
}

/**
 * 获取异常警告（差评预警、未回复提醒、AI回复待审核、评分下降）
 * 返回单条最紧急的警告（Dashboard 只展示一条）
 */
export async function fetchAlert(): Promise<AlertData | null> {
  const alerts = await fetchAPI<AlertData[]>(`/v1/dashboard/alert`);
  if (alerts && alerts.length > 0) {
    // 按严重程度排序，返回最紧急的一条
    const priority: Record<string, number> = { high: 3, medium: 2, low: 1 };
    alerts.sort((a, b) => (priority[a.severity] || 0) - (priority[b.severity] || 0));
    return alerts[alerts.length - 1];
  }
  return null;
}

/** 获取当前用户所辖门店的健康值列表（商户视图用） */
export async function fetchStoreHealth(): Promise<any[]> {
  return fetchAPI<any[]>(`/v1/dashboard/store-health`);
}

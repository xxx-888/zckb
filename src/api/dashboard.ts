import { api } from '@/lib/api';

// ==================== 测试数据 ====================
const MOCK_CORE_STATS: CoreStats = {
  total_reviews: 1284,
  review_trend: '+12.5%',
  avg_rating: 4.2,
  rating_trend: '+0.3',
  positive_rate: '78.5%',
  positive_trend: '+5.2%',
  ai_reply_rate: '65.0%',
  reply_trend: '+15.0%',
};

const MOCK_PLATFORM_DATA: PlatformData[] = [
  { platform: '美团', count: 586, percentage: 45.6, color: 'bg-yellow-400', icon: 'simple-icons:meituan' },
  { platform: '大众点评', count: 385, percentage: 30.0, color: 'bg-red-500', icon: 'simple-icons:dianping' },
  { platform: '抖音', count: 218, percentage: 17.0, color: 'bg-slate-900', icon: 'simple-icons:tiktok' },
  { platform: '小红书', count: 95, percentage: 7.4, color: 'bg-red-500', icon: 'simple-icons:xiaohongshu' },
];

const MOCK_RECENT_REVIEWS: Review[] = [
  {
    id: '1',
    store_name: '旗舰店',
    user_name: '张三',
    content: '服务态度很好，菜品口味正宗，下次还会再来！环境也很舒适，推荐给大家。',
    rating: 5,
    sentiment: 'positive',
    platform: '美团',
    time: '5分钟前',
    avatar: '',
    tags: ['服务好', '口味正', '环境好'],
    hasImage: true,
    store_id: 'store_001',
    platform_review_id: 'mt_001',
  },
  {
    id: '2',
    store_name: '旗舰店',
    user_name: '李四',
    content: '菜品分量很足，味道也不错，就是上菜有点慢，希望改进。',
    rating: 4,
    sentiment: 'positive',
    platform: '大众点评',
    time: '32分钟前',
    avatar: '',
    tags: ['分量足', '味道好'],
    hasImage: false,
    store_id: 'store_001',
    platform_review_id: 'dianping_001',
  },
  {
    id: '3',
    store_name: '分店',
    user_name: '王五',
    content: '等了半小时才上菜，服务员态度也不好，体验很差，不会再来。',
    rating: 2,
    sentiment: 'negative',
    platform: '抖音',
    time: '1小时前',
    avatar: '',
    tags: ['上菜慢', '态度差'],
    hasImage: false,
    store_id: 'store_002',
    platform_review_id: 'dy_001',
  },
  {
    id: '4',
    store_name: '旗舰店',
    user_name: '赵六',
    content: '环境不错，适合聚餐，推荐招牌菜。',
    rating: 4,
    sentiment: 'positive',
    platform: '小红书',
    time: '2小时前',
    avatar: '',
    tags: ['环境好', '适合聚餐'],
    hasImage: true,
    store_id: 'store_001',
    platform_review_id: 'xhs_001',
  },
  {
    id: '5',
    store_name: '分店',
    user_name: '孙七',
    content: '菜品一般，价格偏贵，性价比不高。',
    rating: 3,
    sentiment: 'neutral',
    platform: '美团',
    time: '3小时前',
    avatar: '',
    tags: ['性价比低'],
    hasImage: false,
    store_id: 'store_002',
    platform_review_id: 'mt_002',
  },
];

const MOCK_STORE_RANKINGS: StoreRanking[] = [
  { name: '旗舰店', score: 4.5, reviews: 586, trend: 'up', health: 92 },
  { name: '分店', score: 4.2, reviews: 423, trend: 'up', health: 85 },
  { name: '东城店', score: 4.0, reviews: 312, trend: 'stable', health: 78 },
  { name: '西城店', score: 3.8, reviews: 198, trend: 'down', health: 65 },
  { name: '南城店', score: 3.5, reviews: 156, trend: 'down', health: 58 },
];

const MOCK_HEALTH_STATUS: HealthStatus[] = [
  { platform: '美团', status: 'normal', time: '2分钟前' },
  { platform: '大众点评', status: 'normal', time: '5分钟前' },
  { platform: '抖音', status: 'warning', time: '1小时前' },
  { platform: '小红书', status: 'normal', time: '10分钟前' },
];

const MOCK_ALERT: AlertData = {
  id: 'alert_001',
  title: '差评预警',
  description: '分店出现3条差评，平均评分低于3.0，建议立即处理',
  severity: 'high',
};

const MOCK_STORE_HEALTH = {
  healthScore: 85,
  rankPercentile: 92,
  suggestion: '您的门店口碑健康值优于92%的同行，继续保持优质服务！',
};

// ==================== 类型定义 ====================
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

// ==================== API 函数 ====================
const fetchAPI = async <T,>(url: string, mockData: T): Promise<T> => {
  try {
    const response = await api.get<any>(url);
    if (response.code === 200 && response.data) {
      return response.data;
    }
    console.warn(`[Dashboard API] ${url} 返回格式异常，使用测试数据`);
    return mockData;
  } catch (error) {
    console.warn(`[Dashboard API] ${url} 调用失败，使用测试数据:`, error);
    return mockData;
  }
};

export const dashboardApi = {
  // 获取核心统计
  getCoreStats: async (period: string = '7d', storeId?: string): Promise<CoreStats> => {
    const url = storeId ? `/dashboard/core-stats?period=${period}&store_id=${storeId}` : `/dashboard/core-stats?period=${period}`;
    return fetchAPI<CoreStats>(url, MOCK_CORE_STATS);
  },

  // 获取平台分布
  getPlatformDistribution: async (storeId?: string): Promise<PlatformData[]> => {
    const url = storeId ? `/dashboard/platform-distribution?store_id=${storeId}` : '/dashboard/platform-distribution';
    return fetchAPI<PlatformData[]>(url, MOCK_PLATFORM_DATA);
  },

  // 获取最新评论
  getRecentReviews: async (limit: number = 10, storeId?: string): Promise<Review[]> => {
    const url = storeId ? `/dashboard/recent-reviews?limit=${limit}&store_id=${storeId}` : `/dashboard/recent-reviews?limit=${limit}`;
    return fetchAPI<Review[]>(url, MOCK_RECENT_REVIEWS.slice(0, limit));
  },

  // 获取门店排行
  getStoreRankings: async (limit: number = 10, storeId?: string): Promise<StoreRanking[]> => {
    const url = storeId ? `/dashboard/store-rankings?limit=${limit}&store_id=${storeId}` : `/dashboard/store-rankings?limit=${limit}`;
    return fetchAPI<StoreRanking[]>(url, MOCK_STORE_RANKINGS.slice(0, limit));
  },

  // 获取数据源健康状态
  getHealthStatus: async (storeId?: string): Promise<HealthStatus[]> => {
    const url = storeId ? `/dashboard/health-status?store_id=${storeId}` : '/dashboard/health-status';
    return fetchAPI<HealthStatus[]>(url, MOCK_HEALTH_STATUS);
  },

  // 获取警告信息
  getAlerts: async (storeId?: string): Promise<AlertData[]> => {
    const url = storeId ? `/dashboard/alerts?store_id=${storeId}` : '/dashboard/alerts';
    return fetchAPI<AlertData[]>(url, [MOCK_ALERT]);
  },

  // 获取单个门店健康值（商户视图）
  getStoreHealth: async (storeId?: string): Promise<any> => {
    const url = storeId ? `/dashboard/store-health?store_id=${storeId}` : '/dashboard/store-health';
    return fetchAPI<any>(url, MOCK_STORE_HEALTH);
  },
};

// 兼容旧函数名的别名
export const fetchCoreStats = dashboardApi.getCoreStats;
export const fetchPlatformData = dashboardApi.getPlatformDistribution;
export const fetchRecentReviews = dashboardApi.getRecentReviews;
export const fetchStoreRankings = dashboardApi.getStoreRankings;
export const fetchHealthStatus = dashboardApi.getHealthStatus;
export const fetchAlert = async (): Promise<AlertData | null> => {
  try {
    const alerts = await dashboardApi.getAlerts();
    return alerts && alerts.length > 0 ? alerts[0] : null;
  } catch {
    return MOCK_ALERT;
  }
};
export const fetchStoreHealth = dashboardApi.getStoreHealth;

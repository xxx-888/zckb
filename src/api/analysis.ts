import { api } from '@/lib/api';

// ==================== 营业额分析 ====================

export interface DailyRevenue {
  date: string;
  total_revenue: number;
  meituan_revenue: number;
  douyin_revenue: number;
  other_revenue: number;
  visitor_count: number;
  table_count: number;
  avg_people_per_table: number;
  avg_per_capita: number;
}

export interface RevenueTrendData {
  daily: DailyRevenue[];
  weekly: {
    week_label: string;
    total_revenue: number;
    meituan_revenue: number;
    douyin_revenue: number;
    visitor_count: number;
    table_count: number;
  }[];
}

// ==================== 套餐分析 ====================

export interface PackageRanking {
  product_name: string;
  meituan_buy: number;
  meituan_verify: number;
  douyin_buy: number;
  douyin_verify: number;
  total_verify: number;
  verify_rate: number;
  mom_verify_change?: number; // 环比核销变化
}

export interface PackageAnalysisData {
  top_ranking: PackageRanking[];
  bottom_ranking: PackageRanking[];
  overall_summary: {
    total_buy: number;
    total_verify: number;
    avg_verify_rate: number;
  };
}

// ==================== 门店分析 ====================

export interface StoreFunnel {
  platform: string;
  impressions: number;    // 曝光
  visits: number;          // 访问
  purchases: number;       // 购买
  verifications: number;   // 核销
  impression_to_visit: number;
  visit_to_purchase: number;
}

export interface StoreHealthData {
  funnels: StoreFunnel[];
  rankings: {
    platform: string;
    ranking_name: string;
    current_rank: string;
    prev_rank: string;
    rank_change: string;
  }[];
  reviews_summary: {
    platform: string;
    star_rating: number;
    prev_star_rating: number;
    new_reviews: number;
    bad_reviews: number;
    bad_keywords: string[];
  }[];
  daily_metrics: {
    date: string;
    platform: string;
    impressions: number;
    visits: number;
    purchases: number;
    verifications: number;
    star_rating: number;
    new_reviews: number;
  }[];
}

// ==================== Mock 数据 ====================

const mockDailyRevenue: DailyRevenue[] = Array.from({ length: 7 }, (_, i) => {
  const d = new Date(2026, 4, 25 + i);
  return {
    date: `${d.getMonth() + 1}.${d.getDate()}`,
    total_revenue: 15000 + Math.floor(Math.random() * 8000),
    meituan_revenue: 5000 + Math.floor(Math.random() * 3000),
    douyin_revenue: 8000 + Math.floor(Math.random() * 5000),
    other_revenue: 1000 + Math.floor(Math.random() * 2000),
    visitor_count: 180 + Math.floor(Math.random() * 80),
    table_count: 60 + Math.floor(Math.random() * 30),
    avg_people_per_table: 2.8 + Math.random() * 0.4,
    avg_per_capita: 75 + Math.random() * 20,
  };
});

export const mockRevenueTrend: RevenueTrendData = {
  daily: mockDailyRevenue,
  weekly: [
    { week_label: '5.16-23', total_revenue: 86800, meituan_revenue: 45680, douyin_revenue: 34120, visitor_count: 1210, table_count: 403 },
    { week_label: '5.24-31', total_revenue: 124580, meituan_revenue: 31290, douyin_revenue: 78900, visitor_count: 1458, table_count: 486 },
  ],
};

export const mockPackageAnalysis: PackageAnalysisData = {
  top_ranking: [
    { product_name: '【牛牛爆款】鲜切4人餐', meituan_buy: 57, meituan_verify: 50, douyin_buy: 45, douyin_verify: 50, total_verify: 100, verify_rate: 97.1, mom_verify_change: 65.8 },
    { product_name: '【撸串搭子】当日现串2人餐', meituan_buy: 36, meituan_verify: 31, douyin_buy: 28, douyin_verify: 35, total_verify: 66, verify_rate: 100, mom_verify_change: 82.5 },
    { product_name: '招牌牛肉系列（10串）', meituan_buy: 8, meituan_verify: 7, douyin_buy: 10, douyin_verify: 2, total_verify: 9, verify_rate: 50, mom_verify_change: 100 },
    { product_name: '招牌广式猪杂粥（大份）', meituan_buy: 10, meituan_verify: 7, douyin_buy: 3, douyin_verify: 1, total_verify: 8, verify_rate: 61.5, mom_verify_change: 300 },
    { product_name: '【聚会首选】当日现串6-8人餐', meituan_buy: 13, meituan_verify: 12, douyin_buy: 5, douyin_verify: 8, total_verify: 20, verify_rate: 111, mom_verify_change: 100 },
  ],
  bottom_ranking: [
    { product_name: '50元代金券', meituan_buy: 6, meituan_verify: 6, douyin_buy: 0, douyin_verify: 0, total_verify: 6, verify_rate: 100, mom_verify_change: 100 },
    { product_name: '25元代金券', meituan_buy: 5, meituan_verify: 3, douyin_buy: 0, douyin_verify: 0, total_verify: 3, verify_rate: 60, mom_verify_change: 50 },
    { product_name: '小朋友必点组合', meituan_buy: 4, meituan_verify: 3, douyin_buy: 0, douyin_verify: 1, total_verify: 4, verify_rate: 80, mom_verify_change: 100 },
    { product_name: '生蚝10个+荤串10串', meituan_buy: 6, meituan_verify: 5, douyin_buy: 0, douyin_verify: 5, total_verify: 10, verify_rate: 83.3, mom_verify_change: 100 },
    { product_name: '招牌霸王大串3串', meituan_buy: 0, meituan_verify: 0, douyin_buy: 0, douyin_verify: 0, total_verify: 0, verify_rate: 0, mom_verify_change: 0 },
  ],
  overall_summary: {
    total_buy: 139,
    total_verify: 226,
    avg_verify_rate: 80.8,
  },
};

export const mockStoreHealth: StoreHealthData = {
  funnels: [
    { platform: '美团', impressions: 55363, visits: 5283, purchases: 273, verifications: 220, impression_to_visit: 9.5, visit_to_purchase: 5.2 },
    { platform: '点评', impressions: 55363, visits: 5283, purchases: 273, verifications: 220, impression_to_visit: 9.5, visit_to_purchase: 5.2 },
    { platform: '抖音', impressions: 753, visits: 564, purchases: 105, verifications: 72, impression_to_visit: 74.9, visit_to_purchase: 18.6 },
  ],
  rankings: [
    { platform: '美团', ranking_name: '人气榜', current_rank: '第1名', prev_rank: '第1名', rank_change: '持平' },
    { platform: '点评', ranking_name: '热门榜', current_rank: '第2名', prev_rank: '第2名', rank_change: '持平' },
    { platform: '抖音', ranking_name: '人气榜', current_rank: '第6名', prev_rank: '第6名', rank_change: '持平' },
  ],
  reviews_summary: [
    { platform: '美团', star_rating: 4.8, prev_star_rating: 4.8, new_reviews: 33, bad_reviews: 1, bad_keywords: ['室内抽烟'] },
    { platform: '点评', star_rating: 4.0, prev_star_rating: 4.0, new_reviews: 0, bad_reviews: 0, bad_keywords: [] },
    { platform: '抖音', star_rating: 4.7, prev_star_rating: 4.7, new_reviews: 0, bad_reviews: 0, bad_keywords: [] },
  ],
  daily_metrics: mockDailyRevenue.map(d => ({
    ...d,
    platform: '美团',
    impressions: 7000 + Math.floor(Math.random() * 2000),
    visits: 600 + Math.floor(Math.random() * 200),
    purchases: 35 + Math.floor(Math.random() * 15),
    verifications: 28 + Math.floor(Math.random() * 12),
    star_rating: 4.7 + Math.random() * 0.2,
    new_reviews: Math.floor(Math.random() * 6),
  })),
};

// ==================== API 函数 ====================

export async function fetchRevenueTrend(params?: any): Promise<RevenueTrendData> {
  await new Promise(r => setTimeout(r, 300));
  return mockRevenueTrend;
}

export async function fetchPackageAnalysis(params?: any): Promise<PackageAnalysisData> {
  await new Promise(r => setTimeout(r, 300));
  return mockPackageAnalysis;
}

export async function fetchStoreHealth(params?: any): Promise<StoreHealthData> {
  await new Promise(r => setTimeout(r, 300));
  return mockStoreHealth;
}

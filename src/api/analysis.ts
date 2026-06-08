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
  impressions: number;
  visits: number;
  purchases: number;
  verifications: number;
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

// ==================== API 参数 ====================

export interface AnalysisParams {
  store_id?: string;
  start_date?: string;
  end_date?: string;
  compare_start?: string;
  compare_end?: string;
}

// ==================== API 函数 ====================

const API_BASE = '/v1/store-dashboard';

/** 获取营业额趋势数据 */
export async function fetchRevenueTrend(params?: AnalysisParams): Promise<RevenueTrendData> {
  try {
    const res = await api.get<any>(`${API_BASE}/revenue/trend`, { params });
    const data = res?.data || res;
    return {
      daily: (data?.daily || []).map((d: any) => ({
        date: d.date,
        total_revenue: d.total_revenue || 0,
        meituan_revenue: d.meituan_revenue || 0,
        douyin_revenue: d.douyin_revenue || 0,
        other_revenue: d.other_revenue || 0,
        visitor_count: d.visitor_count || 0,
        table_count: d.table_count || 0,
        avg_people_per_table: d.avg_people_per_table || 0,
        avg_per_capita: d.avg_per_capita || 0,
      })),
      weekly: (data?.weekly || []).map((w: any) => ({
        week_label: w.week_label,
        total_revenue: w.total_revenue || 0,
        meituan_revenue: w.meituan_revenue || 0,
        douyin_revenue: w.douyin_revenue || 0,
        visitor_count: w.visitor_count || 0,
        table_count: w.table_count || 0,
      })),
    };
  } catch {
    return { daily: [], weekly: [] };
  }
}

/** 获取套餐分析排行 */
export async function fetchPackageAnalysis(params?: AnalysisParams): Promise<PackageAnalysisData> {
  try {
    const res = await api.get<any>(`${API_BASE}/packages/ranking`, { params });
    const data = res?.data || res;
    if (!data) {
      return { top_ranking: [], bottom_ranking: [], overall_summary: { total_buy: 0, total_verify: 0, avg_verify_rate: 0 } };
    }
    return {
      top_ranking: (data.top_ranking || []).map((r: any) => ({
        product_name: r.product_name,
        meituan_buy: r.meituan_buy || 0,
        meituan_verify: r.meituan_verify || 0,
        douyin_buy: r.douyin_buy || 0,
        douyin_verify: r.douyin_verify || 0,
        total_verify: r.total_verify || 0,
        verify_rate: r.verify_rate || 0,
      })),
      bottom_ranking: (data.bottom_ranking || []).map((r: any) => ({
        product_name: r.product_name,
        meituan_buy: r.meituan_buy || 0,
        meituan_verify: r.meituan_verify || 0,
        douyin_buy: r.douyin_buy || 0,
        douyin_verify: r.douyin_verify || 0,
        total_verify: r.total_verify || 0,
        verify_rate: r.verify_rate || 0,
      })),
      overall_summary: data.overall_summary || { total_buy: 0, total_verify: 0, avg_verify_rate: 0 },
    };
  } catch {
    return { top_ranking: [], bottom_ranking: [], overall_summary: { total_buy: 0, total_verify: 0, avg_verify_rate: 0 } };
  }
}

/** 获取门店运营健康度 */
export async function fetchStoreHealth(params?: AnalysisParams): Promise<StoreHealthData> {
  try {
    const res = await api.get<any>(`${API_BASE}/metrics/health`, { params });
    const data = res?.data || res;
    if (!data) {
      return { funnels: [], rankings: [], reviews_summary: [], daily_metrics: [] };
    }
    return {
      funnels: (data.funnels || []).map((f: any) => ({
        platform: f.platform,
        impressions: f.impressions || 0,
        visits: f.visits || 0,
        purchases: f.purchases || 0,
        verifications: f.verifications || 0,
        impression_to_visit: f.impression_to_visit || 0,
        visit_to_purchase: f.visit_to_purchase || 0,
      })),
      rankings: data.rankings || [],
      reviews_summary: (data.reviews_summary || []).map((r: any) => ({
        platform: r.platform,
        star_rating: r.star_rating || 0,
        prev_star_rating: r.prev_star_rating || 0,
        new_reviews: r.new_reviews || 0,
        bad_reviews: r.bad_reviews || 0,
        bad_keywords: r.bad_keywords || [],
      })),
      daily_metrics: (data.daily_metrics || []).map((d: any) => ({
        date: d.date,
        platform: d.platform,
        impressions: d.impressions || 0,
        visits: d.visits || 0,
        purchases: d.purchases || 0,
        verifications: d.verifications || 0,
        star_rating: d.star_rating || 0,
        new_reviews: d.new_reviews || 0,
      })),
    };
  } catch {
    return { funnels: [], rankings: [], reviews_summary: [], daily_metrics: [] };
  }
}

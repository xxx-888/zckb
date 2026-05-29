/**
 * 年度报告 API 接口
 */

export interface YearlyData {
  year: number;
  totalReviews: number;
  averageRating: number;
  sentiment: {
    positive: number;
    negative: number;
    neutral: number;
  };
  replyStats: {
    replyRate: number;
    avgReplyTime: number;
    repliedCount: number;
    unrepliedCount: number;
    replySentiment: {
      positive: number;
      negative: number;
      neutral: number;
    };
  };
  monthlyData: Array<{
    month: number;
    count: number;
    avgRating: number;
    replyCount: number;
  }>;
  topKeywords: Array<{
    word: string;
    count: number;
    sentiment: 'positive' | 'negative' | 'neutral';
  }>;
  categoryScores: {
    service: number;
    food: number;
    environment: number;
    price: number;
    speed: number;
  };
  competitorAvgRating?: number;
  marketShare?: number;
  // 新增丰富数据项
  ratingDistribution: {
    1: number; 2: number; 3: number; 4: number; 5: number;
    avg: number;
    total: number;
  };
  platformDistribution: Record<string, number>;
  replySentiment: {
    positive: number;
    negative: number;
    neutral: number;
    total: number;
  };
  peakMonth: {
    month: number;
    count: number;
  };
  activeDays: number;
  monthlySentiment: Array<{
    month: number;
    positive: number;
    negative: number;
    neutral: number;
    replied: number;
    total: number;
    replyRate: number;
  }>;
}

export interface ReportInsights {
  yearOverYear: {
    reviewGrowth: number;
    ratingChange: number;
    replyRateChange: number;
  };
  highlights: string[];
  improvements: string[];
  aiSummary: string;
  personalityType: string;
  recommendations: string[];
}

export interface HistoricalTrends {
  bestYear: number;
  worstYear: number;
  averageRating3Years: number;
  totalReviews3Years: number;
}

import { api } from '@/lib/api';

/** 将后端 snake_case 的年度数据转换为前端 camelCase */
function transformYearlyData(d: any): YearlyData {
  if (!d) return null as any;
  return {
    year: d.year,
    totalReviews: d.total_reviews || 0,
    averageRating: d.average_rating || 0,
    sentiment: {
      positive: d.sentiment_distribution?.positive || 0,
      negative: d.sentiment_distribution?.negative || 0,
      neutral: d.sentiment_distribution?.neutral || 0,
    },
    replyStats: {
      replyRate: d.reply_stats?.reply_rate || 0,
      avgReplyTime: d.reply_stats?.avg_reply_time_hours || 0,
      repliedCount: d.reply_stats?.replied_count || 0,
      unrepliedCount: d.reply_stats?.unreplied_count || 0,
      replySentiment: {
        positive: d.reply_stats?.reply_sentiment_positive || 0,
        negative: d.reply_stats?.reply_sentiment_negative || 0,
        neutral: d.reply_stats?.reply_sentiment_neutral || 0,
      },
    },
    monthlyData: (d.monthly_data || []).map((m: any) => ({
      month: m.month,
      count: m.total || 0,
      avgRating: m.avg_rating || 0,
      replyCount: m.replied || 0,
    })),
    topKeywords: (d.top_keywords || []).map((kw: any) => ({
      word: kw.word,
      count: kw.count,
      sentiment: kw.sentiment || 'neutral',
    })),
    categoryScores: {
      service: d.category_scores?.service || 0,
      food: d.category_scores?.taste || 0,
      environment: d.category_scores?.environment || 0,
      price: d.category_scores?.value || 0,
      speed: d.category_scores?.speed || 0,
    },
    // 新增字段映射
    ratingDistribution: d.rating_distribution || { 1:0, 2:0, 3:0, 4:0, 5:0, avg:0, total:0 },
    platformDistribution: d.platform_distribution || {},
    replySentiment: d.reply_sentiment || { positive:0, negative:0, neutral:0, total:0 },
    peakMonth: d.peak_month || { month:0, count:0 },
    activeDays: d.active_days || 0,
    monthlySentiment: (d.monthly_sentiment || []).map((m: any) => ({
      month: m.month,
      positive: m.positive || 0,
      negative: m.negative || 0,
      neutral: m.neutral || 0,
      replied: m.replied || 0,
      total: m.total || 0,
      replyRate: m.reply_rate || 0,
    })),
  };
}

/** 将后端 snake_case 的洞察数据转换为前端 camelCase */
function transformInsights(d: any): ReportInsights {
  if (!d) return null as any;
  return {
    yearOverYear: {
      reviewGrowth: d.year_over_year?.review_growth ?? d.year_over_year?.growth_rate ?? 0,
      ratingChange: d.year_over_year?.rating_change ?? 0,
      replyRateChange: d.year_over_year?.reply_rate_change ?? 0,
    },
    highlights: d.highlights || [],
    improvements: d.improvements || [],
    aiSummary: d.ai_summary || '',
    personalityType: d.personality_type || '',
    recommendations: d.recommendations || [],
  };
}

/** 获取年度报告数据 GET /v1/reports/annual */
export async function fetchAnnualReport(storeId: string, year: number): Promise<{
  yearlyData: YearlyData | null;
  insights: ReportInsights | null;
  historicalTrends: HistoricalTrends | null;
}> {
  if (!storeId) {
    return { yearlyData: null, insights: null, historicalTrends: null };
  }
  try {
    const res = await api.get<any>(`/v1/reports/annual?store_id=${storeId}&year=${year}`);
    const response = res?.data || res;
    if (!response) return { yearlyData: null, insights: null, historicalTrends: null };

    const yearlyData = transformYearlyData(response.data);
    const insights = transformInsights(response.insights);
    const ht = response.historical_trends || null;

    return {
      yearlyData,
      insights: insights || {
        yearOverYear: { reviewGrowth: 0, ratingChange: 0, replyRateChange: 0 },
        highlights: [],
        improvements: [],
        aiSummary: '',
        personalityType: '',
        recommendations: [],
      },
      historicalTrends: ht ? {
        bestYear: ht.best_year,
        worstYear: ht.worst_year,
        averageRating3Years: ht.average_rating_3_years,
        totalReviews3Years: ht.total_reviews_3_years,
      } : null,
    };
  } catch (err: any) {
    if (err?.status === 404) {
      return { yearlyData: null, insights: null, historicalTrends: null };
    }
    throw err;
  }
}

/** 获取所有年份数据 GET /v1/reports/annual (无 year 参数) */
export async function fetchAllYearlyData(storeId?: string): Promise<Record<number, YearlyData>> {
  const endpoint = storeId ? `/v1/reports/annual?store_id=${storeId}` : '/v1/reports/annual';
  try {
    const res = await api.get<any>(endpoint);
    const data = res?.data || res || {};
    const result: Record<number, YearlyData> = {};
    for (const [k, v] of Object.entries(data)) {
      const yd = transformYearlyData((v as any).data || v);
      if (yd) result[parseInt(k)] = yd;
    }
    return result;
  } catch {
    return {};
  }
}

/** 生成年度报告 POST /v1/reports/annual/generate */
export async function generateAnnualReport(year: number, storeId?: string): Promise<{success: boolean; message: string; data?: any}> {
  try {
    const response = await api.post<any, any>('/v1/reports/annual/generate', { year, store_id: storeId });
    const result = response?.data || response;
    return {
      success: true,
      message: result?.message || `${year}年度报告生成成功`,
      data: result,
    };
  } catch (err: any) {
    const msg = err?.response?.data?.message || err?.message || '生成失败';
    return { success: false, message: msg };
  }
}

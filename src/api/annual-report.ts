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

// 测试数据
const MOCK_ANNUAL_REPORT = {
  yearlyData: {
    '2024': {
      year: 2024,
      totalReviews: 568,
      averageRating: 4.2,
      sentiment: { positive: 342, negative: 85, neutral: 141 },
      replyStats: { replyRate: 85.5, avgReplyTime: 3.2, repliedCount: 485, unrepliedCount: 83, replySentiment: { positive: 308, negative: 8, neutral: 42 } },
      monthlyData: Array.from({ length: 12 }, (_, i) => ({ month: i + 1, count: Math.floor(Math.random() * 50) + 20, avgRating: 4.0 + Math.random() * 0.5, replyCount: Math.floor(Math.random() * 40) + 15 })),
      topKeywords: [
        { word: '服务态度', count: 199, sentiment: 'positive' },
        { word: '菜品口味', count: 159, sentiment: 'positive' },
        { word: '上菜速度', count: 85, sentiment: 'negative' },
        { word: '环境卫生', count: 68, sentiment: 'neutral' },
        { word: '性价比', count: 57, sentiment: 'positive' },
      ],
      categoryScores: { service: 4.4, food: 4.2, environment: 4.1, price: 3.9, speed: 4.0 },
    },
    '2023': {
      year: 2023,
      totalReviews: 423,
      averageRating: 4.0,
      sentiment: { positive: 248, negative: 102, neutral: 73 },
      replyStats: { replyRate: 78.2, avgReplyTime: 4.1, repliedCount: 331, unrepliedCount: 92, replySentiment: { positive: 223, negative: 10, neutral: 37 } },
      monthlyData: Array.from({ length: 12 }, (_, i) => ({ month: i + 1, count: Math.floor(Math.random() * 40) + 15, avgRating: 3.8 + Math.random() * 0.5, replyCount: Math.floor(Math.random() * 30) + 10 })),
      topKeywords: [
        { word: '服务态度', count: 148, sentiment: 'positive' },
        { word: '菜品口味', count: 118, sentiment: 'positive' },
        { word: '上菜速度', count: 102, sentiment: 'negative' },
        { word: '环境卫生', count: 53, sentiment: 'neutral' },
        { word: '性价比', count: 42, sentiment: 'positive' },
      ],
      categoryScores: { service: 4.2, food: 4.0, environment: 3.9, price: 3.7, speed: 3.8 },
    },
  },
  insights: {
    '2024': {
      yearOverYear: { reviewGrowth: 34.3, ratingChange: 0.2, replyRateChange: 7.3 },
      highlights: ['服务态度评价提升显著', '回复率提升至85.5%，超过行业平均水平', '负面评价同比下降15%'],
      improvements: ['上菜速度仍需优化', '性价比评分有提升空间'],
      aiSummary: '2024年整体表现优秀，好评率持续上升。建议重点关注上菜速度和性价比反馈，进一步提升客户满意度。',
      personalityType: '品质追求型',
      recommendations: ['建议优化厨房出餐流程，缩短上菜时间', '可考虑推出性价比套餐，提升竞争力', '继续保持服务优势，加强员工培训'],
    },
  },
  historicalTrends: {
    bestYear: 2024,
    worstYear: 2022,
    averageRating3Years: 4.1,
    totalReviews3Years: 1256,
  },
};

async function fetchAPI<T>(endpoint: string, opts?: { suppress404?: boolean }): Promise<T> {
  try {
    const res = await api.get<any>(endpoint);
    if (res?.code === 200 && res?.data) return res.data;
    if (res?.data) return res.data;
    return res as T;
  } catch (err: any) {
    // 404（报告不存在）不报错，让调用方处理
    if (opts?.suppress404 && err?.status === 404) {
      return null as T;
    }
    throw err;
  }
}

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
      repliedCount: 0,
      unrepliedCount: 0,
      replySentiment: { positive: 0, negative: 0, neutral: 0 },
    },
    monthlyData: (d.monthly_data || []).map((m: any) => ({
      month: m.month,
      count: m.total || 0,
      avgRating: m.avg_rating || 0,
      replyCount: 0,
    })),
    topKeywords: (d.top_keywords || []).map((kw: any) => ({
      word: kw.word,
      count: kw.count,
      sentiment: 'neutral',
    })),
    categoryScores: {
      service: d.category_scores?.service || 0,
      food: d.category_scores?.taste || 0,
      environment: d.category_scores?.environment || 0,
      price: d.category_scores?.value || 0,
      speed: 0,
    },
  };
}

/** 将后端 snake_case 的洞察数据转换为前端 camelCase */
function transformInsights(d: any): ReportInsights {
  if (!d) return null as any;
  return {
    yearOverYear: {
      reviewGrowth: d.year_over_year?.growth_rate || 0,
      ratingChange: 0,
      replyRateChange: 0,
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
    return {
      yearlyData: null,
      insights: null,
      historicalTrends: null,
    };
  }
  const response = await fetchAPI<any>(`/v1/reports/annual?store_id=${storeId}&year=${year}`, { suppress404: true });
  if (!response) {
    return {
      yearlyData: null,
      insights: null,
      historicalTrends: null,
    };
  }
  
  // 后端返回结构: { id, store_id, year, data: {...}, insights: {...}, generated_at }
  const yearlyData = transformYearlyData(response.data);
  const insights = transformInsights(response.insights);
  
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
    historicalTrends: response.historicalTrends || null,
  };
}

/** 获取所有年份数据 GET /v1/reports/annual */
export async function fetchAllYearlyData(storeId?: string): Promise<Record<number, YearlyData>> {
  const endpoint = storeId ? `/v1/reports/annual?store_id=${storeId}` : '/v1/reports/annual';
  const data = await fetchAPI<any>(endpoint);
  return data?.yearlyData || data || {};
}

/** 生成年度报告 POST /v1/reports/annual/generate */
export async function generateAnnualReport(year: number, storeId?: string): Promise<{success: boolean; message: string; data?: any}> {
  try {
    const response = await api.post<any, any>('/v1/reports/annual/generate', { year, store_id: storeId });
    // api 拦截器返回 response.data，后端返回 { code: 200, data: {...}, message: '...' }
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

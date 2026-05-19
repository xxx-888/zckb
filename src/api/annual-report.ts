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

const BASE_URL = '/api';

async function fetchAPI<T>(endpoint: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${endpoint}`);
  if (!res.ok) throw new Error(`API 请求失败: ${res.status}`);
  return res.json();
}

/** 获取年度报告数据 GET /api/annual_report */
export async function fetchAnnualReport(year: number): Promise<{
  yearlyData: YearlyData;
  insights: ReportInsights;
  historicalTrends: HistoricalTrends;
}> {
  const data = await fetchAPI<any>('/annual_report');
  const yd = data?.yearlyData?.[String(year)] || null;
  const yearInsights = data?.insights?.[String(year)] || null;
  return {
    yearlyData: yd,
    insights: yearInsights || {
      yearOverYear: { reviewGrowth: 12.3, ratingChange: 0.2, replyRateChange: 7.4 },
      highlights: [],
      improvements: [],
      aiSummary: '',
      personalityType: data?.personalityType || '',
      recommendations: [],
    },
    historicalTrends: data?.historicalTrends || {
      bestYear: year,
      worstYear: year - 2,
      averageRating3Years: 0,
      totalReviews3Years: 0,
    },
  };
}

/** 获取所有年份数据 GET /api/annual_report */
export async function fetchAllYearlyData(): Promise<Record<number, YearlyData>> {
  const data = await fetchAPI<any>('/annual_report');
  return data.yearlyData || {};
}

/** 生成年度报告 POST /api/annual_report/generate */
export async function generateAnnualReport(year: number): Promise<{success: boolean; message: string}> {
  const res = await fetch(`${BASE_URL}/annual_report/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ year }),
  });
  if (!res.ok) throw new Error(`生成报告失败: ${res.status}`);
  return res.json();
}

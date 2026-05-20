import { api } from '@/lib/api';

export interface YearlyData {
  year: number;
  total_reviews: number;
  average_rating: number;
  sentiment_distribution: any;
  reply_stats: any;
  monthly_data: any[];
  top_keywords: any[];
  category_scores: any;
}

export interface ReportInsights {
  year_over_year: any;
  highlights: string[];
  improvements: string[];
  ai_summary: string;
  personality_type: string;
  recommendations: string[];
}

export interface AnnualReport {
  id: string;
  store_id: string;
  year: number;
  data: YearlyData;
  insights: ReportInsights;
  generated_at: string;
}

export interface WeeklyBrief {
  id: string;
  store_id: string;
  week_start: string;
  week_end: string;
  total_reviews: number;
  positive_count: number;
  negative_count: number;
  neutral_count: number;
  avg_rating: number;
  top_issues: string[];
  top_praises: string[];
  dish_analysis: any;
  ai_summary: string;
}

export const reportsApi = {
  getAnnualReport: async (storeId: string, year: number): Promise<AnnualReport> => {
    const response = await api.get<any>(`/reports/annual?store_id=${storeId}&year=${year}`);
    return response.data || response;
  },

  getAllYearsData: async (storeId: string): Promise<YearlyData[]> => {
    const response = await api.get<any>(`/reports/annual/all-years?store_id=${storeId}`);
    return response.data || response;
  },

  generateAnnualReport: async (storeId: string, year: number): Promise<AnnualReport> => {
    const response = await api.post<any, any>('/reports/annual/generate', { store_id: storeId, year });
    return response.data || response;
  },

  getWeeklyBrief: async (storeId: string, weekStart?: string): Promise<WeeklyBrief> => {
    const url = weekStart 
      ? `/reports/weekly?store_id=${storeId}&week_start=${weekStart}`
      : `/reports/weekly?store_id=${storeId}`;
    const response = await api.get<any>(url);
    return response.data || response;
  },

  generateWeeklyBrief: async (storeId: string): Promise<WeeklyBrief> => {
    const response = await api.post<any, any>('/reports/weekly/generate', { store_id: storeId });
    return response.data || response;
  },
};

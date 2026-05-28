import { api } from '@/lib/api';

export interface Competitor {
  id: string;
  store_id: string;
  name: string;
  platform: string;
  platform_store_id: string;
  rating: number;
  positive_rate: number;
  review_count: number;
  trends_data?: any;
  bad_tags?: string[];
  last_synced_at?: string;
}

export interface CompetitorPlan {
  id: string;
  name: string;
  price: number;
  description: string;
  features: string[];
  competitor_count: number;
  analysis_depth: string;
  report_format: string;
}

export interface CompetitorTask {
  id: string;
  competitor_name: string;
  platform: string;
  status: 'pending' | 'collecting' | 'analyzing' | 'completed' | 'failed';
  payment_status: 'unpaid' | 'paid';
  price: number;
  result_data?: any;
  created_at: string;
  updated_at?: string;
}

export const competitorApi = {
  getCompetitors: async (storeId?: string): Promise<Competitor[]> => {
    const url = storeId ? `/v1/competitors?store_id=${storeId}` : '/v1/competitors';
    const response = await api.get<any>(url);
    return response.data || response;
  },

  addCompetitor: async (data: Partial<Competitor>): Promise<Competitor> => {
    const response = await api.post<any, any>('/v1/competitors', data);
    return response.data || response;
  },

  deleteCompetitor: async (id: string): Promise<void> => {
    const response = await api.delete(`/v1/competitors/${id}`);
    return response.data;
  },

  getCompetitorDetail: async (id: string): Promise<Competitor> => {
    const response = await api.get<any>(`/v1/competitors/${id}`);
    return response.data || response;
  },

  generateReport: async (competitorId: string): Promise<any> => {
    const response = await api.post<any, any>('/v1/competitors/generate-report', { competitor_id: competitorId });
    return response.data || response;
  },

  getPlans: async (): Promise<CompetitorPlan[]> => {
    const response = await api.get<any>('/v1/competitors/plans');
    return response.data || response;
  },

  createTask: async (competitorId: string, planId: string): Promise<CompetitorTask> => {
    const response = await api.post<any, any>('/v1/competitors/tasks', {
      competitor_id: competitorId,
      plan_id: planId,
    });
    return response.data || response;
  },

  getTasks: async (storeId?: string): Promise<CompetitorTask[]> => {
    const url = storeId ? `/v1/competitors/tasks?store_id=${storeId}` : '/v1/competitors/tasks';
    const response = await api.get<any>(url);
    return response.data || response;
  },
};

// 兼容旧函数名的别名
export const fetchCompetitorTasks = competitorApi.getTasks;
export const createCompetitorTask = competitorApi.createTask;
export const fetchCompetitorPlans = competitorApi.getPlans;
export const addCompetitor = competitorApi.addCompetitor;

import { api } from '@/lib/api';

export interface SpiderPlatform {
  id: string;
  name: string;
  display_name: string;
  status: 'active' | 'paused' | 'error';
  reliability: number;
  error_log?: string;
  config: any;
  last_sync_at?: string;
  created_at: string;
}

export interface SpiderSyncLog {
  id: string;
  platform_id: string;
  store_id: string;
  status: 'running' | 'success' | 'failed';
  records_synced: number;
  error_message?: string;
  duration_ms: number;
  started_at: string;
  finished_at?: string;
}

export interface SpiderTask {
  id: string;
  platform_id: string;
  store_id: string;
  task_type: 'full_sync' | 'incremental' | 'reply';
  status: 'pending' | 'running' | 'success' | 'failed';
  priority: number;
  result: any;
  error_message?: string;
  scheduled_at?: string;
  started_at?: string;
  finished_at?: string;
}

export const spiderApi = {
  getPlatforms: async (): Promise<SpiderPlatform[]> => {
    const response = await api.get<any>('/v1/spider/platforms');
    return response.data || response;
  },

  createPlatform: async (data: Partial<SpiderPlatform>): Promise<SpiderPlatform> => {
    const response = await api.post<any, any>('/v1/spider/platforms', data);
    return response.data || response;
  },

  updatePlatform: async (id: string, data: Partial<SpiderPlatform>): Promise<SpiderPlatform> => {
    const response = await api.put<any, any>(`/v1/spider/platforms/${id}`, data);
    return response.data || response;
  },

  deletePlatform: async (id: string): Promise<void> => {
    const response = await api.delete(`/v1/spider/platforms/${id}`);
    return response.data;
  },

  syncPlatform: async (id: string): Promise<void> => {
    const response = await api.post(`/v1/spider/platforms/${id}/sync`);
    return response.data;
  },

  syncAllPlatforms: async (): Promise<void> => {
    const response = await api.post('/v1/spider/sync-all');
    return response.data;
  },

  getSyncLogs: async (platformId?: string, page: number = 1, pageSize: number = 20): Promise<any> => {
    let url = `/v1/spider/logs?page=${page}&page_size=${pageSize}`;
    if (platformId) url += `&platform_id=${platformId}`;
    const response = await api.get<any>(url);
    return response.data || response;
  },

  testPlatformConnection: async (id: string): Promise<void> => {
    const response = await api.post(`/v1/spider/platforms/${id}/test`);
    return response.data;
  },

  getTasks: async (status?: string): Promise<SpiderTask[]> => {
    const url = status ? `/v1/spider/tasks?status=${status}` : '/v1/spider/tasks';
    const response = await api.get<any>(url);
    return response.data || response;
  },

  createTask: async (data: Partial<SpiderTask>): Promise<SpiderTask> => {
    const response = await api.post<any, any>('/v1/spider/tasks', data);
    return response.data || response;
  },

  cancelTask: async (id: string): Promise<void> => {
    const response = await api.post(`/v1/spider/tasks/${id}/cancel`);
    return response.data;
  },
};

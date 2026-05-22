import { api } from '@/lib/api';

export interface SystemStats {
  total_users: number;
  total_stores: number;
  total_reviews: number;
  total_platforms: number;
  active_spiders: number;
  system_health: string;
  pending_audit?: number;
}

export interface AdminUser {
  id: string;
  username: string;
  email: string;
  phone: string;
  role: string;
  status: string;
  is_active?: boolean;
  assignedStores?: string[];
  last_login_at?: string;
  created_at: string;
  password?: string; // 仅创建时使用
}

export interface Role {
  id: string;
  name: string;
  permissions: string[];
  description: string;
}

export const adminApi = {
  getSystemStats: async (period?: string): Promise<SystemStats> => {
    const url = period ? `/v1/admin/dashboard/stats?period=${period}` : '/v1/admin/dashboard/stats';
    const response = await api.get<any>(url);
    return response.data || response;
  },

  getSystemHealth: async (): Promise<any> => {
    const response = await api.get<any>('/v1/admin/system/health');
    return response.data || response;
  },

  exportReport: async (reportType: string, period: string): Promise<Blob> => {
    const response = await api.post(`/v1/admin/system/export-report`, { report_type: reportType, period });
    return response.data;
  },

  getAdminUsers: async (page: number = 1, pageSize: number = 20): Promise<any> => {
    const response = await api.get<any>(`/v1/admin/permissions/admins?page=${page}&page_size=${pageSize}`);
    return response.data || response;
  },

  createAdminUser: async (data: Partial<AdminUser>): Promise<AdminUser> => {
    const response = await api.post<any, any>('/v1/admin/permissions/admins', data);
    return response.data || response;
  },

  updateAdminUser: async (id: string, data: Partial<AdminUser>): Promise<AdminUser> => {
    const response = await api.put<any, any>(`/v1/admin/permissions/admins/${id}`, data);
    return response.data || response;
  },

  disableAdminUser: async (id: string): Promise<void> => {
    const response = await api.post(`/v1/admin/permissions/admins/${id}/disable`);
    return response.data;
  },

  /** 分配门店给用户 */
  assignStores: async (userId: string, storeIds: string[]): Promise<any> => {
    const response = await api.put<any, any>(`/v1/admin/permissions/admins/${userId}`, {
      assigned_stores: storeIds,
    });
    return response.data || response;
  },

  getRoles: async (): Promise<Role[]> => {
    const response = await api.get<any>('/v1/admin/permissions/roles');
    return response.data || response;
  },

  createRole: async (data: Partial<Role>): Promise<Role> => {
    const response = await api.post<any, any>('/v1/admin/permissions/roles', data);
    return response.data || response;
  },

  updateRole: async (id: string, data: Partial<Role>): Promise<Role> => {
    const response = await api.put<any, any>(`/v1/admin/permissions/roles/${id}`, data);
    return response.data || response;
  },

  /** 删除角色 */
  deleteRole: async (id: string): Promise<void> => {
    const response = await api.delete(`/v1/admin/permissions/roles/${id}`);
    return response.data;
  },

  getPermissionsStructure: async (): Promise<any[]> => {
    const response = await api.get<any>('/v1/admin/permissions/structure');
    return response.data || response;
  },

  // ============ AI 配置管理 ============

  getAIModels: async (): Promise<any[]> => {
    const response = await api.get<any>('/v1/ai/models');
    return response.data || response || [];
  },

  createAIModel: async (data: any): Promise<any> => {
    const response = await api.post<any, any>('/v1/ai/models', data);
    return response.data || response;
  },

  updateAIModel: async (configId: string, data: any): Promise<any> => {
    const response = await api.put<any, any>(`/v1/ai/models/${configId}`, data);
    return response.data || response;
  },

  deleteAIModel: async (configId: string): Promise<void> => {
    const response = await api.delete(`/v1/ai/models/${configId}`);
    return response.data;
  },

  testAIModel: async (configId: string): Promise<any> => {
    const response = await api.post(`/v1/ai/models/${configId}/test`);
    return response.data;
  },

  getAIPrompts: async (): Promise<any[]> => {
    const response = await api.get<any>('/v1/ai/prompts');
    return response.data || response || [];
  },

  createAIPrompt: async (data: any): Promise<any> => {
    const response = await api.post<any, any>('/v1/ai/prompts', data);
    return response.data || response;
  },

  updateAIPrompt: async (configId: string, data: any): Promise<any> => {
    const response = await api.put<any, any>(`/v1/ai/prompts/${configId}`, data);
    return response.data || response;
  },

  getAIRules: async (): Promise<any[]> => {
    const response = await api.get<any>('/v1/ai/rules');
    return response.data || response || [];
  },

  createAIRule: async (data: any): Promise<any> => {
    const response = await api.post<any, any>('/v1/ai/rules', data);
    return response.data || response;
  },

  updateAIRule: async (engineId: string, data: any): Promise<any> => {
    const response = await api.put<any, any>(`/v1/ai/rules/${engineId}`, data);
    return response.data || response;
  },

  getAIMonitoring: async (): Promise<any> => {
    const response = await api.get<any>('/v1/ai/monitoring');
    return response.data || response;
  },

  getAIEvaluation: async (): Promise<any> => {
    const response = await api.get<any>('/v1/ai/evaluation');
    return response.data || response;
  },

  getAIConfig: async (): Promise<any> => {
    const response = await api.get<any>('/v1/ai/config');
    return response.data || response;
  },
};

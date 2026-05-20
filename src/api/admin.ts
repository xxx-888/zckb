import { api } from '@/lib/api';

export interface SystemStats {
  total_users: number;
  total_stores: number;
  total_reviews: number;
  total_platforms: number;
  active_spiders: number;
  system_health: string;
}

export interface AdminUser {
  id: string;
  username: string;
  email: string;
  phone: string;
  role: string;
  status: string;
  last_login_at?: string;
  created_at: string;
}

export interface Role {
  id: string;
  name: string;
  permissions: string[];
  description: string;
}

export const adminApi = {
  getSystemStats: async (period?: string): Promise<SystemStats> => {
    const url = period ? `/admin/dashboard/stats?period=${period}` : '/admin/dashboard/stats';
    const response = await api.get<any>(url);
    return response.data || response;
  },

  getSystemHealth: async (): Promise<any> => {
    const response = await api.get<any>('/admin/system/health');
    return response.data || response;
  },

  exportReport: async (reportType: string, period: string): Promise<Blob> => {
    const response = await api.post(`/admin/system/export-report`, { report_type: reportType, period });
    return response.data;
  },

  getAdminUsers: async (page: number = 1, pageSize: number = 20): Promise<any> => {
    const response = await api.get<any>(`/admin/permissions/admins?page=${page}&page_size=${pageSize}`);
    return response.data || response;
  },

  createAdminUser: async (data: Partial<AdminUser>): Promise<AdminUser> => {
    const response = await api.post<any, any>('/admin/permissions/admins', data);
    return response.data || response;
  },

  updateAdminUser: async (id: string, data: Partial<AdminUser>): Promise<AdminUser> => {
    const response = await api.put<any, any>(`/admin/permissions/admins/${id}`, data);
    return response.data || response;
  },

  disableAdminUser: async (id: string): Promise<void> => {
    const response = await api.post(`/admin/permissions/admins/${id}/disable`);
    return response.data;
  },

  getRoles: async (): Promise<Role[]> => {
    const response = await api.get<any>('/admin/permissions/roles');
    return response.data || response;
  },

  createRole: async (data: Partial<Role>): Promise<Role> => {
    const response = await api.post<any, any>('/admin/permissions/roles', data);
    return response.data || response;
  },

  updateRole: async (id: string, data: Partial<Role>): Promise<Role> => {
    const response = await api.put<any, any>(`/admin/permissions/roles/${id}`, data);
    return response.data || response;
  },

  getPermissionsStructure: async (): Promise<any[]> => {
    const response = await api.get<any>('/admin/permissions/structure');
    return response.data || response;
  },
};

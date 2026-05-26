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

  /** 启用用户 */
  enableAdminUser: async (id: string): Promise<void> => {
    const response = await api.post(`/v1/admin/permissions/admins/${id}/enable`);
    return response.data;
  },

  /** 删除用户（硬删除）*/
  deleteAdminUser: async (id: string): Promise<void> => {
    const response = await api.delete(`/v1/admin/permissions/admins/${id}`);
    return response.data;
  },

  /** 分配门店给用户 - 调用专用接口 */
  assignStores: async (userId: string, storeIds: string[]): Promise<any> => {
    const response = await api.post<any, any>(`/v1/admin/permissions/admins/${userId}/stores`, {
      store_ids: storeIds,
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

  // ==================== 区域分配管理 ====================

  /** 获取区域树形结构 */
  getRegionTree: async (): Promise<any> => {
    const response = await api.get<any>('/v1/admin/regions/tree');
    return response.data || response;
  },

  /** 获取用户关联的区域 */
  getUserRegions: async (userId: string): Promise<any> => {
    const response = await api.get<any>(`/v1/admin/permissions/admins/${userId}/regions`);
    return response.data || response;
  },

  /** 添加用户区域关联 */
  addUserRegion: async (userId: string, regionId: string): Promise<any> => {
    const response = await api.post<any, any>(`/v1/admin/permissions/admins/${userId}/regions`, {
      region_id: regionId,
    });
    return response.data || response;
  },

  /** 移除用户区域关联 */
  removeUserRegion: async (userId: string, regionId: string): Promise<any> => {
    const response = await api.delete(`/v1/admin/permissions/admins/${userId}/regions/${regionId}`);
    return response.data || response;
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

  testAIModel: async (configId: string, testMessage?: string, apiKey?: string): Promise<any> => {
    const payload: any = {};
    if (testMessage) payload.test_message = testMessage;
    if (apiKey) payload.api_key = apiKey;
    const response = await api.post(`/v1/ai/models/${configId}/test`, payload, {
      timeout: 60000, // 模型调用可能较慢，60秒超时
    });
    // 拦截器已解一层 response.data，直接返回
    return response;
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

  // ============ AI 指令/规则测试 ============

  testAIPrompt: async (params: any): Promise<any> => {
    const response = await api.post('/v1/ai/test-prompt', params, { timeout: 60000 });
    return response;
  },

  testAIRule: async (params: any): Promise<any> => {
    const response = await api.post('/v1/ai/test-rule', params, { timeout: 60000 });
    return response;
  },

  // ==================== 订阅记录管理 ====================
  
  /** 获取所有用户订阅记录（管理员）*/
  getSubscriptionRecords: async (params: {
    user_id?: string;
    status?: string;
    plan_id?: string;
    page?: number;
    page_size?: number;
  }): Promise<any> => {
    const queryParams = new URLSearchParams();
    if (params.user_id) queryParams.append('user_id', params.user_id);
    if (params.status) queryParams.append('status', params.status);
    if (params.plan_id) queryParams.append('plan_id', params.plan_id);
    if (params.page) queryParams.append('page', params.page.toString());
    if (params.page_size) queryParams.append('page_size', params.page_size.toString());
    
    const response = await api.get<any>(`/v1/admin/subscription/records?${queryParams.toString()}`);
    return response.data || response;
  },

  /** 获取所有支付记录（管理员）*/
  getPaymentRecords: async (params: {
    user_id?: string;
    status?: string;
    payment_method?: string;
    start_date?: string;
    end_date?: string;
    page?: number;
    page_size?: number;
  }): Promise<any> => {
    const queryParams = new URLSearchParams();
    if (params.user_id) queryParams.append('user_id', params.user_id);
    if (params.status) queryParams.append('status', params.status);
    if (params.payment_method) queryParams.append('payment_method', params.payment_method);
    if (params.start_date) queryParams.append('start_date', params.start_date);
    if (params.end_date) queryParams.append('end_date', params.end_date);
    if (params.page) queryParams.append('page', params.page.toString());
    if (params.page_size) queryParams.append('page_size', params.page_size.toString());
    
    const response = await api.get<any>(`/v1/admin/subscription/payments?${queryParams.toString()}`);
    return response.data || response;
  },

  /** 更新订阅状态（管理员）*/
  updateSubscriptionStatus: async (subscriptionId: string, status: string): Promise<any> => {
    const response = await api.patch<any>(`/v1/admin/subscription/records/${subscriptionId}/status?status=${status}`);
    return response.data || response;
  },

  /** 更新支付状态（管理员）*/
  updatePaymentStatus: async (paymentId: string, status: string, transactionId?: string): Promise<any> => {
    const params = new URLSearchParams();
    params.append('status', status);
    if (transactionId) params.append('transaction_id', transactionId);
    
    const response = await api.patch<any>(`/v1/admin/subscription/payments/${paymentId}/status?${params.toString()}`);
    return response.data || response;
  },
};

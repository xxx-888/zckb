import { api } from '@/lib/api';

// 类型定义
export interface PlatformConnectRequest {
  platform: string;
  username: string;
  password: string;
  verify_code?: string;
}

export interface PlatformStoreInfo {
  platform_store_id: string;
  platform_store_name: string;
  platform: string;
  rating: number;
  review_count: number;
  binded?: boolean;
}

export interface PlatformAccount {
  id: string;
  user_id?: string;
  platform: string;
  platform_username: string;
  cookies_status: string;
  last_sync_at?: string;
  error_msg?: string;
  created_at?: string;
  stores_count?: number;
}

export interface UpdatePlatformAccountDto {
  username?: string;
  password?: string;
}

// API 函数
export const platformsApi = {
  // 连接平台账号
  connectPlatform: async (data: PlatformConnectRequest): Promise<{
    success: boolean;
    message: string;
    stores: PlatformStoreInfo[];
  }> => {
    const response = await api.post<any, any>('/v1/platforms/connect', data);
    return response.data || response;
  },

  // 获取平台店铺列表
  getPlatformStores: async (platform: string): Promise<PlatformStoreInfo[]> => {
    const response = await api.get<any>(`/v1/platforms/${platform}/stores`);
    return response.data || response;
  },

  // 绑定平台店铺
  bindPlatformStore: async (platformStoreId: string, storeId: string): Promise<void> => {
    const response = await api.post('/v1/platforms/bind', {
      platform_store_id: platformStoreId,
      store_id: storeId,
    });
    return response.data;
  },

  // 解绑平台店铺
  unbindPlatformStore: async (storePlatformId: string): Promise<void> => {
    const response = await api.delete(`/v1/platforms/${storePlatformId}`);
    return response.data;
  },

  // 同步平台数据
  syncPlatformData: async (storeId: string, platform: string, fullSync: boolean = false): Promise<void> => {
    const response = await api.post('/v1/platforms/sync', {
      store_id: storeId,
      platform,
      full_sync: fullSync,
    });
    return response.data;
  },

  // 获取同步状态
  getSyncStatus: async (storePlatformId: string): Promise<any> => {
    const response = await api.get<any>(`/v1/platforms/sync-status/${storePlatformId}`);
    return response.data || response;
  },

  // 在平台上回复评论
  replyOnPlatform: async (storePlatformId: string, reviewId: string, content: string): Promise<void> => {
    const response = await api.post(`/v1/platforms/${storePlatformId}/reply`, {
      review_id: reviewId,
      content,
    });
    return response.data;
  },

  // 获取已连接的平台账号（用户维度）
  getAccounts: async (): Promise<PlatformAccount[]> => {
    const response = await api.get<any>('/v1/platforms/accounts');
    return response.data || response;
  },

  // 管理员：获取所有用户的平台绑定账号
  getAllAccounts: async (): Promise<PlatformAccount[]> => {
    const response = await api.get<any>('/v1/platforms/admin/accounts');
    return response.data || response;
  },

  // 解绑平台账号
  unbindPlatform: async (accountId: string): Promise<void> => {
    await api.delete(`/v1/platforms/account/${accountId}`);
  },

  // 刷新 Cookies
  refreshCookies: async (accountId: string): Promise<any> => {
    const response = await api.post(`/v1/platforms/account/${accountId}/refresh`);
    return response.data || response;
  },

  // 同步账号登录状态（普通用户）
  syncAccountStatus: async (accountId: string): Promise<void> => {
    const response = await api.post(`/v1/platforms/accounts/${accountId}/sync-status`);
    return response.data || response;
  },

  // 更新平台账号（修改用户名/密码）
  updateAccount: async (accountId: string, data: UpdatePlatformAccountDto): Promise<void> => {
    await api.put(`/v1/platforms/account/${accountId}`, data);
  },

  // ============ 二维码扫码登录 ============

  // 启动二维码登录，返回 {task_id, qr_image, status, expires_in}
  startQRLogin: async (platform: string): Promise<{
    task_id: string;
    qr_image: string;
    status: string;
    expires_in: number;
  }> => {
    const response = await api.post<any, any>('/v1/platforms/qr-login/start', { platform }, {
      timeout: 60000,  // 启动浏览器需要较长时间，给 60 秒
    });
    return response.data || response;
  },

  // 查询二维码登录状态
  getQRLoginStatus: async (taskId: string): Promise<{
    status: string;
    platform?: string;
    platform_username?: string;
    remaining_seconds?: number;
    error_message?: string;
  }> => {
    const response = await api.get<any>(`/v1/platforms/qr-login/status/${taskId}`);
    return response.data || response;
  },

  // 取消二维码登录
  cancelQRLogin: async (taskId: string): Promise<void> => {
    await api.post(`/v1/platforms/qr-login/cancel/${taskId}`);
  },
};

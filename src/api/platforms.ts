import { api } from '@/lib/api';

// 类型定义
export interface PlatformConnectRequest {
  platform: string;
  username: string;
  password: string;
  verify_code?: string;
}

export interface PlatformStoreInfo {
  id?: string;
  platform_store_id: string;
  platform_store_name: string;
  platform: string;
  rating?: number;
  review_count?: number;
  connected?: boolean;
  sync_status?: string;
  binded?: boolean;
}

export interface PlatformAccount {
  id: string;
  user_id?: string;
  user_email?: string;
  user_name?: string;
  platform: string;
  platform_username: string;
  platform_account_id?: string;
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

  // 同步平台评论数据（异步，返回 task_id）
  syncAccountReviews: async (accountId: string): Promise<{ task_id: string; platforms: string[]; store_count: number }> => {
    const response = await api.post<any>(`/v1/platforms/accounts/${accountId}/sync-reviews`);
    return response.data || response;
  },

  // 查询评论同步任务进度（轮询）
  getSyncReviewsStatus: async (accountId: string, taskId: string): Promise<{
    status: string;
    current_platform: string;
    progress: string;
    error?: string;
    result?: { created?: number; skipped?: number; errors?: string[]; [key: string]: any };
  }> => {
    const response = await api.get<any>(`/v1/platforms/accounts/${accountId}/sync-reviews/status/${taskId}`);
    return response.data || response;
  },

  // 获取评论同步结果（入库已在后台完成，此接口只返回统计数字）
  getSyncReviewsResult: async (accountId: string, taskId: string): Promise<{ created: number; skipped: number; total: number; errors: string[]; message: string }> => {
    const response = await api.get<any>(`/v1/platforms/accounts/${accountId}/sync-reviews/result/${taskId}`);
    return response.data || response;
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

  // 获取账号下已同步的店铺列表（从 store_platforms 表查询）
  getAccountStores: async (accountId: string): Promise<PlatformStoreInfo[]> => {
    const response = await api.get<any>(`/v1/platforms/accounts/${accountId}/stores`);
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

  // 同步账号登录状态（普通用户）— 验证登录态 + 同步店铺数据
  syncAccountStatus: async (accountId: string): Promise<{
    status: string;
    platform_username?: string;
    store_count?: number;
    sync_error?: string;
    sync_detail?: { method?: string; [key: string]: any };
    stores?: any[];
    error?: string;
  }> => {
    const response = await api.post(`/v1/platforms/accounts/${accountId}/sync-status`, null, {
      timeout: 60000,  // 同步需要启动浏览器，给 60 秒
    });
    return response.data?.data || response.data || response;
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

  // ============ 短信验证码登录（抖音来客） ============

  // 启动短信登录：发送验证码，返回 {task_id, status, code_sent}
  startSMSLogin: async (platform: string, phone: string): Promise<{
    success: boolean;
    task_id?: string;
    status?: string;
    code_sent?: boolean;
    error?: string;
  }> => {
    const response = await api.post<any, any>('/v1/platforms/sms-login/start', { platform, phone }, {
      timeout: 30000,
    });
    return response.data || response;
  },

  // 提交验证码完成登录
  verifySMSCode: async (taskId: string, platform: string, verifyCode: string): Promise<{
    status: string;
    platform?: string;
    error?: string;
  }> => {
    const response = await api.post<any, any>('/v1/platforms/sms-login/verify', {
      task_id: taskId,
      platform,
      verify_code: verifyCode,
    }, {
      timeout: 45000,
    });
    return response.data || response;
  },

  // 取消短信登录
  cancelSMSLogin: async (taskId: string): Promise<void> => {
    await api.post('/v1/platforms/sms-login/cancel', null, { params: { task_id: taskId } });
  },
};

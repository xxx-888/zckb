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
}

export interface PlatformAccount {
  id: string;
  platform: string;
  platform_account: string;
  connected: boolean;
  last_sync_at?: string;
}

// API 函数
export const platformsApi = {
  // 连接平台账号
  connectPlatform: async (data: PlatformConnectRequest): Promise<{
    success: boolean;
    message: string;
    stores: PlatformStoreInfo[];
  }> => {
    const response = await api.post<any, any>('/platforms/connect', data);
    return response.data || response;
  },

  // 获取平台店铺列表
  getPlatformStores: async (platform: string): Promise<PlatformStoreInfo[]> => {
    const response = await api.get<any>(`/platforms/${platform}/stores`);
    return response.data || response;
  },

  // 绑定平台店铺
  bindPlatformStore: async (platformStoreId: string, storeId: string): Promise<void> => {
    const response = await api.post('/platforms/bind', {
      platform_store_id: platformStoreId,
      store_id: storeId,
    });
    return response.data;
  },

  // 解绑平台店铺
  unbindPlatformStore: async (storePlatformId: string): Promise<void> => {
    const response = await api.delete(`/platforms/${storePlatformId}`);
    return response.data;
  },

  // 同步平台数据
  syncPlatformData: async (storeId: string, platform: string, fullSync: boolean = false): Promise<void> => {
    const response = await api.post('/platforms/sync', {
      store_id: storeId,
      platform,
      full_sync: fullSync,
    });
    return response.data;
  },

  // 获取同步状态
  getSyncStatus: async (storePlatformId: string): Promise<any> => {
    const response = await api.get<any>(`/platforms/sync-status/${storePlatformId}`);
    return response.data || response;
  },

  // 在平台上回复评论
  replyOnPlatform: async (storePlatformId: string, reviewId: string, content: string): Promise<void> => {
    const response = await api.post(`/platforms/${storePlatformId}/reply`, {
      review_id: reviewId,
      content,
    });
    return response.data;
  },

  // 获取已连接的平台账号
  getConnectedAccounts: async (): Promise<PlatformAccount[]> => {
    const response = await api.get<any>('/platforms/accounts');
    return response.data || response;
  },
};

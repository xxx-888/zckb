import { api } from '@/lib/api';

// 类型定义
export interface Store {
  id: string;
  name: string;
  type: 'restaurant' | 'hotel' | 'beverage';
  address?: string;
  owner_name?: string;
  owner_id?: string;
  phone?: string;
  email?: string;
  description?: string;
  status: 'active' | 'pending' | 'inactive';
  health_score?: number;
  platform_count: number;
  review_count: number;
  region_id?: string;
  region_name?: string;
  platforms?: StorePlatform[];
  created_at: string;
}

export interface StorePlatform {
  id: string;
  platform: string;
  platform_store_id: string;
  platform_store_name: string;
  connected: boolean;
  last_sync_at?: string;
  sync_status?: string;
}

export interface StoreReviewStats {
  total_reviews: number;
  avg_rating: number;
  positive_rate: number;
  negative_rate: number;
  reply_rate: number;
  sentiment_distribution: {
    positive: number;
    negative: number;
    neutral: number;
  };
}

export interface MonthlyStats {
  month: string;
  total_reviews: number;
  avg_rating: number;
  positive_count: number;
  negative_count: number;
  reply_count: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
}

// API 函数
export const storesApi = {
  // 获取门店列表
  getStores: async (params?: {
    type?: string;
    status?: string;
    keyword?: string;
    page?: number;
    page_size?: number;
  }): Promise<PaginatedResponse<Store>> => {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          searchParams.append(key, String(value));
        }
      });
    }
    const response = await api.get<any>(`/v1/stores?${searchParams.toString()}`);
    return response.data || response;
  },

  // 获取门店详情
  getStoreById: async (id: string): Promise<Store> => {
    const response = await api.get<any>(`/v1/stores/${id}`);
    return response.data || response;
  },

  // 创建门店
  createStore: async (data: Partial<Store>): Promise<Store> => {
    const response = await api.post<any, any>('/v1/stores', data);
    return response.data || response;
  },

  // 更新门店
  updateStore: async (id: string, data: Partial<Store>): Promise<Store> => {
    const response = await api.put<any, any>(`/v1/stores/${id}`, data);
    return response.data || response;
  },

  // 删除门店
  deleteStore: async (id: string): Promise<void> => {
    const response = await api.delete(`/v1/stores/${id}`);
    return response.data;
  },

  // 激活门店
  activateStore: async (id: string): Promise<Store> => {
    const response = await api.post<any>(`/v1/stores/${id}/activate`);
    return response.data || response;
  },

  // 获取门店评价统计
  getReviewStats: async (id: string, period?: string): Promise<StoreReviewStats> => {
    const url = period ? `/v1/stores/${id}/review-stats?period=${period}` : `/stores/${id}/review-stats`;
    const response = await api.get<any>(url);
    return response.data || response;
  },

  // 获取门店月度统计
  getMonthlyStats: async (id: string): Promise<MonthlyStats[]> => {
    const response = await api.get<any>(`/v1/stores/${id}/monthly-stats`);
    return response.data || response;
  },

  // 获取门店最近评论
  getRecentReviews: async (id: string, limit: number = 10): Promise<any[]> => {
    const response = await api.get<any>(`/v1/stores/${id}/recent-reviews?limit=${limit}`);
    return response.data || response;
  },

  // 获取门店汇总统计
  getStoresStats: async (): Promise<any> => {
    const response = await api.get<any>('/v1/stores/stats');
    return response.data || response;
  },

  // ============ 店铺绑定（当前用户） ============

  // 获取当前用户绑定的店铺
  getMyStores: async (): Promise<Store[]> => {
    const response = await api.get<any>('/v1/user/stores');
    return response.data || response || [];
  },

  // 当前用户绑定店铺（单个）
  bindStore: async (storeId: string): Promise<any> => {
    const response = await api.post<any, any>(`/v1/stores/${storeId}/bind`);
    return response.data || response;
  },

  // 当前用户解绑店铺
  unbindStore: async (storeId: string): Promise<any> => {
    const response = await api.delete(`/v1/stores/${storeId}/bind`);
    return response.data || response;
  },
};

import { api } from '@/lib/api';

// ==================== 类型定义 ====================

export interface CollectionPack {
  id: string;
  name: string;
  credit_amount: number;
  price: number;
  description: string | null;
  is_active: boolean;
}

export interface CollectionOrder {
  id: string;
  user_id: string;
  user_name: string;
  email: string;
  pack_id: string;
  pack_name: string;
  credit_amount: number;
  amount: number;
  payment_method: string;
  status: string;
  transaction_id: string | null;
  paid_at: string | null;
  created_at: string;
}

export interface UserCollectionBalance {
  user_id: string;
  balance: number;
  total_purchased: number;
}

// ==================== 主 API 对象 ====================

export const collectionPackApi = {
  // ==================== 用户端 API ====================

  getPacks: async (): Promise<CollectionPack[]> => {
    const data = await api.get<any>('/v1/collection-packs/plans');
    return data || [];
  },

  purchasePack: async (packId: string, paymentMethod: string = 'wechat'): Promise<CollectionOrder> => {
    const data = await api.post<any, any>('/v1/collection-packs/purchase', {
      pack_id: packId,
      payment_method: paymentMethod,
    });
    return data || {} as CollectionOrder;
  },

  getBalance: async (): Promise<UserCollectionBalance> => {
    const data = await api.get<any>('/v1/collection-packs/balance');
    return data || { user_id: '', balance: 0, total_purchased: 0 };
  },

  getMyOrders: async (page: number = 1, pageSize: number = 20): Promise<CollectionOrder[]> => {
    const data = await api.get<any>(
      `/v1/collection-packs/my-orders?page=${page}&page_size=${pageSize}`
    );
    return data || [];
  },

  // ==================== 后台管理 API ====================

  admin: {
    getPacks: async (): Promise<CollectionPack[]> => {
      const data = await api.get<any>('/v1/admin/collection-packs');
      return data || [];
    },

    createPack: async (data: Partial<CollectionPack>): Promise<CollectionPack> => {
      const result = await api.post<any, any>('/v1/admin/collection-packs', data);
      return result || {} as CollectionPack;
    },

    updatePack: async (id: string, data: Partial<CollectionPack>): Promise<CollectionPack> => {
      const result = await api.put<any, any>(`/v1/admin/collection-packs/${id}`, data);
      return result || {} as CollectionPack;
    },

    deletePack: async (id: string): Promise<void> => {
      await api.delete<any>(`/v1/admin/collection-packs/${id}`);
    },

    getOrders: async (params: {
      user_id?: string;
      status?: string;
      page?: number;
      page_size?: number;
    } = {}): Promise<{ list: CollectionOrder[]; total: number }> => {
      const query = new URLSearchParams();
      if (params.user_id) query.append('user_id', params.user_id);
      if (params.status) query.append('status', params.status);
      if (params.page) query.append('page', String(params.page));
      if (params.page_size) query.append('page_size', String(params.page_size));
      const queryStr = query.toString();
      const url = `/v1/admin/collection-packs/orders${queryStr ? '?' + queryStr : ''}`;
      const data = await api.get<any>(url);
      return data || { list: [], total: 0 };
    },

    updateOrderStatus: async (id: string, newStatus: string): Promise<void> => {
      await api.put<any, any>(
        `/v1/admin/collection-packs/orders/${id}/status`,
        null,
        { params: { new_status: newStatus } }
      );
    },
  },
};

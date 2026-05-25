import { api } from '@/lib/api';

// 类型定义
export interface SubscriptionPlan {
  id: string;
  name: string;
  price_monthly: number;
  price_yearly: number;
  features: string[] | null;
  max_stores: number;
  max_reviews_per_month: number | null;
  is_active: boolean;
}

export interface UserSubscription {
  id: string;
  plan: SubscriptionPlan;
  status: 'trial' | 'active' | 'expired' | 'cancelled';
  start_date: string;
  end_date: string | null;
  auto_renew: boolean;
}

export interface PaymentRecord {
  id: string;
  user_id: string;
  subscription_id: string | null;
  amount: number;
  payment_method: string;
  status: string;
  transaction_id: string | null;
  paid_at: string | null;
}

// API 函数
export const subscriptionApi = {
  // ============ 用户端 ============

  // 获取所有启用的订阅计划
  getPlans: async (): Promise<SubscriptionPlan[]> => {
    const response = await api.get<any>('/v1/subscription/plans');
    return response.data || response;
  },

  // 获取当前用户订阅
  getCurrentSubscription: async (): Promise<UserSubscription | null> => {
    const response = await api.get<any>('/v1/subscription/current');
    return response.data;
  },

  // 升级/订阅套餐
  upgradePlan: async (planId: string): Promise<UserSubscription> => {
    const response = await api.post<any, any>('/v1/subscription/upgrade', { plan_id: planId });
    return response.data || response;
  },

  // 取消订阅
  cancelSubscription: async (): Promise<void> => {
    const response = await api.post('/v1/subscription/cancel');
    return response.data;
  },

  // ============ 管理员 ============

  // 获取所有套餐（含未启用）
  getAllPlans: async (): Promise<SubscriptionPlan[]> => {
    const response = await api.get<any>('/v1/admin/subscription/plans?include_inactive=true');
    return response.data || response;
  },

  // 创建套餐
  createPlan: async (data: Partial<SubscriptionPlan>): Promise<SubscriptionPlan> => {
    const response = await api.post<any, any>('/v1/admin/subscription/plans', data);
    return response.data || response;
  },

  // 更新套餐
  updatePlan: async (id: string, data: Partial<SubscriptionPlan>): Promise<SubscriptionPlan> => {
    const response = await api.put<any, any>(`/v1/admin/subscription/plans/${id}`, data);
    return response.data || response;
  },

  // 删除套餐
  deletePlan: async (id: string): Promise<void> => {
    const response = await api.delete(`/v1/admin/subscription/plans/${id}`);
    return response.data;
  },

  // 切换套餐启用/禁用
  togglePlan: async (id: string): Promise<SubscriptionPlan> => {
    const response = await api.patch<any, any>(`/v1/admin/subscription/plans/${id}/toggle`);
    return response.data || response;
  },

  // ============ 支付模拟 ============

  // 创建支付订单
  createPayment: async (data: { plan_id: string; payment_method: string }): Promise<PaymentRecord> => {
    const response = await api.post<any, any>('/v1/subscription/payment/create', data);
    return response.data || response;
  },

  // 查询支付状态
  getPayment: async (id: string): Promise<PaymentRecord> => {
    const response = await api.get<any>(`/v1/subscription/payment/${id}`);
    return response.data || response;
  },

  // 模拟支付成功
  simulatePayment: async (id: string): Promise<PaymentRecord> => {
    const response = await api.post<any, any>(`/v1/subscription/payment/${id}/simulate`);
    return response.data || response;
  },
};

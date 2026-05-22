import { api } from '@/lib/api';

// 类型定义
export interface SubscriptionPlan {
  id: string;
  name: string;
  price_monthly: number;
  price_yearly: number;
  features: string[];
  max_stores: number;
  max_reviews_per_month: number;
  is_active: boolean;
}

export interface UserSubscription {
  id: string;
  plan: SubscriptionPlan;
  status: 'trial' | 'active' | 'expired' | 'cancelled';
  start_date: string;
  end_date: string;
  auto_renew: boolean;
}

// API 函数
export const subscriptionApi = {
  // 获取所有订阅计划
  getPlans: async (): Promise<SubscriptionPlan[]> => {
    const response = await api.get<any>('/v1/subscription/plans');
    return response.data || response;
  },

  // 获取当前订阅
  getCurrentSubscription: async (): Promise<UserSubscription | null> => {
    const response = await api.get<any>('/v1/subscription/current');
    return response.data;
  },

  // 升级订阅
  upgradePlan: async (planId: string): Promise<UserSubscription> => {
    const response = await api.post<any, any>('/v1/subscription/upgrade', { plan_id: planId });
    return response.data || response;
  },

  // 取消订阅
  cancelSubscription: async (): Promise<void> => {
    const response = await api.post('/v1/subscription/cancel');
    return response.data;
  },
};

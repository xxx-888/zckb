import { api } from '@/lib/api';

export interface HighQualityReview {
  id: string;
  user_name?: string;
  user?: string;
  avatar?: string;
  avatar_url?: string;
  content: string;
  rating: number;
  has_image?: boolean;
  hasImage?: boolean;
  length?: string;
  sentiment: string;
  authorized?: boolean;
  suggested_script?: string;
  suggestedScript?: string;
  created_at?: string;
  time?: string;
}

export interface BrandScript {
  id: string;
  name: string;
  content: string;
  category: string;
  usage_count?: number;
  count?: number;
  tag?: string;
  progress?: number;
}

export const positiveActivationApi = {
  getHighQualityReviews: async (page: number = 1, pageSize: number = 20): Promise<any> => {
    const response = await api.get<any>(`/positive-activation/high-quality-reviews?page=${page}&page_size=${pageSize}`);
    return response.data || response;
  },

  getBrandScripts: async (): Promise<BrandScript[]> => {
    const response = await api.get<any>('/positive-activation/brand-scripts');
    return response.data || response;
  },

  copyScript: async (scriptId: string): Promise<void> => {
    const response = await api.post(`/positive-activation/copy-script/${scriptId}`);
    return response.data;
  },

  sendAuthorization: async (reviewId: string): Promise<void> => {
    const response = await api.post(`/positive-activation/send-authorization/${reviewId}`);
    return response.data;
  },

  generateContent: async (reviewId: string, platform: string): Promise<any> => {
    const response = await api.post<any, any>('/positive-activation/generate-content', {
      review_id: reviewId,
      platform,
    });
    return response.data || response;
  },
};

// 兼容旧函数名的别名
export const fetchHighQualityReviews = positiveActivationApi.getHighQualityReviews;
export const fetchBrandScripts = positiveActivationApi.getBrandScripts;
export const copyScript = positiveActivationApi.copyScript;
export const sendAuthorization = positiveActivationApi.sendAuthorization;
export const generateContent = positiveActivationApi.generateContent;

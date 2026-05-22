import { api } from '@/lib/api';

// 类型定义
export interface Review {
  id: string;
  store_id?: string;
  store_name?: string;
  platform: string;
  platform_review_id?: string;
  user_name?: string;
  user_avatar?: string;
  user?: string;
  rating: number;
  content: string;
  images?: string[];
  sentiment: 'positive' | 'negative' | 'neutral';
  tags?: string[];
  reply?: string;
  reply_time?: string;
  ai_generated?: boolean;
  ai_reply_draft?: string;
  risk_level?: 'high' | 'medium' | 'low';
  status: string;
  platform_created_at?: string;
  created_at?: string;
  time?: string;
  hasImage?: boolean;
  has_image?: boolean;
  replied?: boolean;
}

export interface ReviewFilter {
  sentiment?: string;
  keyword?: string;
  store_id?: string;
  platform?: string;
  rating_min?: number;
  rating_max?: number;
  has_reply?: boolean;
  has_image?: boolean;
  start_date?: string;
  end_date?: string;
  page?: number;
  page_size?: number;
}

export interface ReviewStats {
  total_reviews: number;
  positive_count: number;
  negative_count: number;
  neutral_count: number;
  avg_rating: number;
  reply_rate: number;
  ai_reply_rate: number;
  period: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
}

// API 函数
export const reviewsApi = {
  // 获取评论列表
  getReviews: async (filters?: ReviewFilter): Promise<PaginatedResponse<Review>> => {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          params.append(key, String(value));
        }
      });
    }
    const response = await api.get<any>(`/v1/reviews?${params.toString()}`);
    return response.data || response;
  },

  // 获取评论详情
  getReviewById: async (id: string): Promise<Review> => {
    const response = await api.get<any>(`/v1/reviews/${id}`);
    return response.data || response;
  },

  // 获取相似评论
  getSimilarReviews: async (id: string): Promise<Review[]> => {
    const response = await api.get<any>(`/v1/reviews/${id}/similar`);
    return response.data || response;
  },

  // 获取评论统计
  getStats: async (period?: string): Promise<ReviewStats> => {
    const url = period ? `/v1/reviews/stats?period=${period}` : '/v1/reviews/stats';
    const response = await api.get<any>(url);
    return response.data || response;
  },

  // 更新评论（如添加回复）
  updateReview: async (id: string, data: { reply?: string; status?: string }): Promise<Review> => {
    const response = await api.put<any, any>(`/v1/reviews/${id}`, data);
    return response.data || response;
  },

  // 快速回复
  quickReply: async (id: string, replyContent: string): Promise<Review> => {
    const response = await api.post<any, any>(`/v1/reviews/${id}/reply`, { reply_content: replyContent });
    return response.data || response;
  },

  // 审核通过并发送回复
  approveReply: async (id: string): Promise<Review> => {
    const response = await api.post<any, any>(`/v1/reviews/${id}/approve-reply`);
    return response.data || response;
  },

  // 批量删除
  batchDelete: async (ids: string[]): Promise<void> => {
    const response = await api.post('/v1/reviews/batch-delete', { ids });
    return response.data;
  },

  // 点赞评论
  likeReview: async (id: string): Promise<void> => {
    const response = await api.post(`/v1/reviews/${id}/like`);
    return response.data;
  },

  // 创建评论（用于管理后台）
  createReview: async (data: Partial<Review>): Promise<Review> => {
    const response = await api.post<any, any>('/v1/reviews', data);
    return response.data || response;
  },

  // 删除评论
  deleteReview: async (id: string): Promise<void> => {
    const response = await api.delete(`/v1/reviews/${id}`);
    return response.data;
  },
};

// 兼容旧函数名的别名
export const fetchReviews = reviewsApi.getReviews;
export const fetchReviewById = reviewsApi.getReviewById;
export const createReview = reviewsApi.createReview;
export const updateReview = reviewsApi.updateReview;
export const deleteReview = reviewsApi.deleteReview;

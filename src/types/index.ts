/**
 * 全局类型定义
 * 为项目提供完整的TypeScript类型支持
 */

// 用户相关
export interface User {
  id: string;
  username: string;
  email: string;
  role: 'MERCHANT' | 'HQ' | 'OPERATOR';
  assignedStores: string[];
  avatar?: string;
}

// 门店相关
export interface Store {
  id: string;
  name: string;
  type: 'restaurant' | 'hotel' | 'beverage';
  address: string;
  rating: number;
  reviewCount: number;
  status: 'active' | 'inactive' | 'pending';
  createdAt: string;
  owner_id?: string;
  owner_name?: string;
  region_id?: string;
  region_name?: string;
}

// 评论相关
export interface Review {
  id: string;
  userId: string;
  storeId: string;
  platform: 'meituan' | 'dianping' | 'douyin' | 'xiaohongshu';
  rating: number;
  content: string;
  images?: string[];
  reply?: string;
  repliedAt?: string;
  createdAt: string;
}

// API响应类型
export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

// 分页类型
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
}

// 统计数据类型
export interface DashboardStats {
  totalReviews: number;
  averageRating: number;
  positiveRate: number;
  aiReplyRate: number;
  trends: {
    reviews: number;
    rating: number;
    positiveRate: number;
    aiReplyRate: number;
  };
}

// 系统状态类型
export interface SystemStatus {
  name: string;
  status: 'normal' | 'warning' | 'error';
  health: number;
  load: 'low' | 'medium' | 'high';
}

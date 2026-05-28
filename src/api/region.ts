import { api } from '@/lib/api';

// 类型定义
export interface Region {
  id: string;
  name: string;
  parent_id: string | null;
  level: 'province' | 'city' | 'district';
  code: string | null;
  created_at: string | null;
  updated_at: string | null;
  parent?: Region | null;
  children?: Region[];
  store_count?: number;
}

export interface RegionTree {
  id: string;
  name: string;
  level: string;
  code: string | null;
  children?: RegionTree[];
}

export interface RegionCreateRequest {
  name: string;
  parent_id?: string | null;
  level: 'province' | 'city' | 'district';
  code?: string | null;
}

export interface RegionUpdateRequest {
  name?: string;
  parent_id?: string | null;
  level?: 'province' | 'city' | 'district';
  code?: string | null;
}

// API 函数
export const regionApi = {
  // 获取区域列表
  getRegions: async (params?: {
    parent_id?: string;
    level?: string;
    tree?: boolean;
  }): Promise<Region[]> => {
    const response = await api.get<any>('/v1/admin/regions', { params });
    return response?.data || [];
  },

  // 获取区域树形结构
  getRegionTree: async (): Promise<RegionTree[]> => {
    const response = await api.get<any>('/v1/admin/regions/tree');
    return response?.data || [];
  },

  // 获取单个区域详情
  getRegion: async (id: string): Promise<Region | null> => {
    const response = await api.get<any>(`/v1/admin/regions/${id}`);
    return response?.data || null;
  },

  // 创建区域
  createRegion: async (data: RegionCreateRequest): Promise<Region> => {
    const result = await api.post<any, any>('/v1/admin/regions', data);
    return result?.data;
  },

  // 更新区域
  updateRegion: async (id: string, data: RegionUpdateRequest): Promise<Region> => {
    const result = await api.put<any, any>(`/v1/admin/regions/${id}`, data);
    return result?.data;
  },

  // 删除区域
  deleteRegion: async (id: string): Promise<void> => {
    await api.delete(`/v1/admin/regions/${id}`);
  },
};

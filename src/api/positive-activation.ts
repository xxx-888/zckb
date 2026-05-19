/**
 * 好评激活 & 营销 API 接口
 */

export interface HighQualityReview {
  id: number;
  user: string;
  avatar: string;
  content: string;
  rating: number;
  hasImage: boolean;
  length: string;
  sentiment: string;
  authorized: boolean;
  suggestedScript: string;
}

export interface BrandScript {
  tag: string;
  progress: string;
  count: number;
}

const BASE_URL = '/api';

async function fetchAPI<T>(endpoint: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${endpoint}`);
  if (!res.ok) throw new Error(`API 请求失败: ${res.status}`);
  return res.json();
}

/** 获取优质好评列表 GET /api/positive_activation */
export async function fetchHighQualityReviews(): Promise<HighQualityReview[]> {
  const data = await fetchAPI<any>('/positive_activation');
  return data.highQualityReviews || [];
}

/** 获取品牌话术库 GET /api/positive_activation */
export async function fetchBrandScripts(): Promise<BrandScript[]> {
  const data = await fetchAPI<any>('/positive_activation');
  return data.brandScripts || [];
}

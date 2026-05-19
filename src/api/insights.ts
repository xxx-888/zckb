/**
 * 经营洞察 API 接口
 */

export interface Dish {
  name: string;
  score: number;
  positive: number;
  negative: number;
  type: 'recommended' | 'potential' | 'problem';
}

export interface ThreeGoodThreeBad {
  goods: string[];
  bads: string[];
}

const BASE_URL = '/api';

async function fetchAPI<T>(endpoint: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${endpoint}`);
  if (!res.ok) throw new Error(`API 请求失败: ${res.status}`);
  return res.json();
}

/** 获取菜品口碑排行 GET /api/insights */
export async function fetchTopDish(): Promise<Dish[]> {
  const data = await fetchAPI<any>('/insights');
  return data.topDish || [];
}

/** 获取三好三差 GET /api/insights */
export async function fetchThreeGoodThreeBad(): Promise<ThreeGoodThreeBad> {
  const data = await fetchAPI<any>('/insights');
  return data.threeGoodThreeBad || { goods: [], bads: [] };
}

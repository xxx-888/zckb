/**
 * 经营洞察 API 接口
 */

import { api } from '@/lib/api';

// 类型定义
export interface Dish {
  id?: string;
  name: string;
  type: 'recommended' | 'potential' | 'questionable';
  score: number;
  positive: number;
  negative: number;
  trend?: 'up' | 'down' | 'stable';
}

export interface ThreeGoodThreeBad {
  goods: string[];
  bads: string[];
}

export interface DishElimination {
  id?: string;
  name: string;
  score: number;
  negativeRate: number;
  reason: string;
  suggestion: string;
}

export interface ServiceCase {
  id?: string;
  type: 'complaint' | 'praise' | 'suggestion';
  content: string;
  result: string;
  date: string;
}

export interface CompetitorOpportunity {
  id?: string;
  title: string;
  description: string;
  action: string;
}

// ============ API 函数（无 mock 降级） ============

/** 获取菜品口碑排行 */
export async function fetchTopDish(period?: string, storeId?: string): Promise<Dish[]> {
  const params = new URLSearchParams();
  if (period) params.append('period', period);
  if (storeId) params.append('store_id', storeId);
  const query = params.toString();
  const res = await api.get<any>(`/v1/insights/top-dishes${query ? `?${query}` : ''}`);
  const data = res.data || res;
  return data.map((d: any) => ({
    id: d.id,
    name: d.name || d.dish_name || '',
    type: d.type || 'potential',
    score: d.score || d.avg_rating || 0,
    positive: d.positive || d.positive_count || 0,
    negative: d.negative || d.negative_count || 0,
    trend: d.trend || 'stable',
  }));
}

/** 获取三好三差报告 */
export async function fetchThreeGoodThreeBad(period?: string, storeId?: string): Promise<ThreeGoodThreeBad> {
  const params = new URLSearchParams();
  if (period) params.append('period', period);
  if (storeId) params.append('store_id', storeId);
  const query = params.toString();
  const res = await api.get<any>(`/v1/insights/three-good-three-bad${query ? `?${query}` : ''}`);
  const data = res.data || res;
  return {
    goods: data.goods || data.good_items || [],
    bads: data.bads || data.bad_items || [],
  };
}

/** 获取末位淘汰建议 */
export async function fetchDishElimination(storeId?: string): Promise<DishElimination[]> {
  const params = new URLSearchParams();
  if (storeId) params.append('store_id', storeId);
  const query = params.toString();
  const res = await api.get<any>(`/v1/insights/dish-elimination${query ? `?${query}` : ''}`);
  const data = res.data || res;
  return data.map((d: any) => ({
    id: d.id,
    name: d.name || d.dish_name || '',
    score: d.score || d.avg_rating || 0,
    negativeRate: d.negativeRate || d.negative_rate || 0,
    reason: d.reason || '',
    suggestion: d.suggestion || '',
  }));
}

/** 获取服务案例库 */
export async function fetchServiceCases(caseType?: string, storeId?: string): Promise<ServiceCase[]> {
  const params = new URLSearchParams();
  if (caseType) params.append('case_type', caseType);
  if (storeId) params.append('store_id', storeId);
  const query = params.toString();
  const res = await api.get<any>(`/v1/insights/service-cases${query ? `?${query}` : ''}`);
  const data = res.data || res;
  return data.map((c: any) => ({
    id: c.id,
    type: c.type || 'suggestion',
    content: c.content || '',
    result: c.result || '',
    date: c.date || c.created_at || '',
  }));
}

/** 获取同行机会洞察 */
export async function fetchCompetitorOpportunities(storeId?: string): Promise<CompetitorOpportunity[]> {
  const params = new URLSearchParams();
  if (storeId) params.append('store_id', storeId);
  const query = params.toString();
  const res = await api.get<any>(`/v1/insights/competitor-opportunities${query ? `?${query}` : ''}`);
  const data = res.data || res;
  return data.map((o: any) => ({
    id: o.id,
    title: o.title || '',
    description: o.description || '',
    action: o.action || '',
  }));
}

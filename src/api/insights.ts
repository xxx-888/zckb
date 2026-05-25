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

// ============ 测试数据 ============
const MOCK_TOP_DISHES: Dish[] = [
  { name: '招牌牛肉面', type: 'recommended', score: 4.8, positive: 245, negative: 12, trend: 'up' },
  { name: '酸菜鱼', type: 'recommended', score: 4.6, positive: 198, negative: 15, trend: 'stable' },
  { name: '宫保鸡丁', type: 'potential', score: 4.3, positive: 156, negative: 23, trend: 'up' },
  { name: '麻辣烫', type: 'questionable', score: 3.8, positive: 89, negative: 45, trend: 'down' },
  { name: '水煮鱼', type: 'potential', score: 4.1, positive: 134, negative: 28, trend: 'stable' },
];

const MOCK_THREE_GOOD_THREE_BAD: ThreeGoodThreeBad = {
  goods: ['服务态度热情', '菜品口味正宗', '上菜速度快'],
  bads: ['停车不便', '排队时间长', '部分菜品偏咸'],
};

const MOCK_DISH_ELIMINATION: DishElimination[] = [
  { name: '麻辣烫', score: 3.8, negativeRate: 22, reason: '差评率持续高于20%，销量表现一般', suggestion: '建议优化口味或下架' },
  { name: '干煸豆角', score: 3.9, negativeRate: 18, reason: '食材新鲜度反馈不佳', suggestion: '建议更换供应商或优化烹饪方式' },
];

const MOCK_SERVICE_CASES: ServiceCase[] = [
  { type: 'praise', content: '服务员主动帮客人打包剩余菜品', result: '客户满意度提升', date: '2025-01-15' },
  { type: 'complaint', content: '客人投诉上菜慢', result: '优化厨房流程，缩短出餐时间', date: '2025-01-14' },
  { type: 'suggestion', content: '建议增加儿童餐具', result: '已采购并投入使用', date: '2025-01-13' },
];

const MOCK_COMPETITOR_OPPORTUNITIES: CompetitorOpportunity[] = [
  { title: '30分钟未上齐免单', description: '竞品A近期"上菜慢"差评增多', action: '建议主推此服务' },
  { title: '免费停车券', description: '周边竞品均提供停车优惠', action: '建议跟进，提升竞争力' },
];

// ============ API 函数 ============
/** 获取菜品口碑排行 GET /api/v1/insights/top-dishes */
export async function fetchTopDish(period?: string, storeId?: string): Promise<Dish[]> {
  try {
    const params = new URLSearchParams();
    if (period) params.append('period', period);
    if (storeId) params.append('store_id', storeId);
    const query = params.toString();
    const res = await api.get<any[]>(`/v1/insights/top-dishes${query ? `?${query}` : ''}`);
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
  } catch {
    return MOCK_TOP_DISHES;
  }
}

/** 获取三好三差报告 GET /api/v1/insights/three-good-three-bad */
export async function fetchThreeGoodThreeBad(period?: string, storeId?: string): Promise<ThreeGoodThreeBad> {
  try {
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
  } catch {
    return MOCK_THREE_GOOD_THREE_BAD;
  }
}

/** 获取末位淘汰建议 GET /api/v1/insights/dish-elimination */
export async function fetchDishElimination(storeId?: string): Promise<DishElimination[]> {
  try {
    const params = new URLSearchParams();
    if (storeId) params.append('store_id', storeId);
    const query = params.toString();
    const res = await api.get<any[]>(`/v1/insights/dish-elimination${query ? `?${query}` : ''}`);
    const data = res.data || res;
    return data.map((d: any) => ({
      id: d.id,
      name: d.name || d.dish_name || '',
      score: d.score || d.avg_rating || 0,
      negativeRate: d.negativeRate || d.negative_rate || 0,
      reason: d.reason || '',
      suggestion: d.suggestion || '',
    }));
  } catch {
    return MOCK_DISH_ELIMINATION;
  }
}

/** 获取服务案例库 GET /api/v1/insights/service-cases */
export async function fetchServiceCases(caseType?: string, storeId?: string): Promise<ServiceCase[]> {
  try {
    const params = new URLSearchParams();
    if (caseType) params.append('case_type', caseType);
    if (storeId) params.append('store_id', storeId);
    const query = params.toString();
    const res = await api.get<any[]>(`/v1/insights/service-cases${query ? `?${query}` : ''}`);
    const data = res.data || res;
    return data.map((c: any) => ({
      id: c.id,
      type: c.type || 'suggestion',
      content: c.content || '',
      result: c.result || '',
      date: c.date || c.created_at || '',
    }));
  } catch {
    return MOCK_SERVICE_CASES;
  }
}

/** 获取同行机会洞察 GET /api/v1/insights/competitor-opportunities */
export async function fetchCompetitorOpportunities(storeId?: string): Promise<CompetitorOpportunity[]> {
  try {
    const params = new URLSearchParams();
    if (storeId) params.append('store_id', storeId);
    const query = params.toString();
    const res = await api.get<any[]>(`/v1/insights/competitor-opportunities${query ? `?${query}` : ''}`);
    const data = res.data || res;
    return data.map((o: any) => ({
      id: o.id,
      title: o.title || '',
      description: o.description || '',
      action: o.action || '',
    }));
  } catch {
    return MOCK_COMPETITOR_OPPORTUNITIES;
  }
}

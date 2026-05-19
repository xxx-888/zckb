/**
 * 竞对分析 API 接口
 */

export interface CompetitorPlan {
  id: string;
  name: string;
  price: number;
  description: string;
  features: string[];
  iconBg: string;
  bgColor: string;
  borderColor: string;
  recommended?: boolean;
}

export interface CompetitorTask {
  id: string;
  competitor_name: string;
  platform: string;
  status: 'pending' | 'collecting' | 'analyzing' | 'completed';
  payment_status: 'unpaid' | 'paid';
  price: number;
  created_at: string;
}

const BASE_URL = '/api';

async function fetchAPI<T>(endpoint: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${endpoint}`);
  if (!res.ok) throw new Error(`API 请求失败: ${res.status}`);
  return res.json();
}

/** 获取套餐列表 GET /api/competitor/plans */
export async function fetchCompetitorPlans(): Promise<CompetitorPlan[]> {
  const data = await fetchAPI<any>('/competitor');
  return data.plans || [];
}

/** 获取任务列表 GET /api/competitor/tasks */
export async function fetchCompetitorTasks(): Promise<CompetitorTask[]> {
  const data = await fetchAPI<any>('/competitor');
  return data.tasks || [];
}

/** 创建竞对分析任务 POST /api/competitor/tasks */
export async function createCompetitorTask(task: Omit<CompetitorTask, 'id' | 'created_at'>): Promise<CompetitorTask> {
  const res = await fetch(`${BASE_URL}/competitor/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(task),
  });
  if (!res.ok) throw new Error(`创建任务失败: ${res.status}`);
  return res.json();
}

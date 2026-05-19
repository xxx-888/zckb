/**
 * 差评回复 API 接口
 */

export interface NegativeReplyTask {
  id: number;
  user: string;
  rating: number;
  content: string;
  time: string;
  platform: string;
  aiDraft: string;
  risk: 'high' | 'medium' | 'low';
  scores: {
    realism: number;
    empathy: number;
    concreteness: number;
    consistency: number;
  };
}

const BASE_URL = '/api';

async function fetchAPI<T>(endpoint: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${endpoint}`);
  if (!res.ok) throw new Error(`API 请求失败: ${res.status}`);
  return res.json();
}

/** 获取差评回复任务列表 */
export async function fetchNegativeReplyTasks(): Promise<NegativeReplyTask[]> {
  const data = await fetchAPI<{ tasks: NegativeReplyTask[] }>('/negative_reply');
  return data.tasks || [];
}

import { api } from '@/lib/api';

// 类型定义
export interface NegativeReplyTask {
  id: string;
  review_id: string;
  user_name: string;
  rating: number;
  content: string;
  platform: string;
  ai_draft: string;
  risk: 'high' | 'medium' | 'low';
  scores: {
    realism: number;
    empathy: number;
    concreteness: number;
    consistency: number;
  };
  status: string;
  created_at: string;
  // 兼容字段
  user?: string;
  aiDraft?: string;
}

export interface NegativeReplyHistory {
  id: string;
  review_id: string;
  user_name: string;
  content: string;
  rating: number;
  platform: string;
  ai_draft: string;
  final_reply?: string;
  status: string;
  created_at: string;
}

export const negativeReplyApi = {
  getTasks: async (status?: string, page: number = 1, pageSize: number = 20, storeId?: string, search?: string, risk?: string): Promise<any> => {
    let url = `/v1/negative-reply/tasks?page=${page}&page_size=${pageSize}`;
    if (status) url += `&status=${status}`;
    if (storeId) url += `&store_id=${storeId}`;
    if (search) url += `&search=${encodeURIComponent(search)}`;
    if (risk && risk !== 'all') url += `&risk=${risk}`;
    const response = await api.get<any>(url);
    console.log('negativeReplyApi.getTasks response:', response);
    return response.data || response;
  },

  approveTask: async (taskId: string): Promise<void> => {
    const response = await api.post(`/v1/negative-reply/tasks/${taskId}/approve`, {});
    return response.data;
  },

  rejectTask: async (taskId: string, reason: string): Promise<void> => {
    const response = await api.post(`/v1/negative-reply/tasks/${taskId}/reject`, { reason });
    return response.data;
  },

  regenerateReply: async (taskId: string): Promise<void> => {
    const response = await api.post(`/v1/negative-reply/tasks/${taskId}/regenerate`, {});
    return response.data;
  },

  getHistory: async (page: number = 1, pageSize: number = 20): Promise<any> => {
    const response = await api.get<any>(`/v1/negative-reply/history?page=${page}&page_size=${pageSize}`);
    return response.data || response;
  },
};

// 兼容旧函数名的别名（支持分页 + 搜索/筛选）
export const fetchNegativeReplyTasks = async (
  storeId?: string,
  page: number = 1,
  pageSize: number = 20,
  search?: string,
  risk?: string
): Promise<{ items: NegativeReplyTask[]; total: number; page: number; pageSize: number }> => {
  console.log('fetchNegativeReplyTasks called with:', { storeId, page, pageSize, search, risk });
  const response = await negativeReplyApi.getTasks('pending', page, pageSize, storeId, search, risk);
  console.log('fetchNegativeReplyTasks response:', response);
  const items = response.items || [];
  const total = response.total || items.length;
  
  // 转换数据格式以匹配前端期望
  const formattedItems = items.map((item: any) => ({
    id: item.id || item.review_id,
    review_id: item.review_id || item.id,
    user: item.user_name || item.user || '匿名用户',
    user_name: item.user_name || item.user || '匿名用户',
    rating: item.rating || 3,
    content: item.content || '',
    platform: item.platform || '大众点评',
    aiDraft: item.ai_draft || item.ai_reply_draft || '',
    ai_draft: item.ai_draft || item.ai_reply_draft || '',
    risk: item.risk || 'medium',
    scores: item.scores || {
      realism: 7,
      empathy: 7,
      concreteness: 7,
      consistency: 7,
    },
    status: item.status || 'pending',
    created_at: item.created_at || new Date().toISOString(),
  }));
  
  console.log('fetchNegativeReplyTasks returning:', { 
    itemsCount: formattedItems.length, 
    total, 
    page: response.page || page,
    pageSize: response.pageSize || pageSize 
  });
  
  return {
    items: formattedItems,
    total: total,
    page: response.page || page,
    pageSize: response.pageSize || pageSize,
  };
};

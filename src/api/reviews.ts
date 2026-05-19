/**
 * 评论数据 API 接口
 */

export interface Review {
  id: number;
  store: string;
  avatar: string;
  rating: number;
  user: string;
  content: string;
  platform: string;
  time: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  replied: boolean;
  reply?: string;
  replyTime?: string;
  tags?: string[];
  hasImage?: boolean;
  images?: string[];
  likeCount?: number;
  aiGenerated?: boolean;
}

export interface ReviewStreamItem {
  id: number;
  user: string;
  avatar: string;
  rating: number;
  content: string;
  platform: string;
  time: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  tags: string[];
  hasImage: boolean;
}

const BASE_URL = '/api';

async function fetchAPI<T>(endpoint: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${endpoint}`);
  if (!res.ok) throw new Error(`API 请求失败: ${res.status}`);
  return res.json();
}

/** 获取评论列表 GET /api/reviews/list */
export async function fetchReviews(params?: {
  sentiment?: string;
  keyword?: string;
  store?: string;
}): Promise<Review[]> {
  const data = await fetchAPI<{ list: Review[] }>('/reviews');
  let list: Review[] = data.list || [];

  if (params?.sentiment && params.sentiment !== 'all') {
    list = list.filter(r => r.sentiment === params.sentiment);
  }
  if (params?.keyword) {
    const kw = params.keyword.toLowerCase();
    list = list.filter(r =>
      r.content.toLowerCase().includes(kw) ||
      r.user.toLowerCase().includes(kw) ||
      (r.store && r.store.toLowerCase().includes(kw))
    );
  }
  return list;
}

/** 根据 ID 获取单条评论 */
export async function fetchReviewById(id: string): Promise<Review | null> {
  const data = await fetchAPI<{ list: Review[] }>('/reviews');
  const list = data.list || [];
  return list.find(r => String(r.id) === id) || null;
}

/** 新增评论 POST /api/reviews/list */
export async function createReview(data: Omit<Review, 'id'>): Promise<Review> {
  const res = await fetch(`${BASE_URL}/reviews/list`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(`创建评论失败: ${res.status}`);
  return res.json();
}

/** 更新评论 PUT /api/reviews/list/:id */
export async function updateReview(id: number, data: Partial<Review>): Promise<Review> {
  const res = await fetch(`${BASE_URL}/reviews/list/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(`更新评论失败: ${res.status}`);
  return res.json();
}

/** 删除评论 DELETE /api/reviews/list/:id */
export async function deleteReview(id: number): Promise<void> {
  const res = await fetch(`${BASE_URL}/reviews/list/${id}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error(`删除评论失败: ${res.status}`);
}

/** 获取评论动态流 GET /api/reviews/stream */
export async function fetchReviewStream(): Promise<
  Array<{ id: number; user: string; avatar: string; action: string; target: string; rating?: number; time: string }>
> {
  const data = await fetchAPI<{ stream: any[] }>('/reviews');
  return data.stream || [];
}

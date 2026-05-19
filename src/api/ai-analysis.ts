/**
 * AI 智能分析 API 接口
 */

export interface Topic {
  label: string;
  sentiment: number;
  count: number;
  trend: 'up' | 'down' | 'stable';
}

export interface TagCluster {
  category: string;
  items: string[];
  percentage: number;
  color: string;
}

export interface SentimentSummary {
  score: number;
  trend: string;
  positive: number;
  negative: number;
  aiAccuracy: number;
}

export interface RiskLevels {
  high: { count: number; desc: string };
  medium: { count: number; desc: string };
  low: { count: number; desc: string };
}

export interface ReplyRecord {
  id: number;
  user: string;
  rating: number;
  content: string;
  reply: string;
  time: string;
  status: string;
}

export interface ReplyStats {
  todayCount: number;
  autoBlocked: number;
  avgTime: string;
}

export interface AppealSuggestion {
  id: string;
  user: string;
  platform: string;
  date: string;
  content: string;
  status: string;
  draft: string;
}

const BASE_URL = '/api';

async function fetchAPI<T>(endpoint: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${endpoint}`);
  if (!res.ok) throw new Error(`API 请求失败: ${res.status}`);
  return res.json();
}

/** 获取语义分析主题 GET /api/ai_analysis */
export async function fetchTopics(): Promise<Topic[]> {
  const data = await fetchAPI<any>('/ai_analysis');
  return data.topics || [];
}

/** 获取差评标签聚类 GET /api/ai_analysis */
export async function fetchTagClustering(): Promise<TagCluster[]> {
  const data = await fetchAPI<any>('/ai_analysis');
  return data.tagClustering || [];
}

/** 获取情感指数摘要 GET /api/ai_analysis */
export async function fetchSentimentSummary(): Promise<SentimentSummary> {
  const data = await fetchAPI<any>('/ai_analysis');
  return data.sentimentSummary || { score: 0, trend: '', positive: 0, negative: 0, aiAccuracy: 0 };
}

/** 获取风险分级 GET /api/ai_analysis */
export async function fetchRiskLevels(): Promise<RiskLevels> {
  const data = await fetchAPI<any>('/ai_analysis');
  return data.riskLevels || { high: { count: 0, desc: '' }, medium: { count: 0, desc: '' }, low: { count: 0, desc: '' } };
}

/** 获取 AI 洞察 GET /api/ai_analysis */
export async function fetchAIInsight(): Promise<string> {
  const data = await fetchAPI<any>('/ai_analysis');
  return data.insights || '';
}

/** 获取自动回复历史 GET /api/ai_analysis */
export async function fetchReplyHistory(): Promise<ReplyRecord[]> {
  const data = await fetchAPI<any>('/ai_analysis');
  return data.replyHistory || [];
}

/** 获取回复统计 GET /api/ai_analysis */
export async function fetchReplyStats(): Promise<ReplyStats> {
  const data = await fetchAPI<any>('/ai_analysis');
  return data.replyStats || { todayCount: 0, autoBlocked: 0, avgTime: '' };
}

/** 获取申诉建议 GET /api/ai_analysis */
export async function fetchAppealSuggestions(): Promise<AppealSuggestion[]> {
  const data = await fetchAPI<any>('/ai_analysis');
  return data.appealSuggestions || [];
}

import { api } from '@/lib/api';

const API_BASE = '/v1/admin/store-dashboard';

export interface StoreOption {
  id: string;
  name: string;
}

export interface RevenueRecord {
  id: string;
  store_id: string;
  store_name?: string;
  record_date: string;
  total_revenue: number;
  meituan_revenue: number;
  douyin_revenue: number;
  other_revenue: number;
  visitor_count: number;
  table_count: number;
  avg_people_per_table: number;
  avg_per_capita: number;
  notes?: string;
  created_at: string;
}

export interface PackageRecord {
  id: string;
  store_id: string;
  store_name?: string;
  period_start: string;
  period_end: string;
  product_name: string;
  meituan_buy: number;
  meituan_verify: number;
  douyin_buy: number;
  douyin_verify: number;
  notes?: string;
  created_at: string;
}

export interface StoreMetricRecord {
  id: string;
  store_id: string;
  store_name?: string;
  metric_date: string;
  platform: string;
  ranking_name?: string;
  ranking_position?: string;
  prev_ranking_position?: string;
  star_rating?: number;
  impressions?: number;
  visits?: number;
  purchases?: number;
  verifications?: number;
  new_favorites?: number;
  checkins?: number;
  scan_count?: number;
  product_impressions?: number;
  product_visits?: number;
  product_purchases?: number;
  new_reviews?: number;
  new_bad_reviews?: number;
  bad_keywords?: string[];
  notes?: string;
  created_at: string;
}

export interface OperationAnalysisRecord {
  id: string;
  store_id: string;
  store_name?: string;
  period_start: string;
  period_end: string;
  analysis_opinion: string;
  goals: string[];
  created_at: string;
}

export interface PaginatedResult<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

// ==================== 通用 ====================

export async function fetchStores(): Promise<StoreOption[]> {
  const res = await api.get<{ data: StoreOption[] }>(`${API_BASE}/stores`);
  return res?.data || [];
}

// ==================== 营业额 ====================

export async function fetchRevenueList(params?: Record<string, any>): Promise<PaginatedResult<RevenueRecord>> {
  const res = await api.get<any>(`${API_BASE}/revenue`, { params });
  const d = res?.data || res;
  return { items: d?.items || [], total: d?.total || 0, page: d?.page || 1, page_size: d?.page_size || 50 };
}

export async function createRevenue(data: any): Promise<any> {
  return api.post(`${API_BASE}/revenue`, data);
}

export async function batchCreateRevenue(records: any[]): Promise<any> {
  return api.post(`${API_BASE}/revenue/batch`, { records });
}

export async function updateRevenue(id: string, data: any): Promise<any> {
  return api.put(`${API_BASE}/revenue/${id}`, data);
}

export async function deleteRevenue(id: string): Promise<any> {
  return api.delete(`${API_BASE}/revenue/${id}`);
}

// ==================== 套餐核销 ====================

export async function fetchPackageList(params?: Record<string, any>): Promise<PaginatedResult<PackageRecord>> {
  const res = await api.get<any>(`${API_BASE}/packages`, { params });
  const d = res?.data || res;
  return { items: d?.items || [], total: d?.total || 0, page: d?.page || 1, page_size: d?.page_size || 50 };
}

export async function createPackage(data: any): Promise<any> {
  return api.post(`${API_BASE}/packages`, data);
}

export async function batchCreatePackages(records: any[]): Promise<any> {
  return api.post(`${API_BASE}/packages/batch`, { records });
}

export async function updatePackage(id: string, data: any): Promise<any> {
  return api.put(`${API_BASE}/packages/${id}`, data);
}

export async function deletePackage(id: string): Promise<any> {
  return api.delete(`${API_BASE}/packages/${id}`);
}

// ==================== 运营指标 ====================

export async function fetchMetricList(params?: Record<string, any>): Promise<PaginatedResult<StoreMetricRecord>> {
  const res = await api.get<any>(`${API_BASE}/metrics`, { params });
  const d = res?.data || res;
  return { items: d?.items || [], total: d?.total || 0, page: d?.page || 1, page_size: d?.page_size || 50 };
}

export async function createMetric(data: any): Promise<any> {
  return api.post(`${API_BASE}/metrics`, data);
}

export async function batchCreateMetrics(records: any[]): Promise<any> {
  return api.post(`${API_BASE}/metrics/batch`, { records });
}

export async function updateMetric(id: string, data: any): Promise<any> {
  return api.put(`${API_BASE}/metrics/${id}`, data);
}

export async function deleteMetric(id: string): Promise<any> {
  return api.delete(`${API_BASE}/metrics/${id}`);
}

// ==================== 运营分析 ====================

export async function fetchAnalysisList(params?: Record<string, any>): Promise<PaginatedResult<OperationAnalysisRecord>> {
  const res = await api.get<any>(`${API_BASE}/analysis`, { params });
  const d = res?.data || res;
  return { items: d?.items || [], total: d?.total || 0, page: d?.page || 1, page_size: d?.page_size || 50 };
}

export async function createAnalysis(data: any): Promise<any> {
  return api.post(`${API_BASE}/analysis`, data);
}

export async function updateAnalysis(id: string, data: any): Promise<any> {
  return api.put(`${API_BASE}/analysis/${id}`, data);
}

export async function deleteAnalysis(id: string): Promise<any> {
  return api.delete(`${API_BASE}/analysis/${id}`);
}

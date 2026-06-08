import { api } from '@/lib/api';

// ==================== 营业额与经营数据 ====================

export interface RevenueData {
  total_revenue: number;
  meituan_revenue: number;
  douyin_revenue: number;
  mom_change: number;
  mom_type: 'up' | 'down' | 'stable';
  period_label: string;
  compare_period_label: string;
}

export interface BusinessMetrics {
  visitor_count: number;
  table_count: number;
  avg_people_per_table: number;
  avg_per_capita: number;
  mom_visitor_change: number;
  mom_table_change: number;
}

// ==================== 套餐数据 ====================

export interface PackageItem {
  product_name: string;
  meituan_buy: number;
  meituan_verify: number;
  douyin_buy?: number;
  douyin_verify: number;
}

export interface PackagePeriodData {
  period_label: string;
  items: PackageItem[];
  total_meituan_buy: number;
  total_meituan_verify: number;
  total_douyin_verify: number;
}

export interface PackageComparison {
  store_name: string;
  current_period: PackagePeriodData;
  compare_period: PackagePeriodData | null;
}

// ==================== 运营分析 ====================

export interface OperationAnalysis {
  analysis_opinion: string;
  goals: string[];
}

// ==================== 运营指标对比 ====================

export interface MetricItem {
  name: string;
  current_value: string | number;
  compare_value: string | number | null;
  mom_change: string | number | null;
  highlight?: 'positive' | 'negative' | 'neutral';
}

export interface PlatformMetrics {
  platform: string;
  metrics: MetricItem[];
}

export interface OperationMetrics {
  meituan_metrics: MetricItem[];
  dianping_metrics: MetricItem[];
  douyin_metrics: MetricItem[];
}

// ==================== 完整看板数据 ====================

export interface StoreDashboardData {
  revenue: RevenueData;
  business_metrics: BusinessMetrics;
  package_comparison: PackageComparison | null;
  operation_analysis: OperationAnalysis | null;
  operation_metrics: OperationMetrics | null;
}

// ==================== 数据录入类型 ====================

export interface RevenueRecordInput {
  store_id: string;
  record_date: string;
  total_revenue: number;
  meituan_revenue: number;
  douyin_revenue: number;
  other_revenue?: number;
  visitor_count: number;
  table_count: number;
  avg_people_per_table: number;
  avg_per_capita: number;
  notes?: string;
}

export interface PackageRecordInput {
  store_id: string;
  period_start: string;
  period_end: string;
  product_name: string;
  meituan_buy: number;
  meituan_verify: number;
  douyin_buy?: number;
  douyin_verify: number;
  notes?: string;
}

export interface StoreMetricInput {
  store_id: string;
  metric_date: string;
  platform: string;
  ranking_name?: string;
  ranking_position?: string;
  prev_ranking_position?: string;
  star_rating?: number;
  prev_star_rating?: number;
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
}

export interface AnalysisInput {
  store_id: string;
  period_start: string;
  period_end: string;
  analysis_opinion: string;
  goals: string[];
}

// ==================== API 参数 ====================

export interface DashboardParams {
  store_id?: string;
  start_date?: string;
  end_date?: string;
  compare_start?: string;
  compare_end?: string;
}

// ==================== 辅助函数 ====================

const API_BASE = '/v1/store-dashboard';

/** 后端返回数据 → 前端格式 */
function mapRevenueData(raw: any): RevenueData {
  const change = raw.mom_revenue_change;
  return {
    total_revenue: raw.total_revenue || 0,
    meituan_revenue: raw.meituan_revenue || 0,
    douyin_revenue: raw.douyin_revenue || 0,
    mom_change: change ?? 0,
    mom_type: change === null || change === undefined ? 'stable' : change > 0 ? 'up' : change < 0 ? 'down' : 'stable',
    period_label: raw.period_label || '',
    compare_period_label: raw.compare_period_label || '',
  };
}

function mapBusinessMetrics(raw: any): BusinessMetrics {
  return {
    visitor_count: raw.visitor_count || 0,
    table_count: raw.table_count || 0,
    avg_people_per_table: raw.avg_people_per_table || 0,
    avg_per_capita: raw.avg_per_capita || 0,
    mom_visitor_change: raw.mom_visitor_change ?? 0,
    mom_table_change: raw.mom_table_change ?? 0,
  };
}

function mapPackagePeriod(raw: any): PackagePeriodData {
  return {
    period_label: raw.period_label || '',
    items: (raw.items || []).map((item: any) => ({
      product_name: item.product_name,
      meituan_buy: item.meituan_buy || 0,
      meituan_verify: item.meituan_verify || 0,
      douyin_buy: item.douyin_buy || 0,
      douyin_verify: item.douyin_verify || 0,
    })),
    total_meituan_buy: raw.total_meituan_buy || 0,
    total_meituan_verify: raw.total_meituan_verify || 0,
    total_douyin_verify: raw.total_douyin_verify || 0,
  };
}

// ==================== 看板查询 API ====================

/** 获取看板完整数据（聚合接口） */
export async function fetchStoreDashboard(params?: DashboardParams): Promise<StoreDashboardData> {
  const res = await api.get<any>(`${API_BASE}/overview`, { params });
  const data = res?.data || res;
  if (!data) {
    return getFallbackData();
  }
  return {
    revenue: mapRevenueData(data.revenue || {}),
    business_metrics: mapBusinessMetrics(data.business_metrics || {}),
    package_comparison: data.package_comparison ? {
      store_name: data.package_comparison.store_name || '',
      current_period: mapPackagePeriod(data.package_comparison.current_period || {}),
      compare_period: data.package_comparison.compare_period ? mapPackagePeriod(data.package_comparison.compare_period) : null,
    } : null,
    operation_analysis: data.operation_analysis ? {
      analysis_opinion: data.operation_analysis.analysis_opinion || '',
      goals: data.operation_analysis.goals || [],
    } : null,
    operation_metrics: data.operation_metrics || null,
  };
}

/** 获取营业额汇总 */
export async function fetchRevenueData(params?: DashboardParams): Promise<RevenueData> {
  const res = await api.get<any>(`${API_BASE}/revenue/summary`, { params });
  const data = res?.data || res;
  return data ? mapRevenueData(data) : getFallbackData().revenue;
}

/** 获取经营指标 */
export async function fetchBusinessMetrics(params?: DashboardParams): Promise<BusinessMetrics> {
  const res = await api.get<any>(`${API_BASE}/revenue/summary`, { params });
  const data = res?.data || res;
  return data ? mapBusinessMetrics(data) : getFallbackData().business_metrics;
}

/** 获取套餐对比数据 */
export async function fetchPackageComparison(params?: DashboardParams): Promise<PackageComparison | null> {
  if (!params?.start_date || !params?.end_date) {
    return getFallbackData().package_comparison;
  }
  const res = await api.get<any>(`${API_BASE}/packages/comparison`, {
    params: {
      current_start: params.start_date,
      current_end: params.end_date,
      compare_start: params.compare_start,
      compare_end: params.compare_end,
      store_id: params.store_id,
    },
  });
  const data = res?.data || res;
  if (!data) {
    return getFallbackData().package_comparison;
  }
  return {
    store_name: data.store_name || '',
    current_period: mapPackagePeriod(data.current_period || {}),
    compare_period: data.compare_period ? mapPackagePeriod(data.compare_period) : null,
  };
}

/** 获取运营分析 */
export async function fetchOperationAnalysis(params?: DashboardParams): Promise<OperationAnalysis | null> {
  const res = await api.get<any>(`${API_BASE}/analysis`, { params });
  const list = res?.data || res;
  if (Array.isArray(list) && list.length > 0) {
    return {
      analysis_opinion: list[0].analysis_opinion || '',
      goals: list[0].goals || [],
    };
  }
  return null;
}

// ==================== 数据录入 API ====================

/** 创建营业额记录 */
export async function createRevenueRecord(data: RevenueRecordInput) {
  return api.post(`${API_BASE}/revenue`, data);
}

/** 批量创建营业额记录 */
export async function batchCreateRevenueRecords(records: RevenueRecordInput[]) {
  return api.post(`${API_BASE}/revenue/batch`, { records });
}

/** 创建套餐核销记录 */
export async function createPackageRecord(data: PackageRecordInput) {
  return api.post(`${API_BASE}/packages`, data);
}

/** 批量创建套餐核销记录 */
export async function batchCreatePackageRecords(records: PackageRecordInput[]) {
  return api.post(`${API_BASE}/packages/batch`, { records });
}

/** 创建门店运营指标 */
export async function createStoreMetric(data: StoreMetricInput) {
  return api.post(`${API_BASE}/metrics`, data);
}

/** 批量创建门店运营指标 */
export async function batchCreateStoreMetrics(records: StoreMetricInput[]) {
  return api.post(`${API_BASE}/metrics/batch`, { records });
}

/** 创建运营分析 */
export async function createOperationAnalysis(data: AnalysisInput) {
  return api.post(`${API_BASE}/analysis`, data);
}

/** 更新营业额记录 */
export async function updateRevenueRecord(id: string, data: Partial<RevenueRecordInput>) {
  return api.put(`${API_BASE}/revenue/${id}`, data);
}

/** 删除营业额记录 */
export async function deleteRevenueRecord(id: string) {
  return api.delete(`${API_BASE}/revenue/${id}`);
}

/** 更新套餐核销记录 */
export async function updatePackageRecord(id: string, data: Partial<PackageRecordInput>) {
  return api.put(`${API_BASE}/packages/${id}`, data);
}

/** 删除套餐核销记录 */
export async function deletePackageRecord(id: string) {
  return api.delete(`${API_BASE}/packages/${id}`);
}

/** 更新运营指标 */
export async function updateStoreMetric(id: string, data: Partial<StoreMetricInput>) {
  return api.put(`${API_BASE}/metrics/${id}`, data);
}

/** 删除运营指标 */
export async function deleteStoreMetric(id: string) {
  return api.delete(`${API_BASE}/metrics/${id}`);
}

/** 更新运营分析 */
export async function updateOperationAnalysis(id: string, data: Partial<AnalysisInput>) {
  return api.put(`${API_BASE}/analysis/${id}`, data);
}

/** 删除运营分析 */
export async function deleteOperationAnalysis(id: string) {
  return api.delete(`${API_BASE}/analysis/${id}`);
}

// ==================== 数据查询 API ====================

/** 查询营业额记录列表 */
export async function listRevenueRecords(params?: {
  store_id?: string;
  start_date?: string;
  end_date?: string;
  page?: number;
  page_size?: number;
}) {
  return api.get(`${API_BASE}/revenue`, { params });
}

/** 查询套餐核销记录列表 */
export async function listPackageRecords(params?: {
  store_id?: string;
  period_start?: string;
  period_end?: string;
  page?: number;
  page_size?: number;
}) {
  return api.get(`${API_BASE}/packages`, { params });
}

/** 查询运营指标记录列表 */
export async function listStoreMetrics(params?: {
  store_id?: string;
  start_date?: string;
  end_date?: string;
  platform?: string;
  page?: number;
  page_size?: number;
}) {
  return api.get(`${API_BASE}/metrics`, { params });
}

// ==================== Fallback 数据 ====================

function getFallbackData(): StoreDashboardData {
  return {
    revenue: {
      total_revenue: 0,
      meituan_revenue: 0,
      douyin_revenue: 0,
      mom_change: 0,
      mom_type: 'stable',
      period_label: '',
      compare_period_label: '',
    },
    business_metrics: {
      visitor_count: 0,
      table_count: 0,
      avg_people_per_table: 0,
      avg_per_capita: 0,
      mom_visitor_change: 0,
      mom_table_change: 0,
    },
    package_comparison: {
      store_name: '',
      current_period: { period_label: '', items: [], total_meituan_buy: 0, total_meituan_verify: 0, total_douyin_verify: 0 },
      compare_period: null,
    },
    operation_analysis: null,
    operation_metrics: null,
  };
}

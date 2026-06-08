import { api } from '@/lib/api';

// ==================== 营业额与经营数据 ====================

export interface RevenueData {
  total_revenue: number;        // 总营业额
  meituan_revenue: number;      // 美团营业额
  douyin_revenue: number;       // 抖音营业额
  mom_change: number;           // 环比变化率 (%)
  mom_type: 'up' | 'down' | 'stable'; // 环比类型
  period_label: string;         // 当前周期标签
  compare_period_label: string; // 对比周期标签
}

export interface BusinessMetrics {
  visitor_count: number;        // 到店人数
  table_count: number;          // 接待桌数
  avg_people_per_table: number; // 桌均人数
  avg_per_capita: number;       // 人均消费
  mom_visitor_change: number;   // 到店人数环比
  mom_table_change: number;     // 桌数环比
}

// ==================== 套餐数据 ====================

export interface PackageItem {
  product_name: string;         // 商品名称
  meituan_buy: number;          // 美团购买
  meituan_verify: number;       // 美团核销券数
  douyin_verify: number;        // 抖音核销券数
}

export interface PackagePeriodData {
  period_label: string;         // 周期标签，如 "5.16-23号"
  items: PackageItem[];         // 套餐列表
  total_meituan_buy: number;    // 美团购买合计
  total_meituan_verify: number; // 美团核销合计
  total_douyin_verify: number;  // 抖音核销合计
}

export interface PackageComparison {
  store_name: string;           // 核销门店
  current_period: PackagePeriodData;  // 当期数据
  compare_period: PackagePeriodData;  // 对比期数据
}

// ==================== 运营分析 ====================

export interface OperationAnalysis {
  analysis_opinion: string;     // 分析意见
  next_week_goals: string[];    // 下周目标列表
  store_name: string;           // 门店名称
}

// ==================== 运营指标对比 ====================

export interface MetricItem {
  name: string;                 // 指标名称
  current_value: string | number;  // 当期值
  compare_value: string | number;  // 对比期值
  mom_change: string | number;     // 环比变化
  highlight?: 'positive' | 'negative' | 'neutral'; // 高亮类型
}

export interface PlatformMetrics {
  platform: string;             // 平台名称
  metrics: MetricItem[];        // 指标列表
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
  package_comparison: PackageComparison;
  operation_analysis: OperationAnalysis;
  operation_metrics: OperationMetrics;
}

// ==================== Mock 数据 ====================

const mockRevenueData: RevenueData = {
  total_revenue: 124580,
  meituan_revenue: 45680,
  douyin_revenue: 78900,
  mom_change: 43.4,
  mom_type: 'up',
  period_label: '5.25-31号',
  compare_period_label: '5.16-23号',
};

const mockBusinessMetrics: BusinessMetrics = {
  visitor_count: 1458,
  table_count: 486,
  avg_people_per_table: 3.0,
  avg_per_capita: 85.4,
  mom_visitor_change: 12.5,
  mom_table_change: 8.3,
};

const mockPackageComparison: PackageComparison = {
  store_name: '綦江爱琴海店',
  current_period: {
    period_label: '5.24-31号',
    items: [
      { product_name: '【牛牛爆款】鲜切4人餐', meituan_buy: 57, meituan_verify: 50, douyin_verify: 50 },
      { product_name: '【撸串搭子】当日现串2人餐', meituan_buy: 36, meituan_verify: 31, douyin_verify: 35 },
      { product_name: '【聚会首选】当日现串6-8人餐', meituan_buy: 13, meituan_verify: 12, douyin_verify: 8 },
      { product_name: '生蚝10个+荤串10串', meituan_buy: 6, meituan_verify: 5, douyin_verify: 5 },
      { product_name: '招牌广式猪杂粥（大份）', meituan_buy: 10, meituan_verify: 7, douyin_verify: 1 },
      { product_name: '招牌霸王大串3串', meituan_buy: 0, meituan_verify: 0, douyin_verify: 0 },
      { product_name: '招牌牛肉系列（10串）', meituan_buy: 8, meituan_verify: 7, douyin_verify: 2 },
      { product_name: '小朋友必点组合', meituan_buy: 4, meituan_verify: 3, douyin_verify: 1 },
      { product_name: '25元代金券', meituan_buy: 5, meituan_verify: 3, douyin_verify: 0 },
      { product_name: '50元代金券', meituan_buy: 6, meituan_verify: 6, douyin_verify: 0 },
    ],
    total_meituan_buy: 145,
    total_meituan_verify: 124,
    total_douyin_verify: 102,
  },
  compare_period: {
    period_label: '5.16-23号',
    items: [
      { product_name: '【牛牛爆款】鲜切4人餐', meituan_buy: 79, meituan_verify: 40, douyin_verify: 34 },
      { product_name: '【撸串搭子】当日现串2人套餐', meituan_buy: 56, meituan_verify: 32, douyin_verify: 13 },
      { product_name: '【聚会首选】当时现穿6-8人餐', meituan_buy: 10, meituan_verify: 0, douyin_verify: 5 },
      { product_name: '【超多"马"内】乳山生蚝10个+荤串10串', meituan_buy: 0, meituan_verify: 0, douyin_verify: 1 },
      { product_name: '招牌猪杂粥大份', meituan_buy: 7, meituan_verify: 2, douyin_verify: 0 },
      { product_name: '小朋友必点系列', meituan_buy: 1, meituan_verify: 0, douyin_verify: 0 },
      { product_name: '招牌牛肉系列10串', meituan_buy: 20, meituan_verify: 0, douyin_verify: 0 },
      { product_name: '25元代金券', meituan_buy: 2, meituan_verify: 2, douyin_verify: 0 },
      { product_name: '50元代金券', meituan_buy: 4, meituan_verify: 0, douyin_verify: 0 },
    ],
    total_meituan_buy: 179,
    total_meituan_verify: 76,
    total_douyin_verify: 53,
  },
};

const mockOperationAnalysis: OperationAnalysis = {
  store_name: '犇犇牛牛牛（大学城店）',
  analysis_opinion: '营业额上涨43.4%，抖音上涨47.87%，美团下滑54.5%，4人餐、2人餐下滑严重，会议后优化4人、2人餐营销工具。差评关键词：室内抽烟。',
  next_week_goals: [
    '每日评价：美团3条、点评1条、抖音1条',
    '差评率控制在3%',
    '每日扫码：1000元',
  ],
};

const mockOperationMetrics: OperationMetrics = {
  meituan_metrics: [
    { name: '美团人气榜榜单', current_value: '大学城烤串人气榜第1名', compare_value: '大学城烤串人气榜第1名', mom_change: '持平', highlight: 'neutral' },
    { name: '美团星级', current_value: '4.8', compare_value: '4.8', mom_change: '0%', highlight: 'neutral' },
    { name: '曝光次数', current_value: '55363', compare_value: '14037', mom_change: '+294%', highlight: 'positive' },
    { name: '访问次数', current_value: '5283', compare_value: '1718', mom_change: '+208%', highlight: 'positive' },
    { name: '曝光-访问转化率', current_value: '13.28%', compare_value: '12.19%', mom_change: '+9%', highlight: 'positive' },
    { name: '购买人数', current_value: '273', compare_value: '318', mom_change: '-14%', highlight: 'negative' },
    { name: '访问-购买转化率', current_value: '21.93%', compare_value: '17.88%', mom_change: '+23%', highlight: 'positive' },
    { name: '新增收藏人数', current_value: '20', compare_value: '13', mom_change: '+54%', highlight: 'positive' },
    { name: '打卡人数', current_value: '1', compare_value: '4', mom_change: '-75%', highlight: 'negative' },
    { name: '扫码人数', current_value: '143', compare_value: '132', mom_change: '+8%', highlight: 'positive' },
    { name: '商品曝光人数', current_value: '20338', compare_value: '20130', mom_change: '+1%', highlight: 'positive' },
    { name: '商品访问人数', current_value: '1785', compare_value: '2361', mom_change: '-24%', highlight: 'negative' },
    { name: '商品曝光-访问转化率', current_value: '8.78%', compare_value: '0', mom_change: '-28%', highlight: 'negative' },
    { name: '商品购买人数', current_value: '273', compare_value: '318', mom_change: '-14%', highlight: 'negative' },
    { name: '商品访问-购买转化率', current_value: '15.29%', compare_value: '0', mom_change: '+18%', highlight: 'positive' },
    { name: '新评价数', current_value: '33', compare_value: '46', mom_change: '-28%', highlight: 'negative' },
    { name: '新中差评数', current_value: '1', compare_value: '0', mom_change: '+100%', highlight: 'negative' },
  ],
  dianping_metrics: [
    { name: '点评热门榜榜单', current_value: '大学城烤串热门榜第2名', compare_value: '大学城烤串热门榜第2名', mom_change: '持平', highlight: 'neutral' },
    { name: '点评星级', current_value: '4.0', compare_value: '4.0', mom_change: '0%', highlight: 'neutral' },
  ],
  douyin_metrics: [
    { name: '抖音星级', current_value: '4.7', compare_value: '4.7', mom_change: '0%', highlight: 'neutral' },
    { name: '抖音人气榜榜单', current_value: '大学城烤串人气榜第6名', compare_value: '大学城烤串人气榜第6名', mom_change: '0%', highlight: 'neutral' },
    { name: '视频曝光', current_value: '/', compare_value: '/', mom_change: '/', highlight: 'neutral' },
    { name: '页面曝光人数', current_value: '753', compare_value: '670', mom_change: '+12%', highlight: 'positive' },
    { name: '页面访问人数', current_value: '564', compare_value: '483', mom_change: '+17%', highlight: 'positive' },
    { name: '购买人数', current_value: '105', compare_value: '88', mom_change: '+19%', highlight: 'positive' },
    { name: '核销人数', current_value: '72', compare_value: '64', mom_change: '+13%', highlight: 'positive' },
  ],
};

// ==================== API 函数 ====================

export interface DashboardParams {
  store_id?: string;
  period_type?: 'week' | 'custom';
  start_date?: string;
  end_date?: string;
  compare_start_date?: string;
  compare_end_date?: string;
}

/** 获取看板完整数据 */
export async function fetchStoreDashboard(params?: DashboardParams): Promise<StoreDashboardData> {
  // TODO: 接入真实 API
  // const response = await api.get<any>('/v1/store/dashboard', { params });
  // return response.data || response;

  // 返回 mock 数据
  await new Promise(r => setTimeout(r, 300));
  return {
    revenue: mockRevenueData,
    business_metrics: mockBusinessMetrics,
    package_comparison: mockPackageComparison,
    operation_analysis: mockOperationAnalysis,
    operation_metrics: mockOperationMetrics,
  };
}

/** 获取营业额数据 */
export async function fetchRevenueData(params?: DashboardParams): Promise<RevenueData> {
  await new Promise(r => setTimeout(r, 200));
  return mockRevenueData;
}

/** 获取经营指标 */
export async function fetchBusinessMetrics(params?: DashboardParams): Promise<BusinessMetrics> {
  await new Promise(r => setTimeout(r, 200));
  return mockBusinessMetrics;
}

/** 获取套餐对比数据 */
export async function fetchPackageComparison(params?: DashboardParams): Promise<PackageComparison> {
  await new Promise(r => setTimeout(r, 200));
  return mockPackageComparison;
}

/** 获取运营分析 */
export async function fetchOperationAnalysis(params?: DashboardParams): Promise<OperationAnalysis> {
  await new Promise(r => setTimeout(r, 200));
  return mockOperationAnalysis;
}

/** 获取运营指标 */
export async function fetchOperationMetrics(params?: DashboardParams): Promise<OperationMetrics> {
  await new Promise(r => setTimeout(r, 200));
  return mockOperationMetrics;
}

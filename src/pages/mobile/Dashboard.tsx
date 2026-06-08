import React, { useState, useEffect, useCallback } from 'react';
import {
  TrendingUp,
  TrendingDown,
  Minus,
  Calendar,
  ChevronDown,
  ChevronRight,
  Store,
  Users,
  UtensilsCrossed,
  UserRound,
  Wallet,
  Package,
  BarChart3,
  Target,
  Lightbulb,
  CheckCircle2,
  ArrowUpRight,
  ArrowDownRight,
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { Skeleton } from '../../components/ui/skeleton';
import { Button } from '../../components/ui/button';
import { MobileLayout } from '../../components/MobileLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';
import {
  fetchStoreDashboard,
  type StoreDashboardData,
  type RevenueData,
  type BusinessMetrics,
  type PackageComparison,
  type OperationAnalysis,
  type OperationMetrics,
  type MetricItem,
} from '../../api/store-dashboard';

// ==================== 时间周期选项 ====================

interface TimeOption {
  value: string;
  label: string;
  dateRange: string;
}

function getWeekOptions(): TimeOption[] {
  const now = new Date();
  const formatDate = (d: Date) => `${d.getMonth() + 1}.${d.getDate()}`;
  const getWeekRange = (weeksAgo: number) => {
    const end = new Date(now.getTime() - weeksAgo * 7 * 86400000);
    const start = new Date(end.getTime() - 6 * 86400000);
    return { start, end, label: formatDate(start) + '-' + formatDate(end) };
  };
  return [
    { value: 'current', label: '本周', dateRange: getWeekRange(0).label },
    { value: 'last', label: '上周', dateRange: getWeekRange(1).label },
    { value: 'week2', label: '两周前', dateRange: getWeekRange(2).label },
    { value: 'week3', label: '三周前', dateRange: getWeekRange(3).label },
  ];
}

// ==================== 子组件：营业额卡片 ====================

const RevenueCard: React.FC<{ data: RevenueData }> = ({ data }) => {
  const formatMoney = (n: number) => `¥${n.toLocaleString()}`;

  return (
    <Card className="p-4 bg-white border-slate-100 shadow-sm">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-orange-50 flex items-center justify-center">
            <Wallet className="w-4 h-4 text-orange-500" />
          </div>
          <span className="text-sm font-bold text-slate-700">营业额概览</span>
        </div>
        <Badge className={cn(
          "text-[10px] border-none",
          data.mom_type === 'up' ? "bg-emerald-50 text-emerald-600" :
          data.mom_type === 'down' ? "bg-rose-50 text-rose-600" :
          "bg-slate-50 text-slate-600"
        )}>
          环比 {data.mom_type === 'up' ? '+' : data.mom_type === 'down' ? '' : ''}{data.mom_change}%
        </Badge>
      </div>

      {/* 总营业额 */}
      <div className="mb-4">
        <p className="text-[10px] text-slate-400 mb-1">总营业额</p>
        <div className="flex items-baseline gap-2">
          <p className="text-3xl font-black text-slate-900">{formatMoney(data.total_revenue)}</p>
          {data.mom_type === 'up' ? (
            <span className="flex items-center gap-0.5 text-xs font-bold text-emerald-500">
              <TrendingUp className="w-3.5 h-3.5" />+{data.mom_change}%
            </span>
          ) : data.mom_type === 'down' ? (
            <span className="flex items-center gap-0.5 text-xs font-bold text-rose-500">
              <TrendingDown className="w-3.5 h-3.5" />{data.mom_change}%
            </span>
          ) : (
            <span className="flex items-center gap-0.5 text-xs font-bold text-slate-400">
              <Minus className="w-3.5 h-3.5" />持平
            </span>
          )}
        </div>
      </div>

      {/* 分平台 */}
      <div className="grid grid-cols-2 gap-3">
        <div className="bg-slate-50 rounded-xl p-3">
          <div className="flex items-center gap-1.5 mb-1">
            <div className="w-5 h-5 rounded bg-yellow-400 flex items-center justify-center">
              <span className="text-[8px] font-bold text-white">美</span>
            </div>
            <span className="text-[10px] text-slate-500">美团</span>
          </div>
          <p className="text-lg font-bold text-slate-900">{formatMoney(data.meituan_revenue)}</p>
          <p className="text-[9px] text-slate-400 mt-0.5">
            占比 {((data.meituan_revenue / data.total_revenue) * 100).toFixed(1)}%
          </p>
        </div>
        <div className="bg-slate-50 rounded-xl p-3">
          <div className="flex items-center gap-1.5 mb-1">
            <div className="w-5 h-5 rounded bg-slate-900 flex items-center justify-center">
              <span className="text-[8px] font-bold text-white">抖</span>
            </div>
            <span className="text-[10px] text-slate-500">抖音</span>
          </div>
          <p className="text-lg font-bold text-slate-900">{formatMoney(data.douyin_revenue)}</p>
          <p className="text-[9px] text-slate-400 mt-0.5">
            占比 {((data.douyin_revenue / data.total_revenue) * 100).toFixed(1)}%
          </p>
        </div>
      </div>
    </Card>
  );
};

// ==================== 子组件：经营指标卡片 ====================

const BusinessMetricsCard: React.FC<{ data: BusinessMetrics }> = ({ data }) => {
  const metrics = [
    { label: '到店人数', value: data.visitor_count.toLocaleString(), icon: Users, color: 'text-blue-500', bg: 'bg-blue-50', mom: data.mom_visitor_change },
    { label: '接待桌数', value: data.table_count.toLocaleString(), icon: UtensilsCrossed, color: 'text-purple-500', bg: 'bg-purple-50', mom: data.mom_table_change },
    { label: '桌均人数', value: data.avg_people_per_table.toFixed(1), icon: UserRound, color: 'text-amber-500', bg: 'bg-amber-50', mom: null },
    { label: '人均消费', value: `¥${data.avg_per_capita.toFixed(1)}`, icon: Wallet, color: 'text-emerald-500', bg: 'bg-emerald-50', mom: null },
  ];

  return (
    <Card className="p-4 bg-white border-slate-100 shadow-sm">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center">
          <BarChart3 className="w-4 h-4 text-blue-500" />
        </div>
        <span className="text-sm font-bold text-slate-700">经营指标</span>
      </div>
      <div className="grid grid-cols-2 gap-3">
        {metrics.map((m) => (
          <div key={m.label} className="bg-slate-50 rounded-xl p-3">
            <div className="flex items-center gap-1.5 mb-2">
              <div className={cn("w-6 h-6 rounded-lg flex items-center justify-center", m.bg)}>
                <m.icon className={cn("w-3.5 h-3.5", m.color)} />
              </div>
              <span className="text-[10px] text-slate-500">{m.label}</span>
            </div>
            <p className="text-xl font-bold text-slate-900">{m.value}</p>
            {m.mom !== null && (
              <p className={cn(
                "text-[9px] mt-0.5 font-medium",
                m.mom >= 0 ? "text-emerald-500" : "text-rose-500"
              )}>
                {m.mom >= 0 ? '+' : ''}{m.mom}% 环比
              </p>
            )}
          </div>
        ))}
      </div>
    </Card>
  );
};

// ==================== 子组件：套餐数据表格 ====================

const PackageTable: React.FC<{ data: PackageComparison }> = ({ data }) => {
  const [expanded, setExpanded] = useState(true);

  const current = data.current_period;
  const compare = data.compare_period;

  // 对齐两个周期的商品（按名称匹配）
  const allNames = Array.from(new Set([
    ...current.items.map(i => i.product_name),
    ...compare.items.map(i => i.product_name),
  ]));

  return (
    <Card className="bg-white border-slate-100 shadow-sm overflow-hidden">
      <div
        className="p-4 flex items-center justify-between cursor-pointer"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-indigo-50 flex items-center justify-center">
            <Package className="w-4 h-4 text-indigo-500" />
          </div>
          <div>
            <span className="text-sm font-bold text-slate-700">套餐核销数据</span>
            <p className="text-[9px] text-slate-400">{data.store_name}</p>
          </div>
        </div>
        <ChevronDown className={cn("w-5 h-5 text-slate-400 transition-transform", expanded && "rotate-180")} />
      </div>

      {expanded && (
        <div className="px-4 pb-4">
          {/* 表头 */}
          <div className="overflow-x-auto -mx-4 px-4">
            <table className="w-full text-[10px] border-collapse">
              <thead>
                <tr className="bg-slate-50">
                  <th className="p-2 text-left text-slate-500 font-medium rounded-tl-lg w-[120px]">商品名称</th>
                  <th className="p-2 text-center text-slate-500 font-medium" colSpan={3}>
                    <span className="text-orange-600">{compare.period_label}</span>
                  </th>
                  <th className="p-2 text-center text-slate-500 font-medium rounded-tr-lg" colSpan={3}>
                    <span className="text-indigo-600">{current.period_label}</span>
                  </th>
                </tr>
                <tr className="bg-slate-50">
                  <th className="p-1.5 text-left"></th>
                  <th className="p-1.5 text-center text-slate-400 font-normal">美团购买</th>
                  <th className="p-1.5 text-center text-slate-400 font-normal">美团核销</th>
                  <th className="p-1.5 text-center text-slate-400 font-normal">抖音核销</th>
                  <th className="p-1.5 text-center text-slate-400 font-normal">美团购买</th>
                  <th className="p-1.5 text-center text-slate-400 font-normal">美团核销</th>
                  <th className="p-1.5 text-center text-slate-400 font-normal">抖音核销</th>
                </tr>
              </thead>
              <tbody>
                {allNames.map((name, idx) => {
                  const cItem = compare.items.find(i => i.product_name === name);
                  const curItem = current.items.find(i => i.product_name === name);
                  return (
                    <tr key={idx} className={cn("border-b border-slate-100", idx % 2 === 0 ? "bg-white" : "bg-slate-50/50")}>
                      <td className="p-2 text-slate-700 font-medium leading-tight">{name}</td>
                      <td className="p-1.5 text-center text-slate-600">{cItem?.meituan_buy ?? 0}</td>
                      <td className="p-1.5 text-center text-slate-600">{cItem?.meituan_verify ?? 0}</td>
                      <td className="p-1.5 text-center text-slate-600">{cItem?.douyin_verify ?? 0}</td>
                      <td className="p-1.5 text-center text-slate-600 font-medium">{curItem?.meituan_buy ?? 0}</td>
                      <td className="p-1.5 text-center text-slate-600 font-medium">{curItem?.meituan_verify ?? 0}</td>
                      <td className="p-1.5 text-center text-slate-600 font-medium">{curItem?.douyin_verify ?? 0}</td>
                    </tr>
                  );
                })}
                {/* 合计行 */}
                <tr className="bg-orange-50 font-bold">
                  <td className="p-2 text-orange-700">合计</td>
                  <td className="p-1.5 text-center text-orange-700">{compare.total_meituan_buy}</td>
                  <td className="p-1.5 text-center text-orange-700">{compare.total_meituan_verify}</td>
                  <td className="p-1.5 text-center text-orange-700">{compare.total_douyin_verify}</td>
                  <td className="p-1.5 text-center text-orange-700">{current.total_meituan_buy}</td>
                  <td className="p-1.5 text-center text-orange-700">{current.total_meituan_verify}</td>
                  <td className="p-1.5 text-center text-orange-700">{current.total_douyin_verify}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}
    </Card>
  );
};

// ==================== 子组件：运营分析 ====================

const AnalysisCard: React.FC<{ data: OperationAnalysis }> = ({ data }) => {
  return (
    <Card className="p-4 bg-white border-slate-100 shadow-sm">
      <div className="flex items-center gap-2 mb-3">
        <div className="w-8 h-8 rounded-lg bg-emerald-50 flex items-center justify-center">
          <Lightbulb className="w-4 h-4 text-emerald-500" />
        </div>
        <span className="text-sm font-bold text-slate-700">运营分析</span>
      </div>

      {/* 分析意见 */}
      <div className="mb-4">
        <div className="flex items-center gap-1.5 mb-2">
          <BarChart3 className="w-3.5 h-3.5 text-orange-500" />
          <span className="text-xs font-bold text-slate-700">分析意见</span>
        </div>
        <div className="bg-slate-50 rounded-xl p-3">
          <p className="text-xs text-slate-600 leading-relaxed">{data.analysis_opinion}</p>
        </div>
      </div>

      {/* 下周目标 */}
      <div>
        <div className="flex items-center gap-1.5 mb-2">
          <Target className="w-3.5 h-3.5 text-indigo-500" />
          <span className="text-xs font-bold text-slate-700">下周目标</span>
        </div>
        <div className="space-y-2">
          {data.next_week_goals.map((goal, idx) => (
            <div key={idx} className="flex items-start gap-2 bg-indigo-50 rounded-xl p-3">
              <CheckCircle2 className="w-4 h-4 text-indigo-500 flex-shrink-0 mt-0.5" />
              <p className="text-xs text-slate-700 leading-relaxed">{goal}</p>
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
};

// ==================== 子组件：指标对比表格 ====================

const MetricsTable: React.FC<{ metrics: MetricItem[]; platformName: string; platformColor: string }> = ({
  metrics,
  platformName,
  platformColor,
}) => {
  const [expanded, setExpanded] = useState(true);

  const getHighlightClass = (h?: string) => {
    if (h === 'positive') return 'text-emerald-600 font-bold';
    if (h === 'negative') return 'text-rose-600 font-bold';
    return 'text-slate-600';
  };

  return (
    <Card className="bg-white border-slate-100 shadow-sm overflow-hidden">
      <div
        className="p-4 flex items-center justify-between cursor-pointer"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center gap-2">
          <div className={cn("w-8 h-8 rounded-lg flex items-center justify-center", platformColor)}>
            <BarChart3 className="w-4 h-4 text-white" />
          </div>
          <span className="text-sm font-bold text-slate-700">{platformName}</span>
        </div>
        <ChevronDown className={cn("w-5 h-5 text-slate-400 transition-transform", expanded && "rotate-180")} />
      </div>

      {expanded && (
        <div className="px-4 pb-4">
          <div className="overflow-x-auto -mx-4 px-4">
            <table className="w-full text-[11px] border-collapse">
              <thead>
                <tr className="bg-slate-50">
                  <th className="p-2 text-left text-slate-500 font-medium rounded-tl-lg">项目</th>
                  <th className="p-2 text-center text-slate-500 font-medium">上期</th>
                  <th className="p-2 text-center text-slate-500 font-medium">本期</th>
                  <th className="p-2 text-center text-slate-500 font-medium rounded-tr-lg">环比</th>
                </tr>
              </thead>
              <tbody>
                {metrics.map((m, idx) => (
                  <tr key={idx} className={cn("border-b border-slate-100", idx % 2 === 0 ? "bg-white" : "bg-slate-50/50")}>
                    <td className="p-2 text-slate-700 font-medium whitespace-nowrap">{m.name}</td>
                    <td className="p-2 text-center text-slate-500">{m.compare_value}</td>
                    <td className="p-2 text-center text-slate-700 font-medium">{m.current_value}</td>
                    <td className={cn("p-2 text-center", getHighlightClass(m.highlight))}>
                      {typeof m.mom_change === 'string' && (m.mom_change as string).startsWith('+') ? (
                        <span className="flex items-center justify-center gap-0.5">
                          <ArrowUpRight className="w-3 h-3" />{m.mom_change}
                        </span>
                      ) : typeof m.mom_change === 'string' && (m.mom_change as string).startsWith('-') ? (
                        <span className="flex items-center justify-center gap-0.5">
                          <ArrowDownRight className="w-3 h-3" />{m.mom_change}
                        </span>
                      ) : (
                        m.mom_change
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </Card>
  );
};

// ==================== 主页面 ====================

export const Dashboard: React.FC = () => {
  const { success } = useToast();
  const [timePeriod, setTimePeriod] = useState('current');
  const [showTimeDropdown, setShowTimeDropdown] = useState(false);
  const dropdownRef = React.useRef<HTMLDivElement>(null);
  const timeOptions = React.useMemo(() => getWeekOptions(), []);

  const [data, setData] = useState<StoreDashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await fetchStoreDashboard({ period_type: 'week' });
      setData(result);
    } catch (err) {
      console.error('[Dashboard] 获取数据失败:', err);
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally {
      setLoading(false);
    }
  }, [timePeriod]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowTimeDropdown(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleTimeChange = (value: string) => {
    setTimePeriod(value);
    setShowTimeDropdown(false);
    const label = timeOptions.find(o => o.value === value)?.label;
    success('时间筛选', `已切换到${label}`);
  };

  const getCurrentDateRange = () => {
    return timeOptions.find(opt => opt.value === timePeriod)?.dateRange || '';
  };

  // ===== 加载状态 =====
  if (loading) {
    return (
      <MobileLayout title="经营看板">
        <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500 p-4">
          <Skeleton lines={1} className="h-8 w-48 mb-4" />
          <Card className="p-5">
            <Skeleton lines={1} className="h-8 w-32 mb-4" />
            <Skeleton lines={3} className="space-y-2" />
          </Card>
          <Skeleton card className="mt-4" />
          <Skeleton lines={5} className="mt-4 space-y-3" />
        </div>
      </MobileLayout>
    );
  }

  // ===== 错误状态 =====
  if (error || !data) {
    return (
      <MobileLayout title="经营看板">
        <div className="p-4">
          <Card className="p-6 text-center">
            <p className="text-sm text-slate-600 mb-4">{error || '暂无数据'}</p>
            <Button onClick={() => fetchData()} className="bg-orange-500 hover:bg-orange-600 text-white">
              重试
            </Button>
          </Card>
        </div>
      </MobileLayout>
    );
  }

  return (
    <MobileLayout title="经营看板">
      <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500 pb-20">

        {/* 时间筛选 */}
        <div className="relative" ref={dropdownRef}>
          <div className="flex items-center justify-between bg-white p-3 rounded-2xl shadow-sm border border-slate-100">
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-slate-400" />
              <span className="text-sm font-medium text-slate-600">{getCurrentDateRange()}</span>
            </div>
            <Button
              variant="ghost"
              size="sm"
              className="h-8 text-orange-600 font-semibold gap-1"
              onClick={() => setShowTimeDropdown(!showTimeDropdown)}
            >
              {timeOptions.find(opt => opt.value === timePeriod)?.label}
              <ChevronDown className={cn("w-3.5 h-3.5 transition-transform", showTimeDropdown && "rotate-180")} />
            </Button>
          </div>

          {showTimeDropdown && (
            <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-2xl shadow-lg border border-slate-100 z-50 overflow-hidden animate-in fade-in slide-in-from-top-2 duration-200">
              {timeOptions.map((option) => (
                <button
                  key={option.value}
                  className={cn(
                    "w-full px-4 py-3 text-left text-sm font-medium transition-colors flex items-center justify-between",
                    timePeriod === option.value
                      ? "bg-orange-50 text-orange-600"
                      : "text-slate-700 hover:bg-slate-50"
                  )}
                  onClick={() => handleTimeChange(option.value)}
                >
                  <span>{option.label}</span>
                  <span className="text-[10px] text-slate-400">{option.dateRange}</span>
                  {timePeriod === option.value && (
                    <CheckCircle2 className="w-4 h-4 text-orange-600" />
                  )}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* 营业额概览 */}
        <RevenueCard data={data.revenue} />

        {/* 经营指标 */}
        <BusinessMetricsCard data={data.business_metrics} />

        {/* 套餐核销数据 */}
        <PackageTable data={data.package_comparison} />

        {/* 运营分析 */}
        <AnalysisCard data={data.operation_analysis} />

        {/* 运营指标对比 - 美团 */}
        <MetricsTable
          metrics={data.operation_metrics.meituan_metrics}
          platformName="美团数据"
          platformColor="bg-yellow-400"
        />

        {/* 运营指标对比 - 点评 */}
        <MetricsTable
          metrics={data.operation_metrics.dianping_metrics}
          platformName="点评数据"
          platformColor="bg-orange-500"
        />

        {/* 运营指标对比 - 抖音 */}
        <MetricsTable
          metrics={data.operation_metrics.douyin_metrics}
          platformName="抖音数据"
          platformColor="bg-slate-900"
        />

      </div>
    </MobileLayout>
  );
};

import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  TrendingUp,
  TrendingDown,
  Calendar,
  ChevronDown,
  Wallet,
  Users,
  UtensilsCrossed,
  UserRound,
  Package,
  BarChart3,
  Store as StoreIcon,
  ChevronRight,
  CheckCircle2,
  RefreshCw,
  Zap,
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { Skeleton } from '../../components/ui/skeleton';
import { Button } from '../../components/ui/button';
import { MobileLayout, useStore } from '../../components/MobileLayout';
import type { Store } from '../../api/stores';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';
import {
  fetchStoreDashboard,
  syncDashboard,
  type StoreDashboardData,
  type RevenueData,
  type BusinessMetrics,
} from '../../api/store-dashboard';

// ==================== 时间周期 ====================

interface TimeOption { value: string; label: string; dateRange: string; startDate: string; endDate: string; }

function getWeekOptions(): TimeOption[] {
  const now = new Date();
  const formatDate = (d: Date) => `${d.getMonth() + 1}.${d.getDate()}`;
  const toISO = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  const getWeekRange = (weeksAgo: number) => {
    // 计算N周前的周一到周日
    const ref = new Date(now.getTime() - weeksAgo * 7 * 86400000);
    const dayOfWeek = ref.getDay() || 7; // 周日=7
    const monday = new Date(ref.getTime() - (dayOfWeek - 1) * 86400000);
    const sunday = new Date(monday.getTime() + 6 * 86400000);
    return { label: formatDate(monday) + '-' + formatDate(sunday), startDate: toISO(monday), endDate: toISO(sunday) };
  };
  return [
    { value: 'current', label: '本周', dateRange: getWeekRange(0).label, startDate: getWeekRange(0).startDate, endDate: getWeekRange(0).endDate },
    { value: 'last', label: '上周', dateRange: getWeekRange(1).label, startDate: getWeekRange(1).startDate, endDate: getWeekRange(1).endDate },
    { value: 'week2', label: '两周前', dateRange: getWeekRange(2).label, startDate: getWeekRange(2).startDate, endDate: getWeekRange(2).endDate },
    { value: 'week3', label: '三周前', dateRange: getWeekRange(3).label, startDate: getWeekRange(3).startDate, endDate: getWeekRange(3).endDate },
  ];
}

// ==================== 主页面 ====================

export const Dashboard: React.FC = () => {
  const { success } = useToast();
  const navigate = useNavigate();
  const { selectedStore } = useStore();
  const [timePeriod, setTimePeriodState] = useState(() => localStorage.getItem('zc_time_period') || 'current');
  const [showTimeDropdown, setShowTimeDropdown] = useState(false);
  const dropdownRef = React.useRef<HTMLDivElement>(null);
  const timeOptions = React.useMemo(() => getWeekOptions(), []);

  const setTimePeriod = (value: string) => {
    setTimePeriodState(value);
    localStorage.setItem('zc_time_period', value);
  };

  const [data, setData] = useState<StoreDashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [syncing, setSyncing] = useState(false);
  const [syncResult, setSyncResult] = useState<string | null>(null);

  // 获取当前选中的门店ID
  const getEffectiveStoreId = useCallback(() => {
    return selectedStore?.id || localStorage.getItem('zc_selected_store_id') || undefined;
  }, [selectedStore?.id]);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const idx = timeOptions.findIndex(o => o.value === timePeriod);
      const option = timeOptions[idx];
      const prevOption = idx < timeOptions.length - 1 ? timeOptions[idx + 1] : null;
      const storeId = getEffectiveStoreId();
      const result = await fetchStoreDashboard({
        store_id: storeId,
        start_date: option?.startDate,
        end_date: option?.endDate,
        compare_start: prevOption?.startDate,
        compare_end: prevOption?.endDate,
      });
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally {
      setLoading(false);
    }
  }, [timePeriod, timeOptions, getEffectiveStoreId]);

  // 店铺变化或时间变化都触发重新请求
  useEffect(() => { fetchData(); }, [fetchData]);

  // 监听 zc-store-changed 自定义事件（双重保险）
  useEffect(() => {
    const handler = (e: CustomEvent<Store>) => {
      const storeFromEvent = e.detail;
      console.log('[Dashboard] zc-store-changed event:', storeFromEvent?.name, storeFromEvent?.id);
      if (storeFromEvent?.id) {
        // 事件触发后 selectedStore 会更新，fetchData 会自动重跑
        // 这里作为兜底，确保即使 React 状态更新有延迟也能响应
      }
    };
    window.addEventListener('zc-store-changed', handler as any);
    return () => window.removeEventListener('zc-store-changed', handler as any);
  }, []);

  // 监听数据分析页面时间切换事件，保持双向同步
  useEffect(() => {
    const handler = (e: CustomEvent<string>) => {
      setTimePeriod(e.detail);
    };
    window.addEventListener('zc-time-period-changed', handler as any);
    return () => window.removeEventListener('zc-time-period-changed', handler as any);
  }, []);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) setShowTimeDropdown(false);
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const handleTimeChange = (value: string) => {
    setTimePeriod(value);
    setShowTimeDropdown(false);
    success('时间筛选', `已切换到${timeOptions.find(o => o.value === value)?.label}`);
    window.dispatchEvent(new CustomEvent('zc-time-period-changed', { detail: value }));
  };

  // ===== 同步仪表盘数据 =====
  const handleSyncDashboard = async () => {
    if (syncing) return;
    setSyncing(true);
    setSyncResult(null);

    try {
      const idx = timeOptions.findIndex(o => o.value === timePeriod);
      const option = timeOptions[idx];
      const storeId = getEffectiveStoreId();

      setSyncResult('🔄 正在启动浏览器环境同步数据，预计需要 30-120 秒...');
      console.log('[Dashboard] 🚀 开始同步仪表盘数据', { storeId, startDate: option?.startDate, endDate: option?.endDate });

      const result = await syncDashboard({
        store_id: storeId,
        start_date: option?.startDate,
        end_date: option?.endDate,
      });

      console.log('[Dashboard] 📊 同步结果:', result);

      if (result.success) {
        const summary = result.summary;
        const details: string[] = [];
        for (const r of result.results) {
          if (r.success) {
            details.push(`${r.platform === 'meituan' ? '美团' : '抖音'}: 营业额${r.revenue_records || 0}条, 指标${r.metric_records || 0}条${r.package_records ? `, 套餐${r.package_records}条` : ''}`);
          } else {
            details.push(`${r.platform === 'meituan' ? '美团' : '抖音'}: ❌ ${r.error || '同步失败'}`);
          }
        }
        setSyncResult(`✅ ${details.join(' | ')}`);
        console.log('[Dashboard] ✅ 同步成功详情:', details);
        success('同步完成', `已从${summary?.platforms_synced || 0}个平台同步数据`);
        // 重新加载看板数据
        await fetchData();
      } else {
        const errMsg = result.error || '同步失败';
        setSyncResult(`❌ ${errMsg}`);
        console.error('[Dashboard] ❌ 同步失败:', errMsg, result);
      }
    } catch (err) {
      const errMsg = err instanceof Error ? err.message : '同步异常';
      setSyncResult(`❌ ${errMsg}`);
      console.error('[Dashboard] ❌ 同步异常:', err);
    } finally {
      setSyncing(false);
    }
  };

  // ===== 快捷入口卡片 =====
  const quickActions = [
    { label: '营业额分析', desc: '趋势/渠道/客流', icon: Wallet, color: 'bg-orange-500', path: '/mobile/data-analysis?tab=revenue' },
    { label: '套餐分析', desc: '核销率/爆款', icon: Package, color: 'bg-indigo-500', path: '/mobile/data-analysis?tab=package' },
    { label: '门店分析', desc: '流量/转化/评价', icon: StoreIcon, color: 'bg-emerald-500', path: '/mobile/data-analysis?tab=store' },
    { label: '生成报告', desc: '周报/月报', icon: BarChart3, color: 'bg-purple-500', path: '/mobile/report' },
  ];

  // ===== 加载 =====
  if (loading) {
    return (
      <MobileLayout title="经营看板">
        <div className="p-4 space-y-4">
          <Skeleton lines={1} className="h-8 w-48 mb-4" />
          <div className="grid grid-cols-2 gap-3">
            {[1,2,3,4].map(i => <Skeleton key={i} card className="h-28" />)}
          </div>
          <div className="grid grid-cols-2 gap-3 mt-2">
            {[1,2,3,4].map(i => <Skeleton key={i} card className="h-24" />)}
          </div>
        </div>
      </MobileLayout>
    );
  }

  if (error || !data) {
    return (
      <MobileLayout title="经营看板">
        <div className="p-4">
          <Card className="p-6 text-center">
            <p className="text-sm text-slate-600 mb-2">{error || '暂无数据'}</p>
            <p className="text-xs text-slate-400 mb-4">请确认已选择正确的门店和时间范围</p>
            <Button onClick={() => fetchData()} className="bg-orange-500 hover:bg-orange-600 text-white">重试</Button>
          </Card>
        </div>
      </MobileLayout>
    );
  }

  const rev = data.revenue;
  const bm = data.business_metrics;
  const formatMoney = (n: number) => `¥${n.toLocaleString()}`;

  return (
    <MobileLayout title="经营看板">
      <div className="pb-20 space-y-4">

        {/* 时间筛选 + 同步按钮 */}
        <div className="relative" ref={dropdownRef}>
          <div className="flex items-center gap-2">
            <div className="flex-1 flex items-center justify-between bg-white p-3 rounded-2xl shadow-sm border border-slate-100">
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4 text-slate-400" />
                <span className="text-sm font-medium text-slate-600">
                  {timeOptions.find(opt => opt.value === timePeriod)?.dateRange}
                </span>
              </div>
              <Button variant="ghost" size="sm" className="h-8 text-orange-600 font-semibold gap-1"
                onClick={() => setShowTimeDropdown(!showTimeDropdown)}>
                {timeOptions.find(opt => opt.value === timePeriod)?.label}
                <ChevronDown className={cn("w-3.5 h-3.5 transition-transform", showTimeDropdown && "rotate-180")} />
              </Button>
            </div>
            <Button
              variant="outline"
              size="sm"
              className={cn("h-12 w-12 rounded-2xl border-orange-200 flex-shrink-0", syncing && "animate-spin")}
              onClick={handleSyncDashboard}
              disabled={syncing}
              title="同步平台数据"
            >
              <RefreshCw className={cn("w-4 h-4", syncing ? "text-orange-500" : "text-orange-400")} />
            </Button>
          </div>
          {showTimeDropdown && (
            <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-2xl shadow-lg border border-slate-100 z-50 overflow-hidden">
              {timeOptions.map((option) => (
                <button key={option.value}
                  className={cn("w-full px-4 py-3 text-left text-sm font-medium flex items-center justify-between",
                    timePeriod === option.value ? "bg-orange-50 text-orange-600" : "text-slate-700 hover:bg-slate-50")}
                  onClick={() => handleTimeChange(option.value)}>
                  <span>{option.label}</span>
                  <span className="text-[10px] text-slate-400">{option.dateRange}</span>
                  {timePeriod === option.value && <CheckCircle2 className="w-4 h-4 text-orange-600" />}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* 核心KPI - 2x2 网格 */}
        <div className="grid grid-cols-2 gap-3">
          {/* 总营业额 */}
          <Card className="p-4 bg-gradient-to-br from-orange-50 to-orange-100/50 border-orange-100">
            <div className="flex items-center gap-1.5 mb-2">
              <Wallet className="w-4 h-4 text-orange-500" />
              <span className="text-[10px] font-medium text-orange-600">总营业额</span>
            </div>
            <p className="text-2xl font-black text-slate-900">{formatMoney(rev.total_revenue)}</p>
            <div className={cn("flex items-center gap-0.5 mt-1",
              rev.mom_type === 'up' ? "text-emerald-600" : rev.mom_type === 'down' ? "text-rose-600" : "text-slate-400")}>
              {rev.mom_type === 'up' ? <TrendingUp className="w-3 h-3" /> : rev.mom_type === 'down' ? <TrendingDown className="w-3 h-3" /> : null}
              <span className="text-[10px] font-bold">{rev.mom_change > 0 ? '+' : ''}{rev.mom_change}% 环比</span>
            </div>
          </Card>

          {/* 到店人数 */}
          <Card className="p-4 bg-gradient-to-br from-blue-50 to-blue-100/50 border-blue-100">
            <div className="flex items-center gap-1.5 mb-2">
              <Users className="w-4 h-4 text-blue-500" />
              <span className="text-[10px] font-medium text-blue-600">到店人数</span>
            </div>
            <p className="text-2xl font-black text-slate-900">{bm.visitor_count.toLocaleString()}</p>
            <div className={cn("flex items-center gap-0.5 mt-1",
              bm.mom_visitor_change >= 0 ? "text-emerald-600" : "text-rose-600")}>
              {bm.mom_visitor_change >= 0 ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
              <span className="text-[10px] font-bold">{bm.mom_visitor_change >= 0 ? '+' : ''}{bm.mom_visitor_change}% 环比</span>
            </div>
          </Card>

          {/* 接待桌数 */}
          <Card className="p-4 bg-gradient-to-br from-purple-50 to-purple-100/50 border-purple-100">
            <div className="flex items-center gap-1.5 mb-2">
              <UtensilsCrossed className="w-4 h-4 text-purple-500" />
              <span className="text-[10px] font-medium text-purple-600">接待桌数</span>
            </div>
            <p className="text-2xl font-black text-slate-900">{bm.table_count.toLocaleString()}</p>
            <div className={cn("flex items-center gap-0.5 mt-1",
              bm.mom_table_change >= 0 ? "text-emerald-600" : "text-rose-600")}>
              {bm.mom_table_change >= 0 ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
              <span className="text-[10px] font-bold">{bm.mom_table_change >= 0 ? '+' : ''}{bm.mom_table_change}% 环比</span>
            </div>
          </Card>

          {/* 人均消费 */}
          <Card className="p-4 bg-gradient-to-br from-emerald-50 to-emerald-100/50 border-emerald-100">
            <div className="flex items-center gap-1.5 mb-2">
              <UserRound className="w-4 h-4 text-emerald-500" />
              <span className="text-[10px] font-medium text-emerald-600">人均消费</span>
            </div>
            <p className="text-2xl font-black text-slate-900">¥{bm.avg_per_capita.toFixed(1)}</p>
            <div className="flex items-center gap-0.5 mt-1 text-slate-400">
              <span className="text-[10px] font-bold">桌均 {bm.avg_people_per_table.toFixed(1)} 人</span>
            </div>
          </Card>
        </div>

        {/* 平台数据对比 */}
        <Card className="p-4 bg-white border-slate-100 shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <p className="text-xs font-bold text-slate-700">平台数据对比</p>
            <Badge variant="outline" className="text-[9px] text-orange-500 border-orange-200">
              <Zap className="w-2.5 h-2.5 mr-0.5" />同步数据
            </Badge>
          </div>
          <div className="grid grid-cols-2 gap-3">
            {/* 美团 */}
            <div className="bg-yellow-50/80 rounded-xl p-3">
              <div className="flex items-center gap-1.5 mb-2">
                <div className="w-5 h-5 rounded bg-yellow-400 flex items-center justify-center">
                  <span className="text-[8px] font-bold text-white">美</span>
                </div>
                <span className="text-[10px] font-bold text-yellow-700">美团</span>
              </div>
              <p className="text-lg font-black text-slate-900">{formatMoney(rev.meituan_revenue)}</p>
              <p className="text-[9px] text-slate-500 mt-0.5">
                占比 {rev.total_revenue > 0 ? ((rev.meituan_revenue / rev.total_revenue) * 100).toFixed(1) : 0}%
              </p>
            </div>
            {/* 抖音 */}
            <div className="bg-slate-50/80 rounded-xl p-3">
              <div className="flex items-center gap-1.5 mb-2">
                <div className="w-5 h-5 rounded bg-slate-900 flex items-center justify-center">
                  <span className="text-[8px] font-bold text-white">抖</span>
                </div>
                <span className="text-[10px] font-bold text-slate-700">抖音</span>
              </div>
              <p className="text-lg font-black text-slate-900">{formatMoney(rev.douyin_revenue)}</p>
              <p className="text-[9px] text-slate-500 mt-0.5">
                占比 {rev.total_revenue > 0 ? ((rev.douyin_revenue / rev.total_revenue) * 100).toFixed(1) : 0}%
              </p>
            </div>
          </div>
        </Card>

        {/* 同步结果提示 */}
        {syncResult && (
          <Card className={cn("p-3 border text-xs",
            syncResult.includes('成功') ? "bg-emerald-50 border-emerald-200 text-emerald-700" : "bg-rose-50 border-rose-200 text-rose-700"
          )}>
            <div className="flex items-center gap-2">
              {syncResult.includes('成功') ? <CheckCircle2 className="w-4 h-4 flex-shrink-0" /> : <Zap className="w-4 h-4 flex-shrink-0" />}
              <span>{syncResult}</span>
            </div>
          </Card>
        )}

        {/* 渠道构成 + 数据来源 */}
        <Card className="p-4 bg-white border-slate-100 shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <p className="text-xs font-bold text-slate-700">渠道构成</p>
            <Badge variant="outline" className="text-[9px] text-orange-500 border-orange-200">
              <Zap className="w-2.5 h-2.5 mr-0.5" />平台同步
            </Badge>
          </div>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-5 h-5 rounded bg-yellow-400 flex items-center justify-center">
                  <span className="text-[8px] font-bold text-white">美</span>
                </div>
                <span className="text-sm text-slate-600">美团</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm font-bold text-slate-900">{formatMoney(rev.meituan_revenue)}</span>
                <Badge variant="secondary" className="text-[9px]">
                  {((rev.meituan_revenue / rev.total_revenue) * 100).toFixed(1)}%
                </Badge>
              </div>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-2">
              <div className="bg-yellow-400 h-2 rounded-full transition-all"
                style={{ width: `${(rev.meituan_revenue / rev.total_revenue) * 100}%` }} />
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-5 h-5 rounded bg-slate-900 flex items-center justify-center">
                  <span className="text-[8px] font-bold text-white">抖</span>
                </div>
                <span className="text-sm text-slate-600">抖音</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm font-bold text-slate-900">{formatMoney(rev.douyin_revenue)}</span>
                <Badge variant="secondary" className="text-[9px]">
                  {((rev.douyin_revenue / rev.total_revenue) * 100).toFixed(1)}%
                </Badge>
              </div>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-2">
              <div className="bg-slate-900 h-2 rounded-full transition-all"
                style={{ width: `${(rev.douyin_revenue / rev.total_revenue) * 100}%` }} />
            </div>
          </div>
        </Card>

        {/* 运营分析摘要 */}
        <Card className="p-4 bg-white border-slate-100 shadow-sm">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-7 h-7 rounded-lg bg-amber-50 flex items-center justify-center">
              <BarChart3 className="w-3.5 h-3.5 text-amber-500" />
            </div>
            <span className="text-xs font-bold text-slate-700">运营分析</span>
            <Badge variant="outline" className="text-[9px] text-orange-500 border-orange-200 ml-auto">
              <Zap className="w-2.5 h-2.5 mr-0.5" />AI洞察
            </Badge>
          </div>
          {data.operation_analysis?.analysis_opinion ? (
            <>
              <p className="text-xs text-slate-600 leading-relaxed line-clamp-3">{data.operation_analysis.analysis_opinion}</p>
              <div className="mt-2 flex flex-wrap gap-1.5">
                {(data.operation_analysis?.goals || []).slice(0, 3).map((g, i) => (
                  <Badge key={i} variant="secondary" className="text-[9px]">{g.length > 14 ? g.slice(0, 14) + '...' : g}</Badge>
                ))}
              </div>
            </>
          ) : (
            <div className="text-center py-3">
              <p className="text-[10px] text-slate-400">暂无运营分析</p>
              <p className="text-[9px] text-slate-300 mt-1">同步平台数据后自动生成</p>
            </div>
          )}
        </Card>

        {/* 快捷入口 */}
        <div>
          <p className="text-xs font-bold text-slate-700 mb-3 px-1">详细分析</p>
          <div className="grid grid-cols-2 gap-3">
            {quickActions.map((action) => (
              <Card key={action.label}
                className="p-4 bg-white border-slate-100 shadow-sm cursor-pointer hover:shadow-md transition-shadow active:scale-[0.98]"
                onClick={() => navigate(action.path)}>
                <div className="flex items-center gap-3">
                  <div className={cn("w-10 h-10 rounded-xl flex items-center justify-center shadow-sm", action.color)}>
                    <action.icon className="w-5 h-5 text-white" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-bold text-slate-900">{action.label}</p>
                    <p className="text-[10px] text-slate-400">{action.desc}</p>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-300" />
                </div>
              </Card>
            ))}
          </div>
        </div>

      </div>
    </MobileLayout>
  );
};

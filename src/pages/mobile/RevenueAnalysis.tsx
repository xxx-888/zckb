import React, { useState, useEffect } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  Legend,
  AreaChart,
  Area,
} from 'recharts';
import {
  Wallet,
  TrendingUp,
  TrendingDown,
  BarChart3,
  ArrowUpRight,
  ArrowDownRight,
  Calendar,
  ChevronDown,
  CheckCircle2,
  RefreshCw,
  Zap,
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { Button } from '../../components/ui/button';
import { cn } from '../../lib/utils';
import { MobileLayout, useStore } from '../../components/MobileLayout';
import { fetchRevenueTrend, type RevenueTrendData } from '../../api/analysis';
import { syncDashboard } from '../../api/store-dashboard';
import { useToast } from '../../hooks/use-toast';

const COLORS = ['#f59e0b', '#111827', '#6366f1'];

export const RevenueAnalysis: React.FC<{ startDate?: string; endDate?: string }> = ({ startDate, endDate }) => {
  const { success: toastSuccess } = useToast();
  const { selectedStore } = useStore();
  const [data, setData] = useState<RevenueTrendData | null>(null);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState<'daily' | 'weekly'>('daily');
  const [syncing, setSyncing] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const storeId = selectedStore?.id || localStorage.getItem('zc_selected_store_id') || undefined;
        const result = await fetchRevenueTrend({ store_id: storeId, start_date: startDate, end_date: endDate });
        setData(result);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [selectedStore?.id, startDate, endDate]);

  // 同步营业额数据
  const handleSync = async () => {
    if (syncing) return;
    setSyncing(true);
    try {
      const storeId = selectedStore?.id || localStorage.getItem('zc_selected_store_id') || undefined;
      const result = await syncDashboard({ store_id: storeId, start_date: startDate, end_date: endDate });
      if (result.success) {
        toastSuccess('同步完成', `营业额数据已更新`);
        // 重新加载数据
        const storeId2 = selectedStore?.id || localStorage.getItem('zc_selected_store_id') || undefined;
        const trendResult = await fetchRevenueTrend({ store_id: storeId2, start_date: startDate, end_date: endDate });
        setData(trendResult);
      }
    } finally {
      setSyncing(false);
    }
  };

  if (loading || !data) {
    return (
      <div className="space-y-4 p-4">
        {[1,2,3].map(i => <Card key={i} className="p-4 animate-pulse"><div className="h-48 bg-slate-100 rounded-lg" /></Card>)}
      </div>
    );
  }

  // 无数据时展示空状态
  if (!data.daily.length && !data.weekly.length) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-slate-400">
        <BarChart3 className="w-12 h-12 mb-3 opacity-50" />
        <p className="text-sm">暂无营业额数据</p>
        <p className="text-xs mt-1">请在后台录入营业额记录后查看</p>
      </div>
    );
  }

  const weeklyData = data.weekly.length > 0 ? data.weekly : data.daily.length > 0 ? [{ ...data.daily[data.daily.length - 1], week_label: '本周' }] : [];
  const momRevenue = weeklyData.length >= 2
    ? ((weeklyData[1].total_revenue - weeklyData[0].total_revenue) / weeklyData[0].total_revenue * 100).toFixed(1)
    : '0';

  // 分渠道占比
  const latestWeek = weeklyData[weeklyData.length - 1];
  const channelData = latestWeek
    ? [
        { name: '美团', value: latestWeek.meituan_revenue || 0 },
        { name: '抖音', value: latestWeek.douyin_revenue || 0 },
        { name: '其他', value: (latestWeek.total_revenue || 0) - (latestWeek.meituan_revenue || 0) - (latestWeek.douyin_revenue || 0) },
      ].filter(d => d.value > 0)
    : [];

  // 明细表格数据（日维度）
  const formatMoney = (n: number) => `¥${n.toLocaleString()}`;
  const prevWeek = weeklyData.length >= 2 ? weeklyData[weeklyData.length - 2] : null;

  const renderTrend = (val: string) => {
    if (val.startsWith('+')) return <span className="flex items-center gap-0.5 text-emerald-600"><ArrowUpRight className="w-3 h-3" />{val}</span>;
    if (val.startsWith('-')) return <span className="flex items-center gap-0.5 text-rose-600"><ArrowDownRight className="w-3 h-3" />{val}</span>;
    return <span className="text-slate-500">{val}</span>;
  };

  return (
    <div className="space-y-4">
      {/* 日/周切换 + 同步 */}
      <div className="flex items-center justify-between px-1">
        <div className="flex gap-2">
          {(['daily', 'weekly'] as const).map(p => (
            <Button key={p} size="sm" variant={period === p ? 'default' : 'outline'}
              className={cn("text-xs", period === p && "bg-slate-900")}
              onClick={() => setPeriod(p)}>
              {p === 'daily' ? '日维度' : '周维度'}
            </Button>
          ))}
        </div>
        <Button
          variant="outline"
          size="sm"
          className={cn("h-8 gap-1.5 text-xs border-orange-200 text-orange-600", syncing && "opacity-70")}
          onClick={handleSync}
          disabled={syncing}
        >
          <RefreshCw className={cn("w-3 h-3", syncing && "animate-spin")} />
          {syncing ? '同步中' : '同步数据'}
        </Button>
      </div>

      {/* 营业额趋势图 */}
      <Card className="p-4 bg-white border-slate-100 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div>
            <div className="flex items-center gap-2">
              <p className="text-sm font-bold text-slate-700">营业额趋势</p>
              <Badge variant="outline" className="text-[9px] text-orange-500 border-orange-200">
                <Zap className="w-2.5 h-2.5 mr-0.5" />平台数据
              </Badge>
            </div>
            <p className="text-[10px] text-slate-400">
              {period === 'daily' ? data.daily[0]?.date + ' ~ ' + data.daily[data.daily.length - 1]?.date : '周度对比'}
            </p>
          </div>
          <Badge className={cn("text-[10px]",
            Number(momRevenue) > 0 ? "bg-emerald-50 text-emerald-600" :
            Number(momRevenue) < 0 ? "bg-rose-50 text-rose-600" : "bg-slate-50 text-slate-600"
          )}>
            环比 {momRevenue}%
          </Badge>
        </div>
        {period === 'daily' ? (
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={data.daily}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="date" tick={{ fontSize: 10 }} stroke="#94a3b8" />
              <YAxis tick={{ fontSize: 10 }} stroke="#94a3b8" tickFormatter={(v) => `${v / 1000}k`} />
              <Tooltip formatter={(value: any) => formatMoney(Number(value))} />
              <Bar dataKey="meituan_revenue" stackId="a" fill="#f59e0b" name="美团" radius={[0,0,0,0]} />
              <Bar dataKey="douyin_revenue" stackId="a" fill="#111827" name="抖音" radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={weeklyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="week_label" tick={{ fontSize: 10 }} stroke="#94a3b8" />
              <YAxis tick={{ fontSize: 10 }} stroke="#94a3b8" tickFormatter={(v) => `${v / 10000}w`} />
              <Tooltip formatter={(value: any) => formatMoney(Number(value))} />
              <Bar dataKey="meituan_revenue" stackId="a" fill="#f59e0b" name="美团" radius={[0,0,0,0]} />
              <Bar dataKey="douyin_revenue" stackId="a" fill="#111827" name="抖音" radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        )}
      </Card>

      {/* 分渠道构成饼图 */}
      <Card className="p-4 bg-white border-slate-100 shadow-sm">
        <p className="text-sm font-bold text-slate-700 mb-4">分渠道收入构成</p>
        <div className="flex items-center gap-4">
          <ResponsiveContainer width="45%" height={160}>
            <PieChart>
              <Pie data={channelData} cx="50%" cy="50%" innerRadius={35} outerRadius={65} dataKey="value" paddingAngle={2}>
                {channelData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
          <div className="flex-1 space-y-2">
            {channelData.map((d, i) => (
              <div key={d.name} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: COLORS[i] }} />
                  <span className="text-xs text-slate-600">{d.name}</span>
                </div>
                <div className="text-right">
                  <p className="text-xs font-bold text-slate-900">{formatMoney(d.value)}</p>
                  <p className="text-[9px] text-slate-400">
                    {((d.value / latestWeek.total_revenue) * 100).toFixed(1)}%
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </Card>

      {/* 客流与客单价趋势 */}
      <Card className="p-4 bg-white border-slate-100 shadow-sm">
        <p className="text-sm font-bold text-slate-700 mb-4">客流与客单价</p>
        <ResponsiveContainer width="100%" height={180}>
          <AreaChart data={data.daily}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
            <XAxis dataKey="date" tick={{ fontSize: 10 }} stroke="#94a3b8" />
            <YAxis yAxisId="left" tick={{ fontSize: 10 }} stroke="#94a3b8" />
            <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 10 }} stroke="#94a3b8" />
            <Tooltip />
            <Area yAxisId="left" type="monotone" dataKey="visitor_count" fill="#dbeafe" stroke="#3b82f6" strokeWidth={2} name="到店人数" />
            <Area yAxisId="right" type="monotone" dataKey="avg_per_capita" fill="#dcfce7" stroke="#22c55e" strokeWidth={2} name="人均消费" />
          </AreaChart>
        </ResponsiveContainer>
      </Card>

      {/* 明细数据表格 */}
      <Card className="bg-white border-slate-100 shadow-sm overflow-hidden">
        <div className="p-4 pb-2">
          <p className="text-sm font-bold text-slate-700">明细数据</p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-[10px] border-collapse">
            <thead>
              <tr className="bg-slate-50">
                <th className="p-2 text-left text-slate-500 font-medium sticky left-0 bg-slate-50">日期</th>
                <th className="p-2 text-center text-slate-500 font-medium">总营业额</th>
                <th className="p-2 text-center text-slate-500 font-medium">美团</th>
                <th className="p-2 text-center text-slate-500 font-medium">抖音</th>
                <th className="p-2 text-center text-slate-500 font-medium">到店</th>
                <th className="p-2 text-center text-slate-500 font-medium">桌数</th>
                <th className="p-2 text-center text-slate-500 font-medium">桌均</th>
                <th className="p-2 text-center text-slate-500 font-medium">人均</th>
              </tr>
            </thead>
            <tbody>
              {data.daily.map((d, idx) => (
                <tr key={d.date} className={cn("border-b border-slate-100", idx % 2 === 0 ? "bg-white" : "bg-slate-50/50")}>
                  <td className="p-2 font-medium text-slate-700 sticky left-0 bg-inherit">{d.date}</td>
                  <td className="p-2 text-center text-slate-900 font-bold">{formatMoney(d.total_revenue)}</td>
                  <td className="p-2 text-center text-slate-600">{formatMoney(d.meituan_revenue)}</td>
                  <td className="p-2 text-center text-slate-600">{formatMoney(d.douyin_revenue)}</td>
                  <td className="p-2 text-center text-slate-600">{d.visitor_count}</td>
                  <td className="p-2 text-center text-slate-600">{d.table_count}</td>
                  <td className="p-2 text-center text-slate-600">{d.avg_people_per_table.toFixed(1)}</td>
                  <td className="p-2 text-center text-slate-600">¥{d.avg_per_capita.toFixed(1)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};

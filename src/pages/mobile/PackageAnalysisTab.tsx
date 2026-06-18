import React, { useState, useEffect } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  ReferenceLine,
} from 'recharts';
import {
  Package,
  TrendingUp,
  TrendingDown,
  Trophy,
  AlertTriangle,
  ArrowDown,
  RefreshCw,
  Zap,
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { Button } from '../../components/ui/button';
import { cn } from '../../lib/utils';
import { MobileLayout, useStore } from '../../components/MobileLayout';
import { fetchPackageAnalysis, type PackageAnalysisData } from '../../api/analysis';
import { syncDashboard } from '../../api/store-dashboard';
import { useToast } from '../../hooks/use-toast';

export const PackageAnalysisTab: React.FC<{ startDate?: string; endDate?: string }> = ({ startDate, endDate }) => {
  const { selectedStore } = useStore();
  const { success: toastSuccess } = useToast();
  const [data, setData] = useState<PackageAnalysisData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [view, setView] = useState<'top' | 'bottom' | 'all'>('top');
  const [syncing, setSyncing] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        setError(null);
        const storeId = selectedStore?.id || localStorage.getItem('zc_selected_store_id') || undefined;
        const result = await fetchPackageAnalysis({ store_id: storeId, start_date: startDate, end_date: endDate });
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : '获取数据失败');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [selectedStore?.id, startDate, endDate]);

  // 同步套餐数据
  const handleSync = async () => {
    if (syncing) return;
    setSyncing(true);
    try {
      const storeId = selectedStore?.id || localStorage.getItem('zc_selected_store_id') || undefined;
      const result = await syncDashboard({ store_id: storeId, start_date: startDate, end_date: endDate });
      if (result.success) {
        toastSuccess('同步完成', '套餐核销数据已更新');
        const storeId2 = selectedStore?.id || localStorage.getItem('zc_selected_store_id') || undefined;
        const trendResult = await fetchPackageAnalysis({ store_id: storeId2, start_date: startDate, end_date: endDate });
        setData(trendResult);
      }
    } finally {
      setSyncing(false);
    }
  };

  if (loading) {
    return (
      <div className="space-y-4 p-4">
        {[1,2].map(i => <Card key={i} className="p-4 animate-pulse"><div className="h-48 bg-slate-100 rounded-lg" /></Card>)}
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-slate-400">
        <Package className="w-12 h-12 mb-3 opacity-50" />
        <p className="text-sm">{error || '暂无套餐核销数据'}</p>
        <p className="text-xs mt-1">{error ? '' : '请确认已选择正确的门店和时间范围'}</p>
      </div>
    );
  }

  if (!data.top_ranking.length && !data.bottom_ranking.length) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-slate-400">
        <Package className="w-12 h-12 mb-3 opacity-50" />
        <p className="text-sm">暂无套餐核销数据</p>
        <p className="text-xs mt-1">请在后台录入套餐核销记录后查看</p>
      </div>
    );
  }

  const allItems = [...data.top_ranking, ...data.bottom_ranking];
  const displayItems = view === 'top' ? data.top_ranking : view === 'bottom' ? data.bottom_ranking : allItems;

  // 核销率柱状图数据
  const chartData = allItems
    .filter(item => item.total_verify > 0)
    .map(item => ({
      name: item.product_name.length > 8 ? item.product_name.slice(0, 8) + '...' : item.product_name,
      verifyRate: item.verify_rate,
      avgRate: data.overall_summary.avg_verify_rate,
    }))
    .sort((a, b) => b.verifyRate - a.verifyRate);

  const renderMomChange = (change?: number) => {
    if (change === undefined || change === null) return <span className="text-slate-400">-</span>;
    if (change > 0) return <span className="text-emerald-600 font-bold">+{change}%</span>;
    if (change < 0) return <span className="text-rose-600 font-bold">{change}%</span>;
    return <span className="text-slate-500">0%</span>;
  };

  const isLowVerify = (rate: number) => rate < data.overall_summary.avg_verify_rate;

  return (
    <div className="space-y-4">
      {/* 概览卡片 + 同步 */}
      <div className="flex items-start gap-3">
        <div className="grid grid-cols-3 gap-3 flex-1">
          <Card className="p-3 bg-white border-slate-100 text-center">
            <p className="text-[10px] text-slate-400 mb-1">总购买</p>
            <p className="text-xl font-black text-slate-900">{data.overall_summary.total_buy}</p>
          </Card>
          <Card className="p-3 bg-white border-slate-100 text-center">
            <p className="text-[10px] text-slate-400 mb-1">总核销</p>
            <p className="text-xl font-black text-slate-900">{data.overall_summary.total_verify}</p>
          </Card>
          <Card className="p-3 bg-white border-slate-100 text-center">
            <p className="text-[10px] text-slate-400 mb-1">平均核销率</p>
            <p className="text-xl font-black text-indigo-600">{data.overall_summary.avg_verify_rate}%</p>
          </Card>
        </div>
        <Button
          variant="outline"
          size="sm"
          className={cn("h-9 w-9 rounded-xl border-orange-200 flex-shrink-0 p-0", syncing && "opacity-70")}
          onClick={handleSync}
          disabled={syncing}
          title="同步平台数据"
        >
          <RefreshCw className={cn("w-3.5 h-3.5 text-orange-500", syncing && "animate-spin")} />
        </Button>
      </div>

      {/* 核销率柱状图 */}
      <Card className="p-4 bg-white border-slate-100 shadow-sm">
        <div className="flex items-center justify-between mb-1">
          <p className="text-sm font-bold text-slate-700">核销率对比</p>
          <Badge variant="outline" className="text-[9px] text-orange-500 border-orange-200">
            <Zap className="w-2.5 h-2.5 mr-0.5" />平台同步
          </Badge>
        </div>
        <p className="text-[10px] text-slate-400 mb-4">虚线为平均核销率，低于平均值需关注</p>
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={chartData} layout="vertical" margin={{ left: 70, right: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
            <XAxis type="number" domain={[0, 120]} tick={{ fontSize: 10 }} stroke="#94a3b8" />
            <YAxis dataKey="name" type="category" tick={{ fontSize: 9 }} stroke="#94a3b8" width={65} />
            <Tooltip formatter={(value: any) => [`${Number(value)}%`, '核销率']} />
            <ReferenceLine x={data.overall_summary.avg_verify_rate} stroke="#ef4444" strokeDasharray="4 4" label={{ value: '均值', position: 'top', fontSize: 10, fill: '#ef4444' }} />
            <Bar dataKey="verifyRate" radius={[0, 4, 4, 0]} barSize={14}>
                {chartData.map((entry, i) => (
                <Cell key={i} fill={isLowVerify(entry.verifyRate) ? '#fbbf24' : '#6366f1'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </Card>

      {/* 排行切换 */}
      <div className="flex gap-2 px-1">
        {(['top', 'all', 'bottom'] as const).map(v => (
          <button key={v} onClick={() => setView(v)}
            className={cn("px-3 py-1.5 rounded-lg text-[11px] font-bold transition-all",
              view === v ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-500 hover:bg-slate-200"
            )}>
            {v === 'top' ? 'Top 5 爆款' : v === 'bottom' ? '末 5 滞销' : '全部套餐'}
          </button>
        ))}
      </div>

      {/* 明细表格 */}
      <Card className="bg-white border-slate-100 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-[11px] border-collapse">
            <thead>
              <tr className="bg-slate-50">
                <th className="p-2 text-left text-slate-500 font-medium sticky left-0 bg-slate-50 z-10 min-w-[100px]">套餐名称</th>
                <th className="p-2 text-center text-slate-500 font-medium">美团购买</th>
                <th className="p-2 text-center text-slate-500 font-medium">美团核销</th>
                <th className="p-2 text-center text-slate-500 font-medium">抖音购买</th>
                <th className="p-2 text-center text-slate-500 font-medium">抖音核销</th>
                <th className="p-2 text-center text-slate-500 font-medium">总核销</th>
                <th className="p-2 text-center text-slate-500 font-medium">核销率</th>
                <th className="p-2 text-center text-slate-500 font-medium">环比</th>
              </tr>
            </thead>
            <tbody>
              {displayItems.map((item, idx) => (
                <tr key={item.product_name}
                  className={cn("border-b border-slate-100", idx % 2 === 0 ? "bg-white" : "bg-slate-50/50")}>
                  <td className="p-2 font-medium text-slate-700 sticky left-0 bg-inherit z-10 whitespace-nowrap">
                    <div className="flex items-center gap-1.5">
                      {idx === 0 && view === 'top' && <Trophy className="w-3 h-3 text-yellow-500 flex-shrink-0" />}
                      {view === 'bottom' && idx === displayItems.length - 1 && <AlertTriangle className="w-3 h-3 text-rose-400 flex-shrink-0" />}
                      <span className="truncate max-w-[100px]">{item.product_name}</span>
                    </div>
                  </td>
                  <td className="p-2 text-center text-slate-600">{item.meituan_buy}</td>
                  <td className="p-2 text-center text-slate-600">{item.meituan_verify}</td>
                  <td className="p-2 text-center text-slate-600">{item.douyin_buy}</td>
                  <td className="p-2 text-center text-slate-600">{item.douyin_verify}</td>
                  <td className="p-2 text-center font-bold text-slate-900">{item.total_verify}</td>
                  <td className={cn("p-2 text-center font-bold",
                    isLowVerify(item.verify_rate) ? "text-amber-600" : "text-indigo-600"
                  )}>
                    {item.verify_rate.toFixed(1)}%
                  </td>
                  <td className="p-2 text-center">-</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};

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
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { cn } from '../../lib/utils';
import { fetchPackageAnalysis, mockPackageAnalysis, type PackageAnalysisData } from '../../api/analysis';

export const PackageAnalysisTab: React.FC = () => {
  const [data, setData] = useState<PackageAnalysisData | null>(null);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState<'top' | 'bottom' | 'all'>('top');

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const result = await fetchPackageAnalysis();
        setData(result);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading || !data) {
    return (
      <div className="space-y-4 p-4">
        {[1,2].map(i => <Card key={i} className="p-4 animate-pulse"><div className="h-48 bg-slate-100 rounded-lg" /></Card>)}
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
      {/* 概览卡片 */}
      <div className="grid grid-cols-3 gap-3">
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

      {/* 核销率柱状图 */}
      <Card className="p-4 bg-white border-slate-100 shadow-sm">
        <p className="text-sm font-bold text-slate-700 mb-1">核销率对比</p>
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
                  <td className="p-2 text-center">{renderMomChange(item.mom_verify_change)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};

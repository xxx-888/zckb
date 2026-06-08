import React, { useState, useEffect } from 'react';
import {
  Funnel,
  TrendingUp,
  Star,
  MessageSquare,
  Award,
  Eye,
  MousePointerClick,
  ShoppingCart,
  CheckCircle,
  AlertTriangle,
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { cn } from '../../lib/utils';
import { fetchStoreHealth, type StoreHealthData } from '../../api/analysis';

const platformColors: Record<string, string> = {
  '美团': 'bg-yellow-400',
  '点评': 'bg-orange-500',
  '抖音': 'bg-slate-900',
};

const platformTextColors: Record<string, string> = {
  '美团': 'text-yellow-600',
  '点评': 'text-orange-600',
  '抖音': 'text-slate-900',
};

export const StoreAnalysis: React.FC = () => {
  const [data, setData] = useState<StoreHealthData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const result = await fetchStoreHealth();
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
        {[1,2,3].map(i => <Card key={i} className="p-4 animate-pulse"><div className="h-48 bg-slate-100 rounded-lg" /></Card>)}
      </div>
    );
  }

  return (
    <div className="space-y-4">

      {/* 流量漏斗 */}
      <Card className="p-4 bg-white border-slate-100 shadow-sm">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-7 h-7 rounded-lg bg-blue-50 flex items-center justify-center">
            <Funnel className="w-3.5 h-3.5 text-blue-500" />
          </div>
          <span className="text-sm font-bold text-slate-700">线上流量漏斗</span>
        </div>
        <div className="space-y-4">
          {data.funnels.map((funnel) => {
            const steps = [
              { label: '曝光', value: funnel.impressions, icon: Eye, pct: 100 },
              { label: '访问', value: funnel.visits, icon: MousePointerClick, pct: funnel.impression_to_visit },
              { label: '购买', value: funnel.purchases, icon: ShoppingCart, pct: funnel.visit_to_purchase },
            ];
            return (
              <div key={funnel.platform} className="bg-slate-50 rounded-xl p-3">
                <div className="flex items-center gap-2 mb-3">
                  <div className={cn("w-5 h-5 rounded", platformColors[funnel.platform] || 'bg-slate-400', "flex items-center justify-center")}>
                    <span className="text-[8px] font-bold text-white">{funnel.platform[0]}</span>
                  </div>
                  <span className="text-xs font-bold text-slate-700">{funnel.platform}</span>
                </div>
                <div className="space-y-2">
                  {steps.map((step, si) => (
                    <div key={si}>
                      <div className="flex items-center justify-between mb-1">
                        <div className="flex items-center gap-1.5">
                          <step.icon className="w-3 h-3 text-slate-400" />
                          <span className="text-[10px] text-slate-500">{step.label}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-bold text-slate-900">{step.value.toLocaleString()}</span>
                          {si > 0 && (
                            <Badge variant="secondary" className="text-[9px]">
                              {step.pct.toFixed(1)}%
                            </Badge>
                          )}
                        </div>
                      </div>
                      {si < steps.length - 1 && (
                        <div className="w-full bg-slate-200 rounded-full h-1.5 mb-1">
                          <div className="bg-indigo-500 h-1.5 rounded-full transition-all"
                            style={{ width: `${Math.min(100, step.pct * 3)}%` }} />
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </Card>

      {/* 榜单追踪 */}
      <Card className="p-4 bg-white border-slate-100 shadow-sm">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-7 h-7 rounded-lg bg-amber-50 flex items-center justify-center">
            <Award className="w-3.5 h-3.5 text-amber-500" />
          </div>
          <span className="text-sm font-bold text-slate-700">门店榜单追踪</span>
        </div>
        <div className="grid grid-cols-1 gap-2">
          {data.rankings.map((r) => (
            <div key={r.platform + r.ranking_name} className="flex items-center justify-between bg-slate-50 rounded-xl p-3">
              <div className="flex items-center gap-2">
                <div className={cn("w-5 h-5 rounded", platformColors[r.platform] || 'bg-slate-400', "flex items-center justify-center")}>
                  <span className="text-[8px] font-bold text-white">{r.platform[0]}</span>
                </div>
                <div>
                  <p className="text-xs font-medium text-slate-700">{r.platform} {r.ranking_name}</p>
                  <p className="text-[10px] text-slate-400">{r.prev_rank}</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-xs font-bold text-slate-900">{r.current_rank}</p>
                <Badge variant="secondary" className="text-[9px]">{r.rank_change}</Badge>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* 评价监测 */}
      <Card className="p-4 bg-white border-slate-100 shadow-sm">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-7 h-7 rounded-lg bg-emerald-50 flex items-center justify-center">
            <Star className="w-3.5 h-3.5 text-emerald-500" />
          </div>
          <span className="text-sm font-bold text-slate-700">评价监测</span>
        </div>
        <div className="space-y-3">
          {data.reviews_summary.map((review) => (
            <div key={review.platform} className="bg-slate-50 rounded-xl p-3">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className={cn("w-5 h-5 rounded", platformColors[review.platform] || 'bg-slate-400', "flex items-center justify-center")}>
                    <span className="text-[8px] font-bold text-white">{review.platform[0]}</span>
                  </div>
                  <span className="text-xs font-bold text-slate-700">{review.platform}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Star className="w-3 h-3 text-yellow-400 fill-yellow-400" />
                  <span className="text-sm font-bold text-slate-900">{review.star_rating}</span>
                  <span className="text-[9px] text-slate-400">({review.prev_star_rating})</span>
                </div>
              </div>
              <div className="flex items-center gap-4 text-[10px]">
                <div className="flex items-center gap-1 text-slate-500">
                  <MessageSquare className="w-3 h-3" />
                  新评价 <span className="font-bold text-slate-700">{review.new_reviews}</span>
                </div>
                {review.bad_reviews > 0 && (
                  <div className="flex items-center gap-1 text-rose-500">
                    <AlertTriangle className="w-3 h-3" />
                    差评 <span className="font-bold">{review.bad_reviews}</span>
                  </div>
                )}
              </div>
              {review.bad_keywords.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-1">
                  {review.bad_keywords.map(kw => (
                    <Badge key={kw} className="text-[8px] bg-rose-50 text-rose-600 border-rose-200">{kw}</Badge>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </Card>

      {/* 平台指标明细表 */}
      <Card className="bg-white border-slate-100 shadow-sm overflow-hidden">
        <div className="p-4 pb-2">
          <p className="text-sm font-bold text-slate-700">平台运营指标</p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-[11px] border-collapse">
            <thead>
              <tr className="bg-slate-50">
                <th className="p-2 text-left text-slate-500 font-medium">平台</th>
                <th className="p-2 text-center text-slate-500 font-medium">曝光</th>
                <th className="p-2 text-center text-slate-500 font-medium">访问</th>
                <th className="p-2 text-center text-slate-500 font-medium">曝光转化</th>
                <th className="p-2 text-center text-slate-500 font-medium">购买</th>
                <th className="p-2 text-center text-slate-500 font-medium">购买转化</th>
                <th className="p-2 text-center text-slate-500 font-medium">评价</th>
                <th className="p-2 text-center text-slate-500 font-medium">差评</th>
              </tr>
            </thead>
            <tbody>
              {data.funnels.map((f, idx) => {
                const rs = data.reviews_summary[idx];
                return (
                  <tr key={f.platform} className="border-b border-slate-100">
                    <td className="p-2">
                      <div className="flex items-center gap-1.5">
                        <div className={cn("w-5 h-5 rounded", platformColors[f.platform], "flex items-center justify-center")}>
                          <span className="text-[8px] font-bold text-white">{f.platform[0]}</span>
                        </div>
                        <span className="font-medium text-slate-700">{f.platform}</span>
                      </div>
                    </td>
                    <td className="p-2 text-center text-slate-600">{f.impressions.toLocaleString()}</td>
                    <td className="p-2 text-center text-slate-600">{f.visits.toLocaleString()}</td>
                    <td className="p-2 text-center text-slate-600">{f.impression_to_visit}%</td>
                    <td className="p-2 text-center text-slate-600">{f.purchases}</td>
                    <td className="p-2 text-center text-slate-600">{f.visit_to_purchase}%</td>
                    <td className="p-2 text-center text-slate-600">{rs?.new_reviews || 0}</td>
                    <td className={cn("p-2 text-center font-bold", (rs?.bad_reviews || 0) > 0 ? "text-rose-600" : "text-slate-600")}>
                      {rs?.bad_reviews || 0}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};

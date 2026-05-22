import React, { useState, useEffect } from 'react';
import { Card } from '../../../components/ui/card';
import { Button } from '../../../components/ui/button';
import { Badge } from '../../../components/ui/badge';
import { useToast } from '../../../hooks/use-toast';
import { adminApi } from '../../../api/admin';
import { BarChart3, RefreshCw, AlertCircle, TrendingUp, Star, ThumbsUp } from 'lucide-react';

export const Evaluation: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchEvaluation = async () => {
    setLoading(true);
    setError(null);
    try {
      const d = await adminApi.getAIEvaluation().catch(err => { console.warn('[Evaluation] 获取失败:', err); return null; });
      setData(d);
    } catch (err) {
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally { setLoading(false); }
  };

  useEffect(() => { fetchEvaluation(); }, []);

  if (loading) return <div className="flex items-center justify-center h-64"><RefreshCw className="w-6 h-6 text-slate-400 animate-spin" /></div>;
  if (error) return <div className="flex flex-col items-center justify-center h-64 gap-4"><AlertCircle className="w-10 h-10 text-rose-400" /><p className="text-slate-500">{error}</p><Button variant="outline" onClick={fetchEvaluation}>重试</Button></div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2"><BarChart3 className="w-5 h-5 text-amber-500" />AI 效能评估</h2>
          <p className="text-sm text-slate-500">基于真实反馈的 AI 表现分析</p>
        </div>
        <Button variant="outline" onClick={fetchEvaluation}><RefreshCw className="w-4 h-4 mr-1" />刷新</Button>
      </div>

      {!data ? (
        <div className="text-center py-16 text-slate-400"><BarChart3 className="w-12 h-12 mx-auto mb-3 opacity-30" /><p>暂无评估数据</p></div>
      ) : (
        <>
          {/* Score Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card className="p-5 border-slate-100 shadow-sm text-center">
              <Star className="w-8 h-8 text-amber-500 mx-auto mb-2" />
              <p className="text-3xl font-bold text-slate-900">{data.overall_score || data.total_score || 0}</p>
              <p className="text-xs text-slate-500">综合评分</p>
            </Card>
            <Card className="p-5 border-slate-100 shadow-sm text-center">
              <ThumbsUp className="w-8 h-8 text-emerald-500 mx-auto mb-2" />
              <p className="text-3xl font-bold text-slate-900">{data.approval_rate || 0}%</p>
              <p className="text-xs text-slate-500">审核通过率</p>
            </Card>
            <Card className="p-5 border-slate-100 shadow-sm text-center">
              <TrendingUp className="w-8 h-8 text-blue-500 mx-auto mb-2" />
              <p className="text-3xl font-bold text-slate-900">{data.improvement || 0}%</p>
              <p className="text-xs text-slate-500">较上月提升</p>
            </Card>
          </div>

          {/* Dimension Scores */}
          {data?.dimensions && data.dimensions.length > 0 && (
            <div>
              <h3 className="font-bold text-slate-900 mb-3 text-sm">各维度评分</h3>
              <div className="space-y-3">
                {data.dimensions.map((d: any, i: number) => (
                  <Card key={i} className="p-4 border-slate-100 shadow-sm">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-slate-700">{d.name || d.dimension}</span>
                      <span className="text-sm font-bold text-slate-900">{d.score || 0}分</span>
                    </div>
                    <div className="w-full bg-slate-100 rounded-full h-2">
                      <div className="bg-amber-500 h-2 rounded-full" style={{ width: `${Math.min(100, d.score || 0)}%` }} />
                    </div>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

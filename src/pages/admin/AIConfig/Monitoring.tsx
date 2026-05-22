import React, { useState, useEffect } from 'react';
import { Card } from '../../../components/ui/card';
import { Button } from '../../../components/ui/button';
import { Badge } from '../../../components/ui/badge';
import { useToast } from '../../../hooks/use-toast';
import { adminApi } from '../../../api/admin';
import { Activity, RefreshCw, AlertCircle, Zap, Clock, CheckCircle, XCircle } from 'lucide-react';

export const Monitoring: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchMonitoring = async () => {
    setLoading(true);
    setError(null);
    try {
      const d = await adminApi.getAIMonitoring().catch(err => { console.warn('[Monitoring] 获取失败:', err); return null; });
      setData(d);
    } catch (err) {
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally { setLoading(false); }
  };

  useEffect(() => { fetchMonitoring(); }, []);

  if (loading) return <div className="flex items-center justify-center h-64"><RefreshCw className="w-6 h-6 text-slate-400 animate-spin" /></div>;
  if (error) return <div className="flex flex-col items-center justify-center h-64 gap-4"><AlertCircle className="w-10 h-10 text-rose-400" /><p className="text-slate-500">{error}</p><Button variant="outline" onClick={fetchMonitoring}>重试</Button></div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2"><Activity className="w-5 h-5 text-emerald-500" />AI 实时监控</h2>
          <p className="text-sm text-slate-500">AI 处理链路日志与性能指标</p>
        </div>
        <Button variant="outline" onClick={fetchMonitoring}><RefreshCw className="w-4 h-4 mr-1" />刷新</Button>
      </div>

      {!data ? (
        <div className="text-center py-16 text-slate-400"><Activity className="w-12 h-12 mx-auto mb-3 opacity-30" /><p>暂无监控数据</p></div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="p-5 border-slate-100 shadow-sm text-center">
            <Zap className="w-8 h-8 text-amber-500 mx-auto mb-2" />
            <p className="text-2xl font-bold text-slate-900">{data.total_calls || data.total_requests || 0}</p>
            <p className="text-xs text-slate-500">总调用次数</p>
          </Card>
          <Card className="p-5 border-slate-100 shadow-sm text-center">
            <Clock className="w-8 h-8 text-blue-500 mx-auto mb-2" />
            <p className="text-2xl font-bold text-slate-900">{data.avg_latency || data.avg_response_time || 0}ms</p>
            <p className="text-xs text-slate-500">平均响应时间</p>
          </Card>
          <Card className="p-5 border-slate-100 shadow-sm text-center">
            <CheckCircle className="w-8 h-8 text-emerald-500 mx-auto mb-2" />
            <p className="text-2xl font-bold text-slate-900">{data.success_rate || 0}%</p>
            <p className="text-xs text-slate-500">成功率</p>
          </Card>
          <Card className="p-5 border-slate-100 shadow-sm text-center">
            <XCircle className="w-8 h-8 text-rose-500 mx-auto mb-2" />
            <p className="text-2xl font-bold text-slate-900">{data.error_count || data.failed_requests || 0}</p>
            <p className="text-xs text-slate-500">失败次数</p>
          </Card>
        </div>
      )}

      {/* Recent Logs */}
      {data?.recent_logs && data.recent_logs.length > 0 && (
        <div>
          <h3 className="font-bold text-slate-900 mb-3 text-sm">最近日志</h3>
          <div className="space-y-2">
            {data.recent_logs.map((log: any, i: number) => (
              <Card key={i} className="p-3 border-slate-100 shadow-sm flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Badge className={log.status === 'success' ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'}>{log.status || 'unknown'}</Badge>
                  <span className="text-xs text-slate-600">{log.message || log.prompt?.slice(0, 60) || ''}</span>
                </div>
                <span className="text-xs text-slate-400">{log.timestamp || log.created_at?.slice(0, 19) || ''}</span>
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

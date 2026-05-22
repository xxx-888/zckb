import React, { useState, useEffect } from 'react';
import { 
  Monitor, Play, RefreshCcw, AlertTriangle, CheckCircle2, 
  Globe, Activity, History, Plus, Trash2, Search, AlertCircle
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { AdminLayout } from '../../components/AdminLayout';
import { useToast } from '../../hooks/use-toast';
import { spiderApi, SpiderPlatform, SpiderTask } from '../../api/spider';

export const SpiderManagement: React.FC = () => {
  const [platforms, setPlatforms] = useState<SpiderPlatform[]>([]);
  const [tasks, setTasks] = useState<SpiderTask[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [syncingId, setSyncingId] = useState<string | null>(null);
  const [syncAllLoading, setSyncAllLoading] = useState(false);
  const [showAdd, setShowAdd] = useState(false);
  const [newPlat, setNewPlat] = useState({ name: '', display_name: '' });

  const { success, error: toastError } = useToast();

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [pRes, tRes] = await Promise.allSettled([
        spiderApi.getPlatforms().catch(err => { console.warn('[Spider] 获取平台列表失败:', err); return []; }),
        spiderApi.getTasks().catch(err => { console.warn('[Spider] 获取任务列表失败:', err); return []; }),
      ]);
      if (pRes.status === 'fulfilled') {
        const data = pRes.value;
        setPlatforms(Array.isArray(data) ? data : []);
      }
      if (tRes.status === 'fulfilled') {
        const data = tRes.value;
        setTasks(Array.isArray(data) ? data : []);
      }
    } catch (err) {
      console.error('[Spider] 数据加载异常:', err);
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, []);

  const handleSyncPlatform = async (id: string) => {
    setSyncingId(id);
    try {
      await spiderApi.syncPlatform(id);
      success('同步完成', '平台数据已同步');
      fetchData();
    } catch (err: any) {
      toastError('同步失败', err.message);
    } finally {
      setSyncingId(null);
    }
  };

  const handleSyncAll = async () => {
    setSyncAllLoading(true);
    try {
      await spiderApi.syncAllPlatforms();
      success('全局同步', '所有平台同步任务已启动');
      fetchData();
    } catch (err: any) {
      toastError('同步失败', err.message);
    } finally {
      setSyncAllLoading(false);
    }
  };

  const handleAddPlatform = async () => {
    if (!newPlat.name) return;
    try {
      await spiderApi.createPlatform(newPlat as any);
      success('添加成功', `平台 "${newPlat.name}" 已添加`);
      setShowAdd(false);
      setNewPlat({ name: '', display_name: '' });
      fetchData();
    } catch (err: any) {
      toastError('添加失败', err.message);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await spiderApi.deletePlatform(id);
      success('已删除', '平台已移除');
      fetchData();
    } catch (err: any) {
      toastError('删除失败', err.message);
    }
  };

  const handleCancelTask = async (id: string) => {
    try {
      await spiderApi.cancelTask(id);
      success('已取消', '任务已取消');
      fetchData();
    } catch (err: any) {
      toastError('取消失败', err.message);
    }
  };

  const statusBadge = (s: string) => {
    const m: Record<string, { color: string; label: string }> = {
      active: { color: 'bg-emerald-100 text-emerald-700', label: '运行中' },
      paused: { color: 'bg-amber-100 text-amber-700', label: '已暂停' },
      error: { color: 'bg-rose-100 text-rose-700', label: '异常' },
      pending: { color: 'bg-slate-100 text-slate-600', label: '等待中' },
      running: { color: 'bg-blue-100 text-blue-700', label: '执行中' },
      success: { color: 'bg-emerald-100 text-emerald-700', label: '已完成' },
      failed: { color: 'bg-rose-100 text-rose-700', label: '失败' },
    };
    const c = m[s] || { color: 'bg-slate-100 text-slate-600', label: s };
    return <Badge className={c.color}>{c.label}</Badge>;
  };

  if (loading) return <AdminLayout><div className="flex items-center justify-center h-64"><RefreshCcw className="w-6 h-6 text-slate-400 animate-spin" /></div></AdminLayout>;
  if (error) return <AdminLayout><div className="flex flex-col items-center justify-center h-64 gap-4"><AlertCircle className="w-10 h-10 text-rose-400" /><p className="text-slate-500">{error}</p><Button variant="outline" onClick={fetchData}>重试</Button></div></AdminLayout>;

  return (
    <AdminLayout>
      <div className="space-y-6 pb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">爬虫管理</h1>
            <p className="text-slate-500 text-sm mt-1">数据采集平台管理与同步</p>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="outline" onClick={() => setShowAdd(true)}><Plus className="w-4 h-4 mr-1" />添加平台</Button>
            <Button className="bg-indigo-500 hover:bg-indigo-600 text-white" onClick={handleSyncAll} disabled={syncAllLoading}>
              <RefreshCcw className={`w-4 h-4 mr-1 ${syncAllLoading ? 'animate-spin' : ''}`} />
              {syncAllLoading ? '同步中...' : '全局同步'}
            </Button>
          </div>
        </div>

        {/* Platform Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {platforms.length === 0 ? (
            <div className="col-span-full text-center py-12 text-slate-400">
              <Globe className="w-10 h-10 mx-auto mb-3 opacity-50" />
              <p>暂无平台，点击"添加平台"开始</p>
            </div>
          ) : platforms.map(p => (
            <Card key={p.id} className="p-5 border-slate-100 shadow-sm space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Globe className="w-5 h-5 text-blue-500" />
                  <span className="font-bold text-slate-900">{p.display_name || p.name}</span>
                </div>
                {statusBadge(p.status)}
              </div>
              <div className="text-xs text-slate-500 space-y-1">
                <p>最后同步: {p.last_sync_at?.slice(0, 16) || '从未'}</p>
              </div>
              <div className="flex items-center gap-2">
                <Button size="sm" variant="outline" onClick={() => handleSyncPlatform(p.id)} disabled={syncingId === p.id}>
                  <RefreshCcw className={`w-3 h-3 mr-1 ${syncingId === p.id ? 'animate-spin' : ''}`} />
                  {syncingId === p.id ? '同步中' : '同步'}
                </Button>
                <Button size="sm" variant="ghost" className="text-rose-500" onClick={() => handleDelete(p.id)}>
                  <Trash2 className="w-3 h-3" />
                </Button>
              </div>
            </Card>
          ))}
        </div>

        {/* Tasks */}
        <div>
          <h2 className="text-lg font-bold text-slate-900 mb-3">任务列表</h2>
          {tasks.length === 0 ? (
            <div className="text-center py-8 text-slate-400">
              <History className="w-8 h-8 mx-auto mb-2 opacity-50" /><p>暂无任务</p>
            </div>
          ) : (
            <div className="space-y-2">
              {tasks.map(t => (
                <Card key={t.id} className="p-4 border-slate-100 shadow-sm flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    {statusBadge(t.status)}
                    <div>
                      <p className="text-sm font-medium text-slate-900">{t.task_type}</p>
                      <p className="text-xs text-slate-400">{t.started_at?.slice(0, 16) || t.scheduled_at?.slice(0, 16) || ''}</p>
                    </div>
                  </div>
                  {(t.status === 'pending' || t.status === 'running') && (
                    <Button size="sm" variant="ghost" className="text-rose-500" onClick={() => handleCancelTask(t.id)}>
                      取消
                    </Button>
                  )}
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Add Platform Dialog */}
      {showAdd && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
          <Card className="w-96 p-6 space-y-4">
            <h3 className="font-bold text-slate-900">添加平台</h3>
            <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="平台名称 (如 meituan)" value={newPlat.name} onChange={e => setNewPlat(p => ({ ...p, name: e.target.value }))} />
            <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="显示名称 (如 美团)" value={newPlat.display_name} onChange={e => setNewPlat(p => ({ ...p, display_name: e.target.value }))} />
            <div className="flex justify-end gap-3">
              <Button variant="ghost" onClick={() => setShowAdd(false)}>取消</Button>
              <Button className="bg-indigo-500 hover:bg-indigo-600 text-white" onClick={handleAddPlatform}>添加</Button>
            </div>
          </Card>
        </div>
      )}
    </AdminLayout>
  );
};

import React, { useState, useEffect } from 'react';
import { 
  FileCheck, Search, CheckCircle, XCircle, 
  MessageSquare, User, ShieldAlert, RefreshCw,
  AlertCircle, Sparkles,
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { AdminLayout } from '../../components/AdminLayout';
import { useToast } from '../../hooks/use-toast';
import { auditApi, AuditItem, AuditStats } from '../../api/audit';

const statusConfig: Record<string, { label: string; color: string; icon: React.ElementType }> = {
  pending:   { label: '待审核', color: 'bg-amber-100 text-amber-700', icon: AlertCircle },
  approved:  { label: '已通过', color: 'bg-emerald-100 text-emerald-700', icon: CheckCircle },
  rejected:  { label: '已拒绝', color: 'bg-rose-100 text-rose-700', icon: XCircle },
  sent:      { label: '已发送', color: 'bg-blue-100 text-blue-700', icon: FileCheck },
};

export const ReplyAudit: React.FC = () => {
  const [audits, setAudits] = useState<AuditItem[]>([]);
  const [stats, setStats] = useState<AuditStats | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [showRejectDialog, setShowRejectDialog] = useState(false);
  const [rejectReason, setRejectReason] = useState('');
  const [rejectTargetId, setRejectTargetId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { success, error: toastError } = useToast();

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [listRes, statsRes] = await Promise.allSettled([
        auditApi.getAuditList({ limit: 50 }).catch(err => { console.warn('[ReplyAudit] 获取审核列表失败:', err); return { items: [], total: 0 }; }),
        auditApi.getStats().catch(err => { console.warn('[ReplyAudit] 获取统计失败:', err); return null; }),
      ]);
      if (listRes.status === 'fulfilled') {
        const data = listRes.value;
        setAudits(Array.isArray((data as any)?.items) ? (data as any).items : Array.isArray(data) ? data : []);
      }
      if (statsRes.status === 'fulfilled') {
        setStats(statsRes.value);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, []);

  const filtered = audits.filter(a =>
    (a.store_name || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
    (a.content || '').toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleApprove = async (id: string) => {
    try {
      await auditApi.approveAudit(id);
      setAudits(prev => prev.map(a => a.id === id ? { ...a, status: 'approved' } : a));
      success('审核通过', '该回复已通过并发布');
    } catch (err: any) {
      toastError('操作失败', err.message);
    }
  };

  const handleReject = async () => {
    if (!rejectTargetId || !rejectReason.trim()) {
      toastError('拒绝失败', '请填写拒绝原因');
      return;
    }
    try {
      await auditApi.rejectAudit(rejectTargetId, rejectReason);
      setAudits(prev => prev.map(a => a.id === rejectTargetId ? { ...a, status: 'rejected', reject_reason: rejectReason } : a));
      setShowRejectDialog(false);
      setRejectReason('');
      setRejectTargetId(null);
      success('已拒绝', '该回复已拒绝');
    } catch (err: any) {
      toastError('操作失败', err.message);
    }
  };

  const handleRegenerate = async (id: string) => {
    try {
      await auditApi.regenerateReply(id);
      success('重新生成', 'AI正在生成新回复...');
      fetchData();
    } catch (err: any) {
      toastError('操作失败', err.message);
    }
  };

  const openRejectDialog = (id: string) => {
    setRejectTargetId(id);
    setShowRejectDialog(true);
  };

  const selected = audits.find(a => a.id === selectedId);

  if (loading) {
    return <AdminLayout><div className="flex items-center justify-center h-64"><RefreshCw className="w-6 h-6 text-slate-400 animate-spin" /></div></AdminLayout>;
  }

  if (error) {
    return <AdminLayout><div className="flex flex-col items-center justify-center h-64 gap-4"><AlertCircle className="w-10 h-10 text-rose-400" /><p className="text-slate-500">{error}</p><Button variant="outline" onClick={fetchData}>重试</Button></div></AdminLayout>;
  }

  return (
    <AdminLayout>
      <div className="space-y-6 pb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">回复审核</h1>
            <p className="text-slate-500 text-sm mt-1">AI 生成回复人工审核与管理</p>
          </div>
        </div>

        {/* Stats */}
        {stats && (
          <div className="grid grid-cols-4 gap-4">
            <Card className="p-4 text-center"><p className="text-2xl font-bold text-amber-600">{stats.pending_count}</p><p className="text-xs text-slate-500">待审核</p></Card>
            <Card className="p-4 text-center"><p className="text-2xl font-bold text-emerald-600">{stats.approved_count}</p><p className="text-xs text-slate-500">已通过</p></Card>
            <Card className="p-4 text-center"><p className="text-2xl font-bold text-rose-600">{stats.rejected_count}</p><p className="text-xs text-slate-500">已拒绝</p></Card>
            <Card className="p-4 text-center"><p className="text-2xl font-bold text-slate-600">{stats.total_count}</p><p className="text-xs text-slate-500">总计</p></Card>
          </div>
        )}

        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            className="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-sm outline-none focus:border-indigo-300"
            placeholder="搜索门店或评论内容..."
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* List */}
          <div className="lg:col-span-1 space-y-3 max-h-[70vh] overflow-y-auto">
            {filtered.length === 0 ? (
              <div className="text-center py-12 text-slate-400">
                <FileCheck className="w-10 h-10 mx-auto mb-3 opacity-50" />
                <p>{searchQuery ? '无匹配结果' : '暂无审核项'}</p>
              </div>
            ) : (
              filtered.map(a => (
                <Card
                  key={a.id}
                  className={`p-4 cursor-pointer transition-all border-slate-100 shadow-sm ${selectedId === a.id ? 'ring-2 ring-indigo-400 border-indigo-200' : 'hover:border-slate-200'}`}
                  onClick={() => setSelectedId(a.id)}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium text-slate-900 text-sm truncate">{a.store_name || '未知门店'}</span>
                    <Badge className={`text-xs ${statusConfig[a.status]?.color || ''}`}>{statusConfig[a.status]?.label || a.status}</Badge>
                  </div>
                  <p className="text-xs text-slate-500 line-clamp-2">{a.content}</p>
                  <div className="flex items-center gap-2 mt-2 text-xs text-slate-400">
                    <User className="w-3 h-3" />
                    <span>{a.user_name || '匿名'}</span>
                    <span>·</span>
                    <span>{a.created_at?.slice(0, 10) || ''}</span>
                  </div>
                </Card>
              ))
            )}
          </div>

          {/* Detail */}
          <div className="lg:col-span-2">
            {selected ? (
              <Card className="p-6 border-slate-100 shadow-sm space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-bold text-slate-900">{selected.store_name || '未知门店'}</h3>
                    <p className="text-sm text-slate-500">{selected.platform} · {selected.user_name}</p>
                  </div>
                  <Badge className={statusConfig[selected.status]?.color}>{statusConfig[selected.status]?.label || selected.status}</Badge>
                </div>

                {/* Original Review */}
                <div className="bg-slate-50 rounded-xl p-4">
                  <p className="text-xs text-slate-400 mb-1">用户评价</p>
                  <p className="text-sm text-slate-700">{selected.content}</p>
                  {selected.rating && <p className="text-xs text-amber-500 mt-1">{'★'.repeat(selected.rating)}</p>}
                </div>

                {/* AI Reply */}
                <div className="bg-indigo-50 rounded-xl p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Sparkles className="w-4 h-4 text-indigo-500" />
                    <p className="text-xs text-indigo-500 font-medium">AI 生成回复</p>
                  </div>
                  <p className="text-sm text-slate-700">{selected.ai_reply || '暂无'}</p>
                </div>

                {/* Scores */}
                {selected.scores && (
                  <div className="grid grid-cols-4 gap-2 text-center text-xs">
                    {Object.entries(selected.scores).map(([k, v]) => (
                      <div key={k} className="bg-slate-50 rounded-lg p-2">
                        <p className="text-slate-400">{k}</p>
                        <p className="font-bold text-slate-700">{v}</p>
                      </div>
                    ))}
                  </div>
                )}

                {/* Reject reason */}
                {selected.reject_reason && (
                  <div className="bg-rose-50 rounded-xl p-3">
                    <p className="text-xs text-rose-600">拒绝原因: {selected.reject_reason}</p>
                  </div>
                )}

                {/* Actions */}
                {selected.status === 'pending' && (
                  <div className="flex items-center gap-3 pt-2">
                    <Button size="sm" className="bg-emerald-500 hover:bg-emerald-600 text-white" onClick={() => handleApprove(selected.id)}>
                      <CheckCircle className="w-4 h-4 mr-1" />通过并发布
                    </Button>
                    <Button size="sm" variant="outline" className="text-rose-500 border-rose-200" onClick={() => openRejectDialog(selected.id)}>
                      <XCircle className="w-4 h-4 mr-1" />驳回
                    </Button>
                    <Button size="sm" variant="ghost" onClick={() => handleRegenerate(selected.id)}>
                      <RefreshCw className="w-4 h-4 mr-1" />重新生成
                    </Button>
                  </div>
                )}
              </Card>
            ) : (
              <div className="flex flex-col items-center justify-center h-64 text-slate-400">
                <ShieldAlert className="w-10 h-10 mb-3 opacity-50" />
                <p>{filtered.length > 0 ? '选择左侧审核项查看详情' : '暂无审核数据'}</p>
              </div>
            )}
          </div>
        </div>

        {/* Reject Dialog */}
        {showRejectDialog && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
            <Card className="w-96 p-6 space-y-4">
              <h3 className="font-bold text-slate-900">驳回原因</h3>
              <textarea
                className="w-full p-3 border border-slate-200 rounded-xl text-sm outline-none resize-none"
                rows={3}
                placeholder="请填写驳回原因..."
                value={rejectReason}
                onChange={e => setRejectReason(e.target.value)}
              />
              <div className="flex justify-end gap-3">
                <Button variant="ghost" onClick={() => setShowRejectDialog(false)}>取消</Button>
                <Button className="bg-rose-500 hover:bg-rose-600 text-white" onClick={handleReject}>确认驳回</Button>
              </div>
            </Card>
          </div>
        )}
      </div>
    </AdminLayout>
  );
};

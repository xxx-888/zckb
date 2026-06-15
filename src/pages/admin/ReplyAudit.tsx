import React, { useState, useEffect, useCallback } from 'react';
import {
  FileCheck, Search, CheckCircle, XCircle,
  MessageSquare, User, ShieldAlert, RefreshCw,
  AlertCircle, Sparkles, ChevronLeft, ChevronRight,
  Store, Clock, Filter,
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { AdminLayout } from '../../components/AdminLayout';
import { useToast } from '../../hooks/use-toast';
import { auditApi, AuditItem, AuditStats } from '../../api/audit';
import { useSearchDebounce } from '../../lib/utils';

const statusConfig: Record<string, { label: string; color: string; icon: React.ElementType }> = {
  pending:   { label: '待审核', color: 'bg-amber-100 text-amber-700', icon: AlertCircle },
  approved:  { label: '已通过', color: 'bg-emerald-100 text-emerald-700', icon: CheckCircle },
  rejected:  { label: '已拒绝', color: 'bg-rose-100 text-rose-700', icon: XCircle },
  sent:      { label: '已发送', color: 'bg-blue-100 text-blue-700', icon: FileCheck },
};

const platformLabels: Record<string, string> = {
  meituan: '美团',
  dianping: '大众点评',
  douyin: '抖音',
  taobao: '淘宝',
  jd: '京东',
};

const PAGE_SIZE = 15;

export const ReplyAudit: React.FC = () => {
  const [audits, setAudits] = useState<AuditItem[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [stats, setStats] = useState<AuditStats | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const { inputValue: searchInput, debouncedValue: debouncedSearch, handleChange: handleSearchInput } = useSearchDebounce();
  const [showRejectDialog, setShowRejectDialog] = useState(false);
  const [rejectReason, setRejectReason] = useState('');
  const [rejectTargetId, setRejectTargetId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  const { success, error: toastError } = useToast();

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const params: any = { page, limit: PAGE_SIZE };
      if (statusFilter) params.status = statusFilter;
      if (debouncedSearch) params.keyword = debouncedSearch;

      const [listRes, statsRes] = await Promise.allSettled([
        auditApi.getAuditList(params).catch(err => {
          console.warn('[ReplyAudit] 获取审核列表失败:', err);
          return { items: [], total: 0 };
        }),
        auditApi.getStats().catch(err => {
          console.warn('[ReplyAudit] 获取统计失败:', err);
          return null;
        }),
      ]);

      if (listRes.status === 'fulfilled') {
        const data = listRes.value;
        setAudits(Array.isArray(data?.items) ? data.items : []);
        setTotal(data?.total || 0);
      }
      if (statsRes.status === 'fulfilled') {
        setStats(statsRes.value);
      }
    } catch (err) {
      console.error('[ReplyAudit] fetchData error:', err);
    } finally {
      setLoading(false);
    }
  }, [page, statusFilter, debouncedSearch]);

  useEffect(() => { fetchData(); }, [fetchData]);

  // 切换筛选条件时重置页码
  useEffect(() => { setPage(1); }, [statusFilter, debouncedSearch]);

  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  const handleApprove = async (id: string) => {
    setActionLoading(id);
    try {
      await auditApi.approveAudit(id);
      success('审核通过', '该回复已通过并发布');
      fetchData();
    } catch (err: any) {
      toastError('操作失败', err.message);
    } finally {
      setActionLoading(null);
    }
  };

  const handleReject = async () => {
    if (!rejectTargetId || !rejectReason.trim()) {
      toastError('拒绝失败', '请填写拒绝原因');
      return;
    }
    setActionLoading(rejectTargetId);
    try {
      await auditApi.rejectAudit(rejectTargetId, rejectReason);
      setShowRejectDialog(false);
      setRejectReason('');
      setRejectTargetId(null);
      success('已拒绝', '该回复已拒绝');
      fetchData();
    } catch (err: any) {
      toastError('操作失败', err.message);
    } finally {
      setActionLoading(null);
    }
  };

  const handleRegenerate = async (id: string) => {
    setActionLoading(id);
    try {
      await auditApi.regenerateReply(id);
      success('重新生成', 'AI 回复已重新生成');
      fetchData();
    } catch (err: any) {
      toastError('操作失败', err.message);
    } finally {
      setActionLoading(null);
    }
  };

  const openRejectDialog = (id: string) => {
    setRejectTargetId(id);
    setShowRejectDialog(true);
  };

  const selected = audits.find(a => a.id === selectedId);

  const formatTime = (dateStr?: string | null) => {
    if (!dateStr) return '';
    try {
      const d = new Date(dateStr);
      return `${d.getMonth() + 1}/${d.getDate()} ${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`;
    } catch {
      return '';
    }
  };

  return (
    <AdminLayout>
      <div className="space-y-6 pb-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">回复审核</h1>
            <p className="text-slate-500 text-sm mt-1">AI 生成回复人工审核与管理</p>
          </div>
          <Button variant="outline" size="sm" onClick={fetchData} disabled={loading}>
            <RefreshCw className={`w-4 h-4 mr-1 ${loading ? 'animate-spin' : ''}`} />
            刷新
          </Button>
        </div>

        {/* Stats */}
        {stats && (
          <div className="grid grid-cols-5 gap-3">
            <Card className="p-4 text-center border-amber-200 bg-amber-50/50">
              <p className="text-2xl font-bold text-amber-600">{stats.pending_count}</p>
              <p className="text-xs text-amber-600/70">待审核</p>
            </Card>
            <Card className="p-4 text-center border-emerald-200 bg-emerald-50/50">
              <p className="text-2xl font-bold text-emerald-600">{stats.approved_count}</p>
              <p className="text-xs text-emerald-600/70">已通过</p>
            </Card>
            <Card className="p-4 text-center border-rose-200 bg-rose-50/50">
              <p className="text-2xl font-bold text-rose-600">{stats.rejected_count}</p>
              <p className="text-xs text-rose-600/70">已拒绝</p>
            </Card>
            <Card className="p-4 text-center border-blue-200 bg-blue-50/50">
              <p className="text-2xl font-bold text-blue-600">{stats.sent_count || 0}</p>
              <p className="text-xs text-blue-600/70">已发送</p>
            </Card>
            <Card className="p-4 text-center">
              <p className="text-2xl font-bold text-slate-600">{stats.total_count}</p>
              <p className="text-xs text-slate-400">总计</p>
            </Card>
          </div>
        )}

        {/* Filters: Status Tabs + Search */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1 bg-slate-100 rounded-xl p-1">
            <button
              className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-colors ${
                !statusFilter ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'
              }`}
              onClick={() => setStatusFilter('')}
            >
              全部
            </button>
            {Object.entries(statusConfig).map(([key, cfg]) => (
              <button
                key={key}
                className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-colors ${
                  statusFilter === key ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'
                }`}
                onClick={() => setStatusFilter(key)}
              >
                {cfg.label}
              </button>
            ))}
          </div>

          <div className="relative flex-1 max-w-xs">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              className="w-full pl-10 pr-4 py-2 bg-white border border-slate-200 rounded-xl text-sm outline-none focus:border-indigo-300 focus:ring-2 focus:ring-indigo-100 transition-all"
              placeholder="搜索门店/评论/用户名..."
              value={searchInput}
              onChange={e => handleSearchInput(e.target.value)}
            />
          </div>

          <span className="text-xs text-slate-400 ml-auto">
            共 {total} 条
          </span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* List */}
          <div className="lg:col-span-1 space-y-2 max-h-[70vh] overflow-y-auto pr-1">
            {loading && audits.length === 0 ? (
              <div className="flex items-center justify-center h-48">
                <RefreshCw className="w-6 h-6 text-slate-400 animate-spin" />
              </div>
            ) : audits.length === 0 ? (
              <div className="text-center py-12 text-slate-400">
                <FileCheck className="w-10 h-10 mx-auto mb-3 opacity-50" />
                <p>{debouncedSearch || statusFilter ? '无匹配结果' : '暂无审核项'}</p>
              </div>
            ) : (
              audits.map(a => {
                const StatusIcon = statusConfig[a.status]?.icon || AlertCircle;
                return (
                  <Card
                    key={a.id}
                    className={`p-3.5 cursor-pointer transition-all border-slate-100 shadow-sm hover:shadow-md ${
                      selectedId === a.id ? 'ring-2 ring-indigo-400 border-indigo-200 bg-indigo-50/30' : 'hover:border-slate-200'
                    }`}
                    onClick={() => setSelectedId(a.id)}
                  >
                    <div className="flex items-center justify-between mb-1.5">
                      <div className="flex items-center gap-2 min-w-0">
                        <Store className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
                        <span className="font-medium text-slate-900 text-sm truncate">{a.store_name || '未知门店'}</span>
                      </div>
                      <Badge className={`text-[10px] px-1.5 py-0 ${statusConfig[a.status]?.color || ''}`}>
                        {statusConfig[a.status]?.label || a.status}
                      </Badge>
                    </div>
                    <p className="text-xs text-slate-500 line-clamp-2 leading-relaxed">{a.content || '无评论内容'}</p>
                    <div className="flex items-center gap-2 mt-2 text-xs text-slate-400">
                      <User className="w-3 h-3" />
                      <span>{a.user_name || '匿名'}</span>
                      {a.platform && (
                        <>
                          <span>·</span>
                          <span>{platformLabels[a.platform] || a.platform}</span>
                        </>
                      )}
                      <span>·</span>
                      <Clock className="w-3 h-3" />
                      <span>{formatTime(a.created_at)}</span>
                    </div>
                  </Card>
                );
              })
            )}

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-center gap-2 pt-3">
                <Button
                  variant="outline"
                  size="sm"
                  className="h-8 w-8 p-0"
                  disabled={page <= 1 || loading}
                  onClick={() => setPage(p => Math.max(1, p - 1))}
                >
                  <ChevronLeft className="w-4 h-4" />
                </Button>
                <span className="text-xs text-slate-500 min-w-[80px] text-center">
                  {page} / {totalPages}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  className="h-8 w-8 p-0"
                  disabled={page >= totalPages || loading}
                  onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                >
                  <ChevronRight className="w-4 h-4" />
                </Button>
              </div>
            )}
          </div>

          {/* Detail */}
          <div className="lg:col-span-2">
            {selected ? (
              <Card className="p-6 border-slate-100 shadow-sm space-y-5">
                {/* Header */}
                <div className="flex items-center justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <Store className="w-4 h-4 text-slate-400" />
                      <h3 className="font-bold text-slate-900">{selected.store_name || '未知门店'}</h3>
                    </div>
                    <p className="text-sm text-slate-500 mt-1">
                      {(selected.platform && platformLabels[selected.platform]) || selected.platform || '未知平台'} · {selected.user_name || '匿名用户'}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    {selected.risk_level && (
                      <Badge className={`text-xs ${
                        selected.risk_level === 'high' ? 'bg-rose-100 text-rose-700' :
                        selected.risk_level === 'medium' ? 'bg-amber-100 text-amber-700' :
                        'bg-emerald-100 text-emerald-700'
                      }`}>
                        {selected.risk_level === 'high' ? '高风险' : selected.risk_level === 'medium' ? '中风险' : '低风险'}
                      </Badge>
                    )}
                    <Badge className={statusConfig[selected.status]?.color}>
                      {statusConfig[selected.status]?.label || selected.status}
                    </Badge>
                  </div>
                </div>

                {/* Original Review */}
                <div className="bg-slate-50 rounded-xl p-4">
                  <p className="text-xs text-slate-400 mb-1.5 font-medium">用户评价</p>
                  <p className="text-sm text-slate-700 leading-relaxed">{selected.content || '无内容'}</p>
                  <div className="flex items-center gap-3 mt-2">
                    {selected.rating && (
                      <span className="text-amber-500 text-sm">{'★'.repeat(selected.rating)}{'☆'.repeat(5 - selected.rating)}</span>
                    )}
                    {selected.created_at && (
                      <span className="text-xs text-slate-400">{formatTime(selected.created_at)}</span>
                    )}
                  </div>
                </div>

                {/* AI Reply */}
                <div className="bg-indigo-50 rounded-xl p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Sparkles className="w-4 h-4 text-indigo-500" />
                    <p className="text-xs text-indigo-500 font-medium">AI 生成回复</p>
                  </div>
                  <p className="text-sm text-slate-700 leading-relaxed whitespace-pre-wrap">{selected.ai_reply || '暂无'}</p>
                </div>

                {/* Scores */}
                {selected.scores && (
                  <div className="grid grid-cols-4 gap-2 text-center text-xs">
                    {[
                      { key: 'realism', label: '真实性' },
                      { key: 'empathy', label: '共情度' },
                      { key: 'concreteness', label: '具体性' },
                      { key: 'consistency', label: '一致性' },
                    ].map(({ key, label }) => {
                      const val = (selected.scores as any)?.[key];
                      if (val == null) return null;
                      const pct = typeof val === 'number' && val <= 1 ? Math.round(val * 100) : val;
                      return (
                        <div key={key} className="bg-slate-50 rounded-lg p-2.5">
                          <p className="text-slate-400 text-[10px]">{label}</p>
                          <p className="font-bold text-slate-700">{pct}{typeof val === 'number' && val <= 1 ? '%' : ''}</p>
                        </div>
                      );
                    })}
                  </div>
                )}

                {/* Reject reason */}
                {selected.reject_reason && (
                  <div className="bg-rose-50 rounded-xl p-3 border border-rose-100">
                    <p className="text-xs text-rose-600"><span className="font-medium">拒绝原因：</span>{selected.reject_reason}</p>
                  </div>
                )}

                {/* Audit info */}
                {selected.reviewed_at && (
                  <div className="text-xs text-slate-400">
                    {selected.auditor_name && <span>审核人: {selected.auditor_name} · </span>}
                    <span>审核时间: {formatTime(selected.reviewed_at)}</span>
                  </div>
                )}

                {/* Actions */}
                {selected.status === 'pending' && (
                  <div className="flex items-center gap-3 pt-2 border-t border-slate-100">
                    <Button
                      size="sm"
                      className="bg-emerald-500 hover:bg-emerald-600 text-white"
                      onClick={() => handleApprove(selected.id)}
                      disabled={actionLoading === selected.id}
                    >
                      {actionLoading === selected.id ? <RefreshCw className="w-4 h-4 mr-1 animate-spin" /> : <CheckCircle className="w-4 h-4 mr-1" />}
                      通过并发布
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      className="text-rose-500 border-rose-200 hover:bg-rose-50"
                      onClick={() => openRejectDialog(selected.id)}
                      disabled={actionLoading === selected.id}
                    >
                      <XCircle className="w-4 h-4 mr-1" />驳回
                    </Button>
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => handleRegenerate(selected.id)}
                      disabled={actionLoading === selected.id}
                    >
                      {actionLoading === selected.id ? <RefreshCw className="w-4 h-4 mr-1 animate-spin" /> : <RefreshCw className="w-4 h-4 mr-1" />}
                      重新生成
                    </Button>
                  </div>
                )}
              </Card>
            ) : (
              <div className="flex flex-col items-center justify-center h-64 text-slate-400">
                <ShieldAlert className="w-10 h-10 mb-3 opacity-50" />
                <p>{audits.length > 0 ? '选择左侧审核项查看详情' : '暂无审核数据'}</p>
              </div>
            )}
          </div>
        </div>

        {/* Reject Dialog */}
        {showRejectDialog && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
            <Card className="w-96 p-6 space-y-4 shadow-2xl">
              <h3 className="font-bold text-slate-900">驳回原因</h3>
              <textarea
                className="w-full p-3 border border-slate-200 rounded-xl text-sm outline-none resize-none focus:border-rose-300 focus:ring-2 focus:ring-rose-100 transition-all"
                rows={3}
                placeholder="请填写驳回原因..."
                value={rejectReason}
                onChange={e => setRejectReason(e.target.value)}
                autoFocus
              />
              <div className="flex justify-end gap-3">
                <Button variant="ghost" onClick={() => { setShowRejectDialog(false); setRejectReason(''); setRejectTargetId(null); }}>取消</Button>
                <Button className="bg-rose-500 hover:bg-rose-600 text-white" onClick={handleReject} disabled={!rejectReason.trim()}>
                  确认驳回
                </Button>
              </div>
            </Card>
          </div>
        )}
      </div>
    </AdminLayout>
  );
};

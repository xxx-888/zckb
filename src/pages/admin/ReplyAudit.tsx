import React, { useState, useEffect, useCallback } from 'react';
import {
  FileCheck, Search, CheckCircle, XCircle,
  RefreshCw, AlertCircle, Sparkles, ChevronLeft, ChevronRight,
  Clock, Eye,
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

const riskLabels: Record<string, { text: string; cls: string }> = {
  high:   { text: '高', cls: 'bg-rose-100 text-rose-700' },
  medium: { text: '中', cls: 'bg-amber-100 text-amber-700' },
  low:    { text: '低', cls: 'bg-emerald-100 text-emerald-700' },
};

const PAGE_SIZE = 15;

type DialogType = 'approve' | 'reject' | 'regenerate' | 'detail' | null;

export const ReplyAudit: React.FC = () => {
  const [audits, setAudits] = useState<AuditItem[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [stats, setStats] = useState<AuditStats | null>(null);
  const { inputValue: searchInput, debouncedValue: debouncedSearch, handleChange: handleSearchInput } = useSearchDebounce();
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  // 弹窗状态
  const [dialogType, setDialogType] = useState<DialogType>(null);
  const [dialogTarget, setDialogTarget] = useState<AuditItem | null>(null);
  const [rejectReason, setRejectReason] = useState('');

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
  useEffect(() => { setPage(1); }, [statusFilter, debouncedSearch]);

  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  // ── 操作处理 ──
  const openDialog = (type: DialogType, item: AuditItem) => {
    setDialogType(type);
    setDialogTarget(item);
    if (type === 'reject') setRejectReason('');
  };
  const closeDialog = () => {
    setDialogType(null);
    setDialogTarget(null);
    setRejectReason('');
  };

  const handleApprove = async () => {
    if (!dialogTarget) return;
    setActionLoading(dialogTarget.id);
    try {
      await auditApi.approveAudit(dialogTarget.id);
      success('审核通过', '该回复已通过并发布');
      closeDialog();
      fetchData();
    } catch (err: any) {
      toastError('操作失败', err.message);
    } finally {
      setActionLoading(null);
    }
  };

  const handleReject = async () => {
    if (!dialogTarget || !rejectReason.trim()) {
      toastError('拒绝失败', '请填写拒绝原因');
      return;
    }
    setActionLoading(dialogTarget.id);
    try {
      await auditApi.rejectAudit(dialogTarget.id, rejectReason);
      success('已拒绝', '该回复已拒绝');
      closeDialog();
      fetchData();
    } catch (err: any) {
      toastError('操作失败', err.message);
    } finally {
      setActionLoading(null);
    }
  };

  const handleRegenerate = async () => {
    if (!dialogTarget) return;
    setActionLoading(dialogTarget.id);
    try {
      await auditApi.regenerateReply(dialogTarget.id);
      success('重新生成', 'AI 回复已重新生成');
      closeDialog();
      fetchData();
    } catch (err: any) {
      toastError('操作失败', err.message);
    } finally {
      setActionLoading(null);
    }
  };

  const formatTime = (dateStr?: string | null) => {
    if (!dateStr) return '-';
    try {
      const d = new Date(dateStr);
      return `${d.getMonth() + 1}/${d.getDate()} ${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`;
    } catch {
      return '-';
    }
  };

  const truncate = (str: string | null, len: number) => {
    if (!str) return '-';
    return str.length > len ? str.slice(0, len) + '...' : str;
  };

  return (
    <AdminLayout>
      <div className="space-y-5 pb-8">
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

        {/* Filters */}
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

        {/* ── 表格 ── */}
        <Card className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200">
                  <th className="text-left px-4 py-3 font-medium text-slate-500 whitespace-nowrap">门店</th>
                  <th className="text-left px-4 py-3 font-medium text-slate-500 whitespace-nowrap">用户</th>
                  <th className="text-left px-4 py-3 font-medium text-slate-500 whitespace-nowrap">平台</th>
                  <th className="text-left px-4 py-3 font-medium text-slate-500 whitespace-nowrap">评分</th>
                  <th className="text-left px-4 py-3 font-medium text-slate-500 whitespace-nowrap">评论内容</th>
                  <th className="text-left px-4 py-3 font-medium text-slate-500 whitespace-nowrap">AI 回复</th>
                  <th className="text-left px-4 py-3 font-medium text-slate-500 whitespace-nowrap">风险</th>
                  <th className="text-left px-4 py-3 font-medium text-slate-500 whitespace-nowrap">状态</th>
                  <th className="text-left px-4 py-3 font-medium text-slate-500 whitespace-nowrap">提交时间</th>
                  <th className="text-center px-4 py-3 font-medium text-slate-500 whitespace-nowrap">操作</th>
                </tr>
              </thead>
              <tbody>
                {loading && audits.length === 0 ? (
                  <tr>
                    <td colSpan={10} className="text-center py-16">
                      <RefreshCw className="w-6 h-6 text-slate-400 animate-spin mx-auto" />
                      <p className="text-slate-400 mt-2">加载中...</p>
                    </td>
                  </tr>
                ) : audits.length === 0 ? (
                  <tr>
                    <td colSpan={10} className="text-center py-16">
                      <FileCheck className="w-10 h-10 mx-auto mb-3 text-slate-300" />
                      <p className="text-slate-400">{debouncedSearch || statusFilter ? '无匹配结果' : '暂无审核项'}</p>
                    </td>
                  </tr>
                ) : (
                  audits.map(a => {
                    const risk = a.risk_level ? riskLabels[a.risk_level] : null;
                    const isActing = actionLoading === a.id;
                    return (
                      <tr
                        key={a.id}
                        className="border-b border-slate-100 hover:bg-slate-50/60 transition-colors"
                      >
                        {/* 门店 */}
                        <td className="px-4 py-3 whitespace-nowrap">
                          <span className="font-medium text-slate-800">{a.store_name || '-'}</span>
                        </td>
                        {/* 用户 */}
                        <td className="px-4 py-3 whitespace-nowrap text-slate-600">
                          {a.user_name || '-'}
                        </td>
                        {/* 平台 */}
                        <td className="px-4 py-3 whitespace-nowrap">
                          <span className="text-slate-600">{platformLabels[a.platform || ''] || a.platform || '-'}</span>
                        </td>
                        {/* 评分 */}
                        <td className="px-4 py-3 whitespace-nowrap">
                          <span className="text-amber-500">{'★'.repeat(a.rating || 0)}{'☆'.repeat(5 - (a.rating || 0))}</span>
                        </td>
                        {/* 评论内容 */}
                        <td className="px-4 py-3 max-w-[200px]">
                          <span className="text-slate-600 line-clamp-2">{truncate(a.content, 40)}</span>
                        </td>
                        {/* AI 回复 */}
                        <td className="px-4 py-3 max-w-[200px]">
                          <span className="text-slate-600 line-clamp-2">{truncate(a.ai_reply, 40)}</span>
                        </td>
                        {/* 风险 */}
                        <td className="px-4 py-3 whitespace-nowrap">
                          {risk ? (
                            <Badge className={`text-[10px] px-1.5 py-0 ${risk.cls}`}>{risk.text}</Badge>
                          ) : '-'}
                        </td>
                        {/* 状态 */}
                        <td className="px-4 py-3 whitespace-nowrap">
                          <Badge className={`text-[10px] px-1.5 py-0 ${statusConfig[a.status]?.color || ''}`}>
                            {statusConfig[a.status]?.label || a.status}
                          </Badge>
                        </td>
                        {/* 提交时间 */}
                        <td className="px-4 py-3 whitespace-nowrap text-slate-400 text-xs">
                          {formatTime(a.created_at)}
                        </td>
                        {/* 操作 */}
                        <td className="px-4 py-3 whitespace-nowrap text-center">
                          <div className="flex items-center justify-center gap-1">
                            <Button
                              variant="ghost"
                              size="sm"
                              className="h-7 px-2 text-xs text-indigo-600 hover:text-indigo-800 hover:bg-indigo-50"
                              onClick={() => openDialog('detail', a)}
                            >
                              <Eye className="w-3.5 h-3.5 mr-0.5" />
                              详情
                            </Button>
                            {a.status === 'pending' && (
                              <>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  className="h-7 px-2 text-xs text-emerald-600 hover:text-emerald-800 hover:bg-emerald-50"
                                  onClick={() => openDialog('approve', a)}
                                  disabled={isActing}
                                >
                                  <CheckCircle className="w-3.5 h-3.5 mr-0.5" />
                                  通过
                                </Button>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  className="h-7 px-2 text-xs text-rose-600 hover:text-rose-800 hover:bg-rose-50"
                                  onClick={() => openDialog('reject', a)}
                                  disabled={isActing}
                                >
                                  <XCircle className="w-3.5 h-3.5 mr-0.5" />
                                  驳回
                                </Button>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  className="h-7 px-2 text-xs text-slate-500 hover:text-slate-700 hover:bg-slate-50"
                                  onClick={() => openDialog('regenerate', a)}
                                  disabled={isActing}
                                >
                                  <Sparkles className="w-3.5 h-3.5 mr-0.5" />
                                  重新生成
                                </Button>
                              </>
                            )}
                          </div>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>

          {/* 分页 */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between px-4 py-3 border-t border-slate-100 bg-slate-50/50">
              <span className="text-xs text-slate-400">
                第 {(page - 1) * PAGE_SIZE + 1}-{Math.min(page * PAGE_SIZE, total)} 条，共 {total} 条
              </span>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  className="h-8 w-8 p-0"
                  disabled={page <= 1 || loading}
                  onClick={() => setPage(p => Math.max(1, p - 1))}
                >
                  <ChevronLeft className="w-4 h-4" />
                </Button>
                <span className="text-xs text-slate-500 min-w-[60px] text-center">
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
            </div>
          )}
        </Card>

        {/* ── 弹窗：详情 ── */}
        {dialogType === 'detail' && dialogTarget && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={closeDialog}>
            <Card
              className="w-[560px] max-h-[80vh] overflow-y-auto p-6 space-y-5 shadow-2xl"
              onClick={e => e.stopPropagation()}
            >
              <div className="flex items-center justify-between">
                <h3 className="font-bold text-slate-900 text-lg">审核详情</h3>
                <div className="flex items-center gap-2">
                  {dialogTarget.risk_level && (
                    <Badge className={`text-xs ${
                      riskLabels[dialogTarget.risk_level]?.cls || ''
                    }`}>
                      {riskLabels[dialogTarget.risk_level]?.text || dialogTarget.risk_level}风险
                    </Badge>
                  )}
                  <Badge className={statusConfig[dialogTarget.status]?.color}>
                    {statusConfig[dialogTarget.status]?.label || dialogTarget.status}
                  </Badge>
                </div>
              </div>

              {/* 基本信息 */}
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <span className="text-slate-400">门店：</span>
                  <span className="text-slate-800 font-medium">{dialogTarget.store_name || '-'}</span>
                </div>
                <div>
                  <span className="text-slate-400">用户：</span>
                  <span className="text-slate-800">{dialogTarget.user_name || '-'}</span>
                </div>
                <div>
                  <span className="text-slate-400">平台：</span>
                  <span className="text-slate-800">{platformLabels[dialogTarget.platform || ''] || dialogTarget.platform || '-'}</span>
                </div>
                <div>
                  <span className="text-slate-400">评分：</span>
                  <span className="text-amber-500">{'★'.repeat(dialogTarget.rating || 0)}{'☆'.repeat(5 - (dialogTarget.rating || 0))}</span>
                </div>
                <div>
                  <span className="text-slate-400">提交时间：</span>
                  <span className="text-slate-800">{formatTime(dialogTarget.created_at)}</span>
                </div>
                {dialogTarget.reviewed_at && (
                  <div>
                    <span className="text-slate-400">审核时间：</span>
                    <span className="text-slate-800">{formatTime(dialogTarget.reviewed_at)}</span>
                  </div>
                )}
                {dialogTarget.auditor_name && (
                  <div>
                    <span className="text-slate-400">审核人：</span>
                    <span className="text-slate-800">{dialogTarget.auditor_name}</span>
                  </div>
                )}
              </div>

              {/* 评论内容 */}
              <div className="bg-slate-50 rounded-xl p-4">
                <p className="text-xs text-slate-400 mb-1.5 font-medium">用户评价</p>
                <p className="text-sm text-slate-700 leading-relaxed break-words">{dialogTarget.content || '无内容'}</p>
              </div>

              {/* AI 回复 */}
              <div className="bg-indigo-50 rounded-xl p-4">
                <div className="flex items-center gap-2 mb-2">
                  <Sparkles className="w-4 h-4 text-indigo-500" />
                  <p className="text-xs text-indigo-500 font-medium">AI 生成回复</p>
                </div>
                <p className="text-sm text-slate-700 leading-relaxed whitespace-pre-wrap break-words">{dialogTarget.ai_reply || '暂无'}</p>
              </div>

              {/* 评分 */}
              {dialogTarget.scores && (
                <div className="grid grid-cols-4 gap-2 text-center text-xs">
                  {[
                    { key: 'realism', label: '真实性' },
                    { key: 'empathy', label: '共情度' },
                    { key: 'concreteness', label: '具体性' },
                    { key: 'consistency', label: '一致性' },
                  ].map(({ key, label }) => {
                    const val = (dialogTarget.scores as any)?.[key];
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

              {/* 拒绝原因 */}
              {dialogTarget.reject_reason && (
                <div className="bg-rose-50 rounded-xl p-3 border border-rose-100">
                  <p className="text-xs text-rose-600"><span className="font-medium">拒绝原因：</span>{dialogTarget.reject_reason}</p>
                </div>
              )}

              {/* 操作按钮（仅 pending） */}
              {dialogTarget.status === 'pending' && (
                <div className="flex items-center gap-3 pt-2 border-t border-slate-100">
                  <Button
                    size="sm"
                    className="bg-emerald-500 hover:bg-emerald-600 text-white"
                    onClick={() => { setDialogType('approve'); }}
                    disabled={actionLoading === dialogTarget.id}
                  >
                    <CheckCircle className="w-4 h-4 mr-1" />
                    通过并发布
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    className="text-rose-500 border-rose-200 hover:bg-rose-50"
                    onClick={() => { setDialogType('reject'); setRejectReason(''); }}
                    disabled={actionLoading === dialogTarget.id}
                  >
                    <XCircle className="w-4 h-4 mr-1" />驳回
                  </Button>
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => { setDialogType('regenerate'); }}
                    disabled={actionLoading === dialogTarget.id}
                  >
                    <Sparkles className="w-4 h-4 mr-1" />
                    重新生成
                  </Button>
                </div>
              )}

              <div className="flex justify-end">
                <Button variant="outline" size="sm" onClick={closeDialog}>关闭</Button>
              </div>
            </Card>
          </div>
        )}

        {/* ── 弹窗：确认通过 ── */}
        {dialogType === 'approve' && dialogTarget && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={closeDialog}>
            <Card className="w-96 p-6 space-y-5 shadow-2xl" onClick={e => e.stopPropagation()}>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-emerald-100 flex items-center justify-center">
                  <CheckCircle className="w-5 h-5 text-emerald-600" />
                </div>
                <div>
                  <h3 className="font-bold text-slate-900">确认通过</h3>
                  <p className="text-xs text-slate-500">通过后 AI 回复将正式发布到平台</p>
                </div>
              </div>

              <div className="bg-slate-50 rounded-lg p-3 text-xs text-slate-600 space-y-1">
                <p><span className="text-slate-400">门店：</span>{dialogTarget.store_name || '-'}</p>
                <p><span className="text-slate-400">用户：</span>{dialogTarget.user_name || '-'}</p>
                <p><span className="text-slate-400">回复：</span>{truncate(dialogTarget.ai_reply, 60)}</p>
              </div>

              <div className="flex justify-end gap-3">
                <Button variant="ghost" onClick={closeDialog}>取消</Button>
                <Button
                  className="bg-emerald-500 hover:bg-emerald-600 text-white"
                  onClick={handleApprove}
                  disabled={actionLoading === dialogTarget.id}
                >
                  {actionLoading === dialogTarget.id ? <RefreshCw className="w-4 h-4 mr-1 animate-spin" /> : <CheckCircle className="w-4 h-4 mr-1" />}
                  确认通过
                </Button>
              </div>
            </Card>
          </div>
        )}

        {/* ── 弹窗：驳回 ── */}
        {dialogType === 'reject' && dialogTarget && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={closeDialog}>
            <Card className="w-96 p-6 space-y-5 shadow-2xl" onClick={e => e.stopPropagation()}>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-rose-100 flex items-center justify-center">
                  <XCircle className="w-5 h-5 text-rose-600" />
                </div>
                <div>
                  <h3 className="font-bold text-slate-900">驳回回复</h3>
                  <p className="text-xs text-slate-500">请填写驳回原因</p>
                </div>
              </div>

              <div className="bg-slate-50 rounded-lg p-3 text-xs text-slate-600 space-y-1">
                <p><span className="text-slate-400">门店：</span>{dialogTarget.store_name || '-'}</p>
                <p><span className="text-slate-400">用户：</span>{dialogTarget.user_name || '-'}</p>
                <p><span className="text-slate-400">回复：</span>{truncate(dialogTarget.ai_reply, 60)}</p>
              </div>

              <textarea
                className="w-full p-3 border border-slate-200 rounded-xl text-sm outline-none resize-none focus:border-rose-300 focus:ring-2 focus:ring-rose-100 transition-all"
                rows={3}
                placeholder="请填写驳回原因..."
                value={rejectReason}
                onChange={e => setRejectReason(e.target.value)}
                autoFocus
              />
              <div className="flex justify-end gap-3">
                <Button variant="ghost" onClick={closeDialog}>取消</Button>
                <Button
                  className="bg-rose-500 hover:bg-rose-600 text-white"
                  onClick={handleReject}
                  disabled={!rejectReason.trim() || actionLoading === dialogTarget.id}
                >
                  {actionLoading === dialogTarget.id ? <RefreshCw className="w-4 h-4 mr-1 animate-spin" /> : <XCircle className="w-4 h-4 mr-1" />}
                  确认驳回
                </Button>
              </div>
            </Card>
          </div>
        )}

        {/* ── 弹窗：重新生成 ── */}
        {dialogType === 'regenerate' && dialogTarget && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={closeDialog}>
            <Card className="w-96 p-6 space-y-5 shadow-2xl" onClick={e => e.stopPropagation()}>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center">
                  <Sparkles className="w-5 h-5 text-indigo-600" />
                </div>
                <div>
                  <h3 className="font-bold text-slate-900">重新生成 AI 回复</h3>
                  <p className="text-xs text-slate-500">将覆盖当前 AI 回复内容</p>
                </div>
              </div>

              <div className="bg-slate-50 rounded-lg p-3 text-xs text-slate-600 space-y-1">
                <p><span className="text-slate-400">门店：</span>{dialogTarget.store_name || '-'}</p>
                <p><span className="text-slate-400">当前回复：</span>{truncate(dialogTarget.ai_reply, 60)}</p>
              </div>

              <div className="flex justify-end gap-3">
                <Button variant="ghost" onClick={closeDialog}>取消</Button>
                <Button
                  className="bg-indigo-500 hover:bg-indigo-600 text-white"
                  onClick={handleRegenerate}
                  disabled={actionLoading === dialogTarget.id}
                >
                  {actionLoading === dialogTarget.id ? <RefreshCw className="w-4 h-4 mr-1 animate-spin" /> : <Sparkles className="w-4 h-4 mr-1" />}
                  确认重新生成
                </Button>
              </div>
            </Card>
          </div>
        )}
      </div>
    </AdminLayout>
  );
};

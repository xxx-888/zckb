import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  AlertCircle,
  CheckCircle2,
  XCircle,
  RefreshCw,
  Search,
  Filter,
  ChevronLeft,
  ChevronRight,
  Download,
  Trash2,
  Eye,
  MessageSquare,
  Send,
  AlertTriangle,
  Lightbulb
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { AdminLayout } from '../../components/AdminLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';
import { fetchNegativeReplyTasks, negativeReplyApi } from '../../api/negative-reply';
import type { NegativeReplyTask } from '../../api/negative-reply';

export const NegativeReply: React.FC = () => {
  const [tasks, setTasks] = useState<NegativeReplyTask[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [searchKeyword, setSearchKeyword] = useState('');
  const [filterRisk, setFilterRisk] = useState<'all' | 'high' | 'medium' | 'low'>('all');
  const pageSize = 10;

  const navigate = useNavigate();
  const { success, error: showError } = useToast();
  const fetchedRef = React.useRef(false);

  const loadData = async (page: number = 1) => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchNegativeReplyTasks(
        undefined,
        page,
        pageSize,
        searchKeyword || undefined,
        filterRisk || undefined
      );
      setTasks(data.items || []);
      setTotal(data.total || 0);
      setCurrentPage(data.page || page);
    } catch (err) {
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  const getAvgScore = (task: NegativeReplyTask) => {
    const s = task.scores || { realism: 7, empathy: 7, concreteness: 7, consistency: 7 };
    const vals = Object.values(s) as number[];
    return (vals.reduce((a, b) => a + b, 0) / vals.length).toFixed(1);
  };

  const handleSelectAll = (checked: boolean) => {
    if (checked) {
      setSelectedIds(tasks.map(t => Number(t.id)));
    } else {
      setSelectedIds([]);
    }
  };

  const handleSelectTask = (id: number, checked: boolean) => {
    if (checked) {
      setSelectedIds([...selectedIds, id]);
    } else {
      setSelectedIds(selectedIds.filter(i => i !== id));
    }
  };

  const handleApprove = async (taskId: string) => {
    try {
      await negativeReplyApi.approveTask(taskId);
      success('审核通过', `回复已发送 (ID: ${taskId})`);
      loadData(currentPage);
    } catch (err) {
      showError('操作失败', err instanceof Error ? err.message : '请重试');
    }
  };

  const handleReject = async (taskId: string) => {
    try {
      await negativeReplyApi.rejectTask(taskId, '管理员驳回，需人工处理');
      success('已驳回', `AI 回复已驳回 (ID: ${taskId})`);
      loadData(currentPage);
    } catch (err) {
      showError('操作失败', err instanceof Error ? err.message : '请重试');
    }
  };

  const handleViewDetail = (reviewId: string) => {
    navigate(`/admin/review-detail/${reviewId}`);
  };

  const handleBatchApprove = async () => {
    try {
      await Promise.all(selectedIds.map(id => negativeReplyApi.approveTask(String(id))));
      success('批量审核', `已批量通过 ${selectedIds.length} 条差评回复`);
      setSelectedIds([]);
      loadData(currentPage);
    } catch (err) {
      showError('操作失败', err instanceof Error ? err.message : '请重试');
    }
  };

  const handleBatchReject = async () => {
    try {
      await Promise.all(selectedIds.map(id => negativeReplyApi.rejectTask(String(id), '管理员批量驳回')));
      success('批量驳回', `已批量驳回 ${selectedIds.length} 条差评回复`);
      setSelectedIds([]);
      loadData(currentPage);
    } catch (err) {
      showError('操作失败', err instanceof Error ? err.message : '请重试');
    }
  };

  const handleExport = () => {
    success('导出报告', '正在导出差评处理报告...');
  };

  // 搜索和筛选变化时重新加载
  useEffect(() => {
    setCurrentPage(1);
    loadData(1);
  }, [searchKeyword, filterRisk]);

  // 分页变化时加载数据
  useEffect(() => {
    if (fetchedRef.current) {
      loadData(currentPage);
    }
  }, [currentPage]);

  // 初始加载
  useEffect(() => {
    if (fetchedRef.current) return;
    fetchedRef.current = true;
    loadData(1);
  }, []);

  if (loading) {
    return (
      <AdminLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="w-12 h-12 border-4 border-orange-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-sm text-slate-400">加载中...</p>
          </div>
        </div>
      </AdminLayout>
    );
  }

  if (error) {
    return (
      <AdminLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <p className="text-sm text-rose-500 mb-4">{error}</p>
            <Button onClick={() => loadData(currentPage)} className="bg-orange-500 hover:bg-orange-600 text-white">
              重试
            </Button>
          </div>
        </div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">差评危机处理</h2>
            <p className="text-slate-500 mt-1">管理所有差评回复任务，审核AI生成的回复草稿</p>
          </div>
          <div className="flex gap-3">
            <Button variant="outline" className="gap-2" onClick={handleExport}>
              <Download className="w-4 h-4" />
              导出报告
            </Button>
            <Button className="bg-orange-500 hover:bg-orange-600 text-white gap-2" onClick={() => loadData(1)}>
              <RefreshCw className="w-4 h-4" />
              刷新数据
            </Button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[
            { label: '待处理差评', value: tasks.length, color: 'text-rose-600', bg: 'bg-rose-50' },
            { label: '高风险', value: tasks.filter(t => t.risk === 'high').length, color: 'text-rose-600', bg: 'bg-rose-50' },
            { label: '中风险', value: tasks.filter(t => t.risk === 'medium').length, color: 'text-amber-600', bg: 'bg-amber-50' },
            { label: '低风险', value: tasks.filter(t => t.risk === 'low').length, color: 'text-yellow-600', bg: 'bg-yellow-50' },
          ].map((stat, i) => (
            <Card key={i} className="p-6 border-none shadow-sm">
              <div className="flex items-center gap-4">
                <div className={`p-3 rounded-xl ${stat.bg}`}>
                  <AlertCircle className={`w-6 h-6 ${stat.color}`} />
                </div>
                <div>
                  <p className="text-sm text-slate-500">{stat.label}</p>
                  <p className="text-2xl font-bold text-slate-900">{stat.value}</p>
                </div>
              </div>
            </Card>
          ))}
        </div>

        {/* Filters and Search */}
        <Card className="p-4 border-none shadow-sm">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <Input
                placeholder="搜索用户名或评论内容..."
                className="pl-9"
                value={searchKeyword}
                onChange={(e) => setSearchKeyword(e.target.value)}
              />
            </div>
            <div className="flex gap-2">
              {['all', 'high', 'medium', 'low'].map((risk) => (
                <Button
                  key={risk}
                  variant={filterRisk === risk ? 'default' : 'outline'}
                  className={cn(
                    "capitalize",
                    filterRisk === risk && "bg-orange-500 hover:bg-orange-600 text-white"
                  )}
                  onClick={() => setFilterRisk(risk as any)}
                >
                  {risk === 'all' ? '全部' : risk === 'high' ? '高风险' : risk === 'medium' ? '中风险' : '低风险'}
                </Button>
              ))}
            </div>
          </div>
        </Card>

        {/* Batch Actions */}
        {selectedIds.length > 0 && (
          <Card className="p-4 border-none shadow-sm bg-orange-50 border-orange-200">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-orange-900">
                已选择 {selectedIds.length} 条任务
              </span>
              <div className="flex gap-2">
                <Button
                  size="sm"
                  className="bg-emerald-500 hover:bg-emerald-600 text-white gap-1"
                  onClick={handleBatchApprove}
                >
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  批量通过
                </Button>
                <Button
                  size="sm"
                  className="bg-rose-500 hover:bg-rose-600 text-white gap-1"
                  onClick={handleBatchReject}
                >
                  <XCircle className="w-3.5 h-3.5" />
                  批量驳回
                </Button>
              </div>
            </div>
          </Card>
        )}

        {/* Task List */}
        <Card className="border-none shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50 border-b border-slate-100">
                <tr>
                  <th className="p-4 text-left">
                    <input
                      type="checkbox"
                      checked={selectedIds.length === tasks.length && tasks.length > 0}
                      onChange={(e) => handleSelectAll(e.target.checked)}
                      className="rounded border-slate-300"
                    />
                  </th>
                  <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">用户</th>
                  <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">评分</th>
                  <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">评论内容</th>
                  <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">风险等级</th>
                  <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">AI回复质量</th>
                  <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">操作</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50">
                {tasks.map((task) => {
                  const avgScore = parseFloat(getAvgScore(task));
                  const isLowScore = avgScore < 7;
                  const isSelected = selectedIds.includes(Number(task.id));

                  return (
                    <tr key={task.id} className={cn("hover:bg-slate-50 transition-colors", isSelected && "bg-orange-50")}>
                      <td className="p-4">
                        <input
                          type="checkbox"
                          checked={isSelected}
                          onChange={(e) => handleSelectTask(Number(task.id), e.target.checked)}
                          className="rounded border-slate-300"
                        />
                      </td>
                      <td className="p-4">
                        <div className="flex items-center gap-3">
                          <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center">
                            <span className="text-xs font-bold text-slate-600">{(task.user_name || task.user || '?')[0]}</span>
                          </div>
                          <div>
                            <p className="text-sm font-medium text-slate-900">{task.user_name || task.user}</p>
                            <p className="text-xs text-slate-400">{task.platform}</p>
                          </div>
                        </div>
                      </td>
                      <td className="p-4">
                        <div className="flex items-center gap-1">
                          {[1, 2, 3, 4, 5].map(star => (
                            <span key={star} className={cn("text-sm", star <= task.rating ? "text-amber-400" : "text-slate-200")}>★</span>
                          ))}
                        </div>
                      </td>
                      <td className="p-4 max-w-xs">
                        <p className="text-sm text-slate-600 line-clamp-2">{task.content}</p>
                      </td>
                      <td className="p-4">
                        <Badge className={cn(
                          "border-none text-xs",
                          task.risk === 'high' && "bg-rose-100 text-rose-700",
                          task.risk === 'medium' && "bg-amber-100 text-amber-700",
                          task.risk === 'low' && "bg-yellow-100 text-yellow-700"
                        )}>
                          {task.risk === 'high' ? '高风险' : task.risk === 'medium' ? '中风险' : '低风险'}
                        </Badge>
                      </td>
                      <td className="p-4">
                        <div className="flex items-center gap-2">
                          <div className={cn(
                            "px-2 py-1 rounded-lg text-xs font-bold",
                            isLowScore ? "bg-amber-100 text-amber-700" : "bg-emerald-100 text-emerald-700"
                          )}>
                            质量分: {avgScore}
                          </div>
                          {isLowScore && (
                            <AlertTriangle className="w-4 h-4 text-amber-500" />
                          )}
                        </div>
                      </td>
                      <td className="p-4">
                        <div className="flex items-center gap-2">
                          <Button
                            size="sm"
                            variant="ghost"
                            className="h-8 w-8 p-0"
                            title="查看详情"
                            onClick={() => handleViewDetail(task.review_id || String(task.id))}
                          >
                            <Eye className="w-4 h-4" />
                          </Button>
                          <Button
                            size="sm"
                            className="h-8 bg-emerald-500 hover:bg-emerald-600 text-white gap-1"
                            title="通过并发送"
                            onClick={() => handleApprove(String(task.id))}
                          >
                            <Send className="w-3.5 h-3.5" />
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            className="h-8 border-rose-200 text-rose-600 hover:bg-rose-50 gap-1"
                            title="驳回"
                            onClick={() => handleReject(String(task.id))}
                          >
                            <XCircle className="w-3.5 h-3.5" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-between p-4 border-t border-slate-100">
            <p className="text-sm text-slate-500">
              显示 {((currentPage - 1) * pageSize) + 1}-{Math.min(currentPage * pageSize, total)} 条，共 {total} 条
            </p>
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                disabled={currentPage === 1}
              >
                <ChevronLeft className="w-4 h-4" />
              </Button>
              <span className="text-sm font-medium text-slate-700">
                {currentPage} / {Math.ceil(total / pageSize)}
              </span>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setCurrentPage(Math.min(Math.ceil(total / pageSize), currentPage + 1))}
                disabled={currentPage === Math.ceil(total / pageSize)}
              >
                <ChevronRight className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </AdminLayout>
  );
};

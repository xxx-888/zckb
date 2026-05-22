import React, { useState, useEffect } from 'react';
import { MessageSquare, Search, Download, Trash2, Eye, Star, RefreshCw, AlertCircle, StoreIcon, Filter } from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { AdminLayout } from '../../components/AdminLayout';
import { useToast } from '../../hooks/use-toast';
import { fetchReviews, deleteReview } from '../../api/reviews';
import { storesApi } from '../../api/stores';
import type { Review } from '../../api/reviews';
import type { Store as StoreType } from '../../api/stores';

export const ReviewManagement: React.FC = () => {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [stores, setStores] = useState<StoreType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [sentimentFilter, setSentimentFilter] = useState('all');
  const [storeFilter, setStoreFilter] = useState('all');
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [viewingReview, setViewingReview] = useState<Review | null>(null);

  const { success, error: toastError } = useToast();

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [rRes, sRes] = await Promise.allSettled([
        fetchReviews({ page_size: 200 }).catch(err => { console.warn('[ReviewMgmt] 获取评论失败:', err); return { items: [] }; }),
        storesApi.getStores({ page_size: 100 }).catch(err => { console.warn('[ReviewMgmt] 获取门店失败:', err); return { items: [] }; }),
      ]);
      if (rRes.status === 'fulfilled') setReviews((rRes.value as any)?.items || []);
      if (sRes.status === 'fulfilled') setStores((sRes.value as any)?.items || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally { setLoading(false); }
  };

  useEffect(() => { loadData(); }, []);

  const filtered = reviews.filter(r => {
    const match = (r.content || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
                  (r.user_name || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
                  (r.store_name || r.store || '').toLowerCase().includes(searchQuery.toLowerCase());
    const sentiment = sentimentFilter === 'all' || r.sentiment === sentimentFilter;
    const store = storeFilter === 'all' || r.store_id === storeFilter;
    return match && sentiment && store;
  });

  const handleDelete = async (id: string) => {
    try { await deleteReview(id); success('已删除', '评论已移除'); loadData(); }
    catch (err: any) { toastError('删除失败', err.message); }
  };

  const handleBatchDelete = async () => {
    if (!selectedIds.length) return;
    try { await Promise.all(selectedIds.map(id => deleteReview(id))); success('批量删除', `已删除 ${selectedIds.length} 条`); setSelectedIds([]); loadData(); }
    catch (err: any) { toastError('删除失败', err.message); }
  };

  const toggleSelect = (id: string) => setSelectedIds(prev => prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]);
  const toggleAll = () => selectedIds.length === filtered.length ? setSelectedIds([]) : setSelectedIds(filtered.map(r => r.id));

  const sentimentBadge = (s: string) => {
    const m: Record<string, { c: string; t: string }> = {
      positive: { c: 'bg-emerald-100 text-emerald-700', t: '好评' },
      negative: { c: 'bg-rose-100 text-rose-700', t: '差评' },
      neutral: { c: 'bg-slate-100 text-slate-600', t: '中评' },
    };
    const x = m[s] || { c: 'bg-slate-100 text-slate-600', t: s };
    return <Badge className={x.c}>{x.t}</Badge>;
  };

  const starRating = (r: number) => '★'.repeat(r) + '☆'.repeat(5 - r);

  if (loading) return <AdminLayout><div className="flex items-center justify-center h-64"><RefreshCw className="w-6 h-6 text-slate-400 animate-spin" /></div></AdminLayout>;
  if (error) return <AdminLayout><div className="flex flex-col items-center justify-center h-64 gap-4"><AlertCircle className="w-10 h-10 text-rose-400" /><p className="text-slate-500">{error}</p><Button variant="outline" onClick={loadData}>重试</Button></div></AdminLayout>;

  return (
    <AdminLayout>
      <div className="space-y-6 pb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">评论管理</h1>
            <p className="text-sm text-slate-500 mt-1">共 {filtered.length} 条评论</p>
          </div>
          <div className="flex items-center gap-2">
            {selectedIds.length > 0 && (
              <Button variant="outline" className="text-rose-500 border-rose-200" onClick={handleBatchDelete}>
                <Trash2 className="w-4 h-4 mr-1" />批量删除({selectedIds.length})
              </Button>
            )}
            <Button variant="outline" onClick={() => success('导出', '正在生成报表...')}>
              <Download className="w-4 h-4 mr-1" />导出
            </Button>
          </div>
        </div>

        {/* Filters */}
        <div className="flex items-center gap-3 flex-wrap">
          <div className="relative flex-1 min-w-[200px]">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input className="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-sm outline-none" placeholder="搜索评论内容、用户名、门店..." value={searchQuery} onChange={e => setSearchQuery(e.target.value)} />
          </div>
          <select className="bg-white border border-slate-200 rounded-xl px-3 py-2.5 text-sm outline-none" value={sentimentFilter} onChange={e => setSentimentFilter(e.target.value)}>
            <option value="all">全部情感</option>
            <option value="positive">好评</option>
            <option value="negative">差评</option>
            <option value="neutral">中评</option>
          </select>
          <select className="bg-white border border-slate-200 rounded-xl px-3 py-2.5 text-sm outline-none min-w-[140px]" value={storeFilter} onChange={e => setStoreFilter(e.target.value)}>
            <option value="all">全部门店</option>
            {stores.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
          </select>
          <Button variant="ghost" size="sm" onClick={loadData}><RefreshCw className="w-4 h-4 mr-1" />刷新</Button>
        </div>

        {/* Table */}
        {filtered.length === 0 ? (
          <div className="text-center py-16 text-slate-400"><MessageSquare className="w-12 h-12 mx-auto mb-3 opacity-30" /><p>暂无评论数据</p></div>
        ) : (
          <Card className="border-slate-100 shadow-sm overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 text-slate-500 text-xs">
                <tr>
                  <th className="p-3 w-10"><input type="checkbox" checked={selectedIds.length === filtered.length && filtered.length > 0} onChange={toggleAll} /></th>
                  <th className="text-left p-3">门店</th>
                  <th className="text-left p-3">用户</th>
                  <th className="text-left p-3">评论内容</th>
                  <th className="text-center p-3">评分</th>
                  <th className="text-center p-3">情感</th>
                  <th className="text-center p-3">回复</th>
                  <th className="text-right p-3">操作</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map(r => (
                  <tr key={r.id} className="border-t border-slate-50 hover:bg-slate-50/50">
                    <td className="p-3"><input type="checkbox" checked={selectedIds.includes(r.id)} onChange={() => toggleSelect(r.id)} /></td>
                    <td className="p-3">
                      <div className="flex items-center gap-1.5">
                        <StoreIcon className="w-3.5 h-3.5 text-blue-500" />
                        <span className="font-medium text-slate-900 text-xs">{r.store_name || r.store || '未知门店'}</span>
                        {r.platform && <span className="text-[10px] text-slate-400 bg-slate-100 px-1.5 py-0.5 rounded">{r.platform}</span>}
                      </div>
                    </td>
                    <td className="p-3 text-xs text-slate-600">{r.user_name || r.user || '匿名'}</td>
                    <td className="p-3 max-w-[300px]"><p className="text-xs text-slate-700 line-clamp-2">{r.content}</p></td>
                    <td className="p-3 text-center text-amber-500 text-xs">{starRating(r.rating)}</td>
                    <td className="p-3 text-center">{sentimentBadge(r.sentiment)}</td>
                    <td className="p-3 text-center">{r.replied ? <Badge className="bg-blue-100 text-blue-700 text-xs">已回复</Badge> : <span className="text-xs text-slate-400">未回复</span>}</td>
                    <td className="p-3 text-right">
                      <div className="flex items-center justify-end gap-1">
                        <Button size="sm" variant="ghost" onClick={() => setViewingReview(r)}><Eye className="w-3.5 h-3.5" /></Button>
                        <Button size="sm" variant="ghost" className="text-rose-500" onClick={() => handleDelete(r.id)}><Trash2 className="w-3.5 h-3.5" /></Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Card>
        )}

        {/* Detail Modal */}
        {viewingReview && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={() => setViewingReview(null)}>
            <Card className="w-[500px] max-h-[80vh] overflow-y-auto p-6 space-y-4" onClick={e => e.stopPropagation()}>
              <h3 className="font-bold text-slate-900">评论详情</h3>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div><span className="text-slate-400">门店:</span> <span className="font-medium">{viewingReview.store_name || viewingReview.store || '-'}</span></div>
                <div><span className="text-slate-400">平台:</span> <span className="font-medium">{viewingReview.platform || '-'}</span></div>
                <div><span className="text-slate-400">用户:</span> <span className="font-medium">{viewingReview.user_name || viewingReview.user || '-'}</span></div>
                <div><span className="text-slate-400">评分:</span> <span className="text-amber-500">{starRating(viewingReview.rating)}</span></div>
                <div><span className="text-slate-400">情感:</span> {sentimentBadge(viewingReview.sentiment)}</div>
                <div><span className="text-slate-400">状态:</span> {viewingReview.replied ? <Badge className="bg-blue-100 text-blue-700 text-xs">已回复</Badge> : <span className="text-xs text-slate-400">未回复</span>}</div>
              </div>
              <div className="bg-slate-50 rounded-xl p-4">
                <p className="text-xs text-slate-400 mb-1">评论内容</p>
                <p className="text-sm text-slate-700">{viewingReview.content}</p>
              </div>
              {viewingReview.reply && (
                <div className="bg-indigo-50 rounded-xl p-4">
                  <p className="text-xs text-indigo-500 mb-1">回复内容</p>
                  <p className="text-sm text-slate-700">{viewingReview.reply}</p>
                </div>
              )}
              {viewingReview.images && viewingReview.images.length > 0 && (
                <div className="flex gap-2 flex-wrap">
                  {viewingReview.images.map((img, i) => <img key={i} src={img} alt="" className="w-20 h-20 object-cover rounded-lg" />)}
                </div>
              )}
              <div className="flex justify-end"><Button variant="outline" onClick={() => setViewingReview(null)}>关闭</Button></div>
            </Card>
          </div>
        )}
      </div>
    </AdminLayout>
  );
};

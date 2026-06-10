import React, { useState, useEffect, useRef } from 'react';
import { MessageSquare, Search, Download, Trash2, Eye, Star, RefreshCw, AlertCircle, StoreIcon, Filter, Upload } from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { AdminLayout } from '../../components/AdminLayout';
import { useToast } from '../../hooks/use-toast';
import { fetchReviews, deleteReview, reviewsApi } from '../../api/reviews';
import { storesApi } from '../../api/stores';
import type { Review } from '../../api/reviews';
import type { Store as StoreType } from '../../api/stores';
import { api } from '../../lib/api';
import { normalizeImageUrls, useSearchDebounce } from '../../lib/utils';

export const ReviewManagement: React.FC = () => {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [stores, setStores] = useState<StoreType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const { inputValue: searchInput, debouncedValue: debouncedSearch, handleChange: handleSearchInput } = useSearchDebounce();
  const [sentimentFilter, setSentimentFilter] = useState('all');
  const [storeFilter, setStoreFilter] = useState('all');
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [viewingReview, setViewingReview] = useState<Review | null>(null);
  const [importDialog, setImportDialog] = useState(false);
  const [importStoreId, setImportStoreId] = useState('');
  const [importFile, setImportFile] = useState<File | null>(null);
  const [importing, setImporting] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // 分页状态
  const [currentPage, setCurrentPage] = useState(1);
  const [totalItems, setTotalItems] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [pageSize, setPageSize] = useState(20);

  const { success, error: toastError } = useToast();

  // 防抖后的搜索词同步到 searchQuery
  useEffect(() => {
    setSearchQuery(debouncedSearch);
  }, [debouncedSearch]);

  // 加载数据（带分页和过滤）
  const loadData = async (page: number = currentPage) => {
    setLoading(true);
    setError(null);
    try {
      // 构建过滤参数
      const filters: any = {
        page: page,
        page_size: pageSize,
      };
      if (sentimentFilter !== 'all') filters.sentiment = sentimentFilter;
      if (storeFilter !== 'all') filters.store_id = storeFilter;
      if (searchQuery) filters.keyword = searchQuery;

      const [rRes, sRes] = await Promise.allSettled([
        fetchReviews(filters).catch(err => { console.warn('[ReviewMgmt] 获取评论失败:', err); return { items: [], total: 0, page: 1, page_size: 20 }; }),
        storesApi.getStores({ page_size: 100 }).catch(err => { console.warn('[ReviewMgmt] 获取门店失败:', err); return { items: [] }; }),
      ]);
      
      if (rRes.status === 'fulfilled') {
        const reviewData = rRes.value as any;
        setReviews(reviewData?.items || []);
        setTotalItems(reviewData?.total || 0);
        setTotalPages(Math.ceil((reviewData?.total || 0) / pageSize));
        setCurrentPage(reviewData?.page || 1);
      }
      if (sRes.status === 'fulfilled') setStores((sRes.value as any)?.items || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally { setLoading(false); }
  };

  // 过滤条件变化时，重置页码并重新加载
  useEffect(() => {
    setCurrentPage(1);
    loadData(1);
  }, [sentimentFilter, storeFilter, searchQuery]);

  // 页码变化时，重新加载
  useEffect(() => {
    if (currentPage > 1) {
      loadData(currentPage);
    }
  }, [currentPage]);

  const handlePageChange = (newPage: number) => {
    if (newPage >= 1 && newPage <= totalPages) {
      setCurrentPage(newPage);
    }
  };

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
  const toggleAll = () => selectedIds.length === reviews.length ? setSelectedIds([]) : setSelectedIds(reviews.map(r => r.id));

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

  // ===== 下载模板处理函数 =====
  const handleDownloadTemplate = async (example: boolean = false) => {
    try {
      const response = await api.get(`/v1/reviews/import-template?example=${example}`, {
        responseType: 'blob',
      });
      const blob = new Blob([response.data || response]);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = example ? '评论导入模板（带示例）.xlsx' : '评论导入模板（空白）.xlsx';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      success('模板下载成功', example ? '带示例模板已下载' : '空白模板已下载');
    } catch (err: any) {
      toastError('下载失败', err.message);
    }
  };

  // ===== 导入处理函数 =====
  const handleImport = async () => {
    if (!importFile || !importStoreId) {
      toastError('请选择文件和店铺');
      return;
    }
    setImporting(true);
    try {
      const result = await reviewsApi.importReviews(importFile, importStoreId);
      // 兼容 code=0（框架标准）和 code=200（HTTP 状态式）
      if (result.code === 0 || result.code === 200) {
        const info = result.data || result;
        success('导入成功', `成功 ${info.success_count ?? info.total ?? '?'} 条，跳过 ${info.skip_count ?? 0} 条`);
        setImportDialog(false);
        setImportFile(null);
        setImportStoreId('');
        loadData();
      } else {
        throw new Error(result.message);
      }
    } catch (err: any) {
      toastError('导入失败', err.message);
    } finally {
      setImporting(false);
    }
  };

  // ===== 导出处理函数 =====
  const handleExport = async () => {
    try {
      const filters: any = {};
      if (sentimentFilter !== 'all') filters.sentiment = sentimentFilter;
      if (storeFilter !== 'all') filters.store_id = storeFilter;
      if (searchQuery) filters.keyword = searchQuery;

      const blob = await reviewsApi.exportReviews(filters);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `评论导出_${new Date().toISOString().slice(0, 10)}.xlsx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      success('导出成功', '文件已下载');
    } catch (err: any) {
      toastError('导出失败', err.message);
    }
  };

  if (loading) return <AdminLayout><div className="flex items-center justify-center h-64"><RefreshCw className="w-6 h-6 text-slate-400 animate-spin" /></div></AdminLayout>;
  if (error) return <AdminLayout><div className="flex flex-col items-center justify-center h-64 gap-4"><AlertCircle className="w-10 h-10 text-rose-400" /><p className="text-slate-500">{error}</p><Button variant="outline" onClick={() => loadData()}>重试</Button></div></AdminLayout>;

  return (
    <AdminLayout>
      <div className="space-y-6 pb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">评论管理</h1>
            <p className="text-sm text-slate-500 mt-1">共 {totalItems} 条评论，第 {currentPage}/{totalPages} 页</p>
          </div>
          <div className="flex items-center gap-2">
            {selectedIds.length > 0 && (
              <Button variant="outline" className="text-rose-500 border-rose-200" onClick={handleBatchDelete}>
                <Trash2 className="w-4 h-4 mr-1" />批量删除({selectedIds.length})
              </Button>
            )}
            <div className="flex items-center gap-1">
              <Button variant="outline" size="sm" onClick={() => handleDownloadTemplate(false)}>
                空白模板
              </Button>
              <Button variant="outline" size="sm" onClick={() => handleDownloadTemplate(true)}>
                示例模板
              </Button>
            </div>
            <Button variant="outline" onClick={() => fileInputRef.current?.click()}>
              <Upload className="w-4 h-4 mr-1" />导入
            </Button>
            <Button variant="outline" onClick={handleExport}>
              <Download className="w-4 h-4 mr-1" />导出
            </Button>
            <input
              type="file"
              ref={fileInputRef}
              className="hidden"
              accept=".xlsx,.csv"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) {
                  setImportFile(file);
                  setImportDialog(true);
                }
              }}
            />
          </div>
        </div>

        {/* Filters */}
        <div className="flex items-center gap-3 flex-wrap">
          <div className="relative flex-1 min-w-[200px]">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input className="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-sm outline-none" placeholder="搜索评论内容、用户名、门店..." value={searchInput} onChange={e => handleSearchInput(e.target.value)} />
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
          <Button variant="ghost" size="sm" onClick={() => loadData()}><RefreshCw className="w-4 h-4 mr-1" />刷新</Button>
        </div>

        {/* Table */}
        {reviews.length === 0 ? (
          <div className="text-center py-16 text-slate-400"><MessageSquare className="w-12 h-12 mx-auto mb-3 opacity-30" /><p>暂无评论数据</p></div>
        ) : (
          <Card className="border-slate-100 shadow-sm overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 text-slate-500 text-xs">
                <tr>
                  <th className="p-3 w-10"><input type="checkbox" checked={selectedIds.length === reviews.length && reviews.length > 0} onChange={toggleAll} /></th>
                  <th className="text-left p-3">门店</th>
                  <th className="text-left p-3">用户</th>
                  <th className="text-left p-3">评论内容</th>
                  <th className="text-center p-3">图片</th>
                  <th className="text-center p-3">评分</th>
                  <th className="text-center p-3">情感</th>
                  <th className="text-center p-3">入库时间</th>
                  <th className="text-center p-3">评论时间</th>
                  <th className="text-center p-3">回复</th>
                  <th className="text-right p-3">操作</th>
                </tr>
              </thead>
              <tbody>
                {reviews.map(r => (
                  <tr key={r.id} className="border-t border-slate-50 hover:bg-slate-50/50">
                    <td className="p-3"><input type="checkbox" checked={selectedIds.includes(r.id)} onChange={() => toggleSelect(r.id)} /></td>
                    <td className="p-3">
                      <div className="flex items-center gap-1.5">
                        <StoreIcon className="w-3.5 h-3.5 text-blue-500" />
                        <span className="font-medium text-slate-900 text-xs">{r.store_name || '未知门店'}</span>
                        {r.platform && <span className="text-[10px] text-slate-400 bg-slate-100 px-1.5 py-0.5 rounded">{r.platform}</span>}
                      </div>
                    </td>
                    <td className="p-3">
                      <div className="flex items-center gap-2">
                        <div className="w-7 h-7 rounded-lg overflow-hidden bg-slate-100 flex-shrink-0 border border-slate-50">
                          {r.user_avatar ? (
                            <img src={r.user_avatar} alt={r.user_name || '用户'} className="w-full h-full object-cover" />
                          ) : (
                            <div className="w-full h-full flex items-center justify-center text-[10px] font-bold text-slate-400">
                              {(r.user_name || r.user || '?')[0]}
                            </div>
                          )}
                        </div>
                        <span className="text-xs text-slate-600 truncate max-w-[80px]">{r.user_name || r.user || '匿名'}</span>
                      </div>
                    </td>
                    <td className="p-3 max-w-[300px]"><p className="text-xs text-slate-700 line-clamp-2">{r.content}</p></td>
                    <td className="p-3 text-center">{normalizeImageUrls(r.images).length > 0 && <Badge className="bg-emerald-50 text-emerald-600 text-[10px]">{normalizeImageUrls(r.images).length}图</Badge>}</td>
                    <td className="p-3 text-center text-amber-500 text-xs">{starRating(r.rating)}</td>
                    <td className="p-3 text-center">{sentimentBadge(r.sentiment)}</td>
                    <td className="p-3 text-center text-xs text-slate-500">{r.created_at ? new Date(r.created_at).toLocaleDateString('zh-CN') : '-'}</td>
                    <td className="p-3 text-center text-xs text-slate-500">{r.platform_created_at ? new Date(r.platform_created_at).toLocaleDateString('zh-CN') : '-'}</td>
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

        {/* 分页 UI */}
        {totalPages > 1 && (
          <div className="flex items-center justify-between mt-4">
            <div className="text-sm text-slate-500">
              第 {currentPage} 页，共 {totalPages} 页（{totalItems} 条记录）
            </div>
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage <= 1}
              >
                上一页
              </Button>
              <div className="flex items-center gap-1">
                {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                  let pageNum;
                  if (totalPages <= 5) {
                    pageNum = i + 1;
                  } else if (currentPage <= 3) {
                    pageNum = i + 1;
                  } else if (currentPage >= totalPages - 2) {
                    pageNum = totalPages - 4 + i;
                  } else {
                    pageNum = currentPage - 2 + i;
                  }
                  return (
                    <button
                      key={pageNum}
                      onClick={() => handlePageChange(pageNum)}
                      className={`w-8 h-8 rounded-lg text-sm ${
                        currentPage === pageNum
                          ? 'bg-indigo-500 text-white'
                          : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50'
                      }`}
                    >
                      {pageNum}
                    </button>
                  );
                })}
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={currentPage >= totalPages}
              >
                下一页
              </Button>
            </div>
          </div>
        )}

        {/* Detail Modal */}
        {viewingReview && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={() => setViewingReview(null)}>
            <Card className="w-[500px] max-h-[80vh] overflow-y-auto p-6 space-y-4" onClick={e => e.stopPropagation()}>
              <h3 className="font-bold text-slate-900">评论详情</h3>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div><span className="text-slate-400">门店:</span> <span className="font-medium">{viewingReview.store_name || '-'}</span></div>
                <div><span className="text-slate-400">平台:</span> <span className="font-medium">{viewingReview.platform || '-'}</span></div>
                <div><span className="text-slate-400">用户:</span> <span className="font-medium">{viewingReview.user_name || '-'}</span></div>
                <div><span className="text-slate-400">评分:</span> <span className="text-amber-500">{starRating(viewingReview.rating)}</span></div>
                <div><span className="text-slate-400">情感:</span> {sentimentBadge(viewingReview.sentiment)}</div>
                <div><span className="text-slate-400">状态:</span> {viewingReview.replied ? <Badge className="bg-blue-100 text-blue-700 text-xs">已回复</Badge> : <span className="text-xs text-slate-400">未回复</span>}</div>
                <div><span className="text-slate-400">入库时间:</span> <span className="font-medium">{viewingReview.created_at ? new Date(viewingReview.created_at).toLocaleString('zh-CN') : '-'}</span></div>
                <div><span className="text-slate-400">评论时间:</span> <span className="font-medium">{viewingReview.platform_created_at ? new Date(viewingReview.platform_created_at).toLocaleString('zh-CN') : '-'}</span></div>
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
              {normalizeImageUrls(viewingReview.images).length > 0 && (
                <div className="flex gap-2 flex-wrap">
                  {normalizeImageUrls(viewingReview.images).map((url, i) => (
                    <img key={i} src={url} alt="" className="w-20 h-20 object-cover rounded-lg" loading="lazy" />
                  ))}
                </div>
              )}
              <div className="flex justify-end"><Button variant="outline" onClick={() => setViewingReview(null)}>关闭</Button></div>
            </Card>
          </div>
        )}
      </div>

      {/* 导入对话框 */}
      {importDialog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={() => setImportDialog(false)}>
          <div className="bg-white rounded-2xl p-6 w-[480px] shadow-2xl" onClick={e => e.stopPropagation()}>
            <h3 className="text-lg font-bold text-slate-900 mb-4">批量导入评论</h3>
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">选择店铺</label>
                <select
                  value={importStoreId}
                  onChange={e => setImportStoreId(e.target.value)}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm"
                >
                  <option value="">-- 请选择店铺 --</option>
                  {stores.map(s => (
                    <option key={s.id} value={s.id}>{s.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">选择文件</label>
                <input
                  type="file"
                  accept=".xlsx,.csv"
                  onChange={e => {
                    const file = e.target.files?.[0];
                    if (file) setImportFile(file);
                  }}
                  className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm file:mr-4 file:py-1 file:px-3 file:rounded-lg file:border-0 file:bg-indigo-50 file:text-indigo-700 file:text-sm hover:file:bg-indigo-100"
                />
                {importFile && (
                  <p className="mt-1 text-xs text-slate-500">已选：{importFile.name}</p>
                )}
              </div>
              <div className="bg-slate-50 rounded-lg p-3 text-xs text-slate-500">
                <p className="font-medium mb-1">文件格式要求：</p>
                <ul className="list-disc list-inside space-y-0.5">
                  <li>支持 .xlsx 或 .csv 文件</li>
                  <li>必填列：<code className="bg-slate-200 px-1 rounded">评论内容</code> 或 <code className="bg-slate-200 px-1 rounded">content</code></li>
                  <li>可选列：评分、平台、图片、回复</li>
                  <li className="mt-2">
                    <button
                      onClick={async (e) => {
                        e.stopPropagation();
                        try {
                          const response = await api.get('/v1/reviews/import-template?example=false', {
                            responseType: 'blob',
                          });
                          const blob = new Blob([response.data || response]);
                          const url = window.URL.createObjectURL(blob);
                          const a = document.createElement('a');
                          a.href = url;
                          a.download = '评论导入模板（空白）.xlsx';
                          document.body.appendChild(a);
                          a.click();
                          window.URL.revokeObjectURL(url);
                          document.body.removeChild(a);
                          success('模板下载成功', '空白模板已下载');
                        } catch (err: any) {
                          toastError('下载失败', err.message);
                        }
                      }}
                      className="text-indigo-600 hover:text-indigo-800 underline bg-transparent border-none cursor-pointer p-0"
                    >
                      下载空白模板
                    </button>
                    <span className="mx-2 text-slate-300">|</span>
                    <button
                      onClick={async (e) => {
                        e.stopPropagation();
                        try {
                          const response = await api.get('/v1/reviews/import-template?example=true', {
                            responseType: 'blob',
                          });
                          const blob = new Blob([response.data || response]);
                          const url = window.URL.createObjectURL(blob);
                          const a = document.createElement('a');
                          a.href = url;
                          a.download = '评论导入模板（带示例）.xlsx';
                          document.body.appendChild(a);
                          a.click();
                          window.URL.revokeObjectURL(url);
                          document.body.removeChild(a);
                          success('模板下载成功', '示例模板已下载');
                        } catch (err: any) {
                          toastError('下载失败', err.message);
                        }
                      }}
                      className="text-indigo-600 hover:text-indigo-800 underline bg-transparent border-none cursor-pointer p-0"
                    >
                      下载示例模板
                    </button>
                  </li>
                </ul>
              </div>
            </div>
            <div className="flex justify-end gap-2 mt-6">
              <Button variant="ghost" onClick={() => { setImportDialog(false); setImportFile(null); }}>取消</Button>
              <Button
                onClick={handleImport}
                disabled={!importFile || !importStoreId || importing}
                className="bg-indigo-500 hover:bg-indigo-600 text-white"
              >
                {importing ? '导入中...' : '确认导入'}
              </Button>
            </div>
          </div>
        </div>
      )}
    </AdminLayout>
  );
};

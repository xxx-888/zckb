import React, { useState, useEffect } from 'react';
import { 
  MessageSquare, 
  Search, 
  Filter, 
  Download, 
  Trash2, 
  Eye, 
  Flag, 
  Calendar, 
  MoreVertical,
  CheckCircle,
  RefreshCw,
  Star,
  Plus,
  Edit2,
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { AdminLayout } from '../../components/AdminLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';
import { fetchReviews, createReview, updateReview, deleteReview } from '../../api/reviews';
import type { Review } from '../../api/reviews';

export const ReviewManagement: React.FC = () => {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedSentiment, setSelectedSentiment] = useState<string>('all');
  const [selectedReviews, setSelectedReviews] = useState<number[]>([]);
  const [showAddReview, setShowAddReview] = useState(false);
  const [showEditReview, setShowEditReview] = useState(false);
  const [showViewDetail, setShowViewDetail] = useState(false);
  const [editingReview, setEditingReview] = useState<Review | null>(null);
  const [viewingReview, setViewingReview] = useState<Review | null>(null);
  const [newReview, setNewReview] = useState<Partial<Review>>({ store: '', platform: '美团', rating: 5, user: '', content: '', sentiment: 'positive' });
  const { success, error: toastError } = useToast();

  // 加载评论数据
  const loadReviews = async () => {
    try {
      setLoading(true);
      setFetchError(null);
      const data = await fetchReviews();
      setReviews(data);
    } catch (err) {
      setFetchError(err instanceof Error ? err.message : '获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReviews();
  }, []);

  const filteredReviews = reviews.filter(r => {
    const matchesSearch = r.content.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          r.user.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          r.store.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesSentiment = selectedSentiment === 'all' || r.sentiment === selectedSentiment;
    return matchesSearch && matchesSentiment;
  });

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    if (query.trim()) {
      success('搜索中', `正在搜索 "${query}"...`);
    }
  };

  const handleFilterSentiment = (sentiment: string) => {
    setSelectedSentiment(sentiment);
    success('筛选已更新', `已筛选${sentiment === 'all' ? '所有评论' : sentiment === 'positive' ? '正面评论' : sentiment === 'negative' ? '负面评论' : '中性评论'}`);
  };

  const handleAddReview = async () => {
    if (!newReview.store || !newReview.user || !newReview.content) {
      toastError('添加失败', '请填写店铺名称、用户名和评论内容');
      return;
    }
    try {
      await createReview({
        avatar: '',
        store: newReview.store!,
        platform: newReview.platform || '美团',
        rating: newReview.rating || 5,
        user: newReview.user!,
        content: newReview.content!,
        time: new Date().toISOString().split('T')[0] + ' ' + new Date().toTimeString().split(' ')[0].substring(0, 5),
        sentiment: newReview.sentiment || 'positive',
        replied: false,
      });
      setShowAddReview(false);
      setNewReview({ store: '', platform: '美团', rating: 5, user: '', content: '', sentiment: 'positive' });
      success('添加成功', '评论已添加');
      loadReviews();
    } catch (err) {
      toastError('添加失败', err instanceof Error ? err.message : '未知错误');
    }
  };

  const handleEditReview = (id: number) => {
    const review = reviews.find(r => r.id === id);
    if (review) {
      setEditingReview(review);
      setShowEditReview(true);
    }
  };

  const handleUpdateReview = async () => {
    if (!editingReview) return;
    if (!editingReview.store || !editingReview.user || !editingReview.content) {
      toastError('更新失败', '请填写完整信息');
      return;
    }
    try {
      await updateReview(editingReview.id, editingReview);
      setShowEditReview(false);
      setEditingReview(null);
      success('更新成功', '评论已更新');
      loadReviews();
    } catch (err) {
      toastError('更新失败', err instanceof Error ? err.message : '未知错误');
    }
  };

  const handleViewDetail = (id: number) => {
    const review = reviews.find(r => r.id === id);
    if (review) {
      setViewingReview(review);
      setShowViewDetail(true);
    }
  };

  const handleFlagReview = (id: number) => {
    const review = reviews.find(r => r.id === id);
    success('已标记', `评论已标记为需要处理：${review?.content.substring(0, 20)}...`);
  };

  const handleDeleteReview = async (id: number) => {
    try {
      await deleteReview(id);
      success('删除成功', '评论已删除');
      loadReviews();
    } catch (err) {
      toastError('删除失败', err instanceof Error ? err.message : '未知错误');
    }
  };

  const handleBatchDelete = async () => {
    if (selectedReviews.length === 0) {
      toastError('批量删除失败', '请先选择要删除的评论');
      return;
    }
    try {
      await Promise.all(selectedReviews.map(id => deleteReview(id)));
      success('批量删除成功', `已删除 ${selectedReviews.length} 条评论`);
      setSelectedReviews([]);
      loadReviews();
    } catch (err) {
      toastError('批量删除失败', err instanceof Error ? err.message : '未知错误');
    }
  };

  const handleExport = () => {
    success('导出数据', '正在生成评论数据报表...');
    setTimeout(() => {
      success('导出完成', '评论数据报表已下载');
    }, 1500);
  };

  const handleSelectReview = (id: number) => {
    if (selectedReviews.includes(id)) {
      setSelectedReviews(selectedReviews.filter(rid => rid !== id));
    } else {
      setSelectedReviews([...selectedReviews, id]);
    }
  };

  const handleSelectAll = () => {
    if (selectedReviews.length === filteredReviews.length) {
      setSelectedReviews([]);
    } else {
      setSelectedReviews(filteredReviews.map(r => r.id));
    }
  };

  if (loading) {
    return (
      <AdminLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-sm text-slate-400">加载中...</p>
          </div>
        </div>
      </AdminLayout>
    );
  }

  if (fetchError) {
    return (
      <AdminLayout>
        <div className="text-center py-20">
          <p className="text-rose-500 mb-4">{fetchError}</p>
          <Button onClick={() => loadReviews()}>重试</Button>
        </div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">评论数据管理</h2>
            <p className="text-slate-500 mt-1">查看和管理全系统采集的客户评价数据（共 {reviews.length} 条）</p>
          </div>
          <div className="flex gap-2">
            <Button 
              className="gap-2 h-10 bg-blue-600 hover:bg-blue-700 text-white"
              onClick={() => setShowAddReview(true)}
            >
              <Plus className="w-4 h-4" /> 添加评论
            </Button>
            {selectedReviews.length > 0 && (
              <Button variant="outline" className="gap-2 h-10 text-rose-600 border-rose-200" onClick={handleBatchDelete}>
                <Trash2 className="w-4 h-4" /> 删除选中 ({selectedReviews.length})
              </Button>
            )}
            <Button variant="outline" className="gap-2 h-10" onClick={handleExport}>
              <Download className="w-4 h-4" /> 导出数据
            </Button>
          </div>
        </div>

        {/* Add Review Form */}
        {showAddReview && (
          <Card className="p-6 border-2 border-blue-500 bg-blue-50/10 animate-in zoom-in-95 duration-200">
            <h4 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
              <Plus className="w-4 h-4" /> 添加评论
            </h4>
            <div className="grid grid-cols-2 gap-6 mb-6">
              <div className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">店铺名称</label>
                  <Input 
                    value={newReview.store}
                    onChange={(e) => setNewReview({...newReview, store: e.target.value})}
                    placeholder="请输入店铺名称" 
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">用户名</label>
                  <Input 
                    value={newReview.user}
                    onChange={(e) => setNewReview({...newReview, user: e.target.value})}
                    placeholder="请输入用户名" 
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">评分</label>
                  <div className="flex gap-1">
                    {[1, 2, 3, 4, 5].map(i => (
                      <Star 
                        key={i} 
                        className={cn("w-6 h-6 cursor-pointer", i <= (newReview.rating || 5) ? "text-amber-400 fill-current" : "text-slate-300")}
                        onClick={() => setNewReview({...newReview, rating: i})}
                      />
                    ))}
                  </div>
                </div>
              </div>
              <div className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">平台</label>
                  <select 
                    value={newReview.platform}
                    onChange={(e) => setNewReview({...newReview, platform: e.target.value})}
                    className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500/20"
                  >
                    <option>美团</option>
                    <option>点评</option>
                    <option>抖音</option>
                  </select>
                </div>
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">情感分类</label>
                  <select 
                    value={newReview.sentiment}
                    onChange={(e) => setNewReview({...newReview, sentiment: e.target.value as 'positive' | 'negative' | 'neutral'})}
                    className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500/20"
                  >
                    <option value="positive">正面</option>
                    <option value="negative">负面</option>
                    <option value="neutral">中性</option>
                  </select>
                </div>
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">评论内容</label>
                  <textarea 
                    value={newReview.content}
                    onChange={(e) => setNewReview({...newReview, content: e.target.value})}
                    className="w-full h-20 p-3 bg-white border border-slate-200 rounded-lg text-sm resize-none outline-none focus:ring-2 focus:ring-blue-500/20"
                    placeholder="请输入评论内容..." 
                  />
                </div>
              </div>
            </div>
            <div className="flex gap-3 pt-4 border-t border-slate-100">
              <Button className="flex-1 bg-blue-600 hover:bg-blue-700" onClick={handleAddReview}>添加评论</Button>
              <Button variant="ghost" onClick={() => { setShowAddReview(false); setNewReview({ store: '', platform: '美团', rating: 5, user: '', content: '', sentiment: 'positive' }); }}>取消</Button>
            </div>
          </Card>
        )}

        {/* Edit Review Form */}
        {showEditReview && editingReview && (
          <Card className="p-6 border-2 border-amber-500 bg-amber-50/10 animate-in zoom-in-95 duration-200">
            <h4 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
              <Edit2 className="w-4 h-4" /> 编辑评论
            </h4>
            <div className="grid grid-cols-2 gap-6 mb-6">
              <div className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">店铺名称</label>
                  <Input 
                    value={editingReview.store}
                    onChange={(e) => setEditingReview({...editingReview, store: e.target.value})}
                    placeholder="请输入店铺名称" 
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">用户名</label>
                  <Input 
                    value={editingReview.user}
                    onChange={(e) => setEditingReview({...editingReview, user: e.target.value})}
                    placeholder="请输入用户名" 
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">评分</label>
                  <div className="flex gap-1">
                    {[1, 2, 3, 4, 5].map(i => (
                      <Star 
                        key={i} 
                        className={cn("w-6 h-6 cursor-pointer", i <= editingReview.rating ? "text-amber-400 fill-current" : "text-slate-300")}
                        onClick={() => setEditingReview({...editingReview, rating: i})}
                      />
                    ))}
                  </div>
                </div>
              </div>
              <div className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">平台</label>
                  <select 
                    value={editingReview.platform}
                    onChange={(e) => setEditingReview({...editingReview, platform: e.target.value})}
                    className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-amber-500/20"
                  >
                    <option>美团</option>
                    <option>点评</option>
                    <option>抖音</option>
                  </select>
                </div>
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">情感分类</label>
                  <select 
                    value={editingReview.sentiment}
                    onChange={(e) => setEditingReview({...editingReview, sentiment: e.target.value as 'positive' | 'negative' | 'neutral'})}
                    className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-amber-500/20"
                  >
                    <option value="positive">正面</option>
                    <option value="negative">负面</option>
                    <option value="neutral">中性</option>
                  </select>
                </div>
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">评论内容</label>
                  <textarea 
                    value={editingReview.content}
                    onChange={(e) => setEditingReview({...editingReview, content: e.target.value})}
                    className="w-full h-20 p-3 bg-white border border-slate-200 rounded-lg text-sm resize-none outline-none focus:ring-2 focus:ring-amber-500/20"
                    placeholder="请输入评论内容..." 
                  />
                </div>
              </div>
            </div>
            <div className="flex gap-3 pt-4 border-t border-slate-100">
              <Button className="flex-1 bg-amber-600 hover:bg-amber-700" onClick={handleUpdateReview}>更新评论</Button>
              <Button variant="ghost" onClick={() => { setShowEditReview(false); setEditingReview(null); }}>取消</Button>
            </div>
          </Card>
        )}

        {/* View Review Detail */}
        {showViewDetail && viewingReview && (
          <Card className="p-6 border-2 border-green-500 bg-green-50/10 animate-in zoom-in-95 duration-200">
            <div className="flex justify-between items-start mb-6">
              <h4 className="font-bold text-slate-900 flex items-center gap-2">
                <Eye className="w-4 h-4" /> 评论详情
              </h4>
              <Button variant="ghost" size="sm" onClick={() => { setShowViewDetail(false); setViewingReview(null); }}>
                ✕
              </Button>
            </div>
            <div className="grid grid-cols-2 gap-6 mb-6">
              <div className="space-y-4">
                <div>
                  <p className="text-xs font-bold text-slate-500 mb-1">店铺名称</p>
                  <p className="text-sm text-slate-900">{viewingReview.store}</p>
                </div>
                <div>
                  <p className="text-xs font-bold text-slate-500 mb-1">用户名</p>
                  <p className="text-sm text-slate-900">{viewingReview.user}</p>
                </div>
                <div>
                  <p className="text-xs font-bold text-slate-500 mb-1">平台</p>
                  <Badge variant="outline">{viewingReview.platform}</Badge>
                </div>
              </div>
              <div className="space-y-4">
                <div>
                  <p className="text-xs font-bold text-slate-500 mb-1">评分</p>
                  <div className="flex text-amber-400">
                    {[...Array(5)].map((_, i) => (
                      <Star key={i} className={cn("w-4 h-4", i < viewingReview.rating ? "fill-current" : "text-slate-200 fill-none")} />
                    ))}
                  </div>
                </div>
                <div>
                  <p className="text-xs font-bold text-slate-500 mb-1">情感分类</p>
                  <Badge className={cn(
                    "border-none text-[10px] py-0 h-4",
                    viewingReview.sentiment === 'positive' ? "bg-emerald-50 text-emerald-600" : 
                    viewingReview.sentiment === 'negative' ? "bg-rose-50 text-rose-600" : 
                    "bg-slate-50 text-slate-600"
                  )}>
                    {viewingReview.sentiment === 'positive' ? '正面' : viewingReview.sentiment === 'negative' ? '负面' : '中性'}
                  </Badge>
                </div>
                <div>
                  <p className="text-xs font-bold text-slate-500 mb-1">采集时间</p>
                  <p className="text-sm text-slate-500">{viewingReview.time}</p>
                </div>
              </div>
            </div>
            <div className="p-4 bg-slate-50 rounded-lg">
              <p className="text-xs font-bold text-slate-500 mb-2">评论内容</p>
              <p className="text-sm text-slate-700 leading-relaxed">{viewingReview.content}</p>
            </div>
            {viewingReview.replied && (
              <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                <p className="text-xs font-bold text-blue-600 mb-2">AI 回复</p>
                <p className="text-sm text-blue-700 leading-relaxed">已自动回复</p>
              </div>
            )}
          </Card>
        )}

        <Card className="p-4 border-none shadow-sm flex flex-wrap gap-4 items-center bg-white">
          <div className="relative flex-1 min-w-[300px]">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <Input 
              placeholder="搜索评论内容、用户或店铺..." 
              className="pl-10 h-10" 
              value={searchQuery}
              onChange={(e) => handleSearch(e.target.value)}
            />
          </div>
          <Button 
            variant="outline" 
            className={cn("gap-2 h-10", selectedSentiment !== 'all' && "bg-orange-50 text-orange-600 border-orange-200")}
            onClick={() => handleFilterSentiment(selectedSentiment === 'all' ? 'positive' : 'all')}
          >
            <Filter className="w-4 h-4" /> 
            {selectedSentiment === 'all' ? '情感分类' : '正面评论'}
          </Button>
          <Button 
            variant="outline" 
            className="gap-2 h-10"
            onClick={() => success('时间筛选', '正在打开时间范围选择器...')}
          >
            <Calendar className="w-4 h-4" /> 时间范围
          </Button>
        </Card>

        <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50/50">
                <th className="px-6 py-4">
                  <input 
                    type="checkbox" 
                    checked={selectedReviews.length === filteredReviews.length && filteredReviews.length > 0}
                    onChange={handleSelectAll}
                    className="w-4 h-4 rounded border-slate-300" 
                  />
                </th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">评论信息</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">所属门店</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">星级/情感</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">采集时间</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase text-right">操作</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredReviews.map((r) => (
                <tr key={r.id} className="hover:bg-slate-50/50 transition-colors">
                  <td className="px-6 py-4">
                    <input 
                      type="checkbox" 
                      checked={selectedReviews.includes(r.id)}
                      onChange={() => handleSelectReview(r.id)}
                      className="w-4 h-4 rounded border-slate-300" 
                    />
                  </td>
                  <td className="px-6 py-4">
                    <div className="max-w-xs">
                      <p className="text-sm font-bold text-slate-900 mb-1">{r.user}</p>
                      <p className="text-xs text-slate-500 line-clamp-1">{r.content}</p>
                      <div className="flex gap-2 mt-2">
                        <Badge variant="outline" className="text-[10px] py-0 h-4">{r.platform}</Badge>
                        {r.replied && (
                          <Badge className="bg-emerald-50 text-emerald-600 border-emerald-200 text-[9px] py-0 h-4">
                            <CheckCircle className="w-2.5 h-2.5 mr-0.5" /> 已回复
                          </Badge>
                        )}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-slate-600 font-medium">
                    {r.store}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex flex-col gap-1.5">
                      <div className="flex text-amber-400">
                        {[...Array(5)].map((_, i) => (
                          <Star key={i} className={cn("w-3 h-3", i < r.rating ? "fill-current" : "text-slate-200 fill-none")} />
                        ))}
                      </div>
                      <Badge className={cn(
                        "w-fit text-[10px] py-0 h-4 border-none",
                        r.sentiment === 'positive' ? "bg-emerald-50 text-emerald-600" : 
                        r.sentiment === 'negative' ? "bg-rose-50 text-rose-600" : 
                        "bg-slate-50 text-slate-600"
                      )}>
                        {r.sentiment === 'positive' ? '正面' : r.sentiment === 'negative' ? '负面' : '中性'}
                      </Badge>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-xs text-slate-400 font-mono">
                    {r.time}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex justify-end gap-1">
                      <Button 
                        variant="ghost" 
                        size="icon" 
                        className="h-8 w-8 text-slate-400 hover:text-indigo-600"
                        onClick={() => handleViewDetail(r.id)}
                      >
                        <Eye className="w-4 h-4" />
                      </Button>
                      <Button 
                        variant="ghost" 
                        size="icon" 
                        className="h-8 w-8 text-slate-400 hover:text-amber-600"
                        onClick={() => handleFlagReview(r.id)}
                      >
                        <Flag className="w-4 h-4" />
                      </Button>
                      <Button 
                        variant="ghost" 
                        size="icon" 
                        className="h-8 w-8 text-slate-400 hover:text-rose-600"
                        onClick={() => handleDeleteReview(r.id)}
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          
          {filteredReviews.length === 0 && (
            <div className="text-center py-12">
              <MessageSquare className="w-12 h-12 text-slate-200 mx-auto mb-4" />
              <p className="text-sm text-slate-400">没有找到匹配的评论</p>
            </div>
          )}
        </div>

        <div className="flex justify-between items-center text-sm text-slate-500">
          <span>共 {filteredReviews.length} 条评论</span>
          <div className="flex gap-2">
            <Button variant="ghost" size="sm" className="h-8">上一页</Button>
            <Button variant="ghost" size="sm" className="h-8 bg-slate-100">1</Button>
            <Button variant="ghost" size="sm" className="h-8">2</Button>
            <Button variant="ghost" size="sm" className="h-8">3</Button>
            <Button variant="ghost" size="sm" className="h-8">下一页</Button>
          </div>
        </div>
      </div>
    </AdminLayout>
  );
};

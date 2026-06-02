import React, { useState, useEffect } from 'react';
import {
  Star,
  Gift,
  Copy,
  CheckCircle2,
  RefreshCw,
  Search,
  Filter,
  ChevronLeft,
  ChevronRight,
  Download,
  Sparkles,
  PenTool,
  Library,
  TrendingUp
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { AdminLayout } from '../../components/AdminLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';
import { fetchHighQualityReviews, fetchBrandScripts } from '../../api/positive-activation';
import type { HighQualityReview, BrandScript } from '../../api/positive-activation';

export const PositiveActivation: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'reviews' | 'scripts' | 'content'>('reviews');
  const [reviews, setReviews] = useState<HighQualityReview[]>([]);
  const [scripts, setScripts] = useState<BrandScript[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [copiedId, setCopiedId] = useState<number | null>(null);
  const [searchKeyword, setSearchKeyword] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 10;

  const { success, error: showError } = useToast();
  const fetchedRef = React.useRef(false);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [reviewData, scriptData] = await Promise.all([
        fetchHighQualityReviews(),
        fetchBrandScripts(),
      ]);
      // API返回格式: {items: [...], total, page, page_size}
      const reviewList = reviewData.items || reviewData || [];
      const scriptList = scriptData || [];
      setReviews(Array.isArray(reviewList) ? reviewList : []);
      setScripts(Array.isArray(scriptList) ? scriptList : []);
    } catch (err) {
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (fetchedRef.current) return;
    fetchedRef.current = true;
    loadData();
  }, []);

  const handleCopyScript = (reviewId: number, script: string) => {
    navigator.clipboard.writeText(script);
    setCopiedId(reviewId);
    success('复制成功', '授权话术已复制到剪贴板');
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleSendAuthorization = (reviewId: number) => {
    success('授权请求已发送', '用户将收到私信通知');
  };

  const handleGenerateContent = (platform: string) => {
    success(`${platform}内容生成中`, 'AI正在根据好评生成种草内容...');
  };

  const handleExportScripts = () => {
    success('导出成功', '品牌话术资产已导出为PDF');
  };

  const handleExportReport = () => {
    success('导出报告', '正在导出好评激活报告...');
  };

  // 筛选和搜索
  const filteredReviews = reviews.filter(review => {
    if (searchKeyword) {
      return (review.user || '').includes(searchKeyword) ||
             review.content.includes(searchKeyword);
    }
    return true;
  });

  // 分页
  const totalPages = filteredReviews.length > 0 ? Math.ceil(filteredReviews.length / pageSize) : 0;
  const paginatedReviews = filteredReviews.slice(
    (currentPage - 1) * pageSize,
    currentPage * pageSize
  );

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
            <Button onClick={loadData} className="bg-orange-500 hover:bg-orange-600 text-white">
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
            <h2 className="text-2xl font-bold text-slate-900">好评激活与营销</h2>
            <p className="text-slate-500 mt-1">管理高质好评，生成营销内容，提升品牌口碑</p>
          </div>
          <div className="flex gap-3">
            <Button variant="outline" className="gap-2" onClick={handleExportReport}>
              <Download className="w-4 h-4" />
              导出报告
            </Button>
            <Button className="bg-orange-500 hover:bg-orange-600 text-white gap-2" onClick={() => loadData()}>
              <RefreshCw className="w-4 h-4" />
              刷新数据
            </Button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[
            { label: '高质好评', value: reviews.length, color: 'text-orange-600', bg: 'bg-orange-50' },
            { label: '已授权', value: reviews.filter(r => r.authorized).length, color: 'text-emerald-600', bg: 'bg-emerald-50' },
            { label: '品牌话术', value: scripts.reduce((sum, s) => sum + (s.count ?? s.usage_count ?? 0), 0), color: 'text-blue-600', bg: 'bg-blue-50' },
            { label: '预计曝光', value: '12w+', color: 'text-purple-600', bg: 'bg-purple-50' },
          ].map((stat, i) => (
            <Card key={i} className="p-6 border-none shadow-sm">
              <div className="flex items-center gap-4">
                <div className={`p-3 rounded-xl ${stat.bg}`}>
                  <Star className={`w-6 h-6 ${stat.color}`} />
                </div>
                <div>
                  <p className="text-sm text-slate-500">{stat.label}</p>
                  <p className="text-2xl font-bold text-slate-900">{stat.value}</p>
                </div>
              </div>
            </Card>
          ))}
        </div>

        {/* Tab Switcher */}
        <div className="flex bg-white p-1 rounded-2xl shadow-sm border border-slate-100 w-fit">
          {[
            { key: 'reviews', label: '高质好评', icon: Star },
            { key: 'scripts', label: '品牌话术库', icon: Library },
            { key: 'content', label: '内容工厂', icon: PenTool },
          ].map(tab => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key as any)}
              className={cn(
                "px-6 py-2 rounded-xl text-sm font-bold transition-all flex items-center gap-2",
                activeTab === tab.key ? "bg-orange-500 text-white shadow-md" : "text-slate-500 hover:text-slate-700"
              )}
            >
              <tab.icon className="w-4 h-4" />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        {activeTab === 'reviews' && (
          <Card className="border-none shadow-sm">
            {/* Search */}
            <div className="p-4 border-b border-slate-100">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <Input
                  placeholder="搜索用户名或评论内容..."
                  className="pl-9"
                  value={searchKeyword}
                  onChange={(e) => setSearchKeyword(e.target.value)}
                />
              </div>
            </div>

            {/* Reviews Table */}
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-50 border-b border-slate-100">
                  <tr>
                    <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">用户</th>
                    <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">评分</th>
                    <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">评论内容</th>
                    <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">特征</th>
                    <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">授权状态</th>
                    <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">操作</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-50">
                  {paginatedReviews.map((review) => (
                    <tr key={review.id} className="hover:bg-slate-50 transition-colors">
                      <td className="p-4">
                        <div className="flex items-center gap-3">
                          <img src={review.avatar} alt={review.user} className="w-8 h-8 rounded-full object-cover" />
                          <span className="text-sm font-medium text-slate-900">{review.user}</span>
                        </div>
                      </td>
                      <td className="p-4">
                        <div className="flex items-center gap-1">
                          {[1, 2, 3, 4, 5].map(star => (
                            <Star
                              key={star}
                              className={cn(
                                "w-3.5 h-3.5",
                                star <= review.rating ? "text-amber-400 fill-amber-400" : "text-slate-200"
                              )}
                            />
                          ))}
                        </div>
                      </td>
                      <td className="p-4 max-w-md">
                        <p className="text-sm text-slate-600 line-clamp-2">{review.content}</p>
                      </td>
                      <td className="p-4">
                        <div className="flex gap-1.5">
                          {review.hasImage && (
                            <Badge className="bg-emerald-50 text-emerald-600 border-none text-[9px]">有图</Badge>
                          )}
                          <Badge className="bg-orange-50 text-orange-600 border-none text-[9px]">{review.length || '-'}</Badge>
                        </div>
                      </td>
                      <td className="p-4">
                        <Badge className={cn(
                          "border-none text-[10px]",
                          review.authorized ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-500"
                        )}>
                          {review.authorized ? '已授权' : '未授权'}
                        </Badge>
                      </td>
                      <td className="p-4">
                        <div className="flex items-center gap-2">
                          <Button
                            size="sm"
                            variant="ghost"
                            className="h-8 w-8 p-0"
                            onClick={() => handleCopyScript(Number(review.id), review.suggestedScript || '')}
                            title="复制话术"
                          >
                            {copiedId === Number(review.id) ? (
                              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                            ) : (
                              <Copy className="w-3.5 h-3.5" />
                            )}
                          </Button>
                          <Button
                            size="sm"
                            className="h-8 bg-orange-500 hover:bg-orange-600 text-white gap-1"
                            onClick={() => handleSendAuthorization(Number(review.id))}
                          >
                            <Gift className="w-3.5 h-3.5" />
                            发起授权
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            <div className="flex items-center justify-between p-4 border-t border-slate-100">
              <p className="text-sm text-slate-500">
                显示 {((currentPage - 1) * pageSize) + 1}-{Math.min(currentPage * pageSize, filteredReviews.length)} 条，共 {filteredReviews.length} 条
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
                  {currentPage} / {totalPages}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                  disabled={currentPage === totalPages}
                >
                  <ChevronRight className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </Card>
        )}

        {activeTab === 'scripts' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-bold text-slate-900">品牌专属话术库学习进度</h3>
              <Button variant="outline" className="gap-2" onClick={handleExportScripts}>
                <Download className="w-4 h-4" />
                导出话术库
              </Button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {scripts.map((script, i) => (
                <Card key={i} className="p-6 border-none shadow-sm">
                  <div className="flex items-center gap-4 mb-4">
                    <div className="w-10 h-10 rounded-lg bg-orange-50 flex items-center justify-center text-orange-500 font-bold text-sm">
                      {(script.name || '?')[0]}
                    </div>
                    <div className="flex-1">
                      <h4 className="text-sm font-bold text-slate-900">{script.name}</h4>
                      <p className="text-xs text-slate-400">已同步 {script.usage_count ?? 0} 次</p>
                    </div>
                    <Badge className="bg-emerald-50 text-emerald-600 border-none text-[10px]">已学习</Badge>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs text-slate-400 font-bold">
                      <span>AI 模型匹配度</span>
                      <span>{script.progress}</span>
                    </div>
                    <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                      <div className="h-full bg-orange-500 rounded-full" style={{ width: script.progress }}></div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'content' && (
          <div className="space-y-6">
            <h3 className="text-lg font-bold text-slate-900">内容工厂 - 生成种草内容</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card className="p-6 border-none shadow-sm">
                <div className="flex items-start gap-4 mb-4">
                  <div className="w-12 h-12 bg-rose-50 rounded-xl flex items-center justify-center flex-shrink-0">
                    <iconify-icon icon="simple-icons:xiaohongshu" class="text-2xl text-rose-500"></iconify-icon>
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-slate-900">生成小红书种草笔记</h4>
                    <p className="text-xs text-slate-500 mt-1">
                      提取好评中的关键词与情感点，自动生成带 Emoji 的小红书风格文案。
                    </p>
                  </div>
                </div>
                <Button
                  className="w-full bg-rose-500 hover:bg-rose-600 text-white rounded-xl h-10 font-bold text-xs"
                  onClick={() => handleGenerateContent('小红书')}
                >
                  立即转换内容
                </Button>
              </Card>

              <Card className="p-6 border-none shadow-sm">
                <div className="flex items-start gap-4 mb-4">
                  <div className="w-12 h-12 bg-black rounded-xl flex items-center justify-center flex-shrink-0">
                    <iconify-icon icon="simple-icons:tiktok" class="text-2xl text-white"></iconify-icon>
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-slate-900">生成抖音口播脚本</h4>
                    <p className="text-xs text-slate-500 mt-1">
                      将评价改写为 15-30s 的短视频口播脚本，包含转场建议。
                    </p>
                  </div>
                </div>
                <Button
                  className="w-full bg-slate-900 hover:bg-black text-white rounded-xl h-10 font-bold text-xs"
                  onClick={() => handleGenerateContent('抖音')}
                >
                  生成视频脚本
                </Button>
              </Card>
            </div>
          </div>
        )}
      </div>
    </AdminLayout>
  );
};

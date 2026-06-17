import React, { useState, useEffect, useRef } from 'react';
import {
  Search,
  Filter,
  Star,
  MessageSquare,
  ThumbsUp,
  MoreVertical,
  RefreshCw,
  CheckCircle2,
  AlertCircle,
  Clock,
  Download,
  UtensilsCrossed,
  Zap,
  Flame,
  MessageCircle,
  FileText,
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Skeleton } from '../../components/ui/skeleton';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { Tabs, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { MobileLayout, useStore } from '../../components/MobileLayout';
import { cn, normalizeImageUrls, useSearchDebounce } from '../../lib/utils';

// 格式化评论时间为友好字符串
function formatReviewTime(dateStr?: string | null): string {
  if (!dateStr) return '';
  try {
    const d = new Date(dateStr);
    const now = new Date();
    const diff = now.getTime() - d.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return '刚刚';
    if (minutes < 60) return `${minutes}分钟前`;
    if (hours < 24) return `${hours}小时前`;
    if (days < 7) return `${days}天前`;
    // 超过7天显示完整日期
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    const hh = String(d.getHours()).padStart(2, '0');
    const mi = String(d.getMinutes()).padStart(2, '0');
    return `${mm}-${dd} ${hh}:${mi}`;
  } catch {
    return '';
  }
}
// 清理 HTML 内容中不安全的标签，保留 img 和基本格式
function sanitizeHtmlContent(html: string): string {
  if (!html) return html;
  if (!/<\w+[\s>]/.test(html)) return html;
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<iframe[\s\S]*?<\/iframe>/gi, '')
    .replace(/<object[\s\S]*?<\/object>/gi, '')
    .replace(/on\w+\s*=\s*"[^"]*"/gi, '')
    .replace(/on\w+\s*=\s*'[^']*'/gi, '')
    .replace(/on\w+\s*=\s*\S+/gi, '')
    .replace(/javascript\s*:/gi, '');
}

// 检测内容是否包含 HTML
function containsHtml(str: string): boolean {
  return /<(img|br|p|div|span|b|i|em|strong|a)[\s>]/i.test(str);
}

import { useToast } from '../../hooks/use-toast';
import { useNavigate } from 'react-router-dom';
import { fetchReviews } from '../../api/reviews';
import { storesApi } from '../../api/stores';
import { platformsApi } from '../../api/platforms';
import type { Review } from '../../api/reviews';
import type { Store } from '../../api/stores';
import type { PlatformAccount } from '../../api/platforms';
import { useSubscription, SubscriptionPrompt } from '../../hooks/use-subscription-check';

export const ReviewStream: React.FC = () => {
  const { success, error: toastError } = useToast();
  const navigate = useNavigate();
  const { selectedStore } = useStore();
  const [activeTab, setActiveTab] = useState<'all' | 'positive' | 'negative'>('all');
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [syncingReviews, setSyncingReviews] = useState(false);
  const [searchKeyword, setSearchKeyword] = useState('');
  const { inputValue: searchInput, debouncedValue: debouncedKeyword, handleChange: handleSearchInput } = useSearchDebounce();
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);

  // ===== 订阅状态检测（必须在条件返回之前）=====
  const {
    subscription,
    loading: subscriptionLoading,
    error: subscriptionError,
    hasValidSubscription,
  } = useSubscription();

  // ===== 监听店铺切换自定义事件（双重保险）=====
  useEffect(() => {
    const handler = (e: CustomEvent<Store>) => {
      const storeFromEvent = e.detail;
      console.log('[ReviewStream] zc-store-changed event:', storeFromEvent?.name, storeFromEvent?.id);
      if (storeFromEvent?.id) {
        loadReviews(storeFromEvent.id);
      }
    };
    window.addEventListener('zc-store-changed', handler as any);
    return () => window.removeEventListener('zc-store-changed', handler as any);
  }, []);

  // ===== 店铺变化 或 tab 切换 都触发重新加载 =====
  useEffect(() => {
    if (!hasValidSubscription) return;
    const effectiveStoreId = selectedStore?.id || localStorage.getItem('zc_selected_store_id');
    if (!effectiveStoreId) {
      setReviews([]);
      setLoading(false);
      setHasMore(false);
      return;
    }
    console.log('[ReviewStream] load by store/tab change:', effectiveStoreId, activeTab);
    loadReviews(effectiveStoreId, false, activeTab);
  }, [hasValidSubscription, selectedStore?.id, activeTab]);

  // ===== 搜索关键词变化 → 重新加载 =====
  useEffect(() => {
    if (!hasValidSubscription) return;
    const effectiveStoreId = selectedStore?.id || localStorage.getItem('zc_selected_store_id');
    if (effectiveStoreId) {
      loadReviews(effectiveStoreId, false, activeTab);
    }
  }, [searchKeyword, hasValidSubscription]);

  const loadReviews = async (
    storeId?: string,
    loadMoreFlag?: boolean,
    sentimentFilter?: 'all' | 'positive' | 'negative'
  ) => {
    try {
      if (!loadMoreFlag) {
        setLoading(true);
        setFetchError(null);
      } else {
        setLoadingMore(true);
      }
      const filters: any = {};
      // 用 rating 过滤，比不可靠的 sentiment 字段更准确
      if (sentimentFilter === 'negative') {
        filters.rating_max = 2;
      } else if (sentimentFilter === 'positive') {
        filters.rating_min = 4;
      }
      const effectiveStoreId = storeId || selectedStore?.id || localStorage.getItem('zc_selected_store_id');
      if (effectiveStoreId) {
        filters.store_id = effectiveStoreId;
      } else {
        if (!loadMoreFlag) {
          setReviews([]);
          setLoading(false);
        }
        return;
      }

      const currentPage = loadMoreFlag ? page : 1;
      filters.page = currentPage;
      filters.page_size = 20;

      console.log('[ReviewStream] loadReviews filters:', filters);
      const response = await fetchReviews(filters);
      console.log('[ReviewStream] API response:', response);

      const items = response.items || [];
      const total = response.total || 0;
      console.log('[ReviewStream] items count:', items.length, 'total:', total);

      const mapped = items.map((r: any) => ({
        ...r,
        user: r.user_name || '匿名用户',
        avatar: r.user_avatar || '',
        // 格式化时间显示，优先用评论时间
        time: formatReviewTime(r.platform_created_at || r.created_at),
        hasImage: !!(r.images && r.images.length > 0),
        imageUrls: normalizeImageUrls(r.images),
      }));

      if (loadMoreFlag) {
        setReviews(prev => [...prev, ...(Array.isArray(mapped) ? mapped : [])]);
        setPage(prev => prev + 1);
      } else {
        setReviews(Array.isArray(mapped) ? mapped : []);
        setPage(2);
      }

      const loadedCount = loadMoreFlag ? reviews.length + mapped.length : mapped.length;
      setHasMore(loadedCount < total);

    } catch (err) {
      setFetchError(err instanceof Error ? err.message : '获取数据失败');
      if (!loadMoreFlag) {
        setReviews([]);
      }
    } finally {
      if (!loadMoreFlag) {
        setLoading(false);
      } else {
        setLoadingMore(false);
      }
    }
  };

  const handleRefresh = async () => {
    setIsRefreshing(true);
    setPage(1);
    setHasMore(true);
    await loadReviews(undefined, false, activeTab);
    setIsRefreshing(false);
    success('刷新完成', '已重新加载评论数据');
  };

  // 同步评论数据 — 自动检测关联平台，增量同步
  const handleSyncReviews = async () => {
    const effectiveStoreId = selectedStore?.id || localStorage.getItem('zc_selected_store_id');
    if (!effectiveStoreId) {
      toastError('请先选择店铺');
      return;
    }

    setSyncingReviews(true);
    try {
      // 第一步：获取用户关联的平台账号
      const accounts: PlatformAccount[] = await platformsApi.getAccounts();
      if (!accounts || accounts.length === 0) {
        toastError('暂无平台账号', '请先在"平台连接"中绑定平台账号');
        return;
      }

      // 按平台分组，确定需要同步哪些平台
      const platformNames: Record<string, string> = {
        meituan: '美团',
        dianping: '大众点评',
        douyin: '抖音',
      };

      let totalCreated = 0;
      let totalSkipped = 0;
      let syncErrors: string[] = [];
      const syncedPlatforms: string[] = [];

      // 第二步：对每个账号触发异步增量同步，轮询等待结果
      for (const account of accounts) {
        try {
          // 启动异步同步任务
          const { task_id } = await platformsApi.syncAccountReviews(account.id, 'incremental');

          // 轮询等待结果（最多 10 分钟）
          const maxPolls = 120; // 120 * 5s = 600s
          let pollCount = 0;
          let syncDone = false;

          while (pollCount < maxPolls && !syncDone) {
            await new Promise(r => setTimeout(r, 5000)); // 5 秒轮询
            pollCount++;

            const status = await platformsApi.getSyncReviewsStatus(account.id, task_id);
            if (status.status === 'success' || status.status === 'failed') {
              syncDone = true;

              if (status.status === 'success' && status.result) {
                totalCreated += status.result.created || 0;
                totalSkipped += status.result.skipped || 0;
                if (status.result.errors && status.result.errors.length > 0) {
                  syncErrors.push(...status.result.errors);
                }
                // 记录同步的平台
                if (account.platform && !syncedPlatforms.includes(account.platform)) {
                  syncedPlatforms.push(account.platform);
                }
              } else {
                syncErrors.push(status.error || `${platformNames[account.platform] || account.platform} 同步失败`);
              }
            }
          }

          if (!syncDone) {
            syncErrors.push(`${platformNames[account.platform] || account.platform} 同步超时`);
          }
        } catch (err: any) {
          // 单个账号同步失败不影响其他账号
          syncErrors.push(`${platformNames[account.platform] || account.platform}: ${err.message || '未知错误'}`);
        }
      }

      // 第三步：显示结果
      if (syncedPlatforms.length > 0) {
        const names = syncedPlatforms.map(p => platformNames[p] || p).join('+');
        success(
          '评论增量同步完成',
          `${names}：新增 ${totalCreated} 条${totalSkipped > 0 ? `，跳过 ${totalSkipped} 条重复` : ''}${syncErrors.length > 0 ? `，${syncErrors.length} 个错误` : ''}`
        );
      } else if (syncErrors.length > 0) {
        toastError('评论同步失败', syncErrors[0]);
      }

      // 刷新评论列表
      await loadReviews(undefined, false, activeTab);
      // 触发 StoreContext 刷新店铺数据（评论数会变）
      window.dispatchEvent(new Event('visibilitychange'));
    } catch (err: any) {
      toastError('评论同步失败', err.message || '网络错误');
    } finally {
      setSyncingReviews(false);
    }
  };

  // 防抖搜索词同步到 searchKeyword
  useEffect(() => {
    setSearchKeyword(debouncedKeyword);
  }, [debouncedKeyword]);

  const handleFilterClick = () => {
    success('筛选功能', '筛选面板即将上线');
  };

  const handleReviewClick = (reviewId: string) => {
    navigate(`/mobile/review-detail/${reviewId}`);
  };

  const handleLike = (reviewId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    success('赞同成功', '已标记为有价值评论');
  };

  const handleQuickReply = (reviewId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    success('快速回复', 'AI 正在生成回复话术...');
  };

  const handleMoreActions = (reviewId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    success('更多操作', '举报、隐藏、置顶等功能开发中');
  };

  // ===== 条件渲染 =====

  if (subscriptionLoading) {
    return (
      <MobileLayout title="评论瀑布流">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-sm text-slate-400">正在检查订阅状态...</p>
          </div>
        </div>
      </MobileLayout>
    );
  }

  if (!hasValidSubscription) {
    return (
      <MobileLayout title="评论瀑布流">
        <SubscriptionPrompt featureName="评论" />
      </MobileLayout>
    );
  }

  if (loading) {
    return (
      <MobileLayout title="评论瀑布流">
        <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500 p-4">
          <Skeleton lines={1} className="h-8 w-48 mb-4" />
          <Skeleton card className="mt-4" />
          <Skeleton lines={3} className="mt-4 space-y-3" />
        </div>
      </MobileLayout>
    );
  }

  if (fetchError) {
    return (
      <MobileLayout title="评论瀑布流">
        <div className="p-4">
          <Card className="p-6 text-center">
            <AlertCircle className="w-12 h-12 text-rose-500 mx-auto mb-4" />
            <p className="text-sm text-slate-600 mb-4">{fetchError}</p>
            <Button onClick={() => {
              const id = selectedStore?.id || localStorage.getItem('zc_selected_store_id');
              if (id) loadReviews(id, false, activeTab);
            }} className="bg-orange-500 hover:bg-orange-600 text-white">
              重试
            </Button>
          </Card>
        </div>
      </MobileLayout>
    );
  }

  const hasStore = selectedStore?.id || localStorage.getItem('zc_selected_store_id');
  const noStoreWarning = !hasStore ? (
    <Card className="p-4 text-center border-amber-200 bg-amber-50">
      <p className="text-sm text-amber-600">请通过顶部导航选择店铺以筛选评论</p>
    </Card>
  ) : null;

  return (
    <MobileLayout title="评论瀑布流">
      {noStoreWarning}
      <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500 pb-20">

        {/* Spider Status Card */}
        <Card className="p-4 border-none shadow-sm bg-orange-50/50 border border-orange-100/50">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <RefreshCw className={cn("w-3.5 h-3.5 text-orange-600", syncingReviews && "animate-spin")} />
              <span className="text-xs font-bold text-slate-800 uppercase tracking-tight">
                {syncingReviews ? '正在同步评论...' : '评论数据管理'}
              </span>
            </div>
          </div>

          <div className="flex gap-2">
            <Button
              size="sm"
              className="flex-1 h-8 bg-orange-500 hover:bg-orange-600 text-white text-xs font-bold rounded-lg"
              onClick={handleSyncReviews}
              disabled={syncingReviews}
            >
              {syncingReviews ? (
                <>
                  <RefreshCw className="w-3 h-3 mr-1 animate-spin" />
                  同步中...
                </>
              ) : (
                <>
                  <FileText className="w-3 h-3 mr-1" />
                  同步评论
                </>
              )}
            </Button>
            <Button
              size="sm"
              variant="outline"
              className="flex-1 h-8 border-orange-200 text-orange-600 hover:bg-orange-50 text-xs font-bold rounded-lg"
              onClick={handleRefresh}
              disabled={isRefreshing}
            >
              {isRefreshing ? (
                <>
                  <RefreshCw className="w-3 h-3 mr-1 animate-spin" />
                  刷新中...
                </>
              ) : (
                <>
                  <RefreshCw className="w-3 h-3 mr-1" />
                  刷新列表
                </>
              )}
            </Button>
          </div>
        </Card>

        {/* Search and Filters */}
        <div className="flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <Input 
              placeholder="搜索菜品、评价关键词..." 
              className="pl-9 bg-white border-none shadow-sm h-10 text-sm rounded-xl"
              value={searchInput}
              onChange={(e) => handleSearchInput(e.target.value)}
            />
          </div>
          <Button 
            variant="outline" 
            size="icon" 
            className="h-10 w-10 bg-white border-none shadow-sm rounded-xl"
            onClick={handleFilterClick}
          >
            <Filter className="w-4 h-4 text-slate-600" />
          </Button>
        </div>

        {/* Tabs */}
        <div className="flex bg-white p-1 rounded-xl shadow-sm border border-slate-100">
           {['全部', '好评', '差评'].map((tab) => {
             const tabKey = tab === '全部' ? 'all' : tab === '好评' ? 'positive' : 'negative';
             return (
               <button 
                 key={tab}
                 onClick={() => setActiveTab(tabKey)}
                 className={cn(
                   "flex-1 py-1.5 text-xs font-bold rounded-lg transition-all",
                   activeTab === tabKey ? "bg-orange-500 text-white shadow-sm" : "text-slate-400"
                 )}
               >
                 {tab}
               </button>
             );
           })}
        </div>

        {/* Review List */}
        <div className="space-y-3">
          {reviews
            .filter(review => {
              if (!searchKeyword.trim()) return true;
              return (
                (review.content || '').includes(searchKeyword) ||
                (review.user || '').includes(searchKeyword) ||
                (review.tags || []).some((tag: string) => tag.includes(searchKeyword))
              );
            })
            .map((review) => (
            <Card 
              key={review.id} 
              className="p-4 border-none shadow-sm bg-white active:bg-slate-50 cursor-pointer hover:shadow-md transition-all"
              onClick={() => handleReviewClick(review.id)}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl overflow-hidden bg-slate-100 shadow-sm border border-slate-50">
                    <img src={review.user_avatar} alt={review.user} className="w-full h-full object-cover" />
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-slate-800">{review.user}</h4>
                    <div className="flex items-center gap-2">
                      <div className="flex">
                        {[...Array(5)].map((_, i) => (
                          <Star key={i} className={cn("w-2 h-2", i < review.rating ? "text-orange-500 fill-orange-500" : "text-slate-200")} />
                        ))}
                      </div>
                      <span className="text-[9px] text-slate-400">{review.time}</span>
                    </div>
                  </div>
                </div>
                <div className="flex flex-col items-end gap-1">
                   <iconify-icon 
                     icon={review.platform === '美团' ? 'simple-icons:meituan' : 
                           review.platform === '大众点评' ? 'simple-icons:dianping' : 
                           review.platform === '抖音' ? 'simple-icons:tiktok' : 'simple-icons:xiaohongshu'} 
                     class={cn("text-base", 
                       review.platform === '美团' ? 'text-yellow-500' : 
                       review.platform === '大众点评' ? 'text-orange-500' : 
                       review.platform === '抖音' ? 'text-black' : 'text-red-600'
                     )}
                   ></iconify-icon>
                   <span className="text-[8px] text-slate-300 uppercase font-black">{review.platform}</span>
                </div>
              </div>

              {containsHtml(review.content || '') ? (
                <div
                  className="text-sm text-slate-600 leading-relaxed mb-3 break-words overflow-wrap-anywhere line-clamp-4 [&_img]:max-w-[1.2rem] [&_img]:h-[1.2rem] [&_img]:inline [&_img]:align-middle [&_img]:mx-[2px] [&_a]:text-orange-500 [&_a]:underline"
                  dangerouslySetInnerHTML={{ __html: sanitizeHtmlContent(review.content || '') }}
                />
              ) : (
                <p className="text-sm text-slate-600 leading-relaxed mb-3 break-words overflow-wrap-anywhere line-clamp-4">
                  {review.content}
                </p>
              )}

              {/* 图片展示 */}
              {(review as any).imageUrls && (review as any).imageUrls.length > 0 && (
                <div className="grid grid-cols-3 gap-1.5 mb-3 rounded-xl overflow-hidden">
                  {(review as any).imageUrls.map((url: string, i: number) => (
                    <div key={i} className="aspect-square bg-slate-100">
                      <img src={url} alt={`评论图片${i + 1}`} className="w-full h-full object-cover" loading="lazy" />
                    </div>
                  ))}
                </div>
              )}

              <div className="flex flex-wrap gap-1.5 mb-4">
                {(review.tags || []).map((tag: string, i: number) => (
                  <Badge key={i} variant="outline" className="text-[9px] px-1.5 py-0 h-4 border-slate-100 bg-slate-50 text-slate-400 font-medium">
                    {tag}
                  </Badge>
                ))}
                {review.hasImage && <Badge className="bg-emerald-50 text-emerald-600 border-none text-[8px] h-4">有图</Badge>}
              </div>

              <div className="flex items-center justify-between pt-3 border-t border-slate-50">
                <div className="flex gap-6">
                  <button 
                    className="flex items-center gap-1.5 text-slate-300 hover:text-orange-500 transition-colors"
                    onClick={(e) => handleLike(review.id, e)}
                  >
                    <ThumbsUp className="w-3.5 h-3.5" />
                    <span className="text-[9px] font-bold">赞同</span>
                  </button>
                  <button 
                    className="flex items-center gap-1.5 text-slate-300 hover:text-orange-500 transition-colors"
                    onClick={(e) => handleQuickReply(review.id, e)}
                  >
                    <MessageSquare className="w-3.5 h-3.5" />
                    <span className="text-[9px] font-bold">快速回复</span>
                  </button>
                </div>
                <Button 
                  variant="ghost" 
                  size="icon" 
                  className="h-8 w-8 text-slate-300"
                  onClick={(e) => handleMoreActions(review.id, e)}
                >
                  <MoreVertical className="w-4 h-4" />
                </Button>
              </div>
            </Card>
          ))}
        </div>

        {/* Load More Button */}
        {hasMore && !loading && (
          <div className="flex justify-center py-4">
            <Button 
              onClick={() => loadReviews(undefined, true, activeTab)}
              disabled={loadingMore}
              variant="outline"
              className="border-orange-200 text-orange-600 hover:bg-orange-50"
            >
              {loadingMore ? (
                <>
                  <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                  加载中...
                </>
              ) : (
                '加载更多'
              )}
            </Button>
          </div>
        )}

        {/* No More Data Hint */}
        {!hasMore && reviews.length > 0 && (
          <div className="text-center py-4 text-xs text-slate-400">
            没有更多数据了
          </div>
        )}

        {/* Empty State */}
        {!loading && reviews.length === 0 && !fetchError && (
          <Card className="p-8 text-center">
            <MessageCircle className="w-12 h-12 text-slate-300 mx-auto mb-3" />
            <p className="text-sm text-slate-500 mb-1">暂无评论数据</p>
            <p className="text-xs text-slate-400">切换店铺或刷新试试</p>
          </Card>
        )}
      </div>
    </MobileLayout>
  );
};

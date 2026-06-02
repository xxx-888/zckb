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
  MessageCircle
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Skeleton } from '../../components/ui/skeleton';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { Tabs, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { MobileLayout, useStore } from '../../components/MobileLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';
import { useNavigate } from 'react-router-dom';
import { fetchReviews } from '../../api/reviews';
import type { Review } from '../../api/reviews';
import type { Store } from '../../api/stores';
import { useSubscription, SubscriptionPrompt } from '../../hooks/use-subscription-check';

export const ReviewStream: React.FC = () => {
  const { success, error: toastError } = useToast();
  const navigate = useNavigate();
  const { selectedStore } = useStore();
  const [activeTab, setActiveTab] = useState<'all' | 'positive' | 'negative'>('all');
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [searchKeyword, setSearchKeyword] = useState('');
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
        time: r.created_at || r.platform_created_at || '',
        hasImage: !!(r.images && r.images.length > 0),
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
    success('数据刷新', '正在从平台获取最新评论...');
    await loadReviews(undefined, false, activeTab);
    setIsRefreshing(false);
    success('刷新完成', '已获取最新评论');
  };

  const handleSearch = (value: string) => {
    setSearchKeyword(value);
    if (value.trim()) {
      success('搜索中', `正在搜索："${value}"`);
    }
  };

  const handleFilterClick = () => {
    success('筛选功能', '筛选面板即将上线');
  };

  const handleReviewClick = (reviewId: number) => {
    navigate(`/mobile/review-detail/${reviewId}`);
  };

  const handleLike = (reviewId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    success('赞同成功', '已标记为有价值评论');
  };

  const handleQuickReply = (reviewId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    success('快速回复', 'AI 正在生成回复话术...');
  };

  const handleMoreActions = (reviewId: number, e: React.MouseEvent) => {
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
              <RefreshCw className={cn("w-3.5 h-3.5 text-orange-600", isRefreshing && "animate-spin")} />
              <span className="text-xs font-bold text-slate-800 uppercase tracking-tight">数据实时同步中...</span>
            </div>
            <span className="text-[10px] text-slate-400">14:25</span>
          </div>

          <div className="flex gap-2">
             {['美团', '点评', '抖音', '小红书'].map((p, i) => (
                <div key={i} className="flex-1 h-1 bg-slate-100 rounded-full overflow-hidden">
                   <div className={cn("h-full", i < 2 ? "bg-orange-500" : i === 2 ? "bg-orange-300" : "bg-slate-200")} style={{ width: i === 2 ? '60%' : '100%' }}></div>
                </div>
             ))}
          </div>
          <div className="flex justify-between items-center mt-2">
             <div className="flex gap-1.5">
                <span className="text-[8px] font-bold text-orange-600">MEITUAN √</span>
                <span className="text-[8px] font-bold text-orange-600">DIANPING √</span>
             </div>
             <Button 
                size="sm" 
                variant="ghost" 
                className="h-5 text-[9px] text-orange-600 p-0 font-bold"
                onClick={handleRefresh}
              >
                刷新数据
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
              value={searchKeyword}
              onChange={(e) => handleSearch(e.target.value)}
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
              onClick={() => handleReviewClick(Number(review.id))}
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

              <p className="text-sm text-slate-600 leading-relaxed mb-3">
                {review.content}
              </p>

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
                    onClick={(e) => handleLike(Number(review.id), e)}
                  >
                    <ThumbsUp className="w-3.5 h-3.5" />
                    <span className="text-[9px] font-bold">赞同</span>
                  </button>
                  <button 
                    className="flex items-center gap-1.5 text-slate-300 hover:text-orange-500 transition-colors"
                    onClick={(e) => handleQuickReply(Number(review.id), e)}
                  >
                    <MessageSquare className="w-3.5 h-3.5" />
                    <span className="text-[9px] font-bold">快速回复</span>
                  </button>
                </div>
                <Button 
                  variant="ghost" 
                  size="icon" 
                  className="h-8 w-8 text-slate-300"
                  onClick={(e) => handleMoreActions(Number(review.id), e)}
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

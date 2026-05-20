import React, { useState, useEffect } from 'react';
import { 
  Search, 
  Filter, 
  Star, 
  MessageSquare, 
  ThumbsUp, 
  MoreVertical,
  RefreshCcw,
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
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { Tabs, TabsList, TabsTrigger } from '../../components/ui/tabs';
import { MobileLayout } from '../../components/MobileLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';
import { useNavigate } from 'react-router-dom';
import { fetchReviews } from '../../api/reviews';
import type { Review } from '../../api/reviews';

export const ReviewStream: React.FC = () => {
  const { success, error: toastError } = useToast();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'all' | 'positive' | 'negative'>('all');
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [searchKeyword, setSearchKeyword] = useState('');
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState<string | null>(null);

  const loadReviews = async () => {
    try {
      setLoading(true);
      setFetchError(null);
      const response = await fetchReviews();
      // 处理分页响应格式
      const items = response.items || response.data || response;
      setReviews(Array.isArray(items) ? items : []);
    } catch (err) {
      setFetchError(err instanceof Error ? err.message : '获取数据失败');
      setReviews([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReviews();
  }, []);

  const handleRefresh = () => {
    setIsRefreshing(true);
    success('数据刷新', '正在从平台获取最新评论...');
    setTimeout(() => {
      setIsRefreshing(false);
      success('刷新完成', '已获取 24 条新评论');
    }, 2000);
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

  return (
    <MobileLayout title="评论瀑布流">
      <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500 pb-20">
        
        {/* Spider Status Card */}
        <Card className="p-4 border-none shadow-sm bg-orange-50/50 border border-orange-100/50">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <RefreshCcw className={cn("w-3.5 h-3.5 text-orange-600", isRefreshing && "animate-spin")} />
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
              if (activeTab === 'positive') return review.sentiment === 'positive';
              if (activeTab === 'negative') return review.sentiment === 'negative';
              return true;
            })
            .filter(review => {
              if (!searchKeyword.trim()) return true;
              return                      review.content.includes(searchKeyword) || 
                     review.user.includes(searchKeyword) ||
                     (review.tags || []).some(tag => tag.includes(searchKeyword));
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
                    <img src={review.avatar} alt={review.user} className="w-full h-full object-cover" />
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
                {(review.tags || []).map((tag, i) => (
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
      </div>
    </MobileLayout>
  );
};


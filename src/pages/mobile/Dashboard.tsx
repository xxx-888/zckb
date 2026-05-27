import React, { useState, useEffect, useCallback } from 'react';
import {
  TrendingUp,
  MessageSquare,
  Star,
  ThumbsUp,
  Calendar,
  Filter,
  ChevronRight,
  BarChart3,
  Award,
  AlertCircle,
  ShieldCheck,
  Zap,
  Flame,
  ChefHat,
  CheckCircle2,
  Bot,
  TrendingDown,
  Store as StoreIcon
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { Skeleton } from '../../components/ui/skeleton';
import { Button } from '../../components/ui/button';
import { MobileLayout, useStore } from '../../components/MobileLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';
import { useNavigate } from 'react-router-dom';
import {
  fetchCoreStats,
  fetchPlatformData,
  fetchRecentReviews,
  fetchStoreRankings,
  fetchHealthStatus,
  fetchAlert,
  fetchStoreHealth,
  type CoreStats,
  type PlatformData,
  type Review,
  type StoreRanking,
  type HealthStatus,
  type AlertData
} from '../../api/dashboard';
import { authApi } from '../../api/auth';
import { useSubscription, SubscriptionPrompt } from '../../hooks/use-subscription-check';

export const Dashboard: React.FC = () => {
  const { success } = useToast();
  const navigate = useNavigate();
  const { selectedStore } = useStore();
  const [currentUser, setCurrentUser] = useState<any>(null);

  // ===== 判断用户角色 =====
  // SUPER_ADMIN / HQ / OPERATOR 都可以看到全量数据（管理视图）
  const isHQ = currentUser?.role === 'SUPER_ADMIN' || currentUser?.role === 'HQ' || currentUser?.role === 'OPERATOR';
  const [showTimeDropdown, setShowTimeDropdown] = useState(false);
  const [timePeriod, setTimePeriod] = useState<'today' | 'yesterday' | '7days' | '30days' | '90days' | 'custom'>('7days');
  const dropdownRef = React.useRef<HTMLDivElement>(null);

  // ===== API 数据状态 =====
  const [coreStats, setCoreStats] = useState<CoreStats | null>(null);
  const [platformData, setPlatformData] = useState<PlatformData[]>([]);
  const [recentReviews, setRecentReviews] = useState<Review[]>([]);
  const [storeRankings, setStoreRankings] = useState<StoreRanking[]>([]);
  const [healthStats, setHealthStats] = useState<HealthStatus[]>([]);
  const [alert, setAlert] = useState<AlertData | null>(null);
  const [storeHealth, setStoreHealth] = useState<{
    store_id: string;
    store_name: string;
    health_score: number;
    review_count: number;
    avg_rating: number;
    reply_rate: number;
    trend: number;
  } | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const lastPeriodRef = React.useRef<string | null>(null);

  // ===== 订阅状态检测 =====
  const {
    subscription,
    loading: subscriptionLoading,
    error: subscriptionError,
    hasValidSubscription,
  } = useSubscription();

  // ===== 时间筛选选项 =====
  const timeOptions = [
    { value: 'today', label: '今天', dateRange: '2026年05月12日' },
    { value: 'yesterday', label: '昨天', dateRange: '2026年05月11日' },
    { value: '7days', label: '最近7天', dateRange: '2026年05月06日 - 05月12日' },
    { value: '30days', label: '最近30天', dateRange: '2026年04月13日 - 05月12日' },
    { value: '90days', label: '最近90天', dateRange: '2026年02月12日 - 05月12日' },
    { value: 'custom', label: '自定义', dateRange: '选择日期范围' },
  ];

  const getCurrentDateRange = () => {
    return timeOptions.find(opt => opt.value === timePeriod)?.dateRange || '';
  };

  const handleTimePeriodChange = (period: 'today' | 'yesterday' | '7days' | '30days' | 'custom') => {
    setTimePeriod(period);
    setShowTimeDropdown(false);
    success('时间筛选', `已切换到${timeOptions.find(opt => opt.value === period)?.label}`);
  };

  const handleFilterClick = () => {
    setShowTimeDropdown(!showTimeDropdown);
  };

  const handleViewAllStores = () => {
    navigate('/mobile/store-list');
  };

  const handleReviewClick = (reviewId: number) => {
    navigate(`/mobile/review-detail/${reviewId}`);
  };

  const handleAlertClick = () => {
    navigate('/mobile/negative-reply');
  };

  // ===== 时间周期映射（前端 → 后端）=====
  const mapPeriod = (tp: string): string => {
    const m: Record<string, string> = {
      'today': '1d',
      'yesterday': '1d',
      '7days': '7d',
      '30days': '30d',
      '90days': '90d',
      'custom': '7d',
    };
    return m[tp] || '7d';
  };

  // ===== 获取数据 =====
  const fetchAllData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const period = mapPeriod(timePeriod);

      console.log('[Dashboard] fetchAllData 开始获取数据, timePeriod:', timePeriod, 'period:', period);
      console.log('[Dashboard] isHQ:', isHQ, 'currentUser.role:', currentUser?.role);

      const [coreStatsRes, platformDataRes, recentReviewsRes, storeRankingsRes, healthStatsRes] = await Promise.all([
        fetchCoreStats(period),
        fetchPlatformData(),
        fetchRecentReviews(5),
        fetchStoreRankings(5),
        fetchHealthStatus(),
      ]);

      console.log('[Dashboard] coreStatsRes:', coreStatsRes);
      console.log('[Dashboard] platformDataRes:', platformDataRes);
      console.log('[Dashboard] recentReviewsRes:', recentReviewsRes);

      setCoreStats(coreStatsRes);
      setPlatformData(platformDataRes);
      setRecentReviews(recentReviewsRes);

      if (isHQ) {
        setStoreRankings(storeRankingsRes);
      } else {
        const storeHealthRes = await fetchStoreHealth();
        console.log('[Dashboard] storeHealthRes:', storeHealthRes);
        if (storeHealthRes && storeHealthRes.length > 0) {
          setStoreHealth(storeHealthRes[0]);
        } else {
          setStoreHealth(null);
        }
      }

      const alertRes = await fetchAlert();
      console.log('[Dashboard] alertRes:', alertRes);
      setAlert(alertRes);

      setHealthStats(healthStatsRes);
    } catch (err) {
      console.error('[Dashboard] fetchAllData 错误:', err);
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally {
      setLoading(false);
    }
  }, [timePeriod, isHQ, currentUser]);

  // ===== 时间周期变化时重新获取数据 =====
  useEffect(() => {
    // 只在 currentUser 加载完成后才获取数据
    if (!currentUser) {
      console.log('[Dashboard] currentUser 为空，不获取数据');
      return;
    }
    console.log('[Dashboard] useEffect [timePeriod, currentUser] 触发，开始获取数据');
    fetchAllData();
  }, [timePeriod, currentUser]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowTimeDropdown(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // ===== 获取当前用户 =====
  useEffect(() => {
    const user = authApi.getStoredUser();
    setCurrentUser(user);
    if (!user) {
      navigate('/mobile/login');
    }
  }, [navigate]);

  // ===== 订阅状态检测（非阻塞）=====
  // 备注：订阅检查在后台进行，不阻塞页面渲染
  // 如果用户没有有效订阅，会在页面上显示提示
  useEffect(() => {
    if (!hasValidSubscription && !subscriptionLoading) {
      // 可以在这里添加订阅过期提示
      console.log('订阅已过期或无效');
    }
  }, [hasValidSubscription, subscriptionLoading]);

  // ===== 调试面板（临时）=====
  const debugInfo = (
    <div className="fixed top-16 left-2 right-2 bg-black/90 text-white text-[10px] p-2 rounded-lg z-50 font-mono overflow-auto max-h-48">
      <p className="text-orange-400 font-bold">⚡ 调试信息</p>
      <p>loading: {loading ? 'true' : 'false'}</p>
      <p>error: {error || 'null'}</p>
      <p>currentUser?.role: {currentUser?.role || 'null'}</p>
      <p>isHQ: {isHQ ? 'true' : 'false'}</p>
      <p>selectedStore: {selectedStore ? selectedStore.name : 'null'}</p>
      <p>coreStats: {coreStats ? `有数据(${coreStats.total_reviews})` : 'null'}</p>
      <p>platformData: {platformData.length}条</p>
      <p>recentReviews: {recentReviews.length}条</p>
      <p>hasNoData: {(!coreStats || !coreStats.total_reviews || (recentReviews.length === 0 && platformData.length === 0)) ? 'true' : 'false'}</p>
    </div>
  );

  // ===== 加载状态 =====
  if (loading) {
    return (
      <MobileLayout title="数据概览">
        {debugInfo}
        <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500 p-4">
          <Skeleton lines={1} className="h-8 w-48 mb-4" />
          <Card className="p-5">
            <Skeleton lines={1} className="h-8 w-32 mb-4" />
            <Skeleton lines={3} className="space-y-2" />
          </Card>
          <Skeleton card className="mt-4" />
          <Skeleton lines={5} className="mt-4 space-y-3" />
        </div>
      </MobileLayout>
    );
  }

  // ===== 错误状态 =====
  if (error) {
    return (
      <MobileLayout title={isHQ ? "门店动态" : "数据概览"}>
        <div className="p-4">
          <Card className="p-6 text-center">
            <AlertCircle className="w-12 h-12 text-rose-500 mx-auto mb-4" />
            <p className="text-sm text-slate-600 mb-4">{error}</p>
            <Button onClick={() => fetchAllData()} className="bg-orange-500 hover:bg-orange-600 text-white">
              重试
            </Button>
          </Card>
        </div>
      </MobileLayout>
    );
  }

  // ===== 无数据状态 =====
  console.log('[Dashboard] 渲染前检查:', { coreStats, total_reviews: coreStats?.total_reviews, recentReviews: recentReviews.length, platformData: platformData.length, loading });
  const hasNoData = !coreStats || !coreStats.total_reviews || (recentReviews.length === 0 && platformData.length === 0);
  console.log('[Dashboard] hasNoData:', hasNoData);
  if (hasNoData) {
    return (
      <MobileLayout title={isHQ ? "门店动态" : "数据概览"}>
        <div className="flex-1 flex items-center justify-center p-4">
          <div className="text-center">
            <div className="w-16 h-16 rounded-2xl bg-slate-100 flex items-center justify-center mx-auto mb-4">
              <BarChart3 className="w-8 h-8 text-slate-300" />
            </div>
            <p className="text-base font-semibold text-slate-400 mb-2">暂无数据</p>
            <p className="text-sm text-slate-400">当前筛选条件下没有数据</p>
          </div>
        </div>
      </MobileLayout>
    );
  }

  return (
    <MobileLayout title={isHQ ? "门店动态" : "数据概览"}>
      <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500 pb-20">

        {/* Date/Filter Summary */}
        <div className="relative" ref={dropdownRef}>
          <div className="flex items-center justify-between bg-white p-3 rounded-2xl shadow-sm border border-slate-100">
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-slate-400" />
              <span className="text-sm font-medium text-slate-600">{getCurrentDateRange()}</span>
            </div>
            <Button
              variant="ghost"
              size="sm"
              className="h-8 text-orange-600 font-semibold gap-1"
              onClick={handleFilterClick}
            >
              {timeOptions.find(opt => opt.value === timePeriod)?.label} <Filter className="w-3.5 h-3.5" />
            </Button>
          </div>

          {/* Time Period Dropdown */}
          {showTimeDropdown && (
            <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-2xl shadow-lg border border-slate-100 z-50 overflow-hidden animate-in fade-in slide-in-from-top-2 duration-200">
              {timeOptions.map((option) => (
                <button
                  key={option.value}
                  className={cn(
                    "w-full px-4 py-3 text-left text-sm font-medium transition-colors flex items-center justify-between",
                    timePeriod === option.value
                      ? "bg-orange-50 text-orange-600"
                      : "text-slate-700 hover:bg-slate-50"
                  )}
                  onClick={() => handleTimePeriodChange(option.value as any)}
                >
                  <span>{option.label}</span>
                  {option.value !== 'custom' && (
                    <span className="text-[10px] text-slate-400">{option.dateRange}</span>
                  )}
                  {timePeriod === option.value && (
                    <CheckCircle2 className="w-4 h-4 text-orange-600" />
                  )}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* ===== 核心数据融合卡片（含数据源健康度） ===== */}
        <Card className="p-5 bg-white border-slate-100 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-orange-50 flex items-center justify-center">
                <MessageSquare className="w-4 h-4 text-orange-500" />
              </div>
              <span className="text-sm font-bold text-slate-700">核心数据概览</span>
            </div>
            <Badge className="bg-orange-50 text-orange-600 border-orange-200 text-[10px]">
              {timePeriod === '7days' ? '近7天' : timePeriod === '30days' ? '近30天' : '今日'}
            </Badge>
          </div>

          {/* 第一行：评论总数 + 趋势 */}
          <div className="flex items-end justify-between mb-4">
            <div>
              <p className="text-4xl font-black text-slate-900">{coreStats?.total_reviews?.toLocaleString() || '0'}</p>
              <p className="text-xs text-slate-400 mt-1">评论总数</p>
            </div>
            <div className="flex items-center gap-1 bg-emerald-50 px-2 py-1 rounded-full">
              <TrendingUp className="w-3.5 h-3.5 text-emerald-500" />
              <span className="text-xs font-bold text-emerald-600">{coreStats?.review_trend != null ? `+${(coreStats.review_trend as number).toFixed(1)}%` : '0%'}</span>
            </div>
          </div>

          {/* 第二行：三个核心指标紧凑展示 */}
          <div className="grid grid-cols-3 gap-3 mb-4">
            <div className="bg-slate-50 rounded-xl p-3 text-center">
              <Star className="w-4 h-4 fill-amber-400 text-amber-400 mx-auto mb-1" />
              <p className="text-lg font-black text-slate-900">{(coreStats?.avg_rating || 0).toFixed(1)}</p>
              <p className="text-[9px] text-slate-400">平均星级</p>
              <p className="text-[9px] text-emerald-500 mt-0.5">{coreStats?.rating_trend != null ? `+${(coreStats.rating_trend as number).toFixed(1)}` : '+0'}</p>
            </div>
            <div className="bg-slate-50 rounded-xl p-3 text-center">
              <ThumbsUp className="w-4 h-4 text-emerald-500 mx-auto mb-1" />
              <p className="text-lg font-black text-slate-900">{coreStats?.positive_rate != null ? `${(coreStats.positive_rate as number).toFixed(1)}%` : '0%'}</p>
              <p className="text-[9px] text-slate-400">好评率</p>
              <p className="text-[9px] text-emerald-500 mt-0.5">{coreStats?.positive_trend != null ? `+${(coreStats.positive_trend as number).toFixed(1)}%` : '0%'}</p>
            </div>
            <div className="bg-slate-50 rounded-xl p-3 text-center">
              <Bot className="w-4 h-4 text-blue-500 mx-auto mb-1" />
              <p className="text-lg font-black text-slate-900">{coreStats?.ai_reply_rate != null ? `${(coreStats.ai_reply_rate as number).toFixed(1)}%` : '0%'}</p>
              <p className="text-[9px] text-slate-400">AI回复率</p>
              <p className="text-[9px] text-emerald-500 mt-0.5">{coreStats?.reply_trend != null ? `+${(coreStats.reply_trend as number).toFixed(1)}%` : '0%'}</p>
            </div>
          </div>

          {/* 第三行：平台分布 */}
          <div className="mb-3">
            <p className="text-[9px] text-slate-400 mb-2 font-medium flex items-center gap-1">
              <BarChart3 className="w-3 h-3" /> 平台分布
            </p>
            <div className="bg-slate-50 rounded-xl p-3 space-y-2">
              {platformData.map((item, i) => (
                <div key={i} className="flex items-center gap-2">
                  <iconify-icon icon={item.icon} class="text-sm opacity-90 w-5 flex-shrink-0"></iconify-icon>
                  <span className="text-[9px] text-slate-600 w-10 flex-shrink-0">{item.platform === '大众点评' ? '点评' : item.platform === '小红书' ? '小红书' : item.platform}</span>
                  <div className="flex-1 bg-slate-200 rounded-full h-2">
                    <div
                      className={`h-full rounded-full ${item.color}`}
                      style={{ width: `${item.percentage}%` }}
                    ></div>
                  </div>
                  <span className="text-[9px] font-bold text-slate-600 w-10 text-right">{item.count}条</span>
                </div>
              ))}
            </div>
          </div>

          {/* 第四行：数据源健康度 */}
          <div>
            <p className="text-[9px] text-slate-400 mb-2 font-medium flex items-center gap-1">
              <ShieldCheck className="w-3 h-3" /> 数据源状态
            </p>
            <div className="bg-slate-50 rounded-xl p-3">
              <div className="grid grid-cols-4 gap-2">
                {healthStats.map((stat, i) => (
                  <div key={i} className="flex flex-col items-center gap-1">
                    <div className="relative">
                      <iconify-icon
                        icon={stat.platform === '美团' ? 'simple-icons:meituan' :
                               stat.platform === '大众点评' ? 'simple-icons:dianping' :
                               stat.platform === '抖音' ? 'simple-icons:tiktok' : 'simple-icons:xiaohongshu'}
                        class={cn("text-lg",
                          stat.platform === '美团' ? 'text-yellow-500' :
                          stat.platform === '大众点评' ? 'text-orange-500' :
                          stat.platform === '抖音' ? 'text-slate-900' : 'text-red-500'
                        )}
                      ></iconify-icon>
                      <div className={cn(
                        "absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full border-2 border-white",
                        stat.status === 'normal' ? 'bg-emerald-500' : 'bg-amber-500'
                      )}></div>
                    </div>
                    <div className="flex items-center gap-0.5">
                      <div className={cn(
                        "w-1 h-1 rounded-full",
                        stat.status === 'normal' ? 'bg-emerald-500' : 'bg-amber-500'
                      )}></div>
                      <span className="text-[8px] text-slate-400">{stat.time}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </Card>

        {/* Anomaly Warning Section */}
        {alert && (
          <div
            className="px-1 cursor-pointer"
            onClick={handleAlertClick}
          >
            <div className="bg-rose-50 border border-rose-100 rounded-2xl p-4 flex items-center gap-4 relative overflow-hidden hover:bg-rose-100 transition-colors">
              <div className="w-12 h-12 rounded-full bg-rose-100 flex items-center justify-center flex-shrink-0">
                <Flame className="w-6 h-6 text-rose-600 animate-pulse" />
              </div>
              <div className="flex-1 z-10">
                <div className="flex items-center gap-2 mb-1">
                  <h4 className="text-sm font-bold text-rose-900">{alert.title}</h4>
                  <Badge className="bg-rose-500 text-white border-none text-[8px] px-1.5 h-4">紧急</Badge>
                </div>
                <p className="text-xs text-rose-700 leading-tight">
                  {alert.description}
                </p>
              </div>
              <iconify-icon icon="mdi:alert-decagram-outline" class="absolute -right-2 -bottom-2 text-rose-200/50 text-6xl rotate-12"></iconify-icon>
            </div>
          </div>
        )}

        {/* HQ/Operator View: Multi-store leaderboard */}
        {isHQ && (
          <Card className="p-5 border-slate-100 shadow-sm bg-white relative overflow-hidden">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
                <BarChart3 className="w-4 h-4 text-orange-500" />
                管辖门店口碑排行
              </h3>
              <span className="text-[10px] text-slate-400 font-medium italic">基于综合评分</span>
            </div>
            <div className="space-y-4">
              {storeRankings.map((store, i) => (
                <div key={i} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className={cn(
                      "w-5 h-5 rounded flex items-center justify-center text-[10px] font-bold",
                      i === 0 ? "bg-amber-100 text-amber-600" :
                      i === 1 ? "bg-slate-100 text-slate-600" :
                      i === 2 ? "bg-orange-100 text-orange-600" : "bg-slate-100 text-slate-500"
                    )}>{i === 0 ? '👑' : i + 1}</span>
                    <div className="flex flex-col">
                      <span className="text-sm font-medium text-slate-700">{store.name}</span>
                      <span className="text-[10px] text-slate-400">健康值 {store.health_score ?? '-'}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <div className="text-sm font-bold text-slate-900">{store.score}</div>
                      <div className="text-[10px] text-slate-400">{store.reviews} 评论</div>
                    </div>
                    {store.trend === 'up' ? (
                      <TrendingUp className="w-4 h-4 text-emerald-500" />
                    ) : store.trend === 'down' ? (
                      <TrendingDown className="w-4 h-4 text-rose-500" />
                    ) : (
                      <div className="w-4 h-4 rounded-full border-2 border-slate-300"></div>
                    )}
                  </div>
                </div>
              ))}
            </div>
            <Button
              variant="outline"
              className="w-full mt-4 h-10 border-orange-100 text-orange-600 text-xs font-bold rounded-xl bg-orange-50/30"
              onClick={handleViewAllStores}
            >
              查看全部 {currentUser.role === 'HQ' ? '85' : '12'} 家门店
            </Button>
            <iconify-icon icon="mdi:store-outline" class="absolute -right-4 -bottom-4 text-slate-50 text-6xl -rotate-12"></iconify-icon>
          </Card>
        )}

        {/* Merchant View: Store Focus */}
        {!isHQ && storeHealth && (
          <Card className="p-5 border-slate-100 shadow-sm bg-white relative overflow-hidden">
            <div className="relative z-10">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-8 h-8 rounded-lg bg-orange-50 flex items-center justify-center">
                  <ShieldCheck className="w-4 h-4 text-orange-500" />
                </div>
                <p className="text-sm font-bold text-slate-700">口碑健康值</p>
              </div>
              <div className="flex items-baseline gap-2 mt-1">
                <h3 className="text-4xl font-bold text-slate-900 tracking-tight">{storeHealth.health_score}</h3>
                <Badge className={cn(
                  "text-[10px] flex items-center gap-0.5 border",
                  storeHealth.health_score >= 80 ? "bg-emerald-50 text-emerald-600 border-emerald-200" :
                  storeHealth.health_score >= 60 ? "bg-amber-50 text-amber-600 border-amber-200" :
                  "bg-rose-50 text-rose-600 border-rose-200"
                )}>
                  <TrendingUp className="w-3 h-3" />
                  {storeHealth.health_score >= 80 ? '极优' : storeHealth.health_score >= 60 ? '良好' : '需改进'}
                </Badge>
              </div>
              <p className="mt-4 text-slate-500 font-medium text-xs leading-relaxed max-w-[80%]">
                {storeHealth.review_count} 条评论，平均 {storeHealth.avg_rating} 星，回复率 {storeHealth.reply_rate}%
              </p>
            </div>
            <Award className="absolute -right-4 -bottom-4 w-32 h-32 text-orange-50" />
            <ChefHat className="absolute right-4 top-4 w-12 h-12 text-orange-50" />
          </Card>
        )}

        {/* Task List / Alerts */}
        <div className="space-y-3 pb-6">
          <div className="flex items-center justify-between px-1">
            <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
              <Zap className="w-4 h-4 text-orange-500" />
              最新评论动态
            </h3>
            <span className="text-[10px] text-slate-500 font-bold bg-slate-100 px-2 py-0.5 rounded-full">{recentReviews.length} 条评论</span>
          </div>
          {recentReviews.map((review) => (
            <Card
              key={review.id}
              className="p-4 border-slate-100 shadow-sm active:bg-slate-50 transition-colors bg-white relative cursor-pointer hover:shadow-md transition-all"
              onClick={() => handleReviewClick(review.id)}
            >
              <div className="flex justify-between items-start">
                <div className="flex gap-3 flex-1">
                  <div className={cn(
                    "w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold text-white flex-shrink-0",
                    review.rating >= 4 ? "bg-emerald-400" : review.rating >= 3 ? "bg-amber-400" : "bg-rose-400"
                  )}>
                    {review.rating}
                  </div>
                  <div className="flex flex-col flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="text-sm font-bold text-slate-800">{review.user_name}</span>
                      <span className="text-[10px] text-slate-400">{review.time}</span>
                      <Badge className={cn(
                        "text-[9px] px-1.5 h-4 border-none",
                        review.sentiment === 'positive' ? "bg-emerald-100 text-emerald-700" :
                        review.sentiment === 'negative' ? "bg-rose-100 text-rose-700" :
                        "bg-amber-100 text-amber-700"
                      )}>
                        {review.sentiment === 'positive' ? '好评' :
                         review.sentiment === 'negative' ? '差评' : '中评'}
                      </Badge>
                    </div>
                    <p className="text-xs text-slate-500 line-clamp-2 mt-0.5">{review.content}</p>
                    <div className="flex items-center gap-2 mt-2 flex-wrap">
                      <Badge variant="outline" className="text-[9px] border-slate-100 bg-slate-50 text-slate-500 px-1.5 h-4">
                        {review.platform}
                      </Badge>
                      <div className="flex items-center gap-0.5">
                        {[1, 2, 3, 4, 5].map(star => (
                          <Star
                            key={star}
                            className={cn(
                              "w-3 h-3",
                              star <= review.rating ? "text-amber-400 fill-amber-400" : "text-slate-200"
                            )}
                          />
                        ))}
                      </div>
                      {review.rating <= 2 && (
                        <div className="flex items-center gap-1 bg-rose-50 text-rose-600 text-[9px] px-1.5 h-4 rounded-full font-bold">
                          <AlertCircle className="w-3 h-3" />
                          需紧急处理
                        </div>
                      )}
                    </div>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="icon"
                  className="w-8 h-8 rounded-full flex-shrink-0"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleReviewClick(review.id);
                  }}
                >
                  <ChevronRight className="w-4 h-4 text-slate-300" />
                </Button>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </MobileLayout>
  );
};

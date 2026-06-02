import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  TrendingUp,
  Target,
  BarChart3,
  Users,
  ChevronRight,
  ArrowUpRight,
  Lightbulb,
  ThumbsUp,
  ThumbsDown,
  Utensils,
  ClipboardList,
  Award,
  Zap,
  Trash2,
  FileText
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Skeleton } from '../../components/ui/skeleton';
import { MobileLayout, useStore } from '../../components/MobileLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';
import {
  fetchTopDish,
  fetchThreeGoodThreeBad,
  fetchDishElimination,
  fetchServiceCases,
  fetchCompetitorOpportunities,
} from '../../api/insights';
import type { Dish, DishElimination, ServiceCase, CompetitorOpportunity } from '../../api/insights';
import { useSubscription, SubscriptionPrompt } from '../../hooks/use-subscription-check';

export const Insights: React.FC = () => {
  const [reportType, setReportType] = useState<'week' | 'month'>('week');
  const [topDish, setTopDish] = useState<Dish[]>([]);
  const [threeGoodThreeBad, setThreeGoodThreeBad] = useState<{goods: string[], bads: string[]}>({goods: [], bads: []});
  const [dishElimination, setDishElimination] = useState<DishElimination[]>([]);
  const [serviceCases, setServiceCases] = useState<ServiceCase[]>([]);
  const [competitorOpportunities, setCompetitorOpportunities] = useState<CompetitorOpportunity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { success } = useToast();
  const navigate = useNavigate();
  const { selectedStore } = useStore();

  // ===== 订阅状态检测 =====
  const {
    subscription,
    loading: subscriptionLoading,
    error: subscriptionError,
    hasValidSubscription,
  } = useSubscription();

  const loadData = async () => {
    if (!selectedStore?.id) {
      setLoading(false);
      return;
    }
    try {
      setLoading(true);
      setError(null);
      const period = reportType === 'week' ? '7d' : '30d';
      const [dishData, threeData, eliminationData, casesData, opportunityData] = await Promise.all([
        fetchTopDish(period, selectedStore.id),
        fetchThreeGoodThreeBad(period, selectedStore.id),
        fetchDishElimination(selectedStore.id),
        fetchServiceCases(undefined, selectedStore.id),
        fetchCompetitorOpportunities(selectedStore.id),
      ]);
      setTopDish(dishData);
      setThreeGoodThreeBad(threeData);
      setDishElimination(eliminationData);
      setServiceCases(casesData);
      setCompetitorOpportunities(opportunityData);
    } catch (err) {
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (subscriptionLoading) return;
    loadData();
  }, [selectedStore?.id, reportType, subscriptionLoading]);

  const handleViewDetail = () => {
    navigate('/mobile/traceability-detail/RPT-2025-001');
  };

  const handleDishClick = (dishName: string) => {
    success('菜品详情', `正在查看"${dishName}"的详细口碑数据...`);
  };

  const handleEliminationClick = () => {
    navigate('/mobile/dish-elimination');
  };

  // ===== 条件渲染 =====
  // 1. 订阅加载中
  if (subscriptionLoading) {
    return (
      <MobileLayout title="经营洞察">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-sm text-slate-400">正在检查订阅状态...</p>
          </div>
        </div>
      </MobileLayout>
    );
  }

  // 2. 无有效订阅
  if (!hasValidSubscription) {
    return (
      <MobileLayout title="经营洞察">
        <SubscriptionPrompt featureName="经营洞察" />
      </MobileLayout>
    );
  }

  // 3. 数据加载中
  if (loading) {
    return (
      <MobileLayout title="经营洞察">
        <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500 p-4">
          <Skeleton className="h-8 w-48 mb-4" />
          <Card className="p-5">
            <Skeleton className="h-8 w-32 mb-4" />
            <Skeleton className="space-y-2" />
          </Card>
          <Skeleton card className="mt-4" />
          <Skeleton className="mt-4 space-y-3" />
        </div>
      </MobileLayout>
    );
  }

  // 4. 加载错误
  if (error) {
    return (
      <MobileLayout title="经营洞察">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <p className="text-sm text-rose-500 mb-4">{error}</p>
            <button onClick={loadData} className="text-sm text-orange-600 font-bold">重试</button>
          </div>
        </div>
      </MobileLayout>
    );
  }

  // 5. 店铺加载中
  if (!selectedStore) {
    return (
      <MobileLayout title="经营洞察">
        <div className="flex-1 flex items-center justify-center p-4">
          <div className="text-center">
            <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-sm text-slate-400">正在加载店铺数据...</p>
          </div>
        </div>
      </MobileLayout>
    );
  }

  // 统计服务案例数量
  const praiseCount = serviceCases.filter(c => c.type === 'praise').length;
  const complaintCount = serviceCases.filter(c => c.type === 'complaint').length;

  return (
    <MobileLayout title="经营洞察">
      <div className="space-y-6 pb-20 animate-in fade-in slide-in-from-bottom-4 duration-500">

        {/* 竞对分析入口 - 移到最顶部 */}
        <Card
          className="p-5 bg-white border-slate-100 shadow-sm cursor-pointer hover:shadow-md transition-all duration-300"
          onClick={() => navigate('/mobile/competitor-analysis')}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-2xl bg-orange-50 flex items-center justify-center">
                <Target className="w-6 h-6 text-orange-500" />
              </div>
              <div>
                <h4 className="font-bold text-lg text-slate-900">竞对分析</h4>
                <p className="text-sm text-slate-400">付费采集分析竞对数据</p>
              </div>
            </div>
            <ChevronRight className="w-6 h-6 text-slate-300" />
          </div>
        </Card>

        {/* "Three Goods and Three Bads" Report */}
        <div className="space-y-3">
          <h3 className="font-bold text-slate-800 text-sm px-1 flex justify-between items-center">
            "三好三差"智能月报
            <div className="flex bg-slate-100 p-0.5 rounded-lg">
              <button
                onClick={() => setReportType('week')}
                className={cn("px-2 py-1 text-[9px] font-bold rounded-md transition-all", reportType === 'week' ? "bg-white text-orange-600 shadow-sm" : "text-slate-400")}
              >周</button>
              <button
                onClick={() => setReportType('month')}
                className={cn("px-2 py-1 text-[9px] font-bold rounded-md transition-all", reportType === 'month' ? "bg-white text-orange-600 shadow-sm" : "text-slate-400")}
              >月</button>
            </div>
          </h3>
          <Card className="p-5 border-none shadow-sm bg-white space-y-4">
            {threeGoodThreeBad.goods.length === 0 && threeGoodThreeBad.bads.length === 0 ? (
              <div className="text-center py-6">
                <BarChart3 className="w-10 h-10 text-slate-300 mx-auto mb-2" />
                <p className="text-sm text-slate-500">暂无分析数据</p>
                <p className="text-xs text-slate-400 mt-1">采集评论后将自动生成月报</p>
              </div>
            ) : (
              <>
                <div className="space-y-3">
                  <p className="text-[10px] font-bold text-emerald-600 flex items-center gap-1"><ThumbsUp className="w-3 h-3" /> 表现优异 (三好)</p>
                  <div className="flex flex-wrap gap-2">
                    {threeGoodThreeBad.goods.length > 0 ? threeGoodThreeBad.goods.map((item, i) => (
                      <Badge key={i} className="bg-emerald-50 text-emerald-600 border-none font-medium text-[10px]">{item}</Badge>
                    )) : (
                      <span className="text-xs text-slate-400">暂无好评亮点</span>
                    )}
                  </div>
                </div>
                <div className="space-y-3 pt-4 border-t border-slate-50">
                  <p className="text-[10px] font-bold text-rose-500 flex items-center gap-1"><ThumbsDown className="w-3 h-3" /> 急需改进 (三差)</p>
                  <div className="flex flex-wrap gap-2">
                    {threeGoodThreeBad.bads.length > 0 ? threeGoodThreeBad.bads.map((item, i) => (
                      <Badge key={i} className="bg-rose-50 text-rose-600 border-none font-medium text-[10px]">{item}</Badge>
                    )) : (
                      <span className="text-xs text-slate-400">暂无差评要点</span>
                    )}
                  </div>
                </div>
                <Button
                  variant="ghost"
                  className="w-full h-8 text-orange-600 text-[10px] font-bold bg-orange-50/50 rounded-lg"
                  onClick={handleViewDetail}
                >
                  查看溯源详情（从报告下钻到评价）
                </Button>
              </>
            )}
          </Card>
        </div>

        {/* Dish Reputation Ranking */}
        <div className="space-y-3">
          <h3 className="font-bold text-slate-800 text-sm px-1 flex items-center gap-2">
            <Utensils className="w-4 h-4 text-orange-500" /> 菜品口碑排行榜
          </h3>
          {topDish.length === 0 ? (
            <Card className="p-8 text-center">
              <Utensils className="w-10 h-10 text-slate-300 mx-auto mb-2" />
              <p className="text-sm text-slate-500">暂无菜品数据</p>
              <p className="text-xs text-slate-400 mt-1">采集评论后将自动分析菜品口碑</p>
            </Card>
          ) : (
            <div className="space-y-2">
              {topDish.map((dish, i) => (
                <Card
                  key={i}
                  className="p-4 border-none shadow-sm flex items-center justify-between bg-white cursor-pointer hover:shadow-md transition-all"
                  onClick={() => handleDishClick(dish.name)}
                >
                  <div className="flex items-center gap-3">
                    <div className={cn(
                      "w-8 h-8 rounded-lg flex items-center justify-center font-bold text-xs",
                      dish.type === 'recommended' ? "bg-emerald-50 text-emerald-600" :
                      dish.type === 'potential' ? "bg-orange-50 text-orange-600" : "bg-rose-50 text-rose-600"
                    )}>
                      {dish.type === 'recommended' ? '荐' : dish.type === 'potential' ? '潜' : '问'}
                    </div>
                    <div>
                      <h4 className="text-sm font-bold text-slate-800">{dish.name}</h4>
                      <div className="flex items-center gap-2 text-[10px] text-slate-400">
                        <span>好评 {dish.positive}</span>
                        <span className="w-1 h-1 bg-slate-200 rounded-full"></span>
                        <span>差评 {dish.negative}</span>
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-black text-slate-900">{dish.score}</div>
                    <div className="text-[8px] text-slate-400">星级评分</div>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>

        {/* Last-place Elimination Advice */}
        {dishElimination.length > 0 ? (
          <Card
            className="p-5 border-none shadow-sm bg-slate-900 text-white relative overflow-hidden cursor-pointer hover:shadow-lg transition-all"
            onClick={handleEliminationClick}
          >
            <Trash2 className="absolute -right-2 -bottom-2 w-20 h-20 text-white/5" />
            <div className="relative z-10 space-y-4">
              <div className="flex items-center gap-2">
                <Zap className="w-4 h-4 text-amber-400" />
                <h4 className="text-sm font-bold">"末位淘汰"建议</h4>
              </div>
              {dishElimination.slice(0, 2).map((item, i) => (
                <div key={i} className="space-y-2">
                  <p className="text-[11px] text-slate-300 leading-relaxed">
                    基于近 30 天评价，菜品 <span className="text-amber-400 font-bold underline">"{item.name}"</span> {item.reason}
                  </p>
                  <div className="bg-white/5 p-3 rounded-xl border border-white/10 space-y-2">
                    <p className="text-[10px] text-slate-400">建议：{item.suggestion}</p>
                  </div>
                </div>
              ))}
              <Button
                className="w-full bg-amber-500 hover:bg-amber-600 text-white h-8 text-[10px] font-bold border-none"
                onClick={(e) => {
                  e.stopPropagation();
                  navigate('/mobile/dish-elimination');
                }}
              >
                查看详细改进方案
              </Button>
            </div>
          </Card>
        ) : (
          <Card className="p-5 border-none shadow-sm bg-slate-900 text-white relative overflow-hidden">
            <Trash2 className="absolute -right-2 -bottom-2 w-20 h-20 text-white/5" />
            <div className="relative z-10 flex items-center gap-3">
              <Zap className="w-4 h-4 text-amber-400" />
              <div>
                <h4 className="text-sm font-bold">"末位淘汰"建议</h4>
                <p className="text-[11px] text-slate-400 mt-1">暂无需要改进的菜品，整体表现良好</p>
              </div>
            </div>
          </Card>
        )}

        {/* Service Standard & Case Library */}
        <div className="space-y-3">
          <h3 className="font-bold text-slate-800 text-sm px-1">服务标准数字化沉淀</h3>
          <div className="grid grid-cols-2 gap-3">
            <Card className="p-4 border-none shadow-sm bg-white space-y-3 flex flex-col items-center text-center">
              <div className="w-10 h-10 bg-emerald-50 rounded-xl flex items-center justify-center text-emerald-600">
                <Award className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-[11px] font-bold text-slate-800">金牌服务案例库</h4>
                <p className="text-[9px] text-slate-400 mt-1">
                  {praiseCount > 0 ? `已沉淀 ${praiseCount} 条优秀案例` : '暂无优秀案例'}
                </p>
              </div>
              <Button
                variant="outline"
                className="w-full h-8 text-[9px] font-bold border-slate-100"
                onClick={() => success('查看案例', '正在加载金牌服务案例库...')}
                disabled={praiseCount === 0}
              >
                查看
              </Button>
            </Card>
            <Card className="p-4 border-none shadow-sm bg-white space-y-3 flex flex-col items-center text-center">
              <div className="w-10 h-10 bg-rose-50 rounded-xl flex items-center justify-center text-rose-500">
                <ClipboardList className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-[11px] font-bold text-slate-800">反面教材修正工单</h4>
                <p className="text-[9px] text-slate-400 mt-1">
                  {complaintCount > 0 ? `${complaintCount} 条工单正在整改中` : '暂无待处理工单'}
                </p>
              </div>
              <Button
                variant="outline"
                className="w-full h-8 text-[9px] font-bold border-slate-100"
                onClick={() => success('处理工单', '正在加载反面教材修正工单...')}
                disabled={complaintCount === 0}
              >
                去处理
              </Button>
            </Card>
          </div>
        </div>

        {/* 同行机会洞察 */}
        <div className="space-y-3">
          <h3 className="font-bold text-slate-800 text-sm px-1">同行机会洞察</h3>
          {competitorOpportunities.length === 0 ? (
            <Card className="p-5 border-none shadow-sm bg-white text-center">
              <Lightbulb className="w-8 h-8 text-slate-300 mx-auto mb-2" />
              <p className="text-sm text-slate-500">暂无竞品分析数据</p>
              <p className="text-xs text-slate-400 mt-1">采集更多评论后将自动生成机会洞察</p>
            </Card>
          ) : (
            competitorOpportunities.map((opp, i) => (
              <Card key={i} className="p-5 border-none shadow-sm bg-white space-y-3">
                <div className="flex items-center gap-2">
                  <Lightbulb className="w-4 h-4 text-orange-500" />
                  <p className="text-xs font-bold text-slate-700">{opp.title}</p>
                </div>
                <p className="text-[11px] text-slate-500 leading-relaxed">{opp.description}</p>
                <Button
                  variant="outline"
                  className="w-full h-8 text-[10px] font-bold border-orange-200 text-orange-600 hover:bg-orange-50"
                >
                  {opp.action}
                </Button>
              </Card>
            ))
          )}
        </div>
      </div>
    </MobileLayout>
  );
};

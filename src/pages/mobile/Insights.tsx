import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  TrendingUp, 
  Target, 
  BarChart3, 
  PieChart, 
  Users, 
  MapPin,
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
import { fetchTopDish, fetchThreeGoodThreeBad } from '../../api/insights';
import type { Dish } from '../../api/insights';

export const Insights: React.FC = () => {
  const [reportType, setReportType] = useState<'week' | 'month'>('week');
  const [topDish, setTopDish] = useState<Dish[]>([]);
  const [threeGoodThreeBad, setThreeGoodThreeBad] = useState<{goods: string[], bads: string[]}>({goods: [], bads: []});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const fetchedRef = React.useRef(false);

  const { success } = useToast();
  const navigate = useNavigate();
  const { selectedStore } = useStore();

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const storeId = selectedStore?.id;
      const [dishData, threeData] = await Promise.all([
        fetchTopDish(undefined, storeId),
        fetchThreeGoodThreeBad(undefined, storeId),
      ]);
      setTopDish(dishData);
      setThreeGoodThreeBad(threeData);
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

  const handleViewDetail = () => {
    navigate('/mobile/traceability-detail/RPT-2025-001');
  };

  const handleDishClick = (dishName: string) => {
    success('菜品详情', `正在查看"${dishName}"的详细口碑数据...`);
  };

  const handleEliminationClick = () => {
    navigate('/mobile/dish-elimination');
  };

  const handleExportReport = () => {
    success('导出报告', '正在导出完整洞察报告为 PDF...');
  };

  if (loading) {
    return (
      <MobileLayout title="经营洞察">
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

  // ===== 无店铺状态 =====
  if (!loading && !selectedStore) {
    return (
      <MobileLayout title="经营洞察">
        <div className="flex-1 flex items-center justify-center p-4">
          <div className="text-center">
            <div className="w-16 h-16 rounded-2xl bg-slate-100 flex items-center justify-center mx-auto mb-4">
              <TrendingUp className="w-8 h-8 text-slate-300" />
            </div>
            <p className="text-base font-semibold text-slate-400 mb-2">暂无数据</p>
            <p className="text-sm text-slate-400">请通过顶部导航切换店铺</p>
          </div>
        </div>
      </MobileLayout>
    );
  }

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
            “三好三差”智能月报
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
            <div className="space-y-3">
              <p className="text-[10px] font-bold text-emerald-600 flex items-center gap-1"><ThumbsUp className="w-3 h-3" /> 表现优异 (三好)</p>
              <div className="flex flex-wrap gap-2">
                {threeGoodThreeBad.goods.map((item, i) => (
                  <Badge key={i} className="bg-emerald-50 text-emerald-600 border-none font-medium text-[10px]">{item}</Badge>
                ))}
              </div>
            </div>
            <div className="space-y-3 pt-4 border-t border-slate-50">
              <p className="text-[10px] font-bold text-rose-500 flex items-center gap-1"><ThumbsDown className="w-3 h-3" /> 急需改进 (三差)</p>
              <div className="flex flex-wrap gap-2">
                {threeGoodThreeBad.bads.map((item, i) => (
                  <Badge key={i} className="bg-rose-50 text-rose-600 border-none font-medium text-[10px]">{item}</Badge>
                ))}
              </div>
            </div>
            <Button 
              variant="ghost" 
              className="w-full h-8 text-orange-600 text-[10px] font-bold bg-orange-50/50 rounded-lg"
              onClick={handleViewDetail}
            >
              查看溯源详情（从报告下钻到评价）
            </Button>
          </Card>
        </div>

        {/* Dish Reputation Ranking */}
        <div className="space-y-3">
          <h3 className="font-bold text-slate-800 text-sm px-1 flex items-center gap-2">
            <Utensils className="w-4 h-4 text-orange-500" /> 菜品口碑排行榜
          </h3>
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
        </div>

        {/* Last-place Elimination Advice */}
        <Card 
          className="p-5 border-none shadow-sm bg-slate-900 text-white relative overflow-hidden cursor-pointer hover:shadow-lg transition-all"
          onClick={handleEliminationClick}
        >
          <Trash2 className="absolute -right-2 -bottom-2 w-20 h-20 text-white/5" />
          <div className="relative z-10 space-y-4">
            <div className="flex items-center gap-2">
              <Zap className="w-4 h-4 text-amber-400" />
              <h4 className="text-sm font-bold">"末位淘汰”建议</h4>
            </div>
            <p className="text-[11px] text-slate-300 leading-relaxed">
              基于近 30 天评价，菜品 <span className="text-amber-400 font-bold underline">"麻辣烫"</span> 差评率持续高于 20%，且近期销量表现一般。
            </p>
            <div className="bg-white/5 p-3 rounded-xl border border-white/10 space-y-2">
              <p className="text-[10px] text-slate-400">主要问题：口感过咸、食材种类单一</p>
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
          </div>
        </Card>

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
                <p className="text-[9px] text-slate-400 mt-1">已沉淀 42 条优秀案例</p>
              </div>
              <Button 
                variant="outline" 
                className="w-full h-8 text-[9px] font-bold border-slate-100"
                onClick={() => success('查看案例', '正在加载金牌服务案例库...')}
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
                <p className="text-[9px] text-slate-400 mt-1">3 条工单正在整改中</p>
              </div>
              <Button 
                variant="outline" 
                className="w-full h-8 text-[9px] font-bold border-slate-100"
                onClick={() => success('处理工单', '正在加载反面教材修正工单...')}
              >
                去处理
              </Button>
            </Card>
          </div>
        </div>

        {/* 同行机会洞察 */}
        <div className="space-y-3">
          <h3 className="font-bold text-slate-800 text-sm px-1">同行机会洞察</h3>
          <Card className="p-5 border-none shadow-sm bg-white space-y-3">
            <div className="flex items-center gap-2">
              <Lightbulb className="w-4 h-4 text-orange-500" />
              <p className="text-xs font-bold text-slate-700">商圈竞品对比</p>
            </div>
            <p className="text-[11px] text-slate-500 leading-relaxed">
              您的竞品 A 近期“上菜慢”的差评增多，建议您本店主推“30分钟未上齐免单”服务。
            </p>
            <div className="pt-2">
               <div className="flex justify-between text-[10px] mb-1">
                 <span className="text-slate-400">本店好评率</span>
                 <span className="font-bold text-orange-600">94.2%</span>
               </div>
               <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                 <div className="bg-orange-500 h-full w-[94%]"></div>
               </div>
            </div>
          </Card>
        </div>
      </div>
    </MobileLayout>
  );
};


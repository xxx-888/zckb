import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, 
  Trash2, 
  Utensils, 
  TrendingDown, 
  AlertTriangle, 
  BarChart3, 
  Lightbulb, 
  CheckCircle2,
  ChefHat,
  Clock,
  ThumbsDown,
  ThumbsUp
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { useToast } from '../../hooks/use-toast';
import { MobileLayout } from '../../components/MobileLayout';

interface DishData {
  id: number;
  name: string;
  type: string;
  score: number;
  positive: number;
  negative: number;
  negativeRate: number;
  salesTrend: 'up' | 'down' | 'stable';
  avgRating: number;
  recentReviews: number;
  mainProblems: string[];
  suggestion: string;
  actionPlan: string[];
}

export const DishElimination: React.FC = () => {
  const navigate = useNavigate();
  const { success } = useToast();
  
  const [dishData, setDishData] = useState<DishData[]>([
    {
      id: 1,
      name: '麻辣烫',
      type: '淘汰预警',
      score: 3.2,
      positive: 20,
      negative: 15,
      negativeRate: 42.9,
      salesTrend: 'down',
      avgRating: 2.8,
      recentReviews: 8,
      mainProblems: ['口感过咸', '食材种类单一', '分量减少'],
      suggestion: '建议立即优化配方或考虑下架',
      actionPlan: [
        '召集厨师长会议，优化麻辣烫底料配方',
        '增加食材种类至15种以上',
        '调整分量标准，确保性价比',
        '7天后复查评价数据'
      ]
    },
    {
      id: 2,
      name: '酸辣粉',
      type: '观察期',
      score: 3.8,
      positive: 45,
      negative: 12,
      negativeRate: 21.1,
      salesTrend: 'stable',
      avgRating: 3.5,
      recentReviews: 5,
      mainProblems: ['酸度不稳定', '粉质偏软'],
      suggestion: '建议微调配方，继续观察',
      actionPlan: [
        '统一酸辣粉调料包标准',
        '更换粉条供应商，提升口感',
        '14天后复查评价数据'
      ]
    },
    {
      id: 3,
      name: '凉拌黄瓜',
      type: '改进中',
      score: 4.0,
      positive: 38,
      negative: 8,
      negativeRate: 17.4,
      salesTrend: 'up',
      avgRating: 3.9,
      recentReviews: 3,
      mainProblems: ['口味偏淡'],
      suggestion: '已改进，继续观察销量变化',
      actionPlan: [
        '增加调味选项（辣度/酸度可选）',
        '在菜单上标注"可定制口味"',
        '30天后评估是否需要下架'
      ]
    }
  ]);

  const [selectedDish, setSelectedDish] = useState<DishData | null>(null);
  const [showActionModal, setShowActionModal] = useState(false);

  const handleViewDetail = (dish: DishData) => {
    setSelectedDish(dish);
  };

  const handleGeneratePlan = (dish: DishData) => {
    setSelectedDish(dish);
    setShowActionModal(true);
  };

  const handleExecuteAction = (action: string) => {
    success('执行成功', `已开始执行：${action}`);
    setShowActionModal(false);
  };

  const handleExportReport = () => {
    success('导出报告', '正在生成本月"末位淘汰"分析报告...');
  };

  return (
    <MobileLayout title="末位淘汰分析">
      <div className="space-y-6 pb-20 animate-in fade-in slide-in-from-bottom-4 duration-500">
        
        {/* Summary Card */}
        <Card className="p-5 border-slate-100 shadow-sm bg-white">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-xl bg-rose-50 flex items-center justify-center">
                <Trash2 className="w-6 h-6 text-rose-500" />
              </div>
              <div>
                <h3 className="font-bold text-lg text-slate-900">末位淘汰分析</h3>
                <p className="text-xs text-slate-400">基于近30天评价数据</p>
              </div>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-3 text-center">
            <div className="bg-slate-50 rounded-xl p-3">
              <p className="text-2xl font-black text-slate-900">{dishData.length}</p>
              <p className="text-[10px] text-slate-400">待改进菜品</p>
            </div>
            <div className="bg-rose-50 rounded-xl p-3">
              <p className="text-2xl font-black text-rose-600">
                {dishData.filter(d => d.type === '淘汰预警').length}
              </p>
              <p className="text-[10px] text-rose-500">淘汰预警</p>
            </div>
            <div className="bg-amber-50 rounded-xl p-3">
              <p className="text-2xl font-black text-amber-600">
                {dishData.filter(d => d.type === '改进中').length}
              </p>
              <p className="text-[10px] text-amber-500">改进中</p>
            </div>
          </div>
        </Card>

        {/* Elimination List */}
        <div className="space-y-3">
          <h3 className="font-bold text-slate-800 text-sm px-1 flex items-center justify-between">
            <span className="flex items-center gap-2">
              <TrendingDown className="w-4 h-4 text-rose-500" />
              差评率TOP3菜品
            </span>
            <Button 
              variant="ghost" 
              size="sm"
              onClick={handleExportReport}
              className="text-[10px] text-indigo-600 font-bold h-6"
            >
              导出报告
            </Button>
          </h3>

          {dishData.map((dish, idx) => (
            <Card 
              key={dish.id}
              className="p-4 border-none shadow-sm bg-white space-y-3 cursor-pointer hover:shadow-md transition-all"
              onClick={() => handleViewDetail(dish)}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className={`
                    w-10 h-10 rounded-xl flex items-center justify-center font-bold text-white text-sm
                    ${idx === 0 ? 'bg-rose-500' : idx === 1 ? 'bg-orange-500' : 'bg-amber-500'}
                  `}>
                    {idx + 1}
                  </div>
                  <div>
                    <h4 className="font-bold text-slate-900">{dish.name}</h4>
                    <div className="flex items-center gap-2 mt-1">
                      <Badge className={`
                        text-[9px] font-bold border-none
                        ${dish.type === '淘汰预警' ? 'bg-rose-50 text-rose-600' : 
                          dish.type === '观察期' ? 'bg-amber-50 text-amber-600' : 
                          'bg-blue-50 text-blue-600'}
                      `}>
                        {dish.type}
                      </Badge>
                      <span className="text-[10px] text-slate-400">
                        差评率 {dish.negativeRate}%
                      </span>
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="flex items-center gap-1">
                    <span className="text-lg font-black text-rose-600">{dish.score}</span>
                    <span className="text-[10px] text-slate-400">分</span>
                  </div>
                  <div className="flex items-center gap-2 text-[9px] text-slate-400">
                    <span className="flex items-center gap-0.5">
                      <ThumbsUp className="w-3 h-3 text-emerald-500" />
                      {dish.positive}
                    </span>
                    <span className="flex items-center gap-0.5">
                      <ThumbsDown className="w-3 h-3 text-rose-500" />
                      {dish.negative}
                    </span>
                  </div>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="space-y-1">
                <div className="flex justify-between text-[9px]">
                  <span className="text-slate-400">差评率</span>
                  <span className={`font-bold ${dish.negativeRate > 30 ? 'text-rose-600' : dish.negativeRate > 20 ? 'text-amber-600' : 'text-emerald-600'}`}>
                    {dish.negativeRate}%
                  </span>
                </div>
                <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                  <div 
                    className={`h-full rounded-full ${dish.negativeRate > 30 ? 'bg-rose-500' : dish.negativeRate > 20 ? 'bg-amber-500' : 'bg-emerald-500'}`}
                    style={{ width: `${dish.negativeRate}%` }}
                  />
                </div>
              </div>

              {/* Action Button */}
              {dish.type === '淘汰预警' && (
                <Button 
                  onClick={(e) => {
                    e.stopPropagation();
                    handleGeneratePlan(dish);
                  }}
                  className="w-full bg-rose-500 hover:bg-rose-600 text-white h-8 text-[10px] font-bold rounded-xl"
                >
                  <Lightbulb className="w-3 h-3 mr-1" />
                  生成改进方案
                </Button>
              )}

              {dish.type === '观察期' && (
                <Button 
                  onClick={(e) => {
                    e.stopPropagation();
                    success('继续观察', `"${dish.name}"已加入观察列表`);
                  }}
                  variant="outline"
                  className="w-full h-8 text-[10px] font-bold rounded-xl border-amber-200 text-amber-600"
                >
                  <Clock className="w-3 h-3 mr-1" />
                  继续观察
                </Button>
              )}

              {dish.type === '改进中' && (
                <Button 
                  onClick={(e) => {
                    e.stopPropagation();
                    success('查看进度', `"${dish.name}"改进计划执行中`);
                  }}
                  variant="outline"
                  className="w-full h-8 text-[10px] font-bold rounded-xl border-blue-200 text-blue-600"
                >
                  <CheckCircle2 className="w-3 h-3 mr-1" />
                  查看改进进度
                </Button>
              )}
            </Card>
          ))}
        </div>

        {/* Dish Detail Modal */}
        {selectedDish && !showActionModal && (
          <div className="fixed inset-0 bg-black/50 flex items-end justify-center z-50" onClick={() => setSelectedDish(null)}>
            <div 
              className="bg-white rounded-t-3xl w-full max-w-lg p-6 space-y-4 animate-in slide-in-from-bottom duration-300 max-h-[80vh] overflow-y-auto"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-bold text-slate-900">{selectedDish.name} - 详细分析</h2>
                <button 
                  onClick={() => setSelectedDish(null)}
                  className="text-slate-400 hover:text-slate-600"
                >
                  ✕
                </button>
              </div>

              {/* Basic Info */}
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-50 rounded-xl p-3">
                  <p className="text-[10px] text-slate-400 mb-1">综合评分</p>
                  <p className="text-2xl font-black text-slate-900">{selectedDish.score}</p>
                </div>
                <div className="bg-slate-50 rounded-xl p-3">
                  <p className="text-[10px] text-slate-400 mb-1">差评率</p>
                  <p className={`text-2xl font-black ${selectedDish.negativeRate > 30 ? 'text-rose-600' : 'text-amber-600'}`}>
                    {selectedDish.negativeRate}%
                  </p>
                </div>
                <div className="bg-slate-50 rounded-xl p-3">
                  <p className="text-[10px] text-slate-400 mb-1">好评数</p>
                  <p className="text-2xl font-black text-emerald-600">{selectedDish.positive}</p>
                </div>
                <div className="bg-slate-50 rounded-xl p-3">
                  <p className="text-[10px] text-slate-400 mb-1">差评数</p>
                  <p className="text-2xl font-black text-rose-600">{selectedDish.negative}</p>
                </div>
              </div>

              {/* Main Problems */}
              <div className="space-y-2">
                <h4 className="text-xs font-bold text-slate-700 flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-rose-500" />
                  主要问题
                </h4>
                {selectedDish.mainProblems.map((problem, idx) => (
                  <div key={idx} className="flex items-center gap-2 bg-rose-50 p-3 rounded-xl">
                    <ThumbsDown className="w-4 h-4 text-rose-500 flex-shrink-0" />
                    <span className="text-sm text-rose-700">{problem}</span>
                  </div>
                ))}
              </div>

              {/* AI Suggestion */}
              <div className="bg-amber-50 rounded-xl p-4 space-y-2">
                <h4 className="text-xs font-bold text-amber-700 flex items-center gap-2">
                  <Lightbulb className="w-4 h-4" />
                  AI 建议
                </h4>
                <p className="text-sm text-amber-600">{selectedDish.suggestion}</p>
              </div>

              {/* Action Button */}
              {selectedDish.type === '淘汰预警' && (
                <Button 
                  onClick={() => setShowActionModal(true)}
                  className="w-full bg-rose-500 hover:bg-rose-600 text-white rounded-2xl py-6 text-sm font-bold"
                >
                  生成详细改进方案
                </Button>
              )}
            </div>
          </div>
        )}

        {/* Action Plan Modal */}
        {showActionModal && selectedDish && (
          <div className="fixed inset-0 bg-black/50 flex items-end justify-center z-50" onClick={() => setShowActionModal(false)}>
            <div 
              className="bg-white rounded-t-3xl w-full max-w-lg p-6 space-y-4 animate-in slide-in-from-bottom duration-300"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-bold text-slate-900">{selectedDish.name} - 改进方案</h2>
                <button 
                  onClick={() => setShowActionModal(false)}
                  className="text-slate-400 hover:text-slate-600"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-3">
                {selectedDish.actionPlan.map((action, idx) => (
                  <div key={idx} className="flex items-start gap-3 bg-slate-50 p-4 rounded-xl">
                    <div className="w-6 h-6 bg-indigo-100 text-indigo-600 rounded-lg flex items-center justify-center text-xs font-bold flex-shrink-0">
                      {idx + 1}
                    </div>
                    <div className="flex-1">
                      <p className="text-sm text-slate-700">{action}</p>
                    </div>
                    <button
                      onClick={() => handleExecuteAction(action)}
                      className="px-3 py-1 bg-indigo-50 text-indigo-600 rounded-lg text-xs font-bold hover:bg-indigo-100 transition-colors"
                    >
                      执行
                    </button>
                  </div>
                ))}
              </div>

              <Button 
                onClick={() => {
                  success('方案已保存', '改进方案已下发至后厨执行');
                  setShowActionModal(false);
                  setSelectedDish(null);
                }}
                className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-6 text-sm font-bold"
              >
                <CheckCircle2 className="w-4 h-4 mr-2" />
                确认并执行改进方案
              </Button>
            </div>
          </div>
        )}

        {/* Industry Benchmark */}
        <div className="space-y-3">
          <h3 className="font-bold text-slate-800 text-sm px-1 flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-indigo-500" />
            行业基准对比
          </h3>
          <Card className="p-5 border-none shadow-sm bg-white space-y-4">
            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-600">本店平均差评率</span>
                  <span className="font-bold text-rose-600">24.8%</span>
                </div>
                <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                  <div className="bg-rose-500 h-full rounded-full" style={{ width: '24.8%' }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-600">商圈平均差评率</span>
                  <span className="font-bold text-amber-600">18.5%</span>
                </div>
                <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                  <div className="bg-amber-500 h-full rounded-full" style={{ width: '18.5%' }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-600">行业标杆差评率</span>
                  <span className="font-bold text-emerald-600">8.2%</span>
                </div>
                <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                  <div className="bg-emerald-500 h-full rounded-full" style={{ width: '8.2%' }} />
                </div>
              </div>
            </div>
            <div className="bg-rose-50 p-3 rounded-xl">
              <p className="text-xs text-rose-600">
                <AlertTriangle className="w-3 h-3 inline mr-1" />
                您的差评率高于商圈平均 6.3%，建议重点关注差评率TOP3菜品
              </p>
            </div>
          </Card>
        </div>
      </div>
    </MobileLayout>
  );
};

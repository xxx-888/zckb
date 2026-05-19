import React, { useState } from 'react';
import { Card } from '../../../components/ui/card';
import { Button } from '../../../components/ui/button';
import { Badge } from '../../../components/ui/badge';
import { 
  BarChart3, 
  ThumbsUp, 
  ThumbsDown, 
  Lightbulb, 
  ArrowRight,
  PieChart,
  MessageSquare,
  TrendingUp,
  CheckCircle,
  RefreshCw,
  Download,
  Eye,
  Trash2
} from 'lucide-react';
import { cn } from '../../../lib/utils';
import { useToast } from '../../../hooks/use-toast';

interface EvaluationItem {
  id: number;
  comment: string;
  rating: number;
  tag: string;
  date: string;
  addedToTraining?: boolean;
}

interface Insight {
  id: number;
  type: 'suggestion' | 'template';
  title: string;
  description: string;
  improvement: string;
  estimatedImprovement: string;
  status: 'pending' | 'applied' | 'dismissed';
}

export const Evaluation: React.FC = () => {
  const [evaluations, setEvaluations] = useState<EvaluationItem[]>([
    { id: 1, comment: "回复语气过于生硬", rating: 2, tag: "人格设定", date: "2026-05-08" },
    { id: 2, comment: "内容太长了，看着累", rating: 3, tag: "长度控制", date: "2026-05-08" },
    { id: 3, comment: "没有提到具体的改进建议", rating: 1, tag: "逻辑生成", date: "2026-05-07" },
  ]);

  const [insights, setInsights] = useState<Insight[]>([
    {
      id: 1,
      type: 'suggestion',
      title: '针对"配送延时"类差评，当前"诚恳老板"风格显得过于官方。',
      description: '建议切换为"邻家店长"风格，并增加"具体优惠券额度"的说明。',
      improvement: '切换风格 + 增加优惠券说明',
      estimatedImprovement: '+12.4%',
      status: 'pending'
    },
    {
      id: 2,
      type: 'template',
      title: '发现用户对"菜品分量"的反馈较为集中。',
      description: '建议在现有回复中增加"正在核实出餐克重标准"的标准化承诺。',
      improvement: '增加分量承诺模板',
      estimatedImprovement: '+5.8%',
      status: 'pending'
    }
  ]);

  const [showAllFeedback, setShowAllFeedback] = useState(false);
  const { success, error } = useToast();

  const handleAddToTraining = (id: number) => {
    setEvaluations(evaluations.map(item => 
      item.id === id ? { ...item, addedToTraining: true } : item
    ));
    const item = evaluations.find(e => e.id === id);
    success('已加入训练集', `反馈 "${item?.comment}" 已添加到微调数据集`);
  };

  const handleViewAllFeedback = () => {
    setShowAllFeedback(!showAllFeedback);
    success('查看反馈', '正在加载所有低分反馈数据...');
  };

  const handleApplyInsight = (id: number) => {
    setInsights(insights.map(insight => 
      insight.id === id ? { ...insight, status: 'applied' as const } : insight
    ));
    const insight = insights.find(i => i.id === id);
    success('应用建议', `优化建议已应用：${insight?.improvement}`);
  };

  const handleDismissInsight = (id: number) => {
    setInsights(insights.map(insight => 
      insight.id === id ? { ...insight, status: 'dismissed' as const } : insight
    ));
    success('已忽略', '该优化建议已忽略');
  };

  const handleRefreshData = () => {
    success('刷新数据', '正在重新计算满意度指标...');
    setTimeout(() => {
      success('刷新完成', '所有评估指标已更新');
    }, 1500);
  };

  const handleExportReport = () => {
    success('导出报告', '正在生成评估报告...');
    setTimeout(() => {
      success('导出完成', '评估报告已下载');
    }, 1000);
  };

  const handleDeleteFeedback = (id: number) => {
    const item = evaluations.find(e => e.id === id);
    setEvaluations(evaluations.filter(e => e.id !== id));
    success('删除成功', `反馈 "${item?.comment}" 已删除`);
  };

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-2 duration-500">
      <div className="flex justify-between items-center">
        <h3 className="font-bold text-slate-800 text-lg flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-orange-600" />
          效能评估中心
        </h3>
        <div className="flex gap-2">
          <Button 
            variant="outline" 
            size="sm" 
            className="gap-2"
            onClick={handleRefreshData}
          >
            <RefreshCw className="w-4 h-4" />
            刷新数据
          </Button>
          <Button 
            variant="outline" 
            size="sm" 
            className="gap-2"
            onClick={handleExportReport}
          >
            <Download className="w-4 h-4" />
            导出报告
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <Card className="p-4 border-slate-100 bg-white lg:col-span-1">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-4 h-4 text-emerald-500" />
            <span className="text-sm font-bold text-slate-800">总体满意度</span>
          </div>
          <div className="text-center py-6 border-b border-slate-50 mb-6">
            <p className="text-4xl font-bold text-slate-900 mb-1">4.6<span className="text-sm text-slate-400 font-normal">/5.0</span></p>
            <div className="flex justify-center gap-1">
              {[1, 2, 3, 4].map(i => <span key={i} className="text-amber-400">★</span>)}
              <span className="text-slate-200">★</span>
            </div>
            <p className="text-[10px] text-slate-500 mt-2">基于 1,280 次真实评价反馈</p>
          </div>
          <div className="space-y-4">
            <div className="space-y-1">
              <div className="flex justify-between text-[10px] font-bold text-slate-500 uppercase">
                <span>正面反馈</span>
                <span className="text-emerald-500">92%</span>
              </div>
              <div className="h-1 bg-slate-100 rounded-full overflow-hidden">
                <div className="h-full bg-emerald-500 w-[92%]" />
              </div>
            </div>
            <div className="space-y-1">
              <div className="flex justify-between text-[10px] font-bold text-slate-500 uppercase">
                <span>负面反馈</span>
                <span className="text-red-500">8%</span>
              </div>
              <div className="h-1 bg-slate-100 rounded-full overflow-hidden">
                <div className="h-full bg-red-500 w-[8%]" />
              </div>
            </div>
          </div>
        </Card>

        <Card className="p-6 border-slate-100 bg-white lg:col-span-3">
          <div className="flex justify-between items-center mb-6">
            <h4 className="font-bold text-slate-800 flex items-center gap-2">
              <MessageSquare className="w-5 h-5 text-orange-600" />
              低分回复反馈循环 (Feedback Loop)
            </h4>
            <Button 
              variant="outline" 
              size="sm" 
              className="text-xs"
              onClick={handleViewAllFeedback}
            >
              {showAllFeedback ? '收起反馈' : '查看全部反馈'}
            </Button>
          </div>
          
          <div className="space-y-4">
            <div className="p-4 bg-red-50 border border-red-100 rounded-xl flex items-start gap-4 mb-6">
              <div className="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center shrink-0">
                <Lightbulb className="w-6 h-6 text-red-600" />
              </div>
              <div>
                <h5 className="text-sm font-bold text-red-900">自动归档提醒</h5>
                <p className="text-xs text-red-700 mt-1 leading-relaxed">
                  系统已自动将最近 24 小时内评分低于 3 分的 12 条回复归入"微调数据集"。这些案例将被用于优化下一版本的 System Prompt 逻辑。
                </p>
              </div>
            </div>

            <div className="space-y-3">
              {evaluations.map(item => (
                <div 
                  key={item.id} 
                  className={cn(
                    "flex items-center justify-between p-4 bg-slate-50 rounded-xl border border-slate-100 group hover:border-orange-200 transition-colors",
                    item.addedToTraining && "bg-emerald-50 border-emerald-100"
                  )}
                >
                  <div className="flex items-center gap-4">
                    <div className={cn(
                      "w-10 h-10 rounded-full flex items-center justify-center font-bold text-white",
                      item.rating <= 2 ? "bg-red-500" : "bg-amber-500"
                    )}>
                      {item.rating}
                    </div>
                    <div>
                      <p className="text-sm font-bold text-slate-800">{item.comment}</p>
                      <div className="flex items-center gap-3 mt-1">
                        <Badge variant="outline" className={cn("text-[10px] bg-white", item.addedToTraining && "bg-emerald-50 text-emerald-600 border-emerald-200")}>
                          {item.addedToTraining ? '已加入训练集' : item.tag}
                        </Badge>
                        <span className="text-[10px] text-slate-400">{item.date}</span>
                        {item.addedToTraining && (
                          <CheckCircle className="w-3 h-3 text-emerald-500" />
                        )}
                      </div>
                    </div>
                  </div>
                  <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    {!item.addedToTraining && (
                      <Button 
                        variant="ghost" 
                        size="sm" 
                        className="text-xs text-orange-600 font-bold"
                        onClick={() => handleAddToTraining(item.id)}
                      >
                        加入训练集
                        <ArrowRight className="w-3 h-3 ml-1" />
                      </Button>
                    )}
                    <Button 
                      variant="ghost" 
                      size="icon" 
                      className="h-8 w-8 text-slate-400 hover:text-red-600"
                      onClick={() => handleDeleteFeedback(item.id)}
                    >
                      <Trash2 className="w-3 h-3" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <Card className="p-6 border-slate-100 bg-slate-900 text-white relative overflow-hidden">
          <PieChart className="absolute -bottom-6 -right-6 w-32 h-32 text-white/5" />
          <h4 className="font-bold mb-6 flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-amber-400" />
            AI 优化建议 (AI Insights)
          </h4>
          <div className="space-y-4 relative z-10">
            {insights.filter(i => i.status === 'pending').map(insight => (
              <div key={insight.id} className="p-4 bg-white/5 rounded-xl border border-white/10 hover:bg-white/10 transition-colors">
                <div className="flex justify-between items-start mb-2">
                  <Badge className={cn(
                    "text-[9px] py-0 h-4",
                    insight.type === 'suggestion' ? "bg-amber-500/20 text-amber-400 border-amber-500/30" : "bg-blue-500/20 text-blue-400 border-blue-500/30"
                  )}>
                    {insight.type === 'suggestion' ? '高价值建议' : '模板建议'}
                  </Badge>
                  <span className="text-[10px] text-slate-500">预估提升: {insight.estimatedImprovement}</span>
                </div>
                <p className="text-sm font-medium mb-2 text-white">{insight.title}</p>
                <p className="text-xs text-slate-400 leading-relaxed mb-4">{insight.description}</p>
                <div className="flex gap-2">
                  <Button 
                    size="sm" 
                    className="bg-emerald-600 hover:bg-emerald-700 text-[10px] h-7"
                    onClick={() => handleApplyInsight(insight.id)}
                  >
                    <CheckCircle className="w-3 h-3 mr-1" />
                    应用此建议
                  </Button>
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    className="text-[10px] h-7 text-slate-400 hover:text-white"
                    onClick={() => handleDismissInsight(insight.id)}
                  >
                    忽略
                  </Button>
                </div>
              </div>
            ))}

            {insights.filter(i => i.status !== 'pending').length > 0 && (
              <div className="pt-4 border-t border-white/10">
                <p className="text-[10px] text-slate-500 font-bold uppercase mb-2">已处理建议</p>
                {insights.filter(i => i.status !== 'pending').map(insight => (
                  <div key={insight.id} className="flex items-center gap-2 p-2 bg-white/5 rounded-lg mb-2">
                    <CheckCircle className="w-3 h-3 text-emerald-500" />
                    <span className="text-[10px] text-slate-400">{insight.title}</span>
                    <Badge className={cn(
                      "text-[8px] py-0 h-3 ml-auto",
                      insight.status === 'applied' ? "bg-emerald-500/20 text-emerald-400" : "bg-slate-500/20 text-slate-400"
                    )}>
                      {insight.status === 'applied' ? '已应用' : '已忽略'}
                    </Badge>
                  </div>
                ))}
              </div>
            )}
          </div>
        </Card>

        <Card className="p-6 border-slate-100 flex flex-col items-center justify-center text-center space-y-4">
          <div className="w-16 h-16 rounded-full bg-emerald-100 flex items-center justify-center">
            <ThumbsUp className="w-8 h-8 text-emerald-600" />
          </div>
          <h4 className="font-bold text-slate-800 text-lg">品牌满意度持续攀升</h4>
          <p className="text-sm text-slate-500 max-w-sm">
            您的 AI 辅助回复模块已运行 45 天，整体客户二次回访率提升了 <span className="text-emerald-600 font-bold">18.5%</span>。
          </p>
          <div className="flex gap-4 w-full pt-4">
            <div className="flex-1 p-3 bg-slate-50 rounded-xl border border-slate-100">
              <p className="text-xl font-bold text-slate-900">84%</p>
              <p className="text-[10px] text-slate-400 font-bold uppercase">正面口碑增益</p>
            </div>
            <div className="flex-1 p-3 bg-slate-50 rounded-xl border border-slate-100">
              <p className="text-xl font-bold text-slate-900">-42%</p>
              <p className="text-[10px] text-slate-400 font-bold uppercase">差评滞留时间</p>
            </div>
          </div>
          <Button 
            className="w-full bg-emerald-600 hover:bg-emerald-700 text-white gap-2"
            onClick={() => success('查看详情', '正在生成详细分析报告...')}
          >
            <Eye className="w-4 h-4" />
            查看详细分析报告
          </Button>
        </Card>
      </div>
    </div>
  );
};

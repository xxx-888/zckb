import React, { useState, useEffect } from 'react';
import {
  ArrowLeft,
  TrendingUp,
  Target,
  BarChart3,
  Users,
  MapPin,
  ChevronRight,
  Sparkles,
  Trophy,
  Zap,
  Shield,
  CreditCard,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { Button } from '../../components/ui/button';
import { MobileLayout } from '../../components/MobileLayout';
import { Skeleton } from '../../components/ui/skeleton';
import { useToast } from '../../hooks/use-toast';
import { useNavigate } from 'react-router-dom';
import { fetchCompetitorTasks, createCompetitorTask } from '../../api/competitor';
import type { CompetitorTask } from '../../api/competitor';
import { useStore } from '../../context/StoreContext';

const plans = [
  {
    id: 'basic' as const,
    name: '基础版',
    price: 99,
    description: '单个竞对基础分析',
    features: ['1个竞对门店', '基础数据采集', '简单对比报告', '7天数据保留'],
    iconBg: 'bg-blue-500',
    bgColor: 'bg-blue-50',
    borderColor: 'border-blue-200'
  },
  {
    id: 'pro' as const,
    name: '专业版',
    price: 299,
    description: '多竞对深度分析',
    features: ['3个竞对门店', '深度数据采集', 'AI智能洞察', '30天数据保留', '竞对监控预警'],
    iconBg: 'bg-indigo-500',
    bgColor: 'bg-indigo-50',
    borderColor: 'border-indigo-200',
    recommended: true
  },
  {
    id: 'enterprise' as const,
    name: '企业版',
    price: 999,
    description: '全商圈竞对分析',
    features: ['10个竞对门店', '全维度数据采集', 'AI深度洞察', '90天数据保留', '实时监控预警', '定制报告导出'],
    iconBg: 'bg-amber-500',
    bgColor: 'bg-amber-50',
    borderColor: 'border-amber-200'
  }
];

export const MobileCompetitorAnalysis: React.FC = () => {
  const [tasks, setTasks] = useState<CompetitorTask[]>([]);
  const [showPayment, setShowPayment] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState<'basic' | 'pro' | 'enterprise'>('basic');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const fetchedRef = React.useRef(false);

  const { success, error: toastError } = useToast();
  const navigate = useNavigate();
  const { selectedStoreId } = useStore();

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const tasksData = await fetchCompetitorTasks(selectedStoreId);
      setTasks(tasksData);
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

  const handleBack = () => {
    navigate('/mobile/insights');
  };

  const handleSelectPlan = (planId: 'basic' | 'pro' | 'enterprise') => {
    setSelectedPlan(planId);
    setShowPayment(true);
  };

  const handlePayment = async () => {
    try {
      const plan = plans.find(p => p.id === selectedPlan);
      const newTask: Omit<CompetitorTask, 'id' | 'created_at'> = {
        competitor_name: '竞对门店',
        platform: '美团',
        status: 'collecting',
        payment_status: 'paid',
        price: plan?.price || 99,
      };
      const created = await createCompetitorTask(newTask);
      setTasks(prev => [created, ...prev]);
      setShowPayment(false);
      success('支付成功', `您已成功购买${plan?.name}，正在创建采集任务...`);
      setTimeout(() => {
        success('任务创建成功', '系统正在采集竞对数据，预计10分钟完成');
      }, 1500);
    } catch (err) {
      toastError('支付失败', '请稍后重试');
    }
  };

  const handleViewReport = (taskId: string) => {
    success('查看报告', '正在加载竞对分析报告...');
  };

  // ===== 加载状态（骨架屏）=====
  if (loading) {
    return (
      <MobileLayout title="竞对分析">
        <div className="space-y-6 p-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
          {/* 标题骨架 */}
          <Skeleton lines={2} className="p-5" />
          
          {/* 功能介绍骨架 */}
          <Skeleton lines={4} card={true} className="p-5" />
          
          {/* 任务列表骨架 */}
          <Skeleton lines={3} className="p-4" />
        </div>
      </MobileLayout>
    );
  }

  return (
    <MobileLayout title="竞对分析">
      <div className="space-y-6 pb-24 animate-in fade-in slide-in-from-bottom-4 duration-500">
        
        {/* Header */}
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="icon" onClick={handleBack}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div>
            <h2 className="font-bold text-slate-900">竞对分析</h2>
            <p className="text-xs text-slate-500">先付费，再采集分析</p>
          </div>
        </div>

        {!showPayment ? (
          <>
            {/* 功能介绍 */}
            <Card className="p-5 bg-white border-slate-100 shadow-sm">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-10 h-10 rounded-lg bg-orange-50 flex items-center justify-center">
                  <Target className="w-5 h-5 text-orange-500" />
                </div>
                <div>
                  <h3 className="font-bold text-slate-900">智能竞对分析</h3>
                  <p className="text-xs text-slate-400">了解竞争对手，制定精准策略</p>
                </div>
              </div>
              <div className="space-y-2 text-sm text-slate-600">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                  <span>自动采集竞对评价数据</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                  <span>AI生成对比分析报告</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                  <span>实时监控竞对动态</span>
                </div>
              </div>
            </Card>

            {/* 套餐选择 */}
            <div className="space-y-3">
              <h3 className="font-bold text-slate-800 text-sm px-1">选择分析套餐</h3>
              {plans.map((plan) => (
                <Card
                  key={plan.id}
                  className={`p-5 border-2 ${plan.bgColor} ${plan.borderColor} relative cursor-pointer hover:shadow-lg transition-all`}
                  onClick={() => handleSelectPlan(plan.id)}
                >
                  {plan.recommended && (
                    <Badge className="absolute -top-2 left-4 bg-orange-500 text-white border-none">
                      推荐
                    </Badge>
                  )}
                  <div className="flex items-center justify-between mb-3">
                    <div>
                      <h4 className="font-bold text-slate-900">{plan.name}</h4>
                      <p className="text-xs text-slate-500">{plan.description}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-3xl font-black text-slate-900">¥{plan.price}</p>
                      <p className="text-xs text-slate-400">/次</p>
                    </div>
                  </div>
                  <div className="space-y-2">
                    {plan.features.map((feature, idx) => (
                      <div key={idx} className="flex items-center gap-2 text-sm text-slate-600">
                        <CheckCircle2 className="w-4 h-4 text-emerald-500 flex-shrink-0" />
                        <span>{feature}</span>
                      </div>
                    ))}
                  </div>
                  <ChevronRight className="w-5 h-5 text-slate-400 ml-auto mt-3 block" />
                </Card>
              ))}
            </div>
          </>
        ) : (
          <>
            {/* 支付页面 */}
            <Card className="p-5 border-none shadow-lg">
              <div className="text-center mb-6">
                <div className={`w-16 h-16 mx-auto mb-4 rounded-2xl ${plans.find(p => p.id === selectedPlan)?.iconBg} flex items-center justify-center`}>
                  <CreditCard className="w-8 h-8 text-white" />
                </div>
                <h3 className="font-bold text-slate-900">
                  {plans.find(p => p.id === selectedPlan)?.name}
                </h3>
                <p className="text-3xl font-black text-slate-900 mb-4">
                  ¥{plans.find(p => p.id === selectedPlan)?.price}
                </p>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1 block">竞对门店名称</label>
                  <input
                    type="text"
                    placeholder="请输入竞对门店名称"
                    className="w-full px-4 py-3 border border-slate-200 rounded-xl text-sm outline-none focus:border-indigo-500"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1 block">监测平台</label>
                  <div className="grid grid-cols-2 gap-2">
                    {['美团', '大众点评', '抖音', '小红书'].map(platform => (
                      <Button
                        key={platform}
                        variant="outline"
                        className="text-sm py-2"
                      >
                        {platform}
                      </Button>
                    ))}
                  </div>
                </div>
              </div>

              <Button
                className="w-full mt-6 bg-orange-500 hover:bg-orange-600 text-white py-3 rounded-xl font-bold"
                onClick={handlePayment}
              >
                <CreditCard className="w-5 h-5 mr-2" />
                确认支付并创建任务
              </Button>
            </Card>
          </>
        )}

        {/* 我的任务列表 */}
        {tasks.length > 0 && (
          <div className="space-y-3">
            <h3 className="font-bold text-slate-800 text-sm px-1">我的分析任务</h3>
            {tasks.map((task) => (
              <Card key={task.id} className="p-4 bg-white border-none shadow-sm">
                <div className="flex items-center justify-between mb-3">
                  <div>
                    <h4 className="font-bold text-sm text-slate-900">{task.competitor_name}</h4>
                    <p className="text-xs text-slate-500">{task.platform} · {new Date(task.created_at).toLocaleDateString()}</p>
                  </div>
                  <Badge className={
                    task.status === 'completed' ? 'bg-emerald-100 text-emerald-700' :
                    task.status === 'collecting' ? 'bg-blue-100 text-blue-700' :
                    'bg-amber-100 text-amber-700'
                  }>
                    {task.status === 'completed' ? '已完成' :
                     task.status === 'collecting' ? '采集中' : '待处理'}
                  </Badge>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  className="w-full"
                  onClick={() => handleViewReport(task.id)}
                  disabled={task.status !== 'completed'}
                >
                  {task.status === 'completed' ? '查看分析报告' : '等待数据采集...'}
                </Button>
              </Card>
            ))}
          </div>
        )}

        {/* 使用说明 */}
        <Card className="p-5 bg-slate-50 border-slate-200">
          <h4 className="font-bold text-sm text-slate-900 mb-3 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-amber-500" />
            使用说明
          </h4>
          <div className="space-y-2 text-xs text-slate-600">
            <p>1. 选择分析套餐并完成支付</p>
            <p>2. 填写竞对门店信息</p>
            <p>3. 系统自动采集竞对评价数据</p>
            <p>4. 生成AI智能对比分析报告</p>
            <p>5. 根据报告优化您的经营策略</p>
          </div>
        </Card>
      </div>
    </MobileLayout>
  );
};

import React, { useState, useEffect } from 'react';
import {
  ArrowLeft,
  Target,
  CheckCircle2,
  CreditCard,
  Loader2,
  ChevronRight,
  AlertCircle,
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { Button } from '../../components/ui/button';
import { MobileLayout } from '../../components/MobileLayout';
import { Skeleton } from '../../components/ui/skeleton';
import { useToast } from '../../hooks/use-toast';
import { useNavigate } from 'react-router-dom';
import { fetchCompetitorTasks, createCompetitorTask, addCompetitor } from '../../api/competitor';
import type { CompetitorTask } from '../../api/competitor';
import { useStore } from '../../context/StoreContext';
import { collectionPackApi, CollectionPack, UserCollectionBalance } from '../../api/collectionPack';

export const MobileCompetitorAnalysis: React.FC = () => {
  const [tasks, setTasks] = useState<CompetitorTask[]>([]);
  const [showPayment, setShowPayment] = useState(false);
  const [selectedPackId, setSelectedPackId] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [competitorName, setCompetitorName] = useState('');
  const [selectedPlatform, setSelectedPlatform] = useState('美团');
  const fetchedRef = React.useRef(false);

  // 套餐包和余额状态
  const [packs, setPacks] = useState<CollectionPack[]>([]);
  const [balance, setBalance] = useState<UserCollectionBalance | null>(null);
  const [packsLoading, setPacksLoading] = useState(false);

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

  // 加载套餐包和余额
  const loadPacksAndBalance = async () => {
    try {
      setPacksLoading(true);
      const [packsData, balanceData] = await Promise.all([
        collectionPackApi.getPacks(),
        collectionPackApi.getBalance(),
      ]);
      setPacks(packsData || []);
      setBalance(balanceData);
    } catch (err) {
      console.error('加载套餐包失败:', err);
    } finally {
      setPacksLoading(false);
    }
  };

  useEffect(() => {
    if (fetchedRef.current) return;
    fetchedRef.current = true;
    loadData();
    loadPacksAndBalance();
  }, []);

  const handleBack = () => {
    navigate('/mobile/insights');
  };

  const handleSelectPack = (packId: string) => {
    setSelectedPackId(packId);
    setShowPayment(true);
  };

  const handlePayment = async () => {
    try {
      // 1. 先获取最新的余额
      const currentBalance = await collectionPackApi.getBalance();
      const pack = packs.find(p => p.id === selectedPackId);
      const creditCost = pack?.price || 0;

      if (!pack) {
        toastError('套餐不存在', '请重新选择套餐');
        return;
      }

      // 2. 检查积分是否足够
      if (!currentBalance || currentBalance.balance < creditCost) {
        toastError('积分不足', `需要 ${creditCost} 积分，当前余额 ${currentBalance?.balance || 0}，即将跳转到购买页面`);
        setTimeout(() => {
          navigate('/mobile/subscription?tab=credits');
        }, 1500);
        return;
      }

      // 3. 先创建竞品（如果输入了竞品名称）
      let competitorId = '';
      if (competitorName.trim()) {
        const newCompetitor = await addCompetitor({
          store_id: selectedStoreId || '',
          name: competitorName,
          platform: selectedPlatform,
        });
        competitorId = newCompetitor.id;
      } else {
        toastError('请输入竞对门店名称', '竞对门店名称不能为空');
        return;
      }

      // 4. 创建分析任务（后端会扣除积分）
      const created = await createCompetitorTask(competitorId, selectedPackId);
      setTasks(prev => [created, ...prev]);
      setShowPayment(false);
      
      // 5. 刷新余额显示
      const updatedBalance = await collectionPackApi.getBalance();
      setBalance(updatedBalance);
      
      success('支付成功', `您已成功购买${pack.name}，消耗 ${creditCost} 积分，正在创建采集任务...`);
      setTimeout(() => {
        success('任务创建成功', '系统正在采集竞对数据，预计10分钟完成');
      }, 1500);
    } catch (err: any) {
      // 如果后端返回 402，说明积分不足
      if (err?.response?.status === 402) {
        toastError('积分不足', '即将跳转到购买页面');
        setTimeout(() => {
          navigate('/mobile/subscription?tab=credits');
        }, 1500);
      } else {
        toastError('支付失败', err instanceof Error ? err.message : '请稍后重试');
      }
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

              {/* 显示当前积分余额 */}
              {balance && (
                <div className="mt-4 p-3 bg-indigo-50 rounded-xl">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-indigo-700">当前采集积分</span>
                    <span className="text-xl font-bold text-indigo-600">{balance.balance}</span>
                  </div>
                </div>
              )}
            </Card>

            {/* 套餐选择 - 显示真实套餐包 */}
            <div className="space-y-3">
              <h3 className="font-bold text-slate-800 text-sm px-1">选择采集套餐</h3>
              
              {packsLoading ? (
                <div className="text-center py-8 text-slate-400">
                  <Loader2 className="w-6 h-6 mx-auto animate-spin" />
                </div>
              ) : packs.filter(p => p.is_active).length === 0 ? (
                <Card className="p-5 text-center text-slate-400">
                  <p>暂无可用套餐</p>
                  <Button 
                    variant="outline" 
                    size="sm" 
                    className="mt-3"
                    onClick={() => navigate('/mobile/subscription?tab=credits')}
                  >
                    去购买积分
                  </Button>
                </Card>
              ) : (
                packs.filter(p => p.is_active).map((pack) => (
                  <Card
                    key={pack.id}
                    className="p-5 border-2 bg-indigo-50 border-indigo-200 relative cursor-pointer hover:shadow-lg transition-all"
                    onClick={() => handleSelectPack(pack.id)}
                  >
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <h4 className="font-bold text-slate-900">{pack.name}</h4>
                        <p className="text-xs text-slate-500">{pack.description}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-3xl font-black text-slate-900">{pack.price}</p>
                        <p className="text-xs text-slate-400">积分</p>
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center gap-2 text-sm text-slate-600">
                        <CheckCircle2 className="w-4 h-4 text-emerald-500 flex-shrink-0" />
                        <span>采集 {pack.credit_amount} 条数据</span>
                      </div>
                    </div>
                    <ChevronRight className="w-5 h-5 text-slate-400 ml-auto mt-3 block" />
                  </Card>
                ))
              )}
            </div>
          </>
        ) : (
          <>
            {/* 支付页面 */}
            <Card className="p-5 border-none shadow-lg">
              <div className="text-center mb-6">
                <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-indigo-500 flex items-center justify-center">
                  <CreditCard className="w-8 h-8 text-white" />
                </div>
                <h3 className="font-bold text-slate-900">
                  {packs.find(p => p.id === selectedPackId)?.name}
                </h3>
                <p className="text-3xl font-black text-slate-900 mb-4">
                  {packs.find(p => p.id === selectedPackId)?.price} 积分
                </p>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1 block">竞对门店名称</label>
                  <input
                    type="text"
                    placeholder="请输入竞对门店名称"
                    className="w-full px-4 py-3 border border-slate-200 rounded-xl text-sm outline-none focus:border-indigo-500"
                    value={competitorName}
                    onChange={(e) => setCompetitorName(e.target.value)}
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1 block">监测平台</label>
                  <div className="grid grid-cols-2 gap-2">
                    {['美团', '大众点评', '抖音', '小红书'].map(platform => (
                      <Button
                        key={platform}
                        variant={selectedPlatform === platform ? "default" : "outline"}
                        className="text-sm py-2"
                        onClick={() => setSelectedPlatform(platform)}
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

              <Button
                variant="ghost"
                className="w-full mt-3"
                onClick={() => setShowPayment(false)}
              >
                返回套餐选择
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
            <p>1. 选择采集套餐并确认支付（消耗采集积分）</p>
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

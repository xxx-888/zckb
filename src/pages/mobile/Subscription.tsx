import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Check, Star, Crown, Zap, CheckCircle2, Loader2, AlertTriangle } from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';
import { subscriptionApi, SubscriptionPlan, UserSubscription } from '../../api/subscription';

export const Subscription: React.FC = () => {
  const navigate = useNavigate();
  const { success, error } = useToast();
  
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [plans, setPlans] = useState<SubscriptionPlan[]>([]);
  const [currentSubscription, setCurrentSubscription] = useState<UserSubscription | null>(null);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState<SubscriptionPlan | null>(null);
  const [paymentMethod, setPaymentMethod] = useState<'wechat' | 'alipay'>('wechat');
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('yearly');
  const [paymentRecord, setPaymentRecord] = useState<any>(null);

  // 加载订阅计划和当前订阅
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [plansData, currentSub] = await Promise.all([
        subscriptionApi.getPlans(),
        subscriptionApi.getCurrentSubscription()
      ]);
      setPlans(plansData);
      setCurrentSubscription(currentSub);
    } catch (err: any) {
      error('加载失败', err.message || '无法获取订阅信息');
    } finally {
      setLoading(false);
    }
  };

  const handleUpgrade = (plan: SubscriptionPlan) => {
    setSelectedPlan(plan);
    setShowUpgradeModal(true);
  };

  const handleConfirmUpgrade = async () => {
    if (!selectedPlan) return;
    
    try {
      setActionLoading(true);
      // 1. 创建支付订单
      const payment = await subscriptionApi.createPayment({
        plan_id: selectedPlan.id,
        payment_method: paymentMethod,
        billing_cycle: billingCycle,
      });
      setPaymentRecord(payment);
      
      // 2. 模拟支付成功（自动激活订阅）
      await subscriptionApi.simulatePayment(payment.id);
      
      setShowUpgradeModal(false);
      setShowPaymentModal(false);
      success('支付成功', `已成功订阅${selectedPlan.name}`);
      loadData(); // 重新加载数据
    } catch (err: any) {
      error('支付失败', err.message || '支付过程中出现错误');
    } finally {
      setActionLoading(false);
    }
  };

  const handleSelectPaymentMethod = (method: 'wechat' | 'alipay') => {
    setPaymentMethod(method);
  };

  const handleShowPayment = () => {
    setShowUpgradeModal(false);
    setShowPaymentModal(true);
  };

  const handleCancel = async () => {
    if (!confirm('确定要取消订阅吗？取消后当前周期内仍可继续使用。')) {
      return;
    }
    
    try {
      setActionLoading(true);
      const updated = await subscriptionApi.cancelSubscription();
      setCurrentSubscription(updated);
      success('取消成功', '订阅已取消');
      loadData(); // 重新加载数据
    } catch (err: any) {
      error('取消失败', err.message || '取消订阅时出现错误');
    } finally {
      setActionLoading(false);
    }
  };

  // 获取当前计划数据
  const currentPlanData = plans.find(p => 
    currentSubscription && p.id === currentSubscription.plan.id
  );
  
  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-indigo-600 animate-spin" />
      </div>
    );
  }
  
  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      {/* Header */}
      <div className="bg-white px-6 py-4 flex items-center gap-4 shadow-sm">
        <button 
          onClick={() => navigate('/mobile/settings')}
          className="text-slate-600 hover:bg-slate-100 p-2 rounded-xl transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <h1 className="text-lg font-bold text-slate-900">版本订阅</h1>
      </div>
      
      <div className="p-6 space-y-6">
        {/* Current Plan */}
        <Card className="p-6 border-slate-100 shadow-sm bg-white">
          <div className="flex items-center justify-between mb-4">
            <div>
              <p className="text-slate-400 text-xs font-bold uppercase tracking-wider">当前版本</p>
              <h2 className="text-2xl font-black mt-1 text-slate-900">
                {currentPlanData?.name || '未订阅'}
              </h2>
            </div>
            <div className="w-14 h-14 rounded-2xl bg-orange-50 flex items-center justify-center">
              {currentPlanData && (
                <>
                  {currentPlanData.max_stores <= 1 && <Star className="w-7 h-7 text-orange-500" />}
                  {currentPlanData.max_stores > 1 && currentPlanData.max_stores <= 5 && <Zap className="w-7 h-7 text-indigo-600" />}
                  {currentPlanData.max_stores > 5 && <Crown className="w-7 h-7 text-amber-600" />}
                </>
              )}
            </div>
          </div>
          <div className="flex items-center gap-2 text-slate-500 text-sm">
            <CheckCircle2 className="w-4 h-4 text-emerald-500" />
            <span>
              {!currentSubscription && '未订阅'}
              {currentSubscription?.status === 'trial' && `试用中，到期时间：${currentSubscription.end_date}`}
              {currentSubscription?.status === 'active' && `有效期至 ${currentSubscription.end_date}`}
              {currentSubscription?.status === 'expired' && '已过期'}
              {currentSubscription?.status === 'cancelled' && `已取消，有效期至 ${currentSubscription.end_date}`}
            </span>
          </div>
          {currentSubscription && currentSubscription.status !== 'cancelled' && (
            <Button 
              onClick={handleCancel}
              disabled={actionLoading}
              variant="outline"
              className="w-full mt-4 border-rose-100 text-rose-600 hover:bg-rose-50 disabled:opacity-50"
            >
              {actionLoading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  取消中...
                </>
              ) : (
                '取消订阅'
              )}
            </Button>
          )}
        </Card>
        
        {/* Plans */}
        <div className="space-y-4">
          <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-1">选择版本</h4>
          
          {plans.map((plan) => {
            const isCurrent = currentPlanData && plan.id === currentPlanData.id;
            
            return (
              <div 
                key={plan.id}
                className={`bg-white rounded-2xl p-6 shadow-sm relative ${
                  plan.max_stores > 1 && plan.max_stores <= 5 ? 'ring-2 ring-indigo-600' : ''
                }`}
              >
                {plan.max_stores > 1 && plan.max_stores <= 5 && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-indigo-600 text-white text-xs font-bold px-4 py-1 rounded-full">
                    最受欢迎
                  </div>
                )}
                
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-black text-slate-900">{plan.name}</h3>
                    <div className="flex items-baseline gap-1 mt-2">
                      <span className="text-3xl font-black text-slate-900">
                        {plan.price_monthly === 0 ? '免费' : `¥${billingCycle === 'monthly' ? plan.price_monthly : plan.price_yearly}`}
                      </span>
                      {plan.price_monthly > 0 && (
                        <span className="text-sm text-slate-400">/{billingCycle === 'monthly' ? '月' : '年'}</span>
                      )}
                    </div>
                  </div>
                  <div className={`bg-${plan.max_stores <= 1 ? 'slate' : plan.max_stores <= 5 ? 'indigo' : 'amber'}-50 p-3 rounded-2xl`}>
                    {plan.max_stores <= 1 && <Star className={`w-6 h-6 text-slate-600`} />}
                    {plan.max_stores > 1 && plan.max_stores <= 5 && <Zap className={`w-6 h-6 text-indigo-600`} />}
                    {plan.max_stores > 5 && <Crown className={`w-6 h-6 text-amber-600`} />}
                  </div>
                </div>
                
                <div className="space-y-3 mb-6">
                  {plan.features && Array.isArray(plan.features) && plan.features.map((feature: any, idx: number) => (
                    <div key={idx} className="flex items-center gap-3">
                      <Check className={`w-4 h-4 text-${plan.max_stores <= 1 ? 'slate' : plan.max_stores <= 5 ? 'indigo' : 'amber'}-600 flex-shrink-0`} />
                      <span className="text-sm text-slate-700">{typeof feature === 'string' ? feature : feature.name || ''}</span>
                    </div>
                  ))}
                </div>
                
                {isCurrent ? (
                  <Button 
                    disabled
                    className="w-full bg-slate-100 text-slate-400 rounded-2xl py-6 font-bold cursor-not-allowed"
                  >
                    <CheckCircle2 className="w-5 h-5 mr-2" />
                    当前版本
                  </Button>
                ) : (
                  <Button 
                    onClick={() => handleUpgrade(plan)}
                    disabled={actionLoading}
                    className={`w-full rounded-2xl py-6 text-lg font-bold shadow-xl disabled:opacity-50 ${
                      plan.max_stores > 1 && plan.max_stores <= 5
                        ? 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-indigo-100'
                        : 'bg-slate-900 hover:bg-slate-800 text-white'
                    }`}
                  >
                    升级到{plan.name}
                  </Button>
                )}
              </div>
            );
          })}
        </div>
        
        {/* Subscription History */}
        {currentSubscription && (
          <div className="space-y-3">
            <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-1">订阅记录</h4>
            <div className="bg-white rounded-2xl overflow-hidden shadow-sm">
              <div className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-bold text-slate-900">{currentPlanData?.name || '未知版本'}</p>
                    <p className="text-xs text-slate-400 mt-1">
                      {currentSubscription.status === 'trial' ? '试用' : '购买'} - {currentSubscription.start_date}
                    </p>
                  </div>
                  <span className="text-sm font-bold text-green-600">
                    {currentSubscription.status === 'trial' ? '试用' : `¥${currentPlanData?.price_yearly || 0}/年`}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
      
      {/* Upgrade Modal */}
      {showUpgradeModal && selectedPlan && (
        <div className="fixed inset-0 bg-black/50 flex items-end justify-center z-50" onClick={() => setShowUpgradeModal(false)}>
          <div 
            className="bg-white rounded-t-3xl w-full max-w-lg p-6 space-y-4 animate-in slide-in-from-bottom duration-300"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-slate-900">确认升级</h2>
              <button 
                onClick={() => setShowUpgradeModal(false)}
                className="text-slate-400 hover:text-slate-600"
              >
                ✕
              </button>
            </div>
            
            <div className="bg-slate-50 rounded-2xl p-4">
              <h3 className="font-bold text-slate-900">
                {selectedPlan.name}
              </h3>
              <p className="text-2xl font-black text-slate-900 mt-2">
                ¥{billingCycle === 'monthly' ? selectedPlan.price_monthly : selectedPlan.price_yearly}
                <span className="text-sm font-normal text-slate-400">/{billingCycle === 'monthly' ? '月' : '年'}</span>
              </p>
            </div>
            
            {/* 计费周期选择 */}
            <div className="space-y-2">
              <p className="text-xs font-bold text-slate-500 uppercase tracking-wider">计费周期：</p>
              <div className="grid grid-cols-2 gap-3">
                <button
                  onClick={() => setBillingCycle('monthly')}
                  className={`p-4 rounded-xl border-2 transition-colors ${
                    billingCycle === 'monthly'
                      ? 'border-indigo-500 bg-indigo-50'
                      : 'border-slate-200 hover:border-slate-300'
                  }`}
                >
                  <div className="text-center">
                    <div className="text-lg font-black text-slate-900">¥{selectedPlan.price_monthly || 0}</div>
                    <div className="text-xs text-slate-500">/月</div>
                  </div>
                </button>
                <button
                  onClick={() => setBillingCycle('yearly')}
                  className={`p-4 rounded-xl border-2 transition-colors relative ${
                    billingCycle === 'yearly'
                      ? 'border-indigo-500 bg-indigo-50'
                      : 'border-slate-200 hover:border-slate-300'
                  }`}
                >
                  {selectedPlan.price_yearly > 0 && selectedPlan.price_monthly > 0 && (
                    <div className="absolute -top-2 -right-2 bg-emerald-500 text-white text-xs px-2 py-0.5 rounded-full">
                      省{Math.round((1 - selectedPlan.price_yearly / (selectedPlan.price_monthly * 12)) * 100)}%
                    </div>
                  )}
                  <div className="text-center">
                    <div className="text-lg font-black text-slate-900">¥{selectedPlan.price_yearly || 0}</div>
                    <div className="text-xs text-slate-500">/年</div>
                  </div>
                </button>
              </div>
            </div>
            
            <div className="space-y-2">
              <p className="text-xs font-bold text-slate-500 uppercase tracking-wider">包含功能：</p>
              {selectedPlan.features && Array.isArray(selectedPlan.features) && selectedPlan.features.map((feature: any, idx: number) => (
                <div key={idx} className="flex items-center gap-3">
                  <Check className="w-4 h-4 text-indigo-600 flex-shrink-0" />
                  <span className="text-sm text-slate-700">{typeof feature === 'string' ? feature : feature.name || ''}</span>
                </div>
              ))}
            </div>
            
            <div className="space-y-2 mt-4">
              <p className="text-xs font-bold text-slate-500 uppercase tracking-wider">选择支付方式：</p>
              <div className="grid grid-cols-2 gap-3">
                <button
                  onClick={() => handleSelectPaymentMethod('wechat')}
                  className={`p-4 rounded-xl border-2 transition-colors ${
                    paymentMethod === 'wechat'
                      ? 'border-emerald-500 bg-emerald-50'
                      : 'border-slate-200 hover:border-slate-300'
                  }`}
                >
                  <div className="text-center">
                    <div className="text-2xl mb-1">💚</div>
                    <div className="text-sm font-bold text-slate-900">微信支付</div>
                  </div>
                </button>
                <button
                  onClick={() => handleSelectPaymentMethod('alipay')}
                  className={`p-4 rounded-xl border-2 transition-colors ${
                    paymentMethod === 'alipay'
                      ? 'border-emerald-500 bg-emerald-50'
                      : 'border-slate-200 hover:border-slate-300'
                  }`}
                >
                  <div className="text-center">
                    <div className="text-2xl mb-1">💙</div>
                    <div className="text-sm font-bold text-slate-900">支付宝</div>
                  </div>
                </button>
              </div>
            </div>
            
            <Button 
              onClick={handleConfirmUpgrade}
              disabled={actionLoading}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-7 text-lg font-bold shadow-xl shadow-indigo-100 mt-4 disabled:opacity-50"
            >
              {actionLoading ? (
                <>
                  <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                  处理中...
                </>
              ) : (
                `确认支付 ¥${billingCycle === 'monthly' ? selectedPlan?.price_monthly : selectedPlan?.price_yearly}`
              )}
            </Button>
          </div>
        </div>
      )}
      
      {/* Payment Success Modal */}
      {showPaymentModal && paymentRecord && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-3xl p-8 space-y-6 max-w-sm mx-4 animate-in fade-in duration-300">
            <div className="text-center">
              <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Check className="w-8 h-8 text-emerald-600" />
              </div>
              <h3 className="text-xl font-bold text-slate-900">支付成功！</h3>
              <p className="text-sm text-slate-500 mt-2">
                已成功订阅 <span className="font-bold text-indigo-600">{selectedPlan?.name}</span>
              </p>
            </div>
            
            <div className="bg-slate-50 rounded-2xl p-4 space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-slate-500">订单号</span>
                <span className="text-slate-900 font-mono">{paymentRecord.id?.slice(0, 8)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-500">支付方式</span>
                <span className="text-slate-900">{paymentMethod === 'wechat' ? '微信支付' : '支付宝'}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-500">金额</span>
                <span className="text-slate-900 font-bold">¥{paymentRecord.amount}</span>
              </div>
            </div>
            
            <Button 
              onClick={() => {
                setShowPaymentModal(false);
                loadData();
              }}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-6 text-lg font-bold"
            >
              完成
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

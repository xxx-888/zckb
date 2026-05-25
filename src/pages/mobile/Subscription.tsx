import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Check, Star, Crown, Zap, CheckCircle2, Loader2, Store, MessageSquare, Infinity, Flame } from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';
import { subscriptionApi, SubscriptionPlan, UserSubscription } from '../../api/subscription';

const PlanIcon = ({ plan, className }: { plan: SubscriptionPlan; className?: string }) => {
  if (plan.max_stores <= 1) return <Star className={`${className} text-slate-500`} />;
  if (plan.max_stores <= 5) return <Zap className={`${className} text-indigo-600`} />;
  return <Crown className={`${className} text-amber-600`} />;
};

/* ---- 支付方式 SVG 图标 ---- */
const WeChatPayIcon = ({ size = 40 }: { size?: number }) => (
  <svg width={size} height={size} viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="40" height="40" rx="8" fill="#07C160"/>
    {/* 微信气泡 */}
    <path d="M10.5 13C10.5 13 13 11C16.5 11 19 13C19 13 16.5 15 14.5 16.5C13.8 17 13.5 17.8 13.8 18.5L15.5 22.5L12.5 19C11.5 18.3 10.5 18 9.5 18C7.5 18 6 16.8 6 14C6 11.2 8.5 9 11.5 9C14.5 9 16.5 11 16.5 13C16.5 13 16.5 13 10.5 13Z" fill="white"/>
    <path d="M21.5 18C21.5 18 24 20 27.5 20C31 20 33.5 18 33.5 18C33.5 18 31 16 29 15C28.3 14.7 28.5 14.2 28.7 13.8L27.5 11L29.5 13C30.5 13.7 31.5 14 32.5 14C34.5 14 36 15.2 36 18C36 20.8 33.5 23 30.5 23C27.5 23 24.5 21 21.5 18Z" fill="white" fillOpacity="0.55"/>
  </svg>
);

const AlipayIcon = ({ size = 40 }: { size?: number }) => (
  <svg width={size} height={size} viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="40" height="40" rx="8" fill="#1677FF"/>
    {/* 支付宝 "支" 字简化图标 */}
    <path d="M20 8C13.4 8 8 13.4 8 20C8 26.6 13.4 32 20 32C26.6 32 32 26.6 32 20C32 13.4 26.6 8 20 8ZM20 11C22.2 11 24.1 12.5 25 14.8L22.5 16C22 15.2 21.1 14.8 20 14.8C17.5 14.8 15.5 16.8 15.5 19.3C15.5 20.4 15.8 21.3 16.5 22L14.5 23.5C13.3 22.1 12.5 20.2 12.5 18.1C12.5 14.1 15.8 11 20 11ZM20 29C17.8 29 15.9 27.5 15 25.2L17.5 24C18 24.8 18.9 25.2 20 25.2C22.5 25.2 24.5 23.2 24.5 20.7C24.5 19.6 24.2 18.7 23.5 18L25.5 16.5C26.7 17.9 27.5 19.8 27.5 21.9C27.5 25.9 24.2 29 20 29Z" fill="white"/>
  </svg>
);

const PlanBadge = ({ plan }: { plan: SubscriptionPlan }) => {
  if (plan.max_stores > 1 && plan.max_stores <= 5) {
    return (
      <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-indigo-600 text-white text-xs font-bold px-4 py-1 rounded-full shadow-lg">
        最受欢迎
      </div>
    );
  }
  if (plan.price_monthly === 0) {
    return (
      <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-emerald-500 text-white text-xs font-bold px-4 py-1 rounded-full shadow-lg">
        免费试用
      </div>
    );
  }
  return null;
};

const SpecItem = ({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) => (
  <div className="flex items-center gap-3 p-3 bg-slate-50 rounded-xl">
    <div className="text-indigo-600">{icon}</div>
    <div className="flex-1">
      <p className="text-xs text-slate-500">{label}</p>
      <p className="text-sm font-bold text-slate-900">{value}</p>
    </div>
  </div>
);

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
    setBillingCycle('yearly');
    setShowUpgradeModal(true);
  };

  const handleConfirmUpgrade = async () => {
    if (!selectedPlan) return;
    
    try {
      setActionLoading(true);
      const payment = await subscriptionApi.createPayment({
        plan_id: selectedPlan.id,
        payment_method: paymentMethod,
        billing_cycle: billingCycle,
      });
      setPaymentRecord(payment);
      
      await subscriptionApi.simulatePayment(payment.id);
      
      setShowUpgradeModal(false);
      setShowPaymentModal(false);
      success('支付成功', `已成功订阅 ${selectedPlan.name}`);
      loadData();
    } catch (err: any) {
      error('支付失败', err.message || '支付过程中出现错误');
    } finally {
      setActionLoading(false);
    }
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
      loadData();
    } catch (err: any) {
      error('取消失败', err.message || '取消订阅时出现错误');
    } finally {
      setActionLoading(false);
    }
  };

  const currentPlanData = plans.find(p => 
    currentSubscription && p.id === currentSubscription.plan.id
  );

  const getSavingsPercent = (plan: SubscriptionPlan) => {
    if (!plan.price_monthly || !plan.price_yearly) return 0;
    return Math.round((1 - plan.price_yearly / (plan.price_monthly * 12)) * 100);
  };

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
      <div className="bg-white px-6 py-4 flex items-center gap-4 shadow-sm sticky top-0 z-10">
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
        {currentSubscription && (
          <Card className="p-6 border-slate-100 shadow-sm bg-white overflow-hidden relative">
            {/* Status indicator */}
            <div className={`absolute top-0 left-0 w-full h-1 ${
              currentSubscription.status === 'active' ? 'bg-emerald-500' :
              currentSubscription.status === 'trial' ? 'bg-indigo-500' :
              currentSubscription.status === 'expired' ? 'bg-amber-500' :
              'bg-slate-300'
            }`} />
            
            <div className="flex items-center justify-between mb-4">
              <div>
                <p className="text-slate-400 text-xs font-bold uppercase tracking-wider">当前版本</p>
                <h2 className="text-2xl font-black mt-1 text-slate-900">
                  {currentPlanData?.name || '未知版本'}
                </h2>
              </div>
              <div className="w-14 h-14 rounded-2xl bg-orange-50 flex items-center justify-center">
                {currentPlanData && <PlanIcon plan={currentPlanData} className="w-7 h-7" />}
              </div>
            </div>

            {/* Status info */}
            <div className="flex items-center gap-2 text-slate-500 text-sm mb-4">
              <CheckCircle2 className={`w-4 h-4 ${
                currentSubscription.status === 'active' ? 'text-emerald-500' :
                currentSubscription.status === 'trial' ? 'text-indigo-500' :
                'text-slate-400'
              }`} />
              <span>
                {currentSubscription.status === 'trial' && `试用中，到期时间：${currentSubscription.end_date}`}
                {currentSubscription.status === 'active' && `有效期至 ${currentSubscription.end_date}`}
                {currentSubscription.status === 'expired' && '已过期，请续费'}
                {currentSubscription.status === 'cancelled' && `已取消，有效期至 ${currentSubscription.end_date}`}
              </span>
            </div>

            {/* Current plan specs */}
            {currentPlanData && (
              <div className="grid grid-cols-2 gap-3 mb-4">
                <div className="bg-slate-50 rounded-xl p-3">
                  <p className="text-xs text-slate-500">最大门店数</p>
                  <p className="text-lg font-black text-slate-900">
                    {currentPlanData.max_stores >= 999 ? '∞' : currentPlanData.max_stores}
                  </p>
                </div>
                <div className="bg-slate-50 rounded-xl p-3">
                  <p className="text-xs text-slate-500">月评论额度</p>
                  <p className="text-lg font-black text-slate-900">
                    {currentPlanData.max_reviews_per_month ? currentPlanData.max_reviews_per_month.toLocaleString() : '∞'}
                  </p>
                </div>
              </div>
            )}

            {currentSubscription.status !== 'cancelled' && currentSubscription.status !== 'expired' && (
              <Button 
                onClick={handleCancel}
                disabled={actionLoading}
                variant="outline"
                className="w-full border-rose-100 text-rose-600 hover:bg-rose-50 disabled:opacity-50"
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
        )}

        {/* Plans */}
        <div className="space-y-4">
          <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-1">选择版本</h4>
          
          {plans.map((plan) => {
            const isCurrent = currentPlanData && plan.id === currentPlanData.id;
            const savingsPercent = getSavingsPercent(plan);
            
            return (
              <div 
                key={plan.id}
                className={`bg-white rounded-2xl p-6 shadow-sm relative border-2 transition-all ${
                  isCurrent ? 'border-emerald-500' :
                  plan.max_stores > 1 && plan.max_stores <= 5 ? 'border-indigo-200 hover:border-indigo-400' :
                  'border-slate-100 hover:border-slate-300'
                }`}
              >
                <PlanBadge plan={plan} />
                
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-xl font-black text-slate-900">{plan.name}</h3>
                      {isCurrent && (
                        <span className="bg-emerald-100 text-emerald-700 text-xs font-bold px-2 py-0.5 rounded-full">
                          当前版本
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="bg-slate-50 p-3 rounded-2xl">
                    <PlanIcon plan={plan} className="w-6 h-6" />
                  </div>
                </div>

                {/* Pricing - show both monthly and yearly */}
                <div className="mb-4">
                  {plan.price_monthly === 0 ? (
                    <div className="text-3xl font-black text-emerald-600">免费</div>
                  ) : (
                    <div className="space-y-1">
                      {/* Yearly price (primary) */}
                      <div className="flex items-baseline gap-1">
                        <span className="text-3xl font-black text-slate-900">
                          ¥{plan.price_yearly}
                        </span>
                        <span className="text-sm text-slate-400">/年</span>
                        {savingsPercent > 0 && (
                          <span className="ml-1 bg-emerald-100 text-emerald-700 text-xs font-bold px-1.5 py-0.5 rounded">
                            省{savingsPercent}%
                          </span>
                        )}
                      </div>
                      {/* Monthly equivalent */}
                      <div className="text-sm text-slate-500">
                        月付 ¥{plan.price_monthly}/月
                      </div>
                    </div>
                  )}
                </div>

                {/* Key Specs */}
                <div className="grid grid-cols-2 gap-2 mb-4">
                  <div className="flex items-center gap-2 bg-slate-50 rounded-lg p-2">
                    <Store className="w-4 h-4 text-indigo-600 flex-shrink-0" />
                    <div>
                      <p className="text-xs text-slate-500">门店数</p>
                      <p className="text-sm font-bold text-slate-900">
                        {plan.max_stores >= 999 ? '无限' : `最多 ${plan.max_stores} 家`}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 bg-slate-50 rounded-lg p-2">
                    <MessageSquare className="w-4 h-4 text-indigo-600 flex-shrink-0" />
                    <div>
                      <p className="text-xs text-slate-500">月评论额</p>
                      <p className="text-sm font-bold text-slate-900">
                        {plan.max_reviews_per_month ? plan.max_reviews_per_month.toLocaleString() : '无限'}
                      </p>
                    </div>
                  </div>
                </div>
                
                {/* Features */}
                {plan.features && Array.isArray(plan.features) && plan.features.length > 0 && (
                  <div className="mb-4">
                    <p className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">功能特性</p>
                    <div className="space-y-1.5">
                      {plan.features.map((feature: any, idx: number) => (
                        <div key={idx} className="flex items-center gap-2">
                          <Check className="w-3.5 h-3.5 text-indigo-600 flex-shrink-0" />
                          <span className="text-xs text-slate-700">{typeof feature === 'string' ? feature : feature.name || ''}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                
                {/* Action Button */}
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
                    className={`w-full rounded-2xl py-6 text-lg font-bold shadow-lg disabled:opacity-50 ${
                      plan.max_stores > 1 && plan.max_stores <= 5
                        ? 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-indigo-100'
                        : 'bg-slate-900 hover:bg-slate-800 text-white'
                    }`}
                  >
                    升级到 {plan.name}
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
            className="bg-white rounded-t-3xl w-full max-w-lg p-6 space-y-5 animate-in slide-in-from-bottom duration-300 max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-1">
              <h2 className="text-lg font-bold text-slate-900">确认订阅</h2>
              <button 
                onClick={() => setShowUpgradeModal(false)}
                className="text-slate-400 hover:text-slate-600 w-8 h-8 flex items-center justify-center rounded-full hover:bg-slate-100"
              >
                ✕
              </button>
            </div>
            
            {/* Plan Summary */}
            <div className="bg-slate-50 rounded-2xl p-4">
              <div className="flex items-center gap-3 mb-3">
                <div className="bg-white w-10 h-10 rounded-xl flex items-center justify-center">
                  <PlanIcon plan={selectedPlan} className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-bold text-slate-900">{selectedPlan.name}</h3>
                  <p className="text-xs text-slate-500">
                    最多 {selectedPlan.max_stores >= 999 ? '无限' : selectedPlan.max_stores} 家门店
                    · 月额度 {selectedPlan.max_reviews_per_month ? selectedPlan.max_reviews_per_month.toLocaleString() : '无限'}
                  </p>
                </div>
              </div>

              {/* Selected price preview */}
              <div className="bg-white rounded-xl p-3">
                <div className="flex items-baseline gap-1">
                  <span className="text-2xl font-black text-slate-900">
                    ¥{billingCycle === 'monthly' ? selectedPlan.price_monthly : selectedPlan.price_yearly}
                  </span>
                  <span className="text-sm text-slate-400">/{billingCycle === 'monthly' ? '月' : '年'}</span>
                </div>
                {billingCycle === 'yearly' && selectedPlan.price_monthly > 0 && (
                  <p className="text-xs text-emerald-600 mt-1">
                    相比月付省 {Math.round((1 - selectedPlan.price_yearly / (selectedPlan.price_monthly * 12)) * 100)}%
                  </p>
                )}
              </div>
            </div>
            
            {/* Billing Cycle Selection */}
            <div className="space-y-2">
              <p className="text-xs font-bold text-slate-500 uppercase tracking-wider">计费周期</p>
              <div className="grid grid-cols-2 gap-3">
                <button
                  onClick={() => setBillingCycle('monthly')}
                  className={`p-4 rounded-xl border-2 transition-all text-left ${
                    billingCycle === 'monthly'
                      ? 'border-indigo-500 bg-indigo-50'
                      : 'border-slate-200 hover:border-slate-300'
                  }`}
                >
                  <div className="text-lg font-black text-slate-900">¥{selectedPlan.price_monthly || 0}</div>
                  <div className="text-xs text-slate-500">/月 · 灵活试用</div>
                  {billingCycle === 'monthly' && (
                    <div className="mt-2 text-xs font-bold text-indigo-600">✓ 已选择</div>
                  )}
                </button>
                <button
                  onClick={() => setBillingCycle('yearly')}
                  className={`p-4 rounded-xl border-2 transition-all text-left relative ${
                    billingCycle === 'yearly'
                      ? 'border-indigo-500 bg-indigo-50'
                      : 'border-slate-200 hover:border-slate-300'
                  }`}
                >
                  {selectedPlan.price_yearly > 0 && selectedPlan.price_monthly > 0 && (
                    <div className="absolute -top-2 -right-2 bg-emerald-500 text-white text-xs px-2 py-0.5 rounded-full font-bold">
                      省{Math.round((1 - selectedPlan.price_yearly / (selectedPlan.price_monthly * 12)) * 100)}%
                    </div>
                  )}
                  <div className="text-lg font-black text-slate-900">¥{selectedPlan.price_yearly || 0}</div>
                  <div className="text-xs text-slate-500">/年 · 更划算</div>
                  {billingCycle === 'yearly' && (
                    <div className="mt-2 text-xs font-bold text-indigo-600">✓ 已选择</div>
                  )}
                </button>
              </div>
            </div>
            
            {/* Features in modal */}
            {selectedPlan.features && Array.isArray(selectedPlan.features) && (
              <div className="space-y-2">
                <p className="text-xs font-bold text-slate-500 uppercase tracking-wider">包含功能</p>
                <div className="grid grid-cols-1 gap-1.5">
                  {selectedPlan.features.map((feature: any, idx: number) => (
                    <div key={idx} className="flex items-center gap-2">
                      <Check className="w-4 h-4 text-indigo-600 flex-shrink-0" />
                      <span className="text-sm text-slate-700">{typeof feature === 'string' ? feature : feature.name || ''}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Payment Method */}
            <div className="space-y-2">
              <p className="text-xs font-bold text-slate-500 uppercase tracking-wider">支付方式</p>
              <div className="grid grid-cols-2 gap-3">
                <button
                  onClick={() => setPaymentMethod('wechat')}
                  className={`p-4 rounded-xl border-2 transition-all ${
                    paymentMethod === 'wechat'
                      ? 'border-emerald-500 bg-emerald-50'
                      : 'border-slate-200 hover:border-slate-300'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <WeChatPayIcon size={36} />
                    <div className="text-left">
                      <div className="text-sm font-bold text-slate-900">微信支付</div>
                      <div className="text-xs text-slate-400">推荐使用</div>
                    </div>
                  </div>
                  {paymentMethod === 'wechat' && (
                    <div className="mt-2 text-xs font-bold text-emerald-600">✓ 已选择</div>
                  )}
                </button>
                <button
                  onClick={() => setPaymentMethod('alipay')}
                  className={`p-4 rounded-xl border-2 transition-all ${
                    paymentMethod === 'alipay'
                      ? 'border-emerald-500 bg-emerald-50'
                      : 'border-slate-200 hover:border-slate-300'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <AlipayIcon size={36} />
                    <div className="text-left">
                      <div className="text-sm font-bold text-slate-900">支付宝</div>
                      <div className="text-xs text-slate-400">便捷支付</div>
                    </div>
                  </div>
                  {paymentMethod === 'alipay' && (
                    <div className="mt-2 text-xs font-bold text-emerald-600">✓ 已选择</div>
                  )}
                </button>
              </div>
            </div>
            
            <Button 
              onClick={handleConfirmUpgrade}
              disabled={actionLoading}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-7 text-lg font-bold shadow-lg shadow-indigo-100 mt-2 disabled:opacity-50"
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
              <div className="flex justify-between text-sm">
                <span className="text-slate-500">计费周期</span>
                <span className="text-slate-900">{paymentRecord.billing_cycle === 'monthly' ? '月付' : '年付'}</span>
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

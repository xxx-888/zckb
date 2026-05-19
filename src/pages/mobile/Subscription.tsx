import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Check, Star, Crown, Zap, CheckCircle2 } from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';

interface Plan {
  id: string;
  name: string;
  price: number;
  period: string;
  icon: React.ElementType;
  color: string;
  isPopular?: boolean;
  features: string[];
}

export const Subscription: React.FC = () => {
  const navigate = useNavigate();
  const { success } = useToast();
  const [currentPlan, setCurrentPlan] = useState('standard');
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState('');

  const plans: Plan[] = [
    {
      id: 'basic',
      name: '基础版',
      price: 0,
      period: '永久免费',
      icon: Star,
      color: 'slate',
      features: [
        '1个店铺管理',
        '基础评价查看',
        '手动回复',
        '基础数据统计'
      ]
    },
    {
      id: 'standard',
      name: '标准版',
      price: 299,
      period: '年',
      icon: Zap,
      color: 'indigo',
      isPopular: true,
      features: [
        '5个店铺管理',
        'AI智能分析',
        '自动回复',
        '竞品对标分析',
        '小红书数据采集',
        '数据导出'
      ]
    },
    {
      id: 'premium',
      name: '旗舰版',
      price: 999,
      period: '年',
      icon: Crown,
      color: 'amber',
      features: [
        '无限店铺管理',
        '高级AI分析',
        '多平台同步',
        '专属客服',
        '定制化报告',
        'API接口权限',
        '团队协作'
      ]
    }
  ];

  const handleUpgrade = (planId: string) => {
    setSelectedPlan(planId);
    setShowUpgradeModal(true);
  };

  const handleConfirmUpgrade = () => {
    setCurrentPlan(selectedPlan);
    setShowUpgradeModal(false);
    success('升级成功', `已成功升级到${plans.find(p => p.id === selectedPlan)?.name}`);
  };

  const currentPlanData = plans.find(p => p.id === currentPlan);

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
                {currentPlanData?.name}
              </h2>
            </div>
            <div className="w-14 h-14 rounded-2xl bg-orange-50 flex items-center justify-center">
              {currentPlanData && React.createElement(currentPlanData.icon, {
                className: "w-7 h-7 text-orange-500"
              })}
            </div>
          </div>
          <div className="flex items-center gap-2 text-slate-500 text-sm">
            <CheckCircle2 className="w-4 h-4 text-emerald-500" />
            <span>
              {currentPlan === 'basic' ? '免费版永久有效' : '有效期至 2027-05-14'}
            </span>
          </div>
        </Card>

        {/* Plans */}
        <div className="space-y-4">
          <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-1">选择版本</h4>
          
          {plans.map((plan) => {
            const IconComponent = plan.icon;
            return (
              <div 
                key={plan.id}
                className={`bg-white rounded-2xl p-6 shadow-sm relative ${
                  plan.isPopular ? 'ring-2 ring-indigo-600' : ''
                }`}
              >
                {plan.isPopular && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-indigo-600 text-white text-xs font-bold px-4 py-1 rounded-full">
                    最受欢迎
                  </div>
                )}

                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-black text-slate-900">{plan.name}</h3>
                    <div className="flex items-baseline gap-1 mt-2">
                      <span className="text-3xl font-black text-slate-900">
                        {plan.price === 0 ? '免费' : `¥${plan.price}`}
                      </span>
                      {plan.price > 0 && (
                        <span className="text-sm text-slate-400">/{plan.period}</span>
                      )}
                    </div>
                  </div>
                  <div className={`bg-${plan.color}-50 p-3 rounded-2xl`}>
                    <IconComponent className={`w-6 h-6 text-${plan.color}-600`} />
                  </div>
                </div>

                <div className="space-y-3 mb-6">
                  {plan.features.map((feature, idx) => (
                    <div key={idx} className="flex items-center gap-3">
                      <Check className={`w-4 h-4 text-${plan.color}-600 flex-shrink-0`} />
                      <span className="text-sm text-slate-700">{feature}</span>
                    </div>
                  ))}
                </div>

                {currentPlan === plan.id ? (
                  <Button 
                    disabled
                    className="w-full bg-slate-100 text-slate-400 rounded-2xl py-6 font-bold cursor-not-allowed"
                  >
                    <CheckCircle2 className="w-5 h-5 mr-2" />
                    当前版本
                  </Button>
                ) : (
                  <Button 
                    onClick={() => handleUpgrade(plan.id)}
                    className={`w-full rounded-2xl py-6 text-lg font-bold ${
                      plan.isPopular
                        ? 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-xl shadow-indigo-100'
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
        <div className="space-y-3">
          <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-1">订阅记录</h4>
          <div className="bg-white rounded-2xl overflow-hidden shadow-sm">
            <div className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-bold text-slate-900">标准版</p>
                  <p className="text-xs text-slate-400 mt-1">2026-05-14 购买</p>
                </div>
                <span className="text-sm font-bold text-green-600">¥299/年</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Upgrade Modal */}
      {showUpgradeModal && (
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
                {plans.find(p => p.id === selectedPlan)?.name}
              </h3>
              <p className="text-2xl font-black text-slate-900 mt-2">
                ¥{plans.find(p => p.id === selectedPlan)?.price}
                <span className="text-sm font-normal text-slate-400">/{plans.find(p => p.id === selectedPlan)?.period}</span>
              </p>
            </div>

            <div className="space-y-2">
              <p className="text-xs font-bold text-slate-500 uppercase tracking-wider">包含功能：</p>
              {plans.find(p => p.id === selectedPlan)?.features.map((feature, idx) => (
                <div key={idx} className="flex items-center gap-3">
                  <Check className="w-4 h-4 text-indigo-600 flex-shrink-0" />
                  <span className="text-sm text-slate-700">{feature}</span>
                </div>
              ))}
            </div>

            <Button 
              onClick={handleConfirmUpgrade}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-7 text-lg font-bold shadow-xl shadow-indigo-100"
            >
              确认支付
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

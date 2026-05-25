import React, { createContext, useContext, useState, useEffect, useCallback, useMemo, ReactNode } from 'react';
import { subscriptionApi, type UserSubscription } from '@/api/subscription';

interface SubscriptionContextType {
  subscription: UserSubscription | null;
  loading: boolean;
  error: Error | null;
  hasValidSubscription: boolean;
  refetch: () => void;
}

const SubscriptionContext = createContext<SubscriptionContextType | undefined>(undefined);

export function SubscriptionProvider({ children }: { children: ReactNode }) {
  const [subscription, setSubscription] = useState<UserSubscription | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const hasValidSubscription = useMemo(() => {
    return !!subscription && ['trial', 'active'].includes(subscription.status);
  }, [subscription]);

  const fetchSubscription = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await subscriptionApi.getCurrentSubscription();
      setSubscription(data);
    } catch (err: any) {
      if (err?.status === 401 || err?.status === 404) {
        setSubscription(null);
      } else {
        setError(err instanceof Error ? err : new Error('获取订阅信息失败'));
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchSubscription();
  }, [fetchSubscription]);

  return (
    <SubscriptionContext.Provider value={{
      subscription,
      loading,
      error,
      hasValidSubscription,
      refetch: fetchSubscription,
    }}>
      {children}
    </SubscriptionContext.Provider>
  );
}

export function useSubscription() {
  const context = useContext(SubscriptionContext);
  if (context === undefined) {
    throw new Error('useSubscription must be used within a SubscriptionProvider');
  }
  return context;
}

/**
 * 订阅升级提示组件 Props
 */
interface SubscriptionPromptProps {
  featureName?: string;
  onUpgrade?: () => void;
}

/**
 * 订阅升级提示组件
 * 当没有有效订阅时显示
 */
export function SubscriptionPrompt({ 
  featureName = '此功能', 
  onUpgrade 
}: SubscriptionPromptProps) {
  const handleUpgrade = () => {
    if (onUpgrade) {
      onUpgrade();
    } else {
      window.location.href = '/mobile/subscription';
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6">
      <div className="w-full max-w-sm bg-white rounded-3xl shadow-xl shadow-slate-200/50 p-8 text-center">
        {/* 图标 */}
        <div className="w-20 h-20 bg-gradient-to-br from-amber-400 to-orange-500 rounded-2xl mx-auto mb-6 flex items-center justify-center shadow-lg shadow-amber-200/50">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" fill="white" stroke="none" />
          </svg>
        </div>

        {/* 标题 */}
        <h2 className="text-xl font-black text-slate-900 mb-2">
          订阅 required
        </h2>

        {/* 描述 */}
        <p className="text-sm text-slate-500 mb-8 leading-relaxed">
          {featureName}需要有效订阅才能使用。请升级您的套餐以继续使用。
        </p>

        {/* 升级按钮 */}
        <button
          onClick={handleUpgrade}
          className="w-full h-12 bg-gradient-to-r from-emerald-500 to-teal-600 text-white text-sm font-bold rounded-xl hover:from-emerald-600 hover:to-teal-700 transition-all shadow-lg shadow-emerald-200/50 active:scale-[0.98]"
        >
          查看订阅方案
        </button>

        {/* 返回按钮 */}
        <button
          onClick={() => window.history.back()}
          className="w-full h-12 bg-slate-100 text-slate-600 text-sm font-bold rounded-xl hover:bg-slate-200 transition-all mt-3"
        >
          返回
        </button>
      </div>
    </div>
  );
}

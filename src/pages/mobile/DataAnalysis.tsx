import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  Wallet,
  Package,
  Store,
  TrendingUp,
} from 'lucide-react';
import { cn } from '../../lib/utils';
import { MobileLayout } from '../../components/MobileLayout';
import { RevenueAnalysis } from './RevenueAnalysis';
import { PackageAnalysisTab } from './PackageAnalysisTab';
import { StoreAnalysis } from './StoreAnalysis';

const tabs = [
  { key: 'revenue', label: '营业额分析', icon: Wallet, color: 'text-orange-500' },
  { key: 'package', label: '套餐分析', icon: Package, color: 'text-indigo-500' },
  { key: 'store', label: '门店分析', icon: Store, color: 'text-emerald-500' },
];

export const DataAnalysis: React.FC = () => {
  const [searchParams] = useSearchParams();
  const initialTab = searchParams.get('tab') || 'revenue';
  const [activeTab, setActiveTab] = useState(initialTab);

  return (
    <MobileLayout title="数据分析">
      <div className="pb-24 space-y-4">
        {/* Tab 栏 */}
        <div className="bg-white rounded-2xl p-1.5 flex gap-1 shadow-sm border border-slate-100">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={cn(
                "flex-1 flex items-center justify-center gap-1.5 py-2.5 rounded-xl text-xs font-bold transition-all duration-200",
                activeTab === tab.key
                  ? "bg-slate-900 text-white shadow-sm"
                  : "text-slate-500 hover:text-slate-700 hover:bg-slate-50"
              )}
            >
              <tab.icon className={cn("w-4 h-4", activeTab === tab.key ? "text-white" : tab.color)} />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab 内容 */}
        {activeTab === 'revenue' && <RevenueAnalysis />}
        {activeTab === 'package' && <PackageAnalysisTab />}
        {activeTab === 'store' && <StoreAnalysis />}
      </div>
    </MobileLayout>
  );
};

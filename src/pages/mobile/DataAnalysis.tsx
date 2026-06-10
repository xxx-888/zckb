import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  Wallet,
  Package,
  Store,
  Calendar,
  ChevronDown,
  CheckCircle2,
} from 'lucide-react';
import { Button } from '../../components/ui/button';
import { cn } from '../../lib/utils';
import { MobileLayout } from '../../components/MobileLayout';
import { RevenueAnalysis } from './RevenueAnalysis';
import { PackageAnalysisTab } from './PackageAnalysisTab';
import { StoreAnalysis } from './StoreAnalysis';
import { useToast } from '../../hooks/use-toast';

const tabs = [
  { key: 'revenue', label: '营业额分析', icon: Wallet, color: 'text-orange-500' },
  { key: 'package', label: '套餐分析', icon: Package, color: 'text-indigo-500' },
  { key: 'store', label: '门店分析', icon: Store, color: 'text-emerald-500' },
];

// ==================== 时间周期 ====================

interface TimeOption { value: string; label: string; dateRange: string; startDate: string; endDate: string; }

function getWeekOptions(): TimeOption[] {
  const now = new Date();
  const formatDate = (d: Date) => `${d.getMonth() + 1}.${d.getDate()}`;
  const toISO = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  const getWeekRange = (weeksAgo: number) => {
    const ref = new Date(now.getTime() - weeksAgo * 7 * 86400000);
    const dayOfWeek = ref.getDay() || 7;
    const monday = new Date(ref.getTime() - (dayOfWeek - 1) * 86400000);
    const sunday = new Date(monday.getTime() + 6 * 86400000);
    return { label: formatDate(monday) + '-' + formatDate(sunday), startDate: toISO(monday), endDate: toISO(sunday) };
  };
  return [
    { value: 'current', label: '本周', dateRange: getWeekRange(0).label, startDate: getWeekRange(0).startDate, endDate: getWeekRange(0).endDate },
    { value: 'last', label: '上周', dateRange: getWeekRange(1).label, startDate: getWeekRange(1).startDate, endDate: getWeekRange(1).endDate },
    { value: 'week2', label: '两周前', dateRange: getWeekRange(2).label, startDate: getWeekRange(2).startDate, endDate: getWeekRange(2).endDate },
    { value: 'week3', label: '三周前', dateRange: getWeekRange(3).label, startDate: getWeekRange(3).startDate, endDate: getWeekRange(3).endDate },
    { value: '4weeks', label: '近4周', dateRange: getWeekRange(3).startDate + '~' + getWeekRange(0).endDate, startDate: getWeekRange(3).startDate, endDate: getWeekRange(0).endDate },
  ];
}

export { type TimeOption };

export const DataAnalysis: React.FC = () => {
  const { success } = useToast();
  const [searchParams] = useSearchParams();
  const initialTab = searchParams.get('tab') || 'revenue';
  const [activeTab, setActiveTab] = useState(initialTab);
  const [timePeriod, setTimePeriodState] = useState(() => localStorage.getItem('zc_time_period') || 'last');
  const [showTimeDropdown, setShowTimeDropdown] = useState(false);
  const dropdownRef = React.useRef<HTMLDivElement>(null);
  const timeOptions = React.useMemo(() => getWeekOptions(), []);
  const activeOption = timeOptions.find(o => o.value === timePeriod) || timeOptions[1];

  const setTimePeriod = (value: string) => {
    setTimePeriodState(value);
    localStorage.setItem('zc_time_period', value);
  };

  const handleTimeChange = (value: string) => {
    setTimePeriod(value);
    setShowTimeDropdown(false);
    success('时间筛选', `已切换到${timeOptions.find(o => o.value === value)?.label}`);
    window.dispatchEvent(new CustomEvent('zc-time-period-changed', { detail: value }));
  };

  // 监听首页时间切换事件，保持同步
  useEffect(() => {
    const handler = (e: CustomEvent<string>) => {
      setTimePeriod(e.detail);
    };
    window.addEventListener('zc-time-period-changed', handler as any);
    return () => window.removeEventListener('zc-time-period-changed', handler as any);
  }, []);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) setShowTimeDropdown(false);
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  return (
    <MobileLayout title="数据分析">
      <div className="pb-24 space-y-4">

        {/* 时间筛选 */}
        <div className="relative" ref={dropdownRef}>
          <div className="flex items-center justify-between bg-white p-3 rounded-2xl shadow-sm border border-slate-100">
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-slate-400" />
              <span className="text-sm font-medium text-slate-600">{activeOption.dateRange}</span>
            </div>
            <Button variant="ghost" size="sm" className="h-8 text-orange-600 font-semibold gap-1"
              onClick={() => setShowTimeDropdown(!showTimeDropdown)}>
              {activeOption.label}
              <ChevronDown className={cn("w-3.5 h-3.5 transition-transform", showTimeDropdown && "rotate-180")} />
            </Button>
          </div>
          {showTimeDropdown && (
            <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-2xl shadow-lg border border-slate-100 z-50 overflow-hidden">
              {timeOptions.map((option) => (
                <button key={option.value}
                  className={cn("w-full px-4 py-3 text-left text-sm font-medium flex items-center justify-between",
                    timePeriod === option.value ? "bg-orange-50 text-orange-600" : "text-slate-700 hover:bg-slate-50")}
                  onClick={() => handleTimeChange(option.value)}>
                  <span>{option.label}</span>
                  <span className="text-[10px] text-slate-400">{option.dateRange}</span>
                  {timePeriod === option.value && <CheckCircle2 className="w-4 h-4 text-orange-600" />}
                </button>
              ))}
            </div>
          )}
        </div>

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

        {/* Tab 内容 - 传递日期参数 */}
        {activeTab === 'revenue' && <RevenueAnalysis startDate={activeOption.startDate} endDate={activeOption.endDate} />}
        {activeTab === 'package' && <PackageAnalysisTab startDate={activeOption.startDate} endDate={activeOption.endDate} />}
        {activeTab === 'store' && <StoreAnalysis startDate={activeOption.startDate} endDate={activeOption.endDate} />}
      </div>
    </MobileLayout>
  );
};

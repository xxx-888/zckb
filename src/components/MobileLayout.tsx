import React, { useState, useEffect, useRef, type ReactNode } from 'react';
import { NavLink, useLocation, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  MessageSquare,
  Brain,
  TrendingUp,
  Settings,
  Bell,
  ChevronDown,
  Building2 as StoreIcon,
  CheckCircle2
} from 'lucide-react';
import { Button } from './ui/button';
import { Avatar } from './ui/avatar';
import { cn } from '../lib/utils';
import { storesApi } from '../api/stores';
import { authApi } from '../api/auth';
import type { Store } from '../api/stores';
import { useStore as useGlobalStore } from '../context/StoreContext';
import { useSubscription } from '../hooks/use-subscription-check';
import { platformsApi } from '../api/platforms';

// ===== 兼容旧 API 的 useStore =====
interface StoreContextValue {
  selectedStore: Store | null;
  setSelectedStore: (store: Store | null) => void;
  storeList: Store[];
}
export const useStore = (): StoreContextValue => {
  const global = useGlobalStore();
  return {
    selectedStore: global.currentStore || null,
    setSelectedStore: (store: Store | null) => {
      if (store) global.setSelectedStoreId(store.id);
    },
    storeList: global.stores,
  };
};

// 路由分组
const routeGroups: Record<string, string[]> = {
  '/mobile': ['/mobile', '/mobile/dashboard', '/mobile/store-list', '/mobile/store-detail'],
  '/mobile/review-stream': ['/mobile/review-stream', '/mobile/review-detail', '/mobile/negative-reply', '/mobile/positive-activation'],
  '/mobile/ai-analysis': ['/mobile/ai-analysis'],
  '/mobile/insights': ['/mobile/insights', '/mobile/competitor-analysis', '/mobile/dish-elimination', '/mobile/traceability-detail', '/mobile/annual-report'],
  '/mobile/settings': ['/mobile/settings', '/mobile/store-settings', '/mobile/reply-template', '/mobile/platform-connection', '/mobile/notification-settings', '/mobile/auto-reply-settings', '/mobile/help-center', '/mobile/subscription']
};

interface MobileLayoutProps {
  children: ReactNode;
  title?: string;
}

const navItems = [
  { icon: LayoutDashboard, label: '首页', path: '/mobile' },
  { icon: MessageSquare, label: '评论', path: '/mobile/review-stream' },
  { icon: Brain, label: 'AI', path: '/mobile/ai-analysis' },
  { icon: TrendingUp, label: '洞察', path: '/mobile/insights' },
  { icon: Settings, label: '我的', path: '/mobile/settings' },
];

export const MobileLayout: React.FC<MobileLayoutProps> = ({ children, title }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const [isStoreMenuOpen, setIsStoreMenuOpen] = useState(false);

  // 使用全局 StoreContext
  const {
    stores,
    currentStore,
    selectedStoreId,
    setSelectedStoreId,
    loading: storeLoading,
    refresh,
  } = useGlobalStore();

  // 订阅状态
  const { hasValidSubscription, loading: subLoading } = useSubscription();

  // 平台账号绑定状态
  const [hasPlatformAccount, setHasPlatformAccount] = useState(false);
  const [accountCheckDone, setAccountCheckDone] = useState(false);
  // 用 ref 标记账号检查是否正在进行，避免与重定向 useEffect 竞态
  const checkingRef = useRef(false);

  const noStore = stores.length === 0;
  const isBindPage = location.pathname === '/mobile/platform-connection';

  // 获取平台账号状态
  useEffect(() => {
    if (!hasValidSubscription) {
      setHasPlatformAccount(false);
      setAccountCheckDone(true);
      return;
    }
    // 订阅有效时，先重置为未完成，再发起异步检查
    // 同步设置 ref 防止重定向 useEffect 竞态抢跑
    setAccountCheckDone(false);
    checkingRef.current = true;
    const checkPlatformAccounts = async () => {
      try {
        const data = await platformsApi.getAccounts();
        console.log('[MobileLayout] getAccounts 返回:', data);
        setHasPlatformAccount(data.length > 0);
      } catch (err: any) {
        console.error('[MobileLayout] getAccounts 失败:', err);
        setHasPlatformAccount(false);
      } finally {
        checkingRef.current = false;
        setAccountCheckDone(true);
      }
    };
    checkPlatformAccounts();
  }, [hasValidSubscription]);

  // 有订阅但无平台账号、无门店且不在绑定页 → 重定向
  // 用 checkingRef 防止与账号检查 useEffect 的竞态（React 批量执行同周期 effect）
  useEffect(() => {
    // 账号检查正在异步进行中，不执行重定向判断（防止竞态抢跑）
    if (checkingRef.current) return;
    console.log('[MobileLayout] 重定向检查:', {
      subLoading, accountCheckDone, hasValidSubscription, hasPlatformAccount, isBindPage, noStore,
    });
    if (!subLoading && accountCheckDone && hasValidSubscription && !hasPlatformAccount && !isBindPage && noStore) {
      console.log('[MobileLayout] 重定向到绑定页');
      navigate('/mobile/platform-connection', { replace: true });
    }
  }, [subLoading, accountCheckDone, hasValidSubscription, hasPlatformAccount, isBindPage, noStore]);

  // 未绑定店铺 → 跳转绑定页
  const handleNoStore = () => {
    navigate('/mobile/platform-connection');
  };

  // 切换回首页时自动刷新店铺列表
  useEffect(() => {
    if (location.pathname === '/mobile' || location.pathname === '/mobile/dashboard') {
      refresh();
    }
  }, [location.pathname, refresh]);

  // 判断当前路由是否属于某个导航项
  const isRouteActive = (path: string): boolean => {
    const routes = routeGroups[path];
    if (!routes) return location.pathname === path;
    if (path === '/mobile') {
      return location.pathname === '/mobile' || location.pathname === '/mobile/dashboard';
    }
    return routes.some(route => {
      if (location.pathname === route) return true;
      if (location.pathname.startsWith(route + '/')) return true;
      return false;
    });
  };

  const handleStoreSelect = (store: Store) => {
    setSelectedStoreId(store.id);
    setIsStoreMenuOpen(false);
  };

  return (
    <div className="flex flex-col h-screen bg-slate-50 font-sans text-slate-900 overflow-hidden">
      {/* Mobile Top Header */}
      <header className="safe-top bg-white border-b border-slate-100 px-4 h-16 flex items-center justify-between flex-shrink-0 z-30 relative">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 bg-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-100">
            <Brain className="text-white w-5 h-5" />
          </div>
          <div className="flex flex-col min-w-0">
            <h1 className="font-bold text-sm tracking-tight text-slate-400 leading-none mb-1">智策口碑</h1>

            {noStore ? (
              <button
                onClick={handleNoStore}
                className="text-amber-500 font-medium text-sm leading-none hover:underline truncate max-w-[180px]"
              >
                未绑定店铺
              </button>
            ) : stores.length > 1 ? (
              <button
                onClick={() => setIsStoreMenuOpen(!isStoreMenuOpen)}
                className="flex items-center gap-1 text-slate-900 font-bold text-base leading-none group min-w-0"
              >
                <span className="truncate max-w-[180px]">
                  {currentStore?.name || (storeLoading ? '加载中...' : '请选择店铺')}
                </span>
                <ChevronDown className={cn("w-4 h-4 text-slate-400 transition-transform flex-shrink-0", isStoreMenuOpen && "rotate-180")} />
              </button>
            ) : (
              <span className="text-slate-900 font-bold text-base leading-none truncate max-w-[180px]">
                {currentStore?.name || '加载中...'}
              </span>
            )}
          </div>
        </div>

        <div className="flex items-center gap-1">
          <Button variant="ghost" size="icon" className="text-slate-500 w-9 h-9 rounded-full">
            <Bell className="w-5 h-5" />
            <span className="absolute top-2 right-2 w-2 h-2 bg-rose-500 rounded-full border-2 border-white"></span>
          </Button>
          <Avatar className="w-8 h-8 border-2 border-slate-100 ml-1">
            <img src={`https://modao.cc/agent-py/media/generated_images/2026-05-08/663c5bb953c14b82af1394420b59cb55.jpg#desc=%24}`} alt="User Avatar" />
          </Avatar>
        </div>

        {/* Store Switcher Dropdown */}
        {isStoreMenuOpen && (
          <>
            <div
              className="fixed inset-0 bg-black/20 z-40"
              onClick={() => setIsStoreMenuOpen(false)}
            />
            <div className="absolute top-full left-0 right-0 bg-white border-b border-slate-100 shadow-xl z-50 animate-in slide-in-from-top-2 duration-200">
              {noStore ? (
                <div className="p-6 text-center">
                  <StoreIcon className="w-10 h-10 text-amber-400 mx-auto mb-3" />
                  <p className="text-sm font-bold text-amber-900 mb-1">暂无绑定店铺</p>
                  <p className="text-xs text-sber-600 mb-4">绑定店铺后即可查看评价数据</p>
                  <Button
                    size="sm"
                    className="bg-orange-500 hover:bg-orange-600 text-white"
                    onClick={() => { setIsStoreMenuOpen(false); navigate('/mobile/platform-connection'); }}
                  >
                    去绑定店铺
                  </Button>
                </div>
              ) : (
                <div className="p-4 grid grid-cols-1 gap-1 max-h-[60vh] overflow-y-auto">
                  <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2 px-2">切换门店 ({stores.length})</p>
                  {stores.map(store => (
                    <button
                      key={store.id}
                      onClick={() => handleStoreSelect(store)}
                      className={cn(
                        "flex items-center justify-between p-3 rounded-xl transition-colors text-left",
                        selectedStoreId === store.id ? "bg-indigo-50 text-indigo-700" : "hover:bg-slate-50 text-slate-700"
                      )}
                    >
                      <div className="flex items-center gap-3">
                        <div className={cn(
                          "p-2 rounded-lg",
                          selectedStoreId === store.id ? "bg-indigo-100 text-indigo-600" : "bg-slate-100 text-slate-400"
                        )}>
                          <StoreIcon className="w-4 h-4" />
                        </div>
                        <div className="flex flex-col">
                          <span className="font-semibold text-sm">{store.name}</span>
                          {store.status !== 'active' && (
                            <span className="text-[10px] text-amber-600 mt-0.5">
                              {store.status === 'pending' ? '审核中' : '未激活'}
                            </span>
                          )}
                        </div>
                      </div>
                      {selectedStoreId === store.id && (
                        <CheckCircle2 className="w-5 h-5 text-indigo-600" />
                      )}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </>
        )}
      </header>

      {/* Main Content Area */}
      <main className="flex-1 overflow-y-auto pb-24">
        <div className="container px-4 max-w-md mx-auto pt-4">
          {children}
        </div>
      </main>

      {/* Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-slate-100 z-30 pb-safe">
        <div className="flex items-center justify-around h-16 max-w-md mx-auto">
          {navItems.map((item) => {
            const isActive = isRouteActive(item.path);
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={cn(
                  "flex flex-col items-center justify-center flex-1 h-full gap-1 transition-all duration-200",
                  isActive ? "text-indigo-600" : "text-slate-400 hover:text-slate-600"
                )}
              >
                <item.icon className={cn("w-5 h-5 transition-all duration-200", isActive && "stroke-[2.5]")} />
                <span className={cn("text-[10px] font-bold transition-all duration-200", isActive && "scale-105")}>
                  {item.label}
                </span>
                {isActive && (
                  <div className="absolute bottom-1 w-1 h-1 bg-indigo-600 rounded-full" />
                )}
              </NavLink>
            );
          })}
        </div>
      </nav>
    </div>
  );
};

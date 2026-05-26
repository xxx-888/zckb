import React, { useState, useEffect, createContext, useContext, type ReactNode } from 'react';
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
import { Badge } from './ui/badge';
import { cn } from '../lib/utils';
import { storesApi } from '../api/stores';
import { authApi } from '../api/auth';
import type { Store } from '../api/stores';

// ===== StoreContext：向子页面共享选中店铺 =====
interface StoreContextValue {
  selectedStore: Store | null;
  setSelectedStore: (store: Store | null) => void;
  storeList: Store[];
}
export const StoreContext = createContext<StoreContextValue | null>(null);
export const useStore = (): StoreContextValue => {
  const ctx = useContext(StoreContext);
  if (!ctx) {
    // 优雅降级：返回默认值，不抛异常
    return {
      selectedStore: null,
      setSelectedStore: () => {},
      storeList: [],
    };
  }
  return ctx;
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
  const [storeList, setStoreList] = useState<Store[]>([]);
  const [selectedStore, setSelectedStore] = useState<Store | null>(null);
  const [isStoreMenuOpen, setIsStoreMenuOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [noStore, setNoStore] = useState(false);

  // 获取店铺列表（通过接口）
  useEffect(() => {
    const fetchStores = async () => {
      try {
        setLoading(true);
        const res = await storesApi.getStores({ page_size: 100 });
        const stores = res.items || [];
        setStoreList(stores);
        if (stores.length === 0) {
          setNoStore(true);
          setSelectedStore(null);
        } else {
          setNoStore(false);
          // 优先从 localStorage 恢复上次选中的门店
          const savedId = localStorage.getItem('zc_selected_store_id');
          const savedStore = savedId ? stores.find(s => s.id === savedId) : null;
          if (savedStore) {
            setSelectedStore(savedStore);
          } else if (!selectedStore || !stores.find(s => s.id === selectedStore.id)) {
            setSelectedStore(stores[0]);
          }
        }
      } catch (err) {
        console.warn('[MobileLayout] 获取店铺列表失败:', err);
        setNoStore(true);
      } finally {
        setLoading(false);
      }
    };
    fetchStores();
  }, []);

  // 模拟绑定店铺（自动创建测试数据）
  const handleMockBind = async () => {
    try {
      setLoading(true);
      const mockStores = [
        { name: '王府井总店', type: 'restaurant', status: 'active' as const, platform_count: 2, review_count: 586 },
        { name: '国贸分店', type: 'restaurant', status: 'active' as const, platform_count: 1, review_count: 423 },
        { name: '三里屯旗舰店', type: 'restaurant', status: 'pending' as const, platform_count: 0, review_count: 0 },
      ];
      await Promise.all(
        mockStores.map(s => storesApi.createStore(s))
      );
      // 重新获取店铺列表（后端应在 createStore 时自动关联当前用户）
      const res = await storesApi.getStores({ page_size: 100 });
      const stores = res.items || [];
      setStoreList(stores);
      setNoStore(stores.length === 0);
      if (stores.length > 0) { 
        setSelectedStore(stores[0]);
        localStorage.setItem('zc_selected_store_id', stores[0].id);
      }
    } catch (err) {
      console.error('[MobileLayout] 模拟绑定失败:', err);
    } finally {
      setLoading(false);
    }
  };

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
    setSelectedStore(store);
    localStorage.setItem('zc_selected_store_id', store.id);
    setIsStoreMenuOpen(false);
    // 触发自定义事件，通知所有页面店铺已切换
    window.dispatchEvent(new CustomEvent('zc-store-changed', { detail: store }));
  };

  const contextValue: StoreContextValue = {
    selectedStore,
    setSelectedStore,
    storeList,
  };

  return (
    <StoreContext.Provider value={contextValue}>
      <div className="flex flex-col h-screen bg-slate-50 font-sans text-slate-900 overflow-hidden">
        {/* Mobile Top Header */}
        <header className="safe-top bg-white border-b border-slate-100 px-4 h-16 flex items-center justify-between flex-shrink-0 z-30 relative">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-100">
              <Brain className="text-white w-5 h-5" />
            </div>
            <div className="flex flex-col">
              <h1 className="font-bold text-sm tracking-tight text-slate-400 leading-none mb-1">智策口碑</h1>

              {noStore ? (
                <button
                  onClick={handleMockBind}
                  className="text-amber-500 font-medium text-sm leading-none hover:underline"
                >
                  未绑定店铺
                </button>
              ) : storeList.length > 1 ? (
                <button
                  onClick={() => setIsStoreMenuOpen(!isStoreMenuOpen)}
                  className="flex items-center gap-1 text-slate-900 font-bold text-base leading-none group"
                >
                  {selectedStore?.name || (loading ? '加载中...' : '请选择店铺')}
                  <ChevronDown className={cn("w-4 h-4 text-slate-400 transition-transform", isStoreMenuOpen && "rotate-180")} />
                </button>
              ) : (
                <span className="text-slate-900 font-bold text-base leading-none">
                  {selectedStore?.name || '加载中...'}
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
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2 px-2">切换门店 ({storeList.length})</p>
                    {storeList.map(store => (
                      <button
                        key={store.id}
                        onClick={() => handleStoreSelect(store)}
                        className={cn(
                          "flex items-center justify-between p-3 rounded-xl transition-colors text-left",
                          selectedStore?.id === store.id ? "bg-indigo-50 text-indigo-700" : "hover:bg-slate-50 text-slate-700"
                        )}
                      >
                        <div className="flex items-center gap-3">
                          <div className={cn(
                            "p-2 rounded-lg",
                            selectedStore?.id === store.id ? "bg-indigo-100 text-indigo-600" : "bg-slate-100 text-slate-400"
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
                        {selectedStore?.id === store.id && (
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
        <nav className="safe-bottom fixed bottom-0 left-0 right-0 bg-white/90 backdrop-blur-xl border-t border-slate-100 px-2 py-2 flex items-center justify-around z-30 shadow-[0_-4px_20px_rgba(0,0,0,0.03)]">
          {navItems.map((item) => {
            const isActive = isRouteActive(item.path);
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={cn(
                  "flex flex-col items-center gap-1.5 px-4 py-1 rounded-2xl transition-all duration-300 relative",
                  isActive ? "text-indigo-600" : "text-slate-400 hover:text-slate-600"
                )}
              >
                <item.icon className={cn("w-6 h-6 transition-transform duration-300", isActive && "scale-110")} />
                <span className="text-[10px] font-bold tracking-tight">{item.label}</span>
                {isActive && (
                  <span className="absolute -bottom-1 w-1 h-1 bg-indigo-600 rounded-full" />
                )}
              </NavLink>
            );
          })}
        </nav>
      </div>
    </StoreContext.Provider>
  );
};

import React, { useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  MessageSquare, 
  Brain, 
  TrendingUp, 
  Settings,
  Bell,
  Search,
  ChevronDown,
  Store
} from 'lucide-react';
import { Button } from './ui/button';
import { Avatar } from './ui/avatar';
import { Badge } from './ui/badge';
import { cn } from '../lib/utils';
import { currentUser, mockStores } from '../lib/mockData';

// 路由分组：定义每个导航项匹配哪些路径
const routeGroups: Record<string, string[]> = {
  '/mobile': [
    '/mobile',
    '/mobile/dashboard',
    '/mobile/store-list',
    '/mobile/store-detail'
  ],
  '/mobile/review-stream': [
    '/mobile/review-stream',
    '/mobile/review-detail',
    '/mobile/negative-reply',
    '/mobile/positive-activation'
  ],
  '/mobile/ai-analysis': [
    '/mobile/ai-analysis'
  ],
  '/mobile/insights': [
    '/mobile/insights',
    '/mobile/competitor-analysis',
    '/mobile/dish-elimination',
    '/mobile/traceability-detail',
    '/mobile/annual-report'
  ],
  '/mobile/settings': [
    '/mobile/settings',
    '/mobile/store-settings',
    '/mobile/reply-template',
    '/mobile/platform-connection',
    '/mobile/notification-settings',
    '/mobile/auto-reply-settings',
    '/mobile/help-center',
    '/mobile/subscription'
  ]
};

interface MobileLayoutProps {
  children: React.ReactNode;
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
  const [selectedStoreId, setSelectedStoreId] = useState(currentUser.assignedStores[0]);
  const [isStoreMenuOpen, setIsStoreMenuOpen] = useState(false);

  // 判断当前路由是否属于某个导航项
  const isRouteActive = (path: string): boolean => {
    const routes = routeGroups[path];
    if (!routes) return location.pathname === path;
    
    // 特殊处理：首页只精确匹配，避免匹配所有 /mobile 开头的路径
    if (path === '/mobile') {
      return location.pathname === '/mobile' || location.pathname === '/mobile/dashboard';
    }
    
    return routes.some(route => {
      // 使用 startsWith 但要确保完整匹配路径段
      if (location.pathname === route) return true;
      if (location.pathname.startsWith(route + '/')) return true;
      return false;
    });
  };

  const currentStore = mockStores.find(s => s.id === selectedStoreId);
  const showStoreSwitcher = currentUser.role === 'HQ' || currentUser.role === 'OPERATOR';

  const accessibleStores = mockStores.filter(s => currentUser.assignedStores.includes(s.id));

  return (
    <div className="flex flex-col h-screen bg-slate-50 font-sans text-slate-900 overflow-hidden">
      {/* Mobile Top Header */}
      <header className="safe-top bg-white border-b border-slate-100 px-4 h-16 flex items-center justify-between flex-shrink-0 z-30 relative">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 bg-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-100">
            <Brain className="text-white w-5 h-5" />
          </div>
          <div className="flex flex-col">
            <h1 className="font-bold text-sm tracking-tight text-slate-400 leading-none mb-1">智策口碑</h1>
            
            {showStoreSwitcher ? (
              <button 
                onClick={() => setIsStoreMenuOpen(!isStoreMenuOpen)}
                className="flex items-center gap-1 text-slate-900 font-bold text-base leading-none group"
              >
                {currentStore?.name}
                <ChevronDown className={cn("w-4 h-4 text-slate-400 transition-transform", isStoreMenuOpen && "rotate-180")} />
              </button>
            ) : (
              <span className="text-slate-900 font-bold text-base leading-none">
                {currentStore?.name}
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
        {isStoreMenuOpen && showStoreSwitcher && (
          <>
            <div 
              className="fixed inset-0 bg-black/20 z-40" 
              onClick={() => setIsStoreMenuOpen(false)}
            />
            <div className="absolute top-full left-0 right-0 bg-white border-b border-slate-100 shadow-xl z-50 animate-in slide-in-from-top-2 duration-200">
              <div className="p-4 grid grid-cols-1 gap-1 max-h-[60vh] overflow-y-auto">
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2 px-2">切换门店 ({accessibleStores.length})</p>
                {accessibleStores.map(store => (
                  <button
                    key={store.id}
                    onClick={() => {
                      setSelectedStoreId(store.id);
                      setIsStoreMenuOpen(false);
                    }}
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
                        <Store className="w-4 h-4" />
                      </div>
                      <span className="font-semibold text-sm">{store.name}</span>
                    </div>
                    {selectedStoreId === store.id && (
                      <div className="w-2 h-2 rounded-full bg-indigo-600" />
                    )}
                  </button>
                ))}
              </div>
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
      <nav className="safe-bottom fixed bottom-0 left-0 right-0 bg-white/90 backdrop-blur-xl border-t border-slate-100 px-2 py-2 flex items-center justify-around z-30 shadow-[0_-4px_20px_rgba(0,0,0,0,03)]">
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
  );
};

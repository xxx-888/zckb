import React, { useState } from 'react';
import { NavLink, useNavigate, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Users, 
  Store, 
  MessageSquare, 
  Settings2, 
  ShieldCheck, 
  FileCheck,
  LogOut,
  Bell,
  Search,
  Menu,
  ChevronRight,
  Monitor,
  Target,
  Sparkles,
  AlertCircle,
  Star,
  BarChart3,
  Brain,
  Smartphone
} from 'lucide-react';
import { Button } from './ui/button';
import { Avatar } from './ui/avatar';
import { Badge } from './ui/badge';
import { cn } from '../lib/utils';

interface AdminLayoutProps {
  children: React.ReactNode;
}

const adminNavItems = [
  { icon: LayoutDashboard, label: '概览', path: '/admin/dashboard' },
  { icon: Store, label: '店铺管理', path: '/admin/store-management' },
  { icon: MessageSquare, label: '评论管理', path: '/admin/review-management' },
  { icon: AlertCircle, label: '差评处理', path: '/admin/negative-reply' },
  { icon: Star, label: '好评激活', path: '/admin/positive-activation' },
  { icon: BarChart3, label: '经营洞察', path: '/admin/insights' },
  { icon: Brain, label: 'AI分析', path: '/admin/ai-analysis' },
  { icon: Smartphone, label: '移动端设置', path: '/admin/mobile-settings' },
  { icon: Target, label: '竞品对标', path: '/admin/competitor-analysis' },
  { icon: Sparkles, label: '小红书分析', path: '/admin/xiaohongshu-analysis' },
  { icon: ShieldCheck, label: '权限管理', path: '/admin/permission-management' },
  { icon: Monitor, label: '爬虫管理', path: '/admin/spider-management' },
  { icon: Settings2, label: 'AI配置', path: '/admin/ai-config' },
  { icon: FileCheck, label: '回复审核', path: '/admin/reply-audit' },
  { icon: Bell, label: '通知配置', path: '/admin/notification-config' },
];

export const AdminLayout: React.FC<AdminLayoutProps> = ({ children }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    navigate('/admin');
  };

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden font-sans text-slate-900">
      {/* Admin Sidebar */}
      <aside 
        className={cn(
          "bg-slate-900 text-slate-300 transition-all duration-300 flex flex-col z-30",
          isSidebarOpen ? "w-64" : "w-20"
        )}
      >
        <div className="p-6 flex items-center gap-3">
          <div className="w-8 h-8 bg-amber-500 rounded-lg flex items-center justify-center flex-shrink-0">
            <Settings2 className="text-white w-5 h-5" />
          </div>
          {isSidebarOpen && <h1 className="font-bold text-lg text-white tracking-tight truncate">智策后台</h1>}
        </div>

        <nav className="flex-1 px-3 space-y-1 mt-4">
          {adminNavItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 group",
                isActive 
                  ? "bg-amber-500 text-white font-medium" 
                  : "hover:bg-slate-800 hover:text-white"
              )}
            >
              <item.icon className={cn(
                "w-5 h-5 flex-shrink-0",
                location.pathname === item.path ? "text-white" : "text-slate-400 group-hover:text-white"
              )} />
              {isSidebarOpen && <span>{item.label}</span>}
              {location.pathname === item.path && isSidebarOpen && <ChevronRight className="ml-auto w-4 h-4 opacity-50" />}
            </NavLink>
          ))}
        </nav>

        <div className="p-4 border-t border-slate-800">
          <Button 
            variant="ghost" 
            className={cn("w-full justify-start text-slate-400 hover:text-white hover:bg-slate-800", !isSidebarOpen && "px-2")}
            onClick={handleLogout}
          >
            <LogOut className="w-5 h-5 flex-shrink-0" />
            {isSidebarOpen && <span className="ml-3">退出后台</span>}
          </Button>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Admin Topbar */}
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 z-10 shadow-sm">
          <div className="flex items-center gap-4">
            <Button 
              variant="ghost" 
              size="icon" 
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="text-slate-500"
            >
              <Menu className="w-5 h-5" />
            </Button>
            <div className="text-sm font-medium text-slate-500">
              系统管理后台 <span className="mx-2 text-slate-300">|</span> 2026年05月09日
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="relative">
              <Button variant="ghost" size="icon" className="text-slate-500">
                <Bell className="w-5 h-5" />
              </Button>
              <Badge className="absolute -top-1 -right-1 px-1.5 py-0.5 bg-rose-500 text-[10px] min-w-[18px] border-2 border-white">
                12
              </Badge>
            </div>
            
            <div className="h-8 w-[1px] bg-slate-200 mx-1"></div>

            <div className="flex items-center gap-3">
              <div className="text-right hidden sm:block">
                <p className="text-sm font-semibold text-slate-900">超级管理员</p>
                <p className="text-xs text-slate-400">系统维护中心</p>
              </div>
              <Avatar className="h-9 w-9 border border-slate-200">
                <img src="https://modao.cc/agent-py/media/generated_images/2026-05-08/fe4192b57d004bbca9236f5dddf78868.jpg#desc=Admin%20Avatar" alt="Admin" className="object-cover" />
              </Avatar>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <main className="flex-1 overflow-y-auto bg-slate-100 p-8">
          {children}
        </main>
      </div>
    </div>
  );
};

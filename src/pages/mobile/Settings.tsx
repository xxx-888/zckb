import React, { useState, useEffect } from 'react';
import { 
  Settings as SettingsIcon, 
  User, 
  Bell, 
  Shield, 
  HelpCircle, 
  LogOut,
  ChevronRight,
  Store,
  CreditCard,
  MessageSquare,
  Smartphone
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Avatar } from '../../components/ui/avatar';
import { Badge } from '../../components/ui/badge';
import { MobileLayout } from '../../components/MobileLayout';
import { useNavigate } from 'react-router-dom';
import { authApi, UserInfo } from '../../api/auth';
import { useToast } from '../../hooks/use-toast';

export const Settings: React.FC = () => {
  const navigate = useNavigate();
  const { success, error } = useToast();
  const [user, setUser] = useState<UserInfo | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 尝试从本地存储获取用户信息
    const storedUser = authApi.getStoredUser();
    if (storedUser) {
      setUser(storedUser);
    }
    
    // 异步获取最新用户信息
    authApi.getCurrentUser()
      .then(userInfo => {
        setUser(userInfo);
        localStorage.setItem('user_info', JSON.stringify(userInfo));
      })
      .catch(err => {
        console.error('获取用户信息失败:', err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const handleLogout = async () => {
    try {
      await authApi.logout();
      success('退出成功', '已安全退出登录');
      navigate('/mobile/login');
    } catch (err: any) {
      error('退出失败', err.message || '退出登录时出现错误');
      // 即使API调用失败也清除本地存储并跳转
      navigate('/mobile/login');
    }
  };

  const sections = [
    {
      title: '店铺管理',
      items: [
        { icon: Store, label: '店铺信息设置', value: user?.role === 'STORE' ? '门店账号' : '总部账号', path: '/mobile/store-settings' },
        { icon: MessageSquare, label: '回复模板配置', value: '查看模板', path: '/mobile/reply-template' },
        { icon: Smartphone, label: '多平台账号关联', value: '管理平台', path: '/mobile/platform-connection' },
      ]
    },
    {
      title: '偏好设置',
      items: [
        { icon: Bell, label: '消息通知', value: '通知设置', path: '/mobile/notification-settings' },
        { icon: Shield, label: '自动回复策略', value: '回复策略', path: '/mobile/auto-reply-settings' },
      ]
    },
    {
      title: '其他',
      items: [
        { icon: HelpCircle, label: '帮助中心', value: '', path: '/mobile/help-center' },
        { icon: CreditCard, label: '版本订阅', value: '查看套餐', path: '/mobile/subscription' },
      ]
    }
  ];

  const getRoleBadge = (role: string) => {
    switch (role) {
      case 'HQ':
        return '超级管理员权限';
      case 'OPERATOR':
        return '运营管理员权限';
      case 'STORE':
        return '门店管理员权限';
      default:
        return '普通用户权限';
    }
  };

  return (
    <MobileLayout title="我的设置">
      <div className="space-y-6 pb-20 animate-in fade-in slide-in-from-bottom-4 duration-500">
        
        {/* User Profile Header */}
        <div className="flex flex-col items-center py-6">
          {loading ? (
            <div className="w-24 h-24 rounded-full bg-slate-100 animate-pulse mb-4"></div>
          ) : (
            <Avatar className="h-24 w-24 border-4 border-white shadow-xl mb-4">
              <img src={user?.avatar || "https://modao.cc/agent-py/media/generated_images/2026-05-08/9d7953ab82914d99a3152d91b46c75a8.jpg#desc=Manager%20Portrait"} alt="User" className="object-cover" />
            </Avatar>
          )}
          <h3 className="text-xl font-black text-slate-900">{loading ? '加载中...' : (user?.username || '未知用户')}</h3>
          <p className="text-sm text-slate-500 mt-1">{loading ? '加载中...' : (user?.phone || '暂无手机号')}</p>
          <Badge className="mt-3 bg-indigo-50 text-indigo-600 border-none font-bold">
            {loading ? '加载中...' : getRoleBadge(user?.role || '')}
          </Badge>
        </div>

        {/* Setting Groups */}
        {sections.map((section, idx) => (
          <div key={idx} className="space-y-3">
            <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-1">{section.title}</h4>
            <Card className="p-0 border-none shadow-sm overflow-hidden bg-white">
              <div className="divide-y divide-slate-50">
                {section.items.map((item, itemIdx) => (
                  <button 
                    key={itemIdx} 
                    onClick={() => item.path && navigate(item.path)}
                    className="w-full flex items-center justify-between p-4 active:bg-slate-50 transition-colors"
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-8 h-8 rounded-lg bg-slate-50 flex items-center justify-center text-slate-500">
                        <item.icon className="w-4 h-4" />
                      </div>
                      <span className="text-sm font-bold text-slate-700">{item.label}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-slate-400">{item.value}</span>
                      <ChevronRight className="w-4 h-4 text-slate-300" />
                    </div>
                  </button>
                ))}
              </div>
            </Card>
          </div>
        ))}

        {/* Logout Button */}
        <Button 
          variant="outline" 
          className="w-full h-14 rounded-2xl border-rose-100 text-rose-600 font-bold hover:bg-rose-50 hover:text-rose-700 mt-4 transition-all"
          onClick={handleLogout}
        >
          <LogOut className="w-5 h-5 mr-3" /> 退出当前账号
        </Button>

        <p className="text-center text-[10px] text-slate-300 font-medium">
          智策口碑 移动端 v2.4.0 (20260508)
        </p>
      </div>
    </MobileLayout>
  );
};

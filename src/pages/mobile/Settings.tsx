import React from 'react';
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

export const Settings: React.FC = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    navigate('/mobile/login');
  };

  const sections = [
    {
      title: '店铺管理',
      items: [
        { icon: Store, label: '店铺信息设置', value: '香格里拉大酒店...', path: '/mobile/store-settings' },
        { icon: MessageSquare, label: '回复模板配置', value: '3个已启用', path: '/mobile/reply-template' },
        { icon: Smartphone, label: '多平台账号关联', value: '4个已关联', path: '/mobile/platform-connection' },
      ]
    },
    {
      title: '偏好设置',
      items: [
        { icon: Bell, label: '消息通知', value: '开启', path: '/mobile/notification-settings' },
        { icon: Shield, label: '自动回复策略', value: '智能模式', path: '/mobile/auto-reply-settings' },
      ]
    },
    {
      title: '其他',
      items: [
        { icon: HelpCircle, label: '帮助中心', value: '', path: '/mobile/help-center' },
        { icon: CreditCard, label: '版本订阅', value: '标准版', path: '/mobile/subscription' },
      ]
    }
  ];

  return (
    <MobileLayout title="我的设置">
      <div className="space-y-6 pb-20 animate-in fade-in slide-in-from-bottom-4 duration-500">
        
        {/* User Profile Header */}
        <div className="flex flex-col items-center py-6">
          <Avatar className="h-24 w-24 border-4 border-white shadow-xl mb-4">
            <img src="https://modao.cc/agent-py/media/generated_images/2026-05-08/9d7953ab82914d99a3152d91b46c75a8.jpg#desc=Manager%20Portrait" alt="User" className="object-cover" />
          </Avatar>
          <h3 className="text-xl font-black text-slate-900">王店长</h3>
          <p className="text-sm text-slate-500 mt-1">旗舰店负责运营主管</p>
          <Badge className="mt-3 bg-indigo-50 text-indigo-600 border-none font-bold">超级管理员权限</Badge>
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

import React, { useState, useEffect } from 'react';
import {
  Store,
  MessageSquare,
  Smartphone,
  Bell,
  Shield,
  Settings as SettingsIcon,
  Save,
  RefreshCw,
  Plus,
  Trash2,
  Link,
  Unlink
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { Textarea } from '../../components/ui/textarea';
import { Switch } from '../../components/ui/switch';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../../components/ui/tabs';
import { AdminLayout } from '../../components/AdminLayout';
import { useToast } from '../../hooks/use-toast';

interface StoreSettings {
  name: string;
  address: string;
  phone: string;
  businessHours: string;
}

interface ReplyTemplate {
  id: number;
  name: string;
  content: string;
  enabled: boolean;
  type: 'positive' | 'negative' | 'neutral';
}

interface PlatformConnection {
  id: number;
  name: string;
  icon: string;
  connected: boolean;
  account: string;
}

interface NotificationSettings {
  emailEnabled: boolean;
  smsEnabled: boolean;
  wechatEnabled: boolean;
  email: string;
  phone: string;
}

interface AutoReplyStrategy {
  enabled: boolean;
  mode: 'ai' | 'template' | 'hybrid';
  aiAutoSend: boolean;
  needHumanReview: boolean;
  maxDailyReplies: number;
}

export const MobileSettings: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'store' | 'templates' | 'platforms' | 'notifications' | 'autoReply'>('store');
  const [settings, setSettings] = useState<StoreSettings>({
    name: '香格里拉大酒店',
    address: '北京市东城区王府井大街88号',
    phone: '010-8888-6666',
    businessHours: '11:00 - 22:00',
  });
  const [templates, setTemplates] = useState<ReplyTemplate[]>([
    { id: 1, name: '好评感谢模板', content: '感谢您的好评！我们会继续努力，为您提供更优质的服务。', enabled: true, type: 'positive' },
    { id: 2, name: '差评道歉模板', content: '非常抱歉给您带来了不好的体验，我们会认真改进，欢迎您再次光临。', enabled: true, type: 'negative' },
    { id: 3, name: '中评回复模板', content: '感谢您的宝贵意见，我们会不断优化，期待您的再次光临。', enabled: false, type: 'neutral' },
  ]);
  const [platforms, setPlatforms] = useState<PlatformConnection[]>([
    { id: 1, name: '美团', icon: 'simple-icons:meituan', connected: true, account: 'store@meituan.com' },
    { id: 2, name: '大众点评', icon: 'simple-icons:dianping', connected: true, account: 'store@dianping.com' },
    { id: 3, name: '抖音', icon: 'simple-icons:tiktok', connected: false, account: '' },
    { id: 4, name: '小红书', icon: 'simple-icons:xiaohongshu', connected: true, account: 'store@xiaohongshu.com' },
  ]);
  const [notifications, setNotifications] = useState<NotificationSettings>({
    emailEnabled: true,
    smsEnabled: false,
    wechatEnabled: true,
    email: 'admin@example.com',
    phone: '13800138000',
  });
  const [autoReply, setAutoReply] = useState<AutoReplyStrategy>({
    enabled: true,
    mode: 'ai',
    aiAutoSend: false,
    needHumanReview: true,
    maxDailyReplies: 100,
  });

  const { success, error: showError } = useToast();

  const handleSaveSettings = () => {
    success('保存成功', '店铺信息设置已更新');
  };

  const handleSaveTemplates = () => {
    success('保存成功', '回复模板配置已更新');
  };

  const handleSavePlatforms = () => {
    success('保存成功', '平台账号关联已更新');
  };

  const handleSaveNotifications = () => {
    success('保存成功', '消息通知设置已更新');
  };

  const handleSaveAutoReply = () => {
    success('保存成功', '自动回复策略已更新');
  };

  const handleAddTemplate = () => {
    const newTemplate: ReplyTemplate = {
      id: templates.length + 1,
      name: '新模板',
      content: '请输入回复内容...',
      enabled: false,
      type: 'neutral',
    };
    setTemplates([...templates, newTemplate]);
    success('添加成功', '新模板已添加，请编辑内容');
  };

  const handleDeleteTemplate = (id: number) => {
    setTemplates(templates.filter(t => t.id !== id));
    success('删除成功', `模板 ${id} 已删除`);
  };

  const handleConnectPlatform = (id: number) => {
    setPlatforms(platforms.map(p => 
      p.id === id ? { ...p, connected: !p.connected } : p
    ));
    const platform = platforms.find(p => p.id === id);
    success(
      platform?.connected ? '断开成功' : '连接成功',
      `${platform?.name} 平台账号已${platform?.connected ? '断开' : '连接'}`
    );
  };

  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">移动端设置管理</h2>
            <p className="text-slate-500 mt-1">统一管理移动端的店铺信息、回复模板、平台关联、通知设置和自动回复策略</p>
          </div>
          <Button className="bg-orange-500 hover:bg-orange-600 text-white gap-2">
            <RefreshCw className="w-4 h-4" />
            刷新数据
          </Button>
        </div>

        {/* Tab Switcher */}
        <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as any)}>
          <TabsList className="bg-white border border-slate-100 p-1 rounded-2xl w-fit">
            <TabsTrigger value="store" className="px-6 py-2 rounded-xl data-[state=active]:bg-orange-500 data-[state=active]:text-white">
              <Store className="w-4 h-4 mr-2" />
              店铺信息
            </TabsTrigger>
            <TabsTrigger value="templates" className="px-6 py-2 rounded-xl data-[state=active]:bg-orange-500 data-[state=active]:text-white">
              <MessageSquare className="w-4 h-4 mr-2" />
              回复模板
            </TabsTrigger>
            <TabsTrigger value="platforms" className="px-6 py-2 rounded-xl data-[state=active]:bg-orange-500 data-[state=active]:text-white">
              <Smartphone className="w-4 h-4 mr-2" />
              平台关联
            </TabsTrigger>
            <TabsTrigger value="notifications" className="px-6 py-2 rounded-xl data-[state=active]:bg-orange-500 data-[state=active]:text-white">
              <Bell className="w-4 h-4 mr-2" />
              通知设置
            </TabsTrigger>
            <TabsTrigger value="autoReply" className="px-6 py-2 rounded-xl data-[state=active]:bg-orange-500 data-[state=active]:text-white">
              <Shield className="w-4 h-4 mr-2" />
              自动回复
            </TabsTrigger>
          </TabsList>

          {/* Store Settings Tab */}
          <TabsContent value="store">
            <Card className="p-6 border-none shadow-sm">
              <h3 className="text-lg font-bold text-slate-800 mb-6">店铺信息设置</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">店铺名称</label>
                  <Input
                    value={settings.name}
                    onChange={(e) => setSettings({ ...settings, name: e.target.value })}
                    className="max-w-md"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">店铺地址</label>
                  <Input
                    value={settings.address}
                    onChange={(e) => setSettings({ ...settings, address: e.target.value })}
                    className="max-w-md"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">联系电话</label>
                  <Input
                    value={settings.phone}
                    onChange={(e) => setSettings({ ...settings, phone: e.target.value })}
                    className="max-w-md"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">营业时间</label>
                  <Input
                    value={settings.businessHours}
                    onChange={(e) => setSettings({ ...settings, businessHours: e.target.value })}
                    className="max-w-md"
                  />
                </div>
                <div className="pt-4">
                  <Button className="bg-orange-500 hover:bg-orange-600 text-white gap-2" onClick={handleSaveSettings}>
                    <Save className="w-4 h-4" />
                    保存设置
                  </Button>
                </div>
              </div>
            </Card>
          </TabsContent>

          {/* Reply Templates Tab */}
          <TabsContent value="templates">
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-bold text-slate-800">回复模板配置</h3>
                <Button className="bg-orange-500 hover:bg-orange-600 text-white gap-2" onClick={handleAddTemplate}>
                  <Plus className="w-4 h-4" />
                  添加模板
                </Button>
              </div>
              <div className="space-y-4">
                {templates.map((template) => (
                  <Card key={template.id} className="p-6 border-none shadow-sm">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center gap-3">
                        <Badge className={
                          template.type === 'positive' ? "bg-emerald-100 text-emerald-700" :
                          template.type === 'negative' ? "bg-rose-100 text-rose-700" :
                          "bg-slate-100 text-slate-700"
                        }>
                          {template.type === 'positive' ? '好评' : template.type === 'negative' ? '差评' : '中评'}
                        </Badge>
                        <span className="font-bold text-slate-900">{template.name}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Switch
                          checked={template.enabled}
                          onCheckedChange={(checked) => {
                            setTemplates(templates.map(t => 
                              t.id === template.id ? { ...t, enabled: checked } : t
                            ));
                          }}
                        />
                        <Button
                          size="sm"
                          variant="ghost"
                          className="h-8 w-8 p-0 text-rose-500"
                          onClick={() => handleDeleteTemplate(template.id)}
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                    <Textarea
                      value={template.content}
                      onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => {
                        setTemplates(templates.map(t => 
                          t.id === template.id ? { ...t, content: e.target.value } : t
                        ));
                      }}
                      className="min-h-[100px]"
                    />
                  </Card>
                ))}
                <Button className="bg-orange-500 hover:bg-orange-600 text-white gap-2" onClick={handleSaveTemplates}>
                  <Save className="w-4 h-4" />
                  保存模板配置
                </Button>
              </div>
            </div>
          </TabsContent>

          {/* Platform Connections Tab */}
          <TabsContent value="platforms">
            <div className="space-y-6">
              <h3 className="text-lg font-bold text-slate-800">多平台账号关联</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {platforms.map((platform) => (
                  <Card key={platform.id} className="p-6 border-none shadow-sm">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-lg bg-slate-50 flex items-center justify-center">
                          <iconify-icon icon={platform.icon} class="text-xl"></iconify-icon>
                        </div>
                        <div>
                          <h4 className="font-bold text-slate-900">{platform.name}</h4>
                          {platform.connected && (
                            <p className="text-xs text-slate-400">{platform.account}</p>
                          )}
                        </div>
                      </div>
                      <Badge className={platform.connected ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-500"}>
                        {platform.connected ? '已连接' : '未连接'}
                      </Badge>
                    </div>
                    <Button
                      variant={platform.connected ? "outline" : "default"}
                      className={
                        platform.connected
                          ? "w-full border-rose-200 text-rose-600 hover:bg-rose-50 gap-2"
                          : "w-full bg-orange-500 hover:bg-orange-600 text-white gap-2"
                      }
                      onClick={() => handleConnectPlatform(platform.id)}
                    >
                      {platform.connected ? (
                        <>
                          <Unlink className="w-4 h-4" />
                          断开连接
                        </>
                      ) : (
                        <>
                          <Link className="w-4 h-4" />
                          连接账号
                        </>
                      )}
                    </Button>
                  </Card>
                ))}
              </div>
              <Button className="bg-orange-500 hover:bg-orange-600 text-white gap-2" onClick={handleSavePlatforms}>
                <Save className="w-4 h-4" />
                保存平台关联
              </Button>
            </div>
          </TabsContent>

          {/* Notification Settings Tab */}
          <TabsContent value="notifications">
            <Card className="p-6 border-none shadow-sm">
              <h3 className="text-lg font-bold text-slate-800 mb-6">消息通知设置</h3>
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium text-slate-700">邮件通知</h4>
                    <p className="text-sm text-slate-400">差评、重要事件通过邮件通知</p>
                  </div>
                  <Switch
                    checked={notifications.emailEnabled}
                    onCheckedChange={(checked) => setNotifications({ ...notifications, emailEnabled: checked })}
                  />
                </div>
                {notifications.emailEnabled && (
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">通知邮箱</label>
                    <Input
                      value={notifications.email}
                      onChange={(e) => setNotifications({ ...notifications, email: e.target.value })}
                      className="max-w-md"
                    />
                  </div>
                )}
                <div className="border-t border-slate-100 pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-slate-700">短信通知</h4>
                      <p className="text-sm text-slate-400">紧急事件通过短信通知</p>
                    </div>
                    <Switch
                      checked={notifications.smsEnabled}
                      onCheckedChange={(checked) => setNotifications({ ...notifications, smsEnabled: checked })}
                    />
                  </div>
                </div>
                {notifications.smsEnabled && (
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">通知手机号</label>
                    <Input
                      value={notifications.phone}
                      onChange={(e) => setNotifications({ ...notifications, phone: e.target.value })}
                      className="max-w-md"
                    />
                  </div>
                )}
                <div className="border-t border-slate-100 pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-slate-700">企业微信通知</h4>
                      <p className="text-sm text-slate-400">通过企业微信推送通知</p>
                    </div>
                    <Switch
                      checked={notifications.wechatEnabled}
                      onCheckedChange={(checked) => setNotifications({ ...notifications, wechatEnabled: checked })}
                    />
                  </div>
                </div>
                <div className="pt-4">
                  <Button className="bg-orange-500 hover:bg-orange-600 text-white gap-2" onClick={handleSaveNotifications}>
                    <Save className="w-4 h-4" />
                    保存通知设置
                  </Button>
                </div>
              </div>
            </Card>
          </TabsContent>

          {/* Auto Reply Strategy Tab */}
          <TabsContent value="autoReply">
            <Card className="p-6 border-none shadow-sm">
              <h3 className="text-lg font-bold text-slate-800 mb-6">自动回复策略</h3>
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium text-slate-700">启用自动回复</h4>
                    <p className="text-sm text-slate-400">开启后系统将自动处理评论回复</p>
                  </div>
                  <Switch
                    checked={autoReply.enabled}
                    onCheckedChange={(checked) => setAutoReply({ ...autoReply, enabled: checked })}
                  />
                </div>
                {autoReply.enabled && (
                  <>
                    <div className="border-t border-slate-100 pt-6">
                      <h4 className="font-medium text-slate-700 mb-4">回复模式</h4>
                      <div className="flex gap-3">
                        {[
                          { value: 'ai', label: 'AI智能回复' },
                          { value: 'template', label: '模板回复' },
                          { value: 'hybrid', label: '混合模式' },
                        ].map((mode) => (
                          <Button
                            key={mode.value}
                            variant={autoReply.mode === mode.value ? "default" : "outline"}
                            className={
                              autoReply.mode === mode.value
                                ? "bg-orange-500 hover:bg-orange-600 text-white"
                                : ""
                            }
                            onClick={() => setAutoReply({ ...autoReply, mode: mode.value as any })}
                          >
                            {mode.label}
                          </Button>
                        ))}
                      </div>
                    </div>
                    <div className="border-t border-slate-100 pt-6">
                      <div className="flex items-center justify-between">
                        <div>
                          <h4 className="font-medium text-slate-700">AI回复自动发送</h4>
                          <p className="text-sm text-slate-400">开启后AI生成的回复将自动发送，无需人工审核</p>
                        </div>
                        <Switch
                          checked={autoReply.aiAutoSend}
                          onCheckedChange={(checked) => setAutoReply({ ...autoReply, aiAutoSend: checked })}
                        />
                      </div>
                    </div>
                    <div className="border-t border-slate-100 pt-6">
                      <div className="flex items-center justify-between">
                        <div>
                          <h4 className="font-medium text-slate-700">需要人工审核</h4>
                          <p className="text-sm text-slate-400">开启后所有回复将先经过人工审核再发送</p>
                        </div>
                        <Switch
                          checked={autoReply.needHumanReview}
                          onCheckedChange={(checked) => setAutoReply({ ...autoReply, needHumanReview: checked })}
                        />
                      </div>
                    </div>
                    <div className="border-t border-slate-100 pt-6">
                      <label className="block text-sm font-medium text-slate-700 mb-2">每日最大回复数量</label>
                      <Input
                        type="number"
                        value={autoReply.maxDailyReplies}
                        onChange={(e) => setAutoReply({ ...autoReply, maxDailyReplies: parseInt(e.target.value) || 0 })}
                        className="max-w-md"
                      />
                    </div>
                  </>
                )}
                <div className="pt-4">
                  <Button className="bg-orange-500 hover:bg-orange-600 text-white gap-2" onClick={handleSaveAutoReply}>
                    <Save className="w-4 h-4" />
                    保存自动回复策略
                  </Button>
                </div>
              </div>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </AdminLayout>
  );
};

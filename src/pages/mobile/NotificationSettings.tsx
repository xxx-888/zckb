import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Bell, MessageSquare, TrendingUp, AlertTriangle, Mail, Smartphone, Loader2 } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';
import { settingsApi, UserNotificationSetting } from '../../api/settings';

export const NotificationSettings: React.FC = () => {
  const navigate = useNavigate();
  const { success, error } = useToast();
  
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [settings, setSettings] = useState({
    newReview: true,
    negativeAlert: true,
    weeklyReport: false,
    emailNotification: true,
    smsNotification: false,
    pushNotification: true
  });

  // 加载通知设置
  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      setLoading(true);
      const data = await settingsApi.getNotificationSetting();
      setSettings({
        newReview: data.new_review_enabled,
        negativeAlert: data.negative_alert_enabled,
        weeklyReport: data.weekly_report_enabled,
        emailNotification: data.email_enabled,
        smsNotification: data.sms_enabled,
        pushNotification: data.push_enabled
      });
    } catch (err: any) {
      error('加载失败', err.message || '无法获取通知设置');
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (key: 'newReview' | 'negativeAlert' | 'weeklyReport' | 'emailNotification' | 'smsNotification' | 'pushNotification') => {
    const newSettings = { ...settings, [key]: !settings[key] };
    setSettings(newSettings);
    
    try {
      setSaving(true);
      // 转换字段名：camelCase -> snake_case
      const updateData: any = {};
      if (key === 'newReview') updateData.new_review_enabled = newSettings.newReview;
      if (key === 'negativeAlert') updateData.negative_alert_enabled = newSettings.negativeAlert;
      if (key === 'weeklyReport') updateData.weekly_report_enabled = newSettings.weeklyReport;
      if (key === 'emailNotification') updateData.email_enabled = newSettings.emailNotification;
      if (key === 'smsNotification') updateData.sms_enabled = newSettings.smsNotification;
      if (key === 'pushNotification') updateData.push_enabled = newSettings.pushNotification;
      
      await settingsApi.updateNotificationSetting(updateData);
      success('设置已更新', '通知偏好已保存');
    } catch (err: any) {
      error('保存失败', err.message || '更新通知设置时出现错误');
      // 回滚状态
      setSettings(settings);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-indigo-600 animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      {/* Header */}
      <div className="bg-white px-6 py-4 flex items-center gap-4 shadow-sm">
        <button 
          onClick={() => navigate('/mobile/settings')}
          className="text-slate-600 hover:bg-slate-100 p-2 rounded-xl transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <h1 className="text-lg font-bold text-slate-900">消息通知设置</h1>
      </div>

      <div className="p-6 space-y-6">
        {/* Notification Types */}
        <div className="space-y-3">
          <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-1">通知类型</h4>
          <div className="bg-white rounded-2xl overflow-hidden shadow-sm">
            <div className="divide-y divide-slate-50">
              {/* 新评价通知 */}
              <div className="flex items-center justify-between p-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-blue-50 flex items-center justify-center">
                    <MessageSquare className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-sm font-bold text-slate-900">新评价通知</p>
                    <p className="text-xs text-slate-400">收到新评价时通知</p>
                  </div>
                </div>
                <button
                  onClick={() => handleToggle('newReview')}
                  disabled={saving}
                  className={`w-12 h-6 rounded-full transition-colors relative ${
                    settings.newReview ? 'bg-indigo-600' : 'bg-slate-200'
                  }`}
                >
                  <div className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow-sm transition-transform ${
                    settings.newReview ? 'translate-x-6.5' : 'translate-x-0.5'
                  }`} />
                </button>
              </div>

              {/* 差评预警通知 */}
              <div className="flex items-center justify-between p-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-rose-50 flex items-center justify-center">
                    <AlertTriangle className="w-5 h-5 text-rose-600" />
                  </div>
                  <div>
                    <p className="text-sm font-bold text-slate-900">差评预警通知</p>
                    <p className="text-xs text-slate-400">收到低分评价时立即通知</p>
                  </div>
                </div>
                <button
                  onClick={() => handleToggle('negativeAlert')}
                  disabled={saving}
                  className={`w-12 h-6 rounded-full transition-colors relative ${
                    settings.negativeAlert ? 'bg-indigo-600' : 'bg-slate-200'
                  }`}
                >
                  <div className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow-sm transition-transform ${
                    settings.negativeAlert ? 'translate-x-6.5' : 'translate-x-0.5'
                  }`} />
                </button>
              </div>

              {/* 周报通知 */}
              <div className="flex items-center justify-between p-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-amber-50 flex items-center justify-center">
                    <TrendingUp className="w-5 h-5 text-amber-600" />
                  </div>
                  <div>
                    <p className="text-sm font-bold text-slate-900">周报通知</p>
                    <p className="text-xs text-slate-400">每周数据报告推送</p>
                  </div>
                </div>
                <button
                  onClick={() => handleToggle('weeklyReport')}
                  disabled={saving}
                  className={`w-12 h-6 rounded-full transition-colors relative ${
                    settings.weeklyReport ? 'bg-indigo-600' : 'bg-slate-200'
                  }`}
                >
                  <div className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow-sm transition-transform ${
                    settings.weeklyReport ? 'translate-x-6.5' : 'translate-x-0.5'
                  }`} />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Notification Channels */}
        <div className="space-y-3">
          <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-1">通知渠道</h4>
          <div className="bg-white rounded-2xl overflow-hidden shadow-sm">
            <div className="divide-y divide-slate-50">
              {/* 邮件通知 */}
              <div className="flex items-center justify-between p-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-purple-50 flex items-center justify-center">
                    <Mail className="w-5 h-5 text-purple-600" />
                  </div>
                  <p className="text-sm font-bold text-slate-900">邮件通知</p>
                </div>
                <button
                  onClick={() => handleToggle('emailNotification')}
                  disabled={saving}
                  className={`w-12 h-6 rounded-full transition-colors relative ${
                    settings.emailNotification ? 'bg-indigo-600' : 'bg-slate-200'
                  }`}
                >
                  <div className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow-sm transition-transform ${
                    settings.emailNotification ? 'translate-x-6.5' : 'translate-x-0.5'
                  }`} />
                </button>
              </div>

              {/* 短信通知 */}
              <div className="flex items-center justify-between p-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-cyan-50 flex items-center justify-center">
                    <Smartphone className="w-5 h-5 text-cyan-600" />
                  </div>
                  <p className="text-sm font-bold text-slate-900">短信通知</p>
                </div>
                <button
                  onClick={() => handleToggle('smsNotification')}
                  disabled={saving}
                  className={`w-12 h-6 rounded-full transition-colors relative ${
                    settings.smsNotification ? 'bg-indigo-600' : 'bg-slate-200'
                  }`}
                >
                  <div className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow-sm transition-transform ${
                    settings.smsNotification ? 'translate-x-6.5' : 'translate-x-0.5'
                  }`} />
                </button>
              </div>

              {/* 推送通知 */}
              <div className="flex items-center justify-between p-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-indigo-50 flex items-center justify-center">
                    <Bell className="w-5 h-5 text-indigo-600" />
                  </div>
                  <p className="text-sm font-bold text-slate-900">推送通知</p>
                </div>
                <button
                  onClick={() => handleToggle('pushNotification')}
                  disabled={saving}
                  className={`w-12 h-6 rounded-full transition-colors relative ${
                    settings.pushNotification ? 'bg-indigo-600' : 'bg-slate-200'
                  }`}
                >
                  <div className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow-sm transition-transform ${
                    settings.pushNotification ? 'translate-x-6.5' : 'translate-x-0.5'
                  }`} />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Save Button */}
        <Button 
          onClick={() => success('设置已更新', '通知设置已自动保存')}
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-7 text-lg font-bold shadow-xl shadow-indigo-100"
        >
          保存设置
        </Button>
      </div>
    </div>
  );
};

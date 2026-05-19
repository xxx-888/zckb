import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Bell, MessageSquare, TrendingUp, AlertTriangle, Mail, Smartphone } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';

export const NotificationSettings: React.FC = () => {
  const navigate = useNavigate();
  const { success } = useToast();
  
  const [settings, setSettings] = useState({
    newReview: true,
    reviewMention: true,
    negativeAlert: true,
    weeklyReport: false,
    emailNotification: true,
    smsNotification: false,
    pushNotification: true
  });

  const handleToggle = (key: 'newReview' | 'reviewMention' | 'negativeAlert' | 'weeklyReport' | 'emailNotification' | 'smsNotification' | 'pushNotification') => {
    setSettings(prev => ({ ...prev, [key]: !prev[key] }));
    success('设置已更新', '通知偏好已保存');
  };

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
                  className={`w-12 h-6 rounded-full transition-colors relative ${
                    settings.newReview ? 'bg-indigo-600' : 'bg-slate-200'
                  }`}
                >
                  <div className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow-sm transition-transform ${
                    settings.newReview ? 'translate-x-6.5' : 'translate-x-0.5'
                  }`} />
                </button>
              </div>

              {/* 评价提及通知 */}
              <div className="flex items-center justify-between p-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-green-50 flex items-center justify-center">
                    <Bell className="w-5 h-5 text-green-600" />
                  </div>
                  <div>
                    <p className="text-sm font-bold text-slate-900">评价提及通知</p>
                    <p className="text-xs text-slate-400">评价中提到店铺时通知</p>
                  </div>
                </div>
                <button
                  onClick={() => handleToggle('reviewMention')}
                  className={`w-12 h-6 rounded-full transition-colors relative ${
                    settings.reviewMention ? 'bg-indigo-600' : 'bg-slate-200'
                  }`}
                >
                  <div className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow-sm transition-transform ${
                    settings.reviewMention ? 'translate-x-6.5' : 'translate-x-0.5'
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
          onClick={() => success('保存成功', '通知设置已更新')}
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-7 text-lg font-bold shadow-xl shadow-indigo-100"
        >
          保存设置
        </Button>
      </div>
    </div>
  );
};

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Shield, Bot, Zap, Clock, CheckCircle2 } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';

export const AutoReplySettings: React.FC = () => {
  const navigate = useNavigate();
  const { success } = useToast();
  
  const [settings, setSettings] = useState({
    mode: 'smart', // 'manual', 'semi-auto', 'smart'
    autoReplyEnabled: true,
    workingHoursOnly: false,
    maxRepliesPerDay: 50,
    replyDelay: 5, // minutes
    enableAISuggestion: true,
    enableKeywordReply: true
  });

  const handleModeChange = (mode: string) => {
    setSettings(prev => ({ ...prev, mode }));
    success('模式已切换', `已切换到${mode === 'manual' ? '手动模式' : mode === 'semi-auto' ? '半自动模式' : '智能模式'}`);
  };

  const handleToggle = (key: 'autoReplyEnabled' | 'workingHoursOnly' | 'enableAISuggestion' | 'enableKeywordReply') => {
    setSettings(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const handleSave = () => {
    success('保存成功', '自动回复策略已更新');
    setTimeout(() => navigate('/mobile/settings'), 1000);
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
        <h1 className="text-lg font-bold text-slate-900">自动回复策略</h1>
      </div>

      <div className="p-6 space-y-6">
        {/* Mode Selection */}
        <div className="space-y-3">
          <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-1">回复模式</h4>
          <div className="bg-white rounded-2xl overflow-hidden shadow-sm">
            <div className="divide-y divide-slate-50">
              {/* 手动模式 */}
              <button
                onClick={() => handleModeChange('manual')}
                className={`w-full flex items-center gap-4 p-4 transition-colors ${
                  settings.mode === 'manual' ? 'bg-indigo-50' : 'hover:bg-slate-50'
                }`}
              >
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                  settings.mode === 'manual' ? 'bg-indigo-100 text-indigo-600' : 'bg-slate-100 text-slate-400'
                }`}>
                  <Shield className="w-5 h-5" />
                </div>
                <div className="flex-1 text-left">
                  <p className={`text-sm font-bold ${settings.mode === 'manual' ? 'text-indigo-600' : 'text-slate-700'}`}>手动模式</p>
                  <p className="text-xs text-slate-400">所有回复需手动审核后发送</p>
                </div>
                {settings.mode === 'manual' && (
                  <CheckCircle2 className="w-5 h-5 text-indigo-600" />
                )}
              </button>

              {/* 半自动模式 */}
              <button
                onClick={() => handleModeChange('semi-auto')}
                className={`w-full flex items-center gap-4 p-4 transition-colors ${
                  settings.mode === 'semi-auto' ? 'bg-indigo-50' : 'hover:bg-slate-50'
                }`}
              >
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                  settings.mode === 'semi-auto' ? 'bg-indigo-100 text-indigo-600' : 'bg-slate-100 text-slate-400'
                }`}>
                  <Bot className="w-5 h-5" />
                </div>
                <div className="flex-1 text-left">
                  <p className={`text-sm font-bold ${settings.mode === 'semi-auto' ? 'text-indigo-600' : 'text-slate-700'}`}>半自动模式</p>
                  <p className="text-xs text-slate-400">AI生成回复，人工确认后发送</p>
                </div>
                {settings.mode === 'semi-auto' && (
                  <CheckCircle2 className="w-5 h-5 text-indigo-600" />
                )}
              </button>

              {/* 智能模式 */}
              <button
                onClick={() => handleModeChange('smart')}
                className={`w-full flex items-center gap-4 p-4 transition-colors ${
                  settings.mode === 'smart' ? 'bg-indigo-50' : 'hover:bg-slate-50'
                }`}
              >
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                  settings.mode === 'smart' ? 'bg-indigo-100 text-indigo-600' : 'bg-slate-100 text-slate-400'
                }`}>
                  <Zap className="w-5 h-5" />
                </div>
                <div className="flex-1 text-left">
                  <p className={`text-sm font-bold ${settings.mode === 'smart' ? 'text-indigo-600' : 'text-slate-700'}`}>智能模式</p>
                  <p className="text-xs text-slate-400">AI自动回复，高危情况转人工</p>
                </div>
                {settings.mode === 'smart' && (
                  <CheckCircle2 className="w-5 h-5 text-indigo-600" />
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Advanced Settings */}
        <div className="space-y-3">
          <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-1">高级设置</h4>
          <div className="bg-white rounded-2xl overflow-hidden shadow-sm">
            <div className="divide-y divide-slate-50">
              {/* 启用自动回复 */}
              <div className="flex items-center justify-between p-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-green-50 flex items-center justify-center">
                    <Bot className="w-5 h-5 text-green-600" />
                  </div>
                  <p className="text-sm font-bold text-slate-700">启用自动回复</p>
                </div>
                <button
                  onClick={() => handleToggle('autoReplyEnabled')}
                  className={`w-12 h-6 rounded-full transition-colors relative ${
                    settings.autoReplyEnabled ? 'bg-indigo-600' : 'bg-slate-200'
                  }`}
                >
                  <div className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow-sm transition-transform ${
                    settings.autoReplyEnabled ? 'translate-x-6.5' : 'translate-x-0.5'
                  }`} />
                </button>
              </div>

              {/* 仅工作时间回复 */}
              <div className="flex items-center justify-between p-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-amber-50 flex items-center justify-center">
                    <Clock className="w-5 h-5 text-amber-600" />
                  </div>
                  <div>
                    <p className="text-sm font-bold text-slate-700">仅工作时间回复</p>
                    <p className="text-xs text-slate-400">09:00-18:00</p>
                  </div>
                </div>
                <button
                  onClick={() => handleToggle('workingHoursOnly')}
                  className={`w-12 h-6 rounded-full transition-colors relative ${
                    settings.workingHoursOnly ? 'bg-indigo-600' : 'bg-slate-200'
                  }`}
                >
                  <div className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow-sm transition-transform ${
                    settings.workingHoursOnly ? 'translate-x-6.5' : 'translate-x-0.5'
                  }`} />
                </button>
              </div>

              {/* AI建议 */}
              <div className="flex items-center justify-between p-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-purple-50 flex items-center justify-center">
                    <Zap className="w-5 h-5 text-purple-600" />
                  </div>
                  <p className="text-sm font-bold text-slate-700">AI智能建议</p>
                </div>
                <button
                  onClick={() => handleToggle('enableAISuggestion')}
                  className={`w-12 h-6 rounded-full transition-colors relative ${
                    settings.enableAISuggestion ? 'bg-indigo-600' : 'bg-slate-200'
                  }`}
                >
                  <div className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow-sm transition-transform ${
                    settings.enableAISuggestion ? 'translate-x-6.5' : 'translate-x-0.5'
                  }`} />
                </button>
              </div>

              {/* 关键词回复 */}
              <div className="flex items-center justify-between p-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-cyan-50 flex items-center justify-center">
                    <Shield className="w-5 h-5 text-cyan-600" />
                  </div>
                  <p className="text-sm font-bold text-slate-700">关键词自动回复</p>
                </div>
                <button
                  onClick={() => handleToggle('enableKeywordReply')}
                  className={`w-12 h-6 rounded-full transition-colors relative ${
                    settings.enableKeywordReply ? 'bg-indigo-600' : 'bg-slate-200'
                  }`}
                >
                  <div className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow-sm transition-transform ${
                    settings.enableKeywordReply ? 'translate-x-6.5' : 'translate-x-0.5'
                  }`} />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Save Button */}
        <Button 
          onClick={handleSave}
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-7 text-lg font-bold shadow-xl shadow-indigo-100"
        >
          保存设置
        </Button>
      </div>
    </div>
  );
};

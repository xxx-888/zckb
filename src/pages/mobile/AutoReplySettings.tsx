import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Shield, Bot, Zap, Clock, CheckCircle2, Loader2 } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';
import { settingsApi, AutoReplyConfig } from '../../api/settings';

export const AutoReplySettings: React.FC = () => {
  const navigate = useNavigate();
  const { success, error } = useToast();
  
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [storeId, setStoreId] = useState<string>('');
  const [settings, setSettings] = useState({
    mode: 'smart' as 'smart' | 'manual' | 'semi_auto',
    autoReplyEnabled: true,
    workingHoursOnly: false,
    enableAISuggestion: true,
    enableKeywordReply: true
  });

  // 加载自动回复配置
  useEffect(() => {
    const savedStoreId = localStorage.getItem('zc_selected_store_id');
    if (savedStoreId) {
      setStoreId(savedStoreId);
      loadConfig(savedStoreId);
    } else {
      setLoading(false);
      error('加载失败', '请先选择门店');
    }
  }, []);

  const loadConfig = async (storeId: string) => {
    try {
      setLoading(true);
      const data = await settingsApi.getAutoReplyConfig(storeId);
      setSettings({
        mode: data.mode,
        autoReplyEnabled: data.auto_reply_enabled,
        workingHoursOnly: data.work_hours_only,
        enableAISuggestion: data.ai_suggest_enabled,
        enableKeywordReply: data.keyword_reply_enabled
      });
    } catch (err: any) {
      error('加载失败', err.message || '无法获取自动回复配置');
    } finally {
      setLoading(false);
    }
  };

  const handleModeChange = async (mode: 'manual' | 'semi_auto' | 'smart') => {
    try {
      setSaving(true);
      const updated = await settingsApi.updateAutoReplyConfig({ mode }, storeId);
      setSettings(prev => ({ ...prev, mode: updated.mode }));
      success('模式已切换', `已切换到${mode === 'manual' ? '手动模式' : mode === 'semi_auto' ? '半自动模式' : '智能模式'}`);
    } catch (err: any) {
      error('切换失败', err.message || '切换模式时出现错误');
    } finally {
      setSaving(false);
    }
  };

  const handleToggle = async (key: 'autoReplyEnabled' | 'workingHoursOnly' | 'enableAISuggestion' | 'enableKeywordReply') => {
    try {
      setSaving(true);
      
      // 转换字段名：camelCase -> snake_case
      const updateData: any = {};
      if (key === 'autoReplyEnabled') updateData.auto_reply_enabled = !settings.autoReplyEnabled;
      if (key === 'workingHoursOnly') updateData.work_hours_only = !settings.workingHoursOnly;
      if (key === 'enableAISuggestion') updateData.ai_suggest_enabled = !settings.enableAISuggestion;
      if (key === 'enableKeywordReply') updateData.keyword_reply_enabled = !settings.enableKeywordReply;
      
      const updated = await settingsApi.updateAutoReplyConfig(updateData, storeId);
      
      // 更新本地状态
      if (key === 'autoReplyEnabled') setSettings(prev => ({ ...prev, autoReplyEnabled: updated.auto_reply_enabled }));
      if (key === 'workingHoursOnly') setSettings(prev => ({ ...prev, workingHoursOnly: updated.work_hours_only }));
      if (key === 'enableAISuggestion') setSettings(prev => ({ ...prev, enableAISuggestion: updated.ai_suggest_enabled }));
      if (key === 'enableKeywordReply') setSettings(prev => ({ ...prev, enableKeywordReply: updated.keyword_reply_enabled }));
    } catch (err: any) {
      error('操作失败', err.message || '更新设置时出现错误');
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
                disabled={saving}
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
                onClick={() => handleModeChange('semi_auto')}
                disabled={saving}
                className={`w-full flex items-center gap-4 p-4 transition-colors ${
                  settings.mode === 'semi_auto' ? 'bg-indigo-50' : 'hover:bg-slate-50'
                }`}
              >
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                  settings.mode === 'semi_auto' ? 'bg-indigo-100 text-indigo-600' : 'bg-slate-100 text-slate-400'
                }`}>
                  <Bot className="w-5 h-5" />
                </div>
                <div className="flex-1 text-left">
                  <p className={`text-sm font-bold ${settings.mode === 'semi_auto' ? 'text-indigo-600' : 'text-slate-700'}`}>半自动模式</p>
                  <p className="text-xs text-slate-400">AI生成回复，人工确认后发送</p>
                </div>
                {settings.mode === 'semi_auto' && (
                  <CheckCircle2 className="w-5 h-5 text-indigo-600" />
                )}
              </button>

              {/* 智能模式 */}
              <button
                onClick={() => handleModeChange('smart')}
                disabled={saving}
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
                  disabled={saving}
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
                  disabled={saving}
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
                  disabled={saving}
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
                  disabled={saving}
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
          onClick={() => {
            success('设置已更新', '自动回复策略已自动保存');
            setTimeout(() => navigate('/mobile/settings'), 1000);
          }}
          disabled={saving}
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-7 text-lg font-bold shadow-xl shadow-indigo-100 disabled:opacity-50"
        >
          {saving ? (
            <>
              <Loader2 className="w-5 h-5 mr-2 animate-spin" />
              保存中...
            </>
          ) : (
            <>
              <CheckCircle2 className="w-5 h-5 mr-2" />
              保存设置
            </>
          )}
        </Button>
      </div>
    </div>
  );
};

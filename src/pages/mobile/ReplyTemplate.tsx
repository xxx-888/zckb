import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Plus, Trash2, MessageSquare, Check, Loader2 } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';
import { settingsApi, ReplyTemplate } from '../../api/settings';

export const ReplyTemplate: React.FC = () => {
  const navigate = useNavigate();
  const { success, error } = useToast();
  
  const [templates, setTemplates] = useState<ReplyTemplate[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  
  const [showAddModal, setShowAddModal] = useState(false);
  const [editingTemplate, setEditingTemplate] = useState<ReplyTemplate | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    content: '',
    type: 'good' as 'good' | 'bad' | 'neutral',
    is_active: true
  });

  // 加载模板列表
  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    try {
      setLoading(true);
      const data = await settingsApi.getReplyTemplates();
      setTemplates(data);
    } catch (err: any) {
      error('加载失败', err.message || '无法获取模板列表');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field: string, value: string | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSaveTemplate = async () => {
    if (!formData.name.trim()) {
      error('请输入模板名称', '模板名称不能为空');
      return;
    }

    if (!formData.content.trim()) {
      error('请输入模板内容', '模板内容不能为空');
      return;
    }

    try {
      setSaving(true);
      
      if (editingTemplate) {
        // 编辑模板
        const updated = await settingsApi.updateReplyTemplate(editingTemplate.id, {
          name: formData.name,
          content: formData.content,
          type: formData.type,
          is_active: formData.is_active
        });
        setTemplates(prev => prev.map(t => t.id === updated.id ? updated : t));
        success('更新成功', '模板已更新');
      } else {
        // 添加模板
        const newTemplate = await settingsApi.createReplyTemplate({
          name: formData.name,
          content: formData.content,
          type: formData.type,
          is_active: formData.is_active
        });
        setTemplates(prev => [...prev, newTemplate]);
        success('添加成功', '新模板已添加');
      }

      setShowAddModal(false);
      setEditingTemplate(null);
      setFormData({ name: '', content: '', type: 'good', is_active: true });
    } catch (err: any) {
      error('保存失败', err.message || '保存模板时出现错误');
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = (template: ReplyTemplate) => {
    setEditingTemplate(template);
    setFormData({
      name: template.name,
      content: template.content,
      type: template.type,
      is_active: template.is_active
    });
    setShowAddModal(true);
  };

  const handleDelete = async (id: string) => {
    try {
      await settingsApi.deleteReplyTemplate(id);
      setTemplates(prev => prev.filter(t => t.id !== id));
      success('删除成功', '模板已删除');
    } catch (err: any) {
      error('删除失败', err.message || '删除模板时出现错误');
    }
  };

  const handleToggleEnabled = async (template: ReplyTemplate) => {
    try {
      const updated = await settingsApi.updateReplyTemplate(template.id, {
        is_active: !template.is_active
      });
      setTemplates(prev => prev.map(t => t.id === updated.id ? updated : t));
    } catch (err: any) {
      error('操作失败', err.message || '更新模板状态时出现错误');
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
        <h1 className="text-lg font-bold text-slate-900">回复模板配置</h1>
      </div>

      <div className="p-6 space-y-4">
        {/* Stats */}
        <div className="bg-white rounded-2xl p-4 flex items-center justify-around shadow-sm">
          <div className="text-center">
            <p className="text-2xl font-black text-indigo-600">{templates.length}</p>
            <p className="text-xs text-slate-400">总模板</p>
          </div>
          <div className="w-px h-10 bg-slate-200"></div>
          <div className="text-center">
            <p className="text-2xl font-black text-green-600">{templates.filter(t => t.is_active).length}</p>
            <p className="text-xs text-slate-400">已启用</p>
          </div>
          <div className="w-px h-10 bg-slate-200"></div>
          <div className="text-center">
            <p className="text-2xl font-black text-amber-600">{templates.filter(t => t.type === 'good').length}</p>
            <p className="text-xs text-slate-400">好评模板</p>
          </div>
        </div>

        {/* Template List */}
        <div className="space-y-3">
          {templates.map((template) => (
            <div key={template.id} className="bg-white rounded-2xl p-4 shadow-sm space-y-3">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <h3 className="font-bold text-slate-900">{template.name}</h3>
                    {template.type === 'good' && (
                      <span className="px-2 py-0.5 bg-green-100 text-green-700 text-xs font-bold rounded-lg">好评</span>
                    )}
                    {template.type === 'bad' && (
                      <span className="px-2 py-0.5 bg-red-100 text-red-700 text-xs font-bold rounded-lg">差评</span>
                    )}
                    {template.type === 'neutral' && (
                      <span className="px-2 py-0.5 bg-slate-100 text-slate-700 text-xs font-bold rounded-lg">中评</span>
                    )}
                    {!template.is_active && (
                      <span className="px-2 py-0.5 bg-slate-100 text-slate-400 text-xs font-bold rounded-lg">已禁用</span>
                    )}
                  </div>
                  <p className="text-sm text-slate-500 mt-2 line-clamp-2">{template.content}</p>
                </div>
              </div>

              <div className="flex items-center gap-2 pt-2 border-t border-slate-50">
                <button 
                  onClick={() => handleToggleEnabled(template)}
                  className={`flex-1 py-2 rounded-xl text-xs font-bold transition-colors ${
                    template.is_active 
                      ? 'bg-green-50 text-green-600' 
                      : 'bg-slate-50 text-slate-400'
                  }`}
                >
                  {template.is_active ? '已启用' : '已禁用'}
                </button>
                <button 
                  onClick={() => handleEdit(template)}
                  className="px-4 py-2 rounded-xl text-xs font-bold bg-indigo-50 text-indigo-600"
                >
                  编辑
                </button>
                <button 
                  onClick={() => handleDelete(template.id)}
                  className="px-4 py-2 rounded-xl text-xs font-bold bg-rose-50 text-rose-600"
                >
                  <Trash2 className="w-3 h-3" />
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Add Button */}
        <Button 
          onClick={() => {
            setEditingTemplate(null);
            setFormData({ name: '', content: '', type: 'good', is_active: true });
            setShowAddModal(true);
          }}
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-7 text-lg font-bold shadow-xl shadow-indigo-100"
        >
          <Plus className="w-5 h-5 mr-2" />
          添加新模板
        </Button>
      </div>

      {/* Add/Edit Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/50 flex items-end justify-center z-50" onClick={() => setShowAddModal(false)}>
          <div 
            className="bg-white rounded-t-3xl w-full max-w-lg p-6 space-y-4 animate-in slide-in-from-bottom duration-300"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-slate-900">
                {editingTemplate ? '编辑模板' : '添加模板'}
              </h2>
              <button 
                onClick={() => setShowAddModal(false)}
                className="text-slate-400 hover:text-slate-600"
              >
                ✕
              </button>
            </div>

            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">模板名称</label>
                <input 
                  type="text" 
                  value={formData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  placeholder="请输入模板名称"
                  className="w-full bg-slate-50 border-none rounded-2xl py-4 px-4 focus:ring-2 focus:ring-indigo-600 transition-all outline-none text-sm"
                />
              </div>

              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">模板类型</label>
                <div className="flex gap-2">
                  {[
                    { value: 'good', label: '好评', color: 'green' },
                    { value: 'bad', label: '差评', color: 'red' },
                    { value: 'neutral', label: '中评', color: 'slate' }
                  ].map(option => (
                    <button
                      key={option.value}
                      onClick={() => handleInputChange('type', option.value)}
                      className={`flex-1 py-2 rounded-xl text-xs font-bold transition-colors ${
                        formData.type === option.value 
                          ? `bg-${option.color}-100 text-${option.color}-700` 
                          : 'bg-slate-50 text-slate-400'
                      }`}
                    >
                      {option.label}
                    </button>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">模板内容</label>
                <textarea 
                  value={formData.content}
                  onChange={(e) => handleInputChange('content', e.target.value)}
                  placeholder="请输入回复内容"
                  rows={4}
                  className="w-full bg-slate-50 border-none rounded-2xl py-4 px-4 focus:ring-2 focus:ring-indigo-600 transition-all outline-none text-sm resize-none"
                />
              </div>

              <label className="flex items-center gap-3 cursor-pointer">
                <input 
                  type="checkbox" 
                  checked={formData.is_active}
                  onChange={(e) => handleInputChange('is_active', e.target.checked)}
                  className="w-4 h-4 rounded border-slate-200 text-indigo-600 focus:ring-indigo-600" 
                />
                <span className="text-sm text-slate-700">启用此模板</span>
              </label>
            </div>

            <Button 
              onClick={handleSaveTemplate}
              disabled={saving}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-7 text-lg font-bold shadow-xl shadow-indigo-100 mt-4 disabled:opacity-50"
            >
              {saving ? (
                <>
                  <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                  保存中...
                </>
              ) : (
                <>
                  <Check className="w-5 h-5 mr-2" />
                  {editingTemplate ? '保存修改' : '添加模板'}
                </>
              )}
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

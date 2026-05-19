import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Plus, Trash2, MessageSquare, Check } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';

interface ReplyTemplate {
  id: number;
  name: string;
  content: string;
  isDefault: boolean;
  isEnabled: boolean;
}

export const ReplyTemplate: React.FC = () => {
  const navigate = useNavigate();
  const { success, error } = useToast();
  
  const [templates, setTemplates] = useState<ReplyTemplate[]>([
    {
      id: 1,
      name: '好评感谢模板',
      content: '感谢您的好评！您的支持是我们前进的动力，期待您的再次光临！',
      isDefault: true,
      isEnabled: true
    },
    {
      id: 2,
      name: '差评道歉模板',
      content: '非常抱歉给您带来了不好的体验。我们会认真改进，希望能有机会为您提供更好的服务。',
      isDefault: false,
      isEnabled: true
    },
    {
      id: 3,
      name: '中评回复模板',
      content: '感谢您的反馈，我们会继续努力提升服务质量，希望下次能给您更好的体验。',
      isDefault: false,
      isEnabled: false
    }
  ]);

  const [showAddModal, setShowAddModal] = useState(false);
  const [editingTemplate, setEditingTemplate] = useState<ReplyTemplate | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    content: '',
    isDefault: false,
    isEnabled: true
  });

  const handleInputChange = (field: string, value: string | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSaveTemplate = () => {
    if (!formData.name.trim()) {
      error('请输入模板名称', '模板名称不能为空');
      return;
    }

    if (!formData.content.trim()) {
      error('请输入模板内容', '模板内容不能为空');
      return;
    }

    if (editingTemplate) {
      // 编辑模板
      setTemplates(prev => prev.map(t => 
        t.id === editingTemplate.id 
          ? { ...t, name: formData.name, content: formData.content, isDefault: formData.isDefault, isEnabled: formData.isEnabled }
          : t
      ));
      success('更新成功', '模板已更新');
    } else {
      // 添加模板
      const newTemplate: ReplyTemplate = {
        id: Date.now(),
        name: formData.name,
        content: formData.content,
        isDefault: formData.isDefault,
        isEnabled: formData.isEnabled
      };
      setTemplates(prev => [...prev, newTemplate]);
      success('添加成功', '新模板已添加');
    }

    setShowAddModal(false);
    setEditingTemplate(null);
    setFormData({ name: '', content: '', isDefault: false, isEnabled: true });
  };

  const handleEdit = (template: ReplyTemplate) => {
    setEditingTemplate(template);
    setFormData({
      name: template.name,
      content: template.content,
      isDefault: template.isDefault,
      isEnabled: template.isEnabled
    });
    setShowAddModal(true);
  };

  const handleDelete = (id: number) => {
    setTemplates(prev => prev.filter(t => t.id !== id));
    success('删除成功', '模板已删除');
  };

  const handleToggleEnabled = (id: number) => {
    setTemplates(prev => prev.map(t => 
      t.id === id ? { ...t, isEnabled: !t.isEnabled } : t
    ));
  };

  const handleSetDefault = (id: number) => {
    setTemplates(prev => prev.map(t => 
      t.id === id ? { ...t, isDefault: true } : { ...t, isDefault: false }
    ));
    success('设置成功', '默认模板已更新');
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
            <p className="text-2xl font-black text-green-600">{templates.filter(t => t.isEnabled).length}</p>
            <p className="text-xs text-slate-400">已启用</p>
          </div>
          <div className="w-px h-10 bg-slate-200"></div>
          <div className="text-center">
            <p className="text-2xl font-black text-amber-600">{templates.filter(t => t.isDefault).length}</p>
            <p className="text-xs text-slate-400">默认模板</p>
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
                    {template.isDefault && (
                      <span className="px-2 py-0.5 bg-amber-100 text-amber-700 text-xs font-bold rounded-lg">默认</span>
                    )}
                    {!template.isEnabled && (
                      <span className="px-2 py-0.5 bg-slate-100 text-slate-400 text-xs font-bold rounded-lg">已禁用</span>
                    )}
                  </div>
                  <p className="text-sm text-slate-500 mt-2 line-clamp-2">{template.content}</p>
                </div>
              </div>

              <div className="flex items-center gap-2 pt-2 border-t border-slate-50">
                <button 
                  onClick={() => handleToggleEnabled(template.id)}
                  className={`flex-1 py-2 rounded-xl text-xs font-bold transition-colors ${
                    template.isEnabled 
                      ? 'bg-green-50 text-green-600' 
                      : 'bg-slate-50 text-slate-400'
                  }`}
                >
                  {template.isEnabled ? '已启用' : '已禁用'}
                </button>
                {!template.isDefault && (
                  <button 
                    onClick={() => handleSetDefault(template.id)}
                    className="flex-1 py-2 rounded-xl text-xs font-bold bg-amber-50 text-amber-600"
                  >
                    设为默认
                  </button>
                )}
                <button 
                  onClick={() => handleEdit(template)}
                  className="px-4 py-2 rounded-xl text-xs font-bold bg-indigo-50 text-indigo-600"
                >
                  编辑
                </button>
                {!template.isDefault && (
                  <button 
                    onClick={() => handleDelete(template.id)}
                    className="px-4 py-2 rounded-xl text-xs font-bold bg-rose-50 text-rose-600"
                  >
                    <Trash2 className="w-3 h-3" />
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Add Button */}
        <Button 
          onClick={() => {
            setEditingTemplate(null);
            setFormData({ name: '', content: '', isDefault: false, isEnabled: true });
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
                  checked={formData.isEnabled}
                  onChange={(e) => handleInputChange('isEnabled', e.target.checked)}
                  className="w-4 h-4 rounded border-slate-200 text-indigo-600 focus:ring-indigo-600" 
                />
                <span className="text-sm text-slate-700">启用此模板</span>
              </label>

              {!editingTemplate && (
                <label className="flex items-center gap-3 cursor-pointer">
                  <input 
                    type="checkbox" 
                    checked={formData.isDefault}
                    onChange={(e) => handleInputChange('isDefault', e.target.checked)}
                    className="w-4 h-4 rounded border-slate-200 text-amber-600 focus:ring-amber-600" 
                  />
                  <span className="text-sm text-slate-700">设为默认模板</span>
                </label>
              )}
            </div>

            <Button 
              onClick={handleSaveTemplate}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-7 text-lg font-bold shadow-xl shadow-indigo-100 mt-4"
            >
              <Check className="w-5 h-5 mr-2" />
              {editingTemplate ? '保存修改' : '添加模板'}
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

import React, { useState, useEffect, useCallback } from 'react';
import { Card } from '../../../components/ui/card';
import { Button } from '../../../components/ui/button';
import { Badge } from '../../../components/ui/badge';
import { useToast } from '../../../hooks/use-toast';
import { adminApi } from '../../../api/admin';
import { Sparkles, RefreshCw, AlertCircle, Save, Plus, Edit3, Trash2, X } from 'lucide-react';

const SCENARIO_TYPES = [
  { value: 'good_review', label: '好评回复', color: 'bg-emerald-100 text-emerald-700' },
  { value: 'bad_review', label: '差评回复', color: 'bg-rose-100 text-rose-700' },
  { value: 'neutral_review', label: '中评回复', color: 'bg-amber-100 text-amber-700' },
  { value: 'appeal', label: '申诉处理', color: 'bg-blue-100 text-blue-700' },
  { value: 'weekly_report', label: '周报生成', color: 'bg-purple-100 text-purple-700' },
];

const getTypeLabel = (type: string) => {
  const t = SCENARIO_TYPES.find(s => s.value === type);
  return t ? { label: t.label, color: t.color } : { label: type || '其他', color: 'bg-slate-100 text-slate-600' };
};

interface PromptItem {
  id: string;
  name: string;
  type: string;
  template_text: string;
  system_prompt?: string;
  variables?: string[];
  is_default: boolean;
  is_active: boolean;
}

const emptyForm = { name: '', type: 'good_review', template_text: '', system_prompt: '', is_active: true };

export const PromptConfig: React.FC = () => {
  const [prompts, setPrompts] = useState<PromptItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<PromptItem | null>(null);
  const [form, setForm] = useState({ ...emptyForm });
  const [saving, setSaving] = useState(false);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const { success, error: toastError } = useToast();

  const fetchPrompts = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await adminApi.getAIPrompts().catch(() => []);
      setPrompts(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchPrompts(); }, [fetchPrompts]);

  const openAddModal = () => {
    setEditingItem(null);
    setForm({ ...emptyForm });
    setModalOpen(true);
  };

  const openEditModal = (item: PromptItem) => {
    setEditingItem(item);
    setForm({
      name: item.name,
      type: item.type,
      template_text: item.template_text || '',
      system_prompt: item.system_prompt || '',
      is_active: item.is_active,
    });
    setModalOpen(true);
  };

  const handleSave = async () => {
    if (!form.name || !form.template_text) {
      toastError('参数错误', '请填写指令名称和模板内容');
      return;
    }

    setSaving(true);
    try {
      const payload: any = {
        name: form.name,
        type: form.type,
        template_text: form.template_text,
        system_prompt: form.system_prompt || undefined,
        is_active: form.is_active,
      };

      if (editingItem) {
        await adminApi.updateAIPrompt(editingItem.id, payload);
        success('保存成功', '指令已更新');
      } else {
        await adminApi.createAIPrompt(payload);
        success('创建成功', '新指令已添加');
      }
      setModalOpen(false);
      fetchPrompts();
    } catch (err: any) {
      toastError(editingItem ? '保存失败' : '创建失败', err.message || '请求异常');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (item: PromptItem) => {
    if (!confirm(`确定要删除指令「${item.name}」吗？此操作不可恢复。`)) return;
    setDeletingId(item.id);
    try {
      // 后端暂无 DELETE prompts 接口，但可以尝试；失败则提示
      toastError('暂不支持', '后端暂未提供删除指令接口，请通过数据库管理');
    } catch {
      toastError('删除失败', '操作异常');
    } finally {
      setDeletingId(null);
    }
  };

  if (loading) return <div className="flex items-center justify-center h-64"><RefreshCw className="w-6 h-6 text-slate-400 animate-spin" /></div>;
  if (error) return <div className="flex flex-col items-center justify-center h-64 gap-4"><AlertCircle className="w-10 h-10 text-rose-400" /><p className="text-slate-500">{error}</p><Button variant="outline" onClick={fetchPrompts}>重试</Button></div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-purple-500" />AI 指令配置
          </h2>
          <p className="text-sm text-slate-500">管理 AI 回复的人格、语气、场景指令</p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={fetchPrompts}><RefreshCw className="w-4 h-4 mr-1" />刷新</Button>
          <Button size="sm" className="bg-purple-500 hover:bg-purple-600 text-white" onClick={openAddModal}>
            <Plus className="w-4 h-4 mr-1" />新增指令
          </Button>
        </div>
      </div>

      {prompts.length === 0 ? (
        <Card className="border-dashed border-2 border-slate-200">
          <div className="text-center py-16 text-slate-400">
            <Sparkles className="w-12 h-12 mx-auto mb-3 opacity-30" />
            <p className="mb-1 text-slate-500">暂无指令配置</p>
            <p className="text-xs text-slate-300 mb-4">点击下方按钮创建第一条 AI 指令</p>
            <Button className="bg-purple-500 hover:bg-purple-600 text-white" onClick={openAddModal}>
              <Plus className="w-4 h-4 mr-1" />新增指令
            </Button>
          </div>
        </Card>
      ) : (
        <div className="grid gap-3">
          {prompts.map(p => {
            const typeInfo = getTypeLabel(p.type);
            return (
              <Card key={p.id} className="border-slate-100 shadow-sm hover:shadow-md transition-shadow overflow-hidden">
                <div className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2 flex-wrap">
                      <Badge className={typeInfo.color}>{typeInfo.label}</Badge>
                      <span className="font-semibold text-slate-900">{p.name}</span>
                      {p.is_default && <Badge className="bg-violet-100 text-violet-600 text-xs">默认</Badge>}
                      <Badge className={p.is_active ? 'bg-emerald-100 text-emerald-700 text-xs' : 'bg-slate-100 text-slate-400 text-xs'}>
                        {p.is_active ? '启用' : '禁用'}
                      </Badge>
                    </div>
                    <div className="flex items-center gap-1">
                      <Button size="sm" variant="outline" onClick={() => openEditModal(p)}>
                        <Edit3 className="w-3.5 h-3.5 mr-1" />编辑
                      </Button>
                    </div>
                  </div>

                  {p.system_prompt && (
                    <div className="mt-3 bg-violet-50/60 rounded-lg p-3 border border-violet-100">
                      <p className="text-xs font-medium text-violet-600 mb-1">系统提示词</p>
                      <p className="text-xs text-violet-800/80 whitespace-pre-wrap line-clamp-2">{p.system_prompt}</p>
                    </div>
                  )}

                  <div className="mt-3 bg-slate-50 rounded-lg p-3">
                    <p className="text-xs font-medium text-slate-500 mb-1">回复模板</p>
                    <p className="text-sm text-slate-700 whitespace-pre-wrap line-clamp-3">{p.template_text || '暂无内容'}</p>
                  </div>

                  {p.variables && p.variables.length > 0 && (
                    <div className="mt-2 flex items-center gap-1.5 flex-wrap">
                      {p.variables.map(v => (
                        <span key={v} className="text-xs bg-amber-50 text-amber-600 px-2 py-0.5 rounded border border-amber-100">
                          {'{{'}{v}{'}}'}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </Card>
            );
          })}
        </div>
      )}

      {/* 新增/编辑模态框 */}
      {modalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={() => setModalOpen(false)}>
          <Card className="w-[560px] max-h-[80vh] overflow-y-auto p-6 space-y-5" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-slate-900">{editingItem ? '编辑指令' : '新增指令'}</h3>
              <button className="text-slate-400 hover:text-slate-600" onClick={() => setModalOpen(false)}><X className="w-5 h-5" /></button>
            </div>

            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1 block">指令名称 <span className="text-rose-400">*</span></label>
                  <input
                    className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-purple-400 focus:ring-1 focus:ring-purple-200 transition"
                    placeholder="如：好评回复指令"
                    value={form.name}
                    onChange={e => setForm(p => ({ ...p, name: e.target.value }))}
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1 block">场景类型 <span className="text-rose-400">*</span></label>
                  <select
                    className="w-full p-2.5 border border-slate-200 rounded-lg text-sm bg-white focus:border-purple-400 focus:ring-1 focus:ring-purple-200 outline-none transition"
                    value={form.type}
                    onChange={e => setForm(p => ({ ...p, type: e.target.value }))}
                  >
                    {SCENARIO_TYPES.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
                  </select>
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">系统提示词（可选）</label>
                <textarea
                  className="w-full p-3 border border-slate-200 rounded-lg text-sm outline-none focus:border-purple-400 focus:ring-1 focus:ring-purple-200 transition min-h-[80px]"
                  placeholder="设定 AI 的角色和回复风格..."
                  value={form.system_prompt}
                  onChange={e => setForm(p => ({ ...p, system_prompt: e.target.value }))}
                />
              </div>

              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">回复模板内容 <span className="text-rose-400">*</span></label>
                <textarea
                  className="w-full p-3 border border-slate-200 rounded-lg text-sm outline-none focus:border-purple-400 focus:ring-1 focus:ring-purple-200 transition min-h-[180px]"
                  placeholder="编写 AI 回复模板，支持 {{变量}} 占位符..."
                  value={form.template_text}
                  onChange={e => setForm(p => ({ ...p, template_text: e.target.value }))}
                />
                <p className="text-xs text-slate-400 mt-1">支持变量: {'{{customer_name}}'}, {'{{store_name}}'}, {'{{review_content}}'}, {'{{review_rating}}'}</p>
              </div>

              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">状态</label>
                <div className="flex gap-2">
                  <button
                    type="button"
                    className={`px-4 py-2 rounded-lg text-sm font-medium border transition ${form.is_active ? 'bg-emerald-50 border-emerald-200 text-emerald-700' : 'bg-slate-50 border-slate-200 text-slate-500'}`}
                    onClick={() => setForm(p => ({ ...p, is_active: !p.is_active }))}
                  >
                    {form.is_active ? '启用' : '禁用'}
                  </button>
                </div>
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-1">
              <Button variant="ghost" onClick={() => setModalOpen(false)}>取消</Button>
              <Button
                className="bg-purple-500 hover:bg-purple-600 text-white"
                onClick={handleSave}
                disabled={saving || !form.name || !form.template_text}
              >
                {saving ? '保存中...' : <><Save className="w-4 h-4 mr-1" />{editingItem ? '保存' : '创建'}</>}
              </Button>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};

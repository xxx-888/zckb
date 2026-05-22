import React, { useState, useEffect, useCallback } from 'react';
import { Card } from '../../../components/ui/card';
import { Button } from '../../../components/ui/button';
import { Badge } from '../../../components/ui/badge';
import { useToast } from '../../../hooks/use-toast';
import { adminApi } from '../../../api/admin';
import { Plus, Trash2, Play, Edit3, RefreshCw, AlertCircle, Cpu, Check, X } from 'lucide-react';

interface AIModel {
  id: string;
  provider: string;
  model_name: string;
  api_key?: string;
  endpoint_url?: string;
  is_active: boolean;
  priority: number;
  max_tokens: number;
  temperature: number;
  config?: Record<string, any>;
}

interface ModelFormData {
  provider: string;
  model_name: string;
  api_key: string;
  endpoint_url: string;
  is_active: boolean;
  priority: number;
  max_tokens: number;
  temperature: number;
}

const PROVIDERS = [
  { value: 'openai', label: 'OpenAI' },
  { value: 'deepseek', label: 'DeepSeek' },
  { value: 'zhipu', label: '智谱AI' },
  { value: 'tongyi', label: '通义千问' },
  { value: 'hunyuan', label: '腾讯混元' },
  { value: 'doubao', label: '豆包' },
  { value: 'kimi', label: 'Kimi' },
  { value: 'local', label: '本地模型' },
];

const emptyForm: ModelFormData = {
  provider: 'openai',
  model_name: '',
  api_key: '',
  endpoint_url: '',
  is_active: true,
  priority: 0,
  max_tokens: 2048,
  temperature: 0.7,
};

export const ModelConfig: React.FC = () => {
  const [models, setModels] = useState<AIModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [testing, setTesting] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingModel, setEditingModel] = useState<AIModel | null>(null);
  const [form, setForm] = useState<ModelFormData>({ ...emptyForm });
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState<string | null>(null);

  const { success, error: toastError } = useToast();

  const fetchModels = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await adminApi.getAIModels();
      setModels(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err instanceof Error ? err.message : '获取失败');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchModels(); }, [fetchModels]);

  const openAddModal = () => {
    setEditingModel(null);
    setForm({ ...emptyForm });
    setModalOpen(true);
  };

  const openEditModal = (model: AIModel) => {
    setEditingModel(model);
    setForm({
      provider: model.provider,
      model_name: model.model_name,
      api_key: '', // API Key 不回显，留空则不更新
      endpoint_url: model.endpoint_url || '',
      is_active: model.is_active,
      priority: model.priority,
      max_tokens: model.max_tokens,
      temperature: model.temperature,
    });
    setModalOpen(true);
  };

  const handleSave = async () => {
    if (!form.model_name) {
      toastError('参数错误', '请填写模型名称');
      return;
    }
    if (!editingModel && !form.api_key) {
      toastError('参数错误', '新增模型需填写API密钥');
      return;
    }

    setSaving(true);
    try {
      const payload: any = {
        provider: form.provider,
        model_name: form.model_name,
        endpoint_url: form.endpoint_url || undefined,
        is_active: form.is_active,
        priority: form.priority,
        max_tokens: form.max_tokens,
        temperature: form.temperature,
      };
      if (form.api_key) payload.api_key = form.api_key;

      if (editingModel) {
        await adminApi.updateAIModel(editingModel.id, payload);
        success('更新成功', `模型 ${form.model_name} 已更新`);
      } else {
        await adminApi.createAIModel(payload);
        success('添加成功', `模型 ${form.model_name} 已添加`);
      }
      setModalOpen(false);
      fetchModels();
    } catch (err: any) {
      toastError(editingModel ? '更新失败' : '添加失败', err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: string) => {
    setDeleting(id);
    try {
      await adminApi.deleteAIModel(id);
      success('已删除', '模型已移除');
      fetchModels();
    } catch (err: any) {
      toastError('删除失败', err.message);
    } finally {
      setDeleting(null);
    }
  };

  const handleTest = async (id: string) => {
    setTesting(id);
    try {
      await adminApi.testAIModel(id);
      success('测试通过', '模型连接正常');
    } catch (err: any) {
      toastError('测试失败', err.message);
    } finally {
      setTesting(null);
    }
  };

  if (loading) return <div className="flex items-center justify-center h-64"><RefreshCw className="w-6 h-6 text-slate-400 animate-spin" /></div>;
  if (error) return <div className="flex flex-col items-center justify-center h-64 gap-4"><AlertCircle className="w-10 h-10 text-rose-400" /><p className="text-slate-500">{error}</p><Button variant="outline" onClick={fetchModels}>重试</Button></div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-bold text-slate-900">AI 模型配置</h2>
          <p className="text-sm text-slate-500">管理多 LLM 提供商模型接入</p>
        </div>
        <Button onClick={openAddModal}><Plus className="w-4 h-4 mr-1" />添加模型</Button>
      </div>

      {models.length === 0 ? (
        <div className="text-center py-16 text-slate-400">
          <Cpu className="w-12 h-12 mx-auto mb-3 opacity-30" />
          <p>暂无模型配置</p>
          <Button variant="outline" className="mt-4" onClick={openAddModal}><Plus className="w-4 h-4 mr-1" />添加第一个模型</Button>
        </div>
      ) : (
        <div className="grid gap-3">
          {models.map(m => (
            <Card key={m.id} className="p-4 border-slate-100 shadow-sm hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${m.is_active ? 'bg-violet-50' : 'bg-slate-50'}`}>
                    <Cpu className={`w-5 h-5 ${m.is_active ? 'text-violet-500' : 'text-slate-400'}`} />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-slate-900">{m.model_name}</span>
                      <Badge className={m.is_active ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-500'}>
                        {m.is_active ? '启用' : '禁用'}
                      </Badge>
                    </div>
                    <p className="text-xs text-slate-500 mt-0.5">
                      {PROVIDERS.find(p => p.value === m.provider)?.label || m.provider}
                      {' · '}max_tokens: {m.max_tokens}
                      {' · '}temp: {m.temperature}
                      {m.endpoint_url && ` · 自定义端点`}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-1.5">
                  <Button size="sm" variant="outline" onClick={() => openEditModal(m)} title="编辑">
                    <Edit3 className="w-3.5 h-3.5" />
                  </Button>
                  <Button size="sm" variant="outline" onClick={() => handleTest(m.id)} disabled={testing === m.id} title="测试连接">
                    <Play className={`w-3.5 h-3.5 ${testing === m.id ? 'animate-spin' : ''}`} />
                  </Button>
                  <Button size="sm" variant="ghost" className="text-rose-500 hover:text-rose-600 hover:bg-rose-50"
                    onClick={() => handleDelete(m.id)} disabled={deleting === m.id} title="删除">
                    <Trash2 className="w-3.5 h-3.5" />
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* 新增 / 编辑模态框 */}
      {modalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={() => setModalOpen(false)}>
          <Card className="w-[440px] p-6 space-y-5" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-slate-900">{editingModel ? '编辑模型' : '添加模型'}</h3>
              <button className="text-slate-400 hover:text-slate-600" onClick={() => setModalOpen(false)}><X className="w-5 h-5" /></button>
            </div>

            <div className="space-y-4">
              {/* 提供商 */}
              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">提供商</label>
                <select
                  className="w-full p-2.5 border border-slate-200 rounded-lg text-sm bg-white focus:border-violet-400 focus:ring-1 focus:ring-violet-200 outline-none transition"
                  value={form.provider}
                  onChange={e => setForm(p => ({ ...p, provider: e.target.value }))}
                >
                  {PROVIDERS.map(p => <option key={p.value} value={p.value}>{p.label}</option>)}
                </select>
              </div>

              {/* 模型名称 */}
              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">模型名称</label>
                <input
                  className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-violet-400 focus:ring-1 focus:ring-violet-200 transition"
                  placeholder="如 gpt-4o、deepseek-chat"
                  value={form.model_name}
                  onChange={e => setForm(p => ({ ...p, model_name: e.target.value }))}
                />
              </div>

              {/* API Key */}
              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">
                  API Key {editingModel && <span className="text-slate-400 font-normal">（留空则不更新）</span>}
                </label>
                <input
                  className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-violet-400 focus:ring-1 focus:ring-violet-200 transition"
                  type="password"
                  placeholder={editingModel ? '输入新 Key 则更新' : 'sk-xxx'}
                  value={form.api_key}
                  onChange={e => setForm(p => ({ ...p, api_key: e.target.value }))}
                />
              </div>

              {/* 端点 URL */}
              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">API 端点（可选）</label>
                <input
                  className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-violet-400 focus:ring-1 focus:ring-violet-200 transition"
                  placeholder="https://api.openai.com/v1"
                  value={form.endpoint_url}
                  onChange={e => setForm(p => ({ ...p, endpoint_url: e.target.value }))}
                />
              </div>

              {/* 参数行 */}
              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1 block">状态</label>
                  <button
                    type="button"
                    className={`w-full p-2.5 rounded-lg text-sm font-medium border transition ${form.is_active ? 'bg-emerald-50 border-emerald-200 text-emerald-700' : 'bg-slate-50 border-slate-200 text-slate-500'}`}
                    onClick={() => setForm(p => ({ ...p, is_active: !p.is_active }))}
                  >
                    {form.is_active ? '启用' : '禁用'}
                  </button>
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1 block">优先级</label>
                  <input
                    className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-violet-400 focus:ring-1 focus:ring-violet-200 transition"
                    type="number"
                    min={0}
                    value={form.priority}
                    onChange={e => setForm(p => ({ ...p, priority: parseInt(e.target.value) || 0 }))}
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1 block">温度</label>
                  <input
                    className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-violet-400 focus:ring-1 focus:ring-violet-200 transition"
                    type="number"
                    min={0}
                    max={2}
                    step={0.1}
                    value={form.temperature}
                    onChange={e => setForm(p => ({ ...p, temperature: parseFloat(e.target.value) || 0 }))}
                  />
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">最大 Tokens</label>
                <input
                  className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-violet-400 focus:ring-1 focus:ring-violet-200 transition"
                  type="number"
                  min={1}
                  value={form.max_tokens}
                  onChange={e => setForm(p => ({ ...p, max_tokens: parseInt(e.target.value) || 2048 }))}
                />
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-1">
              <Button variant="ghost" onClick={() => setModalOpen(false)}>取消</Button>
              <Button
                className="bg-violet-500 hover:bg-violet-600 text-white"
                onClick={handleSave}
                disabled={saving}
              >
                {saving ? '保存中...' : (editingModel ? <><Check className="w-4 h-4 mr-1" />更新</> : <><Plus className="w-4 h-4 mr-1" />添加</>)}
              </Button>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};

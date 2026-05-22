import React, { useState, useEffect, useCallback } from 'react';
import { Card } from '../../../components/ui/card';
import { Button } from '../../../components/ui/button';
import { Badge } from '../../../components/ui/badge';
import { useToast } from '../../../hooks/use-toast';
import { adminApi } from '../../../api/admin';
import { Plus, Trash2, Edit3, RefreshCw, AlertCircle, Cpu, Check, X, Send, Loader2, Zap, Clock, Coins, ArrowUpRight, ArrowDownRight, Globe, KeyRound } from 'lucide-react';

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

interface TestResult {
  success: boolean;
  message: string;
  reply?: string;
  latency_ms: number;
  model_name?: string;
  provider?: string;
  usage?: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
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

const PROVIDER_ENDPOINTS: Record<string, string> = {
  openai: 'https://api.openai.com/v1/chat/completions',
  deepseek: 'https://api.deepseek.com/v1/chat/completions',
  zhipu: 'https://open.bigmodel.cn/api/paas/v4/chat/completions',
  tongyi: 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
  hunyuan: 'https://api.hunyuan.cloud.tencent.com/v1/chat/completions',
  doubao: 'https://ark.cn-beijing.volces.com/api/v3/chat/completions',
  kimi: 'https://api.moonshot.cn/v1/chat/completions',
  wenxin: 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{model}',
  local: 'http://localhost:11434/v1/chat/completions',
};

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

function getLatencyColor(ms: number): string {
  if (ms < 1000) return 'text-emerald-600';
  if (ms < 3000) return 'text-amber-600';
  return 'text-rose-600';
}

function getLatencyLabel(ms: number): string {
  if (ms < 500) return '极快';
  if (ms < 1000) return '快速';
  if (ms < 3000) return '正常';
  if (ms < 10000) return '较慢';
  return '很慢';
}

export const ModelConfig: React.FC = () => {
  const [models, setModels] = useState<AIModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingModel, setEditingModel] = useState<AIModel | null>(null);
  const [form, setForm] = useState<ModelFormData>({ ...emptyForm });
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState<string | null>(null);

  // 测试对话框状态
  const [testModalOpen, setTestModalOpen] = useState(false);
  const [testingModel, setTestingModel] = useState<AIModel | null>(null);
  const [testMessage, setTestMessage] = useState('');
  const [testApiKey, setTestApiKey] = useState('');
  const [testLoading, setTestLoading] = useState(false);
  const [testResult, setTestResult] = useState<TestResult | null>(null);

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
      api_key: '',
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

  const openTestModal = (model: AIModel) => {
    setTestingModel(model);
    setTestMessage('你好，请用一句话简单介绍一下你自己。');
    setTestApiKey('');
    setTestResult(null);
    setTestLoading(false);
    setTestModalOpen(true);
  };

  const handleTest = async () => {
    if (!testingModel) return;
    setTestLoading(true);
    setTestResult(null);
    try {
      const resp = await adminApi.testAIModel(testingModel.id, testMessage, testApiKey || undefined);
      // 拦截器已解一层 data，resp = {code, message, data: {...}}
      const result = resp.data || resp;
      console.log('[模型测试] 原始响应:', resp);
      console.log('[模型测试] 解析结果:', result);
      console.log('[模型测试] reply:', result?.reply, 'success:', result?.success);
      setTestResult(result);
    } catch (err: any) {
      setTestResult({
        success: false,
        message: err.message || '测试请求失败',
        latency_ms: 0,
      });
    } finally {
      setTestLoading(false);
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
                      {m.endpoint_url && ' · 自定义端点'}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-1.5">
                  <Button size="sm" variant="outline" onClick={() => openEditModal(m)} title="编辑">
                    <Edit3 className="w-3.5 h-3.5" />
                  </Button>
                  <Button size="sm" variant="outline" onClick={() => openTestModal(m)} title="测试连接">
                    <Zap className="w-3.5 h-3.5" />
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
              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">提供商</label>
                <select className="w-full p-2.5 border border-slate-200 rounded-lg text-sm bg-white focus:border-violet-400 focus:ring-1 focus:ring-violet-200 outline-none transition" value={form.provider} onChange={e => setForm(p => ({ ...p, provider: e.target.value }))}>
                  {PROVIDERS.map(p => <option key={p.value} value={p.value}>{p.label}</option>)}
                </select>
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">模型名称</label>
                <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-violet-400 focus:ring-1 focus:ring-violet-200 transition" placeholder="如 gpt-4o、deepseek-chat" value={form.model_name} onChange={e => setForm(p => ({ ...p, model_name: e.target.value }))} />
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">API Key {editingModel && <span className="text-slate-400 font-normal">（留空则不更新）</span>}</label>
                <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-violet-400 focus:ring-1 focus:ring-violet-200 transition" type="password" placeholder={editingModel ? '输入新 Key 则更新' : 'sk-xxx'} value={form.api_key} onChange={e => setForm(p => ({ ...p, api_key: e.target.value }))} />
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">API 端点（可选）</label>
                <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-violet-400 focus:ring-1 focus:ring-violet-200 transition" placeholder="https://api.openai.com/v1" value={form.endpoint_url} onChange={e => setForm(p => ({ ...p, endpoint_url: e.target.value }))} />
              </div>
              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1 block">状态</label>
                  <button type="button" className={`w-full p-2.5 rounded-lg text-sm font-medium border transition ${form.is_active ? 'bg-emerald-50 border-emerald-200 text-emerald-700' : 'bg-slate-50 border-slate-200 text-slate-500'}`} onClick={() => setForm(p => ({ ...p, is_active: !p.is_active }))}>
                    {form.is_active ? '启用' : '禁用'}
                  </button>
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1 block">优先级</label>
                  <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-violet-400 focus:ring-1 focus:ring-violet-200 transition" type="number" min={0} value={form.priority} onChange={e => setForm(p => ({ ...p, priority: parseInt(e.target.value) || 0 }))} />
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1 block">温度</label>
                  <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-violet-400 focus:ring-1 focus:ring-violet-200 transition" type="number" min={0} max={2} step={0.1} value={form.temperature} onChange={e => setForm(p => ({ ...p, temperature: parseFloat(e.target.value) || 0 }))} />
                </div>
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">最大 Tokens</label>
                <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-violet-400 focus:ring-1 focus:ring-violet-200 transition" type="number" min={1} value={form.max_tokens} onChange={e => setForm(p => ({ ...p, max_tokens: parseInt(e.target.value) || 2048 }))} />
              </div>
            </div>
            <div className="flex justify-end gap-3 pt-1">
              <Button variant="ghost" onClick={() => setModalOpen(false)}>取消</Button>
              <Button className="bg-violet-500 hover:bg-violet-600 text-white" onClick={handleSave} disabled={saving}>
                {saving ? '保存中...' : (editingModel ? <><Check className="w-4 h-4 mr-1" />更新</> : <><Plus className="w-4 h-4 mr-1" />添加</>)}
              </Button>
            </div>
          </Card>
        </div>
      )}

      {/* ========== 测试对话框（完整版） ========== */}
      {testModalOpen && testingModel && (
        <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-black/40 pt-8 pb-8" onClick={() => setTestModalOpen(false)}>
          <div className="w-[600px] my-auto" onClick={e => e.stopPropagation()}>
            <Card className="space-y-0">
              {/* 头部 */}
              <div className="px-6 py-4 border-b border-slate-100 bg-gradient-to-r from-violet-50 to-slate-50">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-violet-100 flex items-center justify-center">
                      <Zap className="w-5 h-5 text-violet-600" />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-900">模型测试</h3>
                      <p className="text-xs text-slate-500">
                        {PROVIDERS.find(p => p.value === testingModel.provider)?.label || testingModel.provider}
                        {' · '}{testingModel.model_name}
                      </p>
                    </div>
                  </div>
                  <button className="w-8 h-8 rounded-lg flex items-center justify-center text-slate-400 hover:text-slate-600 hover:bg-white/60 transition" onClick={() => setTestModalOpen(false)}>
                    <X className="w-4 h-4" />
                  </button>
                </div>
              </div>

              <div className="p-6 space-y-5">
                {/* 模型参数快览 */}
                <div className="grid grid-cols-4 gap-2">
                  {[
                    { label: '提供商', value: PROVIDERS.find(p => p.value === testingModel.provider)?.label || testingModel.provider, icon: Globe },
                    { label: '状态', value: testingModel.is_active ? '启用' : '禁用', icon: Cpu },
                    { label: '温度', value: String(testingModel.temperature), icon: Cpu },
                    { label: '最大 Tokens', value: String(testingModel.max_tokens), icon: Coins },
                  ].map(item => (
                    <div key={item.label} className="bg-slate-50 rounded-lg px-3 py-2">
                      <p className="text-[10px] text-slate-400 font-medium uppercase tracking-wide">{item.label}</p>
                      <p className="text-sm font-semibold text-slate-700 mt-0.5">{item.value}</p>
                    </div>
                  ))}
                </div>

                {/* API Key 输入 */}
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1.5 flex items-center gap-1.5">
                    <KeyRound className="w-3.5 h-3.5 text-slate-400" />
                    API Key
                    <span className="text-xs text-slate-400 font-normal">（新模型可留空，旧模型需手动输入）</span>
                  </label>
                  <input
                    className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-violet-400 focus:ring-1 focus:ring-violet-200 transition"
                    type="password"
                    placeholder={testingModel.provider === 'wenxin' ? '输入百度 access_token' : '输入 API Key'}
                    value={testApiKey}
                    onChange={e => setTestApiKey(e.target.value)}
                    disabled={testLoading}
                  />
                </div>

                {/* 测试消息 */}
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1.5 flex items-center gap-1.5">
                    <Send className="w-3.5 h-3.5 text-slate-400" />
                    测试消息
                  </label>
                  <textarea
                    className="w-full p-3 border border-slate-200 rounded-lg text-sm outline-none focus:border-violet-400 focus:ring-1 focus:ring-violet-200 transition resize-none"
                    rows={3}
                    placeholder="输入你想让模型回答的内容..."
                    value={testMessage}
                    onChange={e => setTestMessage(e.target.value)}
                    disabled={testLoading}
                  />
                </div>

                {/* 发送按钮 */}
                <Button
                  className="w-full bg-violet-500 hover:bg-violet-600 text-white h-11"
                  onClick={handleTest}
                  disabled={testLoading || !testMessage.trim()}
                >
                  {testLoading ? (
                    <><Loader2 className="w-4 h-4 mr-2 animate-spin" />正在调用模型 API，请等待响应...</>
                  ) : (
                    <><Send className="w-4 h-4 mr-2" />发送测试请求</>
                  )}
                </Button>

                {/* ========== 测试结果面板 ========== */}
                {testResult && (
                  <div className="space-y-4">
                    {/* 调试信息 */}
                    <details className="text-xs text-slate-400">
                      <summary className="cursor-pointer hover:text-slate-600">原始响应数据（调试用）</summary>
                      <pre className="mt-1 bg-slate-50 rounded-lg p-2 overflow-auto max-h-32 text-[11px] font-mono">
                        {JSON.stringify(testResult, null, 2)}
                      </pre>
                    </details>

                    {/* 分割线 */}
                    <div className="flex items-center gap-3">
                      <div className="flex-1 h-px bg-slate-200" />
                      <span className="text-xs font-medium text-slate-400">测试结果</span>
                      <div className="flex-1 h-px bg-slate-200" />
                    </div>

                    {/* 状态总览条 */}
                    <div className={`rounded-xl border-2 p-4 ${testResult.success
                      ? 'bg-gradient-to-br from-emerald-50 to-white border-emerald-200'
                      : 'bg-gradient-to-br from-rose-50 to-white border-rose-200'
                    }`}>
                      <div className="flex items-center gap-3">
                        <div className={`w-10 h-10 rounded-full flex items-center justify-center ${testResult.success ? 'bg-emerald-100' : 'bg-rose-100'}`}>
                          {testResult.success
                            ? <Check className="w-5 h-5 text-emerald-600" />
                            : <AlertCircle className="w-5 h-5 text-rose-500" />
                          }
                        </div>
                        <div className="flex-1">
                          <p className={`font-bold ${testResult.success ? 'text-emerald-700' : 'text-rose-700'}`}>
                            {testResult.success ? '连接成功 · 模型可用' : '连接失败'}
                          </p>
                          <p className={`text-xs mt-0.5 ${testResult.success ? 'text-emerald-500' : 'text-rose-500'}`}>
                            {testResult.success ? testResult.message : testResult.message}
                          </p>
                        </div>
                      </div>
                    </div>

                    {/* 指标卡片行 */}
                    {testResult.success && (
                      <div className="grid grid-cols-3 gap-3">
                        {/* 响应耗时 */}
                        <div className="bg-white rounded-xl border border-slate-100 p-3 text-center shadow-sm">
                          <Clock className={`w-5 h-5 mx-auto mb-1.5 ${getLatencyColor(testResult.latency_ms)}`} />
                          <p className="text-2xl font-bold text-slate-900">{testResult.latency_ms}</p>
                          <p className="text-xs text-slate-400">毫秒 (ms)</p>
                          <Badge className={`mt-1.5 text-[10px] ${testResult.latency_ms < 1000 ? 'bg-emerald-100 text-emerald-700' : testResult.latency_ms < 3000 ? 'bg-amber-100 text-amber-700' : 'bg-rose-100 text-rose-700'}`}>
                            {getLatencyLabel(testResult.latency_ms)}
                          </Badge>
                        </div>

                        {/* Token 用量 */}
                        <div className="bg-white rounded-xl border border-slate-100 p-3 text-center shadow-sm">
                          <Coins className="w-5 h-5 mx-auto mb-1.5 text-violet-500" />
                          <p className="text-2xl font-bold text-slate-900">{testResult.usage?.total_tokens || '-'}</p>
                          <p className="text-xs text-slate-400">Token 总量</p>
                          {testResult.usage && (
                            <div className="flex items-center justify-center gap-2 mt-1.5">
                              <span className="text-[10px] flex items-center gap-0.5 text-blue-500">
                                <ArrowDownRight className="w-2.5 h-2.5" />{testResult.usage.prompt_tokens}
                              </span>
                              <span className="text-[10px] flex items-center gap-0.5 text-emerald-500">
                                <ArrowUpRight className="w-2.5 h-2.5" />{testResult.usage.completion_tokens}
                              </span>
                            </div>
                          )}
                        </div>

                        {/* 模型信息 */}
                        <div className="bg-white rounded-xl border border-slate-100 p-3 text-center shadow-sm">
                          <Cpu className="w-5 h-5 mx-auto mb-1.5 text-blue-500" />
                          <p className="text-xs font-bold text-slate-900 truncate px-1" title={testResult.model_name || testingModel.model_name}>
                            {testResult.model_name || testingModel.model_name}
                          </p>
                          <p className="text-xs text-slate-400 mt-1">
                            {testResult.provider ? (PROVIDERS.find(p => p.value === testResult.provider)?.label || testResult.provider) : (PROVIDERS.find(p => p.value === testingModel.provider)?.label || testingModel.provider)}
                          </p>
                          <Badge className="mt-1.5 text-[10px] bg-blue-100 text-blue-700">在线</Badge>
                        </div>
                      </div>
                    )}

                    {/* 耗时进度条 */}
                    {testResult.success && (
                      <div>
                        <div className="flex items-center justify-between mb-1.5">
                          <span className="text-xs text-slate-500 font-medium">响应时间分布</span>
                          <span className={`text-xs font-bold ${getLatencyColor(testResult.latency_ms)}`}>
                            {testResult.latency_ms}ms · {getLatencyLabel(testResult.latency_ms)}
                          </span>
                        </div>
                        <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full transition-all duration-700 ${testResult.latency_ms < 1000 ? 'bg-gradient-to-r from-emerald-400 to-emerald-500' : testResult.latency_ms < 3000 ? 'bg-gradient-to-r from-amber-400 to-amber-500' : 'bg-gradient-to-r from-rose-400 to-rose-500'}`}
                            style={{ width: `${Math.min(100, (testResult.latency_ms / 10000) * 100)}%` }}
                          />
                        </div>
                        <div className="flex justify-between mt-1">
                          <span className="text-[10px] text-slate-300">0ms</span>
                          <span className="text-[10px] text-slate-300">5s</span>
                          <span className="text-[10px] text-slate-300">10s+</span>
                        </div>
                      </div>
                    )}

                    {/* Token 用量可视化 */}
                    {testResult.success && testResult.usage && testResult.usage.total_tokens > 0 && (
                      <div>
                        <div className="flex items-center justify-between mb-1.5">
                          <span className="text-xs text-slate-500 font-medium">Token 用量分布</span>
                          <span className="text-xs text-slate-400">
                            总计 {testResult.usage.total_tokens} tokens
                          </span>
                        </div>
                        <div className="w-full h-2.5 bg-slate-100 rounded-full overflow-hidden flex">
                          <div
                            className="h-full bg-blue-400 transition-all duration-700"
                            style={{ width: `${(testResult.usage.prompt_tokens / testResult.usage.total_tokens) * 100}%` }}
                            title={`输入: ${testResult.usage.prompt_tokens}`}
                          />
                          <div
                            className="h-full bg-emerald-400 transition-all duration-700"
                            style={{ width: `${(testResult.usage.completion_tokens / testResult.usage.total_tokens) * 100}%` }}
                            title={`输出: ${testResult.usage.completion_tokens}`}
                          />
                        </div>
                        <div className="flex items-center gap-4 mt-1.5">
                          <span className="flex items-center gap-1 text-[10px] text-slate-500">
                            <span className="w-2 h-2 rounded-full bg-blue-400" />输入 {testResult.usage.prompt_tokens}
                          </span>
                          <span className="flex items-center gap-1 text-[10px] text-slate-500">
                            <span className="w-2 h-2 rounded-full bg-emerald-400" />输出 {testResult.usage.completion_tokens}
                          </span>
                        </div>
                      </div>
                    )}

                    {/* 请求详情 */}
                    {testResult.success && (
                      <div className="bg-slate-50 rounded-xl p-4 space-y-2">
                        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">请求详情</p>
                        <div className="grid grid-cols-2 gap-x-6 gap-y-1.5 text-xs">
                          <div className="flex justify-between">
                            <span className="text-slate-400">API 端点</span>
                            <span className="text-slate-600 font-mono text-[11px] truncate ml-2 max-w-[200px]" title={testingModel.endpoint_url || PROVIDER_ENDPOINTS[testingModel.provider] || '默认'}>
                              {testingModel.endpoint_url ? '自定义' : '默认'}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-400">认证方式</span>
                            <span className="text-slate-600">{testingModel.provider === 'wenxin' ? 'access_token' : 'Bearer Token'}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-400">max_tokens</span>
                            <span className="text-slate-600">1024</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-400">temperature</span>
                            <span className="text-slate-600">{testingModel.temperature}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-400">API Key</span>
                            <span className="text-slate-600">{testApiKey ? '手动输入' : '已存储'}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-400">HTTP 状态</span>
                            <span className="text-emerald-600 font-medium">200 OK</span>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* 模型回复内容 */}
                    {testResult.success && testResult.reply !== undefined && (
                      <div>
                        <div className="flex items-center justify-between mb-2">
                          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">模型回复</p>
                          <span className="text-[10px] text-slate-400 bg-slate-100 px-2 py-0.5 rounded-full">
                            {testResult.reply.length} 字符
                          </span>
                        </div>
                        <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm relative">
                          <div className="absolute top-3 right-3">
                            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                          </div>
                          <div className="text-sm text-slate-800 leading-relaxed whitespace-pre-wrap pr-4">
                            {testResult.reply || '（模型返回了空内容）'}
                          </div>
                        </div>
                      </div>
                    )}

                    {/* 模型回复为空提示 */}
                    {testResult.success && testResult.reply === undefined && (
                      <div className="bg-amber-50 border border-amber-200 rounded-xl p-4">
                        <div className="flex items-center gap-2">
                          <AlertCircle className="w-4 h-4 text-amber-500" />
                          <p className="text-sm text-amber-700">模型连接成功，但未返回回复内容。请检查后端日志确认 API 调用是否正常。</p>
                        </div>
                      </div>
                    )}

                    {/* 失败详情 */}
                    {!testResult.success && (
                      <div className="bg-rose-50 rounded-xl p-4 border border-rose-100">
                        <p className="text-xs font-semibold text-rose-400 uppercase tracking-wide mb-2">错误详情</p>
                        <div className="bg-white rounded-lg p-3 border border-rose-100">
                          <p className="text-sm text-rose-700 whitespace-pre-wrap break-all">{testResult.message}</p>
                        </div>
                        {testResult.reply && (
                          <div className="mt-3 bg-white rounded-lg p-3 border border-rose-100">
                            <p className="text-xs text-rose-400 mb-1">厂商返回内容：</p>
                            <p className="text-sm text-rose-700 whitespace-pre-wrap">{testResult.reply}</p>
                          </div>
                        )}
                        <div className="mt-3 space-y-1.5">
                          <p className="text-xs text-rose-400 font-medium">常见原因：</p>
                          <ul className="text-xs text-rose-500 space-y-1 pl-3">
                            <li className="list-disc">API Key 无效或已过期</li>
                            <li className="list-disc">API 端点 URL 不正确</li>
                            <li className="list-disc">模型名称与提供商不匹配</li>
                            <li className="list-disc">网络无法访问厂商服务器（代理/防火墙）</li>
                            <li className="list-disc">账户余额不足或调用超限</li>
                          </ul>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </Card>
          </div>
        </div>
      )}
    </div>
  );
};

import React, { useState, useEffect, useCallback } from 'react';
import { Card } from '../../../components/ui/card';
import { Button } from '../../../components/ui/button';
import { Badge } from '../../../components/ui/badge';
import { useToast } from '../../../hooks/use-toast';
import { adminApi } from '../../../api/admin';
import { Sparkles, RefreshCw, AlertCircle, Save, Plus, Edit3, X, Send, Loader2, Zap, Clock, Coins, Cpu, Globe, KeyRound, Check } from 'lucide-react';

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

interface ModelOption {
  id: string;
  provider: string;
  model_name: string;
  is_active: boolean;
}

const PROVIDERS: Record<string, string> = {
  openai: 'OpenAI', deepseek: 'DeepSeek', zhipu: '智谱AI', tongyi: '通义千问',
  hunyuan: '腾讯混元', doubao: '豆包', kimi: 'Kimi', local: '本地模型', wenxin: '文心一言',
};

interface TestResult {
  success: boolean;
  reply?: string;
  latency_ms?: number;
  usage?: { prompt_tokens: number; completion_tokens: number; total_tokens: number };
  error?: string;
  model_name?: string;
  provider?: string;
  rendered_prompt?: string;
  system_prompt_used?: string;
}

const emptyForm = { name: '', type: 'good_review', template_text: '', system_prompt: '', is_active: true };

export const PromptConfig: React.FC = () => {
  const [prompts, setPrompts] = useState<PromptItem[]>([]);
  const [models, setModels] = useState<ModelOption[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<PromptItem | null>(null);
  const [form, setForm] = useState({ ...emptyForm });
  const [saving, setSaving] = useState(false);

  // 测试状态
  const [testOpen, setTestOpen] = useState(false);
  const [testModelId, setTestModelId] = useState('');
  const [testPromptId, setTestPromptId] = useState('');
  const [testMessage, setTestMessage] = useState('');
  const [testVariables, setTestVariables] = useState('');
  const [testApiKey, setTestApiKey] = useState('');
  const [testTemp, setTestTemp] = useState(0.7);
  const [testLoading, setTestLoading] = useState(false);
  const [testResult, setTestResult] = useState<TestResult | null>(null);

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

  const fetchModels = useCallback(async () => {
    try {
      const data = await adminApi.getAIModels().catch(() => []);
      setModels(Array.isArray(data) ? data : []);
    } catch { /* ignore */ }
  }, []);

  useEffect(() => { fetchPrompts(); fetchModels(); }, [fetchPrompts, fetchModels]);

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

  const openTest = (item?: PromptItem) => {
    setTestPromptId(item?.id || '');
    setTestMessage(item?.template_text || '');
    // 如果模板有变量，自动填充变量示例
    if (item?.variables && item.variables.length > 0) {
      const vars: Record<string, string> = {};
      item.variables.forEach(v => { vars[v] = `示例${v}`; });
      setTestVariables(JSON.stringify(vars, null, 2));
    } else {
      setTestVariables('');
    }
    setTestResult(null);
    setTestApiKey('');
    setTestOpen(true);
  };

  const handleSave = async () => {
    if (!form.name || !form.template_text) {
      toastError('参数错误', '请填写指令名称和模板内容');
      return;
    }
    setSaving(true);
    try {
      const payload: any = {
        name: form.name, type: form.type, template_text: form.template_text,
        system_prompt: form.system_prompt || undefined, is_active: form.is_active,
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

  const handleTest = async () => {
    if (!testModelId || !testMessage) {
      toastError('参数错误', '请选择模型并输入测试内容');
      return;
    }
    setTestLoading(true);
    setTestResult(null);
    try {
      let variables = {};
      if (testVariables.trim()) {
        try { variables = JSON.parse(testVariables); }
        catch { toastError('格式错误', '变量 JSON 格式不正确'); setTestLoading(false); return; }
      }
      const resp = await adminApi.testAIPrompt({
        model_id: testModelId,
        prompt_id: testPromptId || undefined,
        user_message: testMessage,
        variables: Object.keys(variables).length > 0 ? variables : undefined,
        api_key: testApiKey || undefined,
        temperature: testTemp,
      });
      const result = resp.data || resp;
      console.log('[指令测试] 结果:', result);
      setTestResult(result);
    } catch (err: any) {
      setTestResult({ success: false, error: err.message || '测试请求失败' });
    } finally {
      setTestLoading(false);
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
          <Button variant="outline" size="sm" onClick={() => openTest()} className="bg-purple-50 border-purple-200 text-purple-700 hover:bg-purple-100">
            <Zap className="w-4 h-4 mr-1" />在线测试
          </Button>
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
            <Button className="bg-purple-500 hover:bg-purple-600 text-white mt-4" onClick={openAddModal}>
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
                      <Button size="sm" variant="outline" className="text-purple-600 hover:bg-purple-50" onClick={() => openTest(p)}>
                        <Zap className="w-3.5 h-3.5" />
                      </Button>
                      <Button size="sm" variant="outline" onClick={() => openEditModal(p)}>
                        <Edit3 className="w-3.5 h-3.5" />
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
                  <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-purple-400 focus:ring-1 focus:ring-purple-200 transition" placeholder="如：好评回复指令" value={form.name} onChange={e => setForm(p => ({ ...p, name: e.target.value }))} />
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1 block">场景类型 <span className="text-rose-400">*</span></label>
                  <select className="w-full p-2.5 border border-slate-200 rounded-lg text-sm bg-white focus:border-purple-400 focus:ring-1 focus:ring-purple-200 outline-none transition" value={form.type} onChange={e => setForm(p => ({ ...p, type: e.target.value }))}>
                    {SCENARIO_TYPES.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
                  </select>
                </div>
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">系统提示词（可选）</label>
                <textarea className="w-full p-3 border border-slate-200 rounded-lg text-sm outline-none focus:border-purple-400 focus:ring-1 focus:ring-purple-200 transition min-h-[80px]" placeholder="设定 AI 的角色和回复风格..." value={form.system_prompt} onChange={e => setForm(p => ({ ...p, system_prompt: e.target.value }))} />
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">回复模板内容 <span className="text-rose-400">*</span></label>
                <textarea className="w-full p-3 border border-slate-200 rounded-lg text-sm outline-none focus:border-purple-400 focus:ring-1 focus:ring-purple-200 transition min-h-[180px]" placeholder="编写 AI 回复模板，支持 {{变量}} 占位符..." value={form.template_text} onChange={e => setForm(p => ({ ...p, template_text: e.target.value }))} />
                <p className="text-xs text-slate-400 mt-1">支持变量: {'{{customer_name}}'}, {'{{store_name}}'}, {'{{review_content}}'}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">状态</label>
                <button type="button" className={`px-4 py-2 rounded-lg text-sm font-medium border transition ${form.is_active ? 'bg-emerald-50 border-emerald-200 text-emerald-700' : 'bg-slate-50 border-slate-200 text-slate-500'}`} onClick={() => setForm(p => ({ ...p, is_active: !p.is_active }))}>{form.is_active ? '启用' : '禁用'}</button>
              </div>
            </div>
            <div className="flex justify-end gap-3 pt-1">
              <Button variant="ghost" onClick={() => setModalOpen(false)}>取消</Button>
              <Button className="bg-purple-500 hover:bg-purple-600 text-white" onClick={handleSave} disabled={saving || !form.name || !form.template_text}>{saving ? '保存中...' : <><Save className="w-4 h-4 mr-1" />{editingItem ? '保存' : '创建'}</>}</Button>
            </div>
          </Card>
        </div>
      )}

      {/* ========== 在线测试对话框 ========== */}
      {testOpen && (
        <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-black/40 pt-8 pb-8" onClick={() => setTestOpen(false)}>
          <div className="w-[640px] my-auto" onClick={e => e.stopPropagation()}>
            <Card>
              {/* 头部 */}
              <div className="px-6 py-4 border-b border-slate-100 bg-gradient-to-r from-purple-50 to-slate-50">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-purple-100 flex items-center justify-center"><Zap className="w-5 h-5 text-purple-600" /></div>
                    <div>
                      <h3 className="font-bold text-slate-900">指令在线测试</h3>
                      <p className="text-xs text-slate-500">选择模型和模板，测试指令效果</p>
                    </div>
                  </div>
                  <button className="w-8 h-8 rounded-lg flex items-center justify-center text-slate-400 hover:text-slate-600 hover:bg-white/60 transition" onClick={() => setTestOpen(false)}><X className="w-4 h-4" /></button>
                </div>
              </div>

              <div className="p-6 space-y-4">
                {/* 模型选择 */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-sm font-medium text-slate-700 mb-1.5 block">AI 模型 <span className="text-rose-400">*</span></label>
                    <select className="w-full p-2.5 border border-slate-200 rounded-lg text-sm bg-white focus:border-purple-400 focus:ring-1 focus:ring-purple-200 outline-none transition" value={testModelId} onChange={e => setTestModelId(e.target.value)}>
                      <option value="">-- 选择模型 --</option>
                      {models.filter(m => m.is_active).map(m => (
                        <option key={m.id} value={m.id}>{PROVIDERS[m.provider] || m.provider} · {m.model_name}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-slate-700 mb-1.5 block">指令模板</label>
                    <select className="w-full p-2.5 border border-slate-200 rounded-lg text-sm bg-white focus:border-purple-400 focus:ring-1 focus:ring-purple-200 outline-none transition" value={testPromptId} onChange={e => {
                      setTestPromptId(e.target.value);
                      const p = prompts.find(x => x.id === e.target.value);
                      if (p) {
                        setTestMessage(p.template_text);
                        if (p.variables && p.variables.length > 0) {
                          const vars: Record<string, string> = {};
                          p.variables.forEach(v => { vars[v] = `示例${v}`; });
                          setTestVariables(JSON.stringify(vars, null, 2));
                        }
                      } else {
                        setTestMessage('');
                        setTestVariables('');
                      }
                    }}>
                      <option value="">-- 不使用模板 --</option>
                      {prompts.filter(p => p.is_active).map(p => (
                        <option key={p.id} value={p.id}>{p.name} ({getTypeLabel(p.type).label})</option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* API Key */}
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1.5 flex items-center gap-1.5">
                    <KeyRound className="w-3.5 h-3.5 text-slate-400" />API Key
                    <span className="text-xs text-slate-400 font-normal">（新模型可留空）</span>
                  </label>
                  <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-purple-400 focus:ring-1 focus:ring-purple-200 transition" type="password" placeholder="输入 API Key" value={testApiKey} onChange={e => setTestApiKey(e.target.value)} disabled={testLoading} />
                </div>

                {/* 变量替换 */}
                {testPromptId && (
                  <div>
                    <label className="text-sm font-medium text-slate-700 mb-1.5 block">模板变量 (JSON)</label>
                    <textarea className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-purple-400 focus:ring-1 focus:ring-purple-200 transition font-mono resize-none" rows={3} placeholder='{"store_name": "测试门店", "customer_name": "张先生"}' value={testVariables} onChange={e => setTestVariables(e.target.value)} disabled={testLoading} />
                  </div>
                )}

                {/* 测试消息 */}
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1.5 block">测试消息</label>
                  <textarea className="w-full p-3 border border-slate-200 rounded-lg text-sm outline-none focus:border-purple-400 focus:ring-1 focus:ring-purple-200 transition resize-none" rows={4} placeholder="输入测试消息或直接发送模板内容..." value={testMessage} onChange={e => setTestMessage(e.target.value)} disabled={testLoading} />
                </div>

                {/* 参数行 */}
                <div className="flex items-center gap-3">
                  <div className="flex-1">
                    <label className="text-xs text-slate-500 mb-1 block">Temperature</label>
                    <input className="w-full p-2 border border-slate-200 rounded-lg text-sm outline-none focus:border-purple-400 transition" type="number" min={0} max={2} step={0.1} value={testTemp} onChange={e => setTestTemp(parseFloat(e.target.value) || 0)} />
                  </div>
                  <div className="flex-1" />
                </div>

                {/* 发送 */}
                <Button className="w-full bg-purple-500 hover:bg-purple-600 text-white h-11" onClick={handleTest} disabled={testLoading || !testModelId || !testMessage.trim()}>
                  {testLoading ? <><Loader2 className="w-4 h-4 mr-2 animate-spin" />正在调用模型...</> : <><Send className="w-4 h-4 mr-2" />发送测试</>}
                </Button>

                {/* 结果 */}
                {testResult && (
                  <div className="space-y-3">
                    <div className="flex items-center gap-3">
                      <div className="flex-1 h-px bg-slate-200" /><span className="text-xs font-medium text-slate-400">测试结果</span><div className="flex-1 h-px bg-slate-200" />
                    </div>

                    {testResult.success ? (
                      <>
                        {/* 指标卡片 */}
                        <div className="grid grid-cols-3 gap-3">
                          <div className="bg-white rounded-xl border border-slate-100 p-3 text-center shadow-sm">
                            <Clock className="w-5 h-5 mx-auto mb-1 text-purple-500" />
                            <p className="text-xl font-bold text-slate-900">{testResult.latency_ms}</p>
                            <p className="text-xs text-slate-400">毫秒</p>
                          </div>
                          <div className="bg-white rounded-xl border border-slate-100 p-3 text-center shadow-sm">
                            <Coins className="w-5 h-5 mx-auto mb-1 text-purple-500" />
                            <p className="text-xl font-bold text-slate-900">{testResult.usage?.total_tokens || '-'}</p>
                            <p className="text-xs text-slate-400">Token</p>
                          </div>
                          <div className="bg-white rounded-xl border border-slate-100 p-3 text-center shadow-sm">
                            <Cpu className="w-5 h-5 mx-auto mb-1 text-purple-500" />
                            <p className="text-xs font-bold text-slate-900 truncate px-1">{testResult.model_name}</p>
                            <p className="text-xs text-slate-400">{PROVIDERS[testResult.provider || ''] || ''}</p>
                          </div>
                        </div>

                        {/* 渲染后的模板 */}
                        {testResult.rendered_prompt && testResult.rendered_prompt !== testMessage && (
                          <div className="bg-slate-50 rounded-xl p-3">
                            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-1">变量替换后</p>
                            <p className="text-xs text-slate-600 whitespace-pre-wrap">{testResult.rendered_prompt}</p>
                          </div>
                        )}

                        {/* 模型回复 */}
                        <div>
                          <div className="flex items-center justify-between mb-1.5">
                            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">模型回复</p>
                            <span className="text-[10px] text-slate-400 bg-slate-100 px-2 py-0.5 rounded-full">{testResult.reply?.length || 0} 字符</span>
                          </div>
                          <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
                            <div className="text-sm text-slate-800 leading-relaxed whitespace-pre-wrap">{testResult.reply || '（空回复）'}</div>
                          </div>
                        </div>
                      </>
                    ) : (
                      <div className="bg-rose-50 rounded-xl p-4 border border-rose-100">
                        <p className="text-sm text-rose-700">{testResult.error || '测试失败'}</p>
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

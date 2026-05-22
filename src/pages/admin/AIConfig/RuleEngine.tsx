import React, { useState, useEffect, useCallback } from 'react';
import { Card } from '../../../components/ui/card';
import { Button } from '../../../components/ui/button';
import { Badge } from '../../../components/ui/badge';
import { useToast } from '../../../hooks/use-toast';
import { adminApi } from '../../../api/admin';
import { GitBranch, RefreshCw, AlertCircle, Save, Plus, Edit3, X, Send, Loader2, Zap, Clock, Coins, Cpu, KeyRound, Check, Filter } from 'lucide-react';

interface RuleItem {
  id: string;
  name: string;
  description?: string;
  rules?: Record<string, any>;
  priority: number;
  is_active: boolean;
}

interface ModelOption {
  id: string;
  provider: string;
  model_name: string;
  is_active: boolean;
}

interface PromptOption {
  id: string;
  name: string;
  type: string;
  is_active: boolean;
}

const PROVIDERS: Record<string, string> = {
  openai: 'OpenAI', deepseek: 'DeepSeek', zhipu: '智谱AI', tongyi: '通义千问',
  hunyuan: '腾讯混元', doubao: '豆包', kimi: 'Kimi', local: '本地模型', wenxin: '文心一言',
};

const TYPE_LABELS: Record<string, string> = {
  good_review: '好评', bad_review: '差评', neutral_review: '中评', appeal: '申诉', weekly_report: '周报',
};

interface MatchResult {
  rule_key: string;
  rule_desc: string;
  triggered?: boolean;
  matched?: string[];
  found?: string[];
  input?: any;
  value?: any;
}

interface TestResult {
  success: boolean;
  reply?: string;
  latency_ms?: number;
  usage?: { prompt_tokens: number; completion_tokens: number; total_tokens: number };
  error?: string;
  model_name?: string;
  provider?: string;
  rule_name?: string;
  rule_matched?: boolean;
  match_results?: MatchResult[];
  template_used?: { id: string; name: string; type: string } | null;
}

const emptyForm = { name: '', description: '', rules_json: '{\n  \n}', priority: 0, is_active: true };

const DEFAULT_RULE_TEMPLATES = [
  { name: '差评识别规则', description: '自动识别差评并触发相应处理流程', rules: { min_rating: 3, trigger_keywords: ['差', '失望', '再也不来', '退款', '投诉'], auto_escalate: true, response_timeout_minutes: 30 }, priority: 10 },
  { name: '敏感词过滤规则', description: '过滤回复中的敏感词和不当内容', rules: { blocked_words: ['脏话', '骗子'], max_reply_length: 500, check_before_send: true, alert_on_match: true }, priority: 20 },
  { name: '自动回复策略', description: '控制 AI 自动回复的触发条件和限制', rules: { auto_reply_enabled: true, daily_limit: 100, cooldown_minutes: 5, require_human_review: false }, priority: 5 },
];

export const RuleEngine: React.FC = () => {
  const [rules, setRules] = useState<RuleItem[]>([]);
  const [models, setModels] = useState<ModelOption[]>([]);
  const [prompts, setPrompts] = useState<PromptOption[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<RuleItem | null>(null);
  const [form, setForm] = useState({ ...emptyForm });
  const [jsonError, setJsonError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  // 测试状态
  const [testOpen, setTestOpen] = useState(false);
  const [testModelId, setTestModelId] = useState('');
  const [testRuleId, setTestRuleId] = useState('');
  const [testPromptId, setTestPromptId] = useState('');
  const [testInput, setTestInput] = useState('');
  const [testRating, setTestRating] = useState(3);
  const [testApiKey, setTestApiKey] = useState('');
  const [testLoading, setTestLoading] = useState(false);
  const [testResult, setTestResult] = useState<TestResult | null>(null);

  const { success, error: toastError } = useToast();

  const fetchRules = useCallback(async () => {
    setLoading(true); setError(null);
    try { const data = await adminApi.getAIRules().catch(() => []); setRules(Array.isArray(data) ? data : []); }
    catch (err) { setError(err instanceof Error ? err.message : '获取数据失败'); }
    finally { setLoading(false); }
  }, []);

  const fetchModels = useCallback(async () => {
    try { const data = await adminApi.getAIModels().catch(() => []); setModels(Array.isArray(data) ? data : []); } catch {}
  }, []);

  const fetchPrompts = useCallback(async () => {
    try { const data = await adminApi.getAIPrompts().catch(() => []); setPrompts(Array.isArray(data) ? data : []); } catch {}
  }, []);

  useEffect(() => { fetchRules(); fetchModels(); fetchPrompts(); }, [fetchRules, fetchModels, fetchPrompts]);

  const openAddModal = (templateIndex?: number) => {
    setEditingItem(null);
    if (templateIndex !== undefined && DEFAULT_RULE_TEMPLATES[templateIndex]) {
      const tmpl = DEFAULT_RULE_TEMPLATES[templateIndex];
      setForm({ name: tmpl.name, description: tmpl.description, rules_json: JSON.stringify(tmpl.rules, null, 2), priority: tmpl.priority, is_active: true });
    } else { setForm({ ...emptyForm }); }
    setJsonError(null); setModalOpen(true);
  };

  const openEditModal = (item: RuleItem) => {
    setEditingItem(item);
    setForm({ name: item.name, description: item.description || '', rules_json: item.rules ? JSON.stringify(item.rules, null, 2) : '{\n  \n}', priority: item.priority, is_active: item.is_active });
    setJsonError(null); setModalOpen(true);
  };

  const openTest = (rule?: RuleItem) => {
    setTestRuleId(rule?.id || '');
    setTestResult(null); setTestApiKey(''); setTestInput(''); setTestRating(3); setTestPromptId('');
    setTestOpen(true);
  };

  const validateJson = (text: string): boolean => {
    if (!text.trim() || text.trim() === '{}') { setJsonError(null); return true; }
    try { JSON.parse(text); setJsonError(null); return true; }
    catch (e: any) { setJsonError(`JSON 格式错误: ${e.message}`); return false; }
  };

  const handleSave = async () => {
    if (!form.name) { toastError('参数错误', '请填写规则名称'); return; }
    if (!validateJson(form.rules_json)) { toastError('格式错误', '规则 JSON 格式不正确'); return; }
    let parsedRules: any = {};
    if (form.rules_json.trim()) { try { parsedRules = JSON.parse(form.rules_json); } catch { toastError('格式错误', '规则 JSON 格式不正确'); return; } }
    setSaving(true);
    try {
      const payload: any = { name: form.name, description: form.description || undefined, rules: parsedRules, priority: form.priority, is_active: form.is_active };
      if (editingItem) { await adminApi.updateAIRule(editingItem.id, payload); success('保存成功', '规则已更新'); }
      else { await adminApi.createAIRule(payload); success('创建成功', '新规则已添加'); }
      setModalOpen(false); fetchRules();
    } catch (err: any) { toastError(editingItem ? '保存失败' : '创建失败', err.message || '请求异常'); }
    finally { setSaving(false); }
  };

  const handleTest = async () => {
    if (!testModelId || !testRuleId || !testInput) {
      toastError('参数错误', '请选择模型、规则并输入测试内容');
      return;
    }
    setTestLoading(true); setTestResult(null);
    try {
      const resp = await adminApi.testAIRule({
        model_id: testModelId,
        rule_id: testRuleId,
        prompt_id: testPromptId || undefined,
        test_input: testInput,
        test_rating: testRating,
        api_key: testApiKey || undefined,
      });
      const result = resp.data || resp;
      console.log('[规则测试] 结果:', result);
      setTestResult(result);
    } catch (err: any) {
      setTestResult({ success: false, error: err.message || '测试请求失败' });
    } finally {
      setTestLoading(false);
    }
  };

  const getRuleSummary = (rules?: Record<string, any>): string => {
    if (!rules) return '无规则定义';
    const keys = Object.keys(rules);
    if (keys.length === 0) return '空规则';
    return keys.slice(0, 5).join('、') + (keys.length > 5 ? ` 等 ${keys.length} 项` : '');
  };

  if (loading) return <div className="flex items-center justify-center h-64"><RefreshCw className="w-6 h-6 text-slate-400 animate-spin" /></div>;
  if (error) return <div className="flex flex-col items-center justify-center h-64 gap-4"><AlertCircle className="w-10 h-10 text-rose-400" /><p className="text-slate-500">{error}</p><Button variant="outline" onClick={fetchRules}>重试</Button></div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <GitBranch className="w-5 h-5 text-blue-500" />AI 规则引擎
          </h2>
          <p className="text-sm text-slate-500">管理敏感词过滤、回复策略、触发条件</p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={() => openTest()} className="bg-blue-50 border-blue-200 text-blue-700 hover:bg-blue-100">
            <Zap className="w-4 h-4 mr-1" />在线测试
          </Button>
        </div>
      </div>

      {rules.length === 0 ? (
        <Card className="border-dashed border-2 border-slate-200">
          <div className="text-center py-12 text-slate-400">
            <GitBranch className="w-12 h-12 mx-auto mb-3 opacity-30" />
            <p className="mb-1 text-slate-500">暂无规则配置</p>
            <div className="flex flex-wrap justify-center gap-3 mt-4">
              {DEFAULT_RULE_TEMPLATES.map((tmpl, idx) => (
                <Button key={idx} size="sm" className="bg-blue-500 hover:bg-blue-600 text-white" onClick={() => openAddModal(idx)}><Plus className="w-4 h-4 mr-1" />{tmpl.name}</Button>
              ))}
              <Button size="sm" variant="outline" onClick={() => openAddModal()}><Plus className="w-4 h-4 mr-1" />自定义规则</Button>
            </div>
          </div>
        </Card>
      ) : (
        <>
          <div className="flex gap-2 flex-wrap">
            <Button size="sm" variant="outline" onClick={() => openAddModal()}><Plus className="w-4 h-4 mr-1" />自定义规则</Button>
            {DEFAULT_RULE_TEMPLATES.filter(t => !rules.some(r => r.name === t.name)).map((tmpl, idx) => (
              <Button key={idx} size="sm" variant="outline" onClick={() => openAddModal(idx)}><Plus className="w-4 h-4 mr-1" />{tmpl.name}</Button>
            ))}
          </div>
          <div className="grid gap-3">
            {rules.map(r => (
              <Card key={r.id} className="border-slate-100 shadow-sm hover:shadow-md transition-shadow">
                <div className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1 flex-wrap">
                        <span className="font-semibold text-slate-900">{r.name || '未命名规则'}</span>
                        <Badge className={r.is_active ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-500'}>{r.is_active ? '启用' : '禁用'}</Badge>
                        <Badge className="bg-blue-50 text-blue-600">优先级 {r.priority}</Badge>
                      </div>
                      {r.description && <p className="text-sm text-slate-500">{r.description}</p>}
                      <p className="text-xs text-slate-400 mt-1">规则项: {getRuleSummary(r.rules)}</p>
                    </div>
                    <div className="flex items-center gap-1 ml-3 shrink-0">
                      <Button size="sm" variant="outline" className="text-blue-600 hover:bg-blue-50" onClick={() => openTest(r)}><Zap className="w-3.5 h-3.5" /></Button>
                      <Button size="sm" variant="outline" onClick={() => openEditModal(r)}><Edit3 className="w-3.5 h-3.5 mr-1" />编辑</Button>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </>
      )}

      {/* 新增/编辑模态框 */}
      {modalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={() => setModalOpen(false)}>
          <Card className="w-[560px] max-h-[80vh] overflow-y-auto p-6 space-y-5" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-slate-900">{editingItem ? `编辑规则: ${editingItem.name}` : '新增规则'}</h3>
              <button className="text-slate-400 hover:text-slate-600" onClick={() => setModalOpen(false)}><X className="w-5 h-5" /></button>
            </div>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1 block">规则名称 <span className="text-rose-400">*</span></label>
                  <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-blue-400 focus:ring-1 focus:ring-blue-200 transition" placeholder="如：差评识别规则" value={form.name} onChange={e => setForm(p => ({ ...p, name: e.target.value }))} />
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1 block">优先级</label>
                  <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-blue-400 focus:ring-1 focus:ring-blue-200 transition" type="number" min={0} value={form.priority} onChange={e => setForm(p => ({ ...p, priority: parseInt(e.target.value) || 0 }))} />
                </div>
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">描述</label>
                <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-blue-400 focus:ring-1 focus:ring-blue-200 transition" placeholder="规则用途简述" value={form.description} onChange={e => setForm(p => ({ ...p, description: e.target.value }))} />
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">规则定义 (JSON)</label>
                <textarea className={`w-full p-3 border rounded-lg text-sm outline-none transition min-h-[200px] font-mono ${jsonError ? 'border-rose-300' : 'border-slate-200 focus:border-blue-400 focus:ring-1 focus:ring-blue-200'}`} placeholder={'{\n  "trigger_keywords": ["差", "退款"],\n  "min_rating": 3\n}'} value={form.rules_json} onChange={e => { setForm(p => ({ ...p, rules_json: e.target.value })); validateJson(e.target.value); }} onBlur={() => validateJson(form.rules_json)} />
                {jsonError ? <p className="text-xs text-rose-500 mt-1">{jsonError}</p> : <p className="text-xs text-slate-400 mt-1">使用 JSON 格式定义规则</p>}
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">状态</label>
                <button type="button" className={`px-4 py-2 rounded-lg text-sm font-medium border transition ${form.is_active ? 'bg-emerald-50 border-emerald-200 text-emerald-700' : 'bg-slate-50 border-slate-200 text-slate-500'}`} onClick={() => setForm(p => ({ ...p, is_active: !p.is_active }))}>{form.is_active ? '启用' : '禁用'}</button>
              </div>
            </div>
            <div className="flex justify-end gap-3 pt-1">
              <Button variant="ghost" onClick={() => setModalOpen(false)}>取消</Button>
              <Button className="bg-blue-500 hover:bg-blue-600 text-white" onClick={handleSave} disabled={saving || !form.name || !!jsonError}>{saving ? '保存中...' : <><Save className="w-4 h-4 mr-1" />{editingItem ? '保存' : '创建'}</>}</Button>
            </div>
          </Card>
        </div>
      )}

      {/* ========== 规则引擎在线测试对话框 ========== */}
      {testOpen && (
        <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-black/40 pt-8 pb-8" onClick={() => setTestOpen(false)}>
          <div className="w-[640px] my-auto" onClick={e => e.stopPropagation()}>
            <Card>
              <div className="px-6 py-4 border-b border-slate-100 bg-gradient-to-r from-blue-50 to-slate-50">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-blue-100 flex items-center justify-center"><Zap className="w-5 h-5 text-blue-600" /></div>
                    <div>
                      <h3 className="font-bold text-slate-900">规则引擎测试</h3>
                      <p className="text-xs text-slate-500">输入内容 → 规则匹配 → 模板选择 → 模型调用</p>
                    </div>
                  </div>
                  <button className="w-8 h-8 rounded-lg flex items-center justify-center text-slate-400 hover:text-slate-600 hover:bg-white/60 transition" onClick={() => setTestOpen(false)}><X className="w-4 h-4" /></button>
                </div>
              </div>

              <div className="p-6 space-y-4">
                {/* 步骤1：选择规则和模型 */}
                <div className="bg-slate-50 rounded-lg p-3">
                  <div className="flex items-center gap-2 mb-2"><div className="w-5 h-5 rounded-full bg-blue-500 text-white flex items-center justify-center text-xs font-bold">1</div><span className="text-sm font-medium text-slate-700">选择规则和模型</span></div>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-xs text-slate-500 mb-1 block">AI 模型</label>
                      <select className="w-full p-2 border border-slate-200 rounded-lg text-sm bg-white focus:border-blue-400 outline-none transition" value={testModelId} onChange={e => setTestModelId(e.target.value)}>
                        <option value="">-- 选择模型 --</option>
                        {models.filter(m => m.is_active).map(m => (<option key={m.id} value={m.id}>{PROVIDERS[m.provider] || m.provider} · {m.model_name}</option>))}
                      </select>
                    </div>
                    <div>
                      <label className="text-xs text-slate-500 mb-1 block">规则</label>
                      <select className="w-full p-2 border border-slate-200 rounded-lg text-sm bg-white focus:border-blue-400 outline-none transition" value={testRuleId} onChange={e => setTestRuleId(e.target.value)}>
                        <option value="">-- 选择规则 --</option>
                        {rules.filter(r => r.is_active).map(r => (<option key={r.id} value={r.id}>{r.name}</option>))}
                      </select>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-3 mt-2">
                    <div>
                      <label className="text-xs text-slate-500 mb-1 block">指令模板（可选）</label>
                      <select className="w-full p-2 border border-slate-200 rounded-lg text-sm bg-white focus:border-blue-400 outline-none transition" value={testPromptId} onChange={e => setTestPromptId(e.target.value)}>
                        <option value="">-- 自动匹配 --</option>
                        {prompts.filter(p => p.is_active).map(p => (<option key={p.id} value={p.id}>{p.name} ({TYPE_LABELS[p.type] || p.type})</option>))}
                      </select>
                    </div>
                    <div>
                      <label className="text-xs text-slate-500 mb-1 block">API Key（可选）</label>
                      <input className="w-full p-2 border border-slate-200 rounded-lg text-sm outline-none focus:border-blue-400 transition" type="password" placeholder="手动输入" value={testApiKey} onChange={e => setTestApiKey(e.target.value)} disabled={testLoading} />
                    </div>
                  </div>
                </div>

                {/* 步骤2：输入测试数据 */}
                <div className="bg-slate-50 rounded-lg p-3">
                  <div className="flex items-center gap-2 mb-2"><div className="w-5 h-5 rounded-full bg-blue-500 text-white flex items-center justify-center text-xs font-bold">2</div><span className="text-sm font-medium text-slate-700">输入测试数据</span></div>
                  <div>
                    <label className="text-xs text-slate-500 mb-1 block">模拟评论内容</label>
                    <textarea className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-blue-400 transition resize-none" rows={3} placeholder="输入模拟的用户评论..." value={testInput} onChange={e => setTestInput(e.target.value)} disabled={testLoading} />
                  </div>
                  <div className="mt-2">
                    <label className="text-xs text-slate-500 mb-1 block">模拟评分</label>
                    <div className="flex items-center gap-1">
                      {[1,2,3,4,5].map(n => (
                        <button key={n} className={`w-8 h-8 rounded-lg text-sm font-bold border transition cursor-pointer ${testRating === n ? 'bg-amber-50 border-amber-300 text-amber-600' : 'bg-white border-slate-200 text-slate-400 hover:border-amber-200'}`} onClick={() => setTestRating(n)}>{n}</button>
                      ))}
                      <span className="text-xs text-slate-400 ml-2">{testRating <= 2 ? '差评' : testRating <= 3 ? '中评' : '好评'}</span>
                    </div>
                  </div>
                </div>

                {/* 发送 */}
                <Button className="w-full bg-blue-500 hover:bg-blue-600 text-white h-11" onClick={handleTest} disabled={testLoading || !testModelId || !testRuleId || !testInput.trim()}>
                  {testLoading ? <><Loader2 className="w-4 h-4 mr-2 animate-spin" />规则匹配 + 模型调用中...</> : <><Send className="w-4 h-4 mr-2" />执行规则测试</>}
                </Button>

                {/* 结果 */}
                {testResult && (
                  <div className="space-y-3">
                    <div className="flex items-center gap-3"><div className="flex-1 h-px bg-slate-200" /><span className="text-xs font-medium text-slate-400">测试结果</span><div className="flex-1 h-px bg-slate-200" /></div>

                    {/* 规则匹配结果 */}
                    {testResult.match_results && testResult.match_results.length > 0 && (
                      <div>
                        <div className="flex items-center gap-2 mb-2">
                          <Filter className="w-4 h-4 text-blue-500" />
                          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">规则匹配结果</p>
                          <Badge className={testResult.rule_matched ? 'bg-amber-100 text-amber-700 text-xs' : 'bg-emerald-100 text-emerald-700 text-xs'}>
                            {testResult.rule_matched ? '已触发' : '未触发'}
                          </Badge>
                        </div>
                        <div className="space-y-1.5">
                          {testResult.match_results.map((mr, idx) => (
                            <div key={idx} className={`rounded-lg p-2.5 border ${mr.triggered ? 'bg-amber-50 border-amber-200' : 'bg-slate-50 border-slate-100'}`}>
                              <div className="flex items-center justify-between">
                                <span className="text-xs font-medium text-slate-600">{mr.rule_desc}</span>
                                <Badge className={mr.triggered ? 'bg-amber-200 text-amber-800 text-[10px]' : 'bg-slate-200 text-slate-500 text-[10px]'}>
                                  {mr.triggered ? '触发' : '未触发'}
                                </Badge>
                              </div>
                              {mr.matched && mr.matched.length > 0 && (
                                <div className="flex gap-1 mt-1.5 flex-wrap">
                                  {mr.matched.map((kw, ki) => <span key={ki} className="text-[10px] bg-amber-100 text-amber-700 px-1.5 py-0.5 rounded">{kw}</span>)}
                                </div>
                              )}
                              {mr.found && mr.found.length > 0 && (
                                <div className="flex gap-1 mt-1.5 flex-wrap">
                                  {mr.found.map((w, wi) => <span key={wi} className="text-[10px] bg-rose-100 text-rose-700 px-1.5 py-0.5 rounded">{w}</span>)}
                                </div>
                              )}
                              {mr.input !== undefined && <p className="text-[10px] text-slate-400 mt-1">输入值: {String(mr.input)}</p>}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* 模板匹配 */}
                    {testResult.template_used && (
                      <div className="bg-purple-50 rounded-lg p-3 border border-purple-100">
                        <p className="text-xs font-medium text-purple-600 mb-1">匹配模板</p>
                        <p className="text-sm text-purple-800">{testResult.template_used.name} ({TYPE_LABELS[testResult.template_used.type] || testResult.template_used.type})</p>
                      </div>
                    )}

                    {testResult.success ? (
                      <>
                        {/* 指标 */}
                        <div className="grid grid-cols-3 gap-3">
                          <div className="bg-white rounded-xl border border-slate-100 p-3 text-center shadow-sm">
                            <Clock className="w-5 h-5 mx-auto mb-1 text-blue-500" />
                            <p className="text-xl font-bold text-slate-900">{testResult.latency_ms}</p>
                            <p className="text-xs text-slate-400">毫秒</p>
                          </div>
                          <div className="bg-white rounded-xl border border-slate-100 p-3 text-center shadow-sm">
                            <Coins className="w-5 h-5 mx-auto mb-1 text-blue-500" />
                            <p className="text-xl font-bold text-slate-900">{testResult.usage?.total_tokens || '-'}</p>
                            <p className="text-xs text-slate-400">Token</p>
                          </div>
                          <div className="bg-white rounded-xl border border-slate-100 p-3 text-center shadow-sm">
                            <Cpu className="w-5 h-5 mx-auto mb-1 text-blue-500" />
                            <p className="text-xs font-bold text-slate-900 truncate px-1">{testResult.model_name}</p>
                            <p className="text-xs text-slate-400">{PROVIDERS[testResult.provider || ''] || ''}</p>
                          </div>
                        </div>

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

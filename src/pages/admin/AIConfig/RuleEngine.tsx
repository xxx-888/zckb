import React, { useState, useEffect, useCallback } from 'react';
import { Card } from '../../../components/ui/card';
import { Button } from '../../../components/ui/button';
import { Badge } from '../../../components/ui/badge';
import { useToast } from '../../../hooks/use-toast';
import { adminApi } from '../../../api/admin';
import { GitBranch, RefreshCw, AlertCircle, Save, Plus, Edit3, X } from 'lucide-react';

interface RuleItem {
  id: string;
  name: string;
  description?: string;
  rules?: Record<string, any>;
  priority: number;
  is_active: boolean;
}

const emptyForm = {
  name: '',
  description: '',
  rules_json: '{\n  \n}',
  priority: 0,
  is_active: true,
};

const DEFAULT_RULE_TEMPLATES = [
  {
    name: '差评识别规则',
    description: '自动识别差评并触发相应处理流程',
    rules: {
      "min_rating": 3,
      "trigger_keywords": ["差", "失望", "再也不来", "退款", "投诉"],
      "auto_escalate": true,
      "response_timeout_minutes": 30,
    },
    priority: 10,
  },
  {
    name: '敏感词过滤规则',
    description: '过滤回复中的敏感词和不当内容',
    rules: {
      "blocked_words": [],
      "max_reply_length": 500,
      "check_before_send": true,
      "alert_on_match": true,
    },
    priority: 20,
  },
  {
    name: '自动回复策略',
    description: '控制 AI 自动回复的触发条件和限制',
    rules: {
      "auto_reply_enabled": true,
      "daily_limit": 100,
      "cooldown_minutes": 5,
      "require_human_review": false,
    },
    priority: 5,
  },
];

export const RuleEngine: React.FC = () => {
  const [rules, setRules] = useState<RuleItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<RuleItem | null>(null);
  const [form, setForm] = useState({ ...emptyForm });
  const [jsonError, setJsonError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const { success, error: toastError } = useToast();

  const fetchRules = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await adminApi.getAIRules().catch(() => []);
      setRules(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchRules(); }, [fetchRules]);

  const openAddModal = (templateIndex?: number) => {
    setEditingItem(null);
    if (templateIndex !== undefined && DEFAULT_RULE_TEMPLATES[templateIndex]) {
      const tmpl = DEFAULT_RULE_TEMPLATES[templateIndex];
      setForm({
        name: tmpl.name,
        description: tmpl.description,
        rules_json: JSON.stringify(tmpl.rules, null, 2),
        priority: tmpl.priority,
        is_active: true,
      });
    } else {
      setForm({ ...emptyForm });
    }
    setJsonError(null);
    setModalOpen(true);
  };

  const openEditModal = (item: RuleItem) => {
    setEditingItem(item);
    setForm({
      name: item.name,
      description: item.description || '',
      rules_json: item.rules ? JSON.stringify(item.rules, null, 2) : '{\n  \n}',
      priority: item.priority,
      is_active: item.is_active,
    });
    setJsonError(null);
    setModalOpen(true);
  };

  const validateJson = (text: string): boolean => {
    if (!text.trim() || text.trim() === '{}') {
      setJsonError(null);
      return true;
    }
    try {
      JSON.parse(text);
      setJsonError(null);
      return true;
    } catch (e: any) {
      setJsonError(`JSON 格式错误: ${e.message}`);
      return false;
    }
  };

  const handleSave = async () => {
    if (!form.name) {
      toastError('参数错误', '请填写规则名称');
      return;
    }

    if (!validateJson(form.rules_json)) {
      toastError('格式错误', '规则 JSON 格式不正确');
      return;
    }

    let parsedRules: any = {};
    if (form.rules_json.trim()) {
      try {
        parsedRules = JSON.parse(form.rules_json);
      } catch {
        toastError('格式错误', '规则 JSON 格式不正确，请检查');
        return;
      }
    }

    setSaving(true);
    try {
      const payload: any = {
        name: form.name,
        description: form.description || undefined,
        rules: parsedRules,
        priority: form.priority,
        is_active: form.is_active,
      };

      if (editingItem) {
        await adminApi.updateAIRule(editingItem.id, payload);
        success('保存成功', '规则已更新');
      } else {
        await adminApi.createAIRule(payload);
        success('创建成功', '新规则已添加');
      }
      setModalOpen(false);
      fetchRules();
    } catch (err: any) {
      toastError(editingItem ? '保存失败' : '创建失败', err.message || '请求异常');
    } finally {
      setSaving(false);
    }
  };

  const getRuleSummary = (rules?: Record<string, any>): string => {
    if (!rules) return '无规则定义';
    const keys = Object.keys(rules);
    if (keys.length === 0) return '空规则';
    return keys.slice(0, 5).join('、') + (keys.length > 5 ? ` 等 ${keys.length} 项` : '');
  };

  const getRuleValuePreview = (rules?: Record<string, any>): string => {
    if (!rules) return '';
    const entries = Object.entries(rules).slice(0, 2);
    return entries.map(([k, v]) => `${k}: ${typeof v === 'object' ? JSON.stringify(v) : v}`).join(' | ');
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
          <Button variant="outline" size="sm" onClick={fetchRules}><RefreshCw className="w-4 h-4 mr-1" />刷新</Button>
        </div>
      </div>

      {rules.length === 0 ? (
        <Card className="border-dashed border-2 border-slate-200">
          <div className="text-center py-12 text-slate-400">
            <GitBranch className="w-12 h-12 mx-auto mb-3 opacity-30" />
            <p className="mb-1 text-slate-500">暂无规则配置</p>
            <p className="text-xs text-slate-300 mb-6">选择预设模板快速创建，或自定义规则</p>
            <div className="flex flex-wrap justify-center gap-3">
              {DEFAULT_RULE_TEMPLATES.map((tmpl, idx) => (
                <Button key={idx} size="sm" className="bg-blue-500 hover:bg-blue-600 text-white" onClick={() => openAddModal(idx)}>
                  <Plus className="w-4 h-4 mr-1" />{tmpl.name}
                </Button>
              ))}
              <Button size="sm" variant="outline" onClick={() => openAddModal()}>
                <Plus className="w-4 h-4 mr-1" />自定义规则
              </Button>
            </div>
          </div>
        </Card>
      ) : (
        <>
          <div className="flex gap-2">
            <Button size="sm" variant="outline" onClick={() => openAddModal()}>
              <Plus className="w-4 h-4 mr-1" />自定义规则
            </Button>
            {DEFAULT_RULE_TEMPLATES.filter(t => !rules.some(r => r.name === t.name)).map((tmpl, idx) => (
              <Button key={idx} size="sm" variant="outline" onClick={() => openAddModal(idx)}>
                <Plus className="w-4 h-4 mr-1" />{tmpl.name}
              </Button>
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
                        <Badge className={r.is_active ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-500'}>
                          {r.is_active ? '启用' : '禁用'}
                        </Badge>
                        <Badge className="bg-blue-50 text-blue-600">优先级 {r.priority}</Badge>
                      </div>
                      {r.description && <p className="text-sm text-slate-500">{r.description}</p>}
                      <div className="mt-1.5 space-y-0.5">
                        <p className="text-xs text-slate-400">规则项: {getRuleSummary(r.rules)}</p>
                        {getRuleValuePreview(r.rules) && (
                          <p className="text-xs text-slate-300 font-mono truncate">{getRuleValuePreview(r.rules)}</p>
                        )}
                      </div>
                    </div>
                    <Button size="sm" variant="outline" className="ml-3 shrink-0" onClick={() => openEditModal(r)}>
                      <Edit3 className="w-3.5 h-3.5 mr-1" />编辑
                    </Button>
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
                  <input
                    className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-blue-400 focus:ring-1 focus:ring-blue-200 transition"
                    placeholder="如：差评识别规则"
                    value={form.name}
                    onChange={e => setForm(p => ({ ...p, name: e.target.value }))}
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-slate-700 mb-1 block">优先级</label>
                  <input
                    className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-blue-400 focus:ring-1 focus:ring-blue-200 transition"
                    type="number"
                    min={0}
                    value={form.priority}
                    onChange={e => setForm(p => ({ ...p, priority: parseInt(e.target.value) || 0 }))}
                  />
                  <p className="text-xs text-slate-400 mt-0.5">数字越小优先级越高</p>
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">描述</label>
                <input
                  className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none focus:border-blue-400 focus:ring-1 focus:ring-blue-200 transition"
                  placeholder="规则用途简述"
                  value={form.description}
                  onChange={e => setForm(p => ({ ...p, description: e.target.value }))}
                />
              </div>

              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">规则定义 (JSON)</label>
                <textarea
                  className={`w-full p-3 border rounded-lg text-sm outline-none transition min-h-[200px] font-mono ${jsonError ? 'border-rose-300 focus:border-rose-400 focus:ring-1 focus:ring-rose-200' : 'border-slate-200 focus:border-blue-400 focus:ring-1 focus:ring-blue-200'}`}
                  placeholder={'{\n  "sensitive_words": ["脏话"],\n  "max_reply_length": 200\n}'}
                  value={form.rules_json}
                  onChange={e => {
                    setForm(p => ({ ...p, rules_json: e.target.value }));
                    validateJson(e.target.value);
                  }}
                  onBlur={() => validateJson(form.rules_json)}
                />
                {jsonError ? (
                  <p className="text-xs text-rose-500 mt-1">{jsonError}</p>
                ) : (
                  <p className="text-xs text-slate-400 mt-1">使用 JSON 格式定义规则，如敏感词列表、回复限制、触发条件等</p>
                )}
              </div>

              <div>
                <label className="text-sm font-medium text-slate-700 mb-1 block">状态</label>
                <button
                  type="button"
                  className={`px-4 py-2 rounded-lg text-sm font-medium border transition ${form.is_active ? 'bg-emerald-50 border-emerald-200 text-emerald-700' : 'bg-slate-50 border-slate-200 text-slate-500'}`}
                  onClick={() => setForm(p => ({ ...p, is_active: !p.is_active }))}
                >
                  {form.is_active ? '启用' : '禁用'}
                </button>
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-1">
              <Button variant="ghost" onClick={() => setModalOpen(false)}>取消</Button>
              <Button
                className="bg-blue-500 hover:bg-blue-600 text-white"
                onClick={handleSave}
                disabled={saving || !form.name || !!jsonError}
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

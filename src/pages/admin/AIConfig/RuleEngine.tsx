import React, { useState } from 'react';
import { Card } from '../../../components/ui/card';
import { Button } from '../../../components/ui/button';
import { Badge } from '../../../components/ui/badge';
import { Switch } from '../../../components/ui/switch';
import { 
  GitBranch, 
  Layers, 
  ArrowRight, 
  Download, 
  Upload, 
  Plus, 
  MoreVertical,
  CheckCircle,
  AlertTriangle,
  FileText,
  GripVertical,
  Zap,
  Split,
  Settings,
  Activity,
  Power,
  Info,
  Clock,
  ArrowDown,
  Trash2,
  Copy
} from 'lucide-react';
import { cn } from '../../../lib/utils';
import { useToast } from '../../../hooks/use-toast';

interface Rule {
  id: string;
  name: string;
  trigger: string;
  template: string;
  priority: number;
  status: 'active' | 'draft';
  enabled: boolean;
  branch?: string;
  dependencies?: string[];
}

export const RuleEngine: React.FC = () => {
  const [globalActive, setGlobalActive] = useState(true);
  const [rules, setRules] = useState<Rule[]>([
    {
      id: '1',
      name: '食安问题-极速响应',
      trigger: '标签包含 "食品安全" 或 "异物"',
      template: '深度致歉模板-食安专用',
      priority: 100,
      status: 'active',
      enabled: true,
      branch: 'High Risk'
    },
    {
      id: '2',
      name: '环境差评-优化引导',
      trigger: '标签包含 "环境" 且 评分 < 3',
      template: '环境改善说明模板',
      priority: 80,
      status: 'active',
      enabled: true,
      dependencies: ['1']
    },
    {
      id: '3',
      name: '日常好评-品牌文化',
      trigger: '情感极性 = 好评',
      template: '品牌温度回馈模板',
      priority: 10,
      status: 'draft',
      enabled: false
    }
  ]);
  
  const [showNewRule, setShowNewRule] = useState(false);
  const [newRule, setNewRule] = useState({
    name: '',
    trigger: '',
    template: '',
    priority: 50,
  });
  
  const { success, error } = useToast();

  const toggleRule = (id: string) => {
    setRules(rules.map(r => r.id === id ? { ...r, enabled: !r.enabled } : r));
    const rule = rules.find(r => r.id === id);
    if (rule) {
      success('状态已更新', `规则 "${rule.name}" 已${rule.enabled ? '禁用' : '启用'}`);
    }
  };

  const handleAddRule = () => {
    if (!newRule.name || !newRule.trigger || !newRule.template) {
      error('添加失败', '请填写完整的规则信息');
      return;
    }
    const newId = (rules.length + 1).toString();
    const rule: Rule = {
      id: newId,
      name: newRule.name,
      trigger: newRule.trigger,
      template: newRule.template,
      priority: newRule.priority,
      status: 'draft',
      enabled: false
    };
    setRules([...rules, rule]);
    setShowNewRule(false);
    setNewRule({ name: '', trigger: '', template: '', priority: 50 });
    success('添加成功', `规则 "${newRule.name}" 已创建，请启用后生效`);
  };

  const handleDeleteRule = (id: string) => {
    const rule = rules.find(r => r.id === id);
    setRules(rules.filter(r => r.id !== id));
    success('删除成功', `规则 "${rule?.name}" 已删除`);
  };

  const handleExportConfig = () => {
    success('导出配置', '正在生成规则配置...');
    setTimeout(() => {
      success('导出完成', '配置文件已下载');
    }, 1000);
  };

  const handleTestMode = () => {
    success('测试模式', '正在启用规则测试模式...');
    setTimeout(() => {
      success('测试完成', '所有规则测试通过，未发现冲突');
    }, 1500);
  };

  const handleFixDependencies = () => {
    success('修复依赖', '正在自动修复逻辑依赖...');
    setTimeout(() => {
      setRules(rules.map(r => r.id === '3' ? { ...r, enabled: true, status: 'active' as const } : r));
      success('修复完成', '已启用兜底规则，依赖关系已完善');
    }, 1000);
  };

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-2 duration-500">
      <div className="flex justify-between items-center mb-2 bg-white p-4 rounded-2xl border border-slate-100 shadow-sm">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <GitBranch className="w-6 h-6 text-blue-600" />
            <h3 className="font-bold text-slate-800 text-lg">规则引擎控制中心</h3>
          </div>
          <div className="h-8 w-px bg-slate-200" />
          <div className="flex items-center gap-3">
            <label className="text-sm font-bold text-slate-500">全域规则开关</label>
            <div 
              onClick={() => {
                setGlobalActive(!globalActive);
                success('全局开关', `规则引擎已${globalActive ? '暂停' : '开启'}`);
              }}
              className={cn(
                "flex items-center px-3 py-1.5 rounded-full cursor-pointer transition-all gap-2",
                globalActive ? "bg-emerald-50 text-emerald-600 border border-emerald-100" : "bg-slate-100 text-slate-400 border border-slate-200"
              )}
            >
              <Power className="w-4 h-4" />
              <span className="text-xs font-bold">{globalActive ? '已开启' : '已暂停'}</span>
            </div>
          </div>
        </div>
        <div className="flex gap-3">
          <Button 
            variant="outline" 
            size="sm" 
            className="gap-2 border-slate-200 bg-white"
            onClick={handleTestMode}
          >
            <Activity className="w-4 h-4" /> 测试模式
          </Button>
          <Button 
            variant="outline" 
            size="sm" 
            className="gap-2 border-slate-200 bg-white"
            onClick={handleExportConfig}
          >
            <Download className="w-4 h-4" /> 导出配置
          </Button>
          <Button 
            size="sm" 
            className="gap-2 bg-blue-600 hover:bg-blue-700 shadow-lg shadow-blue-100"
            onClick={() => setShowNewRule(true)}
          >
            <Plus className="w-4 h-4" /> 新增策略规则
          </Button>
        </div>
      </div>

      {showNewRule && (
        <Card className="p-6 border-2 border-blue-500 bg-blue-50/10 animate-in zoom-in-95 duration-200">
          <h4 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
            <Plus className="w-4 h-4" /> 新增策略规则
          </h4>
          <div className="grid grid-cols-2 gap-6 mb-6">
            <div className="space-y-4">
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-slate-500">规则名称</label>
                <input 
                  value={newRule.name}
                  onChange={(e) => setNewRule({...newRule, name: e.target.value})}
                  className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500/20" 
                  placeholder="如：配送延时-补偿方案" 
                />
              </div>
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-slate-500">触发条件</label>
                <input 
                  value={newRule.trigger}
                  onChange={(e) => setNewRule({...newRule, trigger: e.target.value})}
                  className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500/20" 
                  placeholder='标签包含 "配送"' 
                />
              </div>
            </div>
            <div className="space-y-4">
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-slate-500">回复模板</label>
                <input 
                  value={newRule.template}
                  onChange={(e) => setNewRule({...newRule, template: e.target.value})}
                  className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500/20" 
                  placeholder="诚恳道歉模板" 
                />
              </div>
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-slate-500">优先级 (0-100)</label>
                <input 
                  type="number"
                  value={newRule.priority}
                  onChange={(e) => setNewRule({...newRule, priority: parseInt(e.target.value) || 0})}
                  className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500/20" 
                />
              </div>
            </div>
          </div>
          <div className="flex gap-3 pt-4 border-t border-slate-100">
            <Button className="flex-1 bg-blue-600 hover:bg-blue-700" onClick={handleAddRule}>保存规则</Button>
            <Button variant="ghost" onClick={() => setShowNewRule(false)}>取消</Button>
          </div>
        </Card>
      )}

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Rules Orchestration */}
        <div className="xl:col-span-2 space-y-6">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2">
               <Layers className="w-4 h-4 text-slate-400" />
               <span className="text-sm font-bold text-slate-700">策略规则编排 (可拖拽调整优先级)</span>
            </div>
            <Badge className="bg-blue-50 text-blue-600 border-none font-bold">
              共 {rules.length} 条规则
            </Badge>
          </div>

          <div className="space-y-4">
            {rules.sort((a, b) => b.priority - a.priority).map((rule, idx) => (
              <Card key={rule.id} className={cn(
                "p-5 border-slate-100 transition-all relative overflow-hidden group",
                !rule.enabled ? "opacity-60 grayscale-[0.5] bg-slate-50/50" : "hover:shadow-lg hover:border-blue-200"
              )}>
                <div className="flex items-start gap-4">
                  <div className="mt-1 cursor-grab active:cursor-grabbing text-slate-300 hover:text-slate-500">
                    <GripVertical className="w-5 h-5" />
                  </div>
                  
                  <div className="flex-1">
                    <div className="flex justify-between items-start mb-4">
                      <div className="flex items-center gap-3">
                        <div className={cn(
                          "w-10 h-10 rounded-xl flex items-center justify-center font-bold text-xs border shadow-sm",
                          rule.enabled ? "bg-white text-blue-600 border-blue-100" : "bg-slate-100 text-slate-400 border-slate-200"
                        )}>
                          P{rule.priority}
                        </div>
                        <div>
                          <div className="flex items-center gap-2">
                            <h4 className="font-bold text-slate-900">{rule.name}</h4>
                            {rule.branch && <Badge className="bg-red-50 text-red-600 border-red-100 text-[9px] py-0 h-4">{rule.branch}</Badge>}
                          </div>
                          <div className="flex items-center gap-3 mt-1">
                             <span className="text-[10px] text-slate-400 flex items-center gap-1">
                               <Clock className="w-3 h-3" /> 最后修改: 2026-05-09
                             </span>
                             {rule.dependencies && (
                               <span className="text-[10px] text-amber-600 font-bold flex items-center gap-1">
                                 <GitBranch className="w-3 h-3" /> 依赖: {rule.dependencies.join(', ')}
                               </span>
                             )}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        <div className="flex flex-col items-end mr-2">
                          <span className="text-[10px] font-bold text-slate-400 mb-1 uppercase">启用状态</span>
                          <Switch 
                            checked={rule.enabled} 
                            onCheckedChange={() => toggleRule(rule.id)}
                            className="data-[state=checked]:bg-blue-600"
                          />
                        </div>
                        <Button 
                          variant="ghost" 
                          size="icon" 
                          className="h-8 w-8 text-slate-400 hover:text-blue-600"
                          onClick={() => success('编辑规则', `正在打开 "${rule.name}" 的编辑界面...`)}
                        >
                          <Settings className="w-4 h-4" />
                        </Button>
                        <Button 
                          variant="ghost" 
                          size="icon" 
                          className="h-8 w-8 text-slate-400 hover:text-red-600"
                          onClick={() => handleDeleteRule(rule.id)}
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>

                    <div className="relative">
                      {rule.branch && (
                        <div className="absolute -left-6 top-1/2 -translate-y-1/2 flex flex-col items-center">
                           <div className="w-0.5 h-12 bg-slate-200" />
                           <Split className="w-4 h-4 text-slate-300" />
                        </div>
                      )}
                      <div className="flex flex-wrap items-center gap-2 text-sm text-slate-600 bg-slate-50/80 p-4 rounded-xl border border-slate-100 group-hover:bg-blue-50/30 transition-colors">
                        <div className="flex items-center gap-1.5 font-bold text-blue-600 text-xs uppercase tracking-tight">
                          <Zap className="w-3.5 h-3.5 fill-blue-600" /> Trigger
                        </div>
                        <div className="px-3 py-1 bg-white border border-slate-200 rounded-lg text-xs font-mono font-medium shadow-sm">
                          {rule.trigger}
                        </div>
                        <ArrowRight className="w-4 h-4 text-slate-300 mx-2" />
                        <div className="flex items-center gap-1.5 font-bold text-purple-600 text-xs uppercase tracking-tight">
                          <FileText className="w-3.5 h-3.5" /> Action
                        </div>
                        <div className="px-3 py-1 bg-white border border-slate-200 rounded-lg text-xs font-mono font-medium shadow-sm">
                          {rule.template}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Rule Chain Visualizer */}
        <div className="space-y-6">
          <Card className="p-6 border-slate-100 bg-slate-900 text-white relative overflow-hidden">
             <div className="absolute -right-10 -top-10 opacity-10">
                <GitBranch className="w-48 h-48" />
             </div>
             
             <div className="relative z-10">
               <h4 className="font-bold text-white mb-6 flex items-center gap-2">
                 <Layers className="w-5 h-5 text-blue-400" />
                 AI 处理流水线 (Visual Chain)
               </h4>
               
               <div className="space-y-0">
                 {[
                   { step: 1, label: '情感与意图分析', icon: '🧠', status: 'completed', desc: 'NLP 极性判断与核心诉求提取' },
                   { step: 2, label: '条件分支分流', icon: '⑂', status: 'processing', type: 'branch', desc: '根据风险等级分配处理链路' },
                   { step: 3, label: '规则引擎匹配', icon: '🎯', status: 'waiting', desc: '匹配预设策略与回复模板' },
                   { step: 4, label: 'AI 内容生成', icon: '✍️', status: 'waiting', desc: '基于角色设定渲染回复初稿' },
                   { step: 5, label: '多重安全合规检查', icon: '🛡️', status: 'waiting', desc: '禁忌词过滤与逻辑合理性检查' },
                 ].map((step, i) => (
                   <div key={i} className="relative pb-8 last:pb-0">
                     {i < 4 && (
                       <div className={cn(
                         "absolute left-4 top-8 bottom-0 w-0.5",
                         step.status === 'completed' ? "bg-blue-500" : "bg-white/10"
                       )} />
                     )}
                     
                     <div className="flex gap-4">
                       <div className={cn(
                         "w-8 h-8 rounded-full flex items-center justify-center text-xs shrink-0 z-10 border-2",
                         step.status === 'completed' ? "bg-blue-600 border-blue-400 text-white" :
                         step.status === 'processing' ? "bg-white border-blue-500 text-blue-600 animate-pulse" : "bg-slate-800 border-slate-700 text-slate-500"
                       )}>
                         {step.status === 'completed' ? <CheckCircle className="w-4 h-4" /> : step.step}
                       </div>
                       
                       <div className={cn(
                         "flex-1 p-3 rounded-xl border transition-all",
                         step.status === 'processing' ? "bg-white/10 border-white/20 shadow-lg" : "border-transparent"
                       )}>
                         <div className="flex justify-between items-start">
                            <div>
                               <div className="flex items-center gap-2">
                                 <span className="text-xs font-bold text-white">{step.label}</span>
                                 <span className="text-[14px]">{step.icon}</span>
                               </div>
                               <p className="text-[10px] text-slate-400 mt-1">{step.desc}</p>
                            </div>
                            {step.status === 'processing' && (
                              <Badge className="bg-blue-500 text-white text-[8px] h-4 py-0">RUNNING</Badge>
                            )}
                         </div>
                         
                         {step.type === 'branch' && step.status === 'processing' && (
                           <div className="mt-4 grid grid-cols-2 gap-2 animate-in slide-in-from-top-2">
                             <div className="p-2 bg-red-500/20 border border-red-500/30 rounded-lg text-[9px] text-red-200">
                               <div className="font-bold mb-1 flex items-center gap-1"><AlertTriangle className="w-2.5 h-2.5" /> High Risk</div>
                               进入极速响应链路
                             </div>
                             <div className="p-2 bg-blue-500/20 border border-blue-500/30 rounded-lg text-[9px] text-blue-200">
                               <div className="font-bold mb-1 flex items-center gap-1"><Zap className="w-2.5 h-2.5" /> Standard</div>
                               进入常规回复生成
                             </div>
                           </div>
                         )}
                       </div>
                     </div>
                   </div>
                 ))}
               </div>
             </div>
          </Card>

          <Card className="p-5 border-slate-100 bg-amber-50 border-amber-100">
            <h4 className="text-xs font-bold text-amber-900 mb-2 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4" />
              逻辑完整性检查
            </h4>
            <p className="text-[11px] text-amber-700 leading-relaxed mb-4">
              检测到"日常好评"规则处于未启用状态，且没有任何降级处理规则。
            </p>
            <div className="space-y-2">
               <div className="flex items-center gap-2 text-[10px] text-amber-800 bg-white/50 p-2 rounded border border-amber-200">
                 <Info className="w-3 h-3" /> 建议：添加一条优先级最低的通配兜底规则。
               </div>
               <Button 
                 size="sm" 
                 variant="outline" 
                 className="w-full text-[10px] h-7 border-amber-300 text-amber-700 hover:bg-amber-100"
                 onClick={handleFixDependencies}
               >
                 一键修复依赖项
               </Button>
            </div>
          </Card>

          <Card className="p-5 border-slate-100 bg-slate-50 border-slate-200">
             <h4 className="text-xs font-bold text-slate-800 mb-4 flex items-center gap-2">
               <Activity className="w-4 h-4 text-blue-500" />
               规则生效统计
             </h4>
             <div className="grid grid-cols-2 gap-4">
                <div className="text-center p-3 bg-white rounded-xl border border-slate-200 shadow-sm">
                   <p className="text-2xl font-black text-slate-900">2.4k</p>
                   <p className="text-[9px] font-bold text-slate-400 uppercase mt-1">今日触发</p>
                </div>
                <div className="text-center p-3 bg-white rounded-xl border border-slate-200 shadow-sm">
                   <p className="text-2xl font-black text-emerald-600">98.2%</p>
                   <p className="text-[9px] font-bold text-slate-400 uppercase mt-1">执行成功率</p>
                </div>
             </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

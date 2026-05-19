import React, { useState } from 'react';
import { 
  Brain, 
  Save, 
  RefreshCw,
  Sliders,
  Wand2,
  Zap,
  Plus,
  Target,
  Info,
  Cpu,
  GitBranch,
  Activity,
  BarChart3
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { AdminLayout } from '../../components/AdminLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';
import { useNavigate } from 'react-router-dom';

// Import sub-modules
import { ModelConfig } from './AIConfig/ModelConfig';
import { PromptConfig } from './AIConfig/PromptConfig';
import { RuleEngine } from './AIConfig/RuleEngine';
import { Monitoring } from './AIConfig/Monitoring';
import { Evaluation } from './AIConfig/Evaluation';

type ConfigTab = 'models' | 'prompts' | 'rules' | 'monitoring' | 'evaluation';

export const AIConfig: React.FC = () => {
  const [activeTab, setActiveTab] = useState<ConfigTab>('models');
  const { success, error } = useToast();
  const navigate = useNavigate();
  
  const handleExportConfig = () => {
    success('导出配置', '正在生成全局 AI 配置文件...');
  };

  const handleSyncUpdate = () => {
    success('同步热更新', '正在将配置同步到所有节点...');
    setTimeout(() => {
      success('同步完成', '全量节点同步耗时 1.2s，未发现异常。');
    }, 1500);
  };

  const tabs = [
    { id: 'models', label: '模型配置', icon: Cpu, color: 'text-orange-600' },
    { id: 'prompts', label: '深度指令', icon: Wand2, color: 'text-purple-600' },
    { id: 'rules', label: '规则引擎', icon: GitBranch, color: 'text-blue-600' },
    { id: 'monitoring', label: '实时监控', icon: Activity, color: 'text-emerald-600' },
    { id: 'evaluation', label: '效能评估', icon: BarChart3, color: 'text-amber-600' },
  ];

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-end">
          <div>
            <h2 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
              <Brain className="w-7 h-7 text-orange-600" />
              智策 AI 核心配置中枢
            </h2>
            <p className="text-slate-500 mt-1">
              {activeTab === 'models' && "管理多平台大模型接口并进行并发质量测试"}
              {activeTab === 'prompts' && "精细化配置 AI 角色人格、语气、字数及词库过滤规则"}
              {activeTab === 'rules' && "编排复杂的处理流水线，设置条件触发与冲突优先级"}
              {activeTab === 'monitoring' && "实时监控 AI 处理链路日志，进行 A/B 测试实验"}
              {activeTab === 'evaluation' && "基于真实反馈优化 AI 表现，建立持续迭代的反馈闭环"}
            </p>
          </div>
          <div className="flex gap-3">
            <Button variant="outline" className="gap-2 border-slate-200 bg-white" onClick={handleExportConfig}>
              <RefreshCw className="w-4 h-4" /> 导出全局配置
            </Button>
            <Button className="bg-slate-900 hover:bg-slate-800 text-white gap-2 shadow-lg shadow-slate-200" onClick={handleSyncUpdate}>
              <Save className="w-4 h-4" /> 同步热更新
            </Button>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex bg-slate-100 p-1.5 rounded-2xl w-fit border border-slate-200/50">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as ConfigTab)}
              className={cn(
                "flex items-center gap-2 px-6 py-2.5 rounded-xl text-sm font-bold transition-all",
                activeTab === tab.id 
                  ? "bg-white text-slate-900 shadow-sm border border-slate-200/50" 
                  : "text-slate-500 hover:text-slate-700 hover:bg-slate-200/50"
              )}
            >
              <tab.icon className={cn("w-4 h-4", activeTab === tab.id ? tab.color : "text-slate-400")} />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Dynamic Content Area */}
        <div className="min-h-[600px]">
          {activeTab === 'models' && <ModelConfig />}
          {activeTab === 'prompts' && <PromptConfig />}
          {activeTab === 'rules' && <RuleEngine />}
          {activeTab === 'monitoring' && <Monitoring />}
          {activeTab === 'evaluation' && <Evaluation />}
        </div>
        
        {/* Footer Support Info */}
        <div className="pt-8 border-t border-slate-100 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 rounded-lg bg-orange-50 flex items-center justify-center shrink-0">
              <Info className="w-5 h-5 text-orange-600" />
            </div>
            <div>
              <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">智能建议</h4>
              <p className="text-[11px] text-slate-500 mt-1 leading-relaxed">
                当前模型响应时间环比增加 15%，建议检查 API 接口负载或切换备用线路。
              </p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-50 flex items-center justify-center shrink-0">
              <Zap className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">热更新状态</h4>
              <p className="text-[11px] text-slate-500 mt-1 leading-relaxed">
                上次同步时间：今天 14:32:10。全量节点同步耗时 1.2s，未发现异常。
              </p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center shrink-0">
              <Target className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">合规审计</h4>
              <p className="text-[11px] text-slate-500 mt-1 leading-relaxed">
                已启用全量禁忌词库及食安合规引擎，拦截了 3 条潜在不当回复。
              </p>
            </div>
          </div>
        </div>
      </div>
    </AdminLayout>
  );
};

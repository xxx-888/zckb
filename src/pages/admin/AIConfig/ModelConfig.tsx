import React, { useState } from 'react';
import { Card } from '../../../components/ui/card';
import { Button } from '../../../components/ui/button';
import { Input } from '../../../components/ui/input';
import { Badge } from '../../../components/ui/badge';
import {
  Plus,
  Settings2,
  Trash2,
  Play,
  CheckCircle2,
  Clock,
  Zap,
  Cpu,
  Globe,
  Database,
  RefreshCw,
  BarChart3,
  ShieldCheck,
  Activity,
  AlertCircle,
  ExternalLink,
  ChevronRight
} from 'lucide-react';
import { cn } from '../../../lib/utils';
import { useToast } from '../../../hooks/use-toast';
import { useNavigate } from 'react-router-dom';

interface ModelProvider {
  id: string;
  name: string;
  provider: 'OpenAI' | 'DeepSeek' | 'Tongyi' | 'Hunyuan' | 'Doubao' | 'Kimi' | string;
  baseUrl: string;
  apiKey: string;
  modelName: string;
  temperature: number;
  top_p: number;
  presence_penalty: number;
  frequency_penalty: number;
  maxTokens: number;
  status: 'active' | 'inactive';
  latency?: string;
  cost?: string;
  score?: number;
}

const PROVIDER_OPTIONS = [
  { id: 'OpenAI', name: 'OpenAI', icon: 'https://api.iconify.design/logos:openai-icon.svg' },
  { id: 'DeepSeek', name: 'DeepSeek', icon: 'https://api.iconify.design/logos:deepseek-icon.svg' },
  { id: 'Tongyi', name: '阿里通义千问', icon: 'https://api.iconify.design/logos:alibaba-icon.svg' },
  { id: 'Hunyuan', name: '腾讯混元', icon: 'https://api.iconify.design/logos:tencent-icon.svg' },
  { id: 'Doubao', name: '字节豆包', icon: 'https://api.iconify.design/logos:bytedance-icon.svg' },
  { id: 'Kimi', name: '月之暗面 Kimi', icon: 'https://api.iconify.design/logos:moon-icon.svg' },
];

export const ModelConfig: React.FC = () => {
  const { success, error } = useToast();
  const navigate = useNavigate();
  
  const [providers, setProviders] = useState<ModelProvider[]>([
    {
      id: '1',
      name: '生产环境主力',
      provider: 'OpenAI',
      baseUrl: 'https://api.openai.com/v1',
      apiKey: 'sk-**************',
      modelName: 'gpt-4o',
      temperature: 0.7,
      top_p: 1,
      presence_penalty: 0,
      frequency_penalty: 0,
      maxTokens: 2000,
      status: 'active',
      latency: '2.4s',
      cost: '¥0.12/1k tokens',
      score: 9.2
    },
    {
      id: '2',
      name: '备用模型 - 快速响应',
      provider: 'DeepSeek',
      baseUrl: 'https://api.deepseek.com/v1',
      apiKey: 'sk-**************',
      modelName: 'deepseek-chat',
      temperature: 0.5,
      top_p: 1,
      presence_penalty: 0,
      frequency_penalty: 0,
      maxTokens: 1500,
      status: 'active',
      latency: '1.2s',
      cost: '¥0.01/1k tokens',
      score: 8.8
    }
  ]);

  const [showAddForm, setShowAddForm] = useState(false);
  const [isTestingConnection, setIsTestingConnection] = useState<string | null>(null);
  const [testPrompt, setTestPrompt] = useState('顾客投诉：菜品太咸了，等了40分钟才上桌。请生成一段真诚的回复。');
  const [isTesting, setIsTesting] = useState(false);
  const [testResults, setTestResults] = useState<any[]>([]);
  
  // 新模型表单状态
  const [newProvider, setNewProvider] = useState({
    provider: 'OpenAI',
    name: '',
    apiKey: '',
    modelName: '',
    baseUrl: ''
  });

  const runTest = () => {
    setIsTesting(true);
    success('并发测试', '正在对多模型执行并发测试...');
    setTimeout(() => {
      setTestResults([
        {
          providerId: '1',
          response: '非常抱歉让您有不愉快的用餐体验。关于菜品偏咸及上菜慢的问题，我们已反馈给主厨和前厅管理团队。为了补偿您的损失，下次到店我们将赠送您一份精美甜品...',
          responseTime: '2.4s',
          tokens: 156,
          score: 9.2
        },
        {
          providerId: '2',
          response: '亲，实在对不起！听到您等了这么久且菜品口味不佳，我们深感内疚。我们会立即核查厨房流水并优化流程。感谢您的反馈，这对我们非常重要...',
          responseTime: '1.2s',
          tokens: 142,
          score: 8.8
        }
      ]);
      setIsTesting(false);
      success('测试完成', '所有模型测试完成，请查看结果。');
    }, 1500);
  };

  const testConnection = (id: string) => {
    setIsTestingConnection(id);
    success('连接测试', `正在测试模型 ${id === 'new' ? '新配置' : providers.find(p => p.id === id)?.name} 的连接...`);
    setTimeout(() => {
      setIsTestingConnection(null);
      success('连接成功', 'API 响应正常，延迟 2.4s。');
    }, 1000);
  };

  const handleSaveProvider = () => {
    if (!newProvider.name || !newProvider.apiKey) {
      error('保存失败', '请填写模型名称和 API Key');
      return;
    }
    const newId = (providers.length + 1).toString();
    const providerToAdd: ModelProvider = {
      id: newId,
      name: newProvider.name,
      provider: newProvider.provider,
      baseUrl: newProvider.baseUrl || 'https://api.openai.com/v1',
      apiKey: newProvider.apiKey,
      modelName: newProvider.modelName || 'gpt-4o',
      temperature: 0.7,
      top_p: 1,
      presence_penalty: 0,
      frequency_penalty: 0,
      maxTokens: 2000,
      status: 'active',
      latency: '2.0s',
      cost: '¥0.10/1k tokens',
      score: 9.0
    };
    setProviders([...providers, providerToAdd]);
    setShowAddForm(false);
    setNewProvider({ provider: 'OpenAI', name: '', apiKey: '', modelName: '', baseUrl: '' });
    success('保存成功', `模型 ${providerToAdd.name} 已添加并启用`);
  };

  const handleDeleteProvider = (id: string) => {
    const name = providers.find(p => p.id === id)?.name;
    setProviders(providers.filter(p => p.id !== id));
    success('删除成功', `模型 ${name} 已删除`);
  };

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-2 duration-500">
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        {/* Model List & Config */}
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="font-bold text-slate-800 flex items-center gap-2">
              <Cpu className="w-5 h-5 text-orange-600" />
              模型接口配置
            </h3>
            <Button size="sm" onClick={() => setShowAddForm(true)} className="gap-2 bg-orange-600 hover:bg-orange-700">
              <Plus className="w-4 h-4" /> 添加模型
            </Button>
          </div>
          
          <div className="grid gap-4">
            {showAddForm && (
              <Card className="p-6 border-2 border-orange-500 shadow-xl bg-orange-50/10">
                <div className="flex justify-between items-center mb-6">
                  <h4 className="font-bold text-slate-900">配置新模型接口</h4>
                  <Button variant="ghost" size="sm" onClick={() => setShowAddForm(false)}>取消</Button>
                </div>
                
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-slate-500">模型厂商</label>
                    <select 
                      value={newProvider.provider}
                      onChange={(e) => setNewProvider({...newProvider, provider: e.target.value})}
                      className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-orange-500/20"
                    >
                      {PROVIDER_OPTIONS.map(opt => (
                        <option key={opt.id} value={opt.id}>{opt.name}</option>
                      ))}
                    </select>
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-slate-500">自定义名称</label>
                    <Input 
                      value={newProvider.name}
                      onChange={(e) => setNewProvider({...newProvider, name: e.target.value})}
                      placeholder="如：测试实验室模型" className="bg-white" />
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-slate-500">API Key (必填)</label>
                    <Input 
                      type="password" 
                      value={newProvider.apiKey}
                      onChange={(e) => setNewProvider({...newProvider, apiKey: e.target.value})}
                      placeholder="sk-..." className="bg-white font-mono" />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-500">模型标识符</label>
                      <Input 
                        value={newProvider.modelName}
                        onChange={(e) => setNewProvider({...newProvider, modelName: e.target.value})}
                        placeholder="gpt-4 / qwen-max" className="bg-white" />
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-500">API 域名 (选填)</label>
                      <Input 
                        value={newProvider.baseUrl}
                        onChange={(e) => setNewProvider({...newProvider, baseUrl: e.target.value})}
                        placeholder="默认官方地址" className="bg-white" />
                    </div>
                  </div>
                </div>
                
                <div className="mt-6 flex gap-3">
                  <Button className="flex-1 bg-slate-900 hover:bg-slate-800" onClick={handleSaveProvider}>保存并启用</Button>
                  <Button variant="outline" className="gap-2" onClick={() => testConnection('new')}>
                    {isTestingConnection === 'new' ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Activity className="w-4 h-4" />}
                    连接测试
                  </Button>
                </div>
              </Card>
            )}

            {providers.map(p => (
              <Card key={p.id} className="p-4 border-slate-100 hover:border-orange-200 transition-all hover:shadow-md group">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex gap-4">
                    <div className="w-12 h-12 rounded-xl bg-slate-50 flex items-center justify-center border border-slate-100 shrink-0">
                      <img src={`https://modao.cc/agent-py/media/generated_images/2026-05-09/dccd6075d2724f05ac83a131bd7dfc90.jpg#desc=%24`} alt={`${p.provider} logo`} className="w-8 h-8 opacity-70" />
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-slate-900">{p.name}</span>
                        <Badge variant="outline" className="bg-slate-50 text-slate-600 border-slate-200 uppercase text-[10px]">
                          {p.provider}
                        </Badge>
                        {p.status === 'active' && (
                          <div className="flex items-center gap-1 text-[10px] text-emerald-500 font-medium">
                            <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse"></span>
                            在线
                          </div>
                        )}
                      </div>
                      <p className="text-xs text-slate-500 mt-1 font-mono">{p.modelName} · {p.baseUrl}</p>
                    </div>
                  </div>
                  <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-400 hover:text-blue-600" onClick={() => testConnection(p.id)}>
                      {isTestingConnection === p.id ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Activity className="w-4 h-4" />}
                    </Button>
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-400 hover:text-orange-600">
                      <Settings2 className="w-4 h-4" />
                    </Button>
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-400 hover:text-red-600" onClick={() => handleDeleteProvider(p.id)}>
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
                
                <div className="grid grid-cols-4 gap-4 bg-slate-50/50 p-3 rounded-xl border border-slate-100">
                  <div className="space-y-1">
                    <label className="text-[10px] text-slate-400 font-bold uppercase block">Temp</label>
                    <span className="text-xs font-bold text-slate-700">{p.temperature}</span>
                  </div>
                  <div className="space-y-1">
                    <label className="text-[10px] text-slate-400 font-bold uppercase block">延迟</label>
                    <div className="flex items-center gap-1">
                      <Clock className="w-3 h-3 text-slate-300" />
                      <span className="text-xs font-bold text-slate-700">{p.latency}</span>
                    </div>
                  </div>
                  <div className="space-y-1">
                    <label className="text-[10px] text-slate-400 font-bold uppercase block">预估成本</label>
                    <span className="text-xs font-bold text-slate-700">{p.cost}</span>
                  </div>
                  <div className="space-y-1">
                    <label className="text-[10px] text-slate-400 font-bold uppercase block">效能评分</label>
                    <div className="flex items-center gap-1">
                      <Zap className="w-3 h-3 text-amber-500 fill-amber-500" />
                      <span className="text-xs font-bold text-slate-700">{p.score}/10</span>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
        
        {/* Performance Comparison Panel */}
        <div className="space-y-6">
          <Card className="p-6 border-slate-100">
            <h4 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-blue-500" />
              性能对比看板 (24h 均值)
            </h4>
            <div className="space-y-6">
              {[
                { label: '平均响应时间 (秒)', data: [
                  { name: 'OpenAI', val: 2.4, color: 'bg-orange-500', width: '60%' },
                  { name: 'DeepSeek', val: 1.2, color: 'bg-blue-500', width: '30%' },
                  { name: 'Tongyi', val: 1.8, color: 'bg-purple-500', width: '45%' },
                  { name: 'Kimi', val: 2.1, color: 'bg-emerald-500', width: '52%' },
                ]},
                { label: '回复质量评分 (0-10)', data: [
                  { name: 'OpenAI', val: 9.4, color: 'bg-orange-500', width: '94%' },
                  { name: 'DeepSeek', val: 8.9, color: 'bg-blue-500', width: '89%' },
                  { name: 'Tongyi', val: 8.7, color: 'bg-purple-500', width: '87%' },
                  { name: 'Kimi', val: 9.1, color: 'bg-emerald-500', width: '91%' },
                ]}
              ].map(group => (
                <div key={group.label} className="space-y-3">
                  <div className="flex justify-between items-center">
                    <label className="text-xs font-bold text-slate-600">{group.label}</label>
                  </div>
                  <div className="space-y-2">
                    {group.data.map(item => (
                      <div key={item.name} className="flex items-center gap-3">
                        <span className="text-[10px] font-bold text-slate-400 w-16">{item.name}</span>
                        <div className="flex-1 h-2.5 bg-slate-100 rounded-full overflow-hidden">
                          <div className={cn("h-full rounded-full transition-all duration-1000", item.color)} style={{ width: item.width }} />
                        </div>
                        <span className="text-[10px] font-bold text-slate-700 w-8">{item.val}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card className="p-5 bg-slate-900 text-white overflow-hidden relative">
            <div className="absolute top-0 right-0 p-4 opacity-10">
              <Cpu className="w-24 h-24 rotate-12" />
            </div>
            <div className="relative z-10">
              <h4 className="text-sm font-bold mb-2 flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-orange-400" />
                资源负载预警
              </h4>
              <p className="text-slate-400 text-xs mt-1 leading-relaxed">
                检测到主模型 OpenAI 接口在高并发环境下延迟波动较大，建议配置自动降级规则。
              </p>
              <Button size="sm" className="bg-orange-500 hover:bg-orange-600 text-[11px] h-8 mt-4">
                配置自动降级路由 <ChevronRight className="w-3 h-3 ml-1" />
              </Button>
            </div>
          </Card>
        </div>
      </div>

      {/* Test Workbench */}
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <h3 className="font-bold text-slate-800 flex items-center gap-2">
            <Zap className="w-5 h-5 text-amber-500" />
            多模型测试工作台
          </h3>
          <div className="flex gap-2">
             <Button variant="outline" size="sm" className="gap-2" onClick={() => success('合规拦截', '已开启合规拦截')}>
                <ShieldCheck className="w-4 h-4" /> 开启合规拦截
              </Button>
              <Button 
                size="sm" 
                onClick={runTest} 
                disabled={isTesting}
                className="gap-2 bg-slate-900 hover:bg-slate-800 text-white"
              >
                {isTesting ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
                执行并发联调
              </Button>
          </div>
        </div>

        <Card className="p-4 space-y-4 border-slate-100">
          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="text-xs font-bold text-slate-500">测试场景模拟</label>
              <div className="flex gap-2">
                <Badge variant="outline" className="text-[9px] cursor-pointer hover:bg-slate-100" onClick={() => setTestPrompt('口味咸淡问题...')}>餐饮口味</Badge>
                <Badge variant="outline" className="text-[9px] cursor-pointer hover:bg-slate-100" onClick={() => setTestPrompt('服务员态度不好...')}>服务纠纷</Badge>
                <Badge variant="outline" className="text-[9px] cursor-pointer hover:bg-slate-100" onClick={() => setTestPrompt('环境卫生不达标...')}>环境卫生</Badge>
              </div>
            </div>
            <textarea 
              value={testPrompt}
              onChange={(e) => setTestPrompt(e.target.value)}
              className="w-full min-h-[120px] p-4 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all outline-none resize-none font-medium"
              placeholder="输入模拟评价内容..."
            />
          </div>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-2">
              <span className="text-xs font-bold text-slate-500 uppercase">输出内容对比</span>
              <span className="text-[10px] text-slate-400">已选：{providers.length} 个模型</span>
            </div>
            
            {testResults.length === 0 && !isTesting && (
              <div className="py-20 flex flex-col items-center justify-center text-slate-400 space-y-4 bg-slate-50/50 rounded-2xl border border-dashed border-slate-200">
                <Database className="w-12 h-12 opacity-10" />
                <div className="text-center">
                  <p className="text-sm font-bold text-slate-500">等待测试任务</p>
                  <p className="text-xs text-slate-400 mt-1">配置完成后点击上方"执行并发联调"</p>
                </div>
              </div>
            )}

            {isTesting && (
              <div className="py-20 flex flex-col items-center justify-center text-slate-400 space-y-4">
                <div className="relative">
                  <RefreshCw className="w-12 h-12 animate-spin text-orange-500" />
                  <Zap className="w-5 h-5 text-amber-500 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />
                </div>
                <div className="text-center">
                  <p className="text-sm font-bold text-slate-600 animate-pulse">正在穿透多厂商接口...</p>
                  <p className="text-xs text-slate-400 mt-1">正在模拟真实生产环境并发请求</p>
                </div>
              </div>
            )}

            <div className="space-y-6">
              {testResults.map((res, i) => {
                const provider = providers.find(p => p.id === res.providerId);
                return (
                  <div key={i} className="group">
                    <div className="flex justify-between items-center mb-2">
                      <div className="flex items-center gap-2">
                        <div className={cn(
                          "w-2 h-2 rounded-full",
                          i === 0 ? "bg-orange-500" : "bg-blue-500"
                        )} />
                        <span className="text-xs font-bold text-slate-700">{provider?.name}</span>
                        <span className="text-[10px] text-slate-400">({provider?.modelName})</span>
                      </div>
                      <div className="flex items-center gap-3">
                        <div className="flex items-center gap-1">
                          <Clock className="w-3 h-3 text-slate-400" />
                          <span className="text-[10px] font-medium text-slate-500">{res.responseTime}</span>
                        </div>
                        <Badge className={cn(
                          "text-[10px] py-0 h-4",
                          res.score >= 9 ? "bg-emerald-50 text-emerald-600 border-emerald-100" : "bg-blue-50 text-blue-600 border-blue-100"
                        )}>
                          效能: {res.score}
                        </Badge>
                      </div>
                    </div>
                    <div className="relative">
                      <div className="p-4 bg-white rounded-xl text-sm text-slate-600 border border-slate-200 leading-relaxed group-hover:border-orange-200 group-hover:shadow-sm transition-all">
                        {res.response}
                      </div>
                      <Button variant="ghost" size="sm" className="absolute bottom-2 right-2 h-7 text-[10px] gap-1 text-slate-400 hover:text-orange-600">
                        <ExternalLink className="w-3 h-3" /> 查看完整日志
                      </Button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

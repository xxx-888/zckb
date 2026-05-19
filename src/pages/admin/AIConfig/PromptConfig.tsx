import React, { useState, useMemo } from 'react';
import { Card } from '../../../components/ui/card';
import { Button } from '../../../components/ui/button';
import { Badge } from '../../../components/ui/badge';
import { Input } from '../../../components/ui/input';
import { 
  Wand2, 
  Smile, 
  UserCircle, 
  Type, 
  Ban, 
  Sparkles,
  ChevronRight,
  Info,
  Zap,
  Plus,
  FileEdit,
  Layout,
  MessageSquare,
  Search,
  Filter,
  Copy,
  Download,
  Upload,
  Settings,
  Eye,
  Trash2,
  Share2,
  RefreshCw
} from 'lucide-react';
import { cn } from '../../../lib/utils';
import { useToast } from '../../../hooks/use-toast';

interface Persona {
  id: string;
  label: string;
  icon: any;
  desc: string;
  traits: string[];
  style: string;
  tone: string;
  category: 'restaurant' | 'service' | 'brand';
}

interface ReplyTemplate {
  id: string;
  name: string;
  scenario: string;
  platform: string[];
  content: string;
  structure: string;
}

const PRESET_PERSONAS: Persona[] = [
  { id: 'warm', label: '热情客服', icon: Smile, desc: '语气活泼亲切，多使用语气助词和表情', traits: ['亲切', '活泼'], style: '口语化', tone: '感性', category: 'service' },
  { id: 'pro', label: '专业顾问', icon: UserCircle, desc: '用词考究，逻辑严密，给人极强的信任感', traits: ['专业', '严谨'], style: '书面语', tone: '中性', category: 'service' },
  { id: 'humor', label: '幽默店长', icon: Sparkles, desc: '风趣幽默，擅长化解尴尬，多见于年轻网红店', traits: ['风趣', '机智'], style: '网络语', tone: '幽默', category: 'restaurant' },
  { id: 'sincere', label: '诚恳老板', icon: UserCircle, desc: '朴实真诚，代表最高决策层直接对话', traits: ['真诚', '稳重'], style: '朴实', tone: '庄重', category: 'brand' },
];

const PRESET_TEMPLATES: ReplyTemplate[] = [
  { id: '1', name: '差评致歉-食材新鲜度', scenario: '投诉菜品不新鲜', platform: ['美团', '点评'], content: '亲爱的{用户昵称}，非常抱歉给您带来不佳体验。关于您提到的{菜品名称}不够新鲜的问题，店长已连夜核查供应链...', structure: '道歉+调查结果+补偿+承诺' },
  { id: '2', name: '好评回复-品牌故事', scenario: '优质长文好评', platform: ['小红书', '抖音'], content: '感谢{用户昵称}的认可！{门店名称}一直坚持手工现做，每一份{菜品名称}都承载着我们的初心...', structure: '感谢+共鸣+品牌价值+邀约' },
];

export const PromptConfig: React.FC = () => {
  const [activeSubTab, setActiveSubTab] = useState<'persona' | 'template' | 'editor'>('persona');
  const [personas, setPersonas] = useState<Persona[]>(PRESET_PERSONAS);
  const [selectedPersona, setSelectedPersona] = useState('warm');
  const [showNewPersona, setShowNewPersona] = useState(false);
  
  const [templates, setTemplates] = useState<ReplyTemplate[]>(PRESET_TEMPLATES);
  const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);
  
  const [customPrompt, setCustomPrompt] = useState('你是一名资深的餐饮店长，现在需要回复顾客的评价。要求：\n1. 语言亲切自然\n2. 针对具体问题给出解决方案\n3. 严禁使用官话套话\n4. 长度控制在150字左右');
  
  const [testComment, setTestComment] = useState('今天去吃饭，等了1个小时才上菜，而且服务员态度很差，菜还特别咸。');
  const [isPreviewing, setIsPreviewing] = useState(false);
  const [previewResult, setPreviewResult] = useState('');
  
  const [newPersonaData, setNewPersonaData] = useState({
    name: '',
    desc: '',
    traits: [] as string[],
    style: '活泼口语',
  });
  
  const { success, error } = useToast();
  
  const currentPersona = useMemo(() => personas.find(p => p.id === selectedPersona) || personas[0], [personas, selectedPersona]);

  const handleRunPreview = () => {
    if (!testComment.trim()) {
      error('测试失败', '请输入测试评价内容');
      return;
    }
    setIsPreviewing(true);
    success('开始测试', '正在使用当前配置生成回复...');
    setTimeout(() => {
      setPreviewResult(`【${currentPersona.label}模式渲染】\n\n亲爱的顾客，非常抱歉让您等了这么久！对于上菜慢和服务员态度的问题，我代表全店向您致歉。我们已经核实了当时的情况，是因为厨房系统突发故障导致的积压。至于您反映的菜品口味偏咸，厨师长已经记录并调整了配比。为了弥补您的不快，下次到店请联系我，我为您准备了特制甜品。再次抱歉！`);
      setIsPreviewing(false);
      success('测试完成', 'AI 回复已生成，请查看效果');
    }, 800);
  };

  const handleSavePersona = () => {
    if (!newPersonaData.name || !newPersonaData.desc) {
      error('保存失败', '请填写角色名称和描述');
      return;
    }
    const newId = (personas.length + 1).toString();
    const newPersona: Persona = {
      id: newId,
      label: newPersonaData.name,
      icon: UserCircle,
      desc: newPersonaData.desc,
      traits: newPersonaData.traits.length > 0 ? newPersonaData.traits : ['自定义'],
      style: newPersonaData.style,
      tone: '中性',
      category: 'service',
    };
    setPersonas([...personas, newPersona]);
    setShowNewPersona(false);
    setNewPersonaData({ name: '', desc: '', traits: [], style: '活泼口语' });
    success('保存成功', `角色 "${newPersonaData.name}" 已创建`);
  };

  const handleDeletePersona = (id: string) => {
    const name = personas.find(p => p.id === id)?.label;
    setPersonas(personas.filter(p => p.id !== id));
    if (selectedPersona === id) {
      setSelectedPersona(personas[0]?.id || '');
    }
    success('删除成功', `角色 "${name}" 已删除`);
  };

  const handleSavePrompt = () => {
    if (!customPrompt.trim()) {
      error('保存失败', '提示词内容不能为空');
      return;
    }
    success('保存成功', '自定义提示词已应用到全局');
  };

  const handleCopyTemplate = (content: string) => {
    navigator.clipboard.writeText(content);
    success('复制成功', '模板内容已复制到剪贴板');
  };

  const handleImportPersona = () => {
    success('导入角色', '正在打开角色导入对话框...');
  };

  const handleExportReport = () => {
    success('导出报告', '正在生成测试报告...');
    setTimeout(() => {
      success('导出完成', '测试报告已下载');
    }, 1000);
  };

  return (
    <div className="flex gap-6 animate-in fade-in slide-in-from-bottom-2 duration-500 min-h-[700px]">
      {/* Main Config Area */}
      <div className="flex-1 space-y-6 overflow-hidden">
        {/* Sub-tab Navigation */}
        <div className="flex border-b border-slate-200">
          {[
            { id: 'persona', label: '角色设定', icon: UserCircle },
            { id: 'template', label: '回复模板', icon: Layout },
            { id: 'editor', label: '自定义提示词', icon: FileEdit },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveSubTab(tab.id as any)}
              className={cn(
                "flex items-center gap-2 px-6 py-3 text-sm font-bold transition-all border-b-2 -mb-px",
                activeSubTab === tab.id 
                  ? "border-purple-600 text-purple-600" 
                  : "border-transparent text-slate-400 hover:text-slate-600"
              )}
            >
              <tab.icon className="w-4 h-4" />
              {tab.label}
            </button>
          ))}
        </div>

        <div className="space-y-6">
          {activeSubTab === 'persona' && (
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <div className="flex gap-4">
                   <div className="relative">
                    <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                    <input 
                      className="pl-9 pr-4 py-1.5 bg-slate-100 border-none rounded-lg text-xs w-48 outline-none focus:ring-1 focus:ring-purple-500" 
                      placeholder="搜索角色..." 
                    />
                  </div>
                  <div className="flex gap-2">
                    <Badge className="bg-purple-50 text-purple-600 border-purple-100 cursor-pointer hover:bg-purple-100 transition-colors">全部</Badge>
                    <Badge variant="outline" className="text-slate-400 cursor-pointer hover:bg-slate-50">餐饮行业</Badge>
                    <Badge variant="outline" className="text-slate-400 cursor-pointer hover:bg-slate-50">服务类型</Badge>
                  </div>
                </div>
                <div className="flex gap-2">
                   <Button variant="outline" size="sm" className="gap-1 text-[11px] h-8" onClick={handleImportPersona}>
                    <Upload className="w-3.5 h-3.5" /> 导入角色
                  </Button>
                  <Button size="sm" className="gap-1 bg-purple-600 hover:bg-purple-700 text-[11px] h-8" onClick={() => setShowNewPersona(true)}>
                    <Plus className="w-3.5 h-3.5" /> 新建角色
                  </Button>
                </div>
              </div>

              {showNewPersona && (
                <Card className="p-6 border-2 border-purple-500 bg-purple-50/10 animate-in zoom-in-95 duration-200">
                  <h4 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
                    <Plus className="w-4 h-4" /> 定义新 AI 角色
                  </h4>
                  <div className="grid grid-cols-2 gap-6 mb-6">
                    <div className="space-y-4">
                      <div className="space-y-1.5">
                        <label className="text-xs font-bold text-slate-500">角色名称</label>
                        <Input 
                          value={newPersonaData.name}
                          onChange={(e) => setNewPersonaData({...newPersonaData, name: e.target.value})}
                          placeholder="如：活力值班经理" 
                        />
                      </div>
                      <div className="space-y-1.5">
                        <label className="text-xs font-bold text-slate-500">角色描述</label>
                        <textarea 
                          value={newPersonaData.desc}
                          onChange={(e) => setNewPersonaData({...newPersonaData, desc: e.target.value})}
                          className="w-full h-20 p-3 bg-white border border-slate-200 rounded-lg text-sm resize-none outline-none focus:ring-2 focus:ring-purple-500/20" 
                          placeholder="描述角色的身份背景..." 
                        />
                      </div>
                    </div>
                    <div className="space-y-4">
                      <div className="space-y-1.5">
                        <label className="text-xs font-bold text-slate-500">性格特征</label>
                        <div className="flex flex-wrap gap-2">
                          {['稳重', '幽默', '干练', '温柔'].map(t => (
                            <Badge 
                              key={t} 
                              variant={newPersonaData.traits.includes(t) ? "default" : "outline"} 
                              className={`cursor-pointer transition-colors ${newPersonaData.traits.includes(t) ? "bg-purple-600 text-white" : "hover:bg-purple-50 hover:text-purple-600"}`}
                              onClick={() => {
                                if (newPersonaData.traits.includes(t)) {
                                  setNewPersonaData({...newPersonaData, traits: newPersonaData.traits.filter(tr => tr !== t)});
                                } else {
                                  setNewPersonaData({...newPersonaData, traits: [...newPersonaData.traits, t]});
                                }
                              }}
                            >
                              {t}
                            </Badge>
                          ))}
                        </div>
                      </div>
                      <div className="space-y-1.5">
                        <label className="text-xs font-bold text-slate-500">语言风格</label>
                        <select 
                          value={newPersonaData.style}
                          onChange={(e) => setNewPersonaData({...newPersonaData, style: e.target.value})}
                          className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-purple-500/20"
                        >
                          <option>活泼口语</option>
                          <option>职场专业</option>
                          <option>传统朴实</option>
                        </select>
                      </div>
                    </div>
                  </div>
                  <div className="flex gap-3 pt-4 border-t border-slate-100">
                    <Button className="flex-1 bg-purple-600 hover:bg-purple-700" onClick={handleSavePersona}>保存角色</Button>
                    <Button variant="ghost" onClick={() => setShowNewPersona(false)}>取消</Button>
                  </div>
                </Card>
              )}

              <div className="grid grid-cols-2 gap-4">
                {personas.map(p => (
                  <Card 
                    key={p.id}
                    onClick={() => setSelectedPersona(p.id)}
                    className={cn(
                      "p-4 border-2 cursor-pointer transition-all flex items-start gap-4 group relative overflow-hidden",
                      selectedPersona === p.id 
                        ? "border-purple-500 bg-purple-50/30 shadow-sm" 
                        : "border-slate-100 hover:border-slate-200 bg-white"
                    )}
                  >
                    <div className={cn(
                      "w-12 h-12 rounded-xl flex items-center justify-center shrink-0 border",
                      selectedPersona === p.id ? "bg-purple-500 text-white border-purple-400" : "bg-slate-50 text-slate-400 border-slate-100"
                    )}>
                      <p.icon className="w-6 h-6" />
                    </div>
                    <div className="flex-1">
                      <div className="flex justify-between items-center">
                        <h4 className={cn("font-bold text-sm", selectedPersona === p.id ? "text-purple-700" : "text-slate-700")}>
                          {p.label}
                        </h4>
                        <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button 
                            className="p-1 text-slate-400 hover:text-blue-500 transition-colors" 
                            onClick={(e) => { e.stopPropagation(); handleCopyTemplate(p.desc); }}
                          >
                            <Copy className="w-3 h-3" />
                          </button>
                          <button 
                            className="p-1 text-slate-400 hover:text-purple-500 transition-colors"
                            onClick={(e) => e.stopPropagation()}
                          >
                            <Settings className="w-3 h-3" />
                          </button>
                          <button 
                            className="p-1 text-slate-400 hover:text-red-500 transition-colors"
                            onClick={(e) => { e.stopPropagation(); handleDeletePersona(p.id); }}
                          >
                            <Trash2 className="w-3 h-3" />
                          </button>
                        </div>
                      </div>
                      <p className="text-[11px] text-slate-500 leading-relaxed mt-1 line-clamp-2">{p.desc}</p>
                      <div className="flex gap-1.5 mt-3">
                        {p.traits.map(t => (
                          <span key={t} className="text-[9px] px-1.5 py-0.5 bg-slate-100 rounded text-slate-500 font-medium">{t}</span>
                        ))}
                      </div>
                    </div>
                    {selectedPersona === p.id && (
                      <div className="absolute right-0 top-0 p-1">
                        <Badge className="bg-purple-500 text-[8px] py-0 h-4">Active</Badge>
                      </div>
                    )}
                  </Card>
                ))}
                <Card 
                  className="p-4 border-2 border-dashed border-slate-200 bg-slate-50/50 flex flex-col items-center justify-center gap-2 cursor-pointer hover:border-purple-300 hover:bg-purple-50/30 transition-all group" 
                  onClick={() => setShowNewPersona(true)}
                >
                  <div className="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-300 group-hover:text-purple-500 group-hover:border-purple-200 shadow-sm transition-all">
                    <Plus className="w-5 h-5" />
                  </div>
                  <span className="text-xs font-bold text-slate-400 group-hover:text-purple-600 transition-all">创建自定义角色</span>
                </Card>
              </div>
            </div>
          )}
          
          {activeSubTab === 'template' && (
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <h4 className="font-bold text-slate-800 flex items-center gap-2">
                  <Layout className="w-4 h-4 text-purple-600" />
                  回复模板库
                </h4>
                <Button size="sm" className="gap-1 bg-purple-600 hover:bg-purple-700 text-[11px] h-8">
                  <Plus className="w-3.5 h-3.5" /> 创建新模板
                </Button>
              </div>

              <div className="grid grid-cols-1 gap-4">
                {templates.map(t => (
                  <Card key={t.id} className="p-5 border-slate-100 hover:border-purple-200 transition-all group">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h5 className="font-bold text-slate-900 flex items-center gap-2">
                          {t.name}
                          <Badge variant="outline" className="text-[9px] h-4">Markdown 支持</Badge>
                        </h5>
                        <div className="flex items-center gap-3 mt-1.5">
                          <span className="text-[11px] text-slate-400 font-medium flex items-center gap-1">
                             场景：<span className="text-slate-600">{t.scenario}</span>
                          </span>
                          <span className="text-[11px] text-slate-400 font-medium flex items-center gap-1">
                             平台：{t.platform.map(p => <Badge key={p} className="bg-slate-100 text-slate-600 border-none text-[8px] h-3.5 py-0">{p}</Badge>)}
                          </span>
                        </div>
                      </div>
                      <div className="flex gap-2">
                         <Button 
                           variant="ghost" 
                           size="sm" 
                           className="h-7 text-[10px] gap-1 text-slate-400 hover:text-purple-600"
                           onClick={() => handleCopyTemplate(t.content)}
                         >
                          <Copy className="w-3 h-3" /> 复用
                        </Button>
                        <Button variant="ghost" size="sm" className="h-7 text-[10px] gap-1 text-slate-400 hover:text-blue-600">
                          <FileEdit className="w-3 h-3" /> 编辑
                        </Button>
                      </div>
                    </div>
                    <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                      <p className="text-xs text-slate-500 font-mono leading-relaxed whitespace-pre-wrap">{t.content}</p>
                    </div>
                    <div className="mt-3 flex items-center justify-between">
                      <div className="flex gap-2">
                        {['用户昵称', '菜品名称', '门店名称'].map(v => (
                          <span key={v} className="text-[9px] px-1.5 py-0.5 bg-purple-50 text-purple-600 rounded border border-purple-100">{`{${v}}`}</span>
                        ))}
                      </div>
                      <span className="text-[10px] text-slate-400 italic">结构: {t.structure}</span>
                    </div>
                  </Card>
                ))}
              </div>
            </div>
          )}
          
          {activeSubTab === 'editor' && (
            <div className="space-y-6">
              <Card className="p-6 border-slate-100 bg-slate-900 text-white relative overflow-hidden">
                <div className="absolute top-0 right-0 p-6 opacity-10">
                  <FileEdit className="w-32 h-32" />
                </div>
                <div className="relative z-10">
                  <h4 className="font-bold text-white mb-4 flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-amber-400" />
                    自定义 System Prompt 编辑器
                  </h4>
                  <p className="text-xs text-slate-400 mb-6 leading-relaxed max-w-2xl">
                    通过精细化的指令编排，您可以彻底定义 AI 的回复逻辑。支持插入全局变量和动态逻辑。
                    点击"变量面板"可查看所有可用占位符。
                  </p>
                  
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                       <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Markdown 源代码</label>
                       <div className="flex gap-2">
                          <Badge className="bg-white/10 text-white border-white/20 hover:bg-white/20 cursor-pointer transition-colors">变量面板</Badge>
                          <Badge className="bg-white/10 text-white border-white/20 hover:bg-white/20 cursor-pointer transition-colors">常用片段</Badge>
                       </div>
                    </div>
                    <textarea 
                      value={customPrompt}
                      onChange={(e) => setCustomPrompt(e.target.value)}
                      className="w-full h-80 bg-black/40 border border-white/10 rounded-xl p-4 font-mono text-sm text-amber-50 outline-none focus:ring-2 focus:ring-purple-500/50 transition-all resize-none"
                    />
                    <div className="flex justify-between items-center pt-2">
                      <div className="flex items-center gap-4">
                        <span className="text-[10px] text-slate-500 font-mono">Tokens: {Math.ceil(customPrompt.length / 1.5)}</span>
                        <span className="text-[10px] text-slate-500 font-mono">Lines: {customPrompt.split('\n').length}</span>
                      </div>
                      <div className="flex gap-2">
                        <Button 
                          variant="ghost" 
                          size="sm" 
                          className="h-8 text-xs text-slate-400 hover:text-white border border-white/10"
                          onClick={() => {
                            setCustomPrompt('你是一名资深的餐饮店长，现在需要回复顾客的评价。要求：\n1. 语言亲切自然\n2. 针对具体问题给出解决方案\n3. 严禁使用官话套话\n4. 长度控制在150字左右');
                            success('已重置', '提示词已恢复到默认状态');
                          }}
                        >
                          放弃修改
                        </Button>
                        <Button 
                          size="sm" 
                          className="h-8 text-xs bg-purple-600 hover:bg-purple-700"
                          onClick={handleSavePrompt}
                        >
                          保存并应用到全局
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              </Card>

              <div className="grid grid-cols-2 gap-6">
                <Card className="p-5 border-slate-100">
                  <h5 className="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                    <Type className="w-4 h-4 text-slate-400" />
                    参数微调
                  </h5>
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between mb-2">
                        <label className="text-[11px] font-bold text-slate-500">字数弹性控制 (±20%)</label>
                        <Badge className="bg-slate-100 text-slate-600 border-none">150 字</Badge>
                      </div>
                      <input type="range" className="w-full h-1 bg-slate-100 rounded-lg appearance-none cursor-pointer accent-purple-600" />
                    </div>
                    <div className="pt-4 border-t border-slate-50 space-y-3">
                       <label className="text-[11px] font-bold text-slate-500">禁忌策略</label>
                       <div className="space-y-2">
                          {['拦截涉黄涉政', '拦截恶意比价', '拦截竞争对手点名'].map(l => (
                            <div key={l} className="flex items-center justify-between">
                              <span className="text-xs text-slate-600">{l}</span>
                              <div className="w-8 h-4 bg-purple-600 rounded-full relative cursor-pointer">
                                <div className="absolute right-0.5 top-0.5 w-3 h-3 bg-white rounded-full" />
                              </div>
                            </div>
                          ))}
                       </div>
                    </div>
                  </div>
                </Card>
                <Card className="p-5 border-slate-100 bg-purple-50/50">
                   <h5 className="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                    <Share2 className="w-4 h-4 text-purple-400" />
                    最佳实践分享
                  </h5>
                  <div className="space-y-3">
                    {[
                      { title: '网红火锅店专属话术', author: '智策AI' },
                      { title: '轻食沙拉专业风范', author: '智策AI' },
                    ].map(p => (
                      <div key={p.title} className="flex items-center justify-between p-2 bg-white rounded border border-slate-100 hover:border-purple-200 transition-colors cursor-pointer">
                        <div className="text-xs">
                          <p className="font-bold text-slate-700">{p.title}</p>
                          <p className="text-[10px] text-slate-400 mt-0.5">作者：{p.author}</p>
                        </div>
                        <Button 
                          variant="ghost" 
                          size="icon" 
                          className="h-6 w-6 text-purple-600"
                          onClick={() => success('下载模板', `正在下载 "${p.title}"...`)}
                        >
                          <Download className="w-3.5 h-3.5" />
                        </Button>
                      </div>
                    ))}
                    <button className="w-full py-2 text-[10px] font-bold text-purple-600 border border-dashed border-purple-200 rounded mt-2 hover:bg-purple-100/50 transition-all">查看角色广场</button>
                  </div>
                </Card>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Right Preview & Validation Panel */}
      <div className="w-[380px] space-y-6">
        <Card className="p-6 border-slate-100 sticky top-6 shadow-xl shadow-slate-200/50 flex flex-col h-[calc(100vh-200px)]">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-bold text-slate-800 flex items-center gap-2">
              <Eye className="w-5 h-5 text-orange-500" />
              实时效果预览
            </h3>
            <Badge variant="outline" className="text-[10px] font-mono">PROD MODE</Badge>
          </div>

          <div className="space-y-4 flex-1 overflow-y-auto pr-2 custom-scrollbar">
            <div className="space-y-2">
              <label className="text-[10px] font-bold text-slate-400 uppercase">输入示例评价</label>
              <textarea 
                value={testComment}
                onChange={(e) => setTestComment(e.target.value)}
                className="w-full h-24 p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs resize-none outline-none focus:ring-2 focus:ring-purple-500/20"
                placeholder="在此输入或粘贴一段真实的差评..."
              />
              <div className="flex gap-2">
                <Button 
                  onClick={handleRunPreview}
                  disabled={isPreviewing}
                  className="flex-1 bg-slate-900 hover:bg-slate-800 text-xs h-9 gap-2"
                >
                  {isPreviewing ? <RefreshCw className="w-3 h-3 animate-spin" /> : <Zap className="w-3 h-3 text-amber-400" />}
                  测试当前配置
                </Button>
                <Button variant="outline" size="icon" className="h-9 w-9 border-slate-200">
                  <Settings className="w-4 h-4 text-slate-400" />
                </Button>
              </div>
            </div>

            <div className="space-y-2 pt-4">
              <label className="text-[10px] font-bold text-slate-400 uppercase flex justify-between">
                输出效果
                {previewResult && <span className="text-emerald-500 font-bold tracking-tighter animate-pulse">GENERATED</span>}
              </label>
              <div className={cn(
                "w-full min-h-[200px] p-4 rounded-xl border-2 transition-all leading-relaxed relative",
                isPreviewing ? "bg-slate-50 border-slate-100 opacity-60" : 
                previewResult ? "bg-purple-50/20 border-purple-100" : "bg-slate-50 border-dashed border-slate-200"
              )}>
                {!previewResult && !isPreviewing && (
                  <div className="absolute inset-0 flex flex-col items-center justify-center text-slate-300 gap-2">
                    <MessageSquare className="w-8 h-8 opacity-20" />
                    <p className="text-[10px] font-bold">待生成渲染结果</p>
                  </div>
                )}
                {isPreviewing && (
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="flex gap-1.5">
                      <div className="w-1.5 h-1.5 bg-purple-400 rounded-full animate-bounce [animation-delay:-0.3s]" />
                      <div className="w-1.5 h-1.5 bg-purple-400 rounded-full animate-bounce [animation-delay:-0.15s]" />
                      <div className="w-1.5 h-1.5 bg-purple-400 rounded-full animate-bounce" />
                    </div>
                  </div>
                )}
                <p className="text-xs text-slate-600 whitespace-pre-wrap">{previewResult}</p>
              </div>
            </div>

            {previewResult && (
              <div className="space-y-3 animate-in fade-in slide-in-from-top-4 duration-500">
                <label className="text-[10px] font-bold text-slate-400 uppercase">AI 自我评分 (模型反馈)</label>
                <div className="grid grid-cols-2 gap-3">
                  {[
                    { label: '品牌一致性', score: 9.8 },
                    { label: '共情深度', score: 9.2 },
                    { label: '方案具象度', score: 8.5 },
                    { label: '禁忌词过滤', score: 10 },
                  ].map(s => (
                    <div key={s.label} className="bg-white p-2 border border-slate-100 rounded-lg shadow-sm">
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-[9px] font-bold text-slate-500">{s.label}</span>
                        <span className="text-[10px] font-bold text-purple-600">{s.score}</span>
                      </div>
                      <div className="h-1 bg-slate-100 rounded-full overflow-hidden">
                        <div className="h-full bg-purple-500 rounded-full" style={{ width: `${s.score * 10}%` }} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="pt-6 border-t border-slate-100 mt-auto">
            <Button 
              variant="outline" 
              className="w-full text-[11px] h-9 gap-2 border-slate-200 text-slate-500 hover:bg-slate-50"
              onClick={handleExportReport}
            >
              <Download className="w-3.5 h-3.5" /> 批量导出测试报告
            </Button>
            <p className="text-[10px] text-slate-400 mt-3 text-center">
              上次测试完成于: 今天 14:32:10 (耗时 1.2s)
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
};

import React, { useState, useEffect } from 'react';
import { Card } from '../../../components/ui/card';
import { Button } from '../../../components/ui/button';
import { Badge } from '../../../components/ui/badge';
import { 
  Activity, 
  BarChart3, 
  Terminal, 
  Zap, 
  RefreshCw,
  Search,
  Filter,
  Monitor,
  CheckCircle,
  AlertTriangle,
  TrendingUp,
  Download,
  Upload
} from 'lucide-react';
import { cn } from '../../../lib/utils';
import { useToast } from '../../../hooks/use-toast';

interface LogEntry {
  id: string;
  time: string;
  event: string;
  model: string;
  prompt: string;
  latency: string;
  status: string;
}

export const Monitoring: React.FC = () => {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [activeTab, setActiveTab] = useState<'realtime' | 'ab_test'>('realtime');
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [abTestRunning, setAbTestRunning] = useState(false);
  
  const { success, error } = useToast();

  useEffect(() => {
    if (activeTab === 'realtime') {
      // Simulate real-time logs
      const interval = setInterval(() => {
        const newLog: LogEntry = {
          id: Math.random().toString(36).substr(2, 9),
          time: new Date().toLocaleTimeString(),
          event: '回复生成',
          model: Math.random() > 0.5 ? 'GPT-4o' : 'DeepSeek',
          prompt: '品牌人格-热情客服',
          latency: (Math.random() * 2 + 1).toFixed(2) + 's',
          status: 'success'
        };
        setLogs(prev => [newLog, ...prev].slice(0, 10));
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [activeTab]);

  const handleRefresh = () => {
    setIsRefreshing(true);
    success('刷新数据', '正在重新获取监控数据...');
    setTimeout(() => {
      setIsRefreshing(false);
      success('刷新完成', '监控数据已更新');
    }, 1000);
  };

  const handleForceSync = () => {
    success('强制刷新', '正在强制同步所有节点配置...');
    setTimeout(() => {
      success('同步完成', '124/124 节点已同步，未发现异常');
    }, 1500);
  };

  const handleApplyConfig = () => {
    success('应用配置', '正在将 B 组配置全量应用到所有门店...');
    setTimeout(() => {
      success('应用成功', 'B 组配置已全量发布，所有流量已切换');
    }, 2000);
  };

  const handleStartABTest = () => {
    setAbTestRunning(true);
    success('A/B 测试', '正在启动 A/B 测试实验...');
    setTimeout(() => {
      setAbTestRunning(false);
      success('测试完成', 'A/B 测试已完成，B 组表现更优');
    }, 3000);
  };

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-2 duration-500">
      <div className="flex bg-slate-100 p-1 rounded-xl w-fit mb-4">
        <button
          onClick={() => setActiveTab('realtime')}
          className={cn(
            "flex items-center gap-2 px-6 py-2 rounded-lg text-sm font-bold transition-all",
            activeTab === 'realtime' ? "bg-white text-orange-600 shadow-sm" : "text-slate-500 hover:text-slate-700"
          )}
        >
          <Activity className="w-4 h-4" />
          实时流监控
        </button>
        <button
          onClick={() => setActiveTab('ab_test')}
          className={cn(
            "flex items-center gap-2 px-6 py-2 rounded-lg text-sm font-bold transition-all",
            activeTab === 'ab_test' ? "bg-white text-orange-600 shadow-sm" : "text-slate-500 hover:text-slate-700"
          )}
        >
          <BarChart3 className="w-4 h-4" />
          A/B 测试实验
        </button>
      </div>

      {activeTab === 'realtime' ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Monitor */}
          <div className="lg:col-span-2 space-y-4">
            <Card className="p-0 border-slate-100 overflow-hidden bg-slate-950 text-slate-300 font-mono text-xs">
              <div className="bg-slate-900 px-4 py-2 border-b border-slate-800 flex justify-between items-center">
                <div className="flex items-center gap-2">
                  <Terminal className="w-4 h-4 text-emerald-500" />
                  <span className="font-bold text-slate-400">AI 实时处理日志</span>
                </div>
                <div className="flex items-center gap-2">
                  <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-[10px]">
                    ● 正在监听
                  </Badge>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-6 text-[10px] text-slate-400 hover:text-white"
                    onClick={handleRefresh}
                    disabled={isRefreshing}
                  >
                    {isRefreshing ? <RefreshCw className="w-3 h-3 animate-spin" /> : <RefreshCw className="w-3 h-3" />}
                    刷新
                  </Button>
                </div>
              </div>
              <div className="p-4 space-y-3 min-h-[400px]">
                {logs.length === 0 && <p className="text-slate-600 italic">正在等待数据流入...</p>}
                {logs.map((log) => (
                  <div key={log.id} className="flex gap-4 group">
                    <span className="text-slate-600 shrink-0">[{log.time}]</span>
                    <span className="text-emerald-500 shrink-0 uppercase">{log.event}</span>
                    <span className="text-blue-400">model={log.model}</span>
                    <span className="text-purple-400">prompt={log.prompt}</span>
                    <span className="text-amber-500">latency={log.latency}</span>
                    <span className="text-slate-500 group-hover:text-slate-300 transition-colors">...SUCCESS</span>
                  </div>
                ))}
              </div>
            </Card>

            <div className="grid grid-cols-3 gap-4">
              <Card className="p-4 border-slate-100 bg-white">
                <p className="text-[10px] font-bold text-slate-400 uppercase mb-1">今日调用总量</p>
                <p className="text-xl font-bold text-slate-900">12,482</p>
                <div className="mt-2 flex items-center gap-1 text-[10px] text-emerald-500">
                  <TrendingUp className="w-3 h-3" />
                  +12% 环比昨日
                </div>
              </Card>
              <Card className="p-4 border-slate-100 bg-white">
                <p className="text-[10px] font-bold text-slate-400 uppercase mb-1">平均响应延迟</p>
                <p className="text-xl font-bold text-slate-900">1.64s</p>
                <div className="mt-2 flex items-center gap-1 text-[10px] text-emerald-500">
                  <TrendingUp className="w-3 h-3" />
                  -0.3s 性能提升
                </div>
              </Card>
              <Card className="p-4 border-slate-100 bg-white">
                <p className="text-[10px] font-bold text-slate-400 uppercase mb-1">异常报错率</p>
                <p className="text-xl font-bold text-slate-900">0.04%</p>
                <div className="mt-2 flex items-center gap-1 text-[10px] text-emerald-500">
                  <CheckCircle className="w-3 h-3" />
                  稳定运行中
                </div>
              </Card>
            </div>
          </div>

          {/* Sidebar Stats */}
          <div className="space-y-6">
            <Card className="p-6 border-slate-100">
              <h4 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                <Monitor className="w-4 h-4 text-orange-500" />
                热更新控制台
              </h4>
              <p className="text-xs text-slate-500 mb-6">修改规则或提示词后，可在此一键推送至所有边缘节点，无需重启服务。</p>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-100">
                  <div>
                    <p className="text-xs font-bold text-slate-700">配置同步状态</p>
                    <p className="text-[10px] text-emerald-600 font-medium">124/124 节点已同步</p>
                  </div>
                  <Button 
                    size="sm" 
                    className="bg-slate-900 hover:bg-slate-800 text-white text-[10px] h-7"
                    onClick={handleForceSync}
                  >
                    强制刷新
                  </Button>
                </div>

                <div className="p-4 bg-orange-50 rounded-xl border border-orange-100">
                  <div className="flex items-start gap-3">
                    <Zap className="w-4 h-4 text-orange-500 mt-0.5" />
                    <div>
                      <h5 className="text-[11px] font-bold text-orange-900">配置增量发布 (Canary)</h5>
                      <p className="text-[10px] text-orange-700 mt-1 leading-relaxed">
                        您可以先对 5% 的流量应用新规则进行观察，确认无异常后再全量发布。
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </Card>

            <Card className="p-5 border-slate-100">
              <h4 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                <Activity className="w-4 h-4 text-blue-500" />
                实时监控设置
              </h4>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-600">自动刷新频率</span>
                  <select className="text-[10px] px-2 py-1 bg-slate-50 border border-slate-200 rounded">
                    <option>3 秒</option>
                    <option>5 秒</option>
                    <option>10 秒</option>
                  </select>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-600">日志级别</span>
                  <select className="text-[10px] px-2 py-1 bg-slate-50 border border-slate-200 rounded">
                    <option>INFO</option>
                    <option>DEBUG</option>
                    <option>ERROR</option>
                  </select>
                </div>
                <Button 
                  size="sm" 
                  variant="outline" 
                  className="w-full text-[10px] h-7"
                  onClick={() => success('设置已保存', '监控设置已更新')}
                >
                  保存设置
                </Button>
              </div>
            </Card>
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h3 className="font-bold text-slate-800 text-lg">A/B 测试实验管理</h3>
            <Button 
              size="sm" 
              className="gap-2 bg-blue-600 hover:bg-blue-700"
              onClick={handleStartABTest}
              disabled={abTestRunning}
            >
              {abTestRunning ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Activity className="w-4 h-4" />}
              {abTestRunning ? '测试进行中...' : '启动新实验'}
            </Button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card className="p-6 border-slate-100 relative overflow-hidden">
              <div className="absolute top-4 right-4">
                <Badge className="bg-blue-600 text-white border-transparent">实验 A: 热情客服</Badge>
              </div>
              <h4 className="font-bold text-slate-800 mb-6">对照组 (Control)</h4>
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="p-3 bg-slate-50 rounded-lg">
                  <p className="text-[10px] text-slate-400 font-bold mb-1">采纳率</p>
                  <p className="text-2xl font-bold text-slate-900">72.4%</p>
                </div>
                <div className="p-3 bg-slate-50 rounded-lg">
                  <p className="text-[10px] text-slate-400 font-bold mb-1">满意度</p>
                  <p className="text-2xl font-bold text-slate-900">4.2</p>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-[10px] font-bold text-slate-500 uppercase">
                  <span>转化效率</span>
                  <span>72%</span>
                </div>
                <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                  <div className="h-full bg-blue-500 w-[72%]" />
                </div>
              </div>
            </Card>

            <Card className="p-6 border-slate-100 border-2 border-emerald-500/20 relative overflow-hidden">
              <div className="absolute top-4 right-4">
                <Badge className="bg-emerald-600 text-white border-transparent">实验 B: 诚恳老板</Badge>
              </div>
              <div className="absolute top-0 right-0 p-1 bg-emerald-500 text-white text-[8px] font-bold uppercase rotate-45 translate-x-3 -translate-y-1 w-16 text-center shadow-sm">
                WINNER
              </div>
              <h4 className="font-bold text-slate-800 mb-6">实验组 (Variation)</h4>
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="p-3 bg-emerald-50 rounded-lg">
                  <p className="text-[10px] text-emerald-600 font-bold mb-1">采纳率</p>
                  <p className="text-2xl font-bold text-slate-900">89.1%</p>
                </div>
                <div className="p-3 bg-emerald-50 rounded-lg">
                  <p className="text-[10px] text-emerald-600 font-bold mb-1">满意度</p>
                  <p className="text-2xl font-bold text-slate-900">4.8</p>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-[10px] font-bold text-slate-500 uppercase">
                  <span>转化效率 (+17%)</span>
                  <span>89%</span>
                </div>
                <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500 w-[89%]" />
                </div>
              </div>
            </Card>
          </div>
          
          <Card className="p-6 border-slate-100 text-center py-12">
            <BarChart3 className="w-12 h-12 text-slate-200 mx-auto mb-4" />
            <h4 className="font-bold text-slate-800 mb-2">基于当前实验结果的建议</h4>
            <p className="text-sm text-slate-500 max-w-md mx-auto">
              基于当前的置信度 (98.4%)，我们强烈建议将实验组 B (诚恳老板) 的规则策略全量发布到所有门店。
            </p>
            <Button 
              className="mt-6 bg-emerald-600 hover:bg-emerald-700 text-white gap-2 px-8"
              onClick={handleApplyConfig}
            >
              <Zap className="w-4 h-4" /> 采纳并全量应用 B 组配置
            </Button>
          </Card>
        </div>
      )}
    </div>
  );
};

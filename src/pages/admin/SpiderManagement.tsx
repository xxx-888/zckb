import React, { useState } from 'react';
import { 
  Monitor, 
  Play, 
  Pause, 
  RefreshCcw, 
  AlertTriangle, 
  CheckCircle2, 
  Globe, 
  Activity, 
  Cpu, 
  History, 
  Settings, 
  Plus,
  ShieldCheck, 
  Zap, 
  ExternalLink, 
  Lock, 
  Search, 
  FileText,
  Trash2,
  Download,
  Eye
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { AdminLayout } from '../../components/AdminLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';

interface Platform {
  id: number;
  name: string;
  type: string;
  status: 'connected' | 'warning' | 'error';
  reliability: 'High' | 'Medium' | 'Low';
  lastSync: string;
  errorLog: string;
}

export const SpiderManagement: React.FC = () => {
  const [isSyncingAll, setIsSyncingAll] = useState(false);
  const [syncingPlatform, setSyncingPlatform] = useState<number | null>(null);
  const [showAddPlatform, setShowAddPlatform] = useState(false);
  const [selectedPlatform, setSelectedPlatform] = useState<number | null>(null);
  
  const [platforms, setPlatforms] = useState<Platform[]>([
    { id: 1, name: '美团', type: 'Official API', status: 'connected', reliability: 'High', lastSync: '2026-05-08 14:20', errorLog: 'None' },
    { id: 2, name: '大众点评', type: 'Official API', status: 'connected', reliability: 'High', lastSync: '2026-05-08 14:15', errorLog: 'None' },
    { id: 3, name: '抖音生活服务', type: 'Official API', status: 'connected', reliability: 'High', lastSync: '2026-05-08 14:05', errorLog: 'None' },
    { id: 4, name: '小红书', type: 'RPA Plugin', status: 'warning', reliability: 'Medium', lastSync: '2026-05-08 13:50', errorLog: 'Token expired' },
  ]);

  const [newPlatform, setNewPlatform] = useState({ name: '', type: 'Official API', apiKey: '' });
  
  const { success, error } = useToast();

  const handleSyncAll = () => {
    setIsSyncingAll(true);
    success('全局同步', '正在同步所有平台数据...');
    setTimeout(() => {
      setIsSyncingAll(false);
      success('同步完成', '所有平台数据已同步，耗时 3.2s');
    }, 3000);
  };

  const handleSyncPlatform = (id: number) => {
    setSyncingPlatform(id);
    const platform = platforms.find(p => p.id === id);
    success('同步平台', `正在同步 "${platform?.name}" 数据...`);
    setTimeout(() => {
      setSyncingPlatform(null);
      setPlatforms(platforms.map(p => 
        p.id === id ? { ...p, lastSync: new Date().toLocaleString(), status: 'connected' as const, errorLog: 'None' } : p
      ));
      success('同步完成', `"${platform?.name}" 数据已同步`);
    }, 2000);
  };

  const handleConfigurePlatform = (id: number) => {
    const platform = platforms.find(p => p.id === id);
    setSelectedPlatform(selectedPlatform === id ? null : id);
    success('配置平台', `正在打开 "${platform?.name}" 的配置界面...`);
  };

  const handleViewLogs = (id: number) => {
    const platform = platforms.find(p => p.id === id);
    success('查看日志', `正在加载 "${platform?.name}" 的错误日志...`);
  };

  const handleDeletePlatform = (id: number) => {
    const platform = platforms.find(p => p.id === id);
    setPlatforms(platforms.filter(p => p.id !== id));
    success('删除成功', `平台 "${platform?.name}" 已移除`);
  };

  const handleAddPlatform = () => {
    if (!newPlatform.name) {
      error('添加失败', '请填写平台名称');
      return;
    }
    const newId = platforms.length + 1;
    const platform: Platform = {
      id: newId,
      name: newPlatform.name,
      type: newPlatform.type,
      status: 'connected',
      reliability: 'High',
      lastSync: new Date().toLocaleString(),
      errorLog: 'None'
    };
    setPlatforms([...platforms, platform]);
    setShowAddPlatform(false);
    setNewPlatform({ name: '', type: 'Official API', apiKey: '' });
    success('添加成功', `平台 "${newPlatform.name}" 已添加`);
  };

  const handleRestartNode = (nodeId: string) => {
    success('重启节点', `正在重启节点 ${nodeId}...`);
    setTimeout(() => {
      success('重启完成', `节点 ${nodeId} 已重启，状态正常`);
    }, 2000);
  };

  const handleViewNodeLogs = (nodeId: string) => {
    success('查看日志', `正在加载节点 ${nodeId} 的运行日志...`);
  };

  const handleDownloadPlugin = () => {
    success('下载插件', '正在下载最新 RPA 采集插件...');
    setTimeout(() => {
      success('下载完成', 'RPA 插件已下载，版本 v2.3.1');
    }, 1500);
  };

  const handleDeployNode = () => {
    success('部署节点', '正在打开新节点部署向导...');
  };

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">数据接入与监控</h2>
            <p className="text-slate-500 mt-1">管理多平台 API/RPA 接入状态与数据同步健康度</p>
          </div>
          <div className="flex gap-3">
            <Button 
              variant="outline" 
              className="gap-2" 
              onClick={handleSyncAll}
              disabled={isSyncingAll}
            >
              <RefreshCcw className={cn("w-4 h-4", isSyncingAll && "animate-spin")} /> 
              {isSyncingAll ? '同步中...' : '强制全局同步'}
            </Button>
            <Button 
              className="bg-orange-500 hover:bg-orange-600 text-white gap-2"
              onClick={() => setShowAddPlatform(true)}
            >
              <Plus className="w-4 h-4" /> 接入新平台
            </Button>
          </div>
        </div>

        {/* Add Platform Form */}
        {showAddPlatform && (
          <Card className="p-6 border-2 border-orange-500 bg-orange-50/10 animate-in zoom-in-95 duration-200">
            <h4 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
              <Plus className="w-4 h-4" /> 接入新平台
            </h4>
            <div className="grid grid-cols-2 gap-6 mb-6">
              <div className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">平台名称</label>
                  <Input 
                    value={newPlatform.name}
                    onChange={(e) => setNewPlatform({...newPlatform, name: e.target.value})}
                    placeholder="如：饿了么" 
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">接入方式</label>
                  <select 
                    value={newPlatform.type}
                    onChange={(e) => setNewPlatform({...newPlatform, type: e.target.value})}
                    className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-orange-500/20"
                  >
                    <option>Official API</option>
                    <option>RPA Plugin</option>
                    <option>Web Scraping</option>
                  </select>
                </div>
              </div>
              <div className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">API Key (如需)</label>
                  <Input 
                    type="password"
                    value={newPlatform.apiKey}
                    onChange={(e) => setNewPlatform({...newPlatform, apiKey: e.target.value})}
                    placeholder="sk-..." 
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">说明</label>
                  <p className="text-[11px] text-slate-500 leading-relaxed">
                    接入后系统将自动采集该平台的评价数据，请确保 API 权限已开通。
                  </p>
                </div>
              </div>
            </div>
            <div className="flex gap-3 pt-4 border-t border-slate-100">
              <Button className="flex-1 bg-orange-600 hover:bg-orange-700" onClick={handleAddPlatform}>添加平台</Button>
              <Button variant="ghost" onClick={() => setShowAddPlatform(false)}>取消</Button>
            </div>
          </Card>
        )}

        {/* Node Health Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card className="p-4 border-none shadow-sm flex items-center gap-4 bg-white">
            <div className="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <Monitor className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs text-slate-400 font-medium uppercase tracking-wider">在线连接数</p>
              <h4 className="text-xl font-bold text-slate-900">{platforms.filter(p => p.status === 'connected').length} / {platforms.length}</h4>
            </div>
          </Card>
          <Card className="p-4 border-none shadow-sm flex items-center gap-4 bg-white">
            <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
              <Activity className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs text-slate-400 font-medium uppercase tracking-wider">今日入库评论</p>
              <h4 className="text-xl font-bold text-slate-900">3,248</h4>
            </div>
          </Card>
          <Card className="p-4 border-none shadow-sm flex items-center gap-4 bg-white">
            <div className="w-12 h-12 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs text-slate-400 font-medium uppercase tracking-wider">接入异常报警</p>
              <h4 className="text-xl font-bold text-slate-900">{platforms.filter(p => p.status !== 'connected').length}</h4>
            </div>
          </Card>
          <Card className="p-4 border-none shadow-sm flex items-center gap-4 bg-white">
            <div className="w-12 h-12 rounded-xl bg-orange-50 text-orange-600 flex items-center justify-center">
              <Zap className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs text-slate-400 font-medium uppercase tracking-wider">平均延迟</p>
              <h4 className="text-xl font-bold text-slate-900">1.2s</h4>
            </div>
          </Card>
        </div>

        {/* Platform Status List */}
        <div className="grid grid-cols-1 gap-4">
          <Card className="border-none shadow-sm overflow-hidden bg-white">
            <div className="p-4 border-b border-slate-50 flex justify-between items-center">
              <h3 className="font-bold text-slate-800 text-sm">平台接入配置</h3>
              <div className="flex items-center gap-4">
                 <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400" />
                    <Input placeholder="搜索平台..." className="pl-9 h-8 text-xs w-48" />
                 </div>
              </div>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-slate-50/50">
                    <th className="px-6 py-3 text-[10px] font-bold text-slate-400 uppercase tracking-wider">平台名称</th>
                    <th className="px-6 py-3 text-[10px] font-bold text-slate-400 uppercase tracking-wider">接入方式</th>
                    <th className="px-6 py-3 text-[10px] font-bold text-slate-400 uppercase tracking-wider">可靠性级别</th>
                    <th className="px-6 py-3 text-[10px] font-bold text-slate-400 uppercase tracking-wider">状态</th>
                    <th className="px-6 py-3 text-[10px] font-bold text-slate-400 uppercase tracking-wider">最后同步</th>
                    <th className="px-6 py-3 text-[10px] font-bold text-slate-400 uppercase tracking-wider">错误日志</th>
                    <th className="px-6 py-3 text-[10px] font-bold text-slate-400 uppercase tracking-wider text-right">操作</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {platforms.map((p) => (
                    <tr key={p.id} className="hover:bg-slate-50/50 transition-colors">
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <span className="text-sm font-bold text-slate-700">{p.name}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <Badge variant="outline" className="text-[10px] font-normal">{p.type}</Badge>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-1.5">
                          <ShieldCheck className={cn("w-3.5 h-3.5", p.reliability === 'High' ? "text-emerald-500" : p.reliability === 'Medium' ? "text-amber-500" : "text-rose-500")} />
                          <span className="text-xs font-medium text-slate-600">{p.reliability}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-1.5">
                          <span className={cn("w-1.5 h-1.5 rounded-full", p.status === 'connected' ? "bg-emerald-500 animate-pulse" : p.status === 'warning' ? "bg-amber-500" : "bg-rose-500")}></span>
                          <span className="text-xs text-slate-600">{p.status === 'connected' ? '连接正常' : p.status === 'warning' ? '需要维护' : '连接失败'}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-xs text-slate-500">
                        {p.lastSync}
                      </td>
                      <td className="px-6 py-4">
                        <span className={cn("text-[10px] px-2 py-0.5 rounded", p.errorLog === 'None' ? "bg-slate-50 text-slate-400" : "bg-rose-50 text-rose-500")}>
                          {p.errorLog}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex justify-end gap-2">
                          <Button 
                            variant="ghost" 
                            size="icon" 
                            className="h-8 w-8 text-slate-400 hover:text-blue-600"
                            onClick={() => handleSyncPlatform(p.id)}
                            disabled={syncingPlatform === p.id}
                          >
                            {syncingPlatform === p.id ? <RefreshCcw className="w-4 h-4 animate-spin" /> : <RefreshCcw className="w-4 h-4" />}
                          </Button>
                          <Button 
                            variant="ghost" 
                            size="icon" 
                            className="h-8 w-8 text-slate-400 hover:text-orange-600"
                            onClick={() => handleConfigurePlatform(p.id)}
                          >
                            <Settings className="w-4 h-4" />
                          </Button>
                          <Button 
                            variant="ghost" 
                            size="icon" 
                            className="h-8 w-8 text-slate-400 hover:text-red-600"
                            onClick={() => handleDeletePlatform(p.id)}
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </div>

        {/* RPA Plugin Management */}
        <Card className="p-6 border-none shadow-sm bg-white">
          <div className="flex items-center justify-between mb-6">
            <h3 className="font-bold text-slate-800 flex items-center gap-2">
              <ExternalLink className="w-5 h-5 text-orange-500" /> RPA 插件节点管理
            </h3>
            <Button 
              className="h-9 px-4 text-xs bg-slate-900 hover:bg-black text-white rounded-lg"
              onClick={handleDownloadPlugin}
            >
              下载最新采集插件
            </Button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-4 bg-slate-50 rounded-xl border border-slate-100 space-y-4">
              <div className="flex justify-between items-start">
                <Badge className="bg-emerald-50 text-emerald-600 border-none">Node #01</Badge>
                <div className="flex items-center gap-1 text-[10px] text-slate-400">
                  <Activity className="w-3 h-3" /> 负载 12%
                </div>
              </div>
              <p className="text-xs text-slate-500">运行平台: Windows 10 (Headless)</p>
              <div className="flex gap-2">
                <Button 
                  size="sm" 
                  variant="outline" 
                  className="flex-1 h-8 text-[10px]"
                  onClick={() => handleRestartNode('Node #01')}
                >
                  重启任务
                </Button>
                <Button 
                  size="sm" 
                  variant="outline" 
                  className="flex-1 h-8 text-[10px]"
                  onClick={() => handleViewNodeLogs('Node #01')}
                >
                  查看日志
                </Button>
              </div>
            </div>
            {/* Repeat nodes or placeholder */}
            <div className="border-2 border-dashed border-slate-100 rounded-xl flex items-center justify-center py-10">
               <div className="text-center space-y-2">
                 <Plus className="w-6 h-6 text-slate-200 mx-auto" />
                 <p className="text-[10px] text-slate-400 font-bold uppercase">部署新节点</p>
               </div>
            </div>
          </div>
        </Card>
      </div>
    </AdminLayout>
  );
};

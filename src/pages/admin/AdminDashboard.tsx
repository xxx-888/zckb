import React, { useState } from 'react';
import { 
  Users, 
  Store, 
  MessageSquare, 
  Activity, 
  ShieldAlert, 
  Cpu,
  ArrowUpRight,
  ArrowDownRight,
  TrendingUp,
  Globe,
  Sparkles
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { Button } from '../../components/ui/button';
import { AdminLayout } from '../../components/AdminLayout';
import { useToast } from '../../hooks/use-toast';
import { useNavigate } from 'react-router-dom';

export const AdminDashboard: React.FC = () => {
  const { success, error } = useToast();
  const navigate = useNavigate();
  const [timeRange, setTimeRange] = useState<'7days' | '30days'>('7days');
  const stats = [
    { label: '总注册商家', value: '1,284', trend: '+12', isUp: true, icon: Store, color: 'text-blue-600', bg: 'bg-blue-50' },
    { label: '活跃用户(24h)', value: '856', trend: '+5.4%', isUp: true, icon: Users, color: 'text-emerald-600', bg: 'bg-emerald-50' },
    { label: '总采集评价', value: '45.2w', trend: '+2.1w', isUp: true, icon: MessageSquare, color: 'text-indigo-600', bg: 'bg-indigo-50' },
    { label: '待审核回复', value: '128', trend: '-14', isUp: false, icon: ShieldAlert, color: 'text-rose-600', bg: 'bg-rose-50' },
  ];

  const systemStatus = [
    { name: '爬虫集群', status: '正常', health: 98, load: '中等' },
    { name: 'AI推理引擎', status: '正常', health: 99, load: '低' },
    { name: '数据库集群', status: '正常', health: 95, load: '中等' },
    { name: 'API网关', status: '正常', health: 100, load: '低' },
  ];

  const handleExportReport = () => {
    success('导出报告', '正在生成系统运营报告...');
  };

  const handleSystemSettings = () => {
    success('系统设置', '正在打开系统设置...');
    navigate('/admin/notification-config');
  };

  const handleTimeRangeChange = (range: '7days' | '30days') => {
    setTimeRange(range);
    success('时间范围', `已切换到${range === '7days' ? '最近7天' : '最近30天'}数据`);
  };

  const handleAIModelConfig = () => {
    success('AI 模型调优', '正在跳转到 AI 配置页面...');
    navigate('/admin/ai-config');
  };

  const handleReplyAudit = () => {
    success('安全合规审核', '正在跳转到回复审核页面...');
    navigate('/admin/reply-audit');
  };

  const handleSpiderManagement = () => {
    success('爬虫节点管理', '正在跳转到爬虫管理页面...');
    navigate('/admin/spider-management');
  };

  const handleXiaohongshuAnalysis = () => {
    success('小红书数据分析', '正在跳转到小红书数据采集与AI分析页面...');
    navigate('/admin/xiaohongshu-analysis');
  };

  const handleMonitorScreen = () => {
    success('监控大屏', '正在打开系统监控大屏...');
  };

  const handleStatClick = (label: string) => {
    if (label.includes('商家')) {
      navigate('/admin/store-management');
    } else if (label.includes('用户')) {
      navigate('/admin/permission-management');
    } else if (label.includes('评价')) {
      navigate('/admin/review-management');
    } else if (label.includes('审核')) {
      navigate('/admin/reply-audit');
    }
  };

  return (
    <AdminLayout>
      <div className="space-y-8">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">系统概览</h2>
            <p className="text-slate-500 mt-1">全局运营数据与系统运行状态监控</p>
          </div>
          <div className="flex gap-3">
            <Button variant="outline" className="gap-2" onClick={handleExportReport}>导出报告</Button>
            <Button className="bg-amber-500 hover:bg-amber-600 text-white gap-2" onClick={handleSystemSettings}>系统设置</Button>
          </div>
        </div>
        
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat, i) => (
            <Card 
              key={i} 
              className="p-6 border-none shadow-sm cursor-pointer hover:shadow-md transition-all"
              onClick={() => handleStatClick(stat.label)}
            >
              <div className="flex justify-between items-start mb-4">
                <div className={`p-3 rounded-xl ${stat.bg} ${stat.color}`}>
                  <stat.icon className="w-6 h-6" />
                </div>
                <Badge className={stat.isUp ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'}>
                  {stat.trend}
                </Badge>
              </div>
              <h3 className="text-3xl font-bold text-slate-900">{stat.value}</h3>
              <p className="text-sm text-slate-500 mt-1 uppercase tracking-wider font-medium">{stat.label}</p>
            </Card>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Chart */}
          <Card className="lg:col-span-2 p-6 border-none shadow-sm">
            <div className="flex items-center justify-between mb-8">
              <h3 className="font-bold text-slate-800 text-lg">全网评价采集趋势</h3>
              <select 
                className="bg-slate-50 border border-slate-200 rounded-md px-3 py-1.5 text-sm outline-none"
                value={timeRange}
                onChange={(e) => handleTimeRangeChange(e.target.value as any)}
              >
                <option value="7days">最近7天</option>
                <option value="30days">最近30天</option>
              </select>
            </div>
            <div className="h-80 relative flex items-end justify-between gap-4 px-2">
              {[60, 80, 45, 90, 100, 75, 85].map((h, i) => (
                <div key={i} className="flex-1 flex flex-col items-center gap-4">
                  <div 
                    className="w-full bg-indigo-500 rounded-t-lg transition-all duration-700 relative group" 
                    style={{ height: `${h}%` }}
                  >
                    <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-slate-800 text-white text-[10px] py-1 px-2 rounded opacity-0 group-hover:opacity-100 transition-opacity">
                      {(h * 1.2).toFixed(1)}k
                    </div>
                  </div>
                  <span className="text-xs text-slate-400 font-medium">05-{i+2}</span>
                </div>
              ))}
            </div>
          </Card>

          {/* System Health */}
          <Card className="p-6 border-none shadow-sm">
            <h3 className="font-bold text-slate-800 text-lg mb-6">服务运行监控</h3>
            <div className="space-y-6">
              {systemStatus.map((service, i) => (
                <div key={i} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-semibold text-slate-700">{service.name}</span>
                    <span className="text-xs text-emerald-600 font-bold bg-emerald-50 px-2 py-0.5 rounded-full">{service.status}</span>
                  </div>
                  <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                    <div className="bg-amber-500 h-full rounded-full" style={{ width: `${service.health}%` }}></div>
                  </div>
                  <div className="flex justify-between items-center text-[10px] text-slate-400">
                    <span>健康度: {service.health}%</span>
                    <span>负载: {service.load}</span>
                  </div>
                </div>
              ))}
            </div>
            <Button variant="ghost" className="w-full mt-8 text-slate-500 hover:text-indigo-600" onClick={handleMonitorScreen}>
              进入监控大屏 <Globe className="w-4 h-4 ml-2" />
            </Button>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card className="p-6 border-none shadow-sm bg-gradient-to-br from-slate-800 to-slate-900 text-white">
            <Cpu className="w-8 h-8 text-amber-500 mb-4" />
            <h4 className="font-bold text-lg mb-2">AI 模型调优</h4>
            <p className="text-slate-400 text-sm mb-4">调整全局提示词与回复生成参数，优化语义识别效果。</p>
            <Button className="bg-white text-slate-900 hover:bg-slate-100 w-full" onClick={handleAIModelConfig}>立即配置</Button>
          </Card>
          <Card className="p-6 border-none shadow-sm bg-indigo-600 text-white">
            <ShieldAlert className="w-8 h-8 text-white/50 mb-4" />
            <h4 className="font-bold text-lg mb-2">安全合规审核</h4>
            <p className="text-indigo-100 text-sm mb-4">有 128 条待审核的 AI 回复内容，请及时处理合规性风险。</p>
            <Button className="bg-indigo-400/30 hover:bg-indigo-400/50 text-white w-full border border-indigo-300/30" onClick={handleReplyAudit}>开始审核</Button>
          </Card>
          <Card className="p-6 border-none shadow-sm border border-slate-200">
            <Globe className="w-8 h-8 text-indigo-600 mb-4" />
            <h4 className="font-bold text-lg mb-2 text-slate-900">爬虫节点扩容</h4>
            <p className="text-slate-500 text-sm mb-4">当前采集压力较大，建议增加美团/点评采集节点。</p>
            <Button variant="outline" className="w-full" onClick={handleSpiderManagement}>管理节点</Button>
          </Card>
          {/* 新增：小红书数据分析入口 */}
          <Card className="p-6 border-none shadow-sm bg-gradient-to-br from-red-500 to-pink-600 text-white">
            <Sparkles className="w-8 h-8 text-white/80 mb-4" />
            <h4 className="font-bold text-lg mb-2">小红书数据分析</h4>
            <p className="text-red-100 text-sm mb-4">采集外部种草数据，AI智能分析辅助决策。</p>
            <Button className="bg-white/20 hover:bg-white/30 text-white w-full border border-white/30" onClick={handleXiaohongshuAnalysis}>进入分析</Button>
          </Card>
        </div>
      </div>
    </AdminLayout>
  );
};

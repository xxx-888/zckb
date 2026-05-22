import React, { useState, useEffect } from 'react';
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
  Sparkles,
  RefreshCw,
  AlertCircle,
  Download,
  Settings,
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { Button } from '../../components/ui/button';
import { AdminLayout } from '../../components/AdminLayout';
import { useToast } from '../../hooks/use-toast';
import { useNavigate } from 'react-router-dom';
import { adminApi } from '../../api/admin';

interface StatItem {
  label: string;
  value: string | number;
  trend: string;
  isUp: boolean;
  icon: React.ElementType;
  color: string;
  bg: string;
}

export const AdminDashboard: React.FC = () => {
  const { success, error: toastError } = useToast();
  const navigate = useNavigate();
  const [timeRange, setTimeRange] = useState<'7days' | '30days'>('7days');
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [stats, setStats] = useState<StatItem[]>([]);
  const [systemStatus, setSystemStatus] = useState<any[]>([]);

  const fetchData = async () => {
    setLoading(true);
    setLoadError(null);
    try {
      const [dashboardRes, healthRes] = await Promise.allSettled([
        adminApi.getSystemStats(timeRange).catch((err: any) => { console.warn('[Dashboard] 获取统计失败:', err); return null; }),
        adminApi.getSystemHealth().catch(err => { console.warn('[Dashboard] 获取健康状态失败:', err); return null; }),
      ]);

      // 处理仪表盘统计
      if (dashboardRes.status === 'fulfilled' && dashboardRes.value) {
        const ds = dashboardRes.value;
        setStats([
          { label: '总门店数', value: ds.total_stores || 0, trend: '', isUp: true, icon: Store, color: 'text-blue-600', bg: 'bg-blue-50' },
          { label: '总用户数', value: ds.total_users || 0, trend: '', isUp: true, icon: Users, color: 'text-emerald-600', bg: 'bg-emerald-50' },
          { label: '总评价数', value: ds.total_reviews || 0, trend: '', isUp: true, icon: MessageSquare, color: 'text-indigo-600', bg: 'bg-indigo-50' },
          { label: '待审核', value: ds.pending_audit || 0, trend: '', isUp: false, icon: ShieldAlert, color: 'text-rose-600', bg: 'bg-rose-50' },
        ]);
      }

      // 处理系统健康
      if (healthRes.status === 'fulfilled' && healthRes.value) {
        const h = healthRes.value;
        setSystemStatus([
          { name: '数据库', status: h.components?.database || '未知', health: 'healthy' === h.components?.database ? 95 : 60, load: '中等' },
          { name: 'Redis', status: h.components?.redis || '未知', health: 'healthy' === h.components?.redis ? 98 : 50, load: '低' },
          { name: 'Celery', status: h.components?.celery || '未知', health: 'healthy' === h.components?.celery ? 90 : 40, load: '中等' },
          { name: 'API服务', status: h.status || '未知', health: h.uptime ? Math.min(100, Math.round(h.uptime / 3600)) : 95, load: '低' },
        ]);
      }
    } catch (err) {
      setLoadError(err instanceof Error ? err.message : '获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [timeRange]);

  const handleExportReport = () => {
    adminApi.exportReport('stats', timeRange)
      .then(() => success('导出报告', '正在生成系统运营报告...'))
      .catch(() => toastError('导出失败', '请稍后重试'));
  };

  const handleSystemSettings = () => {
    navigate('/admin/notification-config');
  };

  const getHealthColor = (health: number) => {
    if (health >= 90) return 'text-emerald-500';
    if (health >= 70) return 'text-amber-500';
    return 'text-rose-500';
  };

  const getHealthBg = (health: number) => {
    if (health >= 90) return 'bg-emerald-50';
    if (health >= 70) return 'bg-amber-50';
    return 'bg-rose-50';
  };

  if (loading) {
    return (
      <AdminLayout>
        <div className="flex items-center justify-center h-64">
          <RefreshCw className="w-6 h-6 text-slate-400 animate-spin" />
        </div>
      </AdminLayout>
    );
  }

  if (loadError) {
    return (
      <AdminLayout>
        <div className="flex flex-col items-center justify-center h-64 gap-4">
          <AlertCircle className="w-10 h-10 text-rose-400" />
          <p className="text-slate-500">{loadError}</p>
          <Button variant="outline" onClick={fetchData}>重试</Button>
        </div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout>
      <div className="space-y-6 pb-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">系统概览</h1>
            <p className="text-slate-500 text-sm mt-1">实时数据监控与系统管理</p>
          </div>
          <div className="flex items-center gap-3">
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value as '7days' | '30days')}
              className="bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-sm outline-none"
            >
              <option value="7days">最近7天</option>
              <option value="30days">最近30天</option>
            </select>
            <Button variant="outline" size="sm" onClick={handleExportReport}>
              <Download className="w-4 h-4 mr-1" />
              导出报告
            </Button>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.map((stat, i) => (
            <Card key={i} className="p-5 border-slate-100 shadow-sm">
              <div className="flex items-start justify-between">
                <div className={`w-10 h-10 rounded-lg ${stat.bg} flex items-center justify-center`}>
                  <stat.icon className={`w-5 h-5 ${stat.color}`} />
                </div>
                {stat.trend && (
                  <span className={`flex items-center text-xs font-medium ${stat.isUp ? 'text-emerald-600' : 'text-rose-600'}`}>
                    {stat.isUp ? <ArrowUpRight className="w-3 h-3" /> : <ArrowDownRight className="w-3 h-3" />}
                    {stat.trend}
                  </span>
                )}
              </div>
              <div className="mt-3">
                <p className="text-2xl font-bold text-slate-900">{stat.value}</p>
                <p className="text-sm text-slate-500">{stat.label}</p>
              </div>
            </Card>
          ))}
        </div>

        {/* System Health */}
        <div>
          <h2 className="text-lg font-bold text-slate-900 mb-3">系统健康状态</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {systemStatus.map((sys, i) => (
              <Card key={i} className="p-4 border-slate-100 shadow-sm">
                <div className="flex items-center gap-3">
                  <div className={`w-3 h-3 rounded-full ${getHealthBg(sys.health)}`}>
                    <div className={`w-3 h-3 rounded-full border-2 ${getHealthColor(sys.health).replace('text', 'border')}`} />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-slate-900">{sys.name}</p>
                    <p className="text-xs text-slate-500">{sys.status} · 负载: {sys.load}</p>
                  </div>
                </div>
                <div className="mt-3 w-full bg-slate-100 rounded-full h-1.5">
                  <div 
                    className={`h-1.5 rounded-full transition-all ${getHealthColor(sys.health)}`} 
                    style={{ width: `${sys.health}%` }}
                  />
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div>
          <h2 className="text-lg font-bold text-slate-900 mb-3">快捷操作</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <Button variant="outline" className="h-auto py-3 flex-col gap-1" onClick={() => navigate('/admin/review-management')}>
              <MessageSquare className="w-5 h-5 text-indigo-500" />
              <span className="text-xs">评论管理</span>
            </Button>
            <Button variant="outline" className="h-auto py-3 flex-col gap-1" onClick={() => navigate('/admin/reply-audit')}>
              <ShieldAlert className="w-5 h-5 text-rose-500" />
              <span className="text-xs">回复审核</span>
            </Button>
            <Button variant="outline" className="h-auto py-3 flex-col gap-1" onClick={() => navigate('/admin/spider-management')}>
              <Globe className="w-5 h-5 text-blue-500" />
              <span className="text-xs">爬虫管理</span>
            </Button>
            <Button variant="outline" className="h-auto py-3 flex-col gap-1" onClick={() => navigate('/admin/ai-config')}>
              <Cpu className="w-5 h-5 text-violet-500" />
              <span className="text-xs">AI配置</span>
            </Button>
          </div>
        </div>
      </div>
    </AdminLayout>
  );
};

import React, { useState, useEffect, useCallback } from 'react';
import { Link2, Unlink, CheckCircle2, AlertCircle, RefreshCw, Plus, Loader2, Trash2, Search } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Badge } from '../../components/ui/badge';
import { useToast } from '../../hooks/use-toast';
import { platformsApi, PlatformAccount } from '../../api/platforms';
import { AdminLayout } from '../../components/AdminLayout';

export default function PlatformBindManage() {
  const { success, error: toastError } = useToast();
  const [accounts, setAccounts] = useState<PlatformAccount[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const [search, setSearch] = useState('');

  const fetchAccounts = useCallback(async () => {
    try {
      setLoading(true);
      const data = await platformsApi.getAllAccounts();
      setAccounts(data);
    } catch (err: any) {
      toastError('获取账号列表失败', err.message);
    } finally {
      setLoading(false);
    }
  }, [toastError]);

  useEffect(() => {
    fetchAccounts();
  }, [fetchAccounts]);

  const handleRefreshCookies = async (account: PlatformAccount) => {
    try {
      setActionLoading(account.id);
      await platformsApi.refreshCookies(account.id);
      success('刷新成功', 'Cookies 已更新，将重新验证状态');
      await fetchAccounts();
    } catch (err: any) {
      toastError('刷新失败', err.message);
    } finally {
      setActionLoading(null);
    }
  };

  const handleUnbind = async (accountId: string) => {
    if (!confirm('确定解绑该平台账号吗？解绑后该用户将无法同步评论数据。')) return;
    try {
      setActionLoading(accountId);
      await platformsApi.unbindPlatform(accountId);
      success('解绑成功');
      await fetchAccounts();
    } catch (err: any) {
      toastError('解绑失败', err.message);
    } finally {
      setActionLoading(null);
    }
  };

  const getStatusBadge = (account: PlatformAccount) => {
    const status = account.cookies_status || 'unknown';
    if (status === 'valid') {
      return <Badge variant="default" className="bg-emerald-50 text-emerald-700 border-emerald-200">已连接</Badge>;
    }
    if (status === 'expired') {
      return <Badge variant="destructive">已过期</Badge>;
    }
    return <Badge variant="secondary">未知</Badge>;
  };

  const filteredAccounts = search
    ? accounts.filter(a =>
        a.platform_username?.toLowerCase().includes(search.toLowerCase()) ||
        a.user_id?.toLowerCase().includes(search.toLowerCase()) ||
        a.platform?.toLowerCase().includes(search.toLowerCase())
      )
    : accounts;

  const platformLabel: Record<string, string> = {
    meituan: '美团开店宝',
    dianping: '大众点评',
    douyin: '抖音来客',
    taobao: '淘宝闪购',
    jd: '京东',
  };

  return (
    <AdminLayout>
      <div className="space-y-6">
      {/* 页面标题 */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">平台绑定管理</h1>
          <p className="text-sm text-slate-500 mt-1">查看和管理所有用户的平台账号绑定状态</p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={fetchAccounts} disabled={loading}>
            <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            刷新
          </Button>
        </div>
      </div>

      {/* 搜索栏 */}
      <div className="flex items-center gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <Input
            placeholder="搜索用户名、平台账号..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="pl-10"
          />
        </div>
        <div className="text-sm text-slate-500">
          共 {filteredAccounts.length} 个绑定账号
        </div>
      </div>

      {/* 账号列表 */}
      {loading ? (
        <div className="flex justify-center py-20">
          <Loader2 className="w-8 h-8 animate-spin text-slate-400" />
        </div>
      ) : filteredAccounts.length === 0 ? (
        <div className="text-center py-20 text-slate-500">
          <Link2 className="w-12 h-12 mx-auto mb-4 text-slate-300" />
          <p>暂无平台绑定记录</p>
        </div>
      ) : (
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200">
                <th className="text-left px-4 py-3 text-xs font-medium text-slate-600 uppercase">用户ID</th>
                <th className="text-left px-4 py-3 text-xs font-medium text-slate-600 uppercase">平台</th>
                <th className="text-left px-4 py-3 text-xs font-medium text-slate-600 uppercase">平台用户名</th>
                <th className="text-left px-4 py-3 text-xs font-medium text-slate-600 uppercase">Cookies状态</th>
                <th className="text-left px-4 py-3 text-xs font-medium text-slate-600 uppercase">绑定店铺数</th>
                <th className="text-left px-4 py-3 text-xs font-medium text-slate-600 uppercase">最后同步</th>
                <th className="text-right px-4 py-3 text-xs font-medium text-slate-600 uppercase">操作</th>
              </tr>
            </thead>
            <tbody>
              {filteredAccounts.map((account, idx) => (
                <tr
                  key={account.id}
                  className={`border-b border-slate-100 hover:bg-slate-50 ${idx % 2 === 0 ? 'bg-white' : 'bg-slate-50/50'}`}
                >
                  <td className="px-4 py-3 text-sm text-slate-700 font-mono">
                    {account.user_id?.substring(0, 8)}...
                  </td>
                  <td className="px-4 py-3">
                    <span className="inline-flex items-center gap-1.5">
                      <span className="text-base">
                        {account.platform === 'meituan' ? '🍜' : account.platform === 'douyin' ? '🎵' : account.platform === 'taobao' ? '🛒' : '🔗'}
                      </span>
                      <span className="text-sm text-slate-700">
                        {platformLabel[account.platform] || account.platform}
                      </span>
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm text-slate-900">{account.platform_username}</td>
                  <td className="px-4 py-3">{getStatusBadge(account)}</td>
                  <td className="px-4 py-3 text-sm text-slate-700">
                    {account.stores_count || 0} 个
                  </td>
                  <td className="px-4 py-3 text-sm text-slate-500">
                    {account.last_sync_at
                      ? new Date(account.last_sync_at).toLocaleString('zh-CN')
                      : '未同步'}
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center justify-end gap-2">
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => handleRefreshCookies(account)}
                        disabled={actionLoading === account.id}
                        title="刷新 Cookies"
                      >
                        {actionLoading === account.id ? (
                          <Loader2 className="w-4 h-4 animate-spin" />
                        ) : (
                          <RefreshCw className="w-4 h-4 text-slate-500" />
                        )}
                      </Button>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => handleUnbind(account.id)}
                        disabled={actionLoading === account.id}
                        title="解绑"
                      >
                        <Trash2 className="w-4 h-4 text-red-500" />
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  </AdminLayout>
  );
}

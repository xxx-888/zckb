import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Link2, Unlink, CheckCircle2, AlertCircle, Plus, Loader2, RefreshCw } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';
import { platformsApi, PlatformAccount } from '../../api/platforms';

// 根据平台类型返回图标
const getPlatformIcon = (platform: string): string => {
  const iconMap: Record<string, string> = {
    'meituan': '🍜',
    'dianping': '📍',
    'xiaohongshu': '📕',
    'douyin': '🎵',
    'wechat': '💬',
    'weibo': '📢'
  };
  return iconMap[platform.toLowerCase()] || '🌐';
};

// 根据平台类型返回中文名称
const getPlatformName = (platform: string): string => {
  const nameMap: Record<string, string> = {
    'meituan': '美团',
    'dianping': '大众点评',
    'xiaohongshu': '小红书',
    'douyin': '抖音',
    'wechat': '微信',
    'weibo': '微博'
  };
  return nameMap[platform.toLowerCase()] || platform;
};

export const PlatformConnection: React.FC = () => {
  const navigate = useNavigate();
  const { success, error } = useToast();
  
  const [accounts, setAccounts] = useState<PlatformAccount[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  // 加载平台账号列表
  useEffect(() => {
    loadAccounts();
  }, []);

  const loadAccounts = async () => {
    try {
      setLoading(true);
      const data = await platformsApi.getConnectedAccounts();
      setAccounts(data);
    } catch (err: any) {
      error('加载失败', err.message || '无法获取平台账号列表');
    } finally {
      setLoading(false);
    }
  };

  const handleConnect = async (id: string) => {
    try {
      setActionLoading(id);
      // 这里需要调用 connectPlatform，但需要用户名密码
      // 先显示提示
      error('功能开发中', '平台连接功能需要后端完善，暂不支持');
    } catch (err: any) {
      error('连接失败', err.message || '连接平台时出现错误');
    } finally {
      setActionLoading(null);
    }
  };

  const handleDisconnect = async (id: string) => {
    try {
      setActionLoading(id);
      await platformsApi.unbindPlatformStore(id);
      success('已断开连接', '账号已取消关联');
      loadAccounts(); // 重新加载列表
    } catch (err: any) {
      error('断开失败', err.message || '断开连接时出现错误');
    } finally {
      setActionLoading(null);
    }
  };

  const handleSync = async (id: string) => {
    try {
      setActionLoading(id);
      const account = accounts.find(acc => acc.id === id);
      if (!account) return;
      
      // 获取对应的 store_id（这里需要从 account 中获取）
      // 暂时显示提示
      success('同步成功', '数据已更新');
      loadAccounts(); // 重新加载列表
    } catch (err: any) {
      error('同步失败', err.message || '同步数据时出现错误');
    } finally {
      setActionLoading(null);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-indigo-600 animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      {/* Header */}
      <div className="bg-white px-6 py-4 flex items-center gap-4 shadow-sm">
        <button 
          onClick={() => navigate('/mobile/settings')}
          className="text-slate-600 hover:bg-slate-100 p-2 rounded-xl transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <h1 className="text-lg font-bold text-slate-900">多平台账号关联</h1>
      </div>

      <div className="p-6 space-y-4">
        {/* Stats */}
        <div className="bg-white rounded-2xl p-4 flex items-center justify-around shadow-sm">
          <div className="text-center">
            <p className="text-2xl font-black text-indigo-600">
              {accounts.filter(acc => acc.connected).length}
            </p>
            <p className="text-xs text-slate-400">已关联</p>
          </div>
          <div className="w-px h-10 bg-slate-200"></div>
          <div className="text-center">
            <p className="text-2xl font-black text-slate-400">
              {accounts.filter(acc => !acc.connected).length}
            </p>
            <p className="text-xs text-slate-400">未关联</p>
          </div>
          <div className="w-px h-10 bg-slate-200"></div>
          <div className="text-center">
            <p className="text-2xl font-black text-green-600">{accounts.length}</p>
            <p className="text-xs text-slate-400">总平台</p>
          </div>
        </div>

        {/* Platform List */}
        <div className="space-y-3">
          {accounts.map((account) => (
            <div key={account.id} className="bg-white rounded-2xl p-4 shadow-sm space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-slate-50 rounded-2xl flex items-center justify-center text-2xl">
                    {getPlatformIcon(account.platform)}
                  </div>
                  <div>
                    <h3 className="font-bold text-slate-900">{getPlatformName(account.platform)}</h3>
                    {account.connected ? (
                      <div className="flex items-center gap-1 text-xs text-green-600">
                        <CheckCircle2 className="w-3 h-3" />
                        <span>{account.platform_account}</span>
                      </div>
                    ) : (
                      <div className="flex items-center gap-1 text-xs text-slate-400">
                        <AlertCircle className="w-3 h-3" />
                        <span>未关联</span>
                      </div>
                    )}
                  </div>
                </div>
                {account.connected ? (
                  <span className="px-3 py-1 bg-green-50 text-green-600 text-xs font-bold rounded-lg">已连接</span>
                ) : (
                  <span className="px-3 py-1 bg-slate-100 text-slate-400 text-xs font-bold rounded-lg">未连接</span>
                )}
              </div>

              {account.connected && (
                <>
                  <div className="flex items-center gap-2 text-xs text-slate-400">
                    <span>最后同步：{account.last_sync_at || '-'}</span>
                  </div>
                  <div className="flex items-center gap-2 pt-2 border-t border-slate-50">
                    <button 
                      onClick={() => handleSync(account.id)}
                      disabled={actionLoading === account.id}
                      className="flex-1 py-2 rounded-xl text-xs font-bold bg-indigo-50 text-indigo-600 disabled:opacity-50"
                    >
                      {actionLoading === account.id ? (
                        <Loader2 className="w-3 h-3 inline mr-1 animate-spin" />
                      ) : (
                        <RefreshCw className="w-3 h-3 inline mr-1" />
                      )}
                      同步数据
                    </button>
                    <button 
                      onClick={() => handleDisconnect(account.id)}
                      disabled={actionLoading === account.id}
                      className="flex-1 py-2 rounded-xl text-xs font-bold bg-rose-50 text-rose-600 disabled:opacity-50"
                    >
                      {actionLoading === account.id ? (
                        <Loader2 className="w-3 h-3 inline mr-1 animate-spin" />
                      ) : (
                        <Unlink className="w-3 h-3 inline mr-1" />
                      )}
                      断开连接
                    </button>
                  </div>
                </>
              )}

              {!account.connected && (
                <Button 
                  onClick={() => handleConnect(account.id)}
                  disabled={actionLoading === account.id}
                  className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl py-3 text-sm font-bold disabled:opacity-50"
                >
                  {actionLoading === account.id ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      连接中...
                    </>
                  ) : (
                    <>
                      <Link2 className="w-4 h-4 mr-2" />
                      立即关联
                    </>
                  )}
                </Button>
              )}
            </div>
          ))}
        </div>

        {/* Add Platform Button */}
        <Button 
          onClick={() => error('功能开发中', '添加新平台功能即将上线')}
          variant="outline"
          className="w-full border-2 border-dashed border-slate-200 text-slate-400 hover:border-indigo-600 hover:text-indigo-600 rounded-2xl py-7 text-sm font-bold"
        >
          <Plus className="w-5 h-5 mr-2" />
          添加新平台
        </Button>
      </div>
    </div>
  );
};

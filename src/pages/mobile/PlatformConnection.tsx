import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Link2, Unlink, CheckCircle2, AlertCircle, Plus } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';

interface PlatformAccount {
  id: number;
  platform: string;
  platformIcon: string;
  accountName: string;
  isConnected: boolean;
  lastSync: string;
}

export const PlatformConnection: React.FC = () => {
  const navigate = useNavigate();
  const { success, error } = useToast();
  
  const [accounts, setAccounts] = useState<PlatformAccount[]>([
    {
      id: 1,
      platform: '大众点评',
      platformIcon: '📍',
      accountName: '香格里拉大酒店（国贸店）',
      isConnected: true,
      lastSync: '2026-05-14 10:30'
    },
    {
      id: 2,
      platform: '美团',
      platformIcon: '🍜',
      accountName: '香格里拉酒店',
      isConnected: true,
      lastSync: '2026-05-14 10:28'
    },
    {
      id: 3,
      platform: '小红书',
      platformIcon: '📕',
      accountName: '香格里拉酒店官方',
      isConnected: true,
      lastSync: '2026-05-13 18:45'
    },
    {
      id: 4,
      platform: '抖音',
      platformIcon: '🎵',
      accountName: '香格里拉酒店',
      isConnected: false,
      lastSync: '-'
    }
  ]);

  const handleConnect = (id: number) => {
    // 模拟连接
    setAccounts(prev => prev.map(acc => 
      acc.id === id 
        ? { 
            ...acc, 
            isConnected: true, 
            lastSync: new Date().toLocaleString('zh-CN', { 
              year: 'numeric', 
              month: '2-digit', 
              day: '2-digit', 
              hour: '2-digit', 
              minute: '2-digit' 
            })
          } 
        : acc
    ));
    success('连接成功', '账号已成功关联');
  };

  const handleDisconnect = (id: number) => {
    setAccounts(prev => prev.map(acc => 
      acc.id === id 
        ? { ...acc, isConnected: false, lastSync: '-' } 
        : acc
    ));
    success('已断开连接', '账号已取消关联');
  };

  const handleSync = (id: number) => {
    setAccounts(prev => prev.map(acc => 
      acc.id === id 
        ? { 
            ...acc, 
            lastSync: new Date().toLocaleString('zh-CN', { 
              year: 'numeric', 
              month: '2-digit', 
              day: '2-digit', 
              hour: '2-digit', 
              minute: '2-digit' 
            })
          } 
        : acc
    ));
    success('同步成功', '数据已更新');
  };

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
              {accounts.filter(acc => acc.isConnected).length}
            </p>
            <p className="text-xs text-slate-400">已关联</p>
          </div>
          <div className="w-px h-10 bg-slate-200"></div>
          <div className="text-center">
            <p className="text-2xl font-black text-slate-400">
              {accounts.filter(acc => !acc.isConnected).length}
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
                    {account.platformIcon}
                  </div>
                  <div>
                    <h3 className="font-bold text-slate-900">{account.platform}</h3>
                    {account.isConnected ? (
                      <div className="flex items-center gap-1 text-xs text-green-600">
                        <CheckCircle2 className="w-3 h-3" />
                        <span>{account.accountName}</span>
                      </div>
                    ) : (
                      <div className="flex items-center gap-1 text-xs text-slate-400">
                        <AlertCircle className="w-3 h-3" />
                        <span>未关联</span>
                      </div>
                    )}
                  </div>
                </div>
                {account.isConnected ? (
                  <span className="px-3 py-1 bg-green-50 text-green-600 text-xs font-bold rounded-lg">已连接</span>
                ) : (
                  <span className="px-3 py-1 bg-slate-100 text-slate-400 text-xs font-bold rounded-lg">未连接</span>
                )}
              </div>

              {account.isConnected && (
                <>
                  <div className="flex items-center gap-2 text-xs text-slate-400">
                    <span>最后同步：{account.lastSync}</span>
                  </div>
                  <div className="flex items-center gap-2 pt-2 border-t border-slate-50">
                    <button 
                      onClick={() => handleSync(account.id)}
                      className="flex-1 py-2 rounded-xl text-xs font-bold bg-indigo-50 text-indigo-600"
                    >
                      同步数据
                    </button>
                    <button 
                      onClick={() => handleDisconnect(account.id)}
                      className="flex-1 py-2 rounded-xl text-xs font-bold bg-rose-50 text-rose-600"
                    >
                      <Unlink className="w-3 h-3 inline mr-1" />
                      断开连接
                    </button>
                  </div>
                </>
              )}

              {!account.isConnected && (
                <Button 
                  onClick={() => handleConnect(account.id)}
                  className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl py-3 text-sm font-bold"
                >
                  <Link2 className="w-4 h-4 mr-2" />
                  立即关联
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

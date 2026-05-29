import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ArrowLeft, Link2, Unlink, CheckCircle2, AlertCircle, Plus,
  Loader2, RefreshCw, ChevronDown, X, Eye, EyeOff, Pencil
} from 'lucide-react';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';
import { platformsApi, PlatformAccount, PlatformStoreInfo, UpdatePlatformAccountDto } from '../../api/platforms';
import { storesApi, Store } from '../../api/stores';

// 支持的平台列表
const SUPPORTED_PLATFORMS = [
  { value: 'meituan', label: '美团开店宝', icon: '🍜', color: 'from-amber-400 to-orange-500' },
  { value: 'douyin', label: '抖音来客', icon: '🎵', color: 'from-slate-900 to-slate-700' },
  { value: 'taobao', label: '淘宝闪购', icon: '🛒', color: 'from-orange-400 to-red-500' },
];

export default function PlatformConnection() {
  const navigate = useNavigate();
  const { success, error: toastError } = useToast();

  const [accounts, setAccounts] = useState<PlatformAccount[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [syncingId, setSyncingId] = useState<string | null>(null);

  // 绑定弹窗状态
  const [showBindModal, setShowBindModal] = useState(false);
  const [bindPlatform, setBindPlatform] = useState('');
  const [bindUsername, setBindUsername] = useState('');
  const [bindPassword, setBindPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [bindLoading, setBindLoading] = useState(false);
  const [bindError, setBindError] = useState('');

  // 编辑弹窗状态
  const [showEditModal, setShowEditModal] = useState(false);
  const [editAccountId, setEditAccountId] = useState('');
  const [editUsername, setEditUsername] = useState('');
  const [editPassword, setEditPassword] = useState('');
  const [showEditPassword, setShowEditPassword] = useState(false);
  const [editLoading, setEditLoading] = useState(false);
  const [editError, setEditError] = useState('');

  // 店铺列表弹窗
  const [showStoresModal, setShowStoresModal] = useState(false);
  const [platformStores, setPlatformStores] = useState<PlatformStoreInfo[]>([]);
  const [storesLoading, setStoresLoading] = useState(false);
  const [bindAccountId, setBindAccountId] = useState<string>('');

  // 系统门店列表
  const [systemStores, setSystemStores] = useState<Store[]>([]);

  const fetchAccounts = useCallback(async () => {
    try {
      setLoading(true);
      const data = await platformsApi.getAccounts();
      setAccounts(data);
    } catch (err: any) {
      toastError('获取账号列表失败', err.message);
    } finally {
      setLoading(false);
    }
  }, [toastError]);

  const fetchSystemStores = useCallback(async () => {
    try {
      const data = await storesApi.getStores();
      setSystemStores(data);
    } catch {}
  }, []);

  useEffect(() => {
    fetchAccounts();
    fetchSystemStores();
  }, [fetchAccounts, fetchSystemStores]);

  // 提交绑定
  const handleBindSubmit = async () => {
    if (!bindPlatform || !bindUsername || !bindPassword) {
      setBindError('请填写完整信息');
      return;
    }
    setBindLoading(true);
    setBindError('');
    try {
      await platformsApi.connectPlatform({
        platform: bindPlatform,
        username: bindUsername,
        password: bindPassword,
      });
      success('绑定成功', '正在获取店铺列表...');
      setShowBindModal(false);
      setBindUsername('');
      setBindPassword('');
      await fetchAccounts();
    } catch (err: any) {
      setBindError(err.message || '绑定失败，请检查账号密码');
    } finally {
      setBindLoading(false);
    }
  };

  // 打开编辑弹窗
  const handleOpenEdit = (account: PlatformAccount) => {
    setEditAccountId(account.id);
    setEditUsername(account.platform_username || '');
    setEditPassword('');
    setEditError('');
    setShowEditModal(true);
  };

  // 提交编辑
  const handleEditSubmit = async () => {
    if (!editUsername) {
      setEditError('账号不能为空');
      return;
    }
    setEditLoading(true);
    setEditError('');
    try {
      const dto: UpdatePlatformAccountDto = { username: editUsername };
      if (editPassword) dto.password = editPassword;
      await platformsApi.updateAccount(editAccountId, dto);
      success('修改成功');
      setShowEditModal(false);
      await fetchAccounts();
    } catch (err: any) {
      setEditError(err.message || '修改失败');
    } finally {
      setEditLoading(false);
    }
  };

  // 查看平台店铺列表
  const handleViewStores = async (account: PlatformAccount) => {
    setBindAccountId(account.id);
    setStoresLoading(true);
    setShowStoresModal(true);
    try {
      const stores = await platformsApi.getPlatformStores(account.id);
      setPlatformStores(stores);
    } catch (err: any) {
      toastError('获取店铺列表失败', err.message);
    } finally {
      setStoresLoading(false);
    }
  };

  // 绑定平台店铺到系统门店
  const handleBindStore = async (platformStoreId: string, systemStoreId: string) => {
    try {
      setActionLoading(true);
      await platformsApi.bindStore(bindAccountId, platformStoreId, systemStoreId);
      success('店铺绑定成功');
      await fetchAccounts();
      setShowStoresModal(false);
    } catch (err: any) {
      toastError('绑定失败', err.message);
    } finally {
      setActionLoading(false);
    }
  };

  // 解绑
  const handleUnbind = async (accountId: string) => {
    if (!confirm('确定解绑该平台账号吗？')) return;
    try {
      setActionLoading(true);
      await platformsApi.unbindPlatform(accountId);
      success('解绑成功');
      await fetchAccounts();
    } catch (err: any) {
      toastError('解绑失败', err.message);
    } finally {
      setActionLoading(false);
    }
  };

  // 同步登录状态
  const handleSyncStatus = async (accountId: string) => {
    try {
      setSyncingId(accountId);
      await platformsApi.syncAccountStatus(accountId);
      success('已提交同步请求', '请稍后刷新查看最新状态');
      await fetchAccounts();
    } catch (err: any) {
      toastError('同步失败', err.message);
    } finally {
      setSyncingId(null);
    }
  };

  const getPlatformInfo = (platformValue: string) => {
    return SUPPORTED_PLATFORMS.find(p => p.value === platformValue) || SUPPORTED_PLATFORMS[0];
  };

  const getStatusBadge = (account: PlatformAccount) => {
    if (account.cookies_status === 'valid') {
      return <span className="inline-flex items-center gap-1 text-xs text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full"><CheckCircle2 className="w-3 h-3" />已连接</span>;
    }
    if (account.cookies_status === 'expired') {
      return <span className="inline-flex items-center gap-1 text-xs text-red-600 bg-red-50 px-2 py-0.5 rounded-full"><AlertCircle className="w-3 h-3" />已过期</span>;
    }
    return <span className="inline-flex items-center gap-1 text-xs text-amber-600 bg-amber-50 px-2 py-0.5 rounded-full"><AlertCircle className="w-3 h-3" />未知</span>;
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* 顶部导航 */}
      <div className="bg-white border-b border-slate-200 px-4 py-3 flex items-center gap-3 sticky top-0 z-10">
        <button onClick={() => navigate(-1)} className="p-1"><ArrowLeft className="w-5 h-5 text-slate-700" /></button>
        <h1 className="text-base font-semibold text-slate-900">平台账号绑定</h1>
      </div>

      <div className="p-4">
        <p className="text-sm text-slate-500 mb-4">绑定美团开店宝、抖音来客或淘宝闪购商家后台，系统将加密存储您的账号凭证，用于评论数据爬取。</p>

        {/* 已绑定账号列表 */}
        {loading ? (
          <div className="flex justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-slate-400" /></div>
        ) : (
          <>
            {accounts.length > 0 && (
              <div className="space-y-3 mb-6">
                <h2 className="text-sm font-medium text-slate-700">已绑定账号</h2>
                {accounts.map(account => {
                  const pInfo = getPlatformInfo(account.platform);
                  return (
                    <div key={account.id} className="bg-white rounded-xl border border-slate-200 p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-3">
                          <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${pInfo.color} flex items-center justify-center text-lg text-white shadow-sm`}>
                            {pInfo.icon}
                          </div>
                          <div>
                            <p className="text-sm font-semibold text-slate-900">{account.platform_username}</p>
                            <p className="text-xs text-slate-500">{pInfo.label}</p>
                          </div>
                        </div>
                        {getStatusBadge(account)}
                      </div>
                      <div className="flex gap-2">
                        <Button size="sm" variant="outline" onClick={() => handleViewStores(account)} className="flex-1">
                          <Link2 className="w-3.5 h-3.5 mr-1" />查看店铺
                        </Button>
                        <Button size="sm" variant="outline" onClick={() => handleOpenEdit(account)} className="flex-1">
                          <Pencil className="w-3.5 h-3.5 mr-1" />编辑
                        </Button>
                        <Button size="sm" variant="outline" onClick={() => handleSyncStatus(account.id)} disabled={syncingId === account.id} className="flex-1">
                          {syncingId === account.id ? <Loader2 className="w-3.5 h-3.5 mr-1 animate-spin" /> : <RefreshCw className="w-3.5 h-3.5 mr-1" />}
                          {syncingId === account.id ? '同步中' : '同步状态'}
                        </Button>
                        <Button size="sm" variant="destructive" onClick={() => handleUnbind(account.id)} disabled={actionLoading}>
                          <Unlink className="w-3.5 h-3.5" />
                        </Button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}

            {/* 绑定新账号 */}
            <Button onClick={() => { setBindPlatform(''); setBindError(''); setShowBindModal(true); }} className="w-full">
              <Plus className="w-4 h-4 mr-2" />绑定新平台账号
            </Button>
          </>
        )}
      </div>

      {/* 绑定弹窗 */}
      {showBindModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-end justify-center" onClick={() => setShowBindModal(false)}>
          <div className="bg-white w-full max-w-lg rounded-t-2xl p-6" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-slate-900">绑定平台账号</h3>
              <button onClick={() => setShowBindModal(false)} className="p-1"><X className="w-5 h-5 text-slate-400" /></button>
            </div>

            {/* 选择平台 */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-slate-700 mb-2">选择平台</label>
              <div className="grid grid-cols-3 gap-3">
                {SUPPORTED_PLATFORMS.map(p => (
                  <button key={p.value} onClick={() => setBindPlatform(p.value)}
                    className={`flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all
                      ${bindPlatform === p.value ? 'border-indigo-500 bg-indigo-50' : 'border-slate-200 hover:border-slate-300'}`}>
                    <span className="text-2xl">{p.icon}</span>
                    <span className="text-xs font-medium text-slate-700">{p.label}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* 账号 */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-slate-700 mb-2">商家账号</label>
              <input type="text" value={bindUsername} onChange={e => setBindUsername(e.target.value)}
                placeholder="请输入商家后台账号" className="w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>

            {/* 密码 */}
            <div className="mb-2">
              <label className="block text-sm font-medium text-slate-700 mb-2">密码</label>
              <div className="relative">
                <input type={showPassword ? 'text' : 'password'} value={bindPassword} onChange={e => setBindPassword(e.target.value)}
                  placeholder="请输入密码" className="w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 pr-10" />
                <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 p-0.5">
                  {showPassword ? <EyeOff className="w-4 h-4 text-slate-400" /> : <Eye className="w-4 h-4 text-slate-400" />}
                </button>
              </div>
            </div>

            {bindError && (
              <p className="text-sm text-red-600 mb-4">{bindError}</p>
            )}

            <p className="text-xs text-slate-400 mb-6">系统将加密存储您的账号凭证，仅用于评论数据爬取。</p>

            <div className="flex gap-3">
              <Button variant="outline" onClick={() => setShowBindModal(false)} className="flex-1">取消</Button>
              <Button onClick={handleBindSubmit} disabled={bindLoading} className="flex-1">
                {bindLoading ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : null}
                确认绑定
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* 编辑弹窗 */}
      {showEditModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-end justify-center" onClick={() => setShowEditModal(false)}>
          <div className="bg-white w-full max-w-lg rounded-t-2xl p-6" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-slate-900">编辑平台账号</h3>
              <button onClick={() => setShowEditModal(false)} className="p-1"><X className="w-5 h-5 text-slate-400" /></button>
            </div>

            {/* 账号 */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-slate-700 mb-2">商家账号</label>
              <input type="text" value={editUsername} onChange={e => setEditUsername(e.target.value)}
                placeholder="请输入商家后台账号" className="w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>

            {/* 密码 */}
            <div className="mb-2">
              <label className="block text-sm font-medium text-slate-700 mb-2">新密码（留空则不修改）</label>
              <div className="relative">
                <input type={showEditPassword ? 'text' : 'password'} value={editPassword} onChange={e => setEditPassword(e.target.value)}
                  placeholder="不修改请留空" className="w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 pr-10" />
                <button type="button" onClick={() => setShowEditPassword(!showEditPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 p-0.5">
                  {showEditPassword ? <EyeOff className="w-4 h-4 text-slate-400" /> : <Eye className="w-4 h-4 text-slate-400" />}
                </button>
              </div>
            </div>

            {editError && (
              <p className="text-sm text-red-600 mb-4">{editError}</p>
            )}

            <div className="flex gap-3">
              <Button variant="outline" onClick={() => setShowEditModal(false)} className="flex-1">取消</Button>
              <Button onClick={handleEditSubmit} disabled={editLoading} className="flex-1">
                {editLoading ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : null}
                保存修改
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* 店铺列表弹窗 */}
      {showStoresModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-end justify-center" onClick={() => setShowStoresModal(false)}>
          <div className="bg-white w-full max-w-lg rounded-t-2xl p-6 max-h-[80vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-slate-900">平台店铺列表</h3>
              <button onClick={() => setShowStoresModal(false)} className="p-1"><X className="w-5 h-5 text-slate-400" /></button>
            </div>

            {storesLoading ? (
              <div className="flex justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-slate-400" /></div>
            ) : platformStores.length === 0 ? (
              <p className="text-center text-sm text-slate-500 py-12">未获取到店铺，请检查账号绑定状态</p>
            ) : (
              <div className="space-y-3">
                {platformStores.map(ps => (
                  <div key={ps.platform_store_id} className="border border-slate-200 rounded-xl p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <p className="text-sm font-semibold text-slate-900">{ps.platform_store_name}</p>
                        <p className="text-xs text-slate-500">ID: {ps.platform_store_id}</p>
                      </div>
                      {ps.binded ? (
                        <span className="text-xs text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full">已绑定</span>
                      ) : (
                        <span className="text-xs text-slate-500">未绑定</span>
                      )}
                    </div>
                    {!ps.binded && (
                      <div className="flex gap-2 items-center">
                        <select
                          className="flex-1 px-3 py-2 border border-slate-200 rounded-lg text-sm"
                          value={(ps as any)._selectedStoreId || ''}
                          onChange={e => {
                            const val = e.target.value;
                            setPlatformStores(prev => prev.map(s =>
                              s.platform_store_id === ps.platform_store_id ? { ...s, _selectedStoreId: val } as any : s
                            ));
                          }}
                        >
                          <option value="">绑定到系统门店...</option>
                          {systemStores.map(ss => (
                            <option key={ss.id} value={ss.id}>{ss.name}</option>
                          ))}
                        </select>
                        <Button size="sm" onClick={() => {
                          const sid = (ps as any)._selectedStoreId;
                          if (!sid) { toastError('请先选择系统门店'); return; }
                          handleBindStore(ps.platform_store_id, sid);
                        }} disabled={actionLoading}>绑定</Button>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

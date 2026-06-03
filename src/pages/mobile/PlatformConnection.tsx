import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ArrowLeft, Link2, Unlink, CheckCircle2, AlertCircle, Plus,
  Loader2, RefreshCw, X, Eye, EyeOff, Pencil, FileText,
  QrCode, Clock, Smartphone, ShieldCheck, MessageSquare, Keyboard
} from 'lucide-react';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';
import { platformsApi, PlatformAccount, PlatformStoreInfo, UpdatePlatformAccountDto } from '../../api/platforms';

// 支持的平台列表
const SUPPORTED_PLATFORMS = [
  {
    value: 'meituan', label: '美团开店宝', icon: '🍜',
    color: 'from-amber-400 to-orange-500',
    desc: '使用美团App扫码登录开店宝',
    bindMethod: 'qr' as const,
  },
  {
    value: 'douyin', label: '抖音来客', icon: '🎵',
    color: 'from-slate-900 to-slate-700',
    desc: '手机号验证码登录抖音来客',
    bindMethod: 'sms' as const,
  },
];

export default function PlatformConnection() {
  const navigate = useNavigate();
  const { success, error: toastError } = useToast();

  const [accounts, setAccounts] = useState<PlatformAccount[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [syncingId, setSyncingId] = useState<string | null>(null);
  const [syncingReviewsId, setSyncingReviewsId] = useState<string | null>(null);
  const [syncReviewsProgress, setSyncReviewsProgress] = useState('');

  // 编辑弹窗状态
  const [showEditModal, setShowEditModal] = useState(false);
  const [editAccountId, setEditAccountId] = useState('');
  const [editUsername, setEditUsername] = useState('');
  const [editPassword, setEditPassword] = useState('');
  const [showEditPassword, setShowEditPassword] = useState(false);
  const [editLoading, setEditLoading] = useState(false);
  const [editError, setEditError] = useState('');

  // 二维码扫码登录状态（仅美团）
  const [showQRModal, setShowQRModal] = useState(false);
  const [qrTaskId, setQrTaskId] = useState('');
  const [qrImage, setQrImage] = useState('');
  const [qrStatus, setQrStatus] = useState('');
  const [qrRemaining, setQrRemaining] = useState(120);
  const [qrErrorMessage, setQrErrorMessage] = useState('');
  const [qrInitLoading, setQrInitLoading] = useState(false);
  const qrPollRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const qrCountdownRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // 短信验证码登录状态（抖音）
  const [showSMSModal, setShowSMSModal] = useState(false);
  const [smsPlatform, setSmsPlatform] = useState('');
  const [smsStep, setSmsStep] = useState<'phone' | 'code'>('phone');
  const [smsTaskId, setSmsTaskId] = useState('');
  const [smsPhone, setSmsPhone] = useState('');
  const [smsCode, setSmsCode] = useState('');
  const [smsLoading, setSmsLoading] = useState(false);
  const [smsError, setSmsError] = useState('');
  const [smsCodeSent, setSmsCodeSent] = useState(false);

  // 店铺列表弹窗
  const [showStoresModal, setShowStoresModal] = useState(false);
  const [platformStores, setPlatformStores] = useState<PlatformStoreInfo[]>([]);
  const [storesLoading, setStoresLoading] = useState(false);

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

  // ═══════════════════════════════════════════════════
  // 二维码扫码登录（美团开店宝）
  // ═══════════════════════════════════════════════════

  const handleStartQRLogin = async (platform: string) => {
    setQrInitLoading(true);
    setQrStatus('');
    setQrImage('');
    setQrErrorMessage('');
    setQrRemaining(120);
    setShowQRModal(true);

    try {
      const result = await platformsApi.startQRLogin(platform);
      setQrTaskId(result.task_id);
      setQrImage(result.qr_image);
      setQrStatus('waiting_scan');
      setQrRemaining(result.expires_in);
    } catch (err: any) {
      setQrErrorMessage(err.message || '获取二维码失败');
      setQrStatus('failed');
    } finally {
      setQrInitLoading(false);
    }
  };

  // 轮询二维码登录状态（优化：1秒轮询 + 支持 scanned 中间状态）
  useEffect(() => {
    if ((qrStatus !== 'waiting_scan' && qrStatus !== 'scanned') || !qrTaskId) return;

    qrPollRef.current = setInterval(async () => {
      try {
        const result = await platformsApi.getQRLoginStatus(qrTaskId);
        setQrStatus(result.status);
        setQrRemaining(result.remaining_seconds || 0);

        if (result.status === 'success') {
          success('绑定成功', `${result.platform_username || '账号'} 已连接`);
          setShowQRModal(false);
          cleanupQR();
          fetchAccounts(); // 不 await，后台刷新即可
        } else if (result.status === 'expired' || result.status === 'failed') {
          setQrErrorMessage(result.error_message || (result.status === 'expired' ? '二维码已过期' : '登录失败'));
          cleanupQR();
        }
        // scanned 状态由 qrStatus 更新自动处理 UI
      } catch (err: any) {
        // 网络错误不中断轮询
      }
    }, 1000);  // 优化：3秒 → 1秒，配合后端 0.5s 检测间隔

    return () => { if (qrPollRef.current) clearInterval(qrPollRef.current); };
  }, [qrStatus, qrTaskId]);

  // 倒计时（waiting_scan 和 scanned 状态都需要倒计时）
  useEffect(() => {
    if (qrStatus !== 'waiting_scan' && qrStatus !== 'scanned') return;
    qrCountdownRef.current = setInterval(() => {
      setQrRemaining(prev => {
        if (prev <= 1) {
          setQrStatus('expired');
          setQrErrorMessage('二维码已过期，请重新获取');
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => { if (qrCountdownRef.current) clearInterval(qrCountdownRef.current); };
  }, [qrStatus]);

  const cleanupQR = () => {
    if (qrPollRef.current) { clearInterval(qrPollRef.current); qrPollRef.current = null; }
    if (qrCountdownRef.current) { clearInterval(qrCountdownRef.current); qrCountdownRef.current = null; }
  };

  const handleCloseQRModal = async () => {
    cleanupQR();
    if (qrTaskId) {
      try { await platformsApi.cancelQRLogin(qrTaskId); } catch {}
    }
    setShowQRModal(false);
    setQrStatus('');
    setQrImage('');
    setQrTaskId('');
  };

  const handleRefreshQR = () => {
    cleanupQR();
    handleStartQRLogin('meituan');
  };

  // ═══════════════════════════════════════════════════
  // 短信验证码登录（抖音来客）
  // ═══════════════════════════════════════════════════

  const handleOpenSMSLogin = (platform: string) => {
    setSmsPlatform(platform);
    setSmsStep('phone');
    setSmsPhone('');
    setSmsCode('');
    setSmsTaskId('');
    setSmsError('');
    setSmsCodeSent(false);
    setSmsLoading(false);
    setShowSMSModal(true);
  };

  // 第一步：发送验证码
  const handleSendSMSCode = async () => {
    if (!smsPhone || smsPhone.length < 11) {
      setSmsError('请输入正确的手机号');
      return;
    }
    setSmsLoading(true);
    setSmsError('');
    try {
      const result = await platformsApi.startSMSLogin(smsPlatform, smsPhone);
      if (result.success && result.task_id) {
        setSmsTaskId(result.task_id || '');
        setSmsCodeSent(!!result.code_sent);
        setSmsStep('code');
      } else {
        setSmsError(result.error || '发送验证码失败');
      }
    } catch (err: any) {
      setSmsError(err.message || '发送验证码失败，请重试');
    } finally {
      setSmsLoading(false);
    }
  };

  // 第二步：提交验证码
  const handleVerifySMSCode = async () => {
    if (!smsCode || smsCode.length < 4) {
      setSmsError('请输入正确的验证码');
      return;
    }
    setSmsLoading(true);
    setSmsError('');
    try {
      const result = await platformsApi.verifySMSCode(smsTaskId, smsPlatform, smsCode);
      if (result.status === 'success') {
        success('绑定成功', `${SUPPORTED_PLATFORMS.find(p => p.value === smsPlatform)?.label || '账号'} 已连接`);
        setShowSMSModal(false);
        await fetchAccounts();
      } else {
        setSmsError(result.error || '验证码错误，请重试');
      }
    } catch (err: any) {
      setSmsError(err.message || '验证失败，请重试');
    } finally {
      setSmsLoading(false);
    }
  };

  const handleCloseSMSModal = async () => {
    if (smsTaskId) {
      try { await platformsApi.cancelSMSLogin(smsTaskId); } catch {}
    }
    setShowSMSModal(false);
  };

  // 返回手机号输入步骤
  const handleSMSBack = () => {
    setSmsStep('phone');
    setSmsCode('');
    setSmsError('');
  };

  // ═══════════════════════════════════════════════════
  // 通用功能
  // ═══════════════════════════════════════════════════

  useEffect(() => {
    fetchAccounts();
  }, [fetchAccounts]);

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

  // 查看平台店铺列表（从已同步的 store_platforms 表查询）
  const handleViewStores = async (account: PlatformAccount) => {
    setStoresLoading(true);
    setShowStoresModal(true);
    try {
      const stores = await platformsApi.getAccountStores(account.id);
      setPlatformStores(stores);
    } catch (err: any) {
      toastError('获取店铺列表失败', err.message);
    } finally {
      setStoresLoading(false);
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

  // 同步登录状态 + 店铺数据
  const handleSyncStatus = async (accountId: string) => {
    try {
      setSyncingId(accountId);
      const result = await platformsApi.syncAccountStatus(accountId);
      console.log('[SyncStatus] API result:', result);
      if (result.status === 'valid') {
        const storeCount = result.store_count || 0;
        const username = result.platform_username || '';
        const syncDetail = result.sync_detail || {};
        const syncedStores = result.stores || [];
        // 打印同步详情到控制台方便调试
        if (syncedStores.length > 0) {
          console.log('[SyncStatus] Synced stores:', syncedStores);
        }
        const detailMsg = syncDetail.sync_error
          ? ` (提取方式: ${syncDetail.method || '未知'}，${syncDetail.sync_error})`
          : ` (提取方式: ${syncDetail.method || '未知'})`;
        success(
          '同步成功',
          `${username ? `${username}，` : ''}${storeCount} 个店铺已同步${detailMsg}`,
        );
      } else if (result.status === 'expired') {
        toastError('同步失败', result.sync_error || result.error || '登录态已失效，请重新扫码绑定');
      } else {
        toastError('同步失败', result.sync_error || result.error || '未知错误');
      }
      await fetchAccounts();
    } catch (err: any) {
      toastError('同步失败', err.message || '网络错误');
    } finally {
      setSyncingId(null);
    }
  };

  // 同步评论数据（轮询模式，跟扫码登录一样的体验）
  const syncReviewsTaskRef = useRef<{ accountId: string; taskId: string } | null>(null);
  const syncReviewsPollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const cleanupSyncReviews = () => {
    if (syncReviewsPollRef.current) {
      clearInterval(syncReviewsPollRef.current);
      syncReviewsPollRef.current = null;
    }
    syncReviewsTaskRef.current = null;
    setSyncingReviewsId(null);
    setSyncReviewsProgress('');
  };

  useEffect(() => {
    if (!syncingReviewsId || !syncReviewsTaskRef.current) return;

    const poll = async () => {
      const { accountId, taskId } = syncReviewsTaskRef.current!;
      try {
        const status = await platformsApi.getSyncReviewsStatus(accountId, taskId);

        // 更新进度
        if (status.progress) {
          const platformLabels: Record<string, string> = { meituan: '美团', dianping: '大众点评' };
          const label = platformLabels[status.current_platform] || status.current_platform;
          setSyncReviewsProgress(label ? `${status.progress} - ${label}` : status.progress);
        }

        if (status.status === 'success') {
          // 同步完成（入库已在后台完成），直接从 status.result 取统计
          clearInterval(syncReviewsPollRef.current!);
          syncReviewsPollRef.current = null;
          const result = status.result || {};
          const created = result.created || 0;
          const skipped = result.skipped || 0;
          const errs = result.errors || [];
          if (errs.length > 0 && created === 0) {
            toastError('评论同步失败', errs.join('; '));
          } else {
            success('评论同步完成', `新增 ${created} 条评论${skipped > 0 ? `，跳过 ${skipped} 条重复` : ''}${errs.length > 0 ? `\n${errs.join('; ')}` : ''}`);
          }
          window.dispatchEvent(new Event('visibilitychange'));
          cleanupSyncReviews();
        } else if (status.status === 'failed') {
          clearInterval(syncReviewsPollRef.current!);
          syncReviewsPollRef.current = null;
          toastError('评论同步失败', status.error || '未知错误');
          cleanupSyncReviews();
        }
        // running 状态继续轮询
      } catch {
        // 网络错误不中断轮询
      }
    };

    // 2秒轮询
    syncReviewsPollRef.current = setInterval(poll, 2000);

    return () => {
      if (syncReviewsPollRef.current) {
        clearInterval(syncReviewsPollRef.current);
        syncReviewsPollRef.current = null;
      }
    };
  }, [syncingReviewsId, syncReviewsTaskRef.current]);

  const handleSyncReviews = async (accountId: string) => {
    try {
      setSyncingReviewsId(accountId);
      setSyncReviewsProgress('准备中...');
      const result = await platformsApi.syncAccountReviews(accountId);
      const taskId = result.task_id;
      if (!taskId) {
        toastError('评论同步失败', '未返回任务 ID');
        setSyncingReviewsId(null);
        return;
      }
      // 保存任务信息，触发轮询 effect
      syncReviewsTaskRef.current = { accountId, taskId };
      // 手动触发 re-render 让 useEffect 重新绑定
      setSyncingReviewsId(accountId);
      setSyncReviewsProgress('同步中...');
    } catch (err: any) {
      toastError('评论同步失败', err.message || '网络错误');
      setSyncingReviewsId(null);
      setSyncReviewsProgress('');
    }
  };

  const getPlatformInfo = (platformValue: string) => {
    return SUPPORTED_PLATFORMS.find(p => p.value === platformValue) || SUPPORTED_PLATFORMS[0];
  };

  const getStatusBadge = (account: PlatformAccount) => {
    if (account.cookies_status === 'valid') {
      return <span className="inline-flex items-center gap-1 text-xs text-emerald-600 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full"><CheckCircle2 className="w-3 h-3" />已连接</span>;
    }
    if (account.cookies_status === 'expired') {
      return <span className="inline-flex items-center gap-1 text-xs text-rose-600 bg-rose-50 border border-rose-200 px-2 py-0.5 rounded-full"><AlertCircle className="w-3 h-3" />已过期</span>;
    }
    return <span className="inline-flex items-center gap-1 text-xs text-amber-600 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded-full"><AlertCircle className="w-3 h-3" />未知</span>;
  };

  // 判断平台是否已有效绑定
  const isPlatformBound = (platform: string) =>
    accounts.some(a => a.platform === platform && a.cookies_status === 'valid');

  return (
    <div className="min-h-screen bg-slate-50">
      {/* 顶部导航 */}
      <div className="bg-white border-b border-slate-100 px-4 py-3 flex items-center gap-3 sticky top-0 z-10 safe-top">
        <button onClick={() => navigate(-1)} className="p-1 active:scale-95 transition-transform"><ArrowLeft className="w-5 h-5 text-slate-700" /></button>
        <h1 className="text-base font-semibold text-slate-900">平台账号绑定</h1>
      </div>

      <div className="p-4">
        <p className="text-sm text-slate-500 mb-4">绑定美团开店宝、抖音来客商家后台，系统将加密存储您的账号凭证，用于评论数据爬取。</p>

        {/* 已绑定账号列表 */}
        {loading ? (
          <div className="flex justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-slate-400" /></div>
        ) : (
          <>
            {accounts.length > 0 && (
              <div className="space-y-3 mb-6">
                <h2 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">已绑定账号</h2>
                {accounts.map(account => {
                  const pInfo = getPlatformInfo(account.platform);
                  return (
                    <div key={account.id} className="bg-white rounded-xl border border-slate-100 p-4 shadow-sm">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-3 min-w-0 flex-1">
                          <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${pInfo.color} flex items-center justify-center text-lg text-white shadow-sm flex-shrink-0`}>
                            {pInfo.icon}
                          </div>
                          <div className="min-w-0 flex-1">
                            <p className="text-sm font-semibold text-slate-900 truncate">{account.platform_username || '未获取用户名'}</p>
                            <p className="text-xs text-slate-500">{pInfo.label}</p>
                          </div>
                        </div>
                        {getStatusBadge(account)}
                      </div>
                      <div className="flex flex-wrap gap-2">
                        <Button size="sm" variant="outline" onClick={() => handleViewStores(account)} className="rounded-lg text-xs">
                          <Link2 className="w-3 h-3 mr-1" />查看店铺
                        </Button>
                        <Button size="sm" variant="outline" onClick={() => handleOpenEdit(account)} className="rounded-lg text-xs">
                          <Pencil className="w-3 h-3 mr-1" />编辑
                        </Button>
                        <Button size="sm" variant="outline" onClick={() => handleSyncStatus(account.id)} disabled={syncingId === account.id} className="rounded-lg text-xs">
                          {syncingId === account.id ? <Loader2 className="w-3 h-3 mr-1 animate-spin" /> : <RefreshCw className="w-3 h-3 mr-1" />}
                          {syncingId === account.id ? '同步中' : '同步状态'}
                        </Button>
                        <Button size="sm" variant="outline" onClick={() => handleSyncReviews(account.id)} disabled={syncingReviewsId === account.id || account.cookies_status !== 'valid'} className="rounded-lg border-orange-200 text-orange-600 hover:bg-orange-50 text-xs">
                          {syncingReviewsId === account.id ? <Loader2 className="w-3 h-3 mr-1 animate-spin" /> : <FileText className="w-3 h-3 mr-1" />}
                          {syncingReviewsId === account.id ? (syncReviewsProgress || '同步中...').split(' - ')[0] : '同步评论'}
                        </Button>
                        <Button size="sm" variant="outline" className="border-rose-200 text-rose-600 hover:bg-rose-50 rounded-lg" onClick={() => handleUnbind(account.id)} disabled={actionLoading}>
                          <Unlink className="w-3.5 h-3.5" />
                        </Button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}

            {/* 绑定新账号 — 区分平台绑定方式 */}
            <div className="mb-6">
              <h2 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3">绑定新账号</h2>
              <div className="space-y-3">
                {SUPPORTED_PLATFORMS.filter(p => !isPlatformBound(p.value)).map(p => (
                  <button key={p.value}
                    onClick={() => p.bindMethod === 'qr' ? handleStartQRLogin(p.value) : handleOpenSMSLogin(p.value)}
                    className="w-full flex items-center gap-3 p-4 bg-white rounded-xl border border-slate-100 shadow-sm hover:shadow-md transition-all active:scale-[0.98]">
                    <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${p.color} flex items-center justify-center text-lg text-white shadow-sm shrink-0`}>
                      {p.icon}
                    </div>
                    <div className="text-left flex-1 min-w-0">
                      <p className="text-sm font-semibold text-slate-900">{p.label}</p>
                      <p className="text-xs text-slate-500 truncate">{p.desc}</p>
                    </div>
                    {p.bindMethod === 'qr' ? (
                      <QrCode className="w-5 h-5 text-slate-400 shrink-0" />
                    ) : (
                      <Smartphone className="w-5 h-5 text-slate-400 shrink-0" />
                    )}
                  </button>
                ))}
              </div>
            </div>

            {SUPPORTED_PLATFORMS.every(p => isPlatformBound(p.value)) && (
              <div className="text-center py-8">
                <CheckCircle2 className="w-12 h-12 text-emerald-400 mx-auto mb-3" />
                <p className="text-sm text-slate-600">所有平台均已绑定</p>
              </div>
            )}
          </>
        )}
      </div>

      {/* ═══════════════════════════════════════════════════ */}
      {/* 二维码扫码登录弹窗（仅美团） */}
      {/* ═══════════════════════════════════════════════════ */}
      {showQRModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-end justify-center" onClick={handleCloseQRModal}>
          <div className="bg-white w-full max-w-lg rounded-t-2xl p-6" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center text-sm text-white shadow-sm">
                  🍜
                </div>
                <h3 className="text-lg font-semibold text-slate-900">扫码登录 - 美团开店宝</h3>
              </div>
              <button onClick={handleCloseQRModal} className="p-1 active:scale-95 transition-transform"><X className="w-5 h-5 text-slate-400" /></button>
            </div>

            {qrInitLoading ? (
              <div className="flex flex-col items-center justify-center py-16">
                <Loader2 className="w-8 h-8 animate-spin text-indigo-600 mb-3" />
                <p className="text-sm text-slate-500">正在获取二维码...</p>
              </div>
            ) : qrStatus === 'waiting_scan' || qrStatus === 'scanned' ? (
              <div className="flex flex-col items-center py-6">
                {qrImage && qrStatus === 'waiting_scan' && (
                  <div className="bg-white border-2 border-slate-100 rounded-2xl p-4 mb-4 shadow-sm">
                    <img
                      src={`data:image/png;base64,${qrImage}`}
                      alt="登录二维码"
                      className="w-48 h-48 object-contain"
                    />
                  </div>
                )}
                {qrStatus === 'scanned' ? (
                  <>
                    <div className="w-20 h-20 rounded-2xl bg-indigo-600 flex items-center justify-center mb-4 shadow-lg shadow-indigo-200">
                      <Smartphone className="w-10 h-10 text-white" />
                    </div>
                    <p className="text-base font-semibold text-slate-900">扫码已确认</p>
                    <p className="text-sm text-slate-500 mt-1">正在验证登录状态，请稍候...</p>
                    <div className="mt-4 flex items-center gap-2">
                      <Loader2 className="w-4 h-4 animate-spin text-indigo-600" />
                      <span className="text-xs text-indigo-600 font-medium">登录验证中</span>
                    </div>
                  </>
                ) : (
                  <>
                    <div className="flex items-center gap-2 text-sm text-slate-600 mb-3">
                      <Smartphone className="w-4 h-4 text-indigo-600" />
                      <span>请打开美团App扫码登录开店宝</span>
                    </div>
                    <div className="flex items-center gap-2 text-xs text-slate-400">
                      <Clock className="w-3.5 h-3.5" />
                      <span>{Math.ceil(qrRemaining / 60)}:{String(qrRemaining % 60).padStart(2, '0')} 后过期</span>
                    </div>
                    <Button variant="outline" size="sm" onClick={handleRefreshQR} className="mt-4 rounded-lg">
                      <RefreshCw className="w-3.5 h-3.5 mr-1" />刷新二维码
                    </Button>
                  </>
                )}
              </div>
            ) : qrStatus === 'success' ? (
              <div className="flex flex-col items-center py-12">
                <div className="w-16 h-16 rounded-full bg-emerald-100 flex items-center justify-center mb-4">
                  <CheckCircle2 className="w-8 h-8 text-emerald-600" />
                </div>
                <p className="text-base font-semibold text-slate-900">登录成功</p>
                <p className="text-sm text-slate-500 mt-1">账号已自动绑定</p>
              </div>
            ) : (qrStatus === 'expired' || qrStatus === 'failed') ? (
              <div className="flex flex-col items-center py-12">
                <div className="w-16 h-16 rounded-full bg-rose-50 flex items-center justify-center mb-4">
                  <AlertCircle className="w-8 h-8 text-rose-500" />
                </div>
                <p className="text-base font-semibold text-slate-900">
                  {qrStatus === 'expired' ? '二维码已过期' : '登录失败'}
                </p>
                <p className="text-sm text-slate-500 mt-1 mb-4">{qrErrorMessage || '请重试'}</p>
                <Button onClick={handleRefreshQR} className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg">
                  <RefreshCw className="w-4 h-4 mr-2" />重新获取
                </Button>
              </div>
            ) : null}

            <div className="flex items-center justify-center gap-1.5 mt-4 pt-4 border-t border-slate-100">
              <ShieldCheck className="w-3.5 h-3.5 text-slate-400" />
              <p className="text-xs text-slate-400">扫码信息仅用于评论数据采集，不会泄露</p>
            </div>
          </div>
        </div>
      )}

      {/* ═══════════════════════════════════════════════════ */}
      {/* 短信验证码登录弹窗（抖音来客） */}
      {/* ═══════════════════════════════════════════════════ */}
      {showSMSModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-end justify-center" onClick={handleCloseSMSModal}>
          <div className="bg-white w-full max-w-lg rounded-t-2xl p-6" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-slate-900 to-slate-700 flex items-center justify-center text-sm text-white shadow-sm">
                  🎵
                </div>
                <h3 className="text-lg font-semibold text-slate-900">手机号登录 - 抖音来客</h3>
              </div>
              <button onClick={handleCloseSMSModal} className="p-1 active:scale-95 transition-transform"><X className="w-5 h-5 text-slate-400" /></button>
            </div>

            {smsStep === 'phone' ? (
              /* 第一步：输入手机号 */
              <div>
                <p className="text-sm text-slate-500 mb-6">我们将向您的手机号发送验证码，请在抖音来客后台完成登录绑定。</p>

                <div className="mb-4">
                  <label className="block text-sm font-medium text-slate-700 mb-2">手机号码</label>
                  <div className="flex gap-3">
                    <input
                      type="tel"
                      value={smsPhone}
                      onChange={e => setSmsPhone(e.target.value)}
                      placeholder="请输入抖音来客绑定的手机号"
                      maxLength={11}
                      className="flex-1 px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600"
                    />
                    <Button
                      onClick={handleSendSMSCode}
                      disabled={smsLoading || smsPhone.length < 11}
                      className="px-6 whitespace-nowrap bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl"
                    >
                      {smsLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
                      {smsLoading ? '发送中' : '发送验证码'}
                    </Button>
                  </div>
                </div>

                {smsError && (
                  <div className="flex items-center gap-2 text-sm text-rose-600 mb-4">
                    <AlertCircle className="w-4 h-4 shrink-0" />
                    <span>{smsError}</span>
                  </div>
                )}

                <div className="flex items-center justify-center gap-1.5 mt-6 pt-4 border-t border-slate-100">
                  <ShieldCheck className="w-3.5 h-3.5 text-slate-400" />
                  <p className="text-xs text-slate-400">手机号仅用于登录验证，不会泄露或存储</p>
                </div>
              </div>
            ) : (
              /* 第二步：输入验证码 */
              <div>
                <div className="flex items-center gap-2 text-sm text-slate-500 mb-1">
                  <span>验证码已发送至</span>
                  <span className="font-medium text-slate-700">{smsPhone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')}</span>
                </div>
                <button onClick={handleSMSBack} className="text-sm text-indigo-600 mb-4 hover:underline">
                  更换手机号
                </button>

                <div className="mb-4">
                  <label className="block text-sm font-medium text-slate-700 mb-2">输入验证码</label>
                  <input
                    type="text"
                    value={smsCode}
                    onChange={e => setSmsCode(e.target.value)}
                    placeholder="请输入收到的短信验证码"
                    maxLength={6}
                    className="w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600 text-center text-lg tracking-widest font-mono"
                    autoFocus
                  />
                </div>

                <Button
                  onClick={handleVerifySMSCode}
                  disabled={smsLoading || smsCode.length < 4}
                  className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl"
                >
                  {smsLoading ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <Keyboard className="w-4 h-4 mr-2" />}
                  {smsLoading ? '验证中...' : '确认登录'}
                </Button>

                {smsError && (
                  <div className="flex items-center gap-2 text-sm text-rose-600 mt-3">
                    <AlertCircle className="w-4 h-4 shrink-0" />
                    <span>{smsError}</span>
                  </div>
                )}

                <div className="flex items-center justify-center gap-1.5 mt-4 pt-4 border-t border-slate-100">
                  <ShieldCheck className="w-3.5 h-3.5 text-slate-400" />
                  <p className="text-xs text-slate-400">验证码仅用于本次登录，不会存储</p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* 编辑弹窗 */}
      {showEditModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-end justify-center" onClick={() => setShowEditModal(false)}>
          <div className="bg-white w-full max-w-lg rounded-t-2xl p-6" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-slate-900">编辑平台账号</h3>
              <button onClick={() => setShowEditModal(false)} className="p-1 active:scale-95 transition-transform"><X className="w-5 h-5 text-slate-400" /></button>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-slate-700 mb-2">商家账号</label>
              <input type="text" value={editUsername} onChange={e => setEditUsername(e.target.value)}
                placeholder="请输入商家后台账号" className="w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600" />
            </div>

            <div className="mb-2">
              <label className="block text-sm font-medium text-slate-700 mb-2">新密码（留空则不修改）</label>
              <div className="relative">
                <input type={showEditPassword ? 'text' : 'password'} value={editPassword} onChange={e => setEditPassword(e.target.value)}
                  placeholder="不修改请留空" className="w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600 pr-10" />
                <button type="button" onClick={() => setShowEditPassword(!showEditPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 p-0.5">
                  {showEditPassword ? <EyeOff className="w-4 h-4 text-slate-400" /> : <Eye className="w-4 h-4 text-slate-400" />}
                </button>
              </div>
            </div>

            {editError && (
              <p className="text-sm text-rose-600 mb-4">{editError}</p>
            )}

            <div className="flex gap-3">
              <Button variant="outline" onClick={() => setShowEditModal(false)} className="flex-1 rounded-lg">取消</Button>
              <Button onClick={handleEditSubmit} disabled={editLoading} className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg">
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
              <h3 className="text-lg font-semibold text-slate-900">同步店铺列表</h3>
              <button onClick={() => setShowStoresModal(false)} className="p-1 active:scale-95 transition-transform"><X className="w-5 h-5 text-slate-400" /></button>
            </div>

            {storesLoading ? (
              <div className="flex justify-center py-12"><Loader2 className="w-6 h-6 animate-spin text-slate-400" /></div>
            ) : platformStores.length === 0 ? (
              <p className="text-center text-sm text-slate-500 py-12">未同步到店铺，请先点击"同步状态"获取平台店铺数据</p>
            ) : (
              <div className="space-y-3">
                {platformStores.map(ps => (
                  <div key={ps.platform_store_id} className="border border-slate-100 rounded-xl p-4 shadow-sm">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-semibold text-slate-900">{ps.platform_store_name}</p>
                        <p className="text-xs text-slate-500">平台ID: {ps.platform_store_id}</p>
                      </div>
                      <span className="text-xs text-emerald-600 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full">已绑定</span>
                    </div>
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

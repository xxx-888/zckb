import React, { useState, useEffect } from 'react';
import { Plus, Pencil, Trash2, Check, X, AlertTriangle, Loader2, CreditCard, DollarSign, Search, Filter, Calendar, RefreshCw, ChevronDown, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';
import { subscriptionApi, SubscriptionPlan } from '../../api/subscription';
import { adminApi } from '../../api/admin';
import { AdminLayout } from '../../components/AdminLayout';

export const SubscriptionManagement: React.FC = () => {
  const { success, error } = useToast();

  // Tab 状态
  const [activeTab, setActiveTab] = useState<'plans' | 'subscriptions' | 'payments'>('plans');

  // ==================== 套餐管理状态 ====================
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [plans, setPlans] = useState<SubscriptionPlan[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [editingPlan, setEditingPlan] = useState<SubscriptionPlan | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    price_monthly: 0,
    price_yearly: 0,
    features: [] as string[],
    max_stores: 1,
    max_reviews_per_month: undefined as number | undefined,
    is_active: true,
  });
  const [featureInput, setFeatureInput] = useState('');

  // ==================== 订阅记录管理状态 ====================
  const [subscriptionsLoading, setSubscriptionsLoading] = useState(false);
  const [subscriptions, setSubscriptions] = useState<any[]>([]);
  const [subscriptionsTotal, setSubscriptionsTotal] = useState(0);
  const [subscriptionsPage, setSubscriptionsPage] = useState(1);
  const [subscriptionsPageSize] = useState(20);
  const [subscriptionsFilters, setSubscriptionsFilters] = useState({
    user_id: '',
    status: '',
    plan_id: '',
  });
  const [showStatusModal, setShowStatusModal] = useState(false);
  const [statusUpdateData, setStatusUpdateData] = useState<{ id: string; currentStatus: string }>({ id: '', currentStatus: '' });
  const [newStatus, setNewStatus] = useState('');

  // ==================== 支付记录管理状态 ====================
  const [paymentsLoading, setPaymentsLoading] = useState(false);
  const [payments, setPayments] = useState<any[]>([]);
  const [paymentsTotal, setPaymentsTotal] = useState(0);
  const [paymentsPage, setPaymentsPage] = useState(1);
  const [paymentsPageSize] = useState(20);
  const [paymentsFilters, setPaymentsFilters] = useState({
    user_id: '',
    status: '',
    payment_method: '',
    start_date: '',
    end_date: '',
  });
  const [showPaymentStatusModal, setShowPaymentStatusModal] = useState(false);
  const [paymentStatusUpdateData, setPaymentStatusUpdateData] = useState<{ id: string; currentStatus: string; transaction_id?: string }>({ id: '', currentStatus: '' });
  const [newPaymentStatus, setNewPaymentStatus] = useState('');
  const [newTransactionId, setNewTransactionId] = useState('');

  // ==================== 套餐管理函数 ====================

  // 加载套餐列表
  useEffect(() => {
    if (activeTab === 'plans') {
      loadPlans();
    }
  }, [activeTab]);

  const loadPlans = async () => {
    try {
      setLoading(true);
      const data = await subscriptionApi.getAllPlans();
      setPlans(Array.isArray(data) ? data : []);
    } catch (err: any) {
      error('加载失败', err.message || '无法获取套餐列表');
      setPlans([]);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenCreate = () => {
    setEditingPlan(null);
    setFormData({
      name: '',
      price_monthly: 0,
      price_yearly: 0,
      features: [],
      max_stores: 1,
      max_reviews_per_month: undefined,
      is_active: true,
    });
    setShowModal(true);
  };

  const handleOpenEdit = (plan: SubscriptionPlan) => {
    setEditingPlan(plan);
    setFormData({
      name: plan.name,
      price_monthly: plan.price_monthly,
      price_yearly: plan.price_yearly,
      features: plan.features || [],
      max_stores: plan.max_stores,
      max_reviews_per_month: plan.max_reviews_per_month,
      is_active: plan.is_active,
    });
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingPlan(null);
    setFeatureInput('');
  };

  const handleAddFeature = () => {
    if (!featureInput.trim()) return;
    setFormData(prev => ({
      ...prev,
      features: [...prev.features, featureInput.trim()]
    }));
    setFeatureInput('');
  };

  const handleRemoveFeature = (index: number) => {
    setFormData(prev => ({
      ...prev,
      features: prev.features.filter((_, i) => i !== index)
    }));
  };

  const handleSave = async () => {
    if (!formData.name) {
      error('保存失败', '请输入套餐名称');
      return;
    }

    try {
      setActionLoading(true);
      if (editingPlan) {
        await subscriptionApi.updatePlan(editingPlan.id, formData);
        success('更新成功', `套餐「${formData.name}」已更新`);
      } else {
        await subscriptionApi.createPlan(formData);
        success('创建成功', `套餐「${formData.name}」已创建`);
      }
      handleCloseModal();
      loadPlans();
    } catch (err: any) {
      error('保存失败', err.message || '操作失败');
    } finally {
      setActionLoading(false);
    }
  };

  const handleToggle = async (plan: SubscriptionPlan) => {
    try {
      setActionLoading(true);
      await subscriptionApi.togglePlan(plan.id);
      success('操作成功', `已${plan.is_active ? '禁用' : '启用'}该套餐`);
      loadPlans();
    } catch (err: any) {
      error('操作失败', err.message || '操作失败');
    } finally {
      setActionLoading(false);
    }
  };

  const handleDelete = async (plan: SubscriptionPlan) => {
    if (!confirm(`确定要删除套餐「${plan.name}」吗？此操作不可恢复。`)) {
      return;
    }

    try {
      setActionLoading(true);
      await subscriptionApi.deletePlan(plan.id);
      success('删除成功', `套餐「${plan.name}」已删除`);
      loadPlans();
    } catch (err: any) {
      error('删除失败', err.message || '删除失败');
    } finally {
      setActionLoading(false);
    }
  };

  // ==================== 订阅记录管理函数 ====================

  // 加载订阅记录
  useEffect(() => {
    if (activeTab === 'subscriptions') {
      loadSubscriptions();
    }
  }, [activeTab, subscriptionsPage]);

  const loadSubscriptions = async () => {
    try {
      setSubscriptionsLoading(true);
      const params: any = {
        page: subscriptionsPage,
        page_size: subscriptionsPageSize,
      };
      if (subscriptionsFilters.user_id) params.user_id = subscriptionsFilters.user_id;
      if (subscriptionsFilters.status) params.status = subscriptionsFilters.status;
      if (subscriptionsFilters.plan_id) params.plan_id = subscriptionsFilters.plan_id;

      const data = await adminApi.getSubscriptionRecords(params);
      setSubscriptions(data.items || []);
      setSubscriptionsTotal(data.total || 0);
    } catch (err: any) {
      error('加载失败', err.message || '无法获取订阅记录');
    } finally {
      setSubscriptionsLoading(false);
    }
  };

  const handleSearchSubscriptions = () => {
    setSubscriptionsPage(1);
    loadSubscriptions();
  };

  const handleResetSubscriptions = () => {
    setSubscriptionsFilters({ user_id: '', status: '', plan_id: '' });
    setSubscriptionsPage(1);
    setTimeout(() => loadSubscriptions(), 0);
  };

  const handleUpdateStatus = async () => {
    if (!newStatus) {
      error('更新失败', '请选择新状态');
      return;
    }

    try {
      setActionLoading(true);
      await adminApi.updateSubscriptionStatus(statusUpdateData.id, newStatus);
      success('更新成功', '订阅状态已更新');
      setShowStatusModal(false);
      setNewStatus('');
      loadSubscriptions();
    } catch (err: any) {
      error('更新失败', err.message || '操作失败');
    } finally {
      setActionLoading(false);
    }
  };

  // ==================== 支付记录管理函数 ====================

  // 加载支付记录
  useEffect(() => {
    if (activeTab === 'payments') {
      loadPayments();
    }
  }, [activeTab, paymentsPage]);

  const loadPayments = async () => {
    try {
      setPaymentsLoading(true);
      const params: any = {
        page: paymentsPage,
        page_size: paymentsPageSize,
      };
      if (paymentsFilters.user_id) params.user_id = paymentsFilters.user_id;
      if (paymentsFilters.status) params.status = paymentsFilters.status;
      if (paymentsFilters.payment_method) params.payment_method = paymentsFilters.payment_method;
      if (paymentsFilters.start_date) params.start_date = paymentsFilters.start_date;
      if (paymentsFilters.end_date) params.end_date = paymentsFilters.end_date;

      const data = await adminApi.getPaymentRecords(params);
      setPayments(data.items || []);
      setPaymentsTotal(data.total || 0);
    } catch (err: any) {
      error('加载失败', err.message || '无法获取支付记录');
    } finally {
      setPaymentsLoading(false);
    }
  };

  const handleSearchPayments = () => {
    setPaymentsPage(1);
    loadPayments();
  };

  const handleResetPayments = () => {
    setPaymentsFilters({ user_id: '', status: '', payment_method: '', start_date: '', end_date: '' });
    setPaymentsPage(1);
    setTimeout(() => loadPayments(), 0);
  };

  const handleUpdatePaymentStatus = async () => {
    if (!newPaymentStatus) {
      error('更新失败', '请选择新状态');
      return;
    }

    try {
      setActionLoading(true);
      await adminApi.updatePaymentStatus(paymentStatusUpdateData.id, newPaymentStatus, newTransactionId || undefined);
      success('更新成功', '支付状态已更新');
      setShowPaymentStatusModal(false);
      setNewPaymentStatus('');
      setNewTransactionId('');
      loadPayments();
    } catch (err: any) {
      error('更新失败', err.message || '操作失败');
    } finally {
      setActionLoading(false);
    }
  };

  // ==================== 渲染 ====================

  if (loading && activeTab === 'plans') {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-slate-400">加载中...</div>
      </div>
    );
  }

  return (
    <AdminLayout>
      {/* Header */}
      <div className="bg-white px-6 py-4 flex items-center justify-between shadow-sm">
        <div>
          <h1 className="text-lg font-bold text-slate-900">订阅管理</h1>
          <p className="text-sm text-slate-400 mt-1">管理订阅套餐、用户订阅记录和支付记录</p>
        </div>
        {activeTab === 'plans' && (
          <Button onClick={handleOpenCreate} className="flex items-center gap-2">
            <Plus className="w-4 h-4" />
            新增套餐
          </Button>
        )}
      </div>

      {/* Tab 切换 */}
      <div className="bg-white px-6 border-b border-slate-200">
        <div className="flex gap-6">
          <button
            onClick={() => setActiveTab('plans')}
            className={`pb-3 px-1 border-b-2 transition-colors ${
              activeTab === 'plans'
                ? 'border-indigo-600 text-indigo-600 font-medium'
                : 'border-transparent text-slate-500 hover:text-slate-700'
            }`}
          >
            套餐管理
          </button>
          <button
            onClick={() => setActiveTab('subscriptions')}
            className={`pb-3 px-1 border-b-2 transition-colors ${
              activeTab === 'subscriptions'
                ? 'border-indigo-600 text-indigo-600 font-medium'
                : 'border-transparent text-slate-500 hover:text-slate-700'
            }`}
          >
            订阅记录
          </button>
          <button
            onClick={() => setActiveTab('payments')}
            className={`pb-3 px-1 border-b-2 transition-colors ${
              activeTab === 'payments'
                ? 'border-indigo-600 text-indigo-600 font-medium'
                : 'border-transparent text-slate-500 hover:text-slate-700'
            }`}
          >
            支付记录
          </button>
        </div>
      </div>

      <div className="p-6">
        {/* ==================== 套餐管理 Tab ==================== */}
        {activeTab === 'plans' && (
          <>
            <Card className="overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider">
                    <th className="px-6 py-3 text-left">套餐名称</th>
                    <th className="px-6 py-3 text-left">月价（元）</th>
                    <th className="px-6 py-3 text-left">年价（元）</th>
                    <th className="px-6 py-3 text-left">最大门店数</th>
                    <th className="px-6 py-3 text-left">状态</th>
                    <th className="px-6 py-3 text-right">操作</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {plans.map((plan) => (
                    <tr key={plan.id} className="hover:bg-slate-50">
                      <td className="px-6 py-4">
                        <div className="font-medium text-slate-900">{plan.name}</div>
                        {plan.features && plan.features.length > 0 && (
                          <div className="text-xs text-slate-400 mt-1">
                            {plan.features.length} 项功能
                          </div>
                        )}
                      </td>
                      <td className="px-6 py-4 text-slate-600">
                        {plan.price_monthly === 0 ? '免费' : `¥${plan.price_monthly}`}
                      </td>
                      <td className="px-6 py-4 text-slate-600">
                        {plan.price_yearly === 0 ? '免费' : `¥${plan.price_yearly}`}
                      </td>
                      <td className="px-6 py-4 text-slate-600">{plan.max_stores}</td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          plan.is_active
                            ? 'bg-emerald-50 text-emerald-700'
                            : 'bg-slate-100 text-slate-400'
                        }`}>
                          {plan.is_active ? '启用' : '禁用'}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex items-center justify-end gap-2">
                          <button
                            onClick={() => handleToggle(plan)}
                            disabled={actionLoading}
                            className={`p-2 rounded-lg transition-colors ${
                              plan.is_active
                                ? 'text-amber-600 hover:bg-amber-50'
                                : 'text-emerald-600 hover:bg-emerald-50'
                            }`}
                            title={plan.is_active ? '禁用' : '启用'}
                          >
                            {plan.is_active ? <X className="w-4 h-4" /> : <Check className="w-4 h-4" />}
                          </button>
                          <button
                            onClick={() => handleOpenEdit(plan)}
                            disabled={actionLoading}
                            className="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                            title="编辑"
                          >
                            <Pencil className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => handleDelete(plan)}
                            disabled={actionLoading}
                            className="p-2 text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                            title="删除"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {plans.length === 0 && (
                <div className="text-center py-12 text-slate-400">
                  <AlertTriangle className="w-12 h-12 mx-auto mb-4 text-slate-300" />
                  <p>暂无套餐数据</p>
                  <p className="text-sm mt-1">点击"新增套餐"创建第一个套餐</p>
                </div>
              )}
            </Card>

            {/* Create/Edit Modal */}
            {showModal && (
              <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={handleCloseModal}>
                <div
                  className="bg-white rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto m-4"
                  onClick={(e) => e.stopPropagation()}
                >
                  <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
                    <h2 className="text-lg font-bold text-slate-900">
                      {editingPlan ? '编辑套餐' : '新增套餐'}
                    </h2>
                    <button onClick={handleCloseModal} className="text-slate-400 hover:text-slate-600">
                      <X className="w-5 h-5" />
                    </button>
                  </div>

                  <div className="p-6 space-y-4">
                    {/* Name */}
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-1">套餐名称</label>
                      <input
                        type="text"
                        value={formData.name}
                        onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                        className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        placeholder="例如：标准版"
                      />
                    </div>

                    {/* Prices */}
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">月价格（元）</label>
                        <input
                          type="number"
                          min="0"
                          step="0.01"
                          value={formData.price_monthly}
                          onChange={(e) => setFormData(prev => ({ ...prev, price_monthly: parseFloat(e.target.value) || 0 }))}
                          className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">年价格（元）</label>
                        <input
                          type="number"
                          min="0"
                          step="0.01"
                          value={formData.price_yearly}
                          onChange={(e) => setFormData(prev => ({ ...prev, price_yearly: parseFloat(e.target.value) || 0 }))}
                          className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        />
                      </div>
                    </div>

                    {/* Max Stores */}
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-1">最大门店数</label>
                      <input
                        type="number"
                        min="1"
                        value={formData.max_stores}
                        onChange={(e) => setFormData(prev => ({ ...prev, max_stores: parseInt(e.target.value) || 1 }))}
                        className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>

                    {/* Max Reviews */}
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-1">每月最大评论数（留空表示无限制）</label>
                      <input
                        type="number"
                        min="0"
                        value={formData.max_reviews_per_month || ''}
                        onChange={(e) => setFormData(prev => ({
                          ...prev,
                          max_reviews_per_month: e.target.value ? parseInt(e.target.value) : undefined
                        }))}
                        className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        placeholder="无限制"
                      />
                    </div>

                    {/* Features */}
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-1">功能特性</label>
                      <div className="flex gap-2 mb-2">
                        <input
                          type="text"
                          value={featureInput}
                          onChange={(e) => setFeatureInput(e.target.value)}
                          onKeyDown={(e) => e.key === 'Enter' && handleAddFeature()}
                          className="flex-1 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                          placeholder="输入功能特性，按回车添加"
                        />
                        <Button onClick={handleAddFeature} disabled={!featureInput.trim()}>
                          添加
                        </Button>
                      </div>
                      {formData.features.length > 0 && (
                        <div className="space-y-1">
                          {formData.features.map((feature, index) => (
                            <div key={index} className="flex items-center justify-between bg-slate-50 px-3 py-2 rounded-lg text-sm">
                              <span className="text-slate-700">{feature}</span>
                              <button
                                onClick={() => handleRemoveFeature(index)}
                                className="text-rose-500 hover:text-rose-700"
                              >
                                <X className="w-3.5 h-3.5" />
                              </button>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>

                    {/* Is Active */}
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-slate-700">启用状态</span>
                      <button
                        onClick={() => setFormData(prev => ({ ...prev, is_active: !prev.is_active }))}
                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                          formData.is_active ? 'bg-indigo-600' : 'bg-slate-200'
                        }`}
                      >
                        <span
                          className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                            formData.is_active ? 'translate-x-6' : 'translate-x-1'
                          }`}
                        />
                      </button>
                    </div>
                  </div>

                  <div className="px-6 py-4 border-t border-slate-100 flex justify-end gap-3">
                    <Button variant="outline" onClick={handleCloseModal}>
                      取消
                    </Button>
                    <Button onClick={handleSave} disabled={actionLoading}>
                      {actionLoading ? (
                        <>
                          <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                          保存中...
                        </>
                      ) : (
                        '保存'
                      )}
                    </Button>
                  </div>
                </div>
              </div>
            )}
          </>
        )}

        {/* ==================== 订阅记录 Tab ==================== */}
        {activeTab === 'subscriptions' && (
          <>
            {/* 筛选区 */}
            <Card className="p-4 mb-6">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">用户搜索</label>
                  <input
                    type="text"
                    value={subscriptionsFilters.user_id}
                    onChange={(e) => setSubscriptionsFilters(prev => ({ ...prev, user_id: e.target.value }))}
                    className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    placeholder="用户名/邮箱"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">状态</label>
                  <select
                    value={subscriptionsFilters.status}
                    onChange={(e) => setSubscriptionsFilters(prev => ({ ...prev, status: e.target.value }))}
                    className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="">全部</option>
                    <option value="trial">试用</option>
                    <option value="active">活跃</option>
                    <option value="expired">已过期</option>
                    <option value="cancelled">已取消</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">套餐</label>
                  <select
                    value={subscriptionsFilters.plan_id}
                    onChange={(e) => setSubscriptionsFilters(prev => ({ ...prev, plan_id: e.target.value }))}
                    className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="">全部</option>
                    {plans.map(plan => (
                      <option key={plan.id} value={plan.id}>{plan.name}</option>
                    ))}
                  </select>
                </div>
                <div className="flex items-end gap-2">
                  <Button onClick={handleSearchSubscriptions} className="flex-1">
                    <Search className="w-4 h-4 mr-2" />
                    搜索
                  </Button>
                  <Button variant="outline" onClick={handleResetSubscriptions}>
                    重置
                  </Button>
                </div>
              </div>
            </Card>

            {/* 订阅记录表格 */}
            <Card className="overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider">
                    <th className="px-6 py-3 text-left">用户</th>
                    <th className="px-6 py-3 text-left">套餐</th>
                    <th className="px-6 py-3 text-left">状态</th>
                    <th className="px-6 py-3 text-left">开始日期</th>
                    <th className="px-6 py-3 text-left">结束日期</th>
                    <th className="px-6 py-3 text-left">自动续费</th>
                    <th className="px-6 py-3 text-right">操作</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {subscriptions.map((sub) => (
                    <tr key={sub.id} className="hover:bg-slate-50">
                      <td className="px-6 py-4">
                        <div className="font-medium text-slate-900">{sub.user?.username || '未知'}</div>
                        <div className="text-xs text-slate-400">{sub.user?.email || ''}</div>
                      </td>
                      <td className="px-6 py-4 text-slate-600">
                        {sub.plan?.name || '未知套餐'}
                      </td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          sub.status === 'active' ? 'bg-emerald-50 text-emerald-700' :
                          sub.status === 'trial' ? 'bg-slate-100 text-slate-400' :
                          sub.status === 'expired' ? 'bg-amber-50 text-amber-700' :
                          'bg-rose-50 text-rose-700'
                        }`}>
                          {sub.status === 'active' ? '活跃' :
                           sub.status === 'trial' ? '试用' :
                           sub.status === 'expired' ? '已过期' :
                           '已取消'}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-slate-600">{sub.start_date || '-'}</td>
                      <td className="px-6 py-4 text-slate-600">{sub.end_date || '-'}</td>
                      <td className="px-6 py-4">
                        {sub.auto_renew ? (
                          <CheckCircle className="w-5 h-5 text-emerald-600" />
                        ) : (
                          <XCircle className="w-5 h-5 text-slate-400" />
                        )}
                      </td>
                      <td className="px-6 py-4 text-right">
                        <button
                          onClick={() => {
                            setStatusUpdateData({ id: sub.id, currentStatus: sub.status });
                            setShowStatusModal(true);
                          }}
                          className="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                          title="修改状态"
                        >
                          <Pencil className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {subscriptions.length === 0 && !subscriptionsLoading && (
                <div className="text-center py-12 text-slate-400">
                  <AlertTriangle className="w-12 h-12 mx-auto mb-4 text-slate-300" />
                  <p>暂无订阅记录</p>
                </div>
              )}

              {subscriptionsLoading && (
                <div className="text-center py-12 text-slate-400">
                  <Loader2 className="w-8 h-8 mx-auto animate-spin" />
                </div>
              )}

              {/* 分页 */}
              {subscriptionsTotal > subscriptionsPageSize && (
                <div className="px-6 py-4 border-t border-slate-100 flex items-center justify-between">
                  <div className="text-sm text-slate-500">
                    共 {subscriptionsTotal} 条记录
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      onClick={() => setSubscriptionsPage(prev => Math.max(1, prev - 1))}
                      disabled={subscriptionsPage === 1}
                    >
                      上一页
                    </Button>
                    <span className="text-sm text-slate-600">第 {subscriptionsPage} 页</span>
                    <Button
                      variant="outline"
                      onClick={() => setSubscriptionsPage(prev => prev + 1)}
                      disabled={subscriptionsPage * subscriptionsPageSize >= subscriptionsTotal}
                    >
                      下一页
                    </Button>
                  </div>
                </div>
              )}
            </Card>

            {/* 修改状态模态框 */}
            {showStatusModal && (
              <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={() => setShowStatusModal(false)}>
                <div
                  className="bg-white rounded-2xl w-full max-w-md m-4 p-6"
                  onClick={(e) => e.stopPropagation()}
                >
                  <h3 className="text-lg font-bold text-slate-900 mb-4">修改订阅状态</h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-1">当前状态</label>
                      <div className="text-sm text-slate-600">{statusUpdateData.currentStatus}</div>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-1">新状态</label>
                      <select
                        value={newStatus}
                        onChange={(e) => setNewStatus(e.target.value)}
                        className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      >
                        <option value="">请选择</option>
                        <option value="trial">试用</option>
                        <option value="active">活跃</option>
                        <option value="expired">已过期</option>
                        <option value="cancelled">已取消</option>
                      </select>
                    </div>
                  </div>
                  <div className="mt-6 flex justify-end gap-3">
                    <Button variant="outline" onClick={() => setShowStatusModal(false)}>
                      取消
                    </Button>
                    <Button onClick={handleUpdateStatus} disabled={actionLoading}>
                      {actionLoading ? (
                        <>
                          <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                          更新中...
                        </>
                      ) : (
                        '确认更新'
                      )}
                    </Button>
                  </div>
                </div>
              </div>
            )}
          </>
        )}

        {/* ==================== 支付记录 Tab ==================== */}
        {activeTab === 'payments' && (
          <>
            {/* 筛选区 */}
            <Card className="p-4 mb-6">
              <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">用户搜索</label>
                  <input
                    type="text"
                    value={paymentsFilters.user_id}
                    onChange={(e) => setPaymentsFilters(prev => ({ ...prev, user_id: e.target.value }))}
                    className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    placeholder="用户名/邮箱"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">支付状态</label>
                  <select
                    value={paymentsFilters.status}
                    onChange={(e) => setPaymentsFilters(prev => ({ ...prev, status: e.target.value }))}
                    className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="">全部</option>
                    <option value="pending">待支付</option>
                    <option value="success">成功</option>
                    <option value="failed">失败</option>
                    <option value="refunded">已退款</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">支付方式</label>
                  <select
                    value={paymentsFilters.payment_method}
                    onChange={(e) => setPaymentsFilters(prev => ({ ...prev, payment_method: e.target.value }))}
                    className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="">全部</option>
                    <option value="wechat">微信支付</option>
                    <option value="alipay">支付宝</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">开始日期</label>
                  <input
                    type="date"
                    value={paymentsFilters.start_date}
                    onChange={(e) => setPaymentsFilters(prev => ({ ...prev, start_date: e.target.value }))}
                    className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">结束日期</label>
                  <input
                    type="date"
                    value={paymentsFilters.end_date}
                    onChange={(e) => setPaymentsFilters(prev => ({ ...prev, end_date: e.target.value }))}
                    className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              </div>
              <div className="mt-4 flex gap-2">
                <Button onClick={handleSearchPayments}>
                  <Search className="w-4 h-4 mr-2" />
                  搜索
                </Button>
                <Button variant="outline" onClick={handleResetPayments}>
                  重置
                </Button>
              </div>
            </Card>

            {/* 支付记录表格 */}
            <Card className="overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider">
                    <th className="px-6 py-3 text-left">用户</th>
                    <th className="px-6 py-3 text-left">套餐</th>
                    <th className="px-6 py-3 text-left">金额</th>
                    <th className="px-6 py-3 text-left">支付方式</th>
                    <th className="px-6 py-3 text-left">状态</th>
                    <th className="px-6 py-3 text-left">交易流水号</th>
                    <th className="px-6 py-3 text-left">支付时间</th>
                    <th className="px-6 py-3 text-right">操作</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {payments.map((payment) => (
                    <tr key={payment.id} className="hover:bg-slate-50">
                      <td className="px-6 py-4">
                        <div className="font-medium text-slate-900">{payment.user?.username || '未知'}</div>
                        <div className="text-xs text-slate-400">{payment.user?.email || ''}</div>
                      </td>
                      <td className="px-6 py-4 text-slate-600">
                        {payment.plan?.name || '-'}
                      </td>
                      <td className="px-6 py-4 text-slate-600 font-medium">¥{payment.amount}</td>
                      <td className="px-6 py-4">
                        {payment.payment_method === 'wechat' ? (
                          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700">
                            微信支付
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700">
                            支付宝
                          </span>
                        )}
                      </td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          payment.status === 'success' ? 'bg-emerald-50 text-emerald-700' :
                          payment.status === 'pending' ? 'bg-amber-50 text-amber-700' :
                          payment.status === 'failed' ? 'bg-rose-50 text-rose-700' :
                          'bg-slate-100 text-slate-400'
                        }`}>
                          {payment.status === 'success' ? '成功' :
                           payment.status === 'pending' ? '待支付' :
                           payment.status === 'failed' ? '失败' :
                           '已退款'}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-slate-600 font-mono text-xs">
                        {payment.transaction_id || '-'}
                      </td>
                      <td className="px-6 py-4 text-slate-600">
                        {payment.paid_at ? new Date(payment.paid_at).toLocaleString('zh-CN') : '-'}
                      </td>
                      <td className="px-6 py-4 text-right">
                        <button
                          onClick={() => {
                            setPaymentStatusUpdateData({
                              id: payment.id,
                              currentStatus: payment.status,
                              transaction_id: payment.transaction_id || '',
                            });
                            setShowPaymentStatusModal(true);
                          }}
                          className="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                          title="修改状态"
                        >
                          <Pencil className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {payments.length === 0 && !paymentsLoading && (
                <div className="text-center py-12 text-slate-400">
                  <AlertTriangle className="w-12 h-12 mx-auto mb-4 text-slate-300" />
                  <p>暂无支付记录</p>
                </div>
              )}

              {paymentsLoading && (
                <div className="text-center py-12 text-slate-400">
                  <Loader2 className="w-8 h-8 mx-auto animate-spin" />
                </div>
              )}

              {/* 分页 */}
              {paymentsTotal > paymentsPageSize && (
                <div className="px-6 py-4 border-t border-slate-100 flex items-center justify-between">
                  <div className="text-sm text-slate-500">
                    共 {paymentsTotal} 条记录
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      onClick={() => setPaymentsPage(prev => Math.max(1, prev - 1))}
                      disabled={paymentsPage === 1}
                    >
                      上一页
                    </Button>
                    <span className="text-sm text-slate-600">第 {paymentsPage} 页</span>
                    <Button
                      variant="outline"
                      onClick={() => setPaymentsPage(prev => prev + 1)}
                      disabled={paymentsPage * paymentsPageSize >= paymentsTotal}
                    >
                      下一页
                    </Button>
                  </div>
                </div>
              )}
            </Card>

            {/* 修改支付状态模态框 */}
            {showPaymentStatusModal && (
              <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={() => setShowPaymentStatusModal(false)}>
                <div
                  className="bg-white rounded-2xl w-full max-w-md m-4 p-6"
                  onClick={(e) => e.stopPropagation()}
                >
                  <h3 className="text-lg font-bold text-slate-900 mb-4">修改支付状态</h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-1">当前状态</label>
                      <div className="text-sm text-slate-600">{paymentStatusUpdateData.currentStatus}</div>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-1">新状态</label>
                      <select
                        value={newPaymentStatus}
                        onChange={(e) => setNewPaymentStatus(e.target.value)}
                        className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      >
                        <option value="">请选择</option>
                        <option value="pending">待支付</option>
                        <option value="success">成功</option>
                        <option value="failed">失败</option>
                        <option value="refunded">已退款</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-1">交易流水号（可选）</label>
                      <input
                        type="text"
                        value={newTransactionId}
                        onChange={(e) => setNewTransactionId(e.target.value)}
                        className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        placeholder="输入交易流水号"
                      />
                    </div>
                  </div>
                  <div className="mt-6 flex justify-end gap-3">
                    <Button variant="outline" onClick={() => setShowPaymentStatusModal(false)}>
                      取消
                    </Button>
                    <Button onClick={handleUpdatePaymentStatus} disabled={actionLoading}>
                      {actionLoading ? (
                        <>
                          <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                          更新中...
                        </>
                      ) : (
                        '确认更新'
                      )}
                    </Button>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </AdminLayout>
  );
};

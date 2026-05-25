import React, { useState, useEffect } from 'react';
import { Plus, Pencil, Trash2, Check, X, AlertTriangle, Loader2 } from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';
import { subscriptionApi, SubscriptionPlan } from '../../api/subscription';
import { AdminLayout } from '../../components/AdminLayout';

export const SubscriptionManagement: React.FC = () => {
  const { success, error } = useToast();

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

  // 加载套餐列表
  useEffect(() => {
    loadPlans();
  }, []);

  const loadPlans = async () => {
    try {
      setLoading(true);
      const data = await subscriptionApi.getAllPlans();
      setPlans(data);
    } catch (err: any) {
      error('加载失败', err.message || '无法获取套餐列表');
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

  if (loading) {
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
          <h1 className="text-lg font-bold text-slate-900">订阅套餐管理</h1>
          <p className="text-sm text-slate-400 mt-1">管理所有订阅套餐</p>
        </div>
        <Button onClick={handleOpenCreate} className="flex items-center gap-2">
          <Plus className="w-4 h-4" />
          新增套餐
        </Button>
      </div>

      <div className="p-6">
        {/* Plans Table */}
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
      </div>

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
    </AdminLayout>
  );
};

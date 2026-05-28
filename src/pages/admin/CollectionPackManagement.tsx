import React, { useState, useEffect } from 'react';
import { Plus, Pencil, Trash2, X, Loader2, Database, Search, Filter, AlertCircle } from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';
import { collectionPackApi, CollectionPack, CollectionOrder } from '../../api/collectionPack';
import { AdminLayout } from '../../components/AdminLayout';

export const CollectionPackManagement: React.FC = () => {
  const { success, error } = useToast();

  // Tab 状态
  const [activeTab, setActiveTab] = useState<'packs' | 'orders'>('packs');

  // ==================== 套餐管理状态 ====================
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [packs, setPacks] = useState<CollectionPack[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [editingPack, setEditingPack] = useState<CollectionPack | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    credit_amount: 0,
    price: 0,
    description: '',
    is_active: true,
  });

  // ==================== 订单管理状态 ====================
  const [ordersLoading, setOrdersLoading] = useState(false);
  const [orders, setOrders] = useState<CollectionOrder[]>([]);
  const [ordersTotal, setOrdersTotal] = useState(0);
  const [ordersPage, setOrdersPage] = useState(1);
  const [ordersPageSize] = useState(20);
  const [ordersFilters, setOrdersFilters] = useState({
    user_id: '',
    status: '',
  });
  const [showStatusModal, setShowStatusModal] = useState(false);
  const [statusUpdateData, setStatusUpdateData] = useState<{ id: string; currentStatus: string }>({ id: '', currentStatus: '' });
  const [newStatus, setNewStatus] = useState('');

  // ==================== 套餐管理函数 ====================

  const loadPacks = async () => {
    try {
      setLoading(true);
      const data = await collectionPackApi.admin.getPacks();
      setPacks(Array.isArray(data) ? data : []);
    } catch (err: any) {
      error('加载失败', err.message || '无法获取套餐列表');
      setPacks([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeTab === 'packs') {
      loadPacks();
    }
  }, [activeTab]);

  const handleOpenCreate = () => {
    setEditingPack(null);
    setFormData({ name: '', credit_amount: 0, price: 0, description: '', is_active: true });
    setShowModal(true);
  };

  const handleOpenEdit = (pack: CollectionPack) => {
    setEditingPack(pack);
    setFormData({
      name: pack.name,
      credit_amount: pack.credit_amount,
      price: pack.price,
      description: pack.description || '',
      is_active: pack.is_active,
    });
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingPack(null);
  };

  const handleSave = async () => {
    if (!formData.name) {
      error('保存失败', '请输入套餐名称');
      return;
    }
    if (formData.credit_amount <= 0) {
      error('保存失败', '积分数量必须大于0');
      return;
    }

    try {
      setActionLoading(true);
      if (editingPack) {
        await collectionPackApi.admin.updatePack(editingPack.id, {
          name: formData.name,
          credit_amount: formData.credit_amount,
          price: formData.price,
          description: formData.description || undefined,
          is_active: formData.is_active,
        });
        success('更新成功', `套餐「${formData.name}」已更新`);
      } else {
        await collectionPackApi.admin.createPack({
          name: formData.name,
          credit_amount: formData.credit_amount,
          price: formData.price,
          description: formData.description || undefined,
          is_active: formData.is_active,
        });
        success('创建成功', `套餐「${formData.name}」已创建`);
      }
      handleCloseModal();
      loadPacks();
    } catch (err: any) {
      error('保存失败', err.message || '操作失败');
    } finally {
      setActionLoading(false);
    }
  };

  const handleDelete = async (pack: CollectionPack) => {
    if (!confirm(`确定要删除套餐「${pack.name}」吗？此操作不可恢复。`)) {
      return;
    }
    try {
      setActionLoading(true);
      await collectionPackApi.admin.deletePack(pack.id);
      success('删除成功', `套餐「${pack.name}」已删除`);
      loadPacks();
    } catch (err: any) {
      error('删除失败', err.message || '删除失败');
    } finally {
      setActionLoading(false);
    }
  };

  // ==================== 订单管理函数 ====================

  const loadOrders = async () => {
    try {
      setOrdersLoading(true);
      const res = await collectionPackApi.admin.getOrders({
        ...ordersFilters,
        page: ordersPage,
        page_size: ordersPageSize,
      });
      setOrders(res.list || []);
      setOrdersTotal(res.total || 0);
    } catch (err: any) {
      error('加载失败', err.message || '无法获取订单列表');
    } finally {
      setOrdersLoading(false);
    }
  };

  useEffect(() => {
    if (activeTab === 'orders') {
      loadOrders();
    }
  }, [activeTab, ordersPage]);

  const handleSearchOrders = () => {
    setOrdersPage(1);
    loadOrders();
  };

  const handleResetOrders = () => {
    setOrdersFilters({ user_id: '', status: '' });
    setOrdersPage(1);
    setTimeout(() => loadOrders(), 0);
  };

  const handleUpdateStatus = async () => {
    if (!newStatus) {
      error('更新失败', '请选择新状态');
      return;
    }
    try {
      setActionLoading(true);
      await collectionPackApi.admin.updateOrderStatus(statusUpdateData.id, newStatus);
      success('更新成功', '订单状态已更新');
      setShowStatusModal(false);
      setNewStatus('');
      loadOrders();
    } catch (err: any) {
      error('更新失败', err.message || '操作失败');
    } finally {
      setActionLoading(false);
    }
  };

  // ==================== 渲染 ====================

  return (
    <AdminLayout>
      {/* Header */}
      <div className="bg-white px-6 py-4 flex items-center justify-between shadow-sm">
        <div>
          <h1 className="text-lg font-bold text-slate-900">采集套餐管理</h1>
          <p className="text-sm text-slate-400 mt-1">管理采集积分套餐和购买订单</p>
        </div>
        {activeTab === 'packs' && (
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
            onClick={() => setActiveTab('packs')}
            className={`pb-3 px-1 border-b-2 transition-colors ${
              activeTab === 'packs'
                ? 'border-indigo-600 text-indigo-600 font-medium'
                : 'border-transparent text-slate-500 hover:text-slate-700'
            }`}
          >
            套餐管理
          </button>
          <button
            onClick={() => setActiveTab('orders')}
            className={`pb-3 px-1 border-b-2 transition-colors ${
              activeTab === 'orders'
                ? 'border-indigo-600 text-indigo-600 font-medium'
                : 'border-transparent text-slate-500 hover:text-slate-700'
            }`}
          >
            订单管理
          </button>
        </div>
      </div>

      <div className="p-6">
        {/* ==================== 套餐管理 Tab ==================== */}
        {activeTab === 'packs' && (
          <>
            <Card className="overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider">
                    <th className="px-6 py-3 text-left">套餐名称</th>
                    <th className="px-6 py-3 text-left">积分数量</th>
                    <th className="px-6 py-3 text-left">价格（元）</th>
                    <th className="px-6 py-3 text-left">状态</th>
                    <th className="px-6 py-3 text-right">操作</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {packs.map((pack) => (
                    <tr key={pack.id} className="hover:bg-slate-50">
                      <td className="px-6 py-4">
                        <div className="font-medium text-slate-900">{pack.name}</div>
                        {pack.description && (
                          <div className="text-xs text-slate-400 mt-1">{pack.description}</div>
                        )}
                      </td>
                      <td className="px-6 py-4 text-slate-600">
                        {pack.credit_amount?.toLocaleString()} 条
                      </td>
                      <td className="px-6 py-4 text-slate-600 font-medium">
                        ¥{pack.price}
                      </td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          pack.is_active
                            ? 'bg-emerald-50 text-emerald-700'
                            : 'bg-slate-100 text-slate-400'
                        }`}>
                          {pack.is_active ? '启用' : '禁用'}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex items-center justify-end gap-2">
                          <button
                            onClick={() => handleOpenEdit(pack)}
                            disabled={actionLoading}
                            className="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                            title="编辑"
                          >
                            <Pencil className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => handleDelete(pack)}
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

              {packs.length === 0 && !loading && (
                <div className="text-center py-12 text-slate-400">
                  <AlertCircle className="w-12 h-12 mx-auto mb-4 text-slate-300" />
                  <p>暂无套餐数据</p>
                  <p className="text-sm mt-1">点击"新增套餐"创建第一个采集套餐</p>
                </div>
              )}

              {loading && (
                <div className="text-center py-12 text-slate-400">
                  <Loader2 className="w-8 h-8 mx-auto animate-spin" />
                </div>
              )}
            </Card>

            {/* 新建/编辑 Modal */}
            {showModal && (
              <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={handleCloseModal}>
                <div
                  className="bg-white rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto m-4"
                  onClick={(e) => e.stopPropagation()}
                >
                  <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
                    <h2 className="text-lg font-bold text-slate-900">
                      {editingPack ? '编辑套餐' : '新增套餐'}
                    </h2>
                    <button onClick={handleCloseModal} className="text-slate-400 hover:text-slate-600">
                      <X className="w-5 h-5" />
                    </button>
                  </div>

                  <div className="p-6 space-y-4">
                    {/* 名称 */}
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-1">套餐名称</label>
                      <input
                        type="text"
                        value={formData.name}
                        onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                        className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        placeholder="例如：500条采集包"
                      />
                    </div>

                    {/* 积分数量 */}
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-1">积分数量（条）</label>
                      <input
                        type="number"
                        min="1"
                        value={formData.credit_amount}
                        onChange={(e) => setFormData(prev => ({ ...prev, credit_amount: parseInt(e.target.value) || 0 }))}
                        className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>

                    {/* 价格 */}
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-1">价格（元）</label>
                      <input
                        type="number"
                        min="0"
                        step="0.01"
                        value={formData.price}
                        onChange={(e) => setFormData(prev => ({ ...prev, price: parseFloat(e.target.value) || 0 }))}
                        className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        placeholder="0表示免费"
                      />
                    </div>

                    {/* 描述 */}
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-1">描述（可选）</label>
                      <input
                        type="text"
                        value={formData.description}
                        onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                        className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        placeholder="套餐描述"
                      />
                    </div>

                    {/* 启用状态 */}
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

        {/* ==================== 订单管理 Tab ==================== */}
        {activeTab === 'orders' && (
          <>
            {/* 筛选区 */}
            <Card className="p-4 mb-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">用户ID</label>
                  <input
                    type="text"
                    value={ordersFilters.user_id}
                    onChange={(e) => setOrdersFilters(prev => ({ ...prev, user_id: e.target.value }))}
                    className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    placeholder="输入用户ID"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">状态</label>
                  <select
                    value={ordersFilters.status}
                    onChange={(e) => setOrdersFilters(prev => ({ ...prev, status: e.target.value }))}
                    className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="">全部</option>
                    <option value="pending">待支付</option>
                    <option value="success">成功</option>
                    <option value="failed">失败</option>
                  </select>
                </div>
                <div className="flex items-end gap-2">
                  <Button onClick={handleSearchOrders} className="flex-1">
                    <Search className="w-4 h-4 mr-2" />
                    搜索
                  </Button>
                  <Button variant="outline" onClick={handleResetOrders}>
                    重置
                  </Button>
                </div>
              </div>
            </Card>

            {/* 订单表格 */}
            <Card className="overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider">
                    <th className="px-6 py-3 text-left">用户</th>
                    <th className="px-6 py-3 text-left">套餐</th>
                    <th className="px-6 py-3 text-left">积分数量</th>
                    <th className="px-6 py-3 text-left">金额</th>
                    <th className="px-6 py-3 text-left">状态</th>
                    <th className="px-6 py-3 text-left">创建时间</th>
                    <th className="px-6 py-3 text-right">操作</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {orders.map((order) => (
                    <tr key={order.id} className="hover:bg-slate-50">
                      <td className="px-6 py-4">
                        <div className="font-medium text-slate-900">{order.user_name || order.user_id?.slice(0, 8)}</div>
                        <div className="text-xs text-slate-400">{order.email || ''}</div>
                      </td>
                      <td className="px-6 py-4 text-slate-600">{order.pack_name || '-'}</td>
                      <td className="px-6 py-4 text-slate-600">{order.credit_amount?.toLocaleString()} 条</td>
                      <td className="px-6 py-4 text-slate-600 font-medium">¥{order.amount}</td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          order.status === 'success' ? 'bg-emerald-50 text-emerald-700' :
                          order.status === 'pending' ? 'bg-amber-50 text-amber-700' :
                          'bg-rose-50 text-rose-700'
                        }`}>
                          {order.status === 'success' ? '成功' :
                           order.status === 'pending' ? '待支付' : '失败'}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-slate-600 text-xs">
                        {order.created_at ? new Date(order.created_at).toLocaleString('zh-CN') : '-'}
                      </td>
                      <td className="px-6 py-4 text-right">
                        <button
                          onClick={() => {
                            setStatusUpdateData({ id: order.id, currentStatus: order.status });
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

              {orders.length === 0 && !ordersLoading && (
                <div className="text-center py-12 text-slate-400">
                  <AlertCircle className="w-12 h-12 mx-auto mb-4 text-slate-300" />
                  <p>暂无订单数据</p>
                </div>
              )}

              {ordersLoading && (
                <div className="text-center py-12 text-slate-400">
                  <Loader2 className="w-8 h-8 mx-auto animate-spin" />
                </div>
              )}

              {/* 分页 */}
              {ordersTotal > ordersPageSize && (
                <div className="px-6 py-4 border-t border-slate-100 flex items-center justify-between">
                  <div className="text-sm text-slate-500">
                    共 {ordersTotal} 条记录
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      onClick={() => setOrdersPage(prev => Math.max(1, prev - 1))}
                      disabled={ordersPage === 1}
                    >
                      上一页
                    </Button>
                    <span className="text-sm text-slate-600">第 {ordersPage} 页</span>
                    <Button
                      variant="outline"
                      onClick={() => setOrdersPage(prev => prev + 1)}
                      disabled={ordersPage * ordersPageSize >= ordersTotal}
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
                  <h3 className="text-lg font-bold text-slate-900 mb-4">修改订单状态</h3>
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
                        <option value="pending">待支付</option>
                        <option value="success">成功</option>
                        <option value="failed">失败</option>
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
      </div>
    </AdminLayout>
  );
};

import React, { useState, useEffect } from 'react';
import { Store, Search, Plus, MapPin, Phone, Edit, Trash2, Users, RefreshCw, AlertCircle, UserPlus, X } from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { AdminLayout } from '../../components/AdminLayout';
import { useToast } from '../../hooks/use-toast';
import { storesApi } from '../../api/stores';
import { adminApi } from '../../api/admin';
import type { Store as StoreType } from '../../api/stores';
import type { AdminUser } from '../../api/admin';

export const StoreManagement: React.FC = () => {
  const [stores, setStores] = useState<StoreType[]>([]);
  const [allUsers, setAllUsers] = useState<AdminUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [showAdd, setShowAdd] = useState(false);
  const [showEdit, setShowEdit] = useState(false);
  const [showUsers, setShowUsers] = useState(false);
  const [editingStore, setEditingStore] = useState<StoreType | null>(null);
  const [selectedUserIds, setSelectedUserIds] = useState<string[]>([]);
  const [selectedStoreForUsers, setSelectedStoreForUsers] = useState<StoreType | null>(null);
  const [newStore, setNewStore] = useState({ name: '', type: 'restaurant', address: '', phone: '', owner_name: '' });
  const [editData, setEditData] = useState({ name: '', type: 'restaurant', address: '', phone: '', owner_name: '' });

  const { success, error: toastError } = useToast();

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [st, us] = await Promise.allSettled([
        storesApi.getStores({ page_size: 100 }).catch(err => { console.warn('[StoreMgmt] 门店获取失败:', err); return { items: [] }; }),
        adminApi.getAdminUsers().catch(err => { console.warn('[StoreMgmt] 用户获取失败:', err); return []; }),
      ]);
      if (st.status === 'fulfilled') setStores((st.value as any)?.items || st.value || []);
      if (us.status === 'fulfilled') setAllUsers(Array.isArray(us.value) ? us.value.map(u => ({ ...u, assignedStores: u.assignedStores || (u as any).assigned_stores || [] })) : []);
    } catch (err) {
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally { setLoading(false); }
  };

  useEffect(() => { loadData(); }, []);

  const filteredStores = stores.filter(s =>
    (s.name || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
    (s.address || '').toLowerCase().includes(searchQuery.toLowerCase())
  );

  // 获取该门店下分配的用户
  const getStoreUsers = (storeId: string) => allUsers.filter(u => (u.assignedStores || []).includes(storeId));

  const openUserManager = (store: StoreType) => {
    setSelectedStoreForUsers(store);
    setSelectedUserIds(getStoreUsers(store.id).map(u => u.id));
    setShowUsers(true);
  };

  const handleSaveStoreUsers = async () => {
    if (!selectedStoreForUsers) return;
    try {
      // 更新所有受影响用户的 assignedStores
      for (const user of allUsers) {
        const current = user.assignedStores || [];
        const shouldHave = selectedUserIds.includes(user.id);
        if (shouldHave && !current.includes(selectedStoreForUsers.id)) {
          await adminApi.assignStores(user.id, [...current, selectedStoreForUsers.id]);
        } else if (!shouldHave && current.includes(selectedStoreForUsers.id)) {
          await adminApi.assignStores(user.id, current.filter(sid => sid !== selectedStoreForUsers.id));
        }
      }
      success('分配成功', `已更新 "${selectedStoreForUsers.name}" 的门店用户`);
      setShowUsers(false);
      loadData();
    } catch (err: any) { toastError('分配失败', err.message); }
  };

  const handleAdd = async () => {
    if (!newStore.name) { toastError('添加失败', '请填写门店名称'); return; }
    try {
      await storesApi.createStore(newStore as any);
      success('添加成功', `门店 "${newStore.name}" 已创建`);
      setShowAdd(false);
      setNewStore({ name: '', type: 'restaurant', address: '', phone: '', owner_name: '' });
      loadData();
    } catch (err: any) { toastError('添加失败', err.message); }
  };

  const handleEdit = async () => {
    if (!editingStore) return;
    try {
      await storesApi.updateStore(editingStore.id, editData as any);
      success('更新成功', '门店信息已更新');
      setShowEdit(false);
      loadData();
    } catch (err: any) { toastError('更新失败', err.message); }
  };

  const handleDelete = async (id: string) => {
    try { await storesApi.deleteStore(id); success('已删除', '门店已移除'); loadData(); }
    catch (err: any) { toastError('删除失败', err.message); }
  };

  const openEdit = (s: StoreType) => {
    setEditingStore(s);
    setEditData({ name: s.name, type: s.type || 'restaurant', address: s.address || '', phone: s.phone || '', owner_name: s.owner_name || '' });
    setShowEdit(true);
  };

  const statusBadge = (s: string) => {
    const m: Record<string, { c: string; l: string }> = {
      active: { c: 'bg-emerald-100 text-emerald-700', l: '运行中' },
      pending: { c: 'bg-amber-100 text-amber-700', l: '待审核' },
      inactive: { c: 'bg-slate-100 text-slate-500', l: '已停用' },
    };
    const x = m[s] || { c: 'bg-slate-100 text-slate-500', l: s };
    return <Badge className={x.c}>{x.l}</Badge>;
  };

  if (loading) return <AdminLayout><div className="flex items-center justify-center h-64"><RefreshCw className="w-6 h-6 text-slate-400 animate-spin" /></div></AdminLayout>;
  if (error) return <AdminLayout><div className="flex flex-col items-center justify-center h-64 gap-4"><AlertCircle className="w-10 h-10 text-rose-400" /><p className="text-slate-500">{error}</p><Button variant="outline" onClick={loadData}>重试</Button></div></AdminLayout>;

  return (
    <AdminLayout>
      <div className="space-y-6 pb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">门店管理</h1>
            <p className="text-slate-500 text-sm mt-1">管理所有门店信息、用户权限</p>
          </div>
          <Button onClick={() => setShowAdd(true)}><Plus className="w-4 h-4 mr-1" />新增门店</Button>
        </div>

        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input className="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-sm outline-none" placeholder="搜索门店名称或地址..." value={searchQuery} onChange={e => setSearchQuery(e.target.value)} />
        </div>

        {filteredStores.length === 0 ? (
          <div className="text-center py-16 text-slate-400"><Store className="w-12 h-12 mx-auto mb-3 opacity-30" /><p>{searchQuery ? '无匹配门店' : '暂无门店数据，点击新增'}</p></div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredStores.map(s => {
              const storeUsers = getStoreUsers(s.id);
              return (
                <Card key={s.id} className="p-5 border-slate-100 shadow-sm space-y-3">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-2">
                      <div className="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center"><Store className="w-5 h-5 text-blue-500" /></div>
                      <div>
                        <h3 className="font-bold text-slate-900 text-sm">{s.name}</h3>
                        <p className="text-xs text-slate-400">{s.type || '未知'}</p>
                      </div>
                    </div>
                    {statusBadge(s.status)}
                  </div>
                  <div className="space-y-1 text-xs text-slate-500">
                    {s.address && <p className="flex items-center gap-1"><MapPin className="w-3 h-3" />{s.address}</p>}
                    {s.phone && <p className="flex items-center gap-1"><Phone className="w-3 h-3" />{s.phone}</p>}
                    <p>评论: {s.review_count || 0} · 平台: {s.platform_count || 0}</p>
                    {storeUsers.length > 0 && (
                      <p className="flex items-center gap-1 text-indigo-600 font-medium">
                        <Users className="w-3 h-3" />
                        {storeUsers.map(u => u.username).join(', ')}
                      </p>
                    )}
                  </div>
                  <div className="flex items-center gap-2 pt-1">
                    <Button size="sm" variant="outline" onClick={() => openUserManager(s)}>
                      <Users className="w-3 h-3 mr-1" />用户({storeUsers.length})
                    </Button>
                    <Button size="sm" variant="outline" onClick={() => openEdit(s)}><Edit className="w-3 h-3 mr-1" />编辑</Button>
                    <Button size="sm" variant="ghost" className="text-rose-500" onClick={() => handleDelete(s.id)}><Trash2 className="w-3 h-3" /></Button>
                  </div>
                </Card>
              );
            })}
          </div>
        )}

        {/* Add Dialog */}
        {showAdd && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
            <Card className="w-96 p-6 space-y-4">
              <h3 className="font-bold text-slate-900">新增门店</h3>
              <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="门店名称 *" value={newStore.name} onChange={e => setNewStore(p => ({ ...p, name: e.target.value }))} />
              <select className="w-full p-2.5 border border-slate-200 rounded-lg text-sm" value={newStore.type} onChange={e => setNewStore(p => ({ ...p, type: e.target.value }))}>
                <option value="restaurant">餐饮</option><option value="hotel">酒店</option><option value="beverage">饮品</option>
              </select>
              <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="地址" value={newStore.address} onChange={e => setNewStore(p => ({ ...p, address: e.target.value }))} />
              <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="联系电话" value={newStore.phone} onChange={e => setNewStore(p => ({ ...p, phone: e.target.value }))} />
              <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="负责人" value={newStore.owner_name} onChange={e => setNewStore(p => ({ ...p, owner_name: e.target.value }))} />
              <div className="flex justify-end gap-3"><Button variant="ghost" onClick={() => setShowAdd(false)}>取消</Button><Button className="bg-indigo-500 text-white" onClick={handleAdd}>添加</Button></div>
            </Card>
          </div>
        )}

        {/* Edit Dialog */}
        {showEdit && editingStore && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
            <Card className="w-96 p-6 space-y-4">
              <h3 className="font-bold text-slate-900">编辑门店</h3>
              <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" value={editData.name} onChange={e => setEditData(p => ({ ...p, name: e.target.value }))} />
              <select className="w-full p-2.5 border border-slate-200 rounded-lg text-sm" value={editData.type} onChange={e => setEditData(p => ({ ...p, type: e.target.value }))}>
                <option value="restaurant">餐饮</option><option value="hotel">酒店</option><option value="beverage">饮品</option>
              </select>
              <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" value={editData.address} onChange={e => setEditData(p => ({ ...p, address: e.target.value }))} />
              <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" value={editData.phone} onChange={e => setEditData(p => ({ ...p, phone: e.target.value }))} />
              <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" value={editData.owner_name} onChange={e => setEditData(p => ({ ...p, owner_name: e.target.value }))} />
              <div className="flex justify-end gap-3"><Button variant="ghost" onClick={() => setShowEdit(false)}>取消</Button><Button className="bg-indigo-500 text-white" onClick={handleEdit}>保存</Button></div>
            </Card>
          </div>
        )}

        {/* User Assignment Dialog */}
        {showUsers && selectedStoreForUsers && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
            <Card className="w-[500px] max-h-[600px] p-6 space-y-4 flex flex-col">
              <div className="flex items-center justify-between">
                <h3 className="font-bold text-slate-900">门店用户 - {selectedStoreForUsers.name}</h3>
                <Button variant="ghost" size="sm" onClick={() => setShowUsers(false)}><X className="w-4 h-4" /></Button>
              </div>
              <p className="text-sm text-slate-500">勾选可管理此门店的用户</p>
              <div className="flex-1 overflow-y-auto space-y-2">
                {allUsers.length === 0 ? (
                  <p className="text-center py-8 text-slate-400">暂无管理员用户，请先在权限管理中添加</p>
                ) : allUsers.map(u => (
                  <label key={u.id} className={`flex items-center gap-3 p-3 rounded-xl border cursor-pointer transition-colors ${selectedUserIds.includes(u.id) ? 'border-indigo-300 bg-indigo-50' : 'border-slate-100 hover:border-slate-200'}`}>
                    <input type="checkbox" checked={selectedUserIds.includes(u.id)} onChange={() => setSelectedUserIds(prev => prev.includes(u.id) ? prev.filter(id => id !== u.id) : [...prev, u.id])} className="w-4 h-4 rounded border-slate-300 text-indigo-500" />
                    <div>
                      <p className="text-sm font-medium text-slate-900">{u.username}</p>
                      <p className="text-xs text-slate-400">{u.phone || ''} · {u.role}</p>
                    </div>
                  </label>
                ))}
              </div>
              <div className="flex justify-end gap-3 pt-2 border-t border-slate-100">
                <Button variant="ghost" onClick={() => setShowUsers(false)}>取消</Button>
                <Button className="bg-indigo-500 text-white" onClick={handleSaveStoreUsers}>保存</Button>
              </div>
            </Card>
          </div>
        )}
      </div>
    </AdminLayout>
  );
};

import React, { useState, useEffect } from 'react';
import { Shield, Search, Plus, Users, UserPlus, XCircle, CheckCircle, RefreshCw, AlertCircle, Store, Settings } from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { AdminLayout } from '../../components/AdminLayout';
import { useToast } from '../../hooks/use-toast';
import { adminApi, AdminUser, Role } from '../../api/admin';
import { storesApi } from '../../api/stores';
import type { Store as StoreType } from '../../api/stores';

export const PermissionManagement: React.FC = () => {
  const [tab, setTab] = useState<'users' | 'roles'>('users');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [admins, setAdmins] = useState<AdminUser[]>([]);
  const [roles, setRoles] = useState<Role[]>([]);
  const [allStores, setAllStores] = useState<StoreType[]>([]);
  const [showAdd, setShowAdd] = useState(false);
  const [showStoreAssign, setShowStoreAssign] = useState(false);
  const [selectedUser, setSelectedUser] = useState<AdminUser | null>(null);
  const [selectedStoreIds, setSelectedStoreIds] = useState<string[]>([]);
  const [newItem, setNewItem] = useState({ name: '', username: '', email: '', phone: '', password: '', role: 'OPERATOR', permissions: '', description: '' });
  const [searchQuery, setSearchQuery] = useState('');

  const { success, error: toastError } = useToast();

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [aRes, rRes, sRes] = await Promise.allSettled([
        adminApi.getAdminUsers().catch(err => { console.warn('[Permission] 获取管理员列表失败:', err); return []; }),
        adminApi.getRoles().catch(err => { console.warn('[Permission] 获取角色列表失败:', err); return []; }),
        storesApi.getStores({ page_size: 100 }).catch(err => { console.warn('[Permission] 获取门店列表失败:', err); return { items: [] }; }),
      ]);
      if (aRes.status === 'fulfilled') {
        const data = aRes.value;
        const list = (Array.isArray(data) ? data : []) as AdminUser[];
        // 兼容后端 snake_case 字段名
        setAdmins(list.map(a => ({ ...a, assignedStores: a.assignedStores || (a as any).assigned_stores || [] })));
      }
      if (rRes.status === 'fulfilled') {
        const rolesData = rRes.value;
        setRoles(Array.isArray(rolesData) ? rolesData : []);
      }
      if (sRes.status === 'fulfilled') {
        const storesData = sRes.value;
        setAllStores(Array.isArray((storesData as any)?.items) ? (storesData as any).items : Array.isArray(storesData) ? storesData : []);
      }
    } catch (err) {
      console.error('[Permission] 数据加载异常:', err);
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally { setLoading(false); }
  };

  useEffect(() => { fetchData(); }, []);

  const filteredUsers = admins.filter(a =>
    (a.username || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
    (a.phone || '').includes(searchQuery) ||
    (a.email || '').toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleAddAdmin = async () => {
    if (!newItem.username || !newItem.password) { toastError('参数错误', '请填写用户名和密码'); return; }
    try {
      await adminApi.createAdminUser({ username: newItem.username, email: newItem.email || undefined, phone: newItem.phone || undefined, password: newItem.password, role: newItem.role });
      success('添加成功', '管理员已创建');
      setShowAdd(false);
      setNewItem({ name: '', username: '', email: '', phone: '', password: '', role: 'OPERATOR', permissions: '', description: '' });
      fetchData();
    } catch (err: any) { toastError('添加失败', err.message); }
  };

  const handleAddRole = async () => {
    if (!newItem.name) { toastError('参数错误', '请填写角色名称'); return; }
    try {
      await adminApi.createRole({ name: newItem.name, permissions: newItem.permissions.split(',').map(s => s.trim()).filter(Boolean), description: newItem.description || undefined });
      success('添加成功', '角色已创建');
      setShowAdd(false);
      setNewItem({ name: '', username: '', email: '', phone: '', password: '', role: 'OPERATOR', permissions: '', description: '' });
      fetchData();
    } catch (err: any) { toastError('添加失败', err.message); }
  };

  const handleDisableAdmin = async (id: string) => {
    try { await adminApi.disableAdminUser(id); success('已禁用', '管理员已禁用'); fetchData(); }
    catch (err: any) { toastError('操作失败', err.message); }
  };

  const handleDeleteRole = async (id: string) => {
    try { await adminApi.deleteRole(id); success('已删除', '角色已移除'); fetchData(); }
    catch (err: any) { toastError('删除失败', err.message); }
  };

  const openStoreAssign = (user: AdminUser) => {
    setSelectedUser(user);
    setSelectedStoreIds(user.assignedStores || []);
    setShowStoreAssign(true);
  };

  const handleSaveStoreAssign = async () => {
    if (!selectedUser) return;
    try {
      await adminApi.assignStores(selectedUser.id, selectedStoreIds);
      success('分配成功', '门店权限已更新');
      setShowStoreAssign(false);
      fetchData();
    } catch (err: any) { toastError('分配失败', err.message); }
  };

  const toggleStore = (storeId: string) => {
    setSelectedStoreIds(prev =>
      prev.includes(storeId) ? prev.filter(id => id !== storeId) : [...prev, storeId]
    );
  };

  if (loading) return <AdminLayout><div className="flex items-center justify-center h-64"><RefreshCw className="w-6 h-6 text-slate-400 animate-spin" /></div></AdminLayout>;
  if (error) return <AdminLayout><div className="flex flex-col items-center justify-center h-64 gap-4"><AlertCircle className="w-10 h-10 text-rose-400" /><p className="text-slate-500">{error}</p><Button variant="outline" onClick={fetchData}>重试</Button></div></AdminLayout>;

  return (
    <AdminLayout>
      <div className="space-y-6 pb-8">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-slate-900">用户与权限管理</h1>
          <Button onClick={() => setShowAdd(true)}><Plus className="w-4 h-4 mr-1" />{tab === 'users' ? '添加用户' : '添加角色'}</Button>
        </div>

        {/* Tab Switch */}
        <div className="flex gap-2 bg-slate-50 rounded-xl p-1 w-fit">
          <button onClick={() => setTab('users')} className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${tab === 'users' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500'}`}>
            <Users className="w-4 h-4" />用户管理
          </button>
          <button onClick={() => setTab('roles')} className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${tab === 'roles' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500'}`}>
            <Shield className="w-4 h-4" />角色管理
          </button>
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input className="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-sm outline-none" placeholder={tab === 'users' ? '搜索用户名、手机号、邮箱...' : '搜索角色名称...'} value={searchQuery} onChange={e => setSearchQuery(e.target.value)} />
        </div>

        {/* Users Tab */}
        {tab === 'users' && (
          <div className="space-y-3">
            {filteredUsers.length === 0 ? (
              <div className="text-center py-16 text-slate-400"><Users className="w-12 h-12 mx-auto mb-3 opacity-30" /><p>暂无用户，点击"添加用户"</p></div>
            ) : filteredUsers.map(a => (
              <Card key={a.id} className="p-5 border-slate-100 shadow-sm">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <div className="w-10 h-10 rounded-full bg-indigo-50 flex items-center justify-center text-indigo-600 font-bold text-sm">{a.username?.[0]?.toUpperCase() || '?'}</div>
                      <div>
                        <p className="font-bold text-slate-900">{a.username}</p>
                        <div className="flex items-center gap-2 text-xs text-slate-500">
                          <span>{a.phone || '无手机号'}</span>
                          {a.email && <><span>·</span><span>{a.email}</span></>}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-3 mt-2">
                      <Badge className="bg-indigo-50 text-indigo-700">{a.role}</Badge>
                      {a.is_active ? <Badge className="bg-emerald-50 text-emerald-700">启用</Badge> : <Badge className="bg-slate-100 text-slate-500">禁用</Badge>}
                      {a.assignedStores && a.assignedStores.length > 0 && (
                        <span className="text-xs text-slate-500 flex items-center gap-1">
                          <Store className="w-3 h-3" />
                          管理 {a.assignedStores.length} 家门店
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button size="sm" variant="outline" onClick={() => openStoreAssign(a)}>
                      <Store className="w-3 h-3 mr-1" />门店设置
                    </Button>
                    {a.is_active && (
                      <Button size="sm" variant="ghost" className="text-rose-500" onClick={() => handleDisableAdmin(a.id)}>
                        <XCircle className="w-4 h-4" />
                      </Button>
                    )}
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}

        {/* Roles Tab */}
        {tab === 'roles' && (
          <Card className="border-slate-100 shadow-sm overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 text-slate-500 text-xs">
                <tr><th className="text-left p-4">角色名称</th><th className="text-left">描述</th><th className="text-left">权限</th><th className="text-right p-4">操作</th></tr>
              </thead>
              <tbody>
                {roles.length === 0 ? (
                  <tr><td colSpan={4} className="text-center py-12 text-slate-400"><Shield className="w-8 h-8 mx-auto mb-2 opacity-50" /><p>暂无角色</p></td></tr>
                ) : roles.map(r => (
                  <tr key={r.id} className="border-t border-slate-50">
                    <td className="p-4 font-medium text-slate-900">{r.name}</td>
                    <td className="text-slate-500">{r.description || '-'}</td>
                    <td><div className="flex flex-wrap gap-1">{(r.permissions || []).map(p => <Badge key={p} className="bg-slate-100 text-slate-600 text-xs">{p}</Badge>)}</div></td>
                    <td className="text-right p-4"><Button size="sm" variant="ghost" className="text-rose-500" onClick={() => handleDeleteRole(r.id)}><XCircle className="w-4 h-4" /></Button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Card>
        )}
      </div>

      {/* Add Dialog */}
      {showAdd && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
          <Card className="w-96 p-6 space-y-4">
            <h3 className="font-bold text-slate-900">{tab === 'users' ? '添加用户' : '添加角色'}</h3>
            {tab === 'users' ? (
              <>
                <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="用户名 *" value={newItem.username} onChange={e => setNewItem(p => ({ ...p, username: e.target.value }))} />
                <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="密码 *" type="password" value={newItem.password} onChange={e => setNewItem(p => ({ ...p, password: e.target.value }))} />
                <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="邮箱" value={newItem.email} onChange={e => setNewItem(p => ({ ...p, email: e.target.value }))} />
                <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="手机号" value={newItem.phone} onChange={e => setNewItem(p => ({ ...p, phone: e.target.value }))} />
                <select className="w-full p-2.5 border border-slate-200 rounded-lg text-sm" value={newItem.role} onChange={e => setNewItem(p => ({ ...p, role: e.target.value }))}>
                  <option value="HQ">HQ 总部</option><option value="OPERATOR">OPERATOR 运营</option><option value="STORE">STORE 门店</option>
                </select>
                <div className="flex justify-end gap-3"><Button variant="ghost" onClick={() => setShowAdd(false)}>取消</Button><Button className="bg-indigo-500 text-white" onClick={handleAddAdmin}>添加</Button></div>
              </>
            ) : (
              <>
                <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="角色名称 *" value={newItem.name} onChange={e => setNewItem(p => ({ ...p, name: e.target.value }))} />
                <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="权限 (逗号分隔)" value={newItem.permissions} onChange={e => setNewItem(p => ({ ...p, permissions: e.target.value }))} />
                <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="描述" value={newItem.description} onChange={e => setNewItem(p => ({ ...p, description: e.target.value }))} />
                <div className="flex justify-end gap-3"><Button variant="ghost" onClick={() => setShowAdd(false)}>取消</Button><Button className="bg-indigo-500 text-white" onClick={handleAddRole}>添加</Button></div>
              </>
            )}
          </Card>
        </div>
      )}

      {/* Store Assignment Dialog */}
      {showStoreAssign && selectedUser && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
          <Card className="w-[500px] max-h-[600px] p-6 space-y-4 overflow-hidden flex flex-col">
            <h3 className="font-bold text-slate-900">门店权限设置 - {selectedUser.username}</h3>
            <p className="text-sm text-slate-500">选择该用户可以管理的门店</p>
            <div className="flex-1 overflow-y-auto space-y-2 pr-2">
              {allStores.length === 0 ? (
                <p className="text-center py-8 text-slate-400">暂无门店数据</p>
              ) : allStores.map(s => (
                <label key={s.id} className={`flex items-center gap-3 p-3 rounded-xl border cursor-pointer transition-colors ${selectedStoreIds.includes(s.id) ? 'border-indigo-300 bg-indigo-50' : 'border-slate-100 hover:border-slate-200'}`}>
                  <input type="checkbox" checked={selectedStoreIds.includes(s.id)} onChange={() => toggleStore(s.id)} className="w-4 h-4 rounded border-slate-300 text-indigo-500 focus:ring-indigo-400" />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-slate-900">{s.name}</p>
                    <p className="text-xs text-slate-400">{s.address || '无地址'} · {s.type || '未知类型'}</p>
                  </div>
                  {selectedStoreIds.includes(s.id) && <CheckCircle className="w-4 h-4 text-indigo-500" />}
                </label>
              ))}
            </div>
            <div className="flex justify-end gap-3 pt-2 border-t border-slate-100">
              <Button variant="ghost" onClick={() => setShowStoreAssign(false)}>取消</Button>
              <Button className="bg-indigo-500 text-white" onClick={handleSaveStoreAssign}>保存设置</Button>
            </div>
          </Card>
        </div>
      )}
    </AdminLayout>
  );
};

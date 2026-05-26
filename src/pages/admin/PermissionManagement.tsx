import React, { useState, useEffect } from 'react';
import {
  Shield, Search, Plus, Users, UserPlus, XCircle, CheckCircle, RefreshCw,
  AlertCircle, Store, Settings, Pencil, Trash2, UserCheck, UserX, Clock, Calendar, Globe
} from 'lucide-react';
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

  // 对话框状态
  const [showAdd, setShowAdd] = useState(false);
  const [showEdit, setShowEdit] = useState(false);
  const [editingUser, setEditingUser] = useState<AdminUser | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deletingUser, setDeletingUser] = useState<AdminUser | null>(null);
  const [showStoreAssign, setShowStoreAssign] = useState(false);
  const [selectedUser, setSelectedUser] = useState<AdminUser | null>(null);
  const [selectedStoreIds, setSelectedStoreIds] = useState<string[]>([]);
  
  // 区域分配状态
  const [showRegionAssign, setShowRegionAssign] = useState(false);
  const [selectedRegionIds, setSelectedRegionIds] = useState<string[]>([]);
  const [regionTree, setRegionTree] = useState<any[]>([]);
  const [loadingRegions, setLoadingRegions] = useState(false);

  // 表单状态
  const [formData, setFormData] = useState({ name: '', username: '', email: '', phone: '', password: '', role: 'OPERATOR', permissions: '', description: '' });
  const [searchQuery, setSearchQuery] = useState('');

  const { success, error: toastError } = useToast();

  // ==================== 数据获取 ====================
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
        // 兼容分页格式 { items: [] } 或纯数组
        const list = Array.isArray(data) ? data : (Array.isArray((data as any)?.items) ? (data as any).items : []);
        setAdmins(list.map((a: any) => ({ ...a, assignedStores: a.assignedStores || a.assigned_stores || [] })));
      }
      if (rRes.status === 'fulfilled') {
        const data = rRes.value;
        setRoles(Array.isArray(data) ? data : (Array.isArray((data as any)?.items) ? (data as any).items : []));
      }
      if (sRes.status === 'fulfilled') {
        const data = sRes.value;
        const storesArr = Array.isArray((data as any)?.items) ? (data as any).items : Array.isArray(data) ? data : [];
        setAllStores(storesArr);
      }
    } catch (err) {
      console.error('[Permission] 数据加载异常:', err);
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally { setLoading(false); }
  };

  useEffect(() => { fetchData(); }, []);

  // ==================== 搜索过滤 ====================
  const filteredUsers = admins.filter(a =>
    (a.username || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
    (a.phone || '').includes(searchQuery) ||
    (a.email || '').toLowerCase().includes(searchQuery.toLowerCase())
  );

  // ==================== 用户 CRUD ====================
  const resetForm = () => {
    setFormData({ name: '', username: '', email: '', phone: '', password: '', role: 'OPERATOR', permissions: '', description: '' });
  };

  const handleAddAdmin = async () => {
    if (!formData.username || !formData.password) { toastError('参数错误', '请填写用户名和密码'); return; }
    try {
      await adminApi.createAdminUser({
        username: formData.username,
        email: formData.email || undefined,
        phone: formData.phone || undefined,
        password: formData.password,
        role: formData.role,
      });
      success('添加成功', '管理员已创建');
      setShowAdd(false);
      resetForm();
      fetchData();
    } catch (err: any) { toastError('添加失败', err.message); }
  };

  const openEditUser = (user: AdminUser) => {
    setEditingUser(user);
    setFormData({
      name: '',
      username: user.username || '',
      email: user.email || '',
      phone: user.phone || '',
      password: '', // 编辑时不修改密码
      role: user.role || 'OPERATOR',
      permissions: '',
      description: '',
    });
    setShowEdit(true);
  };

  const handleEditAdmin = async () => {
    if (!editingUser) return;
    try {
      const updateData: Partial<AdminUser> = {
        email: formData.email || undefined,
        phone: formData.phone || undefined,
        role: formData.role,
      };
      // 如果填写了密码则更新密码
      if (formData.password) {
        (updateData as any).password = formData.password;
      }
      await adminApi.updateAdminUser(editingUser.id, updateData);
      success('更新成功', '用户信息已更新');
      setShowEdit(false);
      setEditingUser(null);
      resetForm();
      fetchData();
    } catch (err: any) { toastError('更新失败', err.message); }
  };

  const openDeleteConfirm = (user: AdminUser) => {
    setDeletingUser(user);
    setShowDeleteConfirm(true);
  };

  const handleDeleteAdmin = async () => {
    if (!deletingUser) return;
    try {
      await adminApi.deleteAdminUser(deletingUser.id);
      success('删除成功', '用户已删除');
      setShowDeleteConfirm(false);
      setDeletingUser(null);
      fetchData();
    } catch (err: any) { toastError('删除失败', err.message); }
  };

  const handleDisableAdmin = async (id: string) => {
    try { await adminApi.disableAdminUser(id); success('已禁用', '管理员已禁用'); fetchData(); }
    catch (err: any) { toastError('操作失败', err.message); }
  };

  const handleEnableAdmin = async (id: string) => {
    try { await adminApi.enableAdminUser(id); success('已启用', '管理员已启用'); fetchData(); }
    catch (err: any) { toastError('操作失败', err.message); }
  };

  // ==================== 角色 CRUD ====================
  const handleAddRole = async () => {
    if (!formData.name) { toastError('参数错误', '请填写角色名称'); return; }
    try {
      await adminApi.createRole({
        name: formData.name,
        permissions: formData.permissions.split(',').map(s => s.trim()).filter(Boolean),
        description: formData.description || undefined,
      });
      success('添加成功', '角色已创建');
      setShowAdd(false);
      resetForm();
      fetchData();
    } catch (err: any) { toastError('添加失败', err.message); }
  };

  const handleDeleteRole = async (id: string) => {
    try { await adminApi.deleteRole(id); success('已删除', '角色已移除'); fetchData(); }
    catch (err: any) { toastError('删除失败', err.message); }
  };

  // ==================== 门店分配 ====================
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

  // ==================== 区域分配 ====================
  const fetchRegionTree = async () => {
    try {
      setLoadingRegions(true);
      const data = await adminApi.getRegionTree();
      setRegionTree(data || []);
    } catch (err: any) {
      console.error('[Permission] 获取区域树失败:', err);
      toastError('获取区域失败', err.message);
    } finally {
      setLoadingRegions(false);
    }
  };

  const openRegionAssign = async (user: AdminUser) => {
    setSelectedUser(user);
    setLoadingRegions(true);
    setShowRegionAssign(true);
    
    try {
      // 并行获取区域树和用户已关联区域
      const [treeData, userRegionsRes] = await Promise.all([
        adminApi.getRegionTree(),
        adminApi.getUserRegions(user.id)
      ]);
      
      setRegionTree(treeData || []);
      
      // 设置已选中的区域ID
      const userRegions = userRegionsRes?.items || userRegionsRes?.data?.items || [];
      const regionIds = userRegions.map((r: any) => r.id);
      setSelectedRegionIds(regionIds);
    } catch (err: any) {
      console.error('[Permission] 打开区域分配失败:', err);
      toastError('获取数据失败', err.message);
    } finally {
      setLoadingRegions(false);
    }
  };

  const toggleRegion = (regionId: string) => {
    setSelectedRegionIds(prev =>
      prev.includes(regionId) ? prev.filter(id => id !== regionId) : [...prev, regionId]
    );
  };

  const handleSaveRegionAssign = async () => {
    if (!selectedUser) return;
    
    try {
      // 获取用户当前的区域
      const userRegionsRes = await adminApi.getUserRegions(selectedUser.id);
      const currentRegionIds = (userRegionsRes?.items || userRegionsRes?.data?.items || []).map((r: any) => r.id);
      
      // 计算需要添加和移除的区域
      const toAdd = selectedRegionIds.filter((id: string) => !currentRegionIds.includes(id));
      const toRemove = currentRegionIds.filter((id: string) => !selectedRegionIds.includes(id));
      
      // 并行执行添加和移除
      await Promise.all([
        ...toAdd.map((regionId: string) => adminApi.addUserRegion(selectedUser.id, regionId)),
        ...toRemove.map((regionId: string) => adminApi.removeUserRegion(selectedUser.id, regionId))
      ]);
      
      success('分配成功', '区域权限已更新');
      setShowRegionAssign(false);
      fetchData();
    } catch (err: any) {
      toastError('分配失败', err.message);
    }
  };

  // ==================== 递归渲染区域节点 ====================
  const renderRegionNode = (region: any, depth: number): JSX.Element => {
    const hasChildren = region.children && region.children.length > 0;
    return (
      <div key={region.id}>
        <label className={`flex items-center gap-3 p-3 rounded-xl border cursor-pointer transition-colors ${selectedRegionIds.includes(region.id) ? 'border-indigo-300 bg-indigo-50' : 'border-slate-100 hover:border-slate-200'}`} style={{ marginLeft: `${depth * 20}px` }}>
          <input type="checkbox" checked={selectedRegionIds.includes(region.id)} onChange={() => toggleRegion(region.id)} className="w-4 h-4 rounded border-slate-300 text-indigo-500 focus:ring-indigo-400" />
          <div className="flex-1">
            <p className="text-sm font-medium text-slate-900">{region.name} <span className="text-xs text-slate-400 ml-2">{region.level === 'province' ? '省' : region.level === 'city' ? '市' : '区'}</span></p>
            {region.code && <p className="text-xs text-slate-400">代码: {region.code}</p>}
          </div>
          {selectedRegionIds.includes(region.id) && <CheckCircle className="w-4 h-4 text-indigo-500" />}
        </label>
        {/* 递归渲染子级 */}
        {hasChildren && (
          <div className="ml-6 space-y-2 mt-2">
            {region.children.map((child: any) => renderRegionNode(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };
  
  // ==================== 渲染 ====================
  if (loading) return <AdminLayout><div className="flex items-center justify-center h-64"><RefreshCw className="w-6 h-6 text-slate-400 animate-spin" /></div></AdminLayout>;
  if (error) return <AdminLayout><div className="flex flex-col items-center justify-center h-64 gap-4"><AlertCircle className="w-10 h-10 text-rose-400" /><p className="text-slate-500">{error}</p><Button variant="outline" onClick={fetchData}>重试</Button></div></AdminLayout>;

  return (
    <AdminLayout>
      <div className="space-y-6 pb-8">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-slate-900">用户与权限管理</h1>
          <Button onClick={() => { resetForm(); setShowAdd(true); }}><Plus className="w-4 h-4 mr-1" />{tab === 'users' ? '添加用户' : '添加角色'}</Button>
        </div>

        {/* Tab 切换 */}
        <div className="flex gap-2 bg-slate-50 rounded-xl p-1 w-fit">
          <button onClick={() => setTab('users')} className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${tab === 'users' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500'}`}>
            <Users className="w-4 h-4" />用户管理
          </button>
          <button onClick={() => setTab('roles')} className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${tab === 'roles' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500'}`}>
            <Shield className="w-4 h-4" />角色管理
          </button>
        </div>

        {/* 搜索 */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input className="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-200 rounded-xl text-sm outline-none" placeholder={tab === 'users' ? '搜索用户名、手机号、邮箱...' : '搜索角色名称...'} value={searchQuery} onChange={e => setSearchQuery(e.target.value)} />
        </div>

        {/* ==================== 用户列表 ==================== */}
        {tab === 'users' && (
          <div className="space-y-3">
            {filteredUsers.length === 0 ? (
              <div className="text-center py-16 text-slate-400"><Users className="w-12 h-12 mx-auto mb-3 opacity-30" /><p>暂无用户，点击"添加用户"</p></div>
            ) : filteredUsers.map(a => (
              <Card key={a.id} className="p-5 border-slate-100 shadow-sm hover:shadow-md transition-shadow">
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
                    <div className="flex items-center gap-3 mt-2 flex-wrap">
                      <Badge className="bg-indigo-50 text-indigo-700">{a.role}</Badge>
                      {a.is_active ? (
                        <Badge className="bg-emerald-50 text-emerald-700">启用</Badge>
                      ) : (
                        <Badge className="bg-slate-100 text-slate-500">禁用</Badge>
                      )}
                      {a.assignedStores && a.assignedStores.length > 0 && (
                        <span className="text-xs text-slate-500 flex items-center gap-1">
                          <Store className="w-3 h-3" />
                          管理 {a.assignedStores.length} 家门店
                        </span>
                      )}
                      {a.last_login_at && (
                        <span className="text-xs text-slate-400 flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          最近登录：{new Date(a.last_login_at).toLocaleString('zh-CN')}
                        </span>
                      )}
                      {a.created_at && (
                        <span className="text-xs text-slate-400 flex items-center gap-1">
                          <Calendar className="w-3 h-3" />
                          创建于：{new Date(a.created_at).toLocaleDateString('zh-CN')}
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button size="sm" variant="outline" onClick={() => openStoreAssign(a)}>
                      <Store className="w-3 h-3 mr-1" />门店设置
                    </Button>
                    <Button size="sm" variant="outline" onClick={() => openRegionAssign(a)}>
                      <Globe className="w-3 h-3 mr-1" />区域设置
                    </Button>
                    <Button size="sm" variant="ghost" onClick={() => openEditUser(a)}>
                      <Pencil className="w-3 h-3" />
                    </Button>
                    {a.is_active ? (
                      <Button size="sm" variant="ghost" className="text-amber-500" onClick={() => handleDisableAdmin(a.id)}>
                        <UserX className="w-4 h-4" />
                      </Button>
                    ) : (
                      <Button size="sm" variant="ghost" className="text-emerald-500" onClick={() => handleEnableAdmin(a.id)}>
                        <UserCheck className="w-4 h-4" />
                      </Button>
                    )}
                    <Button size="sm" variant="ghost" className="text-rose-500" onClick={() => openDeleteConfirm(a)}>
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}

        {/* ==================== 角色列表 ==================== */}
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

      {/* ==================== 添加用户/角色 对话框 ==================== */}
      {showAdd && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={() => { setShowAdd(false); resetForm(); }}>
          <Card className="w-96 p-6 space-y-4" onClick={e => e.stopPropagation()}>
            <h3 className="font-bold text-slate-900">{tab === 'users' ? '添加用户' : '添加角色'}</h3>
            {tab === 'users' ? (
              <>
                <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="用户名 *" value={formData.username} onChange={e => setFormData(p => ({ ...p, username: e.target.value }))} />
                <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="密码 *" type="password" value={formData.password} onChange={e => setFormData(p => ({ ...p, password: e.target.value }))} />
                <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="邮箱" value={formData.email} onChange={e => setFormData(p => ({ ...p, email: e.target.value }))} />
                <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="手机号" value={formData.phone} onChange={e => setFormData(p => ({ ...p, phone: e.target.value }))} />
                <select className="w-full p-2.5 border border-slate-200 rounded-lg text-sm" value={formData.role} onChange={e => setFormData(p => ({ ...p, role: e.target.value }))}>
                  <option value="HQ">HQ 总部</option>
                  <option value="OPERATOR">OPERATOR 运营</option>
                  <option value="STORE">STORE 门店</option>
                </select>
                <div className="flex justify-end gap-3">
                  <Button variant="ghost" onClick={() => { setShowAdd(false); resetForm(); }}>取消</Button>
                  <Button className="bg-indigo-500 text-white" onClick={handleAddAdmin}>添加</Button>
                </div>
              </>
            ) : (
              <>
                <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="角色名称 *" value={formData.name} onChange={e => setFormData(p => ({ ...p, name: e.target.value }))} />
                <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="权限 (逗号分隔)" value={formData.permissions} onChange={e => setFormData(p => ({ ...p, permissions: e.target.value }))} />
                <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="描述" value={formData.description} onChange={e => setFormData(p => ({ ...p, description: e.target.value }))} />
                <div className="flex justify-end gap-3">
                  <Button variant="ghost" onClick={() => { setShowAdd(false); resetForm(); }}>取消</Button>
                  <Button className="bg-indigo-500 text-white" onClick={handleAddRole}>添加</Button>
                </div>
              </>
            )}
          </Card>
        </div>
      )}

      {/* ==================== 编辑用户 对话框 ==================== */}
      {showEdit && editingUser && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={() => { setShowEdit(false); setEditingUser(null); resetForm(); }}>
          <Card className="w-96 p-6 space-y-4" onClick={e => e.stopPropagation()}>
            <h3 className="font-bold text-slate-900">编辑用户 - {editingUser.username}</h3>
            <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none bg-slate-50" placeholder="用户名" value={formData.username} disabled />
            <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="新密码（留空则不修改）" type="password" value={formData.password} onChange={e => setFormData(p => ({ ...p, password: e.target.value }))} />
            <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="邮箱" value={formData.email} onChange={e => setFormData(p => ({ ...p, email: e.target.value }))} />
            <input className="w-full p-2.5 border border-slate-200 rounded-lg text-sm outline-none" placeholder="手机号" value={formData.phone} onChange={e => setFormData(p => ({ ...p, phone: e.target.value }))} />
            <select className="w-full p-2.5 border border-slate-200 rounded-lg text-sm" value={formData.role} onChange={e => setFormData(p => ({ ...p, role: e.target.value }))}>
              <option value="HQ">HQ 总部</option>
              <option value="OPERATOR">OPERATOR 运营</option>
              <option value="STORE">STORE 门店</option>
            </select>
            <div className="flex justify-end gap-3">
              <Button variant="ghost" onClick={() => { setShowEdit(false); setEditingUser(null); resetForm(); }}>取消</Button>
              <Button className="bg-indigo-500 text-white" onClick={handleEditAdmin}>保存</Button>
            </div>
          </Card>
        </div>
      )}

      {/* ==================== 删除确认 对话框 ==================== */}
      {showDeleteConfirm && deletingUser && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={() => { setShowDeleteConfirm(false); setDeletingUser(null); }}>
          <Card className="w-96 p-6 space-y-4" onClick={e => e.stopPropagation()}>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-rose-50 flex items-center justify-center"><Trash2 className="w-5 h-5 text-rose-500" /></div>
              <div>
                <h3 className="font-bold text-slate-900">确认删除</h3>
                <p className="text-sm text-slate-500">确定要删除用户「{deletingUser.username}」吗？此操作不可恢复。</p>
              </div>
            </div>
            <div className="flex justify-end gap-3">
              <Button variant="ghost" onClick={() => { setShowDeleteConfirm(false); setDeletingUser(null); }}>取消</Button>
              <Button className="bg-rose-500 text-white" onClick={handleDeleteAdmin}>确认删除</Button>
            </div>
          </Card>
        </div>
      )}

      {/* ==================== 门店分配 对话框 ==================== */}
      {showStoreAssign && selectedUser && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={() => setShowStoreAssign(false)}>
          <Card className="w-[500px] max-h-[600px] p-6 space-y-4 overflow-hidden flex flex-col" onClick={e => e.stopPropagation()}>
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

      {/* ==================== 区域分配 对话框 ==================== */}
      {showRegionAssign && selectedUser && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={() => setShowRegionAssign(false)}>
          <Card className="w-[600px] max-h-[700px] p-6 space-y-4 overflow-hidden flex flex-col" onClick={e => e.stopPropagation()}>
            <h3 className="font-bold text-slate-900">区域权限设置 - {selectedUser.username}</h3>
            <p className="text-sm text-slate-500">选择该用户可以管理的区域（自动包含子级区域）</p>
            <div className="flex-1 overflow-y-auto space-y-2 pr-2">
              {loadingRegions ? (
                <div className="flex items-center justify-center py-8">
                  <RefreshCw className="w-6 h-6 text-slate-400 animate-spin" />
                </div>
              ) : regionTree.length === 0 ? (
                <p className="text-center py-8 text-slate-400">暂无区域数据，请先在"区域管理"中创建区域</p>
              ) : (
                // 渲染区域树（递归）
                regionTree.map(r => renderRegionNode(r, 0))
              )}
            </div>
            <div className="flex justify-end gap-3 pt-2 border-t border-slate-100">
              <Button variant="ghost" onClick={() => setShowRegionAssign(false)}>取消</Button>
              <Button className="bg-indigo-500 text-white" onClick={handleSaveRegionAssign}>保存设置</Button>
            </div>
          </Card>
        </div>
      )}
    </AdminLayout>
  );
};

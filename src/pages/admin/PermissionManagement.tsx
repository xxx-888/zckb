import React, { useState } from 'react';
import { 
  Shield, 
  Search, 
  Plus, 
  MoreHorizontal, 
  Users, 
  Building, 
  Edit, 
  Trash2, 
  Eye,
  CheckCircle,
  XCircle,
  RefreshCw,
  Download,
  UserPlus
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { AdminLayout } from '../../components/AdminLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';

interface Role {
  id: number;
  name: string;
  description: string;
  permissions: string[];
  userCount: number;
  createdAt: string;
}

interface Admin {
  id: number;
  name: string;
  email: string;
  role: string;
  status: 'active' | 'inactive';
  lastLogin: string;
}

interface Structure {
  id: number;
  name: string;
  type: 'department' | 'team';
  parentId: number | null;
  memberCount: number;
}

export const PermissionManagement: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'roles' | 'admins' | 'structure'>('roles');
  
  // Roles state
  const [roles, setRoles] = useState<Role[]>([
    { id: 1, name: '超级管理员', description: '拥有所有权限', permissions: ['all'], userCount: 1, createdAt: '2026-01-01' },
    { id: 2, name: '运营经理', description: '管理店铺和评论', permissions: ['store.manage', 'review.manage'], userCount: 3, createdAt: '2026-01-15' },
    { id: 3, name: '客服主管', description: '审核回复和查看数据', permissions: ['reply.audit', 'data.view'], userCount: 5, createdAt: '2026-02-01' },
  ]);
  
  // Admins state
  const [admins, setAdmins] = useState<Admin[]>([
    { id: 1, name: '张三', email: 'zhangsan@company.com', role: '超级管理员', status: 'active', lastLogin: '2026-05-12 10:30' },
    { id: 2, name: '李四', email: 'lisi@company.com', role: '运营经理', status: 'active', lastLogin: '2026-05-11 16:45' },
    { id: 3, name: '王五', email: 'wangwu@company.com', role: '客服主管', status: 'inactive', lastLogin: '2026-05-10 09:20' },
  ]);
  
  // Structure state
  const [structures, setStructures] = useState<Structure[]>([
    { id: 1, name: '总部', type: 'department', parentId: null, memberCount: 15 },
    { id: 2, name: '技术部', type: 'team', parentId: 1, memberCount: 8 },
    { id: 3, name: '运营部', type: 'team', parentId: 1, memberCount: 7 },
  ]);
  
  // UI state
  const [showAddRole, setShowAddRole] = useState(false);
  const [showEditRole, setShowEditRole] = useState(false);
  const [showViewRole, setShowViewRole] = useState(false);
  const [showAddAdmin, setShowAddAdmin] = useState(false);
  const [showEditAdmin, setShowEditAdmin] = useState(false);
  const [showViewAdmin, setShowViewAdmin] = useState(false);
  
  const [editingRole, setEditingRole] = useState<Role | null>(null);
  const [viewingRole, setViewingRole] = useState<Role | null>(null);
  const [editingAdmin, setEditingAdmin] = useState<Admin | null>(null);
  const [viewingAdmin, setViewingAdmin] = useState<Admin | null>(null);
  
  const [newRole, setNewRole] = useState({ name: '', description: '', permissions: [] as string[] });
  const [newAdmin, setNewAdmin] = useState({ name: '', email: '', role: '运营经理' });
  
  const [searchQuery, setSearchQuery] = useState('');
  const { success, error } = useToast();

  // Role handlers
  const handleAddRole = () => {
    if (!newRole.name) {
      error('添加失败', '请输入角色名称');
      return;
    }
    const newId = roles.length + 1;
    const role: Role = {
      id: newId,
      name: newRole.name,
      description: newRole.description,
      permissions: newRole.permissions,
      userCount: 0,
      createdAt: new Date().toISOString().split('T')[0]
    };
    setRoles([...roles, role]);
    setShowAddRole(false);
    setNewRole({ name: '', description: '', permissions: [] });
    success('添加成功', `角色 "${newRole.name}" 已创建`);
  };

  const handleEditRole = (id: number) => {
    const role = roles.find(r => r.id === id);
    if (role) {
      setEditingRole(role);
      setShowEditRole(true);
    }
  };

  const handleUpdateRole = () => {
    if (!editingRole) return;
    setRoles(roles.map(r => r.id === editingRole.id ? editingRole : r));
    setShowEditRole(false);
    setEditingRole(null);
    success('更新成功', `角色 "${editingRole.name}" 已更新`);
  };

  const handleDeleteRole = (id: number) => {
    const role = roles.find(r => r.id === id);
    if (role && role.userCount > 0) {
      error('删除失败', '该角色下还有用户，无法删除');
      return;
    }
    setRoles(roles.filter(r => r.id !== id));
    success('删除成功', `角色 "${role?.name}" 已删除`);
  };

  const handleViewRole = (id: number) => {
    const role = roles.find(r => r.id === id);
    if (role) {
      setViewingRole(role);
      setShowViewRole(true);
    }
  };

  // Admin handlers
  const handleAddAdmin = () => {
    if (!newAdmin.name || !newAdmin.email) {
      error('添加失败', '请填写完整信息');
      return;
    }
    const newId = admins.length + 1;
    const admin: Admin = {
      id: newId,
      name: newAdmin.name,
      email: newAdmin.email,
      role: newAdmin.role,
      status: 'active',
      lastLogin: '-'
    };
    setAdmins([...admins, admin]);
    setShowAddAdmin(false);
    setNewAdmin({ name: '', email: '', role: '运营经理' });
    success('添加成功', `管理员 "${newAdmin.name}" 已创建`);
  };

  const handleEditAdmin = (id: number) => {
    const admin = admins.find(a => a.id === id);
    if (admin) {
      setEditingAdmin(admin);
      setShowEditAdmin(true);
    }
  };

  const handleUpdateAdmin = () => {
    if (!editingAdmin) return;
    setAdmins(admins.map(a => a.id === editingAdmin.id ? editingAdmin : a));
    setShowEditAdmin(false);
    setEditingAdmin(null);
    success('更新成功', `管理员 "${editingAdmin.name}" 信息已更新`);
  };

  const handleDeleteAdmin = (id: number) => {
    const admin = admins.find(a => a.id === id);
    setAdmins(admins.filter(a => a.id !== id));
    success('删除成功', `管理员 "${admin?.name}" 已删除`);
  };

  const handleViewAdmin = (id: number) => {
    const admin = admins.find(a => a.id === id);
    if (admin) {
      setViewingAdmin(admin);
      setShowViewAdmin(true);
    }
  };

  const handleToggleAdminStatus = (id: number) => {
    setAdmins(admins.map(a => 
      a.id === id ? { ...a, status: a.status === 'active' ? 'inactive' as const : 'active' as const } : a
    ));
    const admin = admins.find(a => a.id === id);
    success('状态已更新', `管理员 "${admin?.name}" 状态已切换`);
  };

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">权限管理</h2>
            <p className="text-slate-500 mt-1">管理系统角色、管理员和组织架构</p>
          </div>
          <div className="flex gap-3">
            <Button 
              variant="outline" 
              className="gap-2"
              onClick={() => success('导出数据', '正在导出权限配置...')}
            >
              <Download className="w-4 h-4" /> 导出配置
            </Button>
            {activeTab === 'roles' && (
              <Button 
                className="bg-amber-500 hover:bg-amber-600 text-white gap-2"
                onClick={() => setShowAddRole(true)}
              >
                <Plus className="w-4 h-4" /> 新增角色
              </Button>
            )}
            {activeTab === 'admins' && (
              <Button 
                className="bg-amber-500 hover:bg-amber-600 text-white gap-2"
                onClick={() => setShowAddAdmin(true)}
              >
                <UserPlus className="w-4 h-4" /> 新增管理员
              </Button>
            )}
          </div>
        </div>

        {/* Tab Switcher */}
        <Card className="p-1 bg-slate-50 inline-flex gap-1">
          {[
            { key: 'roles', label: '角色管理', icon: Shield },
            { key: 'admins', label: '管理员', icon: Users },
            { key: 'structure', label: '组织架构', icon: Building },
          ].map(tab => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key as any)}
              className={cn(
                "px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2",
                activeTab === tab.key 
                  ? "bg-white text-amber-600 shadow-sm" 
                  : "text-slate-500 hover:text-slate-900"
              )}
            >
              <tab.icon className="w-4 h-4" />
              {tab.label}
            </button>
          ))}
        </Card>

        {/* Roles Tab */}
        {activeTab === 'roles' && (
          <>
            {/* Add Role Form */}
            {showAddRole && (
              <Card className="p-6 border-2 border-amber-500 bg-amber-50/10 animate-in zoom-in-95 duration-200">
                <h4 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
                  <Plus className="w-4 h-4" /> 新增角色
                </h4>
                <div className="space-y-4 mb-6">
                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-slate-500">角色名称</label>
                    <Input 
                      value={newRole.name}
                      onChange={(e) => setNewRole({...newRole, name: e.target.value})}
                      placeholder="请输入角色名称" 
                    />
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-slate-500">角色描述</label>
                    <Input 
                      value={newRole.description}
                      onChange={(e) => setNewRole({...newRole, description: e.target.value})}
                      placeholder="请输入角色描述" 
                    />
                  </div>
                </div>
                <div className="flex gap-3 pt-4 border-t border-slate-100">
                  <Button className="flex-1 bg-amber-600 hover:bg-amber-700" onClick={handleAddRole}>创建角色</Button>
                  <Button variant="ghost" onClick={() => setShowAddRole(false)}>取消</Button>
                </div>
              </Card>
            )}

            {/* Edit Role Form */}
            {showEditRole && editingRole && (
              <Card className="p-6 border-2 border-blue-500 bg-blue-50/10 animate-in zoom-in-95 duration-200">
                <h4 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
                  <Edit className="w-4 h-4" /> 编辑角色
                </h4>
                <div className="space-y-4 mb-6">
                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-slate-500">角色名称</label>
                    <Input 
                      value={editingRole.name}
                      onChange={(e) => setEditingRole({...editingRole, name: e.target.value})}
                      placeholder="请输入角色名称" 
                    />
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-xs font-bold text-slate-500">角色描述</label>
                    <Input 
                      value={editingRole.description}
                      onChange={(e) => setEditingRole({...editingRole, description: e.target.value})}
                      placeholder="请输入角色描述" 
                    />
                  </div>
                </div>
                <div className="flex gap-3 pt-4 border-t border-slate-100">
                  <Button className="flex-1 bg-blue-600 hover:bg-blue-700" onClick={handleUpdateRole}>更新角色</Button>
                  <Button variant="ghost" onClick={() => { setShowEditRole(false); setEditingRole(null); }}>取消</Button>
                </div>
              </Card>
            )}

            {/* View Role Detail */}
            {showViewRole && viewingRole && (
              <Card className="p-6 border-2 border-green-500 bg-green-50/10 animate-in zoom-in-95 duration-200">
                <div className="flex justify-between items-start mb-6">
                  <h4 className="font-bold text-slate-900 flex items-center gap-2">
                    <Eye className="w-4 h-4" /> 角色详情
                  </h4>
                  <Button variant="ghost" size="sm" onClick={() => { setShowViewRole(false); setViewingRole(null); }}>
                    ✕
                  </Button>
                </div>
                <div className="space-y-4">
                  <div>
                    <p className="text-xs font-bold text-slate-500 mb-1">角色名称</p>
                    <p className="text-sm text-slate-900">{viewingRole.name}</p>
                  </div>
                  <div>
                    <p className="text-xs font-bold text-slate-500 mb-1">角色描述</p>
                    <p className="text-sm text-slate-900">{viewingRole.description}</p>
                  </div>
                  <div>
                    <p className="text-xs font-bold text-slate-500 mb-1">用户数量</p>
                    <p className="text-sm text-slate-900">{viewingRole.userCount} 人</p>
                  </div>
                  <div>
                    <p className="text-xs font-bold text-slate-500 mb-1">创建时间</p>
                    <p className="text-sm text-slate-900">{viewingRole.createdAt}</p>
                  </div>
                </div>
              </Card>
            )}

            {/* Roles Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {roles.map(role => (
                <Card key={role.id} className="p-6 hover:shadow-md transition-all">
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-lg bg-amber-50 flex items-center justify-center">
                        <Shield className="w-5 h-5 text-amber-600" />
                      </div>
                      <div>
                        <p className="font-bold text-slate-900">{role.name}</p>
                        <p className="text-xs text-slate-400">{role.userCount} 个用户</p>
                      </div>
                    </div>
                    <div className="flex gap-1">
                      <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-400 hover:text-blue-600" onClick={() => handleEditRole(role.id)}>
                        <Edit className="w-4 h-4" />
                      </Button>
                      <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-400 hover:text-red-600" onClick={() => handleDeleteRole(role.id)}>
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                  <p className="text-sm text-slate-500 mb-3">{role.description}</p>
                  <div className="flex items-center justify-between pt-3 border-t border-slate-100">
                    <Badge variant="outline">{role.permissions.length} 个权限</Badge>
                    <Button variant="ghost" size="sm" className="text-amber-600" onClick={() => handleViewRole(role.id)}>
                      <Eye className="w-3 h-3 mr-1" /> 查看详情
                    </Button>
                  </div>
                </Card>
              ))}
            </div>
          </>
        )}

        {/* Admins Tab */}
        {activeTab === 'admins' && (
          <>
            {/* Add Admin Form */}
            {showAddAdmin && (
              <Card className="p-6 border-2 border-amber-500 bg-amber-50/10 animate-in zoom-in-95 duration-200">
                <h4 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
                  <UserPlus className="w-4 h-4" /> 新增管理员
                </h4>
                <div className="grid grid-cols-2 gap-6 mb-6">
                  <div className="space-y-4">
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-500">姓名</label>
                      <Input 
                        value={newAdmin.name}
                        onChange={(e) => setNewAdmin({...newAdmin, name: e.target.value})}
                        placeholder="请输入姓名" 
                      />
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-500">邮箱</label>
                      <Input 
                        value={newAdmin.email}
                        onChange={(e) => setNewAdmin({...newAdmin, email: e.target.value})}
                        placeholder="请输入邮箱" 
                      />
                    </div>
                  </div>
                  <div className="space-y-4">
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-500">分配角色</label>
                      <select 
                        value={newAdmin.role}
                        onChange={(e) => setNewAdmin({...newAdmin, role: e.target.value})}
                        className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-amber-500/20"
                      >
                        {roles.map(role => (
                          <option key={role.id}>{role.name}</option>
                        ))}
                      </select>
                    </div>
                  </div>
                </div>
                <div className="flex gap-3 pt-4 border-t border-slate-100">
                  <Button className="flex-1 bg-amber-600 hover:bg-amber-700" onClick={handleAddAdmin}>创建管理员</Button>
                  <Button variant="ghost" onClick={() => setShowAddAdmin(false)}>取消</Button>
                </div>
              </Card>
            )}

            {/* Edit Admin Form */}
            {showEditAdmin && editingAdmin && (
              <Card className="p-6 border-2 border-blue-500 bg-blue-50/10 animate-in zoom-in-95 duration-200">
                <h4 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
                  <Edit className="w-4 h-4" /> 编辑管理员
                </h4>
                <div className="grid grid-cols-2 gap-6 mb-6">
                  <div className="space-y-4">
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-500">姓名</label>
                      <Input 
                        value={editingAdmin.name}
                        onChange={(e) => setEditingAdmin({...editingAdmin, name: e.target.value})}
                        placeholder="请输入姓名" 
                      />
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-500">邮箱</label>
                      <Input 
                        value={editingAdmin.email}
                        onChange={(e) => setEditingAdmin({...editingAdmin, email: e.target.value})}
                        placeholder="请输入邮箱" 
                      />
                    </div>
                  </div>
                  <div className="space-y-4">
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-500">分配角色</label>
                      <select 
                        value={editingAdmin.role}
                        onChange={(e) => setEditingAdmin({...editingAdmin, role: e.target.value})}
                        className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500/20"
                      >
                        {roles.map(role => (
                          <option key={role.id}>{role.name}</option>
                        ))}
                      </select>
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-xs font-bold text-slate-500">状态</label>
                      <select 
                        value={editingAdmin.status}
                        onChange={(e) => setEditingAdmin({...editingAdmin, status: e.target.value as 'active' | 'inactive'})}
                        className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500/20"
                      >
                        <option value="active">正常</option>
                        <option value="inactive">禁用</option>
                      </select>
                    </div>
                  </div>
                </div>
                <div className="flex gap-3 pt-4 border-t border-slate-100">
                  <Button className="flex-1 bg-blue-600 hover:bg-blue-700" onClick={handleUpdateAdmin}>更新管理员</Button>
                  <Button variant="ghost" onClick={() => { setShowEditAdmin(false); setEditingAdmin(null); }}>取消</Button>
                </div>
              </Card>
            )}

            {/* View Admin Detail */}
            {showViewAdmin && viewingAdmin && (
              <Card className="p-6 border-2 border-green-500 bg-green-50/10 animate-in zoom-in-95 duration-200">
                <div className="flex justify-between items-start mb-6">
                  <h4 className="font-bold text-slate-900 flex items-center gap-2">
                    <Eye className="w-4 h-4" /> 管理员详情
                  </h4>
                  <Button variant="ghost" size="sm" onClick={() => { setShowViewAdmin(false); setViewingAdmin(null); }}>
                    ✕
                  </Button>
                </div>
                <div className="grid grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <p className="text-xs font-bold text-slate-500 mb-1">姓名</p>
                      <p className="text-sm text-slate-900">{viewingAdmin.name}</p>
                    </div>
                    <div>
                      <p className="text-xs font-bold text-slate-500 mb-1">邮箱</p>
                      <p className="text-sm text-slate-900">{viewingAdmin.email}</p>
                    </div>
                  </div>
                  <div className="space-y-4">
                    <div>
                      <p className="text-xs font-bold text-slate-500 mb-1">角色</p>
                      <Badge variant="outline">{viewingAdmin.role}</Badge>
                    </div>
                    <div>
                      <p className="text-xs font-bold text-slate-500 mb-1">状态</p>
                      <Badge className={viewingAdmin.status === 'active' ? "bg-emerald-50 text-emerald-600" : "bg-slate-100 text-slate-400"}>
                        {viewingAdmin.status === 'active' ? '正常' : '已禁用'}
                      </Badge>
                    </div>
                    <div>
                      <p className="text-xs font-bold text-slate-500 mb-1">最后登录</p>
                      <p className="text-sm text-slate-900">{viewingAdmin.lastLogin}</p>
                    </div>
                  </div>
                </div>
              </Card>
            )}

            {/* Admin Table */}
            <Card className="overflow-hidden">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-slate-50/50 border-b border-slate-100">
                    <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">管理员</th>
                    <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">角色</th>
                    <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">状态</th>
                    <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">最后登录</th>
                    <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase text-right">操作</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {admins.map(admin => (
                    <tr key={admin.id} className="hover:bg-slate-50/50 transition-colors">
                      <td className="px-6 py-4">
                        <div>
                          <p className="font-bold text-slate-900">{admin.name}</p>
                          <p className="text-xs text-slate-400">{admin.email}</p>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <Badge variant="outline">{admin.role}</Badge>
                      </td>
                      <td className="px-6 py-4">
                        <Badge className={admin.status === 'active' ? "bg-emerald-50 text-emerald-600" : "bg-slate-100 text-slate-400"}>
                          {admin.status === 'active' ? '正常' : '已禁用'}
                        </Badge>
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">
                        {admin.lastLogin}
                      </td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex justify-end gap-1">
                          <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-400 hover:text-emerald-600" onClick={() => handleToggleAdminStatus(admin.id)}>
                            {admin.status === 'active' ? <XCircle className="w-4 h-4" /> : <CheckCircle className="w-4 h-4" />}
                          </Button>
                          <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-400 hover:text-blue-600" onClick={() => handleEditAdmin(admin.id)}>
                            <Edit className="w-4 h-4" />
                          </Button>
                          <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-400 hover:text-red-600" onClick={() => handleDeleteAdmin(admin.id)}>
                            <Trash2 className="w-4 h-4" />
                          </Button>
                          <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-400 hover:text-green-600" onClick={() => handleViewAdmin(admin.id)}>
                            <Eye className="w-4 h-4" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </Card>
          </>
        )}

        {/* Structure Tab */}
        {activeTab === 'structure' && (
          <Card className="p-6">
            <h4 className="font-bold text-slate-900 mb-4">组织架构</h4>
            <div className="space-y-4">
              {structures.map(struct => (
                <div key={struct.id} className="flex items-center justify-between p-4 bg-slate-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center">
                      {struct.type === 'department' ? <Building className="w-5 h-5 text-blue-600" /> : <Users className="w-5 h-5 text-blue-600" />}
                    </div>
                    <div>
                      <p className="font-medium text-slate-900">{struct.name}</p>
                      <p className="text-xs text-slate-400">{struct.type === 'department' ? '部门' : '团队'} · {struct.memberCount} 人</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        )}
      </div>
    </AdminLayout>
  );
};

import React, { useState } from 'react';
import { 
  Store, 
  Search, 
  Plus, 
  MoreHorizontal, 
  MapPin, 
  Phone, 
  Globe, 
  ExternalLink, 
  Edit, 
  Trash2, 
  Eye,
  CheckCircle2,
  RefreshCw,
  Download
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { AdminLayout } from '../../components/AdminLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';

interface Store {
  id: number;
  name: string;
  type: string;
  owner: string;
  status: 'active' | 'pending' | 'inactive';
  platformCount: number;
  reviewCount: string;
  location: string;
}

export const StoreManagement: React.FC = () => {
  const [stores, setStores] = useState<Store[]>([
    { id: 1, name: '香格里拉大酒店·旗舰店', type: '餐饮/住宿', owner: '王店长', status: 'active', platformCount: 4, reviewCount: '12,842', location: '北京朝阳区' },
    { id: 2, name: '悦享西餐厅', type: '餐饮', owner: '李先生', status: 'active', platformCount: 3, reviewCount: '3,521', location: '上海静安区' },
    { id: 3, name: '心心咖啡厅', type: '饮品', owner: '赵女士', status: 'pending', platformCount: 2, reviewCount: '842', location: '广州天河区' },
    { id: 4, name: '大唐不夜城火锅', type: '餐饮', owner: '周店长', status: 'inactive', platformCount: 5, reviewCount: '25,102', location: '西安雁塔区' },
  ]);

  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState<string>('all');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [showAddStore, setShowAddStore] = useState(false);
  const [showEditStore, setShowEditStore] = useState(false);
  const [showViewDetail, setShowViewDetail] = useState(false);
  const [editingStore, setEditingStore] = useState<Store | null>(null);
  const [viewingStore, setViewingStore] = useState<Store | null>(null);
  const [newStore, setNewStore] = useState({ name: '', type: '餐饮', owner: '', location: '' });
  
  const { success, error } = useToast();

  const filteredStores = stores.filter(store => {
    const matchesSearch = store.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          store.owner.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          store.location.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesType = filterType === 'all' || store.type === filterType;
    const matchesStatus = filterStatus === 'all' || store.status === filterStatus;
    return matchesSearch && matchesType && matchesStatus;
  });

  const handleAddStore = () => {
    if (!newStore.name || !newStore.owner) {
      error('添加失败', '请填写店铺名称和负责人');
      return;
    }
    const newId = stores.length + 1;
    const store: Store = {
      id: newId,
      name: newStore.name,
      type: newStore.type,
      owner: newStore.owner,
      status: 'pending',
      platformCount: 0,
      reviewCount: '0',
      location: newStore.location
    };
    setStores([...stores, store]);
    setShowAddStore(false);
    setNewStore({ name: '', type: '餐饮', owner: '', location: '' });
    success('添加成功', `店铺 "${newStore.name}" 已创建，等待激活`);
  };

  const handleEditStore = (id: number) => {
    const store = stores.find(s => s.id === id);
    if (store) {
      setEditingStore(store);
      setShowEditStore(true);
    }
  };

  const handleUpdateStore = () => {
    if (!editingStore) return;
    if (!editingStore.name || !editingStore.owner) {
      error('更新失败', '请填写店铺名称和负责人');
      return;
    }
    setStores(stores.map(s => s.id === editingStore.id ? editingStore : s));
    setShowEditStore(false);
    setEditingStore(null);
    success('更新成功', `店铺 "${editingStore.name}" 信息已更新`);
  };

  const handleViewDetail = (id: number) => {
    const store = stores.find(s => s.id === id);
    if (store) {
      setViewingStore(store);
      setShowViewDetail(true);
    }
  };

  const handleDeleteStore = (id: number) => {
    const store = stores.find(s => s.id === id);
    setStores(stores.filter(s => s.id !== id));
    success('删除成功', `店铺 "${store?.name}" 已删除`);
  };

  const handleActivateStore = (id: number) => {
    setStores(stores.map(s => 
      s.id === id ? { ...s, status: 'active' as const } : s
    ));
    const store = stores.find(s => s.id === id);
    success('激活成功', `店铺 "${store?.name}" 已激活`);
  };

  const handleExportData = () => {
    success('导出数据', '正在生成店铺数据报表...');
    setTimeout(() => {
      success('导出完成', '店铺数据报表已下载');
    }, 1500);
  };

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">店铺管理</h2>
            <p className="text-slate-500 mt-1">管理系统内所有接入的商家门店</p>
          </div>
          <div className="flex gap-3">
            <Button 
              variant="outline" 
              className="gap-2"
              onClick={handleExportData}
            >
              <Download className="w-4 h-4" /> 导出数据
            </Button>
            <Button 
              className="bg-amber-500 hover:bg-amber-600 text-white gap-2"
              onClick={() => setShowAddStore(true)}
            >
              <Plus className="w-4 h-4" /> 新增店铺
            </Button>
          </div>
        </div>

        {/* Add Store Form */}
        {showAddStore && (
          <Card className="p-6 border-2 border-amber-500 bg-amber-50/10 animate-in zoom-in-95 duration-200">
            <h4 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
              <Plus className="w-4 h-4" /> 新增店铺
            </h4>
            <div className="grid grid-cols-2 gap-6 mb-6">
              <div className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">店铺名称</label>
                  <Input 
                    value={newStore.name}
                    onChange={(e) => setNewStore({...newStore, name: e.target.value})}
                    placeholder="请输入店铺名称" 
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">负责人</label>
                  <Input 
                    value={newStore.owner}
                    onChange={(e) => setNewStore({...newStore, owner: e.target.value})}
                    placeholder="请输入负责人姓名" 
                  />
                </div>
              </div>
              <div className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">店铺类型</label>
                  <select 
                    value={newStore.type}
                    onChange={(e) => setNewStore({...newStore, type: e.target.value})}
                    className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-amber-500/20"
                  >
                    <option>餐饮</option>
                    <option>饮品</option>
                    <option>住宿</option>
                    <option>零售</option>
                  </select>
                </div>
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">所在地区</label>
                  <Input 
                    value={newStore.location}
                    onChange={(e) => setNewStore({...newStore, location: e.target.value})}
                    placeholder="如：北京朝阳区" 
                  />
                </div>
              </div>
            </div>
            <div className="flex gap-3 pt-4 border-t border-slate-100">
              <Button className="flex-1 bg-amber-600 hover:bg-amber-700" onClick={handleAddStore}>创建店铺</Button>
              <Button variant="ghost" onClick={() => setShowAddStore(false)}>取消</Button>
            </div>
          </Card>
        )}

        {/* Edit Store Form */}
        {showEditStore && editingStore && (
          <Card className="p-6 border-2 border-blue-500 bg-blue-50/10 animate-in zoom-in-95 duration-200">
            <h4 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
              <Edit className="w-4 h-4" /> 编辑店铺
            </h4>
            <div className="grid grid-cols-2 gap-6 mb-6">
              <div className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">店铺名称</label>
                  <Input 
                    value={editingStore.name}
                    onChange={(e) => setEditingStore({...editingStore, name: e.target.value})}
                    placeholder="请输入店铺名称" 
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">负责人</label>
                  <Input 
                    value={editingStore.owner}
                    onChange={(e) => setEditingStore({...editingStore, owner: e.target.value})}
                    placeholder="请输入负责人姓名" 
                  />
                </div>
              </div>
              <div className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">店铺类型</label>
                  <select 
                    value={editingStore.type}
                    onChange={(e) => setEditingStore({...editingStore, type: e.target.value})}
                    className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500/20"
                  >
                    <option>餐饮</option>
                    <option>饮品</option>
                    <option>住宿</option>
                    <option>零售</option>
                  </select>
                </div>
                <div className="space-y-1.5">
                  <label className="text-xs font-bold text-slate-500">所在地区</label>
                  <Input 
                    value={editingStore.location}
                    onChange={(e) => setEditingStore({...editingStore, location: e.target.value})}
                    placeholder="如：北京朝阳区" 
                  />
                </div>
              </div>
            </div>
            <div className="flex gap-3 pt-4 border-t border-slate-100">
              <Button className="flex-1 bg-blue-600 hover:bg-blue-700" onClick={handleUpdateStore}>更新店铺</Button>
              <Button variant="ghost" onClick={() => { setShowEditStore(false); setEditingStore(null); }}>取消</Button>
            </div>
          </Card>
        )}

        {/* View Store Detail */}
        {showViewDetail && viewingStore && (
          <Card className="p-6 border-2 border-green-500 bg-green-50/10 animate-in zoom-in-95 duration-200">
            <div className="flex justify-between items-start mb-6">
              <h4 className="font-bold text-slate-900 flex items-center gap-2">
                <Eye className="w-4 h-4" /> 店铺详情
              </h4>
              <Button variant="ghost" size="sm" onClick={() => { setShowViewDetail(false); setViewingStore(null); }}>
                ✕
              </Button>
            </div>
            <div className="grid grid-cols-2 gap-6">
              <div className="space-y-4">
                <div>
                  <p className="text-xs font-bold text-slate-500 mb-1">店铺名称</p>
                  <p className="text-sm text-slate-900">{viewingStore.name}</p>
                </div>
                <div>
                  <p className="text-xs font-bold text-slate-500 mb-1">负责人</p>
                  <p className="text-sm text-slate-900">{viewingStore.owner}</p>
                </div>
                <div>
                  <p className="text-xs font-bold text-slate-500 mb-1">店铺类型</p>
                  <Badge variant="outline">{viewingStore.type}</Badge>
                </div>
              </div>
              <div className="space-y-4">
                <div>
                  <p className="text-xs font-bold text-slate-500 mb-1">所在地区</p>
                  <p className="text-sm text-slate-900 flex items-center gap-1">
                    <MapPin className="w-3 h-3" /> {viewingStore.location}
                  </p>
                </div>
                <div>
                  <p className="text-xs font-bold text-slate-500 mb-1">状态</p>
                  <Badge className={
                    viewingStore.status === 'active' ? "bg-emerald-50 text-emerald-600" :
                    viewingStore.status === 'pending' ? "bg-amber-50 text-amber-600" :
                    "bg-slate-100 text-slate-400"
                  }>
                    {viewingStore.status === 'active' ? '正常运行' : viewingStore.status === 'pending' ? '待审核' : '已禁用'}
                  </Badge>
                </div>
                <div>
                  <p className="text-xs font-bold text-slate-500 mb-1">数据统计</p>
                  <p className="text-sm text-slate-900">{viewingStore.reviewCount} 评论 | 已接入 {viewingStore.platformCount} 个平台</p>
                </div>
              </div>
            </div>
          </Card>
        )}

        <Card className="p-4 border-none shadow-sm flex flex-wrap gap-4 items-center bg-white">
          <div className="relative flex-1 min-w-[300px]">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <Input 
              placeholder="搜索店铺名称、负责人或地区..." 
              className="pl-10" 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <select 
            className="bg-slate-50 border border-slate-200 rounded-md px-3 py-2 text-sm outline-none"
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
          >
            <option value="all">全部行业</option>
            <option>餐饮</option>
            <option>酒店</option>
            <option>零售</option>
          </select>
          <select 
            className="bg-slate-50 border border-slate-200 rounded-md px-3 py-2 text-sm outline-none"
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
          >
            <option value="all">全部状态</option>
            <option value="active">正常运行</option>
            <option value="pending">待激活</option>
            <option value="inactive">已禁用</option>
          </select>
        </Card>

        {/* Store Table */}
        <div className="bg-white rounded-xl shadow-sm overflow-hidden border border-slate-100">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50/50 border-b border-slate-100">
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">店铺信息</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">类型/地区</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">负责人</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">数据统计</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">状态</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-right">操作</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredStores.map((store) => (
                <tr key={store.id} className="hover:bg-slate-50/50 transition-colors">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-lg bg-indigo-50 flex items-center justify-center">
                        <Store className="w-5 h-5 text-indigo-600" />
                      </div>
                      <div>
                        <p className="font-bold text-slate-900">{store.name}</p>
                        <p className="text-xs text-slate-400">ID: ST-2026-0{store.id}</p>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="space-y-1">
                      <p className="text-sm text-slate-600">{store.type}</p>
                      <div className="flex items-center gap-1 text-[10px] text-slate-400">
                        <MapPin className="w-3 h-3" /> {store.location}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-slate-600 font-medium">
                    {store.owner}
                  </td>
                  <td className="px-6 py-4">
                    <div className="space-y-1">
                      <p className="text-sm font-semibold text-slate-700">{store.reviewCount} 评论</p>
                      <p className="text-[10px] text-slate-400">已接入 {store.platformCount} 个平台</p>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <Badge className={
                      store.status === 'active' ? "bg-emerald-50 text-emerald-600 border-none" :
                      store.status === 'pending' ? "bg-amber-50 text-amber-600 border-none" :
                      "bg-slate-100 text-slate-400 border-none"
                    }>
                      {store.status === 'active' ? '正常运行' : store.status === 'pending' ? '待审核' : '已禁用'}
                    </Badge>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <div className="flex justify-end gap-1">
                      {store.status === 'pending' && (
                        <Button 
                          variant="ghost" 
                          size="icon" 
                          className="h-8 w-8 text-emerald-600"
                          onClick={() => handleActivateStore(store.id)}
                        >
                          <CheckCircle2 className="w-4 h-4" />
                        </Button>
                      )}
                      <Button 
                        variant="ghost" 
                        size="icon" 
                        className="h-8 w-8 text-slate-400 hover:text-indigo-600"
                        onClick={() => handleEditStore(store.id)}
                      >
                        <Edit className="w-4 h-4" />
                      </Button>
                      <Button 
                        variant="ghost" 
                        size="icon" 
                        className="h-8 w-8 text-slate-400 hover:text-rose-600"
                        onClick={() => handleDeleteStore(store.id)}
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                      <Button 
                        variant="ghost" 
                        size="icon" 
                        className="h-8 w-8 text-slate-400 hover:text-green-600"
                        onClick={() => handleViewDetail(store.id)}
                      >
                        <Eye className="w-4 h-4" />
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {filteredStores.length === 0 && (
            <div className="text-center py-12">
              <Store className="w-12 h-12 text-slate-200 mx-auto mb-4" />
              <p className="text-sm text-slate-400">没有找到匹配的店铺</p>
            </div>
          )}
        </div>

        {/* Pagination */}
        <div className="flex justify-between items-center px-2 text-sm text-slate-500">
          <span>共 {filteredStores.length} 条记录</span>
          <div className="flex gap-2">
            <Button variant="ghost" size="sm" className="h-8" disabled>上一页</Button>
            <Button variant="ghost" size="sm" className="h-8 bg-slate-100">1</Button>
            <Button variant="ghost" size="sm" className="h-8">2</Button>
            <Button variant="ghost" size="sm" className="h-8">下一页</Button>
          </div>
        </div>
      </div>
    </AdminLayout>
  );
};

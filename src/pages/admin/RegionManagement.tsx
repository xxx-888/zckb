import React, { useState, useEffect, useCallback } from 'react';
import {
  Plus,
  Pencil,
  Trash2,
  Globe,
  List,
  ChevronRight,
  ChevronDown,
  MapPin,
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Skeleton } from '../../components/ui/skeleton';
import { regionApi, type Region, type RegionCreateRequest } from '@/api/region';
import { AdminLayout } from '../../components/AdminLayout';

const RegionManagement: React.FC = () => {
  const [regions, setRegions] = useState<Region[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'list' | 'tree'>('list');
  const [treeData, setTreeData] = useState<any[]>([]);
  const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set());

  // 创建/编辑对话框
  const [showDialog, setShowDialog] = useState(false);
  const [editingRegion, setEditingRegion] = useState<Region | null>(null);
  const [formData, setFormData] = useState<RegionCreateRequest>({
    name: '',
    level: 'province',
    parent_id: undefined,
    code: '',
  });

  // 获取区域列表
  const fetchRegions = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await regionApi.getRegions();
      setRegions(data || []);
    } catch (err: any) {
      setError(err?.message || '获取区域列表失败');
    } finally {
      setLoading(false);
    }
  }, []);

  // 获取树形结构
  const fetchTree = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await regionApi.getRegionTree();
      setTreeData(data || []);
    } catch (err: any) {
      setError(err?.message || '获取树形结构失败');
    } finally {
      setLoading(false);
    }
  }, []);

  // 初始加载
  useEffect(() => {
    if (viewMode === 'list') {
      fetchRegions();
    } else {
      fetchTree();
    }
  }, [viewMode, fetchRegions, fetchTree]);

  // 打开创建对话框
  const handleCreate = () => {
    setEditingRegion(null);
    setFormData({
      name: '',
      level: 'province',
      parent_id: undefined,
      code: '',
    });
    setShowDialog(true);
  };

  // 打开编辑对话框
  const handleEdit = (region: Region) => {
    setEditingRegion(region);
    setFormData({
      name: region.name,
      level: region.level as 'province' | 'city' | 'district',
      parent_id: region.parent_id || undefined,
      code: region.code || '',
    });
    setShowDialog(true);
  };

  // 保存区域
  const handleSave = async () => {
    try {
      if (editingRegion) {
        await regionApi.updateRegion(editingRegion.id, formData);
      } else {
        await regionApi.createRegion(formData);
      }
      setShowDialog(false);
      if (viewMode === 'list') {
        fetchRegions();
      } else {
        fetchTree();
      }
    } catch (err: any) {
      alert(err?.message || '保存失败');
    }
  };

  // 删除区域
  const handleDelete = async (region: Region) => {
    if (!window.confirm(`确定要删除区域「${region.name}」吗？\n\n注意：有关联门店或子级区域的区域无法删除。`)) {
      return;
    }
    try {
      await regionApi.deleteRegion(region.id);
      if (viewMode === 'list') {
        fetchRegions();
      } else {
        fetchTree();
      }
    } catch (err: any) {
      alert(err?.message || '删除失败');
    }
  };

  // 切换树节点展开/收起
  const toggleExpand = (id: string) => {
    setExpandedNodes(prev => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  // 渲染树节点
  const renderTreeNode = (node: any, depth: number = 0): React.ReactNode => {
    const hasChildren = node.children && node.children.length > 0;
    const isExpanded = expandedNodes.has(node.id);

    return (
      <div key={node.id}>
        <div
          className="flex items-center gap-2 px-4 py-2 hover:bg-slate-50 rounded-lg cursor-pointer"
          style={{ paddingLeft: `${depth * 24 + 16}px` }}
        >
          {hasChildren && (
            <button
              onClick={() => toggleExpand(node.id)}
              className="p-0.5 hover:bg-slate-200 rounded"
            >
              {isExpanded ? (
                <ChevronDown className="w-4 h-4 text-slate-400" />
              ) : (
                <ChevronRight className="w-4 h-4 text-slate-400" />
              )}
            </button>
          )}
          {!hasChildren && <div className="w-5" />}
          <MapPin className="w-4 h-4 text-orange-500" />
          <span className="flex-1 text-sm font-medium text-slate-700">{node.name}</span>
          <Badge className={
            node.level === 'province' ? 'bg-blue-50 text-blue-600' :
            node.level === 'city' ? 'bg-green-50 text-green-600' :
            'bg-amber-50 text-amber-600'
          }>
            {node.level === 'province' ? '省' : node.level === 'city' ? '市' : '区'}
          </Badge>
          {node.code && (
            <span className="text-xs text-slate-400">{node.code}</span>
          )}
          <button
            onClick={(e) => {
              e.stopPropagation();
              handleEdit({
                id: node.id,
                name: node.name,
                level: node.level,
                parent_id: null,
                code: node.code,
                created_at: null,
                updated_at: null,
              });
            }}
            className="p-1 hover:bg-slate-200 rounded"
          >
            <Pencil className="w-3.5 h-3.5 text-slate-400" />
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation();
              handleDelete({
                id: node.id,
                name: node.name,
                level: node.level,
                parent_id: null,
                code: node.code,
                created_at: null,
                updated_at: null,
              });
            }}
            className="p-1 hover:bg-red-100 rounded"
          >
            <Trash2 className="w-3.5 h-3.5 text-red-400" />
          </button>
        </div>
        {isExpanded && hasChildren && (
          <div>
            {node.children.map((child: any) => renderTreeNode(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  return (
    <AdminLayout>
      <div className="p-6 max-w-7xl mx-auto">
        {/* 页面标题 */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-slate-900">区域管理</h1>
            <p className="text-sm text-slate-500 mt-1">管理省/市/区层级区域</p>
          </div>
        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setViewMode(viewMode === 'list' ? 'tree' : 'list')}
            className="gap-2"
          >
            {viewMode === 'list' ? <Globe className="w-4 h-4" /> : <List className="w-4 h-4" />}
            {viewMode === 'list' ? '树形视图' : '列表视图'}
          </Button>
          <Button onClick={handleCreate} className="gap-2 bg-orange-500 hover:bg-orange-600 text-white">
            <Plus className="w-4 h-4" />
            新增区域
          </Button>
        </div>
      </div>

      {/* 错误提示 */}
      {error && (
        <Card className="p-4 mb-4 bg-rose-50 border-rose-200">
          <p className="text-sm text-rose-600">{error}</p>
        </Card>
      )}

      {/* 加载状态 */}
      {loading && (
        <div className="space-y-4">
          <Skeleton lines={5} className="space-y-3" />
        </div>
      )}

      {/* 列表视图 */}
      {!loading && viewMode === 'list' && (
        <Card className="p-0 overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-100">
                <th className="text-left px-4 py-3 text-sm font-semibold text-slate-600">名称</th>
                <th className="text-left px-4 py-3 text-sm font-semibold text-slate-600">层级</th>
                <th className="text-left px-4 py-3 text-sm font-semibold text-slate-600">区划代码</th>
                <th className="text-left px-4 py-3 text-sm font-semibold text-slate-600">父级区域</th>
                <th className="text-right px-4 py-3 text-sm font-semibold text-slate-600">操作</th>
              </tr>
            </thead>
            <tbody>
              {regions.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-4 py-8 text-center text-slate-400">
                    暂无数据
                  </td>
                </tr>
              ) : (
                regions.map((region) => (
                  <tr key={region.id} className="border-b border-slate-50 hover:bg-slate-50">
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <MapPin className="w-4 h-4 text-orange-500" />
                        <span className="text-sm font-medium text-slate-700">{region.name}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <Badge className={
                        region.level === 'province' ? 'bg-blue-50 text-blue-600' :
                        region.level === 'city' ? 'bg-green-50 text-green-600' :
                        'bg-amber-50 text-amber-600'
                      }>
                        {region.level === 'province' ? '省' : region.level === 'city' ? '市' : '区'}
                      </Badge>
                    </td>
                    <td className="px-4 py-3 text-sm text-slate-600">
                      {region.code || '-'}
                    </td>
                    <td className="px-4 py-3 text-sm text-slate-600">
                      {region.parent?.name || '-'}
                    </td>
                    <td className="px-4 py-3 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleEdit(region)}
                          className="p-1.5 hover:bg-slate-100 rounded-lg"
                        >
                          <Pencil className="w-4 h-4 text-slate-400" />
                        </button>
                        <button
                          onClick={() => handleDelete(region)}
                          className="p-1.5 hover:bg-red-100 rounded-lg"
                        >
                          <Trash2 className="w-4 h-4 text-red-400" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </Card>
      )}

      {/* 树形视图 */}
      {!loading && viewMode === 'tree' && (
        <Card className="p-4">
          {treeData.length === 0 ? (
            <div className="text-center py-8 text-slate-400">暂无数据</div>
          ) : (
            <div className="space-y-1">
              {treeData.map((node) => renderTreeNode(node))}
            </div>
          )}
        </Card>
      )}

      {/* 创建/编辑对话框 */}
      {showDialog && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <Card className="w-full max-w-md p-6">
            <h3 className="text-lg font-bold text-slate-900 mb-4">
              {editingRegion ? '编辑区域' : '新增区域'}
            </h3>
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-slate-700">名称</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full mt-1 px-3 py-2 border border-slate-200 rounded-lg text-sm"
                  placeholder="请输入区域名称"
                />
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700">层级</label>
                <select
                  value={formData.level}
                  onChange={(e) => setFormData({ ...formData, level: e.target.value as any })}
                  className="w-full mt-1 px-3 py-2 border border-slate-200 rounded-lg text-sm"
                >
                  <option value="province">省</option>
                  <option value="city">市</option>
                  <option value="district">区</option>
                </select>
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700">父级区域</label>
                <select
                  value={formData.parent_id || ''}
                  onChange={(e) => setFormData({ ...formData, parent_id: e.target.value || undefined })}
                  className="w-full mt-1 px-3 py-2 border border-slate-200 rounded-lg text-sm"
                >
                  <option value="">无（顶级）</option>
                  {regions
                    .filter(r => r.level === 'province' || r.level === 'city')
                    .map(r => (
                      <option key={r.id} value={r.id}>{r.name}</option>
                    ))}
                </select>
              </div>
              <div>
                <label className="text-sm font-medium text-slate-700">区划代码</label>
                <input
                  type="text"
                  value={formData.code || ''}
                  onChange={(e) => setFormData({ ...formData, code: e.target.value || undefined })}
                  className="w-full mt-1 px-3 py-2 border border-slate-200 rounded-lg text-sm"
                  placeholder="请输入区划代码（可选）"
                />
              </div>
            </div>
            <div className="flex items-center justify-end gap-3 mt-6">
              <Button variant="outline" onClick={() => setShowDialog(false)}>
                取消
              </Button>
              <Button onClick={handleSave} className="bg-orange-500 hover:bg-orange-600 text-white">
                {editingRegion ? '更新' : '创建'}
              </Button>
            </div>
          </Card>
        </div>
      )}
    </div>
  </AdminLayout>
  );
};

export default RegionManagement;

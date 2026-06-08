import React, { useState, useEffect, useCallback } from 'react';
import {
  Plus, Pencil, Trash2, X, Loader2, Search, Database,
  Wallet, Package, BarChart3, FileText, ChevronLeft, ChevronRight,
  Download, Upload,
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { useToast } from '../../hooks/use-toast';
import { AdminLayout } from '../../components/AdminLayout';
import {
  fetchStores,
  fetchRevenueList, createRevenue, updateRevenue, deleteRevenue, batchCreateRevenue,
  fetchPackageList, createPackage, updatePackage, deletePackage, batchCreatePackages,
  fetchMetricList, createMetric, updateMetric, deleteMetric, batchCreateMetrics,
  fetchAnalysisList, createAnalysis, updateAnalysis, deleteAnalysis,
  type StoreOption,
  type RevenueRecord,
  type PackageRecord,
  type StoreMetricRecord,
  type OperationAnalysisRecord,
} from '../../api/adminDashboardData';

type Tab = 'revenue' | 'packages' | 'metrics' | 'analysis';

const tabConfig: { key: Tab; label: string; icon: React.ElementType; desc: string }[] = [
  { key: 'revenue', label: '营业额', icon: Wallet, desc: '每日营业额、到店人数、桌数等' },
  { key: 'packages', label: '套餐核销', icon: Package, desc: '团购套餐购买和核销数据' },
  { key: 'metrics', label: '运营指标', icon: BarChart3, desc: '曝光、访问、购买、星级等' },
  { key: 'analysis', label: '分析意见', icon: FileText, desc: '运营分析和下周目标' },
];

export const DashboardDataManager: React.FC = () => {
  const { success: toastSuccess, error: toastError } = useToast();
  const [activeTab, setActiveTab] = useState<Tab>('revenue');
  const [stores, setStores] = useState<StoreOption[]>([]);
  const [loadingStores, setLoadingStores] = useState(true);

  // 加载门店列表
  useEffect(() => {
    fetchStores().then(list => { setStores(list); setLoadingStores(false); }).catch(() => setLoadingStores(false));
  }, []);

  const storeMap = React.useMemo(() => {
    const m: Record<string, string> = {};
    stores.forEach(s => m[s.id] = s.name);
    return m;
  }, [stores]);

  return (
    <AdminLayout>
      <div className="p-6 space-y-6">
        {/* 页头 */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
              <Database className="text-white w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-900">经营数据管理</h1>
              <p className="text-sm text-slate-500">录入和管理门店营业数据，移动端看板的数据来源</p>
            </div>
          </div>
          {loadingStores && <Loader2 className="w-5 h-5 animate-spin text-slate-400" />}
        </div>

        {/* Tab 切换 */}
        <div className="flex gap-2 border-b border-slate-200 pb-0">
          {tabConfig.map(tab => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                activeTab === tab.key
                  ? 'border-indigo-600 text-indigo-600'
                  : 'border-transparent text-slate-500 hover:text-slate-700'
              }`}
            >
              <tab.icon className="w-4 h-4" />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab 内容 */}
        {activeTab === 'revenue' && (
          <RevenueTab stores={stores} storeMap={storeMap} toastSuccess={toastSuccess} toastError={toastError} />
        )}
        {activeTab === 'packages' && (
          <PackageTab stores={stores} storeMap={storeMap} toastSuccess={toastSuccess} toastError={toastError} />
        )}
        {activeTab === 'metrics' && (
          <MetricTab stores={stores} storeMap={storeMap} toastSuccess={toastSuccess} toastError={toastError} />
        )}
        {activeTab === 'analysis' && (
          <AnalysisTab stores={stores} storeMap={storeMap} toastSuccess={toastSuccess} toastError={toastError} />
        )}
      </div>
    </AdminLayout>
  );
};

// ==================== 分页组件 ====================

function Pagination({ page, pageSize, total, onPageChange }: {
  page: number; pageSize: number; total: number; onPageChange: (p: number) => void;
}) {
  const totalPages = Math.ceil(total / pageSize);
  if (totalPages <= 1) return null;
  return (
    <div className="flex items-center justify-between pt-4 border-t border-slate-100">
      <span className="text-xs text-slate-500">共 {total} 条记录</span>
      <div className="flex items-center gap-2">
        <Button size="sm" variant="outline" disabled={page <= 1} onClick={() => onPageChange(page - 1)}>
          <ChevronLeft className="w-3 h-3" />
        </Button>
        <span className="text-xs text-slate-600">{page} / {totalPages}</span>
        <Button size="sm" variant="outline" disabled={page >= totalPages} onClick={() => onPageChange(page + 1)}>
          <ChevronRight className="w-3 h-3" />
        </Button>
      </div>
    </div>
  );
}

// ==================== 通用筛选栏 ====================

function FilterBar({ storeId, dateFrom, dateTo, onStoreChange, onDateFromChange, onDateToDateChange, stores, extraFilter }: {
  storeId: string; dateFrom: string; dateTo: string;
  onStoreChange: (v: string) => void; onDateFromChange: (v: string) => void; onDateToDateChange: (v: string) => void;
  stores: StoreOption[]; extraFilter?: React.ReactNode;
}) {
  return (
    <div className="flex flex-wrap items-center gap-3 p-3 bg-slate-50 rounded-xl">
      <select value={storeId} onChange={e => onStoreChange(e.target.value)}
        className="px-3 py-1.5 text-sm border border-slate-200 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500">
        <option value="">全部门店</option>
        {stores.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
      </select>
      <input type="date" value={dateFrom} onChange={e => onDateFromChange(e.target.value)}
        className="px-3 py-1.5 text-sm border border-slate-200 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500" />
      <span className="text-slate-400">~</span>
      <input type="date" value={dateTo} onChange={e => onDateToDateChange(e.target.value)}
        className="px-3 py-1.5 text-sm border border-slate-200 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500" />
      {extraFilter}
    </div>
  );
}

// ==================== 营业额 Tab ====================

function RevenueTab({ stores, storeMap, toastSuccess, toastError }: {
  stores: StoreOption[]; storeMap: Record<string, string>;
  toastSuccess: (title: string, msg?: string) => void; toastError: (title: string, msg?: string) => void;
}) {
  const [data, setData] = useState<RevenueRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<RevenueRecord | null>(null);
  const [storeId, setStoreId] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [form, setForm] = useState({
    store_id: '', record_date: '', total_revenue: 0, meituan_revenue: 0, douyin_revenue: 0, other_revenue: 0,
    visitor_count: 0, table_count: 0, avg_people_per_table: 0, avg_per_capita: 0, notes: '',
  });

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const res = await fetchRevenueList({ store_id: storeId || undefined, start_date: dateFrom || undefined, end_date: dateTo || undefined, page, page_size: 20 });
      setData(res.items); setTotal(res.total);
    } catch { toastError('加载失败'); } finally { setLoading(false); }
  }, [storeId, dateFrom, dateTo, page]);

  useEffect(() => { loadData(); }, [loadData]);

  const handleSave = async () => {
    if (!form.store_id || !form.record_date) return toastError('保存失败', '请选择门店和日期');
    try {
      setActionLoading(true);
      if (editing) {
        await updateRevenue(editing.id, form);
      } else {
        await createRevenue(form);
      }
      toastSuccess(editing ? '更新成功' : '创建成功');
      setShowModal(false); loadData();
    } catch (e: any) { toastError('保存失败', e?.message); } finally { setActionLoading(false); }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('确定删除这条记录？')) return;
    try { await deleteRevenue(id); toastSuccess('删除成功'); loadData(); } catch { toastError('删除失败'); }
  };

  const openCreate = () => {
    setEditing(null);
    setForm({ store_id: stores[0]?.id || '', record_date: new Date().toISOString().slice(0, 10), total_revenue: 0, meituan_revenue: 0, douyin_revenue: 0, other_revenue: 0, visitor_count: 0, table_count: 0, avg_people_per_table: 0, avg_per_capita: 0, notes: '' });
    setShowModal(true);
  };

  const openEdit = (r: RevenueRecord) => {
    setEditing(r);
    setForm({
      store_id: r.store_id, record_date: r.record_date, total_revenue: r.total_revenue, meituan_revenue: r.meituan_revenue,
      douyin_revenue: r.douyin_revenue, other_revenue: r.other_revenue, visitor_count: r.visitor_count, table_count: r.table_count,
      avg_people_per_table: r.avg_people_per_table, avg_per_capita: r.avg_per_capita, notes: r.notes || '',
    });
    setShowModal(true);
  };

  const inputCls = "w-full px-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500";

  return (
    <div className="space-y-4">
      <FilterBar storeId={storeId} dateFrom={dateFrom} dateTo={dateTo} onStoreChange={v => { setStoreId(v); setPage(1); }} onDateFromChange={v => { setDateFrom(v); setPage(1); }} onDateToDateChange={v => { setDateTo(v); setPage(1); }} stores={stores} />

      <div className="flex items-center justify-between">
        <span className="text-sm text-slate-500">{total} 条记录</span>
        <Button size="sm" onClick={openCreate}><Plus className="w-4 h-4 mr-1" />录入营业额</Button>
      </div>

      {loading ? <div className="py-10 text-center text-slate-400"><Loader2 className="w-6 h-6 animate-spin mx-auto" /></div> : (
        <Card className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 text-slate-600">
                <tr>
                  <th className="px-3 py-2 text-left font-medium">日期</th>
                  <th className="px-3 py-2 text-left font-medium">门店</th>
                  <th className="px-3 py-2 text-right font-medium">总营业额</th>
                  <th className="px-3 py-2 text-right font-medium">美团</th>
                  <th className="px-3 py-2 text-right font-medium">抖音</th>
                  <th className="px-3 py-2 text-right font-medium">到店人数</th>
                  <th className="px-3 py-2 text-right font-medium">桌数</th>
                  <th className="px-3 py-2 text-right font-medium">人均</th>
                  <th className="px-3 py-2 text-center font-medium">操作</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {data.length === 0 ? (
                  <tr><td colSpan={9} className="px-3 py-10 text-center text-slate-400">暂无数据，点击右上角录入</td></tr>
                ) : data.map(r => (
                  <tr key={r.id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-3 py-2 text-slate-700">{r.record_date}</td>
                    <td className="px-3 py-2 text-slate-700">{r.store_name || storeMap[r.store_id] || '-'}</td>
                    <td className="px-3 py-2 text-right font-medium text-indigo-600">¥{r.total_revenue.toLocaleString()}</td>
                    <td className="px-3 py-2 text-right text-amber-600">¥{r.meituan_revenue.toLocaleString()}</td>
                    <td className="px-3 py-2 text-right text-slate-900">¥{r.douyin_revenue.toLocaleString()}</td>
                    <td className="px-3 py-2 text-right">{r.visitor_count}</td>
                    <td className="px-3 py-2 text-right">{r.table_count}</td>
                    <td className="px-3 py-2 text-right">¥{r.avg_per_capita}</td>
                    <td className="px-3 py-2 text-center">
                      <div className="flex items-center justify-center gap-1">
                        <button onClick={() => openEdit(r)} className="p-1 text-slate-400 hover:text-indigo-600 transition-colors"><Pencil className="w-3.5 h-3.5" /></button>
                        <button onClick={() => handleDelete(r.id)} className="p-1 text-slate-400 hover:text-rose-600 transition-colors"><Trash2 className="w-3.5 h-3.5" /></button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <Pagination page={page} pageSize={20} total={total} onPageChange={setPage} />
        </Card>
      )}

      {/* 弹窗 */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" onClick={() => setShowModal(false)}>
          <div className="bg-white rounded-2xl shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between p-4 border-b border-slate-100">
              <h3 className="text-lg font-bold">{editing ? '编辑营业额' : '录入营业额'}</h3>
              <button onClick={() => setShowModal(false)} className="p-1 hover:bg-slate-100 rounded-lg"><X className="w-5 h-5" /></button>
            </div>
            <div className="p-4 space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs text-slate-500 mb-1">门店 *</label>
                  <select value={form.store_id} onChange={e => setForm({ ...form, store_id: e.target.value })} className={inputCls}>
                    {stores.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-xs text-slate-500 mb-1">日期 *</label>
                  <input type="date" value={form.record_date} onChange={e => setForm({ ...form, record_date: e.target.value })} className={inputCls} />
                </div>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block text-xs text-slate-500 mb-1">总营业额</label>
                  <input type="number" value={form.total_revenue} onChange={e => setForm({ ...form, total_revenue: +e.target.value })} className={inputCls} />
                </div>
                <div>
                  <label className="block text-xs text-slate-500 mb-1">美团营业额</label>
                  <input type="number" value={form.meituan_revenue} onChange={e => setForm({ ...form, meituan_revenue: +e.target.value })} className={inputCls} />
                </div>
                <div>
                  <label className="block text-xs text-slate-500 mb-1">抖音营业额</label>
                  <input type="number" value={form.douyin_revenue} onChange={e => setForm({ ...form, douyin_revenue: +e.target.value })} className={inputCls} />
                </div>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block text-xs text-slate-500 mb-1">其他收入</label>
                  <input type="number" value={form.other_revenue} onChange={e => setForm({ ...form, other_revenue: +e.target.value })} className={inputCls} />
                </div>
                <div>
                  <label className="block text-xs text-slate-500 mb-1">到店人数</label>
                  <input type="number" value={form.visitor_count} onChange={e => setForm({ ...form, visitor_count: +e.target.value })} className={inputCls} />
                </div>
                <div>
                  <label className="block text-xs text-slate-500 mb-1">接待桌数</label>
                  <input type="number" value={form.table_count} onChange={e => setForm({ ...form, table_count: +e.target.value })} className={inputCls} />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs text-slate-500 mb-1">桌均人数</label>
                  <input type="number" step="0.1" value={form.avg_people_per_table} onChange={e => setForm({ ...form, avg_people_per_table: +e.target.value })} className={inputCls} />
                </div>
                <div>
                  <label className="block text-xs text-slate-500 mb-1">人均消费</label>
                  <input type="number" step="0.1" value={form.avg_per_capita} onChange={e => setForm({ ...form, avg_per_capita: +e.target.value })} className={inputCls} />
                </div>
              </div>
              <div>
                <label className="block text-xs text-slate-500 mb-1">备注</label>
                <textarea value={form.notes} onChange={e => setForm({ ...form, notes: e.target.value })} className={inputCls} rows={2} />
              </div>
            </div>
            <div className="flex items-center justify-end gap-2 p-4 border-t border-slate-100">
              <Button variant="outline" onClick={() => setShowModal(false)}>取消</Button>
              <Button onClick={handleSave} disabled={actionLoading}>
                {actionLoading && <Loader2 className="w-4 h-4 animate-spin mr-1" />}
                {editing ? '保存' : '创建'}
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ==================== 套餐核销 Tab ====================

function PackageTab({ stores, storeMap, toastSuccess, toastError }: {
  stores: StoreOption[]; storeMap: Record<string, string>;
  toastSuccess: (title: string, msg?: string) => void; toastError: (title: string, msg?: string) => void;
}) {
  const [data, setData] = useState<PackageRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<PackageRecord | null>(null);
  const [storeId, setStoreId] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [searchName, setSearchName] = useState('');
  const [form, setForm] = useState({
    store_id: '', period_start: '', period_end: '', product_name: '', meituan_buy: 0, meituan_verify: 0, douyin_buy: 0, douyin_verify: 0, notes: '',
  });

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const res = await fetchPackageList({ store_id: storeId || undefined, start_date: dateFrom || undefined, end_date: dateTo || undefined, product_name: searchName || undefined, page, page_size: 20 });
      setData(res.items); setTotal(res.total);
    } catch { toastError('加载失败'); } finally { setLoading(false); }
  }, [storeId, dateFrom, dateTo, searchName, page]);

  useEffect(() => { loadData(); }, [loadData]);

  const handleSave = async () => {
    if (!form.store_id || !form.product_name || !form.period_start || !form.period_end) return toastError('保存失败', '请填写必填项');
    try {
      setActionLoading(true);
      if (editing) { await updatePackage(editing.id, form); } else { await createPackage(form); }
      toastSuccess(editing ? '更新成功' : '创建成功'); setShowModal(false); loadData();
    } catch (e: any) { toastError('保存失败', e?.message); } finally { setActionLoading(false); }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('确定删除？')) return;
    try { await deletePackage(id); toastSuccess('删除成功'); loadData(); } catch { toastError('删除失败'); }
  };

  const openCreate = () => {
    setEditing(null);
    const today = new Date().toISOString().slice(0, 10);
    setForm({ store_id: stores[0]?.id || '', period_start: today, period_end: today, product_name: '', meituan_buy: 0, meituan_verify: 0, douyin_buy: 0, douyin_verify: 0, notes: '' });
    setShowModal(true);
  };

  const openEdit = (r: PackageRecord) => {
    setEditing(r);
    setForm({ store_id: r.store_id, period_start: r.period_start, period_end: r.period_end, product_name: r.product_name, meituan_buy: r.meituan_buy, meituan_verify: r.meituan_verify, douyin_buy: r.douyin_buy, douyin_verify: r.douyin_verify, notes: r.notes || '' });
    setShowModal(true);
  };

  const inputCls = "w-full px-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500";

  return (
    <div className="space-y-4">
      <FilterBar storeId={storeId} dateFrom={dateFrom} dateTo={dateTo}
        onStoreChange={v => { setStoreId(v); setPage(1); }} onDateFromChange={v => { setDateFrom(v); setPage(1); }} onDateToDateChange={v => { setDateTo(v); setPage(1); }} stores={stores}
        extraFilter={<input type="text" placeholder="搜索商品名称..." value={searchName} onChange={e => { setSearchName(e.target.value); setPage(1); }} className="px-3 py-1.5 text-sm border border-slate-200 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500 w-40" />} />

      <div className="flex items-center justify-between">
        <span className="text-sm text-slate-500">{total} 条记录</span>
        <Button size="sm" onClick={openCreate}><Plus className="w-4 h-4 mr-1" />录入套餐</Button>
      </div>

      {loading ? <div className="py-10 text-center text-slate-400"><Loader2 className="w-6 h-6 animate-spin mx-auto" /></div> : (
        <Card className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 text-slate-600">
                <tr>
                  <th className="px-3 py-2 text-left font-medium">周期</th>
                  <th className="px-3 py-2 text-left font-medium">门店</th>
                  <th className="px-3 py-2 text-left font-medium">商品名称</th>
                  <th className="px-3 py-2 text-right font-medium">美团购买</th>
                  <th className="px-3 py-2 text-right font-medium">美团核销</th>
                  <th className="px-3 py-2 text-right font-medium">抖音购买</th>
                  <th className="px-3 py-2 text-right font-medium">抖音核销</th>
                  <th className="px-3 py-2 text-center font-medium">操作</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {data.length === 0 ? (
                  <tr><td colSpan={8} className="px-3 py-10 text-center text-slate-400">暂无数据</td></tr>
                ) : data.map(r => (
                  <tr key={r.id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-3 py-2 text-slate-500 text-xs">{r.period_start} ~ {r.period_end}</td>
                    <td className="px-3 py-2 text-slate-700">{r.store_name || storeMap[r.store_id] || '-'}</td>
                    <td className="px-3 py-2 text-slate-700 font-medium">{r.product_name}</td>
                    <td className="px-3 py-2 text-right">{r.meituan_buy}</td>
                    <td className="px-3 py-2 text-right text-amber-600 font-medium">{r.meituan_verify}</td>
                    <td className="px-3 py-2 text-right">{r.douyin_buy}</td>
                    <td className="px-3 py-2 text-right text-slate-900 font-medium">{r.douyin_verify}</td>
                    <td className="px-3 py-2 text-center">
                      <div className="flex items-center justify-center gap-1">
                        <button onClick={() => openEdit(r)} className="p-1 text-slate-400 hover:text-indigo-600"><Pencil className="w-3.5 h-3.5" /></button>
                        <button onClick={() => handleDelete(r.id)} className="p-1 text-slate-400 hover:text-rose-600"><Trash2 className="w-3.5 h-3.5" /></button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <Pagination page={page} pageSize={20} total={total} onPageChange={setPage} />
        </Card>
      )}

      {showModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" onClick={() => setShowModal(false)}>
          <div className="bg-white rounded-2xl shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between p-4 border-b border-slate-100">
              <h3 className="text-lg font-bold">{editing ? '编辑套餐' : '录入套餐'}</h3>
              <button onClick={() => setShowModal(false)} className="p-1 hover:bg-slate-100 rounded-lg"><X className="w-5 h-5" /></button>
            </div>
            <div className="p-4 space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs text-slate-500 mb-1">门店 *</label>
                  <select value={form.store_id} onChange={e => setForm({ ...form, store_id: e.target.value })} className={inputCls}>
                    {stores.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-xs text-slate-500 mb-1">商品名称 *</label>
                  <input type="text" value={form.product_name} onChange={e => setForm({ ...form, product_name: e.target.value })} className={inputCls} />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs text-slate-500 mb-1">周期开始 *</label>
                  <input type="date" value={form.period_start} onChange={e => setForm({ ...form, period_start: e.target.value })} className={inputCls} />
                </div>
                <div>
                  <label className="block text-xs text-slate-500 mb-1">周期结束 *</label>
                  <input type="date" value={form.period_end} onChange={e => setForm({ ...form, period_end: e.target.value })} className={inputCls} />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs text-slate-500 mb-1">美团购买数</label>
                  <input type="number" value={form.meituan_buy} onChange={e => setForm({ ...form, meituan_buy: +e.target.value })} className={inputCls} />
                </div>
                <div>
                  <label className="block text-xs text-slate-500 mb-1">美团核销数</label>
                  <input type="number" value={form.meituan_verify} onChange={e => setForm({ ...form, meituan_verify: +e.target.value })} className={inputCls} />
                </div>
                <div>
                  <label className="block text-xs text-slate-500 mb-1">抖音购买数</label>
                  <input type="number" value={form.douyin_buy} onChange={e => setForm({ ...form, douyin_buy: +e.target.value })} className={inputCls} />
                </div>
                <div>
                  <label className="block text-xs text-slate-500 mb-1">抖音核销数</label>
                  <input type="number" value={form.douyin_verify} onChange={e => setForm({ ...form, douyin_verify: +e.target.value })} className={inputCls} />
                </div>
              </div>
              <div>
                <label className="block text-xs text-slate-500 mb-1">备注</label>
                <textarea value={form.notes} onChange={e => setForm({ ...form, notes: e.target.value })} className={inputCls} rows={2} />
              </div>
            </div>
            <div className="flex items-center justify-end gap-2 p-4 border-t border-slate-100">
              <Button variant="outline" onClick={() => setShowModal(false)}>取消</Button>
              <Button onClick={handleSave} disabled={actionLoading}>{actionLoading && <Loader2 className="w-4 h-4 animate-spin mr-1" />}{editing ? '保存' : '创建'}</Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ==================== 运营指标 Tab ====================

function MetricTab({ stores, storeMap, toastSuccess, toastError }: {
  stores: StoreOption[]; storeMap: Record<string, string>;
  toastSuccess: (title: string, msg?: string) => void; toastError: (title: string, msg?: string) => void;
}) {
  const [data, setData] = useState<StoreMetricRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<StoreMetricRecord | null>(null);
  const [storeId, setStoreId] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [platform, setPlatform] = useState('');
  const [form, setForm] = useState({
    store_id: '', metric_date: '', platform: '美团', ranking_name: '', ranking_position: '', star_rating: 0,
    impressions: 0, visits: 0, purchases: 0, verifications: 0, new_favorites: 0, checkins: 0, scan_count: 0,
    product_impressions: 0, product_visits: 0, product_purchases: 0, new_reviews: 0, new_bad_reviews: 0,
    bad_keywords: '', notes: '',
  });

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const res = await fetchMetricList({ store_id: storeId || undefined, start_date: dateFrom || undefined, end_date: dateTo || undefined, platform: platform || undefined, page, page_size: 20 });
      setData(res.items); setTotal(res.total);
    } catch { toastError('加载失败'); } finally { setLoading(false); }
  }, [storeId, dateFrom, dateTo, platform, page]);

  useEffect(() => { loadData(); }, [loadData]);

  const handleSave = async () => {
    if (!form.store_id || !form.metric_date || !form.platform) return toastError('保存失败', '请填写必填项');
    try {
      setActionLoading(true);
      const payload = { ...form, bad_keywords: form.bad_keywords ? form.bad_keywords.split('，').map(s => s.trim()).filter(Boolean) : [] };
      if (editing) { await updateMetric(editing.id, payload); } else { await createMetric(payload); }
      toastSuccess(editing ? '更新成功' : '创建成功'); setShowModal(false); loadData();
    } catch (e: any) { toastError('保存失败', e?.message); } finally { setActionLoading(false); }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('确定删除？')) return;
    try { await deleteMetric(id); toastSuccess('删除成功'); loadData(); } catch { toastError('删除失败'); }
  };

  const openCreate = () => {
    setEditing(null);
    setForm({ store_id: stores[0]?.id || '', metric_date: new Date().toISOString().slice(0, 10), platform: '美团', ranking_name: '', ranking_position: '', star_rating: 0, impressions: 0, visits: 0, purchases: 0, verifications: 0, new_favorites: 0, checkins: 0, scan_count: 0, product_impressions: 0, product_visits: 0, product_purchases: 0, new_reviews: 0, new_bad_reviews: 0, bad_keywords: '', notes: '' });
    setShowModal(true);
  };

  const openEdit = (r: StoreMetricRecord) => {
    setEditing(r);
    setForm({ store_id: r.store_id, metric_date: r.metric_date, platform: r.platform, ranking_name: r.ranking_name || '', ranking_position: r.ranking_position || '', star_rating: r.star_rating || 0, impressions: r.impressions || 0, visits: r.visits || 0, purchases: r.purchases || 0, verifications: r.verifications || 0, new_favorites: r.new_favorites || 0, checkins: r.checkins || 0, scan_count: r.scan_count || 0, product_impressions: r.product_impressions || 0, product_visits: r.product_visits || 0, product_purchases: r.product_purchases || 0, new_reviews: r.new_reviews || 0, new_bad_reviews: r.new_bad_reviews || 0, bad_keywords: r.bad_keywords?.join('，') || '', notes: r.notes || '' });
    setShowModal(true);
  };

  const inputCls = "w-full px-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500";
  const platformColors: Record<string, string> = { '美团': 'bg-yellow-100 text-yellow-700', '点评': 'bg-orange-100 text-orange-700', '抖音': 'bg-slate-100 text-slate-700' };

  return (
    <div className="space-y-4">
      <FilterBar storeId={storeId} dateFrom={dateFrom} dateTo={dateTo}
        onStoreChange={v => { setStoreId(v); setPage(1); }} onDateFromChange={v => { setDateFrom(v); setPage(1); }} onDateToDateChange={v => { setDateTo(v); setPage(1); }} stores={stores}
        extraFilter={<select value={platform} onChange={e => { setPlatform(e.target.value); setPage(1); }} className="px-3 py-1.5 text-sm border border-slate-200 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"><option value="">全部平台</option><option>美团</option><option>点评</option><option>抖音</option></select>} />

      <div className="flex items-center justify-between">
        <span className="text-sm text-slate-500">{total} 条记录</span>
        <Button size="sm" onClick={openCreate}><Plus className="w-4 h-4 mr-1" />录入指标</Button>
      </div>

      {loading ? <div className="py-10 text-center text-slate-400"><Loader2 className="w-6 h-6 animate-spin mx-auto" /></div> : (
        <Card className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 text-slate-600">
                <tr>
                  <th className="px-3 py-2 text-left font-medium">日期</th>
                  <th className="px-3 py-2 text-left font-medium">门店</th>
                  <th className="px-3 py-2 text-left font-medium">平台</th>
                  <th className="px-3 py-2 text-right font-medium">曝光</th>
                  <th className="px-3 py-2 text-right font-medium">访问</th>
                  <th className="px-3 py-2 text-right font-medium">购买</th>
                  <th className="px-3 py-2 text-right font-medium">核销</th>
                  <th className="px-3 py-2 text-right font-medium">星级</th>
                  <th className="px-3 py-2 text-left font-medium">榜单</th>
                  <th className="px-3 py-2 text-center font-medium">操作</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {data.length === 0 ? (
                  <tr><td colSpan={10} className="px-3 py-10 text-center text-slate-400">暂无数据</td></tr>
                ) : data.map(r => (
                  <tr key={r.id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-3 py-2 text-slate-500 text-xs">{r.metric_date}</td>
                    <td className="px-3 py-2 text-slate-700">{r.store_name || storeMap[r.store_id] || '-'}</td>
                    <td className="px-3 py-2"><Badge variant="secondary" className={platformColors[r.platform] || ''}>{r.platform}</Badge></td>
                    <td className="px-3 py-2 text-right">{r.impressions || '-'}</td>
                    <td className="px-3 py-2 text-right">{r.visits || '-'}</td>
                    <td className="px-3 py-2 text-right">{r.purchases || '-'}</td>
                    <td className="px-3 py-2 text-right">{r.verifications || '-'}</td>
                    <td className="px-3 py-2 text-right font-medium">{r.star_rating || '-'}</td>
                    <td className="px-3 py-2 text-xs text-slate-500">{r.ranking_position || '-'}</td>
                    <td className="px-3 py-2 text-center">
                      <div className="flex items-center justify-center gap-1">
                        <button onClick={() => openEdit(r)} className="p-1 text-slate-400 hover:text-indigo-600"><Pencil className="w-3.5 h-3.5" /></button>
                        <button onClick={() => handleDelete(r.id)} className="p-1 text-slate-400 hover:text-rose-600"><Trash2 className="w-3.5 h-3.5" /></button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <Pagination page={page} pageSize={20} total={total} onPageChange={setPage} />
        </Card>
      )}

      {showModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" onClick={() => setShowModal(false)}>
          <div className="bg-white rounded-2xl shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between p-4 border-b border-slate-100">
              <h3 className="text-lg font-bold">{editing ? '编辑指标' : '录入指标'}</h3>
              <button onClick={() => setShowModal(false)} className="p-1 hover:bg-slate-100 rounded-lg"><X className="w-5 h-5" /></button>
            </div>
            <div className="p-4 space-y-3">
              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block text-xs text-slate-500 mb-1">门店 *</label>
                  <select value={form.store_id} onChange={e => setForm({ ...form, store_id: e.target.value })} className={inputCls}>
                    {stores.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-xs text-slate-500 mb-1">日期 *</label>
                  <input type="date" value={form.metric_date} onChange={e => setForm({ ...form, metric_date: e.target.value })} className={inputCls} />
                </div>
                <div>
                  <label className="block text-xs text-slate-500 mb-1">平台 *</label>
                  <select value={form.platform} onChange={e => setForm({ ...form, platform: e.target.value })} className={inputCls}>
                    <option>美团</option><option>点评</option><option>抖音</option>
                  </select>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <div><label className="block text-xs text-slate-500 mb-1">星级</label><input type="number" step="0.1" value={form.star_rating} onChange={e => setForm({ ...form, star_rating: +e.target.value })} className={inputCls} /></div>
                <div><label className="block text-xs text-slate-500 mb-1">榜单名称</label><input type="text" value={form.ranking_name} onChange={e => setForm({ ...form, ranking_name: e.target.value })} className={inputCls} /></div>
                <div><label className="block text-xs text-slate-500 mb-1">排名</label><input type="text" value={form.ranking_position} onChange={e => setForm({ ...form, ranking_position: e.target.value })} className={inputCls} /></div>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <div><label className="block text-xs text-slate-500 mb-1">曝光次数</label><input type="number" value={form.impressions} onChange={e => setForm({ ...form, impressions: +e.target.value })} className={inputCls} /></div>
                <div><label className="block text-xs text-slate-500 mb-1">访问次数</label><input type="number" value={form.visits} onChange={e => setForm({ ...form, visits: +e.target.value })} className={inputCls} /></div>
                <div><label className="block text-xs text-slate-500 mb-1">购买人数</label><input type="number" value={form.purchases} onChange={e => setForm({ ...form, purchases: +e.target.value })} className={inputCls} /></div>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <div><label className="block text-xs text-slate-500 mb-1">核销人数</label><input type="number" value={form.verifications} onChange={e => setForm({ ...form, verifications: +e.target.value })} className={inputCls} /></div>
                <div><label className="block text-xs text-slate-500 mb-1">新增收藏</label><input type="number" value={form.new_favorites} onChange={e => setForm({ ...form, new_favorites: +e.target.value })} className={inputCls} /></div>
                <div><label className="block text-xs text-slate-500 mb-1">打卡人数</label><input type="number" value={form.checkins} onChange={e => setForm({ ...form, checkins: +e.target.value })} className={inputCls} /></div>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <div><label className="block text-xs text-slate-500 mb-1">扫码人数</label><input type="number" value={form.scan_count} onChange={e => setForm({ ...form, scan_count: +e.target.value })} className={inputCls} /></div>
                <div><label className="block text-xs text-slate-500 mb-1">新增评价</label><input type="number" value={form.new_reviews} onChange={e => setForm({ ...form, new_reviews: +e.target.value })} className={inputCls} /></div>
                <div><label className="block text-xs text-slate-500 mb-1">新增差评</label><input type="number" value={form.new_bad_reviews} onChange={e => setForm({ ...form, new_bad_reviews: +e.target.value })} className={inputCls} /></div>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <div><label className="block text-xs text-slate-500 mb-1">商品曝光</label><input type="number" value={form.product_impressions} onChange={e => setForm({ ...form, product_impressions: +e.target.value })} className={inputCls} /></div>
                <div><label className="block text-xs text-slate-500 mb-1">商品访问</label><input type="number" value={form.product_visits} onChange={e => setForm({ ...form, product_visits: +e.target.value })} className={inputCls} /></div>
                <div><label className="block text-xs text-slate-500 mb-1">商品购买</label><input type="number" value={form.product_purchases} onChange={e => setForm({ ...form, product_purchases: +e.target.value })} className={inputCls} /></div>
              </div>
              <div><label className="block text-xs text-slate-500 mb-1">差评关键词（用中文逗号分隔）</label><input type="text" value={form.bad_keywords} onChange={e => setForm({ ...form, bad_keywords: e.target.value })} className={inputCls} placeholder="室内抽烟，服务差，等位久" /></div>
              <div><label className="block text-xs text-slate-500 mb-1">备注</label><textarea value={form.notes} onChange={e => setForm({ ...form, notes: e.target.value })} className={inputCls} rows={2} /></div>
            </div>
            <div className="flex items-center justify-end gap-2 p-4 border-t border-slate-100">
              <Button variant="outline" onClick={() => setShowModal(false)}>取消</Button>
              <Button onClick={handleSave} disabled={actionLoading}>{actionLoading && <Loader2 className="w-4 h-4 animate-spin mr-1" />}{editing ? '保存' : '创建'}</Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ==================== 分析意见 Tab ====================

function AnalysisTab({ stores, storeMap, toastSuccess, toastError }: {
  stores: StoreOption[]; storeMap: Record<string, string>;
  toastSuccess: (title: string, msg?: string) => void; toastError: (title: string, msg?: string) => void;
}) {
  const [data, setData] = useState<OperationAnalysisRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState<OperationAnalysisRecord | null>(null);
  const [storeId, setStoreId] = useState('');
  const [form, setForm] = useState({
    store_id: '', period_start: '', period_end: '', analysis_opinion: '', goals_text: '',
  });

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const res = await fetchAnalysisList({ store_id: storeId || undefined, page, page_size: 20 });
      setData(res.items); setTotal(res.total);
    } catch { toastError('加载失败'); } finally { setLoading(false); }
  }, [storeId, page]);

  useEffect(() => { loadData(); }, [loadData]);

  const handleSave = async () => {
    if (!form.store_id || !form.period_start || !form.period_end) return toastError('保存失败', '请填写必填项');
    try {
      setActionLoading(true);
      const payload = { store_id: form.store_id, period_start: form.period_start, period_end: form.period_end, analysis_opinion: form.analysis_opinion, goals: form.goals_text.split('\n').map(s => s.trim()).filter(Boolean) };
      if (editing) { await updateAnalysis(editing.id, payload); } else { await createAnalysis(payload); }
      toastSuccess(editing ? '更新成功' : '创建成功'); setShowModal(false); loadData();
    } catch (e: any) { toastError('保存失败', e?.message); } finally { setActionLoading(false); }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('确定删除？')) return;
    try { await deleteAnalysis(id); toastSuccess('删除成功'); loadData(); } catch { toastError('删除失败'); }
  };

  const openCreate = () => {
    setEditing(null);
    const today = new Date().toISOString().slice(0, 10);
    setForm({ store_id: stores[0]?.id || '', period_start: today, period_end: today, analysis_opinion: '', goals_text: '' });
    setShowModal(true);
  };

  const openEdit = (r: OperationAnalysisRecord) => {
    setEditing(r);
    setForm({ store_id: r.store_id, period_start: r.period_start, period_end: r.period_end, analysis_opinion: r.analysis_opinion, goals_text: r.goals.join('\n') });
    setShowModal(true);
  };

  const inputCls = "w-full px-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500";

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3 p-3 bg-slate-50 rounded-xl">
        <select value={storeId} onChange={e => { setStoreId(e.target.value); setPage(1); }}
          className="px-3 py-1.5 text-sm border border-slate-200 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500">
          <option value="">全部门店</option>
          {stores.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
        </select>
      </div>

      <div className="flex items-center justify-between">
        <span className="text-sm text-slate-500">{total} 条记录</span>
        <Button size="sm" onClick={openCreate}><Plus className="w-4 h-4 mr-1" />新建分析</Button>
      </div>

      {loading ? <div className="py-10 text-center text-slate-400"><Loader2 className="w-6 h-6 animate-spin mx-auto" /></div> : (
        <div className="space-y-3">
          {data.length === 0 ? (
            <Card className="p-10 text-center text-slate-400">暂无分析意见</Card>
          ) : data.map(r => (
            <Card key={r.id} className="p-4 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-2">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <Badge variant="secondary" className="bg-indigo-100 text-indigo-700">{r.store_name || storeMap[r.store_id] || '-'}</Badge>
                    <span className="text-xs text-slate-500">{r.period_start} ~ {r.period_end}</span>
                  </div>
                  <p className="text-sm text-slate-700 leading-relaxed">{r.analysis_opinion || '暂无分析意见'}</p>
                </div>
                <div className="flex items-center gap-1 flex-shrink-0 ml-3">
                  <button onClick={() => openEdit(r)} className="p-1.5 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"><Pencil className="w-4 h-4" /></button>
                  <button onClick={() => handleDelete(r.id)} className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"><Trash2 className="w-4 h-4" /></button>
                </div>
              </div>
              {r.goals.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {r.goals.map((g, i) => <Badge key={i} variant="outline" className="text-xs bg-emerald-50 text-emerald-700 border-emerald-200">🎯 {g}</Badge>)}
                </div>
              )}
            </Card>
          ))}
          <Pagination page={page} pageSize={20} total={total} onPageChange={setPage} />
        </div>
      )}

      {showModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" onClick={() => setShowModal(false)}>
          <div className="bg-white rounded-2xl shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
            <div className="flex items-center justify-between p-4 border-b border-slate-100">
              <h3 className="text-lg font-bold">{editing ? '编辑分析' : '新建分析意见'}</h3>
              <button onClick={() => setShowModal(false)} className="p-1 hover:bg-slate-100 rounded-lg"><X className="w-5 h-5" /></button>
            </div>
            <div className="p-4 space-y-3">
              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block text-xs text-slate-500 mb-1">门店 *</label>
                  <select value={form.store_id} onChange={e => setForm({ ...form, store_id: e.target.value })} className={inputCls}>
                    {stores.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-xs text-slate-500 mb-1">周期开始 *</label>
                  <input type="date" value={form.period_start} onChange={e => setForm({ ...form, period_start: e.target.value })} className={inputCls} />
                </div>
                <div>
                  <label className="block text-xs text-slate-500 mb-1">周期结束 *</label>
                  <input type="date" value={form.period_end} onChange={e => setForm({ ...form, period_end: e.target.value })} className={inputCls} />
                </div>
              </div>
              <div>
                <label className="block text-xs text-slate-500 mb-1">分析意见</label>
                <textarea value={form.analysis_opinion} onChange={e => setForm({ ...form, analysis_opinion: e.target.value })} className={inputCls} rows={4} placeholder="例：营业额上涨43.4%，抖音上涨47.87%，美团下滑54.5%" />
              </div>
              <div>
                <label className="block text-xs text-slate-500 mb-1">下周目标（每行一个）</label>
                <textarea value={form.goals_text} onChange={e => setForm({ ...form, goals_text: e.target.value })} className={inputCls} rows={4} placeholder={"每日评价：美团3条、点评1条、抖音1条\n差评率控制在3%\n每日扫码：1000元"} />
              </div>
            </div>
            <div className="flex items-center justify-end gap-2 p-4 border-t border-slate-100">
              <Button variant="outline" onClick={() => setShowModal(false)}>取消</Button>
              <Button onClick={handleSave} disabled={actionLoading}>{actionLoading && <Loader2 className="w-4 h-4 animate-spin mr-1" />}{editing ? '保存' : '创建'}</Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

import React, { useState, useEffect } from 'react';
import {
  BarChart3,
  TrendingUp,
  Utensils,
  Trash2,
  Award,
  ClipboardList,
  Lightbulb,
  ChevronLeft,
  ChevronRight,
  Download,
  RefreshCw,
  Search,
  Filter,
  Eye,
  CheckCircle2,
  XCircle
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { AdminLayout } from '../../components/AdminLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';
import { fetchTopDish, fetchThreeGoodThreeBad } from '../../api/insights';
import type { Dish } from '../../api/insights';

export const Insights: React.FC = () => {
  const [reportType, setReportType] = useState<'week' | 'month'>('week');
  const [topDish, setTopDish] = useState<Dish[]>([]);
  const [threeGoodThreeBad, setThreeGoodThreeBad] = useState<{goods: string[], bads: string[]}>({goods: [], bads: []});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [searchKeyword, setSearchKeyword] = useState('');
  const pageSize = 10;

  const { success, error: showError } = useToast();
  const fetchedRef = React.useRef(false);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [dishData, threeData] = await Promise.all([
        fetchTopDish(),
        fetchThreeGoodThreeBad(),
      ]);
      setTopDish(dishData);
      setThreeGoodThreeBad(threeData);
    } catch (err) {
      setError(err instanceof Error ? err.message : '获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (fetchedRef.current) return;
    fetchedRef.current = true;
    loadData();
  }, []);

  const handleExportReport = () => {
    success('导出报告', '正在导出经营洞察报告...');
  };

  const handleViewDish = (dishName: string) => {
    success('菜品详情', `正在查看"${dishName}"的详细口碑数据...`);
  };

  const handleElimination = () => {
    success('末位淘汰', '正在生成末位淘汰建议...');
  };

  const handleViewCase = (type: 'golden' | 'negative') => {
    success('查看案例', `正在加载${type === 'golden' ? '金牌服务' : '反面教材'}案例库...`);
  };

  // 筛选和搜索
  const filteredDishes = topDish.filter(dish => {
    if (searchKeyword) {
      return dish.name.includes(searchKeyword);
    }
    return true;
  });

  // 分页
  const totalPages = Math.ceil(filteredDishes.length / pageSize);
  const paginatedDishes = filteredDishes.slice(
    (currentPage - 1) * pageSize,
    currentPage * pageSize
  );

  if (loading) {
    return (
      <AdminLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="w-12 h-12 border-4 border-orange-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-sm text-slate-400">加载中...</p>
          </div>
        </div>
      </AdminLayout>
    );
  }

  if (error) {
    return (
      <AdminLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <p className="text-sm text-rose-500 mb-4">{error}</p>
            <Button onClick={loadData} className="bg-orange-500 hover:bg-orange-600 text-white">
              重试
            </Button>
          </div>
        </div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">经营洞察</h2>
            <p className="text-slate-500 mt-1">深度分析经营数据，发现改进机会</p>
          </div>
          <div className="flex gap-3">
            <Button variant="outline" className="gap-2" onClick={handleExportReport}>
              <Download className="w-4 h-4" />
              导出报告
            </Button>
            <Button className="bg-orange-500 hover:bg-orange-600 text-white gap-2" onClick={() => loadData()}>
              <RefreshCw className="w-4 h-4" />
              刷新数据
            </Button>
          </div>
        </div>

        {/* Three Good Three Bad Report */}
        <Card className="p-6 border-none shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h3 className="font-bold text-slate-800 text-lg">"三好三差"智能报告</h3>
            <div className="flex bg-slate-100 p-0.5 rounded-lg">
              <button
                onClick={() => setReportType('week')}
                className={cn(
                  "px-4 py-1.5 text-xs font-bold rounded-md transition-all",
                  reportType === 'week' ? "bg-white text-orange-600 shadow-sm" : "text-slate-400"
                )}
              >
                周报
              </button>
              <button
                onClick={() => setReportType('month')}
                className={cn(
                  "px-4 py-1.5 text-xs font-bold rounded-md transition-all",
                  reportType === 'month' ? "bg-white text-orange-600 shadow-sm" : "text-slate-400"
                )}
              >
                月报
              </button>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-3">
              <p className="text-xs font-bold text-emerald-600 flex items-center gap-1">
                <TrendingUp className="w-3 h-3" /> 表现优异 (三好)
              </p>
              <div className="flex flex-wrap gap-2">
                {threeGoodThreeBad.goods.map((item, i) => (
                  <Badge key={i} className="bg-emerald-50 text-emerald-600 border-none font-medium text-xs">
                    {item}
                  </Badge>
                ))}
              </div>
            </div>
            
            <div className="space-y-3">
              <p className="text-xs font-bold text-rose-500 flex items-center gap-1">
                <TrendingUp className="w-3 h-3 rotate-180" /> 急需改进 (三差)
              </p>
              <div className="flex flex-wrap gap-2">
                {threeGoodThreeBad.bads.map((item, i) => (
                  <Badge key={i} className="bg-rose-50 text-rose-600 border-none font-medium text-xs">
                    {item}
                  </Badge>
                ))}
              </div>
            </div>
          </div>
          
          <Button
            variant="ghost"
            className="w-full mt-6 h-8 text-orange-600 text-xs font-bold bg-orange-50/50 rounded-lg"
          >
            查看详细溯源报告
          </Button>
        </Card>

        {/* Dish Reputation Ranking */}
        <Card className="border-none shadow-sm overflow-hidden">
          <div className="p-4 border-b border-slate-100">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-slate-800 text-lg flex items-center gap-2">
                <Utensils className="w-5 h-5 text-orange-500" /> 菜品口碑排行榜
              </h3>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <Input
                  placeholder="搜索菜品..."
                  className="pl-9 w-64"
                  value={searchKeyword}
                  onChange={(e) => setSearchKeyword(e.target.value)}
                />
              </div>
            </div>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50 border-b border-slate-100">
                <tr>
                  <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">排名</th>
                  <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">菜品名称</th>
                  <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">类型</th>
                  <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">好评数</th>
                  <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">差评数</th>
                  <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">评分</th>
                  <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">操作</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50">
                {paginatedDishes.map((dish, i) => (
                  <tr key={i} className="hover:bg-slate-50 transition-colors">
                    <td className="p-4">
                      <span className={cn(
                        "w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold",
                        i === 0 ? "bg-amber-100 text-amber-600" :
                        i === 1 ? "bg-slate-100 text-slate-600" :
                        i === 2 ? "bg-orange-100 text-orange-600" : "bg-slate-100 text-slate-500"
                      )}>
                        {i + 1}
                      </span>
                    </td>
                    <td className="p-4">
                      <span className="text-sm font-medium text-slate-900">{dish.name}</span>
                    </td>
                    <td className="p-4">
                      <Badge className={cn(
                        "text-[10px] border-none",
                        dish.type === 'recommended' ? "bg-emerald-100 text-emerald-700" :
                        dish.type === 'potential' ? "bg-orange-100 text-orange-700" :
                        "bg-rose-100 text-rose-700"
                      )}>
                        {dish.type === 'recommended' ? '推荐' : dish.type === 'potential' ? '潜力' : '疑问'}
                      </Badge>
                    </td>
                    <td className="p-4">
                      <span className="text-sm text-emerald-600 font-medium">{dish.positive}</span>
                    </td>
                    <td className="p-4">
                      <span className="text-sm text-rose-600 font-medium">{dish.negative}</span>
                    </td>
                    <td className="p-4">
                      <span className="text-sm font-bold text-slate-900">{dish.score}</span>
                    </td>
                    <td className="p-4">
                      <Button
                        size="sm"
                        variant="ghost"
                        className="h-8 w-8 p-0"
                        onClick={() => handleViewDish(dish.name)}
                        title="查看详情"
                      >
                        <Eye className="w-4 h-4" />
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          {/* Pagination */}
          <div className="flex items-center justify-between p-4 border-t border-slate-100">
            <p className="text-sm text-slate-500">
              显示 {((currentPage - 1) * pageSize) + 1}-{Math.min(currentPage * pageSize, filteredDishes.length)} 条，共 {filteredDishes.length} 条
            </p>
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                disabled={currentPage === 1}
              >
                <ChevronLeft className="w-4 h-4" />
              </Button>
              <span className="text-sm font-medium text-slate-700">
                {currentPage} / {totalPages}
              </span>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                disabled={currentPage === totalPages}
              >
                <ChevronRight className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </Card>

        {/* Elimination Advice & Service Standards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Elimination Advice */}
          <Card className="p-6 border-none shadow-sm bg-slate-900 text-white">
            <div className="flex items-center gap-2 mb-4">
              <Trash2 className="w-5 h-5 text-amber-400" />
              <h4 className="text-sm font-bold">"末位淘汰"建议</h4>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed mb-4">
              基于近 30 天评价，菜品 <span className="text-amber-400 font-bold underline">"麻辣烫"</span> 差评率持续高于 20%，且近期销量表现一般。
            </p>
            <div className="bg-white/5 p-4 rounded-xl border border-white/10 space-y-2">
              <p className="text-xs text-slate-400">主要问题：口感过咸、食材种类单一</p>
              <Button
                className="w-full bg-amber-500 hover:bg-amber-600 text-white h-8 text-xs font-bold border-none"
                onClick={handleElimination}
              >
                查看详细改进方案
              </Button>
            </div>
          </Card>

          {/* Service Standards */}
          <div className="space-y-4">
            <h3 className="font-bold text-slate-800 text-lg">服务标准数字化沉淀</h3>
            <Card className="p-4 border-none shadow-sm flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-emerald-50 rounded-xl flex items-center justify-center text-emerald-600">
                  <Award className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-xs font-bold text-slate-800">金牌服务案例库</h4>
                  <p className="text-[9px] text-slate-400 mt-1">已沉淀 42 条优秀案例</p>
                </div>
              </div>
              <Button
                variant="outline"
                size="sm"
                className="h-8 text-xs"
                onClick={() => handleViewCase('golden')}
              >
                查看
              </Button>
            </Card>
            
            <Card className="p-4 border-none shadow-sm flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-rose-50 rounded-xl flex items-center justify-center text-rose-500">
                  <ClipboardList className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-xs font-bold text-slate-800">反面教材修正工单</h4>
                  <p className="text-[9px] text-slate-400 mt-1">3 条工单正在整改中</p>
                </div>
              </div>
              <Button
                variant="outline"
                size="sm"
                className="h-8 text-xs"
                onClick={() => handleViewCase('negative')}
              >
                去处理
              </Button>
            </Card>
          </div>
        </div>

        {/* Competitor Opportunity */}
        <Card className="p-6 border-none shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <Lightbulb className="w-5 h-5 text-orange-500" />
            <h4 className="text-sm font-bold text-slate-700">同行机会洞察</h4>
          </div>
          <p className="text-xs text-slate-500 leading-relaxed mb-4">
            您的竞品 A 近期"上菜慢"的差评增多，建议您本店主推"30分钟未上齐免单"服务。
          </p>
          <div className="pt-2">
            <div className="flex justify-between text-xs mb-1">
              <span className="text-slate-400">本店好评率</span>
              <span className="font-bold text-orange-600">94.2%</span>
            </div>
            <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
              <div className="bg-orange-500 h-full w-[94%]"></div>
            </div>
          </div>
        </Card>
      </div>
    </AdminLayout>
  );
};

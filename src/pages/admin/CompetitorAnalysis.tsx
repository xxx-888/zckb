import React, { useState } from 'react';
import { 
  Target, 
  TrendingUp, 
  BarChart3, 
  PieChart, 
  MessageCircle, 
  AlertTriangle, 
  ArrowUpRight,
  ArrowDownRight,
  ChevronRight,
  Lightbulb,
  FileText,
  Share2,
  Plus,
  RefreshCw,
  Download,
  Eye,
  Star,
  Trash2
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { AdminLayout } from '../../components/AdminLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';

interface Competitor {
  id: number;
  name: string;
  rating: number;
  positiveRate: string;
  trends: number[];
  badTags: string[];
  isOurs?: boolean;
}

export const CompetitorAnalysis: React.FC = () => {
  const [competitors, setCompetitors] = useState<Competitor[]>([
    { id: 0, name: '本店 (王府井总店)', rating: 4.7, positiveRate: '94.2%', trends: [60, 65, 75, 80, 85, 90, 88], badTags: ['排队久'], isOurs: true },
    { id: 1, name: '竞品 A (商圈第一)', rating: 4.9, positiveRate: '96.2%', trends: [80, 85, 90, 88, 92, 95, 94], badTags: ['上菜慢', '价格高', '排队久'] },
    { id: 2, name: '竞品 B (老字号)', rating: 4.5, positiveRate: '88.5%', trends: [70, 72, 68, 75, 78, 80, 77], badTags: ['环境旧', '服务一般', '卫生差'] },
  ]);

  const [selectedCompetitor, setSelectedCompetitor] = useState<number | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isSharing, setIsSharing] = useState(false);
  const { success, error } = useToast();

  const handleGenerateReport = () => {
    setIsGenerating(true);
    success('生成周报', '正在生成竞品分析周报...');
    setTimeout(() => {
      setIsGenerating(false);
      success('生成完成', '竞品分析周报已生成，可下载或分享');
    }, 2000);
  };

  const handleShare = () => {
    setIsSharing(true);
    success('分享简报', '正在生成分享链接...');
    setTimeout(() => {
      setIsSharing(false);
      success('分享成功', '分享链接已复制到剪贴板');
      navigator.clipboard.writeText('https://zhice.com/share/competitor-analysis/2026-05-12');
    }, 1500);
  };

  const handleViewDetail = (id: number) => {
    setSelectedCompetitor(selectedCompetitor === id ? null : id);
    const comp = competitors.find(c => c.id === id);
    success('查看详情', `正在加载 "${comp?.name}" 的详细数据...`);
  };

  const handleAddCompetitor = () => {
    const name = prompt('请输入竞品名称：');
    if (!name) return;
    
    const newCompetitor: Competitor = {
      id: competitors.length,
      name: name,
      rating: 4.0 + Math.random(),
      positiveRate: `${(80 + Math.random() * 15).toFixed(1)}%`,
      trends: [65, 70, 75, 72, 78, 80, 76],
      badTags: ['待分析']
    };
    setCompetitors([...competitors, newCompetitor]);
    success('添加成功', `竞品 "${name}" 已添加到对比列表`);
  };

  const handleDeleteCompetitor = (id: number) => {
    const comp = competitors.find(c => c.id === id);
    if (comp?.isOurs) {
      error('操作失败', '不能删除本店数据');
      return;
    }
    setCompetitors(competitors.filter(c => c.id !== id));
    success('删除成功', `竞品 "${comp?.name}" 已从对比列表移除`);
  };

  const handleExportData = () => {
    success('导出数据', '正在导出竞品对比数据...');
    setTimeout(() => {
      success('导出完成', '竞品对比数据已下载（Excel 格式）');
    }, 1500);
  };

  return (
    <AdminLayout>
      <div className="space-y-8">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">竞品评价对标</h2>
            <p className="text-slate-500 mt-1">对比商圈竞品口碑表现，捕捉经营机会点</p>
          </div>
          <div className="flex gap-3">
             <Button 
                variant="outline" 
                className="gap-2"
                onClick={handleGenerateReport}
                disabled={isGenerating}
              >
                {isGenerating ? <RefreshCw className="w-4 h-4 animate-spin" /> : <FileText className="w-4 h-4" />}
                {isGenerating ? '生成中...' : '生成周报'}
             </Button>
             <Button 
                className="bg-orange-500 hover:bg-orange-600 text-white gap-2"
                onClick={handleShare}
                disabled={isSharing}
              >
                {isSharing ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Share2 className="w-4 h-4" />}
                {isSharing ? '分享中...' : '分享简报'}
             </Button>
          </div>
        </div>

        {/* Comparison Dashboard */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <Card className="lg:col-span-2 p-6 border-none shadow-sm bg-white">
            <h3 className="font-bold text-slate-800 mb-6 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-orange-500" /> 星级趋势对比 (最近7天)
            </h3>
            <div className="h-64 flex items-end justify-between gap-4 px-2 relative">
               {/* Y-axis labels */}
               <div className="absolute inset-0 flex flex-col justify-between py-6 px-4">
                  {[1, 2, 3, 4, 5].reverse().map(i => (
                    <div key={i} className="border-t border-slate-50 w-full flex items-center text-[10px] text-slate-300">
                      <span className="bg-white pr-2">{i}.0</span>
                    </div>
                  ))}
               </div>
               {/* Chart bars */}
               <div className="w-full h-full flex items-end justify-between px-6 z-10">
                  {competitors[0].trends.map((h, i) => (
                    <div key={i} className="flex flex-col items-center gap-2 flex-1 group">
                       <div className="w-full flex justify-center items-end gap-1">
                          <div 
                            className="w-3 bg-orange-500 rounded-t-sm transition-all duration-700" 
                            style={{ height: `${h}%` }}
                          ></div>
                          {competitors.length > 1 && (
                            <div 
                              className="w-3 bg-slate-300 rounded-t-sm transition-all duration-700" 
                              style={{ height: `${competitors[1].trends[i]}%` }}
                            ></div>
                          )}
                          {competitors.length > 2 && (
                            <div 
                              className="w-3 bg-blue-300 rounded-t-sm transition-all duration-700" 
                              style={{ height: `${competitors[2].trends[i]}%` }}
                            ></div>
                          )}
                       </div>
                       <span className="text-[10px] text-slate-400">05-{i+2}</span>
                    </div>
                  ))}
               </div>
            </div>
            <div className="flex justify-center gap-6 mt-8">
               <div className="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase">
                  <div className="w-3 h-3 bg-orange-500 rounded-sm"></div> 本店
               </div>
               {competitors.length > 1 && (
                 <div className="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase">
                    <div className="w-3 h-3 bg-slate-300 rounded-sm"></div> {competitors[1].name}
                 </div>
               )}
               {competitors.length > 2 && (
                 <div className="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase">
                    <div className="w-3 h-3 bg-blue-300 rounded-sm"></div> {competitors[2].name}
                 </div>
               )}
            </div>
          </Card>

          <Card className="p-6 border-none shadow-sm bg-slate-900 text-white flex flex-col">
             <h3 className="font-bold mb-6 flex items-center gap-2">
               <Lightbulb className="w-5 h-5 text-amber-400" /> 竞品机会洞察 AI 简报
             </h3>
             <div className="flex-1 space-y-6">
                <div className="p-4 bg-white/5 rounded-xl border border-white/10 space-y-2">
                   <p className="text-xs font-bold text-amber-400"># 突破点建议</p>
                   <p className="text-[11px] text-slate-300 leading-relaxed">
                     竞品 A 近期 <span className="text-white font-bold underline">"上菜慢"</span> 差评激增 25%。建议本店在黄金时段强化 "30分钟未上齐免单" 的服务承诺，并在团购详情页突出"极速出餐"。
                   </p>
                </div>
                <div className="p-4 bg-white/5 rounded-xl border border-white/10 space-y-2">
                   <p className="text-xs font-bold text-emerald-400"># 优势巩固</p>
                   <p className="text-[11px] text-slate-300 leading-relaxed">
                     本店在 "服务细节" 维度的正向评价密度远高于竞品 B。建议将 "金牌服务案例" 转化为抖音视频素材，进一步拉开差距。
                   </p>
                </div>
             </div>
             <Button 
                className="w-full mt-6 bg-white/10 hover:bg-white/20 border-none text-[11px] font-bold"
                onClick={() => success('查看详情', '正在打开完整分析报告...')}
              >
                查看完整分析报告
              </Button>
          </Card>
        </div>

        {/* Competitor List */}
        <Card className="border-none shadow-sm overflow-hidden bg-white">
           <div className="p-4 border-b border-slate-50 flex justify-between items-center">
             <h3 className="font-bold text-slate-800 text-sm">竞品列表管理</h3>
             <Button 
                size="sm" 
                className="gap-2 bg-orange-500 hover:bg-orange-600 text-white"
                onClick={handleAddCompetitor}
              >
                <Plus className="w-3.5 h-3.5" /> 添加竞品
              </Button>
           </div>
           <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                 <thead>
                    <tr className="bg-slate-50/50">
                       <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase">竞品名称</th>
                       <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase">综合评分</th>
                       <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase">好评率</th>
                       <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase">高频差评标签</th>
                       <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase text-right">操作</th>
                    </tr>
                 </thead>
                 <tbody className="divide-y divide-slate-100">
                    {competitors.map((comp) => (
                      <tr key={comp.id} className="hover:bg-slate-50/50 transition-colors">
                         <td className="px-6 py-4">
                            <div className="flex items-center gap-3">
                               <div className={cn(
                                 "w-10 h-10 rounded-xl flex items-center justify-center text-xs font-bold",
                                 comp.isOurs ? "bg-orange-500 text-white" : "bg-slate-100 text-slate-600"
                               )}>
                                 {comp.name[0]}
                               </div>
                               <div>
                                 <p className="text-sm font-bold text-slate-900">{comp.name}</p>
                                 {comp.isOurs && (
                                   <Badge className="bg-orange-50 text-orange-600 border-orange-200 text-[9px] py-0 h-4">本店</Badge>
                                 )}
                               </div>
                            </div>
                         </td>
                         <td className="px-6 py-4">
                            <div className="flex items-center gap-2">
                               <span className="text-sm font-bold text-slate-900">{comp.rating}</span>
                               <div className="flex text-amber-400">
                                 {[1, 2, 3, 4, 5].map(i => (
                                   <Star key={i} className={cn("w-3 h-3", i <= Math.floor(comp.rating) ? "fill-current" : "text-slate-200 fill-none")} />
                                 ))}
                               </div>
                            </div>
                         </td>
                         <td className="px-6 py-4 text-sm text-emerald-600 font-bold">{comp.positiveRate}</td>
                         <td className="px-6 py-4">
                            <div className="flex flex-wrap gap-1">
                               {comp.badTags.map((tag, i) => (
                                 <Badge key={i} variant="outline" className="text-[8px]">{tag}</Badge>
                               ))}
                            </div>
                         </td>
                         <td className="px-6 py-4 text-right">
                            <div className="flex justify-end gap-1">
                              <Button 
                                variant="ghost" 
                                size="icon" 
                                className="h-8 w-8 text-slate-400 hover:text-orange-600"
                                onClick={() => handleViewDetail(comp.id)}
                              >
                                <Eye className="w-4 h-4" />
                              </Button>
                              {!comp.isOurs && (
                                <Button 
                                  variant="ghost" 
                                  size="icon" 
                                  className="h-8 w-8 text-slate-400 hover:text-rose-600"
                                  onClick={() => handleDeleteCompetitor(comp.id)}
                                >
                                  <Trash2 className="w-4 h-4" />
                                </Button>
                              )}
                            </div>
                         </td>
                      </tr>
                    ))}
                 </tbody>
              </table>
           </div>
        </Card>

        {/* Detailed Metrics Table */}
        <Card className="border-none shadow-sm overflow-hidden bg-white">
           <div className="p-4 border-b border-slate-50">
             <h3 className="font-bold text-slate-800 text-sm">核心指标对标</h3>
           </div>
           <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                 <thead>
                    <tr className="bg-slate-50/50">
                       <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase">对比项</th>
                       <th className="px-6 py-4 text-[10px] font-bold text-orange-600 uppercase">本店</th>
                       {competitors.filter(c => !c.isOurs).map(c => (
                         <th key={c.id} className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase">{c.name}</th>
                       ))}
                       <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase text-right">商圈均值</th>
                    </tr>
                 </thead>
                 <tbody className="divide-y divide-slate-100">
                    {[
                      { label: '综合评分', our: '4.7', others: competitors.filter(c => !c.isOurs).map(c => c.rating.toString()), avg: '4.2' },
                      { label: '好评率', our: '94.2%', others: competitors.filter(c => !c.isOurs).map(c => c.positiveRate), avg: '86.4%' },
                      { label: '回复率', our: '99.5%', others: ['82.0%', '45.0%'], avg: '68.2%' },
                      { label: '平均回复时长', our: '2.5m', others: ['45m', '12h+'], avg: '5.2h' },
                    ].map((row, i) => (
                      <tr key={i} className="hover:bg-slate-50/50 transition-colors">
                         <td className="px-6 py-4 text-xs font-bold text-slate-700">{row.label}</td>
                         <td className="px-6 py-4 text-xs font-black text-orange-600">{row.our}</td>
                         {row.others.map((val, j) => (
                           <td key={j} className="px-6 py-4 text-xs text-slate-600">{val}</td>
                         ))}
                         <td className="px-6 py-4 text-xs text-slate-400 text-right">{row.avg}</td>
                      </tr>
                    ))}
                 </tbody>
              </table>
           </div>
        </Card>
      </div>
    </AdminLayout>
  );
};

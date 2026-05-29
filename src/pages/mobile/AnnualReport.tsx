import React, { useState, useEffect } from 'react';
import {
  ArrowLeft,
  MessageSquare,
  Star,
  ThumbsUp,
  ThumbsDown,
  Sparkles,
  Trophy,
  Heart,
  Flame,
  PartyPopper,
  TrendingUp,
  TrendingDown,
  Minus,
  ChevronRight,
  Download,
  RefreshCw,
  Brain,
  Target,
  BarChart3,
  PieChart,
  Calendar,
  Store,
  CheckCircle,
  XCircle,
  Clock,
  Zap,
  Award,
  BookOpen,
  LineChart,
  Activity
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { Button } from '../../components/ui/button';
import { MobileLayout } from '../../components/MobileLayout';
import { Skeleton } from '../../components/ui/skeleton';
import { useToast } from '../../hooks/use-toast';
import { useNavigate } from 'react-router-dom';
import { fetchAnnualReport, fetchAllYearlyData, generateAnnualReport } from '../../api/annual-report';
import type { YearlyData, ReportInsights, HistoricalTrends } from '../../api/annual-report';
import { useStore } from '../../context/StoreContext';

// 辅助：安全取数
const num = (v: any): number => (typeof v === 'number' && !isNaN(v)) ? v : 0;

export const MobileAnnualReport: React.FC = () => {
  const [selectedYear, setSelectedYear] = useState(2025);
  const [yearlyData, setYearlyData] = useState<Record<number, YearlyData>>({});
  const [insights, setInsights] = useState<ReportInsights | null>(null);
  const [historical, setHistorical] = useState<HistoricalTrends | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'reply' | 'trends' | 'comparison'>('overview');
  const lastYearRef = React.useRef<number | null>(null);

  const { success } = useToast();
  const navigate = useNavigate();
  const { selectedStoreId } = useStore();

  const [generating, setGenerating] = useState(false);

  const loadData = async (year: number) => {
    try {
      setLoading(true);
      const data = await fetchAnnualReport(selectedStoreId || '', year);
      if (data.yearlyData) {
        setYearlyData(prev => ({ ...prev, [year]: data.yearlyData! }));
      }
      if (data.insights) setInsights(data.insights);
      if (data.historicalTrends) setHistorical(data.historicalTrends);
    } catch (err) {
      console.error('加载年度报告失败', err);
    } finally {
      setLoading(false);
    }
  };

  // 初始化时预加载所有年份数据（用于年度对比 tab）
  useEffect(() => {
    if (!selectedStoreId) return;
    setLoading(true);
    const allYears = [2023, 2024, 2025];
    let loaded = 0;
    allYears.forEach(y => {
      fetchAnnualReport(selectedStoreId, y).then(data => {
        if (data.yearlyData) {
          setYearlyData(prev => ({ ...prev, [y]: data.yearlyData! }));
        }
        loaded++;
        if (loaded === allYears.length) setLoading(false);
      }).catch(() => {
        loaded++;
        if (loaded === allYears.length) setLoading(false);
      });
    });
  }, [selectedStoreId]);

  // 切换年份时更新 insights 和 historical
  useEffect(() => {
    if (!selectedStoreId || !selectedYear) return;
    fetchAnnualReport(selectedStoreId, selectedYear).then(data => {
      if (data.insights) setInsights(data.insights);
      if (data.historicalTrends) setHistorical(data.historicalTrends);
    }).catch(console.error);
  }, [selectedYear, selectedStoreId]);

  const handleGenerate = async () => {
    if (!selectedStoreId) return;
    setGenerating(true);
    try {
      const result = await generateAnnualReport(selectedYear, selectedStoreId);
      if (result.success) {
        success('生成成功', result.message || `${selectedYear}年度报告已生成`);
        await loadData(selectedYear);
      } else {
        console.error('生成报告失败', result.message);
      }
    } catch (err: any) {
      console.error('生成报告异常', err);
    } finally {
      setGenerating(false);
    }
  };

  const handleExport = () => {
    success('导出报告', '正在生成精美 PDF 报告...');
  };

  const handleBack = () => {
    navigate('/mobile/insights');
  };

  const currentData = yearlyData[selectedYear];

  // ===== 渲染辅助 =====
  const renderStars = (rating: number) => {
    const stars: JSX.Element[] = [];
    for (let i = 1; i <= 5; i++) {
      if (i <= Math.floor(rating)) {
        stars.push(<Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />);
      } else if (i - 0.5 <= rating) {
        stars.push(<Star key={i} className="w-4 h-4 fill-yellow-400/50 text-yellow-400" />);
      } else {
        stars.push(<Star key={i} className="w-4 h-4 text-gray-300" />);
      }
    }
    return <div className="flex">{stars}</div>;
  };

  const getTrendIcon = (value: number) => {
    if (value > 0) return <TrendingUp className="w-4 h-4 text-green-500" />;
    if (value < 0) return <TrendingDown className="w-4 h-4 text-red-500" />;
    return <Minus className="w-4 h-4 text-gray-400" />;
  };

  // ===== 新数据项辅助 =====
  /** 评分分布柱状图 */
  const renderRatingDist = () => {
    const dist = currentData?.ratingDistribution;
    if (!dist || !dist.total) return null;
    const labels = ['1星', '2星', '3星', '4星', '5星'];
    const colors = ['bg-rose-400', 'bg-orange-400', 'bg-amber-400', 'bg-emerald-400', 'bg-emerald-600'];
    return (
      <Card className="p-6" key="rating-dist">
        <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
          <Star className="w-5 h-5 text-amber-500" />
          评分分布
        </h3>
        <div className="space-y-2">
          {[5, 4, 3, 2, 1].map((star, i) => {
            const count = dist[star as keyof typeof dist] || 0;
            const pct = dist.total > 0 ? Math.round((count / dist.total) * 100) : 0;
            return (
              <div key={star} className="flex items-center gap-2">
                <span className="text-xs text-slate-500 w-6 text-right">{star}星</span>
                <div className="flex-1 bg-slate-100 rounded-full h-3">
                  <div
                    className={`${colors[4 - i]} h-full rounded-full transition-all duration-700`}
                    style={{ width: `${pct}%` }}
                  ></div>
                </div>
                <span className="text-xs text-slate-600 w-12 text-right">{count}条</span>
              </div>
            );
          })}
          <div className="text-xs text-slate-400 text-center pt-1">
            均分 {dist.avg || 0} · 共 {dist.total} 条
          </div>
        </div>
      </Card>
    );
  };

  /** 平台来源分布 */
  const renderPlatformDist = () => {
    const pd = currentData?.platformDistribution;
    if (!pd || !Object.keys(pd).length) return null;
    const entries = Object.entries(pd).sort((a: any, b: any) => b[1] - a[1]);
    const total = entries.reduce((s: number, e: any) => s + e[1], 0);
    const colors = ['bg-blue-500', 'bg-emerald-500', 'bg-purple-500', 'bg-orange-500', 'bg-pink-500'];
    return (
      <Card className="p-6" key="platform-dist">
        <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
          <Store className="w-5 h-5 text-blue-500" />
          平台来源分布
        </h3>
        <div className="space-y-3">
          {entries.map(([platform, count]: any, i: number) => {
            const pct = total > 0 ? Math.round((count / total) * 100) : 0;
            return (
              <div key={platform}>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm text-slate-600">{platform}</span>
                  <span className="text-sm font-bold text-slate-700">{count}条 ({pct}%)</span>
                </div>
                <div className="bg-slate-100 rounded-full h-2.5">
                  <div
                    className={`${colors[i % colors.length]} h-full rounded-full transition-all duration-700`}
                    style={{ width: `${pct}%` }}
                  ></div>
                </div>
              </div>
            );
          })}
        </div>
      </Card>
    );
  };

  /** 回复情感分布 */
  const renderReplySentiment = () => {
    const rs = currentData?.replySentiment;
    if (!rs || !rs.total) return null;
    const items = [
      { label: '正面回复', value: rs.positive || 0, color: 'bg-emerald-400' },
      { label: '中性回复', value: rs.neutral || 0, color: 'bg-slate-400' },
      { label: '负面回复', value: rs.negative || 0, color: 'bg-rose-400' },
    ];
    return (
      <Card className="p-6" key="reply-sentiment">
        <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
          <MessageSquare className="w-5 h-5 text-blue-500" />
          回复情感分布
        </h3>
        <div className="flex gap-1 mb-3 h-4 rounded-full overflow-hidden">
          {items.map(item => {
            const pct = rs.total > 0 ? Math.round((item.value / rs.total) * 100) : 0;
            return pct > 0 ? (
              <div
                key={item.label}
                className={item.color}
                style={{ width: `${pct}%` }}
                title={`${item.label}: ${item.value}条`}
              ></div>
            ) : null;
          })}
        </div>
        <div className="flex justify-between text-xs text-slate-500">
          {items.map(item => (
            <span key={item.label}>{item.label}: {item.value}条</span>
          ))}
        </div>
      </Card>
    );
  };

  /** 月度情感趋势 */
  const renderMonthlySentiment = () => {
    const ms = currentData?.monthlySentiment;
    if (!ms || !ms.length) return null;
    const maxCount = Math.max(...ms.map((m: any) => m.total || 0), 1);
    return (
      <Card className="p-6" key="monthly-sentiment">
        <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
          <Activity className="w-5 h-5 text-indigo-600" />
          月度情感 & 回复率趋势
        </h3>
        <div className="space-y-2">
          {ms.map((m: any, i: number) => {
            const posPct = m.total > 0 ? Math.round((m.positive / m.total) * 100) : 0;
            const negPct = m.total > 0 ? Math.round((m.negative / m.total) * 100) : 0;
            const neuPct = 100 - posPct - negPct;
            return (
              <div key={i}>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs text-slate-500 w-8">{m.month}月</span>
                  <span className="text-xs text-slate-400">
                    回复率 {m.replyRate || 0}%
                  </span>
                </div>
                <div className="flex h-3 rounded-full overflow-hidden bg-slate-100">
                  <div className="bg-emerald-400 transition-all duration-700" style={{ width: `${posPct}%` }}></div>
                  <div className="bg-slate-300 transition-all duration-700" style={{ width: `${neuPct}%` }}></div>
                  <div className="bg-rose-400 transition-all duration-700" style={{ width: `${negPct}%` }}></div>
                </div>
              </div>
            );
          })}
          <div className="flex justify-center gap-3 text-xs text-slate-400 pt-1">
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-emerald-400 inline-block"></span>正面</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-slate-300 inline-block"></span>中性</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-rose-400 inline-block"></span>负面</span>
          </div>
        </div>
      </Card>
    );
  };

  // ===== 骨架屏 =====
  if (loading && !currentData) {
    return (
      <MobileLayout title={`${selectedYear} 年度报告`}>
        <div className="space-y-6 p-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <Skeleton lines={2} className="p-6" />
          <div className="flex gap-3">
            <Skeleton lines={3} card={true} className="flex-1 p-4" />
            <Skeleton lines={3} card={true} className="flex-1 p-4" />
          </div>
          <Skeleton lines={4} card={true} className="p-6" />
          <Skeleton lines={4} card={true} className="p-6" />
          <Skeleton lines={3} card={true} className="p-6" />
        </div>
      </MobileLayout>
    );
  }

  // ===== 主渲染 =====
  return (
    <MobileLayout title={`${selectedYear} 年度报告`}>
      <div className="space-y-6 pb-24 animate-in fade-in slide-in-from-bottom-4 duration-500">

        {/* Header with Year Selector */}
        <div className="flex items-center justify-between">
          <Button variant="ghost" size="icon" onClick={handleBack}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <select
            value={selectedYear}
            onChange={(e) => setSelectedYear(parseInt(e.target.value))}
            className="bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-sm outline-none"
          >
            {[2025, 2024, 2023].map(year => (
              <option key={year} value={year}>{year} 年</option>
            ))}
          </select>
          {currentData && (
            <Button variant="outline" size="sm" onClick={handleExport} className="gap-1">
              <Download className="w-4 h-4" /> 导出
            </Button>
          )}
          {!currentData && (
            <Button
              variant="outline"
              size="sm"
              onClick={handleGenerate}
              disabled={generating}
              className="gap-1 text-indigo-600 border-indigo-200"
            >
              <RefreshCw className={`w-4 h-4 ${generating ? 'animate-spin' : ''}`} />
              {generating ? '生成中...' : '生成报告'}
            </Button>
          )}
        </div>

        {/* 报告不存在时显示空状态 */}
        {!currentData && !loading && (
          <Card className="p-8 bg-white border-slate-100 shadow-sm text-center">
            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-slate-100 flex items-center justify-center">
              <BarChart3 className="w-8 h-8 text-slate-400" />
            </div>
            <h3 className="text-lg font-bold text-slate-700 mb-2">{selectedYear} 年度报告暂无数据</h3>
            <p className="text-sm text-slate-400 mb-4">点击下方按钮，系统将基于该年份的评论数据自动生成年度报告</p>
            <Button
              onClick={handleGenerate}
              disabled={generating}
              className="bg-indigo-600 hover:bg-indigo-700 text-white gap-2"
            >
              <Sparkles className={`w-4 h-4 ${generating ? 'animate-pulse' : ''}`} />
              {generating ? '正在生成报告...' : `生成 ${selectedYear} 年度报告`}
            </Button>
          </Card>
        )}

        {currentData && insights && (
          <>
            {/* Personality Type Card */}
            <Card className="p-6 bg-white border-slate-100 shadow-sm">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-12 h-12 rounded-xl bg-orange-50 flex items-center justify-center">
                  <PartyPopper className="w-6 h-6 text-orange-500" />
                </div>
                <Badge className="bg-orange-100 text-orange-600 border-orange-200">
                  {insights.personalityType}
                </Badge>
              </div>
              <h3 className="text-2xl font-black text-slate-900 mb-2">{selectedYear} 年口碑数字资产</h3>
              <p className="text-slate-400">{currentData.totalReviews} 条评价的记忆</p>
              <div className="flex items-center gap-4 mt-4 text-sm text-slate-500">
                <div className="flex items-center gap-1">
                  <MessageSquare className="w-4 h-4" />
                  <span>3年累计 {historical?.totalReviews3Years || 0} 条</span>
                </div>
                <div className="flex items-center gap-1">
                  <LineChart className="w-4 h-4" />
                  <span>均分 {historical?.averageRating3Years || 0}</span>
                </div>
              </div>
              {/* 新增：活跃天数 & 峰值月份 */}
              <div className="flex items-center gap-4 mt-2 text-sm text-slate-500">
                <div className="flex items-center gap-1">
                  <Calendar className="w-4 h-4" />
                  <span>活跃天数 {currentData.activeDays || 0} 天</span>
                </div>
                <div className="flex items-center gap-1">
                  <Flame className="w-4 h-4 text-rose-500" />
                  <span>峰值月份 {currentData.peakMonth?.month || '-'}月 ({currentData.peakMonth?.count || 0}条)</span>
                </div>
              </div>
              <Button
                className="mt-4 bg-orange-50 hover:bg-orange-100 text-orange-600 border-orange-200"
                onClick={handleGenerate}
                disabled={generating}
              >
                <RefreshCw className={`w-4 h-4 mr-2 ${generating ? 'animate-spin' : ''}`} />
                {generating ? '生成中...' : '重新生成'}
              </Button>
            </Card>

            {/* Tab Navigation */}
            <div className="flex bg-slate-100 rounded-lg p-1">
              {[
                { key: 'overview', label: '总览', icon: BarChart3 },
                { key: 'reply', label: '回复分析', icon: MessageSquare },
                { key: 'trends', label: '历史趋势', icon: LineChart },
                { key: 'comparison', label: '年度对比', icon: Activity }
              ].map(tab => (
                <button
                  key={tab.key}
                  onClick={() => setActiveTab(tab.key as any)}
                  className={`flex-1 flex items-center justify-center gap-1 py-2 rounded-md text-sm font-medium transition-all ${
                    activeTab === tab.key
                      ? 'bg-white text-indigo-600 shadow-sm'
                      : 'text-slate-500 hover:text-slate-700'
                  }`}
                >
                  <tab.icon className="w-4 h-4" />
                  <span className="hidden sm:inline">{tab.label}</span>
                </button>
              ))}
            </div>

            {/* ==================== OVERVIEW TAB ==================== */}
            {activeTab === 'overview' && (
              <>
                {/* Year-over-Year Comparison */}
                <Card className="p-6 bg-white border-slate-100 shadow-sm">
                  <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-emerald-500" />
                    同比增长
                  </h3>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-slate-600">评价总数</span>
                      <div className="flex items-center gap-1">
                        {getTrendIcon(insights.yearOverYear.reviewGrowth)}
                        <span className={`font-bold ${insights.yearOverYear.reviewGrowth > 0 ? 'text-emerald-600' : 'text-red-600'}`}>
                          {insights.yearOverYear.reviewGrowth > 0 ? '+' : ''}{insights.yearOverYear.reviewGrowth}%
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-slate-600">平均评分</span>
                      <div className="flex items-center gap-1">
                        {getTrendIcon(insights.yearOverYear.ratingChange)}
                        <span className={`font-bold ${insights.yearOverYear.ratingChange > 0 ? 'text-emerald-600' : 'text-red-600'}`}>
                          {insights.yearOverYear.ratingChange > 0 ? '+' : ''}{insights.yearOverYear.ratingChange}
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-slate-600">回复率</span>
                      <div className="flex items-center gap-1">
                        {getTrendIcon(insights.yearOverYear.replyRateChange)}
                        <span className={`font-bold ${insights.yearOverYear.replyRateChange > 0 ? 'text-emerald-600' : 'text-red-600'}`}>
                          {insights.yearOverYear.replyRateChange > 0 ? '+' : ''}{insights.yearOverYear.replyRateChange}%
                        </span>
                      </div>
                    </div>
                  </div>
                </Card>

                {/* AI Insights Card */}
                {insights && (
                  <Card className="p-6 bg-gradient-to-br from-indigo-50 to-purple-50 border-indigo-100 shadow-sm">
                    <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                      <Brain className="w-5 h-5 text-indigo-600" />
                      AI 年度洞察
                    </h3>
                    {insights.aiSummary && (
                      <p className="text-sm text-slate-600 mb-4 leading-relaxed">{insights.aiSummary}</p>
                    )}
                    {insights.highlights.length > 0 && (
                      <div className="mb-3">
                        <p className="text-xs text-emerald-600 font-bold mb-2">年度亮点</p>
                        <div className="flex flex-wrap gap-1.5">
                          {insights.highlights.map((h, i) => (
                            <Badge key={i} variant="outline" className="text-xs bg-emerald-50 border-emerald-200 text-emerald-700">{h}</Badge>
                          ))}
                        </div>
                      </div>
                    )}
                    {insights.improvements.length > 0 && (
                      <div className="mb-3">
                        <p className="text-xs text-amber-600 font-bold mb-2">改进方向</p>
                        <div className="flex flex-wrap gap-1.5">
                          {insights.improvements.map((imp, i) => (
                            <Badge key={i} variant="outline" className="text-xs bg-amber-50 border-amber-200 text-amber-700">{imp}</Badge>
                          ))}
                        </div>
                      </div>
                    )}
                    {insights.recommendations.length > 0 && (
                      <div>
                        <p className="text-xs text-indigo-600 font-bold mb-2">AI 建议</p>
                        <ul className="space-y-1">
                          {insights.recommendations.map((rec, i) => (
                            <li key={i} className="text-xs text-slate-600 flex items-start gap-1">
                              <Sparkles className="w-3 h-3 text-indigo-400 mt-0.5 shrink-0" />
                              {rec}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </Card>
                )}

                {/* 新增：评分分布 */}
                {renderRatingDist()}

                {/* 新增：平台来源分布 */}
                {renderPlatformDist()}

                {/* Core Stats */}
                <div className="grid grid-cols-2 gap-3">
                  <Card className="p-4 bg-slate-50 border-slate-100">
                    <MessageSquare className="w-6 h-6 text-indigo-500 mb-2" />
                    <p className="text-2xl font-black text-slate-900">{currentData.totalReviews.toLocaleString()}</p>
                    <p className="text-xs text-slate-400">总评价</p>
                  </Card>
                  <Card className="p-4 bg-slate-50 border-slate-100">
                    <Star className="w-6 h-6 text-amber-500 mb-2 fill-amber-400" />
                    <p className="text-2xl font-black text-slate-900">{currentData.averageRating}</p>
                    <p className="text-xs text-slate-400">平均评分</p>
                  </Card>
                  <Card className="p-4 bg-slate-50 border-slate-100">
                    <ThumbsUp className="w-6 h-6 text-emerald-500 mb-2" />
                    <p className="text-2xl font-black text-slate-900">{currentData.sentiment.positive}%</p>
                    <p className="text-xs text-slate-400">好评率</p>
                  </Card>
                  <Card className="p-4 bg-slate-50 border-slate-100">
                    <ThumbsDown className="w-6 h-6 text-rose-500 mb-2" />
                    <p className="text-2xl font-black text-slate-900">{currentData.sentiment.negative}%</p>
                    <p className="text-xs text-slate-400">差评率</p>
                  </Card>
                </div>

                {/* Category Scores */}
                <Card className="p-6">
                  <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                    <PieChart className="w-5 h-5 text-purple-600" />
                    维度评分
                  </h3>
                  <div className="space-y-3">
                    {Object.entries(currentData.categoryScores).map(([key, value]) => {
                      const labels: Record<string, string> = {
                        service: '服务',
                        food: '菜品',
                        environment: '环境',
                        price: '性价比',
                        speed: '速度'
                      };
                      return (
                        <div key={key}>
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-sm text-slate-600">{labels[key] || key}</span>
                            <span className="text-sm font-bold text-slate-700">{value}分</span>
                          </div>
                          <div className="bg-slate-100 rounded-full h-2">
                            <div
                              className="bg-gradient-to-r from-indigo-500 to-purple-500 h-full rounded-full transition-all duration-700"
                              style={{ width: `${(num(value) / 5) * 100}%` }}
                            ></div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </Card>

                {/* Top Keywords */}
                <Card className="p-6">
                  <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-purple-600" />
                    年度热词
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {currentData.topKeywords.map((kw, i) => (
                      <Badge
                        key={i}
                        variant="outline"
                        className={`text-sm py-1.5 px-3 ${
                          kw.sentiment === 'positive'
                            ? 'border-emerald-300 text-emerald-700 bg-emerald-50'
                            : kw.sentiment === 'negative'
                            ? 'border-rose-300 text-rose-700 bg-rose-50'
                            : 'border-slate-300 text-slate-700 bg-slate-50'
                        }`}
                      >
                        {kw.word} ({kw.count})
                      </Badge>
                    ))}
                  </div>
                </Card>
              </>
            )}

            {/* ==================== REPLY TAB ==================== */}
            {activeTab === 'reply' && (
              <>
                {/* Reply Rate Card */}
                <Card className="p-6 bg-white border-slate-100 shadow-sm">
                  <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                    <MessageSquare className="w-5 h-5 text-blue-500" />
                    商家回复分析
                  </h3>

                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div className="text-center">
                      <div className="relative w-20 h-20 mx-auto mb-2">
                        <div className="absolute inset-0 flex items-center justify-center">
                          <span className="text-2xl font-black text-slate-900">{currentData.replyStats.replyRate}%</span>
                        </div>
                        <svg className="w-20 h-20 transform -rotate-90">
                          <circle cx="40" cy="40" r="36" stroke="#e2e8f0" strokeWidth="8" fill="none" />
                          <circle
                            cx="40" cy="40" r="36"
                            stroke="#3b82f6"
                            strokeWidth="8"
                            fill="none"
                            strokeDasharray={`${2 * Math.PI * 36}`}
                            strokeDashoffset={`${2 * Math.PI * 36 * (1 - currentData.replyStats.replyRate / 100)}`}
                            className="transition-all duration-1000"
                          />
                        </svg>
                      </div>
                      <p className="text-xs text-slate-400">回复率</p>
                    </div>
                    <div className="text-center flex flex-col justify-center">
                      <p className="text-3xl font-black text-slate-900 mb-1">{currentData.replyStats.avgReplyTime}h</p>
                      <p className="text-xs text-slate-400">平均回复时间</p>
                    </div>
                  </div>

                  {/* 新增：回复情感分布 */}
                  {renderReplySentiment()}

                  <div className="space-y-2 mt-4">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-600">已回复</span>
                      <span className="font-bold text-emerald-500">{currentData.replyStats.repliedCount} 条</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-600">未回复</span>
                      <span className="font-bold text-rose-500">{currentData.replyStats.unrepliedCount} 条</span>
                    </div>
                  </div>
                </Card>
              </>
            )}

            {/* ==================== TRENDS TAB ==================== */}
            {activeTab === 'trends' && (
              <>
                {/* Monthly Trend Chart */}
                <Card className="p-6">
                  <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                    <LineChart className="w-5 h-5 text-indigo-600" />
                    月度评价趋势
                  </h3>
                  <div className="space-y-3">
                    {currentData.monthlyData.map((month, i) => (
                      <div key={i}>
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs text-slate-500 w-10">{month.month}月</span>
                          <div className="flex-1 mx-3">
                            <div className="bg-slate-100 rounded-full h-3">
                              <div className="bg-indigo-500 h-full rounded-full transition-all duration-700" style={{ width: `${(num(month.count) / 500) * 100}%` }}></div>
                            </div>
                          </div>
                          <span className="text-xs text-slate-700 w-16 text-right">{month.count}条 / {month.avgRating}分</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>

                {/* 新增：月度情感 & 回复率趋势 */}
                {renderMonthlySentiment()}
              </>
            )}

            {/* ==================== COMPARISON TAB ==================== */}
            {activeTab === 'comparison' && historical && (
              <>
                {/* Comparison Table */}
                <Card className="p-6">
                  <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                    <Activity className="w-5 h-5 text-indigo-600" />
                    年度数据对比
                  </h3>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b border-slate-200">
                          <th className="text-left py-2 text-slate-500">指标</th>
                          <th className="text-center py-2 text-slate-500">2023</th>
                          <th className="text-center py-2 text-slate-500">2024</th>
                          <th className="text-center py-2 text-indigo-600">2025</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr className="border-b border-slate-100">
                          <td className="py-3 text-slate-700">总评价数</td>
                          <td className="text-center py-3">{yearlyData[2023]?.totalReviews}</td>
                          <td className="text-center py-3">{yearlyData[2024]?.totalReviews}</td>
                          <td className="text-center py-3 font-bold text-indigo-600">{yearlyData[2025]?.totalReviews}</td>
                        </tr>
                        <tr className="border-b border-slate-100">
                          <td className="py-3 text-slate-700">平均评分</td>
                          <td className="text-center py-3">{yearlyData[2023]?.averageRating}</td>
                          <td className="text-center py-3">{yearlyData[2024]?.averageRating}</td>
                          <td className="text-center py-3 font-bold text-indigo-600">{yearlyData[2025]?.averageRating}</td>
                        </tr>
                        <tr className="border-b border-slate-100">
                          <td className="py-3 text-slate-700">好评率</td>
                          <td className="text-center py-3">{yearlyData[2023]?.sentiment.positive}%</td>
                          <td className="text-center py-3">{yearlyData[2024]?.sentiment.positive}%</td>
                          <td className="text-center py-3 font-bold text-indigo-600">{yearlyData[2025]?.sentiment.positive}%</td>
                        </tr>
                        <tr>
                          <td className="py-3 text-slate-700">回复率</td>
                          <td className="text-center py-3">{yearlyData[2023]?.replyStats.replyRate}%</td>
                          <td className="text-center py-3">{yearlyData[2024]?.replyStats.replyRate}%</td>
                          <td className="text-center py-3 font-bold text-indigo-600">{yearlyData[2025]?.replyStats.replyRate}%</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </Card>

                {/* 新增：最佳/最差月份对比 */}
                <Card className="p-6">
                  <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                    <Award className="w-5 h-5 text-amber-500" />
                    最佳 & 最差月份
                  </h3>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="p-4 bg-emerald-50 rounded-lg border border-emerald-200">
                      <p className="text-xs text-emerald-600 font-bold mb-1">最佳月份</p>
                      <p className="text-2xl font-black text-emerald-700">
                        {currentData.peakMonth?.month || '-'}月
                      </p>
                      <p className="text-xs text-emerald-500 mt-1">{currentData.peakMonth?.count || 0} 条评论</p>
                    </div>
                    <div className="p-4 bg-rose-50 rounded-lg border border-rose-200">
                      <p className="text-xs text-rose-600 font-bold mb-1">最差月份</p>
                      {(() => {
                        const monthlyArr = currentData.monthlyData || [];
                        const worst = monthlyArr.reduce((min: any, m: any) =>
                          (m.count || 0) < (min.count || Infinity) ? m : min, { month: '-', count: Infinity });
                        return (
                          <p className="text-2xl font-black text-rose-700">
                            {worst.month !== '-' ? `${worst.month}月` : '-'}
                          </p>
                        );
                      })()}
                    </div>
                  </div>
                </Card>
              </>
            )}
          </>
        )}
      </div>
    </MobileLayout>
  );
};

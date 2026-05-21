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

  const loadData = async (year: number) => {
    try {
      setLoading(true);
      const data = await fetchAnnualReport(year);
      setYearlyData(prev => ({ ...prev, [year]: data.yearlyData }));
      setInsights(data.insights);
      setHistorical(data.historicalTrends);
    } catch (err) {
      console.error('加载年度报告失败', err);
    } finally {
      setLoading(false);
    }
  };

  // 初始化时预加载所有年份数据（用于年度对比 tab）
  useEffect(() => {
    setLoading(true);
    const allYears = [2023, 2024, 2025];
    let loaded = 0;
    allYears.forEach(y => {
      fetchAnnualReport(y).then(data => {
        setYearlyData(prev => ({ ...prev, [y]: data.yearlyData }));
        loaded++;
        if (loaded === allYears.length) setLoading(false);
      }).catch(() => {
        loaded++;
        if (loaded === allYears.length) setLoading(false);
      });
    });
  }, []);

  // 切换年份时更新 insights 和 historical
  useEffect(() => {
    if (lastYearRef.current === selectedYear) return;
    lastYearRef.current = selectedYear;
    fetchAnnualReport(selectedYear).then(data => {
      setInsights(data.insights);
      setHistorical(data.historicalTrends);
    }).catch(console.error);
  }, [selectedYear]);

  const handleExport = () => {
    success('导出报告', '正在生成精美 PDF 报告...');
  };

  const handleBack = () => {
    navigate('/mobile/insights');
  };

  const currentData = yearlyData[selectedYear];

  const renderStars = (rating: number) => {
    const stars = [];
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

  if (loading && !currentData) {
    return (
      <MobileLayout title={`${selectedYear} 年度报告`}>
        <div className="space-y-6 p-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
          {/* 标题骨架 */}
          <Skeleton lines={2} className="p-6" />
          
          {/* 统计卡片骨架 */}
          <div className="flex gap-3">
            <Skeleton lines={3} card={true} className="flex-1 p-4" />
            <Skeleton lines={3} card={true} className="flex-1 p-4" />
          </div>
          
          {/* 图表骨架 */}
          <Skeleton lines={4} card={true} className="p-6" />
          
          {/* 列表骨架 */}
          <Skeleton lines={4} card={true} className="p-6" />
          
          {/* 底部骨架 */}
          <Skeleton lines={3} card={true} className="p-6" />
        </div>
      </MobileLayout>
    );
  }

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
          <Button variant="outline" size="sm" onClick={handleExport} className="gap-1">
            <Download className="w-4 h-4" /> 导出
          </Button>
        </div>

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
              <Button
                className="mt-4 bg-orange-50 hover:bg-orange-100 text-orange-600 border-orange-200"
                onClick={() => loadData(selectedYear)}
              >
                <RefreshCw className="w-4 h-4 mr-2" /> 重新生成
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

            {/* Overview Tab */}
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

                {/* Market & Competitor Card */}
                {currentData && (
                  <div className="grid grid-cols-2 gap-3">
                    {currentData.competitorAvgRating !== undefined && (
                      <Card className="p-4 bg-slate-50 border-slate-100">
                        <Trophy className="w-6 h-6 text-amber-500 mb-2" />
                        <p className="text-2xl font-black text-slate-900">{currentData.competitorAvgRating}</p>
                        <p className="text-xs text-slate-400">竞品平均分</p>
                      </Card>
                    )}
                    {currentData.marketShare !== undefined && (
                      <Card className="p-4 bg-slate-50 border-slate-100">
                        <Target className="w-6 h-6 text-indigo-500 mb-2" />
                        <p className="text-2xl font-black text-slate-900">{currentData.marketShare}%</p>
                        <p className="text-xs text-slate-400">市场份额</p>
                      </Card>
                    )}
                  </div>
                )}

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
                            <span className="text-sm text-slate-600">{labels[key]}</span>
                            <span className="text-sm font-bold text-slate-700">{value}分</span>
                          </div>
                          <div className="bg-slate-100 rounded-full h-2">
                            <div
                              className="bg-gradient-to-r from-indigo-500 to-purple-500 h-full rounded-full transition-all duration-700"
                              style={{ width: `${(value / 5) * 100}%` }}
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

            {/* Reply Analysis Tab */}
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

                  <div className="space-y-2">
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

            {/* Historical Trends Tab */}
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
                              <div className="bg-indigo-500 h-full rounded-full transition-all duration-700" style={{ width: `${(month.count / 500) * 100}%` }}></div>
                            </div>
                          </div>
                          <span className="text-xs text-slate-700 w-16 text-right">{month.count}条 / {month.avgRating}分</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>
              </>
            )}

            {/* Year Comparison Tab */}
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
              </>
            )}
          </>
        )}
      </div>
    </MobileLayout>
  );
};

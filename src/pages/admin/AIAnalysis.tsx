import React, { useState, useEffect } from 'react';
import {
  Brain,
  BarChart3,
  ShieldAlert,
  Gavel,
  History,
  MessageSquare,
  ChevronLeft,
  ChevronRight,
  Download,
  RefreshCw,
  Search,
  Filter,
  Eye,
  CheckCircle2,
  XCircle,
  Lightbulb
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Input } from '../../components/ui/input';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../../components/ui/tabs';
import { AdminLayout } from '../../components/AdminLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';
import {
  fetchTopics,
  fetchSentimentSummary,
  fetchRiskLevels,
  fetchReplyHistory,
  fetchReplyStats,
  fetchAppealSuggestions
} from '../../api/ai-analysis';
import type {
  Topic,
  SentimentSummary,
  RiskLevels,
  ReplyRecord,
  ReplyStats,
  AppealSuggestion
} from '../../api/ai-analysis';

export const AIAnalysis: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'analysis' | 'history' | 'appeal'>('analysis');
  const [topics, setTopics] = useState<Topic[]>([]);
  const [sentimentSummary, setSentimentSummary] = useState<SentimentSummary | null>(null);
  const [riskLevels, setRiskLevels] = useState<RiskLevels | null>(null);
  const [replyHistory, setReplyHistory] = useState<ReplyRecord[]>([]);
  const [replyStats, setReplyStats] = useState<ReplyStats | null>(null);
  const [appealSuggestions, setAppealSuggestions] = useState<AppealSuggestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchKeyword, setSearchKeyword] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 10;

  const { success, error: showError } = useToast();
  const fetchedRef = React.useRef(false);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [topicsData, summaryData, riskData, historyData, statsData, appealData] = await Promise.all([
        fetchTopics(),
        fetchSentimentSummary(),
        fetchRiskLevels(),
        fetchReplyHistory(),
        fetchReplyStats(),
        fetchAppealSuggestions(),
      ]);
      setTopics(topicsData);
      setSentimentSummary(summaryData);
      setRiskLevels(riskData);
      setReplyHistory(historyData);
      setReplyStats(statsData);
      setAppealSuggestions(appealData);
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
    success('导出报告', '正在导出AI分析完整报告...');
  };

  const handleSubmitAppeal = (id: string) => {
    success('申诉已提交', `申诉工单 ${id} 已提交至平台`);
  };

  const handleIgnoreAppeal = (id: string) => {
    showError('已忽略', `申诉建议 ${id} 已忽略`);
  };

  // 筛选和搜索
  const filteredHistory = replyHistory.filter(record => {
    if (searchKeyword) {
      return record.user.includes(searchKeyword) ||
             record.content.includes(searchKeyword);
    }
    return true;
  });

  const filteredAppeals = appealSuggestions.filter(appeal => {
    if (searchKeyword) {
      return (appeal.user || '').includes(searchKeyword) ||
             appeal.content.includes(searchKeyword);
    }
    return true;
  });

  // 分页
  const totalPagesHistory = Math.ceil(filteredHistory.length / pageSize);
  const paginatedHistory = filteredHistory.slice(
    (currentPage - 1) * pageSize,
    currentPage * pageSize
  );

  const totalPagesAppeals = Math.ceil(filteredAppeals.length / pageSize);
  const paginatedAppeals = filteredAppeals.slice(
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
            <h2 className="text-2xl font-bold text-slate-900">AI 智能分析</h2>
            <p className="text-slate-500 mt-1">语义分析、风险分级、自动回复历史、智能申诉管理</p>
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

        {/* Tab Switcher */}
        <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as any)}>
          <TabsList className="bg-white border border-slate-100 p-1 rounded-2xl w-fit">
            <TabsTrigger value="analysis" className="px-6 py-2 rounded-xl data-[state=active]:bg-orange-500 data-[state=active]:text-white">
              <BarChart3 className="w-4 h-4 mr-2" />
              语义分析
            </TabsTrigger>
            <TabsTrigger value="history" className="px-6 py-2 rounded-xl data-[state=active]:bg-orange-500 data-[state=active]:text-white">
              <History className="w-4 h-4 mr-2" />
              自动回复
            </TabsTrigger>
            <TabsTrigger value="appeal" className="px-6 py-2 rounded-xl data-[state=active]:bg-orange-500 data-[state=active]:text-white">
              <Gavel className="w-4 h-4 mr-2" />
              智能申诉
            </TabsTrigger>
          </TabsList>

          {/* Analysis Tab */}
          <TabsContent value="analysis">
            {sentimentSummary && riskLevels && (
              <div className="space-y-6">
                {/* Sentiment Summary */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <Card className="p-6 border-none shadow-sm">
                    <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">今日情感指数</h3>
                    <div className="flex items-baseline gap-2">
                      <span className="text-4xl font-black text-slate-900">{sentimentSummary.score}</span>
                      <span className="text-emerald-500 text-sm font-bold">{sentimentSummary.trend}</span>
                    </div>
                    <div className="mt-4 space-y-4">
                      <div className="flex items-center gap-4">
                        <div className="flex-1 h-3 bg-slate-100 rounded-full overflow-hidden flex">
                          <div className="bg-emerald-500 h-full" style={{ width: `${sentimentSummary.positive}%` }}></div>
                          <div className="bg-rose-500 h-full" style={{ width: `${sentimentSummary.negative}%` }}></div>
                        </div>
                      </div>
                      <div className="flex justify-between text-xs font-bold">
                        <div className="flex items-center gap-1.5 text-emerald-600 uppercase">
                          正面 {sentimentSummary.positive}%
                        </div>
                        <div className="flex items-center gap-1.5 text-rose-500 uppercase">
                          负面 {sentimentSummary.negative}%
                        </div>
                      </div>
                    </div>
                    <div className="mt-4 flex items-center gap-1 text-xs text-slate-400">
                      <CheckCircle2 className="w-3 h-3 text-emerald-500" /> AI识别率: <span className="text-slate-900 font-bold">{sentimentSummary.aiAccuracy}%</span>
                    </div>
                  </Card>

                  {/* Risk Levels */}
                  <Card className="p-6 border-none shadow-sm">
                    <h3 className="text-sm font-bold text-slate-800 mb-4">风险分级概览</h3>
                    <div className="space-y-4">
                      {[
                        { level: 'high', label: '高风险', color: 'bg-rose-500', bg: 'bg-rose-50', text: 'text-rose-600' },
                        { level: 'medium', label: '中风险', color: 'bg-amber-500', bg: 'bg-amber-50', text: 'text-amber-600' },
                        { level: 'low', label: '低风险', color: 'bg-yellow-500', bg: 'bg-yellow-50', text: 'text-yellow-600' },
                      ].map((risk, i) => (
                        <div key={i} className={`p-4 ${risk.bg} rounded-xl`}>
                          <div className="flex items-center justify-between mb-2">
                            <span className={`text-sm font-bold ${risk.text}`}>{risk.label}</span>
                            <span className={`text-2xl font-black ${risk.text}`}>
                              {risk.level === 'high' ? riskLevels.high.count :
                               risk.level === 'medium' ? riskLevels.medium.count :
                               riskLevels.low.count}
                            </span>
                          </div>
                          <p className={`text-xs ${risk.text} opacity-70`}>
                            {risk.level === 'high' ? riskLevels.high.desc :
                             risk.level === 'medium' ? riskLevels.medium.desc :
                             riskLevels.low.desc}
                          </p>
                        </div>
                      ))}
                    </div>
                  </Card>
                </div>

                {/* Topics */}
                <Card className="p-6 border-none shadow-sm">
                  <h3 className="text-sm font-bold text-slate-800 mb-4">语义分析主题</h3>
                  <div className="space-y-3">
                    {topics.map((topic, i) => (
                      <div key={i} className="flex items-center justify-between p-3 bg-slate-50 rounded-xl">
                        <div className="flex items-center gap-3">
                          <div className="w-8 h-8 rounded-lg bg-orange-50 flex items-center justify-center text-orange-600 font-bold text-xs">
                            {i + 1}
                          </div>
                          <span className="text-sm font-medium text-slate-700">{topic.label}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Badge className="bg-slate-100 text-slate-500 border-none text-xs">
                            {topic.count} 条
                          </Badge>
                          <Badge className={topic.trend.includes('+') ? "bg-emerald-100 text-emerald-700" : "bg-rose-100 text-rose-700"}>
                            {topic.trend}
                          </Badge>
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>
              </div>
            )}
          </TabsContent>

          {/* History Tab */}
          <TabsContent value="history">
            {replyStats && (
              <div className="space-y-6">
                {/* Stats */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {[
                    { label: '今日回复', val: replyStats.todayCount.toString(), icon: MessageSquare, color: 'text-orange-600', bg: 'bg-orange-50' },
                    { label: '自动拦截', val: replyStats.autoBlocked.toString(), icon: Brain, color: 'text-amber-600', bg: 'bg-amber-50' },
                    { label: '平均时长', val: replyStats.avgTime, icon: History, color: 'text-emerald-600', bg: 'bg-emerald-50' },
                  ].map((s, i) => (
                    <Card key={i} className="p-6 border-none shadow-sm text-center">
                      <div className={`w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3 ${s.bg}`}>
                        <s.icon className={`w-6 h-6 ${s.color}`} />
                      </div>
                      <div className="text-2xl font-bold text-slate-900">{s.val}</div>
                      <div className="text-xs text-slate-400 font-bold uppercase">{s.label}</div>
                    </Card>
                  ))}
                </div>

                {/* Search */}
                <Card className="p-4 border-none shadow-sm">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <Input
                      placeholder="搜索用户名或评论内容..."
                      className="pl-9"
                      value={searchKeyword}
                      onChange={(e) => setSearchKeyword(e.target.value)}
                    />
                  </div>
                </Card>

                {/* History Table */}
                <Card className="border-none shadow-sm overflow-hidden">
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead className="bg-slate-50 border-b border-slate-100">
                        <tr>
                          <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">用户</th>
                          <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">评分</th>
                          <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">评论内容</th>
                          <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">AI回复</th>
                          <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">状态</th>
                          <th className="p-4 text-left text-xs font-semibold text-slate-600 uppercase">时间</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-50">
                        {paginatedHistory.map((item) => (
                          <tr key={item.id} className="hover:bg-slate-50 transition-colors">
                            <td className="p-4">
                              <span className="text-sm font-medium text-slate-900">{item.user}</span>
                            </td>
                            <td className="p-4">
                              <div className="flex items-center gap-1">
                                {[1, 2, 3, 4, 5].map(star => (
                                  <span key={star} className={cn("text-sm", star <= item.rating ? "text-amber-400" : "text-slate-200")}>★</span>
                                ))}
                              </div>
                            </td>
                            <td className="p-4 max-w-md">
                              <p className="text-sm text-slate-600 line-clamp-2">{item.content}</p>
                            </td>
                            <td className="p-4 max-w-md">
                              <p className="text-sm text-orange-600 line-clamp-2">{item.reply}</p>
                            </td>
                            <td className="p-4">
                              <Badge className={cn(
                                "border-none text-xs",
                                item.status === '自动已发' ? "bg-emerald-100 text-emerald-700" : "bg-orange-100 text-orange-700"
                              )}>
                                {item.status}
                              </Badge>
                            </td>
                            <td className="p-4">
                              <span className="text-xs text-slate-400">{item.time}</span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>

                  {/* Pagination */}
                  <div className="flex items-center justify-between p-4 border-t border-slate-100">
                    <p className="text-sm text-slate-500">
                      显示 {((currentPage - 1) * pageSize) + 1}-{Math.min(currentPage * pageSize, filteredHistory.length)} 条，共 {filteredHistory.length} 条
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
                        {currentPage} / {totalPagesHistory}
                      </span>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setCurrentPage(Math.min(totalPagesHistory, currentPage + 1))}
                        disabled={currentPage === totalPagesHistory}
                      >
                        <ChevronRight className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </Card>
              </div>
            )}
          </TabsContent>

          {/* Appeal Tab */}
          <TabsContent value="appeal">
            {appealSuggestions.length > 0 && (
              <div className="space-y-6">
                <Card className="p-4 border-none shadow-sm bg-amber-50 border-amber-200">
                  <div className="flex items-start gap-3">
                    <Lightbulb className="w-5 h-5 text-amber-600 flex-shrink-0" />
                    <div>
                      <h4 className="text-sm font-bold text-amber-900">智能申诉建议</h4>
                      <p className="text-xs text-amber-700 leading-relaxed mt-1">
                        AI 识别出 {appealSuggestions.length} 条疑似"恶意评价"或"责任归属有误"的评论，建议发起平台申诉。
                      </p>
                    </div>
                  </div>
                </Card>

                {paginatedAppeals.map((item) => (
                  <Card key={item.id} className="p-6 border-none shadow-sm">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <span className="text-sm font-bold text-slate-800">{item.user}</span>
                        <span className="text-xs text-slate-400 ml-2">{item.platform} · {item.date}</span>
                      </div>
                      <Badge className="bg-rose-100 text-rose-600 border-none text-xs">疑似恶意</Badge>
                    </div>
                    <div className="bg-slate-50 p-4 rounded-xl mb-4">
                      <p className="text-sm text-slate-500 italic">"{item.content}"</p>
                    </div>
                    <div className="p-4 bg-orange-50 rounded-xl border border-orange-100 mb-4">
                      <p className="text-xs font-bold text-orange-600 mb-2 flex items-center gap-1">
                        <MessageSquare className="w-3 h-3" /> AI 生成申诉工单草稿
                      </p>
                      <p className="text-sm text-slate-600 leading-relaxed">
                        {item.draft}
                      </p>
                    </div>
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        className="flex-1 h-10 rounded-xl text-xs"
                        onClick={() => handleIgnoreAppeal(item.id!)}
                      >
                        忽略
                      </Button>
                      <Button
                        className="flex-[2] h-10 rounded-xl text-xs bg-orange-500 hover:bg-orange-600 text-white"
                        onClick={() => handleSubmitAppeal(item.id!)}
                      >
                        一键提交申诉
                      </Button>
                    </div>
                  </Card>
                ))}

                {/* Pagination */}
                <div className="flex items-center justify-between p-4">
                  <p className="text-sm text-slate-500">
                    显示 {((currentPage - 1) * pageSize) + 1}-{Math.min(currentPage * pageSize, filteredAppeals.length)} 条，共 {filteredAppeals.length} 条
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
                      {currentPage} / {totalPagesAppeals}
                    </span>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setCurrentPage(Math.min(totalPagesAppeals, currentPage + 1))}
                      disabled={currentPage === totalPagesAppeals}
                    >
                      <ChevronRight className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </div>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </AdminLayout>
  );
};

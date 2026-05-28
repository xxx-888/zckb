import React, { useState, useEffect } from 'react';
import {
  Brain,
  TrendingUp,
  MessageCircle,
  ThumbsUp,
  ThumbsDown,
  BarChart3,
  ChevronRight,
  Lightbulb,
  History,
  CheckCircle2,
  Clock,
  Zap,
  Star,
  ShieldAlert,
  FileText,
  AlertTriangle,
  Gavel,
  Sparkles
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { Skeleton } from '../../components/ui/skeleton';
import { Button } from '../../components/ui/button';
import { MobileLayout, useStore } from '../../components/MobileLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';
import { useNavigate } from 'react-router-dom';
import {
  fetchTopics,
  fetchTagClustering,
  fetchSentimentSummary,
  fetchRiskLevels,
  fetchReplyHistory,
  fetchReplyStats,
  fetchAppealSuggestions
} from '../../api/ai-analysis';
import type { Topic, TagCluster, SentimentSummary, RiskLevels, ReplyRecord, ReplyStats, AppealSuggestion } from '../../api/ai-analysis';
import { useSubscription, SubscriptionPrompt } from '../../hooks/use-subscription-check';

export const AIAnalysis: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'analysis' | 'history' | 'appeal'>('analysis');
  const [topics, setTopics] = useState<Topic[]>([]);
  const [tagClustering, setTagClustering] = useState<TagCluster[]>([]);
  const [sentimentSummary, setSentimentSummary] = useState<SentimentSummary | null>(null);
  const [riskLevels, setRiskLevels] = useState<RiskLevels | null>(null);
  const [replyHistory, setReplyHistory] = useState<ReplyRecord[]>([]);
  const [replyStats, setReplyStats] = useState<ReplyStats | null>(null);
  const [appealSuggestions, setAppealSuggestions] = useState<AppealSuggestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { success } = useToast();
  const navigate = useNavigate();
  const { selectedStore } = useStore();

  // ===== 订阅状态检测 =====
  const {
    subscription,
    loading: subscriptionLoading,
    error: subscriptionError,
    hasValidSubscription,
  } = useSubscription();

  // ===== 数据加载（店铺变化时重新获取）=====
  useEffect(() => {
    if (!selectedStore?.id) {
      setLoading(false);
      return;
    }

    const loadData = async () => {
      try {
        setLoading(true);
        setError(null);
        const [topicsData, tagData, summaryData, riskData, historyData, statsData, appealData] = await Promise.all([
          fetchTopics(),
          fetchTagClustering(),
          fetchSentimentSummary(),
          fetchRiskLevels(),
          fetchReplyHistory(),
          fetchReplyStats(),
          fetchAppealSuggestions()
        ]);
        setTopics(topicsData);
        setTagClustering(tagData);
        setSentimentSummary(summaryData);
        setRiskLevels(riskData);
        setReplyHistory(historyData);
        setReplyStats(statsData);
        setAppealSuggestions(appealData);
      } catch (err) {
        console.error('[AIAnalysis] load error:', err);
        setError(err instanceof Error ? err.message : '获取数据失败');
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [selectedStore?.id]);

  // ===== 订阅加载中 =====
  if (subscriptionLoading) {
    return (
      <MobileLayout title="AI 智能分析">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-sm text-slate-400">正在检查订阅状态...</p>
          </div>
        </div>
      </MobileLayout>
    );
  }

  // ===== 无有效订阅 =====
  if (!hasValidSubscription) {
    return (
      <MobileLayout title="AI 智能分析">
        <SubscriptionPrompt featureName="AI 分析" />
      </MobileLayout>
    );
  }

  // ===== 数据加载中 =====
  if (loading) {
    return (
      <MobileLayout title="AI 智能分析">
        <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500 p-4">
          <Skeleton lines={1} className="h-8 w-48 mb-4" />
          <Card className="p-5">
            <Skeleton lines={1} className="h-8 w-32 mb-4" />
            <Skeleton lines={3} className="space-y-2" />
          </Card>
          <Skeleton card className="mt-4" />
          <Skeleton lines={5} className="mt-4 space-y-3" />
        </div>
      </MobileLayout>
    );
  }

  return (
    <MobileLayout title="AI 智能分析">
      <div className="space-y-6 pb-24 animate-in fade-in slide-in-from-bottom-4 duration-500">

        {/* Tab Switcher */}
        <div className="flex bg-white p-1 rounded-2xl shadow-sm border border-slate-100 overflow-x-auto no-scrollbar">
          <button
            onClick={() => setActiveTab('analysis')}
            className={cn(
              "flex-1 py-2 px-3 rounded-xl text-[11px] font-bold transition-all flex items-center justify-center gap-1.5 whitespace-nowrap",
              activeTab === 'analysis' ? "bg-orange-500 text-white shadow-md shadow-orange-100" : "text-slate-500"
            )}
          >
            <BarChart3 className="w-3.5 h-3.5" /> 语义分析
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={cn(
              "flex-1 py-2 px-3 rounded-xl text-[11px] font-bold transition-all flex items-center justify-center gap-1.5 whitespace-nowrap",
              activeTab === 'history' ? "bg-orange-500 text-white shadow-md shadow-orange-100" : "text-slate-500"
            )}
          >
            <History className="w-3.5 h-3.5" /> 自动回复
          </button>
          <button
            onClick={() => setActiveTab('appeal')}
            className={cn(
              "flex-1 py-2 px-3 rounded-xl text-[11px] font-bold transition-all flex items-center justify-center gap-1.5 whitespace-nowrap",
              activeTab === 'appeal' ? "bg-orange-500 text-white shadow-md shadow-orange-100" : "text-slate-500"
            )}
          >
            <Gavel className="w-3.5 h-3.5" /> 智能申诉
          </button>
        </div>

        {activeTab === 'analysis' && (
          <>
            {/* 年度报告导航卡片 */}
            <Card
              className="p-5 bg-white border-slate-100 shadow-sm cursor-pointer hover:shadow-md transition-all duration-300"
              onClick={() => navigate('/mobile/annual-report')}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-2xl bg-orange-50 flex items-center justify-center">
                    <Sparkles className="w-6 h-6 text-orange-500" />
                  </div>
                  <div>
                    <h4 className="font-bold text-lg text-slate-900">年度口碑报告</h4>
                    <p className="text-sm text-slate-400">查看您的数字资产沉淀</p>
                  </div>
                </div>
                <ChevronRight className="w-6 h-6 text-slate-300" />
              </div>
            </Card>

            {/* Sentiment Summary */}
            {sentimentSummary && (
              <Card className="p-6 border-none shadow-md bg-white overflow-hidden relative">
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">今日情感指数</h3>
                    <div className="flex items-baseline gap-2 mt-1">
                      <span className="text-4xl font-black text-slate-900">{sentimentSummary.score}</span>
                      <span className="text-emerald-500 text-sm font-bold">{sentimentSummary.trend}</span>
                    </div>
                  </div>
                  <div className="flex flex-col items-end">
                    <div className="w-10 h-10 bg-orange-50 rounded-2xl flex items-center justify-center text-orange-600 mb-2">
                      <Brain className="w-5 h-5" />
                    </div>
                    <div className="flex items-center gap-1 text-[10px] text-slate-400">
                      <CheckCircle2 className="w-3 h-3 text-emerald-500" /> AI识别率: <span className="text-slate-900 font-bold">{sentimentSummary.aiAccuracy}%</span>
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <div className="flex items-center gap-4">
                    <div className="flex-1 h-3 bg-slate-100 rounded-full overflow-hidden flex">
                      <div className="bg-emerald-500 h-full" style={{ width: `${sentimentSummary.positive}%` }}></div>
                      <div className="bg-rose-500 h-full" style={{ width: `${sentimentSummary.negative}%` }}></div>
                    </div>
                  </div>
                  <div className="flex justify-between text-[10px] font-bold">
                    <div className="flex items-center gap-1.5 text-emerald-600 uppercase">
                      <ThumbsUp className="w-3 h-3" /> 正面 {sentimentSummary.positive}%
                    </div>
                    <div className="flex items-center gap-1.5 text-rose-500 uppercase">
                      <ThumbsDown className="w-3 h-3" /> 负面 {sentimentSummary.negative}%
                    </div>
                  </div>
                </div>
              </Card>
            )}

            {/* Risk Classification */}
            {riskLevels && (
              <div className="space-y-3">
                <h3 className="font-bold text-slate-800 text-sm px-1 flex items-center gap-2">
                  <ShieldAlert className="w-4 h-4 text-orange-500" /> 风险分级概览
                </h3>
                <div className="grid grid-cols-3 gap-2">
                  <div className="p-3 bg-rose-50 border border-rose-100 rounded-2xl text-center">
                    <p className="text-[10px] font-bold text-rose-400 uppercase mb-1">高风险</p>
                    <p className="text-xl font-black text-rose-600">{riskLevels.high.count}</p>
                    <p className="text-[8px] text-rose-400">{riskLevels.high.desc}</p>
                  </div>
                  <div className="p-3 bg-amber-50 border border-amber-100 rounded-2xl text-center">
                    <p className="text-[10px] font-bold text-amber-500 uppercase mb-1">中风险</p>
                    <p className="text-xl font-black text-amber-600">{riskLevels.medium.count}</p>
                    <p className="text-[8px] text-amber-400">{riskLevels.medium.desc}</p>
                  </div>
                  <div className="p-3 bg-yellow-50 border border-yellow-100 rounded-2xl text-center">
                    <p className="text-[10px] font-bold text-yellow-600 uppercase mb-1">低风险</p>
                    <p className="text-xl font-black text-yellow-600">{riskLevels.low.count}</p>
                    <p className="text-[8px] text-yellow-500">{riskLevels.low.desc}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Tag Clustering */}
            {tagClustering.length > 0 && (
              <div className="space-y-3">
                <h3 className="font-bold text-slate-800 text-sm px-1 flex justify-between items-center">
                  差评标签聚类 (一级/二级)
                  <span className="text-[10px] text-slate-400 font-normal">基于NLP自动聚合</span>
                </h3>
                <Card className="p-4 border-none shadow-sm space-y-4">
                  <div className="flex items-center gap-6">
                    <div className="relative w-24 h-24 rounded-full border-[12px] border-slate-100 flex items-center justify-center">
                      <div className="absolute inset-0 rounded-full border-[12px] border-orange-500" style={{ clipPath: 'polygon(50% 50%, 50% 0%, 100% 0%, 100% 100%, 50% 100%)' }}></div>
                      <div className="text-center">
                        <p className="text-xs font-black text-slate-900">{tagClustering.reduce((sum, t) => sum + t.percentage, 0)}</p>
                        <p className="text-[8px] text-slate-400">总差评</p>
                      </div>
                    </div>
                    <div className="flex-1 space-y-2">
                      {tagClustering.map((tag, i) => (
                        <div key={i} className="flex items-center justify-between text-[10px]">
                          <div className="flex items-center gap-1.5">
                            <div className={cn("w-1.5 h-1.5 rounded-full", tag.color)}></div>
                            <span className="font-bold text-slate-700">{tag.category}</span>
                          </div>
                          <span className="text-slate-400 font-medium">{tag.percentage}%</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="pt-3 border-t border-slate-50">
                    <p className="text-[10px] text-slate-500 leading-relaxed italic">
                      <span className="font-bold text-orange-600">{tagClustering[0]?.category}类</span>标签细分：{tagClustering[0]?.items.join('、')}
                    </p>
                  </div>
                </Card>
              </div>
            )}

            {/* AI Insights */}
            {topics.length > 0 && (
              <Card className="p-5 border-slate-100 shadow-sm bg-white">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-8 h-8 rounded-lg bg-amber-50 flex items-center justify-center">
                    <Lightbulb className="w-4 h-4 text-amber-500" />
                  </div>
                  <h3 className="font-bold text-sm text-slate-700 tracking-wide">AI 诊断简报</h3>
                </div>
                {(() => {
                  const negativeTopics = topics.filter(t => t.sentiment === 'negative');
                  const topNegative = negativeTopics.length > 0 ? negativeTopics.reduce((a, b) => (a.count >= b.count) ? a : b) : null;
                  if (topNegative) {
                    return (
                      <p className="text-xs text-slate-500 leading-relaxed mb-4">
                        本周"<span className="font-bold text-orange-600">{topNegative.label}</span>"相关的负面评价共 <span className="font-bold text-orange-600">{topNegative.count}条</span>，
                        趋势{topNegative.trend === 'up' ? '正在上升' : topNegative.trend === 'down' ? '有所下降' : '保持稳定'}。
                        建议相关部门跟进处理。
                      </p>
                    );
                  }
                  return (
                    <p className="text-xs text-slate-500 leading-relaxed mb-4">
                      本周数据无明显异常，整体评价{topics.filter(t => t.sentiment === 'positive').length > 0 ? '偏正面' : '稳定'}。
                    </p>
                  );
                })()}
                <button
                  className="w-full py-2.5 bg-orange-50 hover:bg-orange-100 text-orange-600 rounded-xl text-xs font-bold transition-all border border-orange-200"
                  onClick={() => navigate('/mobile/annual-report')}
                >
                  查看详细报告
                </button>
              </Card>
            )}
          </>
        )}

        {activeTab === 'history' && (
          <div className="space-y-4">
            {/* Reply Stats */}
            {replyStats && (
              <div className="grid grid-cols-3 gap-2">
                {[
                  { label: '今日回复', val: replyStats.todayCount.toString(), icon: MessageCircle, color: 'text-orange-600', bg: 'bg-orange-50' },
                  { label: '自动拦截', val: replyStats.autoBlocked.toString(), icon: Zap, color: 'text-amber-600', bg: 'bg-amber-50' },
                  { label: '平均时长', val: replyStats.avgTime, icon: Clock, color: 'text-emerald-600', bg: 'bg-emerald-50' },
                ].map((s, i) => (
                  <Card key={i} className="p-3 border-none shadow-sm text-center">
                    <div className={cn("w-8 h-8 rounded-lg flex items-center justify-center mx-auto mb-2", s.bg)}>
                      <s.icon className={cn("w-4 h-4", s.color)} />
                    </div>
                    <div className="text-lg font-bold text-slate-800">{s.val}</div>
                    <div className="text-[9px] text-slate-400 font-bold uppercase">{s.label}</div>
                  </Card>
                ))}
              </div>
            )}

            {/* History List */}
            <h3 className="font-bold text-slate-800 text-sm px-1 flex items-center justify-between">
              最近自动回复
              <button
                className="text-[10px] text-orange-600 font-bold"
              >
                全部记录
              </button>
            </h3>
            {replyHistory.map((item) => (
              <Card key={item.id} className="p-4 border-none shadow-sm space-y-3 bg-white">
                <div className="flex justify-between items-start">
                  <div className="flex flex-col">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-bold text-slate-800">{item.user}</span>
                      <div className="flex">
                        {[...Array(5)].map((_, i) => (
                          <Star key={i} className={cn("w-2 h-2", i < item.rating ? "text-amber-400 fill-amber-400" : "text-slate-200")} />
                        ))}
                      </div>
                    </div>
                    <span className="text-[10px] text-slate-400">{item.time}</span>
                  </div>
                  <Badge className={cn(
                    "text-[10px] border-none",
                    item.status === '自动已发' ? "bg-emerald-50 text-emerald-600" : "bg-orange-50 text-orange-600"
                  )}>
                    {item.status}
                  </Badge>
                </div>
                <div className="text-xs text-slate-500 bg-slate-50 p-2 rounded-lg border border-slate-100">
                  客户：{item.content}
                </div>
                <div className="text-xs text-orange-700 bg-orange-50 p-3 rounded-lg border border-orange-100 relative">
                  <div className="absolute -top-2 left-4 w-0 h-0 border-l-[6px] border-l-transparent border-r-[6px] border-r-transparent border-b-[6px] border-b-orange-50"></div>
                  AI：{item.reply}
                </div>
              </Card>
            ))}
          </div>
        )}

        {activeTab === 'appeal' && (
          <div className="space-y-4">
            {appealSuggestions.length > 0 ? (
              <>
                <div className="bg-amber-50 border border-amber-100 p-4 rounded-2xl flex items-start gap-3">
                  <AlertTriangle className="w-5 h-5 text-amber-600 flex-shrink-0" />
                  <div>
                    <h4 className="text-sm font-bold text-amber-900">智能申诉建议</h4>
                    <p className="text-xs text-amber-700 leading-relaxed mt-1">
                      AI 识别出 {appealSuggestions.length} 条疑似"恶意评价"或"责任归属有误"的评论，建议发起平台申诉。
                    </p>
                  </div>
                </div>

                {appealSuggestions.map((item) => (
                  <Card key={item.id || item.review_id} className="p-4 border-none shadow-sm space-y-4 bg-white">
                    <div className="flex justify-between items-start">
                      <div className="flex flex-col">
                        <span className="text-sm font-bold text-slate-800">{item.user || '匿名用户'}</span>
                        <span className="text-[10px] text-slate-400">{item.platform} · {item.date || ''}</span>
                      </div>
                      <Badge className="bg-rose-50 text-rose-600 border-none text-[10px]">疑似恶意</Badge>
                    </div>
                    <div className="text-xs text-slate-500 bg-slate-50 p-3 rounded-xl border border-slate-100 italic">
                      "{item.content}"
                    </div>
                    <div className="p-3 bg-orange-50 rounded-xl border border-orange-100">
                      <p className="text-[10px] font-bold text-orange-600 mb-2 flex items-center gap-1 uppercase">
                        <FileText className="w-3 h-3" /> AI 生成申诉工单草稿
                      </p>
                      <p className="text-xs text-slate-600 leading-relaxed">
                        {item.draft || item.appeal_content || '正在生成申诉内容...'}
                      </p>
                    </div>
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        className="flex-1 h-9 rounded-xl text-xs"
                      >
                        忽略
                      </Button>
                      <Button
                        className="flex-[2] h-9 rounded-xl text-xs bg-orange-500 hover:bg-orange-600 text-white"
                      >
                        一键提交申诉
                      </Button>
                    </div>
                  </Card>
                ))}
              </>
            ) : (
              <Card className="p-8 text-center">
                <ShieldAlert className="w-12 h-12 text-slate-300 mx-auto mb-3" />
                <p className="text-sm text-slate-500 mb-1">暂无申诉建议</p>
                <p className="text-xs text-slate-400">AI 未检测到疑似恶意评价</p>
              </Card>
            )}
          </div>
        )}
      </div>
    </MobileLayout>
  );
};

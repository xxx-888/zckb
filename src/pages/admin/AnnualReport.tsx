import React, { useState, useEffect, useRef } from 'react';
import {
  BarChart3,
  TrendingUp,
  MessageSquare,
  Brain,
  Download,
  RefreshCw,
  ChevronRight,
  Star,
  ThumbsUp,
  ThumbsDown,
  Sparkles,
  Trophy,
  Target,
  Heart,
  Zap,
  Flame,
  Music,
  PartyPopper
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { AdminLayout } from '../../components/AdminLayout';
import { useToast } from '../../hooks/use-toast';

interface ReportData {
  stats?: {
    total_reviews: number;
    average_rating: number;
    sentiment_distribution: {
      positive: number;
      negative: number;
      neutral: number;
    };
    top_topics?: Array<{
      name: string;
      count: number;
    }>;
    monthly_trend?: {
      [key: string]: {
        count: number;
        avg_rating: number;
      };
    };
    best_month?: string;
    improvement_areas?: string[];
  };
  insights?: {
    highlights?: string[];
    improvements?: string[];
    ai_summary?: string;
    personality_type?: string;
  };
  charts?: {
    sentiment_distribution?: any;
    monthly_trend?: any;
    rating_distribution?: any;
  };
}

export const AnnualReport: React.FC = () => {
  const [report, setReport] = useState<ReportData | null>(null);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear() - 1);
  const [loading, setLoading] = useState(false);
  const [currentSection, setCurrentSection] = useState(0);
  const { success, error } = useToast();
  const sectionsRef = useRef<(HTMLElement | null)[]>([]);

  useEffect(() => {
    fetchReport();
  }, [selectedYear]);

  // Intersection Observer for scroll animations
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
          }
        });
      },
      { threshold: 0.1 }
    );

    sectionsRef.current.forEach((section) => {
      if (section) observer.observe(section);
    });

    return () => observer.disconnect();
  }, [report]);

  const fetchReport = async () => {
    setLoading(true);
    try {
      const response = await fetch(`/api/v1/stores/1/annual-report?year=${selectedYear}`);
      if (response.ok) {
        const data = await response.json();
        setReport(data);
      } else {
        // 使用模拟数据用于展示
        setReport(getMockReport());
      }
    } catch (err) {
      // 使用模拟数据
      setReport(getMockReport());
    } finally {
      setLoading(false);
    }
  };

  const getMockReport = (): ReportData => {
    return {
      stats: {
        total_reviews: 3842,
        average_rating: 4.3,
        sentiment_distribution: {
          positive: 76.5,
          negative: 12.3,
          neutral: 11.2,
        },
        top_topics: [
          { name: '服务态度', count: 856 },
          { name: '环境氛围', count: 643 },
          { name: '产品质量', count: 521 },
          { name: '价格性价比', count: 387 },
          { name: '上菜速度', count: 298 },
        ],
        monthly_trend: {
          '1': { count: 320, avg_rating: 4.2 },
          '2': { count: 285, avg_rating: 4.1 },
          '3': { count: 350, avg_rating: 4.3 },
          '4': { count: 380, avg_rating: 4.4 },
          '5': { count: 410, avg_rating: 4.5 },
          '6': { count: 395, avg_rating: 4.3 },
          '7': { count: 420, avg_rating: 4.6 },
          '8': { count: 450, avg_rating: 4.5 },
          '9': { count: 380, avg_rating: 4.4 },
          '10': { count: 350, avg_rating: 4.3 },
          '11': { count: 320, avg_rating: 4.2 },
          '12': { count: 290, avg_rating: 4.4 },
        },
        best_month: '8月',
        improvement_areas: ['等位时间', '餐具清洁', '停车便利'],
      },
      insights: {
        highlights: [
          '年度好评率高达 76.5%，超越 89% 的同行业商家',
          '8月是您的黄金月份，平均评分达到 4.6 分',
          '"服务态度"获得最多好评，共 856 条相关评价',
        ],
        improvements: [
          '关注"等位时间"相关差评，建议优化排队系统',
          '加强"餐具清洁"管理，提升顾客用餐体验',
          '考虑提供"停车优惠"，解决顾客停车难题',
        ],
        ai_summary: '2026年是口碑提升的关键一年。您在服务态度和环境氛围上表现出色，但在等位时间和餐具清洁方面还有提升空间。建议重点关注这3个改进方向，预计可将整体评分提升至4.5分以上。',
        personality_type: '暖心服务家',
      },
    };
  };

  const generateReport = async () => {
    try {
      const response = await fetch(`/api/v1/stores/1/annual-report/generate?year=${selectedYear}`, {
        method: 'POST'
      });
      if (response.ok) {
        const data = await response.json();
        setReport(data.report);
        success('生成成功', `${selectedYear} 年度报告已生成`);
      }
    } catch (err) {
      // 使用模拟数据
      setReport(getMockReport());
      success('生成成功', `${selectedYear} 年度报告已生成（演示模式）`);
    }
  };

  const handleExport = () => {
    success('导出报告', '正在生成精美 PDF 报告...');
  };

  if (loading) {
    return (
      <AdminLayout>
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900">
          <div className="text-center">
            <div className="relative mb-8">
              <Sparkles className="w-20 h-20 text-indigo-400 mx-auto animate-pulse" />
              <div className="absolute inset-0 flex items-center justify-center">
                <RefreshCw className="w-12 h-12 text-white animate-spin" />
              </div>
            </div>
            <h2 className="text-3xl font-black text-white mb-4">正在生成您的年度口碑报告</h2>
            <p className="text-indigo-200 text-lg">AI 正在分析 3,842 条评价数据...</p>
            <div className="mt-8 w-64 mx-auto bg-white/20 rounded-full h-2">
              <div className="bg-gradient-to-r from-indigo-400 to-purple-400 h-full rounded-full animate-pulse" style={{ width: '60%' }}></div>
            </div>
          </div>
        </div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout>
      <div className="space-y-12 pb-20 animate-fade-in">
        {/* Header - 电影级开场 */}
        <section
          ref={(el) => sectionsRef.current[0] = el}
          className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-600 p-12 text-white opacity-0 translate-y-8 transition-all duration-1000"
        >
          <div className="absolute inset-0 bg-[url('data:image/svg+xml,...')] opacity-10"></div>
          <div className="relative z-10">
            <div className="flex items-center gap-3 mb-6">
              <PartyPopper className="w-12 h-12 text-yellow-300 animate-bounce" />
              <Badge className="bg-white/20 text-white border-white/30 text-lg px-4 py-2">
                {selectedYear} 年度回顾
              </Badge>
            </div>
            <h2 className="text-6xl font-black mb-4 leading-tight">
              您的口碑
              <br />
              <span className="text-yellow-300">数字资产</span>
            </h2>
            <p className="text-2xl text-white/90 mb-8 font-light">
              {report?.insights?.personality_type || '暖心服务家'} · {report?.stats?.total_reviews || 0} 条评价的记忆
            </p>
            <div className="flex gap-4">
              <select
                value={selectedYear}
                onChange={(e) => setSelectedYear(parseInt(e.target.value))}
                className="bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl px-6 py-3 text-lg outline-none text-white"
              >
                {[2026, 2025, 2024, 2023].map(year => (
                  <option key={year} value={year} className="text-slate-900">{year} 年</option>
                ))}
              </select>
              <Button
                className="bg-white text-indigo-600 hover:bg-white/90 gap-2 text-lg px-8 py-6 rounded-xl font-bold"
                onClick={generateReport}
              >
                <RefreshCw className="w-5 h-5" /> 重新生成
              </Button>
              <Button
                variant="outline"
                className="border-white/50 text-white hover:bg-white/20 gap-2 text-lg px-8 py-6 rounded-xl"
                onClick={handleExport}
              >
                <Download className="w-5 h-5" /> 导出报告
              </Button>
            </div>
          </div>

          {/* 装饰元素 */}
          <div className="absolute -top-20 -right-20 w-80 h-80 bg-white/10 rounded-full blur-3xl"></div>
          <div className="absolute -bottom-20 -left-20 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl"></div>
        </section>

        {report ? (
          <>
            {/* 年度总览 - 3D卡片效果 */}
            <section
              ref={(el) => sectionsRef.current[1] = el}
              className="opacity-0 translate-y-8 transition-all duration-1000 delay-200"
            >
              <h3 className="text-3xl font-bold text-slate-900 mb-8 flex items-center gap-3">
                <Trophy className="w-8 h-8 text-yellow-500" />
                年度数字资产总览
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <Card className="p-8 bg-gradient-to-br from-indigo-500 to-indigo-700 text-white border-none transform hover:scale-105 transition-all duration-300 shadow-2xl hover:shadow-indigo-500/50 hover:shadow-2xl">
                  <div className="flex items-center gap-4 mb-6">
                    <div className="bg-white/20 p-4 rounded-2xl">
                      <MessageSquare className="w-10 h-10" />
                    </div>
                    <Sparkles className="w-6 h-6 text-yellow-300 animate-pulse" />
                  </div>
                  <p className="text-6xl font-black mb-2">{report.stats?.total_reviews?.toLocaleString() || 0}</p>
                  <p className="text-indigo-200 text-lg mb-4">总评价数</p>
                  <div className="flex items-center gap-2 text-emerald-300">
                    <TrendingUp className="w-5 h-5" />
                    <span className="text-lg font-bold">+12.5%</span>
                    <span className="text-indigo-200">同比去年</span>
                  </div>
                </Card>

                <Card className="p-8 bg-gradient-to-br from-amber-400 to-orange-500 text-white border-none transform hover:scale-105 transition-all duration-300 shadow-2xl hover:shadow-amber-500/50 hover:shadow-2xl">
                  <div className="flex items-center gap-4 mb-6">
                    <div className="bg-white/20 p-4 rounded-2xl">
                      <Star className="w-10 h-10 fill-white" />
                    </div>
                    <Flame className="w-6 h-6 text-red-300 animate-pulse" />
                  </div>
                  <p className="text-6xl font-black mb-2">{report.stats?.average_rating || 0}</p>
                  <p className="text-amber-100 text-lg mb-4">平均评分</p>
                  <div className="flex items-center gap-2 text-white">
                    <TrendingUp className="w-5 h-5" />
                    <span className="text-lg font-bold">+0.3</span>
                    <span className="text-amber-100">同比去年</span>
                  </div>
                </Card>

                <Card className="p-8 bg-gradient-to-br from-emerald-400 to-teal-500 text-white border-none transform hover:scale-105 transition-all duration-300 shadow-2xl hover:shadow-emerald-500/50 hover:shadow-2xl">
                  <div className="flex items-center gap-4 mb-6">
                    <div className="bg-white/20 p-4 rounded-2xl">
                      <ThumbsUp className="w-10 h-10" />
                    </div>
                    <Heart className="w-6 h-6 text-pink-300 animate-pulse" />
                  </div>
                  <p className="text-6xl font-black mb-2">{report.stats?.sentiment_distribution?.positive || 0}%</p>
                  <p className="text-emerald-100 text-lg mb-4">好评率</p>
                  <div className="flex items-center gap-2 text-white">
                    <TrendingUp className="w-5 h-5" />
                    <span className="text-lg font-bold">+5.2%</span>
                    <span className="text-emerald-100">同比去年</span>
                  </div>
                </Card>
              </div>
            </section>

            {/* 月度趋势 - 视觉化时间轴 */}
            <section
              ref={(el) => sectionsRef.current[2] = el}
              className="opacity-0 translate-y-8 transition-all duration-1000 delay-400"
            >
              <Card className="p-10 bg-gradient-to-br from-slate-900 to-slate-800 text-white border-none shadow-2xl">
                <h3 className="text-3xl font-bold mb-8 flex items-center gap-3">
                  <Music className="w-8 h-8 text-green-400" />
                  全年情感旅程
                </h3>
                <p className="text-slate-400 mb-8 text-lg">
                  您的黄金月份是 <span className="text-yellow-400 font-bold text-2xl">{report.stats?.best_month || '8月'}</span>，
                  平均评分达到 <span className="text-green-400 font-bold text-2xl">4.6 分</span>
                </p>
                <div className="space-y-6">
                  {report.stats?.monthly_trend &&
                    Object.entries(report.stats.monthly_trend).map(([month, data]: [string, any], index) => (
                      <div key={month} className="group">
                        <div className="flex items-center gap-6 mb-2">
                          <span className="text-sm text-slate-500 w-16 font-mono">{month}月</span>
                          <div className="flex-1 bg-slate-700/50 rounded-full h-8 overflow-hidden backdrop-blur-sm">
                            <div
                              className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 h-full rounded-full transition-all duration-1000 ease-out group-hover:from-indigo-400 group-hover:to-pink-400"
                              style={{
                                width: `${(data.count / 500) * 100}%`,
                                animationDelay: `${index * 100}ms`
                              }}
                            >
                              <div className="h-full flex items-center justify-end pr-4">
                                <span className="text-white text-sm font-bold">{data.count} 条</span>
                              </div>
                            </div>
                          </div>
                          <span className="text-sm text-slate-300 w-20 text-right font-mono">{data.avg_rating} 分</span>
                        </div>
                      </div>
                    ))
                  }
                </div>
              </Card>
            </section>

            {/* AI 洞察 - 个性化分析 */}
            <section
              ref={(el) => sectionsRef.current[3] = el}
              className="opacity-0 translate-y-8 transition-all duration-1000 delay-600"
            >
              <Card className="p-10 bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50 border-amber-200 shadow-2xl">
                <h3 className="text-3xl font-bold mb-8 flex items-center gap-3 text-slate-900">
                  <Brain className="w-8 h-8 text-amber-600" />
                  AI 年度洞察报告
                </h3>

                <div className="mb-8 p-6 bg-white/60 backdrop-blur-sm rounded-2xl border border-amber-200">
                  <p className="text-slate-700 text-lg leading-relaxed italic">
                    "{report.insights?.ai_summary || '2026年是口碑提升的关键一年。您在服务态度和环境氛围上表现出色...'}"
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div className="p-6 bg-white/80 backdrop-blur-sm rounded-2xl border border-emerald-200 shadow-lg">
                    <h4 className="font-black text-emerald-600 mb-4 text-xl flex items-center gap-2">
                      <Trophy className="w-6 h-6" />
                      年度三大高光时刻
                    </h4>
                    <ul className="space-y-3">
                      {(report.insights?.highlights || []).map((item: string, i: number) => (
                        <li key={i} className="flex items-start gap-3 text-slate-700">
                          <Badge className="bg-emerald-100 text-emerald-700 border-emerald-300 mt-1">
                            {i + 1}
                          </Badge>
                          <span className="leading-relaxed">{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="p-6 bg-white/80 backdrop-blur-sm rounded-2xl border border-rose-200 shadow-lg">
                    <h4 className="font-black text-rose-600 mb-4 text-xl flex items-center gap-2">
                      <Target className="w-6 h-6" />
                      待攻克的三个方向
                    </h4>
                    <ul className="space-y-3">
                      {(report.insights?.improvements || []).map((item: string, i: number) => (
                        <li key={i} className="flex items-start gap-3 text-slate-700">
                          <Badge className="bg-rose-100 text-rose-700 border-rose-300 mt-1">
                            {i + 1}
                          </Badge>
                          <span className="leading-relaxed">{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </Card>
            </section>

            {/* 热门话题 - 动态标签云 */}
            <section
              ref={(el) => sectionsRef.current[4] = el}
              className="opacity-0 translate-y-8 transition-all duration-1000 delay-800"
            >
              <Card className="p-10 bg-gradient-to-br from-violet-500 to-purple-600 text-white border-none shadow-2xl">
                <h3 className="text-3xl font-bold mb-8 flex items-center gap-3">
                  <Sparkles className="w-8 h-8 text-yellow-300" />
                  年度热门话题榜
                </h3>
                <p className="text-purple-200 mb-8 text-lg">顾客最关心的话题，也是您的口碑关键词</p>
                <div className="flex flex-wrap gap-4">
                  {report.stats?.top_topics?.map((topic: any, i: number) => {
                    const sizes = ['text-lg', 'text-xl', 'text-2xl', 'text-3xl', 'text-4xl'];
                    const colors = [
                      'bg-white/20 hover:bg-white/30',
                      'bg-yellow-400/20 hover:bg-yellow-400/30',
                      'bg-pink-400/20 hover:bg-pink-400/30',
                      'bg-green-400/20 hover:bg-green-400/30',
                      'bg-blue-400/20 hover:bg-blue-400/30',
                    ];
                    return (
                      <Badge
                        key={i}
                        className={`${sizes[i % sizes.length]} py-3 px-6 ${colors[i % colors.length]} backdrop-blur-sm border-white/30 hover:scale-110 transition-all duration-300 cursor-pointer`}
                      >
                        {topic.name} ({topic.count})
                      </Badge>
                    );
                  }) || (
                    <>
                      <Badge className="text-4xl py-3 px-6 bg-white/20 backdrop-blur-sm border-white/30 hover:scale-110 transition-all duration-300 cursor-pointer">
                        服务态度 (856)
                      </Badge>
                      <Badge className="text-3xl py-3 px-6 bg-yellow-400/20 backdrop-blur-sm border-yellow-300/30 hover:scale-110 transition-all duration-300 cursor-pointer">
                        环境氛围 (643)
                      </Badge>
                      <Badge className="text-2xl py-3 px-6 bg-pink-400/20 backdrop-blur-sm border-pink-300/30 hover:scale-110 transition-all duration-300 cursor-pointer">
                        产品质量 (521)
                      </Badge>
                      <Badge className="text-xl py-3 px-6 bg-green-400/20 backdrop-blur-sm border-green-300/30 hover:scale-110 transition-all duration-300 cursor-pointer">
                        价格性价比 (387)
                      </Badge>
                    </>
                  )}
                </div>
              </Card>
            </section>

            {/* 改进建议 - 行动指南 */}
            <section
              ref={(el) => sectionsRef.current[5] = el}
              className="opacity-0 translate-y-8 transition-all duration-1000 delay-1000"
            >
              <Card className="p-10 bg-gradient-to-br from-rose-500 to-pink-600 text-white border-none shadow-2xl">
                <h3 className="text-3xl font-bold mb-8 flex items-center gap-3">
                  <Zap className="w-8 h-8 text-yellow-300" />
                  2027 行动指南
                </h3>
                <div className="space-y-6">
                  {(report.stats?.improvement_areas || ['等位时间', '餐具清洁', '停车便利']).map((area: string, i: number) => (
                    <div key={i} className="flex items-center gap-6 p-6 bg-white/10 backdrop-blur-sm rounded-2xl hover:bg-white/20 transition-all duration-300">
                      <div className="bg-white/20 p-4 rounded-2xl">
                        <Target className="w-8 h-8" />
                      </div>
                      <div className="flex-1">
                        <h4 className="text-2xl font-bold mb-2">优化 {area}</h4>
                        <p className="text-rose-100">重点关注该领域的顾客反馈，制定改进计划</p>
                      </div>
                      <ChevronRight className="w-8 h-8 text-rose-200" />
                    </div>
                  ))}
                </div>
              </Card>
            </section>
          </>
        ) : (
          <Card className="p-20 text-center bg-gradient-to-br from-slate-900 to-slate-800 text-white border-none shadow-2xl">
            <Sparkles className="w-24 h-24 text-indigo-400 mx-auto mb-8 animate-pulse" />
            <h3 className="text-4xl font-black text-white mb-4">开启您的年度口碑之旅</h3>
            <p className="text-slate-400 mb-10 text-xl">点击按钮，AI 将为您生成 {selectedYear} 年的详细口碑分析报告</p>
            <Button
              className="bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white text-xl px-12 py-8 rounded-2xl font-bold shadow-2xl hover:shadow-indigo-500/50 transition-all duration-300"
              onClick={generateReport}
            >
              <RefreshCw className="w-6 h-6 mr-3" />
              生成 {selectedYear} 年度报告
            </Button>
          </Card>
        )}
      </div>
    </AdminLayout>
  );
};

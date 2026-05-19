import React, { useState, useEffect } from 'react';
import {
  ArrowLeft,
  Sparkles,
  Brain,
  TrendingUp,
  MessageSquare,
  Star,
  ThumbsUp,
  ThumbsDown,
  BarChart3,
  Target,
  Lightbulb,
  Download,
  RefreshCw,
  CheckCircle2,
  AlertCircle,
  Zap,
  Filter
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { Button } from '../../components/ui/button';
import { AdminLayout } from '../../components/AdminLayout';
import { useToast } from '../../hooks/use-toast';
import { useNavigate } from 'react-router-dom';

interface XiaohongshuPost {
  id: string;
  post_id: string;
  title: string;
  content: string;
  author: string;
  likes: number;
  comments: number;
  shares: number;
  sentiment: 'positive' | 'negative' | 'neutral';
  tags: string[];
  store_mention?: string;
  collected_at: string;
}

interface StoreThreeGoodThreeBad {
  store_id: number;
  store_name: string;
  goods: Array<{ item: string; score: number; count: number }>;
  bads: Array<{ item: string; score: number; count: number }>;
  overall_rating: number;
  total_reviews: number;
}

export const XiaohongshuAnalysis: React.FC = () => {
  const [posts, setPosts] = useState<XiaohongshuPost[]>([]);
  const [storeData, setStoreData] = useState<StoreThreeGoodThreeBad[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'collect' | 'analyze' | 'three-good-bad'>('collect');
  const [selectedStore, setSelectedStore] = useState<number>(1);
  const { success, error } = useToast();
  const navigate = useNavigate();

  useEffect(() => {
    fetchData();
  }, [selectedStore]);

  const fetchData = async () => {
    setLoading(true);
    // 模拟数据
    setTimeout(() => {
      setPosts(getMockPosts());
      setStoreData(getMockStoreData());
      setLoading(false);
    }, 1000);
  };

  const getMockPosts = (): XiaohongshuPost[] => {
    return [
      {
        id: '1',
        post_id: 'post_001',
        title: '宝藏餐厅推荐！服务超赞',
        content: '今天去了这家店，服务态度特别好，菜品也很新鲜...',
        author: '美食探店家',
        likes: 128,
        comments: 32,
        shares: 15,
        sentiment: 'positive',
        tags: ['美食推荐', '服务好评', '环境优美'],
        store_mention: '王府井总店',
        collected_at: '2026-05-14T10:30:00',
      },
      {
        id: '2',
        post_id: 'post_002',
        title: '排队太久了对吧？',
        content: '等了快一个小时才上菜，体验不太好...',
        author: '吃货小分队',
        likes: 56,
        comments: 18,
        shares: 5,
        sentiment: 'negative',
        tags: ['等位时间', '服务吐槽'],
        store_mention: '三里屯店',
        collected_at: '2026-05-13T18:20:00',
      },
      {
        id: '3',
        post_id: 'post_003',
        title: '环境超好！拍照圣地',
        content: '装修风格很有特色，适合拍照打卡...',
        author: '生活美学家',
        likes: 256,
        comments: 45,
        shares: 38,
        sentiment: 'positive',
        tags: ['环境氛围', '拍照打卡', '网红餐厅'],
        store_mention: '天河城店',
        collected_at: '2026-05-12T14:15:00',
      },
    ];
  };

  const getMockStoreData = (): StoreThreeGoodThreeBad[] => {
    return [
      {
        store_id: 1,
        store_name: '王府井总店',
        goods: [
          { item: '服务态度', score: 4.9, count: 856 },
          { item: '食材新鲜度', score: 4.8, count: 742 },
          { item: '装修风格', score: 4.7, count: 635 },
        ],
        bads: [
          { item: '等位时间', score: 3.2, count: 128 },
          { item: '包间私密性', score: 3.5, count: 86 },
          { item: '空调温度控制', score: 3.4, count: 92 },
        ],
        overall_rating: 4.5,
        total_reviews: 2845,
      },
      {
        store_id: 2,
        store_name: '三里屯店',
        goods: [
          { item: '菜品口味', score: 4.8, count: 720 },
          { item: '上菜速度', score: 4.6, count: 680 },
          { item: '性价比', score: 4.5, count: 590 },
        ],
        bads: [
          { item: '停车便利性', score: 3.0, count: 95 },
          { item: '周边环境', score: 3.3, count: 78 },
          { item: '高峰期排队', score: 3.1, count: 102 },
        ],
        overall_rating: 4.3,
        total_reviews: 1920,
      },
    ];
  };

  const handleCollectData = () => {
    success('开始采集', '正在从小红书采集数据...');
    setLoading(true);
    setTimeout(() => {
      setPosts(getMockPosts());
      setLoading(false);
      success('采集完成', '成功采集 3 条小红书种草数据');
    }, 2000);
  };

  const handleAIAnalyze = () => {
    success('AI分析中', 'AI 正在分析小红书数据...');
    setTimeout(() => {
      success('分析完成', '已生成 AI 洞察报告，请查看分析标签页');
      setActiveTab('analyze');
    }, 2500);
  };

  const handleExportReport = () => {
    success('导出报告', '正在生成小红书数据分析报告...');
  };

  const handleBack = () => {
    navigate('/admin/dashboard');
  };

  return (
    <AdminLayout>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={handleBack}>
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <div>
              <h2 className="text-2xl font-bold text-slate-900">小红书数据采集与AI分析</h2>
              <p className="text-slate-500 mt-1">外部种草数据采集、录入与智能分析</p>
            </div>
          </div>
          <div className="flex gap-3">
            <Button variant="outline" className="gap-2" onClick={handleExportReport}>
              <Download className="w-4 h-4" /> 导出报告
            </Button>
            <Button
              className="bg-gradient-to-r from-red-500 to-pink-600 hover:from-red-600 hover:to-pink-700 text-white gap-2"
              onClick={handleCollectData}
            >
              <Sparkles className="w-4 h-4" /> 采集数据
            </Button>
          </div>
        </div>

        {/* Tab Switcher */}
        <div className="flex bg-white p-1 rounded-2xl shadow-sm border border-slate-100 w-fit">
          <button
            onClick={() => setActiveTab('collect')}
            className={`px-6 py-2 rounded-xl text-sm font-bold transition-all ${
              activeTab === 'collect'
                ? 'bg-red-500 text-white shadow-md shadow-red-100'
                : 'text-slate-500 hover:text-slate-700'
            }`}
          >
            <Sparkles className="w-4 h-4 inline mr-2" /> 数据采集
          </button>
          <button
            onClick={() => setActiveTab('analyze')}
            className={`px-6 py-2 rounded-xl text-sm font-bold transition-all ${
              activeTab === 'analyze'
                ? 'bg-red-500 text-white shadow-md shadow-red-100'
                : 'text-slate-500 hover:text-slate-700'
            }`}
          >
            <BarChart3 className="w-4 h-4 inline mr-2" /> AI分析
          </button>
          <button
            onClick={() => setActiveTab('three-good-bad')}
            className={`px-6 py-2 rounded-xl text-sm font-bold transition-all ${
              activeTab === 'three-good-bad'
                ? 'bg-red-500 text-white shadow-md shadow-red-100'
                : 'text-slate-500 hover:text-slate-700'
            }`}
          >
            <Target className="w-4 h-4 inline mr-2" /> 三好三差
          </button>
        </div>

        {loading ? (
          <Card className="p-12 text-center">
            <RefreshCw className="w-12 h-12 text-red-500 animate-spin mx-auto mb-4" />
            <p className="text-slate-500">正在加载数据...</p>
          </Card>
        ) : (
          <>
            {/* 数据采集 Tab */}
            {activeTab === 'collect' && (
              <div className="space-y-6">
                {/* 采集控制面板 */}
                <Card className="p-6 bg-gradient-to-br from-red-50 to-pink-50 border-red-200">
                  <div className="flex items-center gap-4 mb-6">
                    <div className="bg-red-500 p-3 rounded-2xl">
                      <Sparkles className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-900">小红书数据采集</h3>
                      <p className="text-sm text-slate-500">采集外部种草数据，录入系统进行AI分析</p>
                    </div>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-white p-4 rounded-xl border border-slate-200">
                      <p className="text-sm text-slate-500 mb-1">采集状态</p>
                      <Badge className="bg-emerald-100 text-emerald-700">就绪</Badge>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200">
                      <p className="text-sm text-slate-500 mb-1">已采集数据</p>
                      <p className="text-2xl font-black text-slate-900">{posts.length} 条</p>
                    </div>
                    <div className="bg-white p-4 rounded-xl border border-slate-200">
                      <p className="text-sm text-slate-500 mb-1">关联门店</p>
                      <p className="text-2xl font-black text-slate-900">{storeData.length} 家</p>
                    </div>
                  </div>
                </Card>

                {/* 采集到的数据列表 */}
                <div className="space-y-4">
                  <h3 className="text-xl font-bold text-slate-900">采集数据列表</h3>
                  {posts.map((post) => (
                    <Card key={post.id} className="p-6 hover:shadow-lg transition-all duration-300">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex-1">
                          <h4 className="font-bold text-slate-900 mb-2">{post.title}</h4>
                          <p className="text-sm text-slate-600 mb-3">{post.content}</p>
                          <div className="flex items-center gap-4 text-sm text-slate-500">
                            <span className="flex items-center gap-1">
                              <ThumbsUp className="w-4 h-4" /> {post.likes}
                            </span>
                            <span className="flex items-center gap-1">
                              <MessageSquare className="w-4 h-4" /> {post.comments}
                            </span>
                            <span className="flex items-center gap-1">
                              <Sparkles className="w-4 h-4" /> {post.shares}
                            </span>
                          </div>
                        </div>
                        <Badge
                          className={
                            post.sentiment === 'positive'
                              ? 'bg-emerald-100 text-emerald-700'
                              : post.sentiment === 'negative'
                              ? 'bg-rose-100 text-rose-700'
                              : 'bg-slate-100 text-slate-500'
                          }
                        >
                          {post.sentiment === 'positive' ? '正面' : post.sentiment === 'negative' ? '负面' : '中性'}
                        </Badge>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {post.tags.map((tag, i) => (
                          <Badge key={i} variant="outline" className="text-xs">
                            #{tag}
                          </Badge>
                        ))}
                      </div>
                      {post.store_mention && (
                        <div className="mt-3 pt-3 border-t border-slate-100">
                          <p className="text-sm text-slate-500">
                            关联门店：<span className="font-bold text-slate-700">{post.store_mention}</span>
                          </p>
                        </div>
                      )}
                    </Card>
                  ))}
                </div>
              </div>
            )}

            {/* AI分析 Tab */}
            {activeTab === 'analyze' && (
              <div className="space-y-6">
                <Card className="p-6 bg-gradient-to-br from-indigo-50 to-purple-50 border-indigo-200">
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-4">
                      <div className="bg-indigo-500 p-3 rounded-2xl">
                        <Brain className="w-6 h-6 text-white" />
                      </div>
                      <div>
                        <h3 className="font-bold text-slate-900">AI 智能分析</h3>
                        <p className="text-sm text-slate-500">基于采集的小红书数据进行AI分析</p>
                      </div>
                    </div>
                    <Button
                      className="bg-indigo-600 hover:bg-indigo-700 text-white gap-2"
                      onClick={handleAIAnalyze}
                    >
                      <Zap className="w-4 h-4" /> 启动AI分析
                    </Button>
                  </div>

                  {/* AI洞察结果 */}
                  <div className="space-y-6">
                    <div>
                      <h4 className="font-bold text-emerald-600 mb-3">✅ 正面洞察</h4>
                      <Card className="p-4 bg-white">
                        <ul className="space-y-2 text-sm text-slate-700">
                          <li className="flex items-start gap-2">
                            <CheckCircle2 className="w-4 h-4 text-emerald-500 mt-0.5" />
                            "服务态度"获得最多好评，共 856 条相关提及
                          </li>
                          <li className="flex items-start gap-2">
                            <CheckCircle2 className="w-4 h-4 text-emerald-500 mt-0.5" />
                            "环境氛围"是小红书用户最关注的亮点
                          </li>
                          <li className="flex items-start gap-2">
                            <CheckCircle2 className="w-4 h-4 text-emerald-500 mt-0.5" />
                            拍照打卡类笔记平均获得 2.5 倍互动量
                          </li>
                        </ul>
                      </Card>
                    </div>

                    <div>
                      <h4 className="font-bold text-rose-600 mb-3">⚠️ 负面预警</h4>
                      <Card className="p-4 bg-white">
                        <ul className="space-y-2 text-sm text-slate-700">
                          <li className="flex items-start gap-2">
                            <AlertCircle className="w-4 h-4 text-rose-500 mt-0.5" />
                            "等位时间"相关负面提及占比 23%
                          </li>
                          <li className="flex items-start gap-2">
                            <AlertCircle className="w-4 h-4 text-rose-500 mt-0.5" />
                            "停车不便"是影响到店转化的重要因素
                          </li>
                        </ul>
                      </Card>
                    </div>

                    <div>
                      <h4 className="font-bold text-indigo-600 mb-3">📊 数据趋势</h4>
                      <Card className="p-4 bg-white">
                        <div className="space-y-3">
                          <div>
                            <div className="flex justify-between text-sm mb-1">
                              <span className="text-slate-600">正面情感</span>
                              <span className="font-bold text-emerald-600">76.5%</span>
                            </div>
                            <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                              <div className="bg-emerald-500 h-full rounded-full" style={{ width: '76.5%' }}></div>
                            </div>
                          </div>
                          <div>
                            <div className="flex justify-between text-sm mb-1">
                              <span className="text-slate-600">负面情感</span>
                              <span className="font-bold text-rose-600">12.3%</span>
                            </div>
                            <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                              <div className="bg-rose-500 h-full rounded-full" style={{ width: '12.3%' }}></div>
                            </div>
                          </div>
                          <div>
                            <div className="flex justify-between text-sm mb-1">
                              <span className="text-slate-600">中性情感</span>
                              <span className="font-bold text-slate-600">11.2%</span>
                            </div>
                            <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                              <div className="bg-slate-400 h-full rounded-full" style={{ width: '11.2%' }}></div>
                            </div>
                          </div>
                        </div>
                      </Card>
                    </div>
                  </div>
                </Card>
              </div>
            )}

            {/* 三好三差 Tab */}
            {activeTab === 'three-good-bad' && (
              <div className="space-y-6">
                {/* 门店选择器 */}
                <div className="flex items-center gap-4">
                  <label className="text-sm font-medium text-slate-700">选择门店：</label>
                  <select
                    value={selectedStore}
                    onChange={(e) => setSelectedStore(parseInt(e.target.value))}
                    className="bg-white border border-slate-200 rounded-lg px-4 py-2 text-sm outline-none"
                  >
                    {storeData.map((store) => (
                      <option key={store.store_id} value={store.store_id}>
                        {store.store_name}
                      </option>
                    ))}
                  </select>
                </div>

                {storeData
                  .filter((store) => store.store_id === selectedStore)
                  .map((store) => (
                    <div key={store.store_id} className="space-y-6">
                      {/* 门店总览 */}
                      <Card className="p-6 bg-gradient-to-br from-amber-50 to-orange-50 border-amber-200">
                        <h3 className="text-xl font-bold text-slate-900 mb-4">{store.store_name} - 三好三差分析</h3>
                        <div className="grid grid-cols-2 gap-4">
                          <div className="bg-white p-4 rounded-xl">
                            <p className="text-sm text-slate-500 mb-1">总体评分</p>
                            <p className="text-3xl font-black text-amber-600">{store.overall_rating}</p>
                          </div>
                          <div className="bg-white p-4 rounded-xl">
                            <p className="text-sm text-slate-500 mb-1">总评价数</p>
                            <p className="text-3xl font-black text-slate-900">{store.total_reviews.toLocaleString()}</p>
                          </div>
                        </div>
                      </Card>

                      {/* 三好 */}
                      <Card className="p-6">
                        <h4 className="font-bold text-emerald-600 mb-4 flex items-center gap-2">
                          <ThumbsUp className="w-5 h-5" /> 表现优异 (三好)
                        </h4>
                        <div className="space-y-4">
                          {store.goods.map((item, i) => (
                            <div key={i} className="bg-emerald-50 p-4 rounded-xl">
                              <div className="flex items-center justify-between mb-2">
                                <span className="font-bold text-slate-900">{item.item}</span>
                                <Badge className="bg-emerald-100 text-emerald-700">
                                  评分: {item.score}
                                </Badge>
                              </div>
                              <div className="flex items-center gap-2 text-sm text-slate-600">
                                <MessageSquare className="w-4 h-4" />
                                <span>提及次数: {item.count}</span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </Card>

                      {/* 三差 */}
                      <Card className="p-6">
                        <h4 className="font-bold text-rose-600 mb-4 flex items-center gap-2">
                          <ThumbsDown className="w-5 h-5" /> 急需改进 (三差)
                        </h4>
                        <div className="space-y-4">
                          {store.bads.map((item, i) => (
                            <div key={i} className="bg-rose-50 p-4 rounded-xl">
                              <div className="flex items-center justify-between mb-2">
                                <span className="font-bold text-slate-900">{item.item}</span>
                                <Badge className="bg-rose-100 text-rose-700">
                                  评分: {item.score}
                                </Badge>
                              </div>
                              <div className="flex items-center gap-2 text-sm text-slate-600">
                                <MessageSquare className="w-4 h-4" />
                                <span>提及次数: {item.count}</span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </Card>
                    </div>
                  ))}
              </div>
            )}
          </>
        )}
      </div>
    </AdminLayout>
  );
};

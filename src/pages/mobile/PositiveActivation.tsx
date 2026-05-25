import React, { useState, useEffect } from 'react';
import {
  Heart,
  Star,
  Gift,
  Share2,
  TrendingUp,
  CheckCircle2,
  ChevronRight,
  Sparkles,
  Camera,
  FileText,
  Copy,
  PenTool,
  Library,
  Flame,
  Zap
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { MobileLayout } from '../../components/MobileLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';
import { useNavigate } from 'react-router-dom';
import { fetchHighQualityReviews, fetchBrandScripts } from '../../api/positive-activation';
import type { HighQualityReview, BrandScript } from '../../api/positive-activation';

export const PositiveActivation: React.FC = () => {
  const [activeView, setActiveView] = useState<'high_quality' | 'scripts' | 'content_factory'>('high_quality');
  const [copiedId, setCopiedId] = useState<number | null>(null);
  const [highQualityReviews, setHighQualityReviews] = useState<HighQualityReview[]>([]);
  const [brandScripts, setBrandScripts] = useState<BrandScript[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const fetchedRef = React.useRef(false);

  const { success } = useToast();
  const navigate = useNavigate();

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const storeId = selectedStore?.id;
      const [reviewData, scriptData] = await Promise.all([
        fetchHighQualityReviews(1, 20, storeId),
        fetchBrandScripts(storeId),
      ]);
      setHighQualityReviews(reviewData);
      setBrandScripts(scriptData);
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

  const handleCopyScript = (reviewId: number, script: string) => {
    navigator.clipboard.writeText(script);
    setCopiedId(reviewId);
    success('复制成功', '授权话术已复制到剪贴板');
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleSendAuthorization = (reviewId: number) => {
    success('授权请求已发送', '用户将收到私信通知');
  };

  const handleGenerateContent = (platform: string) => {
    success(`${platform}内容生成中`, 'AI正在根据好评生成种草内容...');
  };

  if (loading) {
    return (
      <MobileLayout title="好评激活 & 营销">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="w-12 h-12 border-4 border-orange-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-sm text-slate-400">加载中...</p>
          </div>
        </div>
      </MobileLayout>
    );
  }

  if (error) {
    return (
      <MobileLayout title="好评激活 & 营销">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <p className="text-sm text-rose-500 mb-4">{error}</p>
            <button onClick={loadData} className="text-sm text-orange-600 font-bold">重试</button>
          </div>
        </div>
      </MobileLayout>
    );
  }

  return (
    <MobileLayout title="好评激活 & 营销">
      <div className="space-y-6 pb-20 animate-in fade-in slide-in-from-bottom-4 duration-500">
        
        {/* Top Summary Card */}
        <Card className="p-6 border-slate-100 shadow-sm bg-white relative overflow-hidden">
          <Sparkles className="absolute -right-4 -top-4 w-24 h-24 text-orange-50" />
          <div className="relative z-10">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-8 h-8 rounded-lg bg-orange-50 flex items-center justify-center">
                <Sparkles className="w-4 h-4 text-orange-500" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">口碑爆发计划</h3>
            </div>
            <p className="text-slate-500 text-xs leading-relaxed mb-6">
              AI 自动识别带图、长文等高质好评，生成专属授权话术，并支持一键改写为全平台种草内容。
            </p>
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-orange-50 rounded-xl p-3 border border-orange-100">
                <p className="text-[10px] text-orange-600 uppercase font-bold">高质好评</p>
                <p className="text-lg font-black text-slate-900">{highQualityReviews.length} 条</p>
              </div>
              <div className="bg-blue-50 rounded-xl p-3 border border-blue-100">
                <p className="text-[10px] text-blue-600 uppercase font-bold">预计曝光</p>
                <p className="text-lg font-black text-slate-900">12w+</p>
              </div>
            </div>
          </div>
        </Card>

        {/* View Switcher */}
        <div className="flex bg-white p-1 rounded-2xl shadow-sm border border-slate-100 mx-1">
          <button 
            onClick={() => setActiveView('high_quality')}
            className={cn(
              "flex-1 py-2 text-[10px] font-bold rounded-xl transition-all flex flex-col items-center gap-1",
              activeView === 'high_quality' ? "bg-orange-500 text-white" : "text-slate-400"
            )}
          >
            <Star className="w-3.5 h-3.5" /> 优质好评
          </button>
          <button 
            onClick={() => setActiveView('scripts')}
            className={cn(
              "flex-1 py-2 text-[10px] font-bold rounded-xl transition-all flex flex-col items-center gap-1",
              activeView === 'scripts' ? "bg-orange-500 text-white" : "text-slate-400"
            )}
          >
            <Library className="w-3.5 h-3.5" /> 话术资产
          </button>
          <button 
            onClick={() => setActiveView('content_factory')}
            className={cn(
              "flex-1 py-2 text-[10px] font-bold rounded-xl transition-all flex flex-col items-center gap-1",
              activeView === 'content_factory' ? "bg-orange-500 text-white" : "text-slate-400"
            )}
          >
            <PenTool className="w-3.5 h-3.5" /> 内容工厂
          </button>
        </div>

        {activeView === 'high_quality' && (
          <div className="space-y-4">
            {highQualityReviews.map((review) => (
              <Card key={review.id} className="p-0 border-none shadow-sm overflow-hidden bg-white">
                <div className="p-4 border-b border-slate-50">
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex items-center gap-3">
                      <img src={review.avatar} alt={review.user} className="w-10 h-10 rounded-full object-cover" />
                      <div>
                        <h4 className="text-sm font-bold text-slate-800">{review.user}</h4>
                        <div className="flex gap-1 mt-0.5">
                          {review.hasImage && <Badge className="bg-emerald-50 text-emerald-600 border-none text-[8px] h-4"><Camera className="w-2 h-2 mr-0.5" /> 有图</Badge>}
                          <Badge className="bg-orange-50 text-orange-600 border-none text-[8px] h-4"><FileText className="w-2 h-2 mr-0.5" /> {review.length}</Badge>
                        </div>
                      </div>
                    </div>
                    <Badge variant="outline" className="text-[10px] text-slate-400">情感: {review.sentiment}</Badge>
                  </div>
                  <p className="text-xs text-slate-500 line-clamp-2 leading-relaxed italic">"{review.content}"</p>
                </div>
                <div className="p-4 bg-orange-50/30">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[10px] font-bold text-orange-600 uppercase">AI 生成授权请求话术</span>
                    <Button 
                      variant="ghost" 
                      size="icon" 
                      className="w-6 h-6 text-slate-300 hover:text-orange-500"
                      onClick={() => handleCopyScript(review.id, review.suggestedScript)}
                    >
                      {copiedId === review.id ? (
                        <CheckCircle2 className="w-3 h-3 text-emerald-500" />
                      ) : (
                        <Copy className="w-3 h-3" />
                      )}
                    </Button>
                  </div>
                  <div className="bg-white p-3 rounded-xl border border-orange-100 mb-4 text-[11px] text-slate-600 leading-relaxed shadow-sm">
                    {review.suggestedScript}
                  </div>
                  <Button 
                    className="w-full bg-orange-500 hover:bg-orange-600 text-white rounded-xl h-10 font-bold text-xs shadow-md shadow-orange-100"
                    onClick={() => handleSendAuthorization(review.id)}
                  >
                    私信用户发起授权
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        )}

        {activeView === 'scripts' && (
          <div className="space-y-4">
            <h3 className="font-bold text-slate-800 text-sm px-1">品牌专属话术库学习进度</h3>
            <div className="grid grid-cols-1 gap-3">
              {brandScripts.map((script, i) => (
                <Card key={i} className="p-4 border-none shadow-sm space-y-3 bg-white">
                  <div className="flex justify-between items-center">
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 rounded-lg bg-orange-50 flex items-center justify-center text-orange-500 font-bold text-xs">
                        {script.tag[0]}
                      </div>
                      <span className="font-bold text-slate-700 text-sm">{script.tag}风格</span>
                    </div>
                    <Badge className="bg-emerald-50 text-emerald-600 border-none text-[10px]">已同步 {script.count} 条</Badge>
                  </div>
                  <div className="space-y-1.5">
                    <div className="flex justify-between text-[10px] text-slate-400 font-bold">
                      <span>AI 模型匹配度</span>
                      <span>{script.progress}</span>
                    </div>
                    <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                      <div className="h-full bg-orange-500 rounded-full" style={{ width: script.progress }}></div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
            <Button 
              variant="outline" 
              className="w-full border-slate-200 h-12 text-xs font-bold gap-2 bg-white"
              onClick={() => success('导出成功', '品牌话术资产已导出为PDF')}
            >
              <Library className="w-4 h-4" /> 导出品牌话术资产
            </Button>
          </div>
        )}

        {activeView === 'content_factory' && (
          <div className="space-y-4 px-1">
            <Card className="p-5 border-none shadow-sm space-y-4 bg-white">
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 bg-rose-50 rounded-xl flex items-center justify-center flex-shrink-0">
                  <iconify-icon icon="simple-icons:xiaohongshu" class="text-xl text-rose-500"></iconify-icon>
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-800">生成小红书种草笔记</h4>
                  <p className="text-[11px] text-slate-500 mt-1 leading-relaxed">
                    提取好评中的关键词与情感点，自动生成带 Emoji 的小红书风格文案。
                  </p>
                </div>
              </div>
              <Button 
                className="w-full bg-rose-500 hover:bg-rose-600 text-white rounded-xl h-10 font-bold text-xs"
                onClick={() => handleGenerateContent('小红书')}
              >
                立即转换内容
              </Button>
            </Card>

            <Card className="p-5 border-none shadow-sm space-y-4 bg-white">
              <div className="flex items-start gap-4">
                <div className="w-10 h-10 bg-black rounded-xl flex items-center justify-center flex-shrink-0">
                  <iconify-icon icon="simple-icons:tiktok" class="text-xl text-white"></iconify-icon>
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-800">生成抖音口播脚本</h4>
                  <p className="text-[11px] text-slate-500 mt-1 leading-relaxed">
                    将评价改写为 15-30s 的短视频口播脚本，包含转场建议。
                  </p>
                </div>
              </div>
              <Button 
                className="w-full bg-slate-900 hover:bg-black text-white rounded-xl h-10 font-bold text-xs"
                onClick={() => handleGenerateContent('抖音')}
              >
                生成视频脚本
              </Button>
            </Card>
          </div>
        )}
      </div>
    </MobileLayout>
  );
};

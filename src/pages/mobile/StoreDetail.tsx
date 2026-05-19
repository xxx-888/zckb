import React from 'react';
import { 
  ArrowLeft,
  Store,
  Star,
  TrendingUp,
  MessageSquare,
  Activity,
  MapPin,
  Phone,
  Clock,
  CheckCircle2,
  AlertCircle,
  BarChart3,
  ThumbsUp,
  ThumbsDown
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { Button } from '../../components/ui/button';
import { MobileLayout } from '../../components/MobileLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';
import { useParams, useNavigate } from 'react-router-dom';

export const StoreDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { success } = useToast();
  const navigate = useNavigate();

  // 模拟门店详情数据
  const storeData = {
    id: parseInt(id || '1'),
    name: ['', '王府井总店', '三里屯店', '天河城店', '南京路店', '春熙路店'][parseInt(id || '1')] || '未知门店',
    score: [0, 4.9, 4.8, 4.7, 4.6, 4.5][parseInt(id || '1')] || 4.5,
    reviews: [0, 120, 85, 64, 92, 78][parseInt(id || '1')] || 0,
    health: [0, 98, 95, 88, 92, 90][parseInt(id || '1')] || 90,
    address: ['', '北京市东城区王府井大街88号', '北京市朝阳区三里屯路12号', '广州市天河区天河城购物中心3楼', '上海市黄浦区南京东路168号', '成都市锦江区春熙路88号'][parseInt(id || '1')] || '',
    phone: '010-8888-6666',
    businessHours: '11:00 - 22:00',
    platforms: ['美团', '大众点评', '抖音', '小红书'],
    monthlyStats: {
      totalReviews: 485,
      avgRating: 4.7,
      positiveRate: 94.2,
      aiReplyRate: 98.5
    },
    recentReviews: [
      { id: 1, user: '张女士', rating: 5, content: '菜品味道很不错，特别是招牌牛肉，服务也周到。', platform: '美团', time: '10分钟前' },
      { id: 2, user: '李先生', rating: 3, content: '等餐时间有点久，希望改进。', platform: '大众点评', time: '1小时前' },
      { id: 3, user: '王阿姨', rating: 2, content: '食材不新鲜，感觉不太好。', platform: '美团', time: '2小时前' },
    ],
    trend: ['', 'up', 'up', 'down', 'up', 'stable'][parseInt(id || '1')] || 'stable'
  };

  const handleBack = () => {
    navigate('/mobile/store-list');
  };

  const handleViewReviews = () => {
    success('评论流', `正在查看"${storeData.name}"的评论...`);
    navigate('/mobile/review-stream');
  };

  const handleViewAnalysis = () => {
    success('AI分析', `正在分析"${storeData.name}"的数据...`);
    navigate('/mobile/ai-analysis');
  };

  return (
    <MobileLayout title="门店详情">
      <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500 pb-20">
        
        {/* Store Header Card */}
        <Card className="p-5 border-none shadow-sm bg-white relative overflow-hidden">
          <div className="flex items-start gap-4">
            <div className="w-16 h-16 rounded-2xl bg-orange-50 flex items-center justify-center flex-shrink-0">
              <Store className="w-8 h-8 text-orange-500" />
            </div>
            <div className="flex-1">
              <h2 className="text-lg font-bold text-slate-900 mb-1">{storeData.name}</h2>
              <div className="flex items-center gap-2 mb-2">
                <div className="flex items-center gap-0.5">
                  {[1, 2, 3, 4, 5].map(star => (
                    <Star 
                      key={star} 
                      className={cn(
                        "w-4 h-4",
                        star <= Math.floor(storeData.score) ? "text-amber-400 fill-amber-400" : 
                        star === Math.ceil(storeData.score) && storeData.score % 1 !== 0 ? "text-amber-400 fill-amber-400/50" : 
                        "text-slate-200"
                      )} 
                    />
                  ))}
                </div>
                <span className="text-sm font-bold text-slate-700">{storeData.score}</span>
              </div>
              <div className="flex items-center gap-1 text-[10px] text-slate-400">
                <MapPin className="w-3 h-3" />
                <span>{storeData.address}</span>
              </div>
            </div>
          </div>

          {/* Health Score Badge */}
          <div className={cn(
            "absolute top-4 right-4 px-3 py-1.5 rounded-2xl text-sm font-bold",
            storeData.health >= 95 ? "bg-emerald-50 text-emerald-600" :
            storeData.health >= 90 ? "bg-orange-50 text-orange-600" :
            "bg-rose-50 text-rose-600"
          )}>
            健康值 {storeData.health}
          </div>
        </Card>

        {/* Contact Info */}
        <Card className="p-4 border-none shadow-sm bg-white">
          <div className="space-y-3">
            <div className="flex items-center gap-3">
              <Phone className="w-4 h-4 text-slate-400" />
              <span className="text-sm text-slate-600">{storeData.phone}</span>
            </div>
            <div className="flex items-center gap-3">
              <Clock className="w-4 h-4 text-slate-400" />
              <span className="text-sm text-slate-600">{storeData.businessHours}</span>
            </div>
            <div className="flex items-center gap-3">
              <Activity className="w-4 h-4 text-slate-400" />
              <div className="flex gap-1.5">
                {storeData.platforms.map((platform, i) => (
                  <Badge key={i} variant="outline" className="text-[9px] border-slate-100 bg-slate-50 text-slate-500 px-1.5 h-4">
                    {platform}
                  </Badge>
                ))}
              </div>
            </div>
          </div>
        </Card>

        {/* Monthly Stats */}
        <Card className="p-5 border-none shadow-sm bg-white">
          <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2 mb-4">
            <BarChart3 className="w-4 h-4 text-orange-500" />
            本月数据概览
          </h3>
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-slate-50 rounded-2xl p-3">
              <div className="flex items-center gap-1.5 mb-1">
                <MessageSquare className="w-3.5 h-3.5 text-orange-500" />
                <span className="text-[10px] text-slate-400">评论总数</span>
              </div>
              <div className="text-xl font-bold text-slate-900">{storeData.monthlyStats.totalReviews}</div>
            </div>
            <div className="bg-slate-50 rounded-2xl p-3">
              <div className="flex items-center gap-1.5 mb-1">
                <Star className="w-3.5 h-3.5 text-amber-500" />
                <span className="text-[10px] text-slate-400">平均星级</span>
              </div>
              <div className="text-xl font-bold text-slate-900">{storeData.monthlyStats.avgRating}</div>
            </div>
            <div className="bg-emerald-50 rounded-2xl p-3">
              <div className="flex items-center gap-1.5 mb-1">
                <ThumbsUp className="w-3.5 h-3.5 text-emerald-500" />
                <span className="text-[10px] text-emerald-600">好评率</span>
              </div>
              <div className="text-xl font-bold text-emerald-600">{storeData.monthlyStats.positiveRate}%</div>
            </div>
            <div className="bg-blue-50 rounded-2xl p-3">
              <div className="flex items-center gap-1.5 mb-1">
                <Activity className="w-3.5 h-3.5 text-blue-500" />
                <span className="text-[10px] text-blue-600">AI回复率</span>
              </div>
              <div className="text-xl font-bold text-blue-600">{storeData.monthlyStats.aiReplyRate}%</div>
            </div>
          </div>
        </Card>

        {/* Action Buttons */}
        <div className="grid grid-cols-2 gap-3">
          <Button 
            className="h-12 bg-orange-500 hover:bg-orange-600 text-white rounded-2xl font-bold"
            onClick={handleViewReviews}
          >
            <MessageSquare className="w-4 h-4 mr-1.5" />
            查看评论
          </Button>
          <Button 
            className="h-12 bg-blue-500 hover:bg-blue-600 text-white rounded-2xl font-bold"
            onClick={handleViewAnalysis}
          >
            <BarChart3 className="w-4 h-4 mr-1.5" />
            AI分析
          </Button>
        </div>

        {/* Recent Reviews */}
        <div className="space-y-3">
          <div className="flex items-center justify-between px-1">
            <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
              <MessageSquare className="w-4 h-4 text-orange-500" />
              最近评论
            </h3>
            <span className="text-[10px] text-slate-400">{storeData.recentReviews.length} 条</span>
          </div>
          {storeData.recentReviews.map((review) => (
            <Card key={review.id} className="p-4 border-none shadow-sm bg-white">
              <div className="flex gap-3">
                <div className={cn(
                  "w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold text-white flex-shrink-0",
                  review.rating >= 4 ? "bg-emerald-400" : review.rating >= 3 ? "bg-amber-400" : "bg-rose-400"
                )}>
                  {review.rating}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-sm font-bold text-slate-800">{review.user}</span>
                    <span className="text-[10px] text-slate-400">{review.time}</span>
                  </div>
                  <p className="text-xs text-slate-500 line-clamp-2">{review.content}</p>
                  <Badge variant="outline" className="text-[9px] border-slate-100 bg-slate-50 text-slate-500 px-1.5 h-4 mt-2">
                    {review.platform}
                  </Badge>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </MobileLayout>
  );
};

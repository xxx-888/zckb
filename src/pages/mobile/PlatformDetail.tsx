import React, { useState, useEffect } from 'react';
import { ArrowLeft, TrendingUp, MessageSquare, Star, ThumbsUp, Filter } from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { Button } from '../../components/ui/button';
import { MobileLayout } from '../../components/MobileLayout';
import { useToast } from '../../hooks/use-toast';
import { useNavigate, useParams } from 'react-router-dom';

interface Review {
  id: number;
  user: string;
  content: string;
  rating: number;
  platform: string;
  time: string;
  sentiment: 'positive' | 'negative' | 'neutral';
}

export const PlatformDetail: React.FC = () => {
  const { platform } = useParams<{ platform: string }>();
  const [reviews, setReviews] = useState<Review[]>([]);
  const [timePeriod, setTimePeriod] = useState<'today' | '7days' | '30days'>('7days');
  const { success } = useToast();
  const navigate = useNavigate();

  useEffect(() => {
    // 模拟数据 - 根据平台不同显示不同数据
    const mockReviews = [
      { id: 1, user: '张女士', content: '菜品味道很不错，特别是招牌牛肉，服务也周到。', rating: 5, platform: platform || '美团', time: '10分钟前', sentiment: 'positive' as const },
      { id: 2, user: '李先生', content: '等餐时间有点久，希望改进。', rating: 3, platform: platform || '大众点评', time: '1小时前', sentiment: 'neutral' as const },
      { id: 3, user: '王阿姨', content: '食材不新鲜，感觉不太好。', rating: 2, platform: platform || '抖音', time: '2小时前', sentiment: 'negative' as const },
    ];
    setReviews(mockReviews);
  }, [platform, timePeriod]);

  const handleBack = () => {
    navigate('/mobile');
  };

  const handleFilterChange = (period: 'today' | '7days' | '30days') => {
    setTimePeriod(period);
    success('时间筛选', `已切换到${period === 'today' ? '今天' : period === '7days' ? '最近7天' : '最近30天'}`);
  };

  const platformNames = {
    'meituan': '美团',
    'dianping': '大众点评',
    'douyin': '抖音',
    'xiaohongshu': '小红书'
  };

  const platformName = platformNames[platform as keyof typeof platformNames] || platform;

  return (
    <MobileLayout title={`${platformName}评价详情`}>
      <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500 pb-20">
        
        {/* 返回按钮和时间筛选 */}
        <div className="flex items-center justify-between">
          <Button variant="ghost" size="icon" onClick={handleBack}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          
          <div className="flex gap-2">
            {(['today', '7days', '30days'] as const).map(period => (
              <Button
                key={period}
                variant={timePeriod === period ? 'default' : 'outline'}
                size="sm"
                onClick={() => handleFilterChange(period)}
                className="text-xs"
              >
                {period === 'today' ? '今天' : period === '7days' ? '7天' : '30天'}
              </Button>
            ))}
          </div>
        </div>

        {/* 统计卡片 */}
        <div className="grid grid-cols-3 gap-3">
          <Card className="p-4 text-center">
            <MessageSquare className="w-6 h-6 text-orange-500 mx-auto mb-2" />
            <p className="text-2xl font-bold">156</p>
            <p className="text-xs text-slate-500">评价数</p>
          </Card>
          <Card className="p-4 text-center">
            <Star className="w-6 h-6 text-amber-500 mx-auto mb-2" />
            <p className="text-2xl font-bold">4.7</p>
            <p className="text-xs text-slate-500">平均评分</p>
          </Card>
          <Card className="p-4 text-center">
            <ThumbsUp className="w-6 h-6 text-emerald-500 mx-auto mb-2" />
            <p className="text-2xl font-bold">76.5%</p>
            <p className="text-xs text-slate-500">好评率</p>
          </Card>
        </div>

        {/* 评价列表 */}
        <div className="space-y-3">
          <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
            <MessageSquare className="w-4 h-4 text-orange-500" />
            最新评价
          </h3>
          
          {reviews.map(review => (
            <Card key={review.id} className="p-4">
              <div className="flex justify-between items-start mb-2">
                <div className="flex items-center gap-2">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold text-white ${
                    review.rating >= 4 ? 'bg-emerald-400' : review.rating >= 3 ? 'bg-amber-400' : 'bg-rose-400'
                  }`}>
                    {review.rating}
                  </div>
                  <div>
                    <span className="text-sm font-medium">{review.user}</span>
                    <Badge variant="outline" className="ml-2 text-xs">{review.platform}</Badge>
                  </div>
                </div>
                <span className="text-xs text-slate-400">{review.time}</span>
              </div>
              <p className="text-sm text-slate-600 mb-2">{review.content}</p>
              <div className="flex items-center gap-1">
                {[1, 2, 3, 4, 5].map(star => (
                  <Star
                    key={star}
                    className={`w-3 h-3 ${
                      star <= review.rating ? 'text-amber-400 fill-amber-400' : 'text-slate-200'
                    }`}
                  />
                ))}
                <Badge className={`ml-2 text-xs ${
                  review.sentiment === 'positive' ? 'bg-emerald-100 text-emerald-700' :
                  review.sentiment === 'negative' ? 'bg-rose-100 text-rose-700' :
                  'bg-amber-100 text-amber-700'
                }`}>
                  {review.sentiment === 'positive' ? '好评' : 
                   review.sentiment === 'negative' ? '差评' : '中评'}
                </Badge>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </MobileLayout>
  );
};

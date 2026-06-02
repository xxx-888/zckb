import React, { useState, useEffect } from 'react';
import { ArrowLeft, Star, ThumbsUp, MessageSquare, Share2, Flag, CheckCircle } from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { MobileLayout } from '../../components/MobileLayout';
import { Skeleton } from '../../components/ui/skeleton';
import { useToast } from '../../hooks/use-toast';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchReviewById } from '../../api/reviews';
import type { Review } from '../../api/reviews';

export const ReviewDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [review, setReview] = useState<Review | null>(null);
  const [loading, setLoading] = useState(true);
  const { success } = useToast();
  const navigate = useNavigate();

  useEffect(() => {
    if (!id) return;
    const load = async () => {
      try {
        setLoading(true);
        const data = await fetchReviewById(id);
        setReview(data);
      } catch (err) {
        console.error('加载评论详情失败', err);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id]);

  // ===== 加载状态（骨架屏）=====
  if (loading) {
    return (
      <MobileLayout title="评论详情">
        <div className="space-y-6 p-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
          {/* 评论头部骨架 */}
          <Skeleton lines={1} className="w-24" />
          
          {/* 评论内容骨架 */}
          <Skeleton lines={4} card={true} className="p-5" />
          
          {/* 操作按钮骨架 */}
          <Skeleton lines={3} className="p-4" />
        </div>
      </MobileLayout>
    );
  }

  if (!review) {
    return (
      <MobileLayout title="评论详情">
        <div className="text-center py-20 text-slate-400">未找到评论数据</div>
      </MobileLayout>
    );
  }

  const handleLike = () => {
    success('赞同成功', '已标记为有价值评论');
  };

  const handleReply = () => {
    success('快速回复', '正在跳转到回复页面...');
    setTimeout(() => {
      success('AI 生成中', 'AI 正在根据评论生成回复话术...');
    }, 1000);
  };

  const handleShare = () => {
    success('分享功能', '分享链接已复制到剪贴板');
  };

  const handleReport = () => {
    success('举报功能', '举报工单已提交');
  };

  const handleApproveReply = () => {
    success('审核通过', '回复已发送，用户将收到通知');
  };

  return (
    <MobileLayout title="评论详情">
      <div className="space-y-6 pb-20 animate-in fade-in slide-in-from-bottom-4 duration-500">
        
        {/* 返回按钮 */}
        <button 
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 text-sm text-slate-600 font-medium"
        >
          <ArrowLeft className="w-4 h-4" />
          返回
        </button>

        {/* 评论主体 */}
        <Card className="p-5 border-none shadow-sm bg-white">
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-xl overflow-hidden bg-slate-100">
                <img src={review.user_avatar} alt={review.user} className="w-full h-full object-cover" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-slate-800">{review.user}</h4>
                <div className="flex items-center gap-2 mt-1">
                  <div className="flex">
                    {[...Array(5)].map((_, i) => (
                      <Star 
                        key={i} 
                        className={`w-3 h-3 ${i < review.rating ? 'text-orange-500 fill-orange-500' : 'text-slate-200'}`} 
                      />
                    ))}
                  </div>
                  <span className="text-[10px] text-slate-400">{review.time}</span>
                </div>
              </div>
            </div>
            <Badge variant="outline" className="text-[10px] text-slate-400">
              {review.platform}
            </Badge>
          </div>

          <p className="text-sm text-slate-700 leading-relaxed mb-4">
            {review.content}
          </p>

          {/* 图片展示 */}
          {review.hasImage && review.images && (
            <div className="grid grid-cols-2 gap-2 mb-4">
              {review.images.map((img, i) => (
                <div key={i} className="rounded-xl overflow-hidden bg-slate-100 h-32">
                  <img src={img} alt={`评论图片${i + 1}`} className="w-full h-full object-cover" />
                </div>
              ))}
            </div>
          )}

          {/* 标签 */}
          <div className="flex flex-wrap gap-1.5 mb-4">
            {(review.tags || []).map((tag, i) => (
              <Badge key={i} variant="outline" className="text-[9px] px-1.5 py-0 h-5 border-orange-100 bg-orange-50/30 text-orange-600">
                {tag}
              </Badge>
            ))}
          </div>

          {/* 操作按钮 */}
          <div className="flex items-center justify-between pt-3 border-t border-slate-50">
            <div className="flex gap-6">
              <button 
                className="flex items-center gap-1.5 text-slate-400 hover:text-orange-500 transition-colors"
                onClick={handleLike}
              >
                <ThumbsUp className="w-4 h-4" />
                <span className="text-[10px] font-bold">{review.likeCount}</span>
              </button>
              <button 
                className="flex items-center gap-1.5 text-slate-400 hover:text-orange-500 transition-colors"
                onClick={handleReply}
              >
                <MessageSquare className="w-4 h-4" />
                <span className="text-[10px] font-bold">回复</span>
              </button>
              <button 
                className="flex items-center gap-1.5 text-slate-400 hover:text-orange-500 transition-colors"
                onClick={handleShare}
              >
                <Share2 className="w-4 h-4" />
                <span className="text-[10px] font-bold">分享</span>
              </button>
            </div>
            <button 
              className="text-slate-300 hover:text-rose-500 transition-colors"
              onClick={handleReport}
            >
              <Flag className="w-4 h-4" />
            </button>
          </div>
        </Card>

        {/* AI 回复建议 */}
        <Card className="p-5 border-none shadow-sm bg-orange-50/30 border border-orange-100">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-8 h-8 rounded-lg bg-orange-500 flex items-center justify-center">
              <MessageSquare className="w-4 h-4 text-white" />
            </div>
            <div>
              <h4 className="text-sm font-bold text-slate-800">AI 生成的回复</h4>
              <p className="text-[10px] text-slate-400">基于语义分析自动生成</p>
            </div>
          </div>

          <div className="bg-white p-4 rounded-xl border border-orange-100 mb-4 text-sm text-slate-700 leading-relaxed">
            {review.reply}
          </div>

          <div className="flex items-center gap-2 text-[10px] text-slate-400 mb-4">
            <CheckCircle className="w-3 h-3 text-emerald-500" />
            <span>AI 生成 · {review.reply_time}</span>
          </div>

          <div className="flex gap-2">
            <Button 
              variant="outline" 
              className="flex-1 h-10 text-xs"
              onClick={() => success('修改回复', '正在跳转到编辑页面...')}
            >
              修改话术
            </Button>
            <Button 
              className="flex-1 h-10 text-xs bg-orange-500 hover:bg-orange-600 text-white"
              onClick={handleApproveReply}
            >
              发送回复
            </Button>
          </div>
        </Card>

        {/* 相关评论推荐 */}
        <div className="space-y-3">
          <h3 className="text-sm font-bold text-slate-800 px-1">相似评论</h3>
          {[
            { id: 2, user: '美食家-小王', content: '环境很棒，适合约会，菜品也很精致。', rating: 5 },
            { id: 3, user: '探店达人', content: '味道不错，还会再来！推荐和牛塔可。', rating: 4 }
          ].map((related) => (
            <Card 
              key={related.id}
              className="p-4 border-none shadow-sm bg-white cursor-pointer hover:shadow-md transition-all"
              onClick={() => navigate(`/mobile/review-detail/${related.id}`)}
            >
              <div className="flex items-center gap-3 mb-2">
                <div className="flex">
                  {[...Array(5)].map((_, i) => (
                    <Star 
                      key={i} 
                      className={`w-2 h-2 ${i < related.rating ? 'text-orange-500 fill-orange-500' : 'text-slate-200'}`} 
                    />
                  ))}
                </div>
                <span className="text-[10px] text-slate-400">{related.user}</span>
              </div>
              <p className="text-xs text-slate-600 line-clamp-2">{related.content}</p>
            </Card>
          ))}
        </div>
      </div>
    </MobileLayout>
  );
};

export default ReviewDetail;

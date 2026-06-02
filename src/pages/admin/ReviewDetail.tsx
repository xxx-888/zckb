import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  Star,
  MessageSquare,
  Flag,
  CheckCircle2,
  XCircle,
  Trash2,
  ExternalLink,
  Calendar,
  Building2,
  Globe,
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { AdminLayout } from '../../components/AdminLayout';
import { useToast } from '../../hooks/use-toast';
import { fetchReviewById, reviewsApi } from '../../api/reviews';
import type { Review } from '../../api/reviews';

const sentimentLabel: Record<string, string> = {
  positive: '正面',
  negative: '负面',
  neutral: '中性',
};

const sentimentColor: Record<string, string> = {
  positive: 'bg-emerald-100 text-emerald-700',
  negative: 'bg-rose-100 text-rose-700',
  neutral: 'bg-slate-100 text-slate-600',
};

export const ReviewDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { success, error: showError } = useToast();

  const [review, setReview] = useState<Review | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [generatingReply, setGeneratingReply] = useState(false);

  const loadReview = async () => {
    if (!id) return;
    try {
      setLoading(true);
      const data = await fetchReviewById(id);
      setReview(data);
    } catch (err) {
      console.error('加载评论详情失败', err);
      showError('加载失败', err instanceof Error ? err.message : '请重试');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReview();
  }, [id]);

  const handleApproveReply = async () => {
    if (!review) return;
    try {
      setActionLoading(true);
      await reviewsApi.approveReply(review.id);
      success('审核通过', '回复已发送');
      loadReview();
    } catch (err) {
      showError('操作失败', err instanceof Error ? err.message : '请重试');
    } finally {
      setActionLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!review) return;
    if (!window.confirm('确定要删除这条评论吗？此操作不可撤销。')) return;
    try {
      setActionLoading(true);
      await reviewsApi.deleteReview(review.id);
      success('删除成功', '评论已删除');
      navigate('/admin/review-management');
    } catch (err) {
      showError('删除失败', err instanceof Error ? err.message : '请重试');
    } finally {
      setActionLoading(false);
    }
  };

  const handleRegenerateReply = async () => {
    if (!review) return;
    try {
      setActionLoading(true);
      setGeneratingReply(true);
      const result = await reviewsApi.regenerateReply(review.id);
      // result 已经是内层 data: { review_id, ai_reply_draft, status }
      if (result?.ai_reply_draft) {
        setReview(prev => prev ? { ...prev, ai_reply_draft: result.ai_reply_draft } : prev);
      }
      success('已重新生成', 'AI 回复已重新生成');
      // 再刷一次完整数据，确保其他字段也同步
      await loadReview();
    } catch (err) {
      showError('操作失败', err instanceof Error ? err.message : '请重试');
    } finally {
      setActionLoading(false);
      setGeneratingReply(false);
    }
  };

  // 加载状态
  if (loading) {
    return (
      <AdminLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="w-10 h-10 border-3 border-orange-500 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
            <p className="text-sm text-slate-400">加载中...</p>
          </div>
        </div>
      </AdminLayout>
    );
  }

  if (!review) {
    return (
      <AdminLayout>
        <div className="flex flex-col items-center justify-center h-64 gap-4">
          <p className="text-slate-400">未找到评论数据</p>
          <Button variant="outline" onClick={() => navigate(-1)}>返回</Button>
        </div>
      </AdminLayout>
    );
  }

  const renderStars = (rating: number) =>
    [...Array(5)].map((_, i) => (
      <Star
        key={i}
        className={`w-4 h-4 ${i < rating ? 'text-amber-400 fill-amber-400' : 'text-slate-200'}`}
      />
    ));

  return (
    <AdminLayout>
      <div className="space-y-6 animate-in fade-in duration-300">
        {/* 面包屑 + 返回 */}
        <div className="flex items-center gap-3">
          <Button
            variant="ghost"
            size="sm"
            className="gap-1 text-slate-500"
            onClick={() => navigate(-1)}
          >
            <ArrowLeft className="w-4 h-4" />
            返回
          </Button>
          <span className="text-slate-300">/</span>
          <span className="text-sm text-slate-500">评论详情</span>
          <Badge className={sentimentColor[review.sentiment] || sentimentColor.neutral}>
            {sentimentLabel[review.sentiment] || review.sentiment}
          </Badge>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* 左侧：评论主体 */}
          <div className="lg:col-span-2 space-y-6">
            <Card className="p-6 border-none shadow-sm">
              {/* 用户信息头部 */}
              <div className="flex items-start justify-between mb-5">
                <div className="flex items-center gap-3">
                  <div className="w-11 h-11 rounded-xl bg-slate-100 flex items-center justify-center overflow-hidden">
                    {review.user_avatar ? (
                      <img
                        src={review.user_avatar}
                        alt={review.user_name || review.user || '用户'}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <span className="text-sm font-bold text-slate-500">
                        {(review.user_name || review.user || '?')[0]}
                      </span>
                    )}
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-slate-800">
                      {review.user_name || review.user}
                    </h4>
                    <div className="flex items-center gap-2 mt-0.5">
                      <div className="flex">{renderStars(review.rating)}</div>
                      {(review.platform_created_at || review.time) && (
                        <span className="text-[11px] text-slate-400">
                          <Calendar className="w-3 h-3 inline mr-1" />
                          {review.platform_created_at || review.time}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
                <Badge variant="outline" className="text-[11px] text-slate-400 gap-1">
                  <Globe className="w-3 h-3" />
                  {review.platform}
                </Badge>
              </div>

              {/* 评论内容 */}
              <div className="bg-slate-50 rounded-xl p-4 mb-4">
                <p className="text-sm text-slate-700 leading-relaxed whitespace-pre-wrap">
                  {review.content}
                </p>
              </div>

              {/* 图片展示 */}
              {review.images && review.images.length > 0 && (
                <div className="grid grid-cols-2 md:grid-cols-3 gap-2 mb-4">
                  {review.images.map((img: string, i: number) => (
                    <div key={i} className="rounded-xl overflow-hidden bg-slate-100 h-32">
                      <img
                        src={img}
                        alt={`评论图片${i + 1}`}
                        className="w-full h-full object-cover cursor-pointer hover:scale-105 transition-transform"
                        onClick={() => window.open(img, '_blank')}
                      />
                    </div>
                  ))}
                </div>
              )}

              {/* 标签 */}
              {review.tags && review.tags.length > 0 && (
                <div className="flex flex-wrap gap-1.5">
                  {review.tags.map((tag: string, i: number) => (
                    <Badge key={i} variant="outline" className="text-[10px] px-1.5 py-0 h-5 border-orange-200 bg-orange-50/50 text-orange-600">
                      {tag}
                    </Badge>
                  ))}
                </div>
              )}
            </Card>

            {/* 店铺信息 */}
            {(review.store_name || review.store_id) && (
              <Card className="p-5 border-none shadow-sm">
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-3">关联店铺</h4>
                <div className="flex items-center gap-3">
                  <Building2 className="w-4 h-4 text-slate-400" />
                  <div>
                    <p className="text-sm font-medium text-slate-700">{review.store_name || '未知店铺'}</p>
                    {review.store_id && (
                      <p className="text-[11px] text-slate-400">ID: {review.store_id}</p>
                    )}
                  </div>
                </div>
              </Card>
            )}
          </div>

          {/* 右侧：AI 回复 + 操作 */}
          <div className="space-y-6">
            {/* AI 回复草稿 */}
            <Card className="p-5 border-none shadow-sm">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-7 h-7 rounded-lg bg-orange-500 flex items-center justify-center">
                  <MessageSquare className="w-3.5 h-3.5 text-white" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-800">AI 回复</h4>
                  <p className="text-[10px] text-slate-400">
                    {review.ai_generated ? '由 AI 自动生成' : '暂无 AI 回复'}
                  </p>
                </div>
              </div>

              {generatingReply ? (
                <div className="bg-slate-50 p-4 rounded-xl mb-4 flex items-center gap-2 text-sm text-slate-400">
                  <div className="w-4 h-4 border-2 border-orange-500 border-t-transparent rounded-full animate-spin"></div>
                  AI 正在生成回复，请稍候...
                </div>
              ) : review.reply || review.ai_reply_draft ? (
                <div className="bg-slate-50 p-4 rounded-xl mb-4 text-sm text-slate-700 leading-relaxed whitespace-pre-wrap">
                  {review.reply || review.ai_reply_draft}
                </div>
              ) : (
                <div className="bg-slate-50 p-4 rounded-xl mb-4 text-sm text-slate-400 text-center">
                  暂无回复内容
                </div>
              )}

              {review.reply_time && (
                <p className="text-[11px] text-slate-400 mb-3">
                  <CheckCircle2 className="w-3 h-3 inline mr-1 text-emerald-500" />
                  回复时间：{review.reply_time}
                </p>
              )}

              <div className="flex flex-col gap-2">
                {(review.reply || review.ai_reply_draft) && !review.replied && (
                  <Button
                    size="sm"
                    className="w-full bg-emerald-500 hover:bg-emerald-600 text-white gap-1"
                    onClick={handleApproveReply}
                    disabled={actionLoading}
                  >
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    通过并发送
                  </Button>
                )}
                {!review.replied && (
                  <Button
                    size="sm"
                    variant="outline"
                    className="w-full gap-1 border-rose-200 text-rose-600 hover:bg-rose-50"
                    onClick={handleRegenerateReply}
                    disabled={actionLoading}
                  >
                    <MessageSquare className="w-3.5 h-3.5" />
                    重新生成回复
                  </Button>
                )}
              </div>
            </Card>

            {/* 操作区 */}
            <Card className="p-5 border-none shadow-sm">
              <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-3">管理操作</h4>
              <div className="flex flex-col gap-2">
                {review.platform_review_id && (
                  <Button
                    size="sm"
                    variant="outline"
                    className="w-full justify-start gap-2"
                    onClick={() => window.open(review.platform_review_id, '_blank')}
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                    查看原平台评论
                  </Button>
                )}
                <Button
                  size="sm"
                  variant="outline"
                  className="w-full justify-start gap-2 border-rose-200 text-rose-600 hover:bg-rose-50"
                  onClick={handleDelete}
                  disabled={actionLoading}
                >
                  <Trash2 className="w-3.5 h-3.5" />
                  删除评论
                </Button>
              </div>
            </Card>

            {/* 状态信息 */}
            <Card className="p-5 border-none shadow-sm">
              <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-3">状态信息</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-slate-500">评论ID</span>
                  <span className="text-slate-700 font-mono text-xs">{review.id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">状态</span>
                  <Badge className={review.replied ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'}>
                    {review.replied ? '已回复' : review.status === 'pending' ? '待处理' : review.status}
                  </Badge>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">风险等级</span>
                  <Badge className={
                    review.risk_level === 'high' ? 'bg-rose-100 text-rose-700' :
                    review.risk_level === 'medium' ? 'bg-amber-100 text-amber-700' :
                    'bg-yellow-100 text-yellow-700'
                  }>
                    {review.risk_level === 'high' ? '高风险' : review.risk_level === 'medium' ? '中风险' : '低风险'}
                  </Badge>
                </div>
                {review.created_at && (
                  <div className="flex justify-between">
                    <span className="text-slate-500">入库时间</span>
                    <span className="text-slate-600 text-xs">{review.created_at}</span>
                  </div>
                )}
              </div>
            </Card>
          </div>
        </div>
      </div>
    </AdminLayout>
  );
};

export default ReviewDetail;

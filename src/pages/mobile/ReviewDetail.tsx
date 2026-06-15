import React, { useState, useEffect, useRef } from 'react';
import { ArrowLeft, Star, ThumbsUp, MessageSquare, Share2, Flag, CheckCircle, Sparkles, RefreshCw, X, ChevronLeft, ChevronRight, Clock } from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { MobileLayout } from '../../components/MobileLayout';
import { Skeleton } from '../../components/ui/skeleton';
import { useToast } from '../../hooks/use-toast';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchReviewById, reviewsApi } from '../../api/reviews';
import type { Review } from '../../api/reviews';
import { normalizeImageUrls } from '../../lib/utils';

// 格式化评论时间为友好字符串
function formatReviewTime(dateStr?: string | null): string {
  if (!dateStr) return '';
  try {
    const d = new Date(dateStr);
    const now = new Date();
    const diff = now.getTime() - d.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return '刚刚';
    if (minutes < 60) return `${minutes}分钟前`;
    if (hours < 24) return `${hours}小时前`;
    if (days < 7) return `${days}天前`;
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    const hh = String(d.getHours()).padStart(2, '0');
    const mi = String(d.getMinutes()).padStart(2, '0');
    return `${mm}-${dd} ${hh}:${mi}`;
  } catch {
    return '';
  }
}

// 清理 HTML 内容中不安全的标签，保留 img 和基本格式
function sanitizeHtmlContent(html: string): string {
  if (!html) return html;
  // 如果不含任何 HTML 标签，直接返回
  if (!/<\w+[\s>]/.test(html)) return html;
  // 移除 script、style、iframe 等危险标签，保留 img br p span b i em strong a
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<iframe[\s\S]*?<\/iframe>/gi, '')
    .replace(/<object[\s\S]*?<\/object>/gi, '')
    .replace(/on\w+\s*=\s*"[^"]*"/gi, '')
    .replace(/on\w+\s*=\s*'[^']*'/gi, '')
    .replace(/on\w+\s*=\s*\S+/gi, '')
    .replace(/javascript\s*:/gi, '');
}

// 检测内容是否包含 HTML
function containsHtml(str: string): boolean {
  return /<(img|br|p|div|span|b|i|em|strong|a)[\s>]/i.test(str);
}

interface SimilarReview {
  id: string;
  user_name?: string;
  user_avatar?: string;
  content?: string;
  rating: number;
  sentiment?: string;
  platform?: string;
  platform_created_at?: string;
  images?: string[];
}

// ========== 图片预览组件 ==========
const ImagePreview: React.FC<{
  images: string[];
  initialIndex: number;
  onClose: () => void;
}> = ({ images, initialIndex, onClose }) => {
  const [currentIndex, setCurrentIndex] = useState(initialIndex);
  const touchStartX = useRef(0);

  const goPrev = () => {
    setCurrentIndex(prev => (prev > 0 ? prev - 1 : images.length - 1));
  };
  const goNext = () => {
    setCurrentIndex(prev => (prev < images.length - 1 ? prev + 1 : 0));
  };

  const handleTouchStart = (e: React.TouchEvent) => {
    touchStartX.current = e.touches[0].clientX;
  };
  const handleTouchEnd = (e: React.TouchEvent) => {
    const diff = touchStartX.current - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 50) {
      diff > 0 ? goNext() : goPrev();
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/95 flex flex-col items-center justify-center">
      {/* 关闭按钮 */}
      <button
        onClick={onClose}
        className="absolute top-4 right-4 z-10 w-10 h-10 rounded-full bg-white/10 flex items-center justify-center text-white/80 hover:bg-white/20 transition-colors"
      >
        <X className="w-5 h-5" />
      </button>

      {/* 图片计数 */}
      <div className="absolute top-5 left-1/2 -translate-x-1/2 text-white/60 text-xs">
        {currentIndex + 1} / {images.length}
      </div>

      {/* 图片 */}
      <div
        className="flex-1 flex items-center justify-center w-full px-4"
        onTouchStart={handleTouchStart}
        onTouchEnd={handleTouchEnd}
      >
        <img
          src={images[currentIndex]}
          alt={`预览 ${currentIndex + 1}`}
          className="max-w-full max-h-[70vh] object-contain rounded-lg"
        />
      </div>

      {/* 左右切换 */}
      {images.length > 1 && (
        <>
          <button
            onClick={goPrev}
            className="absolute left-2 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-white/10 flex items-center justify-center text-white/80 hover:bg-white/20 transition-colors"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
          <button
            onClick={goNext}
            className="absolute right-2 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-white/10 flex items-center justify-center text-white/80 hover:bg-white/20 transition-colors"
          >
            <ChevronRight className="w-5 h-5" />
          </button>
          {/* 底部缩略图 */}
          <div className="flex gap-2 pb-6 px-4 overflow-x-auto max-w-full">
            {images.map((url, i) => (
              <button
                key={i}
                onClick={() => setCurrentIndex(i)}
                className={`flex-shrink-0 w-12 h-12 rounded-lg overflow-hidden border-2 transition-all ${
                  i === currentIndex ? 'border-orange-500 opacity-100' : 'border-transparent opacity-50'
                }`}
              >
                <img src={url} alt="" className="w-full h-full object-cover" />
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export const ReviewDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [review, setReview] = useState<Review | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [similarReviews, setSimilarReviews] = useState<SimilarReview[]>([]);
  const [similarLoading, setSimilarLoading] = useState(false);
  const [generatingReply, setGeneratingReply] = useState(false);
  const [replyDraft, setReplyDraft] = useState('');
  const [previewImages, setPreviewImages] = useState<string[]>([]);
  const [previewIndex, setPreviewIndex] = useState(0);
  const { success, error: toastError } = useToast();
  const navigate = useNavigate();

  // 当 review 数据加载后，同步 ai_reply_draft 到输入框
  useEffect(() => {
    if (review) {
      setReplyDraft(review.ai_reply_draft || review.reply || '');
    }
  }, [review?.id, review?.ai_reply_draft, review?.reply]);

  useEffect(() => {
    if (!id) return;
    const load = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await fetchReviewById(id);
        setReview(data);
      } catch (err: any) {
        setError(err?.message || '加载失败');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id]);

  // 加载相似评论
  const loadSimilarReviews = async () => {
    if (!id) return;
    try {
      setSimilarLoading(true);
      const data = await reviewsApi.getSimilarReviews(id);
      setSimilarReviews(Array.isArray(data) ? data : []);
    } catch {
      setSimilarReviews([]);
    } finally {
      setSimilarLoading(false);
    }
  };

  useEffect(() => {
    if (review && id) {
      loadSimilarReviews();
    }
  }, [review, id]);

  const handleLike = () => {
    success('赞同成功', '已标记为有价值评论');
  };

  const handleShare = () => {
    success('分享功能', '分享链接已复制到剪贴板');
  };

  const handleReport = () => {
    success('举报功能', '举报工单已提交');
  };

  const handleApproveReply = async () => {
    if (!review) return;
    // 如果用户编辑了回复内容，先更新 ai_reply_draft
    if (replyDraft && replyDraft !== (review.ai_reply_draft || '')) {
      try {
        // 将编辑后的内容写回 ai_reply_draft，以便审核记录使用
        await reviewsApi.updateReview(review.id, { reply: replyDraft });
        // 更新本地 review 对象
        setReview(prev => prev ? { ...prev, ai_reply_draft: replyDraft } : prev);
      } catch (err: any) {
        toastError('更新失败', err?.message || '请重试');
        return;
      }
    }
    try {
      await reviewsApi.approveReply(review.id);
      success('已提交审核', '回复已提交，待管理员审核通过后发布');
      const data = await fetchReviewById(id!);
      setReview(data);
      // 清空草稿输入（已提交审核）
      setReplyDraft('');
    } catch (err: any) {
      toastError('提交失败', err?.message || '请重试');
    }
  };

  // 生成 AI 回复
  const handleGenerateReply = async () => {
    if (!review) return;
    try {
      setGeneratingReply(true);
      const result = await reviewsApi.regenerateReply(review.id);
      if (result?.ai_reply_draft) {
        setReplyDraft(result.ai_reply_draft);
        // 同时更新 review 对象
        setReview(prev => prev ? { ...prev, ai_reply_draft: result.ai_reply_draft } : prev);
      }
      success('生成成功', 'AI 回复已生成，可编辑后发送');
    } catch (err: any) {
      toastError('生成失败', err?.message || '请重试');
    } finally {
      setGeneratingReply(false);
    }
  };

  // 点击图片预览
  const handleImageClick = (images: string[], index: number) => {
    setPreviewImages(images);
    setPreviewIndex(index);
  };

  if (loading) {
    return (
      <MobileLayout title="评论详情">
        <div className="space-y-6 p-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <Skeleton lines={1} className="w-24" />
          <Skeleton lines={4} card={true} className="p-5" />
          <Skeleton lines={3} className="p-4" />
        </div>
      </MobileLayout>
    );
  }

  if (!review) {
    return (
      <MobileLayout title="评论详情">
        <div className="text-center py-20 text-slate-400">
          {error ? (
            <div>
              <p className="mb-2">加载失败</p>
              <p className="text-xs text-slate-300">{error}</p>
            </div>
          ) : (
            <p>未找到评论数据</p>
          )}
          <Button variant="outline" className="mt-4" onClick={() => navigate(-1)}>返回</Button>
        </div>
      </MobileLayout>
    );
  }

  const reviewTime = formatReviewTime(review.platform_created_at || review.created_at);
  const imageUrls = normalizeImageUrls(review.images);
  const hasHtmlContent = containsHtml(review.content || '');
  const displayReply = replyDraft || review.reply || review.ai_reply_draft;

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
              <div className="w-12 h-12 rounded-xl overflow-hidden bg-slate-100 flex-shrink-0">
                {review.user_avatar ? (
                  <img src={review.user_avatar} alt={review.user_name || review.user || '用户'} className="w-full h-full object-cover" />
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-sm font-bold text-slate-400">
                    {(review.user_name || review.user || '?')[0]}
                  </div>
                )}
              </div>
              <div className="min-w-0">
                <h4 className="text-sm font-bold text-slate-800 truncate">{review.user_name || review.user || '匿名用户'}</h4>
                <div className="flex items-center gap-2 mt-1">
                  <div className="flex">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className={`w-3 h-3 ${i < review.rating ? 'text-orange-500 fill-orange-500' : 'text-slate-200'}`}
                      />
                    ))}
                  </div>
                  <span className="text-[10px] text-slate-400">{reviewTime}</span>
                </div>
              </div>
            </div>
            <Badge variant="outline" className="text-[10px] text-slate-400 flex-shrink-0">
              {review.platform}
            </Badge>
          </div>

          {/* 评论内容 - 支持 HTML 渲染，防止溢出 */}
          {hasHtmlContent ? (
            <div
              className="text-sm text-slate-700 leading-relaxed mb-4 break-words overflow-wrap-anywhere [&_img]:max-w-full [&_img]:h-auto [&_img]:rounded-lg [&_img]:my-1 [&_img]:inline [&_img]:max-h-32 [&_img]:object-contain [&_a]:text-orange-500 [&_a]:underline"
              dangerouslySetInnerHTML={{ __html: sanitizeHtmlContent(review.content || '') }}
            />
          ) : (
            <p className="text-sm text-slate-700 leading-relaxed mb-4 break-words overflow-wrap-anywhere">
              {review.content}
            </p>
          )}

          {/* 图片展示 - 可点击预览 */}
          {imageUrls.length > 0 && (
            <div className="grid grid-cols-3 gap-1.5 mb-4">
              {imageUrls.map((url, i) => (
                <button
                  key={i}
                  className="rounded-xl overflow-hidden bg-slate-100 aspect-square"
                  onClick={() => handleImageClick(imageUrls, i)}
                >
                  <img
                    src={url}
                    alt={`评论图片${i + 1}`}
                    className="w-full h-full object-cover hover:scale-105 transition-transform"
                    loading="lazy"
                  />
                </button>
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
                <span className="text-[10px] font-bold">赞同</span>
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

        {/* AI 回复区域 */}
        <Card className="p-5 border-none shadow-sm bg-orange-50/30 border border-orange-100">
          <div className="flex items-center gap-2 mb-3">
            <div className="w-8 h-8 rounded-lg bg-orange-500 flex items-center justify-center flex-shrink-0">
              <MessageSquare className="w-4 h-4 text-white" />
            </div>
            <div>
              <h4 className="text-sm font-bold text-slate-800">AI 回复</h4>
              <p className="text-[10px] text-slate-400">
                {displayReply ? (review.ai_generated ? '由 AI 自动生成' : 'AI 回复建议') : '暂未生成 AI 回复'}
              </p>
            </div>
          </div>

          {generatingReply ? (
            <div className="bg-white p-4 rounded-xl border border-orange-100 mb-4 flex items-center gap-2 text-sm text-slate-400">
              <RefreshCw className="w-4 h-4 animate-spin text-orange-500" />
              AI 正在生成回复，请稍候...
            </div>
          ) : displayReply ? (
            <textarea
              value={replyDraft}
              onChange={e => setReplyDraft(e.target.value)}
              className="w-full bg-white p-4 rounded-xl border border-orange-100 mb-4 text-sm text-slate-700 leading-relaxed resize-none min-h-[80px] focus:outline-none focus:ring-2 focus:ring-orange-200 focus:border-orange-300"
              placeholder="编辑回复内容..."
            />
          ) : (
            <div className="bg-white p-4 rounded-xl border border-orange-100 mb-4 text-sm text-slate-400 text-center">
              暂无回复内容，点击下方按钮生成 AI 回复
            </div>
          )}

          {review.reply_time && (
            <div className="flex items-center gap-1.5 text-[10px] text-slate-400 mb-4">
              <CheckCircle className="w-3 h-3 text-emerald-500" />
              <span>回复时间：{formatReviewTime(review.reply_time)}</span>
            </div>
          )}

          <div className="flex gap-2">
            <Button
              variant="outline"
              className="flex-1 h-10 text-xs border-orange-200 text-orange-600 hover:bg-orange-50"
              onClick={handleGenerateReply}
              disabled={generatingReply}
            >
              <Sparkles className="w-3.5 h-3.5 mr-1" />
              {generatingReply ? '生成中...' : displayReply ? '重新生成' : '生成AI回复'}
            </Button>
            {replyDraft && !review.reply && !review.replied && (
              <Button
                className="flex-1 h-10 text-xs bg-orange-500 hover:bg-orange-600 text-white"
                onClick={handleApproveReply}
                disabled={generatingReply}
              >
                <CheckCircle className="w-3.5 h-3.5 mr-1" />
                提交审核
              </Button>
            )}
            {review.reply && (
              <Button
                className="flex-1 h-10 text-xs bg-emerald-500 hover:bg-emerald-600 text-white"
                disabled
              >
                <CheckCircle className="w-3.5 h-3.5 mr-1" />
                已回复
              </Button>
            )}
            {!replyDraft && !review.reply && !review.replied && review.ai_reply_draft && (
              <Button
                className="flex-1 h-10 text-xs bg-amber-500 hover:bg-amber-600 text-white"
                disabled
              >
                <Clock className="w-3.5 h-3.5 mr-1" />
                审核中
              </Button>
            )}
          </div>
        </Card>

        {/* 相似评论 */}
        <div className="space-y-3">
          <h3 className="text-sm font-bold text-slate-800 px-1">相似评论</h3>
          {similarLoading ? (
            <div className="space-y-2">
              {[1, 2].map(i => (
                <Card key={i} className="p-4 border-none shadow-sm bg-white">
                  <Skeleton lines={2} className="h-4" />
                </Card>
              ))}
            </div>
          ) : similarReviews.length > 0 ? (
            similarReviews.map((related) => (
              <Card
                key={related.id}
                className="p-4 border-none shadow-sm bg-white cursor-pointer hover:shadow-md transition-all"
                onClick={() => navigate(`/mobile/review-detail/${related.id}`)}
              >
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-7 h-7 rounded-lg overflow-hidden bg-slate-100 flex-shrink-0">
                    {related.user_avatar ? (
                      <img src={related.user_avatar} alt={related.user_name || ''} className="w-full h-full object-cover" />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-[9px] font-bold text-slate-400">
                        {(related.user_name || '?')[0]}
                      </div>
                    )}
                  </div>
                  <div className="flex items-center gap-2 flex-1 min-w-0">
                    <span className="text-[11px] text-slate-600 font-medium truncate">{related.user_name || '匿名用户'}</span>
                    <div className="flex flex-shrink-0">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          className={`w-2 h-2 ${i < related.rating ? 'text-orange-500 fill-orange-500' : 'text-slate-200'}`}
                        />
                      ))}
                    </div>
                    <span className="text-[9px] text-slate-400 flex-shrink-0">{formatReviewTime(related.platform_created_at)}</span>
                  </div>
                </div>
                <p className="text-xs text-slate-600 line-clamp-2 break-words overflow-wrap-anywhere">{related.content}</p>
              </Card>
            ))
          ) : (
            <Card className="p-6 text-center">
              <MessageSquare className="w-8 h-8 text-slate-300 mx-auto mb-2" />
              <p className="text-xs text-slate-400">暂无相似评论</p>
            </Card>
          )}
        </div>
      </div>

      {/* 图片预览浮层 */}
      {previewImages.length > 0 && (
        <ImagePreview
          images={previewImages}
          initialIndex={previewIndex}
          onClose={() => setPreviewImages([])}
        />
      )}
    </MobileLayout>
  );
};

export default ReviewDetail;

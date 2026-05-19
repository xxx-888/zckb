import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Search, Filter, Calendar, Store, Star, MessageSquare, ChevronRight, TrendingUp, TrendingDown, Minus, AlertCircle, CheckCircle, XCircle, Eye, BarChart3, FileText, Clock, MapPin, Tag, ThumbsUp, ThumbsDown, Meh, ExternalLink } from 'lucide-react'
import { MobileLayout } from '../../components/MobileLayout'

// 报告数据类型
interface ReportData {
  id: string
  title: string
  type: '三好三查' | '服务质量' | '菜品评价' | '综合评估'
  storeName: string
  storeId: string
  date: string
  score: number
  rating: number
  totalReviews: number
  positiveCount: number
  negativeCount: number
  neutralCount: number
  status: 'normal' | 'warning' | 'critical'
  tags: string[]
  summary: string
}

// 评价详情类型
interface ReviewDetail {
  id: string
  reportId: string
  platform: 'dianping' | 'meituan' | 'xiaohongshu'
  rating: number
  content: string
  author: string
  date: string
  tags: string[]
  sentiment: 'positive' | 'negative' | 'neutral'
  isVerified: boolean
  reply?: string
  replyDate?: string
  images?: string[]
  traceability: {
    source: string
    capturedAt: string
    verified: boolean
    rawData: string
  }
}

// 模拟报告数据
const mockReport: ReportData = {
  id: 'RPT-2025-001',
  title: '5月第一周三好三查评估报告',
  type: '三好三查',
  storeName: '海底捞·盈科店',
  storeId: 'store-001',
  date: '2025-05-08',
  score: 92,
  rating: 4.6,
  totalReviews: 156,
  positiveCount: 128,
  negativeCount: 18,
  neutralCount: 10,
  status: 'normal',
  tags: ['服务优质', '菜品新鲜', '环境舒适'],
  summary: '本店整体表现优秀，顾客满意度高。服务响应迅速，主动关怀到位；菜品质量稳定，食材新鲜度获得一致好评；店内环境整洁舒适，卫生状况良好。需关注个别差评反馈的等位时间过长问题。'
}

// 模拟评价列表数据
const mockReviews: ReviewDetail[] = [
  {
    id: 'REV-001',
    reportId: 'RPT-2025-001',
    platform: 'dianping',
    rating: 5,
    content: '服务非常贴心！服务员主动帮我们涮菜，还送了小零食。食材特别新鲜，毛肚很脆嫩。环境也很舒适，下次还会来！',
    author: '美食达人小王',
    date: '2025-05-07',
    tags: ['服务好', '食材新鲜', '环境舒适'],
    sentiment: 'positive',
    isVerified: true,
    reply: '感谢您的好评！我们会继续保持，为您提供更优质的服务体验~',
    replyDate: '2025-05-07',
    images: ['https://example.com/img1.jpg', 'https://example.com/img2.jpg'],
    traceability: {
      source: '大众点评',
      capturedAt: '2025-05-07 14:30:25',
      verified: true,
      rawData: '{"review_id":"DP20250507001","user_id":"U123456","shop_id":"S001"}'
    }
  },
  {
    id: 'REV-002',
    reportId: 'RPT-2025-001',
    platform: 'meituan',
    rating: 2,
    content: '等位时间太长了，等了一个半小时才吃到。虽然口味还行，但这个等待时间真的很难接受。建议改进叫号系统。',
    author: '匿名用户',
    date: '2025-05-06',
    tags: ['等位久', '需要改进'],
    sentiment: 'negative',
    isVerified: true,
    traceability: {
      source: '美团',
      capturedAt: '2025-05-06 19:45:12',
      verified: true,
      rawData: '{"review_id":"MT20250506002","user_id":"U789012","shop_id":"S001"}'
    }
  },
  {
    id: 'REV-003',
    reportId: 'RPT-2025-001',
    platform: 'xiaohongshu',
    rating: 4,
    content: '和朋友一起来吃的，整体体验不错。推荐虾滑和毛肚，特别好吃！就是价格稍微有点贵，不过品质确实可以。',
    author: '小红薯美食记',
    date: '2025-05-05',
    tags: ['推荐', '虾滑好吃', '价格偏高'],
    sentiment: 'positive',
    isVerified: false,
    reply: '感谢您的推荐！我们会继续努力提供更优质的食材~',
    replyDate: '2025-05-06',
    traceability: {
      source: '小红书',
      capturedAt: '2025-05-05 21:15:33',
      verified: false,
      rawData: '{"note_id":"XHS20250505003","user_id":"U345678","shop_id":"S001"}'
    }
  },
  {
    id: 'REV-004',
    reportId: 'RPT-2025-001',
    platform: 'dianping',
    rating: 3,
    content: '味道中规中矩吧，没有什么特别惊艳的。服务还算可以，但也没有想象中那么好。可能期望太高了。',
    author: '普通食客',
    date: '2025-05-04',
    tags: ['一般', '期望过高'],
    sentiment: 'neutral',
    isVerified: true,
    traceability: {
      source: '大众点评',
      capturedAt: '2025-05-04 12:20:18',
      verified: true,
      rawData: '{"review_id":"DP20250504004","user_id":"U901234","shop_id":"S001"}'
    }
  },
  {
    id: 'REV-005',
    reportId: 'RPT-2025-001',
    platform: 'meituan',
    rating: 5,
    content: '生日聚会选在这里，服务员还特意送了长寿面和果盘，特别暖心！朋友都很满意，拍照也很好看。强烈推荐！',
    author: '生日快乐鸭',
    date: '2025-05-03',
    tags: ['生日推荐', '服务暖心', '适合聚会'],
    sentiment: 'positive',
    isVerified: true,
    reply: '祝您生日快乐🎂！感谢选择我们店庆祝生日，能为您留下美好回忆是我们的荣幸！',
    replyDate: '2025-05-03',
    images: ['https://example.com/img3.jpg'],
    traceability: {
      source: '美团',
      capturedAt: '2025-05-03 22:10:45',
      verified: true,
      rawData: '{"review_id":"MT20250503005","user_id":"U567890","shop_id":"S001"}'
    }
  }
]

const TraceabilityDetail: React.FC = () => {
  const { reportId } = useParams<{ reportId: string }>()
  const navigate = useNavigate()
  
  const [report, setReport] = useState<ReportData | null>(null)
  const [reviews, setReviews] = useState<ReviewDetail[]>([])
  const [filteredReviews, setFilteredReviews] = useState<ReviewDetail[]>([])
  const [selectedReview, setSelectedReview] = useState<ReviewDetail | null>(null)
  const [showReviewDetail, setShowReviewDetail] = useState(false)
  const [searchKeyword, setSearchKeyword] = useState('')
  const [filterSentiment, setFilterSentiment] = useState<'all' | 'positive' | 'negative' | 'neutral'>('all')
  const [filterPlatform, setFilterPlatform] = useState<'all' | 'dianping' | 'meituan' | 'xiaohongshu'>('all')
  const [sortBy, setSortBy] = useState<'date' | 'rating'>('date')
  const [isLoading, setIsLoading] = useState(true)

  // 加载数据
  useEffect(() => {
    setIsLoading(true)
    // 模拟API调用
    setTimeout(() => {
      setReport(mockReport)
      setReviews(mockReviews)
      setFilteredReviews(mockReviews)
      setIsLoading(false)
    }, 800)
  }, [reportId])

  // 筛选和排序
  useEffect(() => {
    let filtered = [...reviews]

    // 关键词搜索
    if (searchKeyword) {
      filtered = filtered.filter(r => 
        r.content.includes(searchKeyword) ||
        r.author.includes(searchKeyword) ||
        r.tags.some(tag => tag.includes(searchKeyword))
      )
    }

    // 情感筛选
    if (filterSentiment !== 'all') {
      filtered = filtered.filter(r => r.sentiment === filterSentiment)
    }

    // 平台筛选
    if (filterPlatform !== 'all') {
      filtered = filtered.filter(r => r.platform === filterPlatform)
    }

    // 排序
    filtered.sort((a, b) => {
      if (sortBy === 'date') {
        return new Date(b.date).getTime() - new Date(a.date).getTime()
      } else {
        return b.rating - a.rating
      }
    })

    setFilteredReviews(filtered)
  }, [reviews, searchKeyword, filterSentiment, filterPlatform, sortBy])

  // 获取状态图标
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'normal':
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case 'warning':
        return <AlertCircle className="w-5 h-5 text-yellow-500" />
      case 'critical':
        return <XCircle className="w-5 h-5 text-red-500" />
      default:
        return null
    }
  }

  // 获取情感图标
  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return <ThumbsUp className="w-4 h-4 text-green-500" />
      case 'negative':
        return <ThumbsDown className="w-4 h-4 text-red-500" />
      case 'neutral':
        return <Meh className="w-4 h-4 text-gray-500" />
      default:
        return null
    }
  }

  // 获取平台图标
  const getPlatformName = (platform: string) => {
    switch (platform) {
      case 'dianping':
        return '大众点评'
      case 'meituan':
        return '美团'
      case 'xiaohongshu':
        return '小红书'
      default:
        return platform
    }
  }

  // 渲染星级
  const renderStars = (rating: number) => {
    const stars = []
    for (let i = 1; i <= 5; i++) {
      if (i <= rating) {
        stars.push(<Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />)
      } else {
        stars.push(<Star key={i} className="w-4 h-4 text-gray-300" />)
      }
    }
    return <div className="flex">{stars}</div>
  }

  // 查看评价详情
  const handleViewReview = (review: ReviewDetail) => {
    setSelectedReview(review)
    setShowReviewDetail(true)
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-500">加载中...</p>
        </div>
      </div>
    )
  }

  if (!report) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500">未找到报告数据</p>
        </div>
      </div>
    )
  }

  return (
    <MobileLayout title="溯源详情">
      {/* 报告概览 */}
      <div className="p-4 space-y-4">
        <div className="bg-white rounded-lg shadow-sm p-4">
          <div className="flex items-start justify-between mb-3">
            <div className="flex-1">
              <h2 className="text-lg font-semibold text-gray-900 mb-1">{report.title}</h2>
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <Store className="w-4 h-4" />
                <span>{report.storeName}</span>
                <span className="text-gray-300">|</span>
                <Calendar className="w-4 h-4" />
                <span>{report.date}</span>
              </div>
            </div>
          </div>

          {/* 评分概览 */}
          <div className="grid grid-cols-4 gap-3 mb-4">
            <div className="bg-blue-50 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-blue-600">{report.score}</div>
              <div className="text-xs text-gray-500 mt-1">综合评分</div>
            </div>
            <div className="bg-yellow-50 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-yellow-600">{report.rating}</div>
              <div className="text-xs text-gray-500 mt-1">星级评分</div>
            </div>
            <div className="bg-green-50 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-green-600">{report.positiveCount}</div>
              <div className="text-xs text-gray-500 mt-1">好评数</div>
            </div>
            <div className="bg-red-50 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-red-600">{report.negativeCount}</div>
              <div className="text-xs text-gray-500 mt-1">差评数</div>
            </div>
          </div>

          {/* 标签 */}
          <div className="flex flex-wrap gap-2 mb-3">
            {report.tags.map((tag, index) => (
              <span key={index} className="px-2 py-1 bg-blue-50 text-blue-600 text-xs rounded-full">
                {tag}
              </span>
            ))}
          </div>

          {/* 摘要 */}
          <div className="bg-gray-50 rounded-lg p-3">
            <p className="text-sm text-gray-700 leading-relaxed">{report.summary}</p>
          </div>
        </div>

        {/* 搜索和筛选 */}
        <div className="bg-white rounded-lg shadow-sm p-4 space-y-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="搜索评价内容、作者、标签..."
              value={searchKeyword}
              onChange={(e) => setSearchKeyword(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div className="flex space-x-2 overflow-x-auto">
            <button
              onClick={() => setFilterSentiment('all')}
              className={`px-3 py-1.5 rounded-full text-sm whitespace-nowrap transition-colors ${
                filterSentiment === 'all'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              全部 ({reviews.length})
            </button>
            <button
              onClick={() => setFilterSentiment('positive')}
              className={`px-3 py-1.5 rounded-full text-sm whitespace-nowrap transition-colors ${
                filterSentiment === 'positive'
                  ? 'bg-green-500 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              好评 ({report.positiveCount})
            </button>
            <button
              onClick={() => setFilterSentiment('negative')}
              className={`px-3 py-1.5 rounded-full text-sm whitespace-nowrap transition-colors ${
                filterSentiment === 'negative'
                  ? 'bg-red-500 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              差评 ({report.negativeCount})
            </button>
            <button
              onClick={() => setFilterSentiment('neutral')}
              className={`px-3 py-1.5 rounded-full text-sm whitespace-nowrap transition-colors ${
                filterSentiment === 'neutral'
                  ? 'bg-gray-500 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              中评 ({report.neutralCount})
            </button>
          </div>

          <div className="flex space-x-2">
            <select
              value={filterPlatform}
              onChange={(e) => setFilterPlatform(e.target.value as any)}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
            >
              <option value="all">全部平台</option>
              <option value="dianping">大众点评</option>
              <option value="meituan">美团</option>
              <option value="xiaohongshu">小红书</option>
            </select>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
            >
              <option value="date">按日期排序</option>
              <option value="rating">按评分排序</option>
            </select>
          </div>
        </div>

        {/* 评价列表 */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="font-medium text-gray-900">
              评价列表 ({filteredReviews.length})
            </h3>
          </div>

          {filteredReviews.length === 0 ? (
            <div className="bg-white rounded-lg shadow-sm p-8 text-center">
              <MessageSquare className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-500">没有找到匹配的评价</p>
            </div>
          ) : (
            filteredReviews.map((review) => (
              <div
                key={review.id}
                className="bg-white rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow cursor-pointer"
                onClick={() => handleViewReview(review)}
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    {getSentimentIcon(review.sentiment)}
                    <span className="font-medium text-gray-900">{review.author}</span>
                    {review.isVerified && (
                      <span className="px-1.5 py-0.5 bg-blue-50 text-blue-600 text-xs rounded">
                        已核验
                      </span>
                    )}
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs text-gray-500">{getPlatformName(review.platform)}</span>
                    <ChevronRight className="w-4 h-4 text-gray-400" />
                  </div>
                </div>

                <div className="flex items-center space-x-2 mb-2">
                  {renderStars(review.rating)}
                  <span className="text-sm text-gray-500">{review.date}</span>
                </div>

                <p className="text-sm text-gray-700 mb-3 line-clamp-2">{review.content}</p>

                <div className="flex flex-wrap gap-1.5">
                  {review.tags.map((tag, index) => (
                    <span key={index} className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">
                      {tag}
                    </span>
                  ))}
                </div>

                {review.reply && (
                  <div className="mt-3 pl-3 border-l-2 border-blue-500 bg-blue-50 rounded-r p-2">
                    <p className="text-xs text-gray-500 mb-1">商家回复：</p>
                    <p className="text-sm text-gray-700">{review.reply}</p>
                  </div>
                )}

                <div className="mt-3 flex items-center justify-between text-xs text-gray-400">
                  <div className="flex items-center space-x-1">
                    <Clock className="w-3 h-3" />
                    <span>溯源时间：{review.traceability.capturedAt}</span>
                  </div>
                  {review.traceability.verified && (
                    <div className="flex items-center space-x-1 text-green-500">
                      <CheckCircle className="w-3 h-3" />
                      <span>已验证</span>
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* 评价详情弹窗 */}
      {showReviewDetail && selectedReview && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-end justify-center">
          <div className="bg-white w-full max-w-lg rounded-t-2xl max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-white border-b border-gray-200 p-4 rounded-t-2xl">
              <div className="flex items-center justify-between">
                <h3 className="font-semibold text-gray-900">评价详情</h3>
                <button
                  onClick={() => setShowReviewDetail(false)}
                  className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <XCircle className="w-5 h-5 text-gray-500" />
                </button>
              </div>
            </div>

            <div className="p-4 space-y-4">
              {/* 评价基本信息 */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    {getSentimentIcon(selectedReview.sentiment)}
                    <span className="font-medium text-gray-900">{selectedReview.author}</span>
                    {selectedReview.isVerified && (
                      <span className="px-1.5 py-0.5 bg-blue-50 text-blue-600 text-xs rounded">
                        已核验
                      </span>
                    )}
                  </div>
                  <span className="text-sm text-gray-500">{getPlatformName(selectedReview.platform)}</span>
                </div>
                {renderStars(selectedReview.rating)}
              </div>

              {/* 评价内容 */}
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-sm text-gray-700 leading-relaxed">{selectedReview.content}</p>
              </div>

              {/* 图片 */}
              {selectedReview.images && selectedReview.images.length > 0 && (
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-2">附图</h4>
                  <div className="grid grid-cols-3 gap-2">
                    {selectedReview.images.map((img, index) => (
                      <div key={index} className="aspect-square bg-gray-200 rounded-lg flex items-center justify-center">
                        <span className="text-xs text-gray-400">图片 {index + 1}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 标签 */}
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-2">标签</h4>
                <div className="flex flex-wrap gap-1.5">
                  {selectedReview.tags.map((tag, index) => (
                    <span key={index} className="px-2 py-1 bg-blue-50 text-blue-600 text-sm rounded-full">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>

              {/* 商家回复 */}
              {selectedReview.reply && (
                <div className="bg-blue-50 rounded-lg p-3">
                  <h4 className="text-sm font-medium text-gray-700 mb-2">商家回复</h4>
                  <p className="text-sm text-gray-700">{selectedReview.reply}</p>
                  <p className="text-xs text-gray-500 mt-1">回复时间：{selectedReview.replyDate}</p>
                </div>
              )}

              {/* 溯源信息 */}
              <div className="bg-yellow-50 rounded-lg p-3">
                <h4 className="text-sm font-medium text-gray-700 mb-2 flex items-center space-x-1">
                  <Eye className="w-4 h-4" />
                  <span>溯源信息</span>
                </h4>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-500">数据来源</span>
                    <span className="text-gray-900">{selectedReview.traceability.source}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-500">采集时间</span>
                    <span className="text-gray-900">{selectedReview.traceability.capturedAt}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-500">验证状态</span>
                    <span className={selectedReview.traceability.verified ? 'text-green-600' : 'text-red-600'}>
                      {selectedReview.traceability.verified ? '已验证' : '未验证'}
                    </span>
                  </div>
                  <div className="pt-2 border-t border-yellow-200">
                    <p className="text-xs text-gray-500 mb-1">原始数据：</p>
                    <pre className="text-xs bg-white rounded p-2 overflow-x-auto">
                      {selectedReview.traceability.rawData}
                    </pre>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </MobileLayout>
  )
}

export default TraceabilityDetail

import React, { useState, useEffect } from 'react';
import { 
  AlertCircle, 
  MessageSquare, 
  Send, 
  RefreshCw, 
  ChevronRight,
  User,
  Star,
  Activity,
  AlertTriangle,
  Lightbulb,
  CheckCircle2
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { Skeleton } from '../../components/ui/skeleton';
import { MobileLayout, useStore } from '../../components/MobileLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';
import { useNavigate } from 'react-router-dom';
import { fetchNegativeReplyTasks, negativeReplyApi } from '../../api/negative-reply';
import type { NegativeReplyTask } from '../../api/negative-reply';

export const NegativeReply: React.FC = () => {
  const { success, error } = useToast();
  const navigate = useNavigate();
  const { selectedStore } = useStore();
  const [tasks, setTasks] = useState<NegativeReplyTask[]>([]);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState<string | null>(null);
  const fetchedRef = React.useRef(false);

  const loadData = async () => {
    try {
      setLoading(true);
      setFetchError(null);
      const storeId = selectedStore?.id;
      const data = await fetchNegativeReplyTasks(storeId);
      setTasks(data.items || []);
    } catch (err) {
      setFetchError(err instanceof Error ? err.message : '获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (fetchedRef.current) return;
    fetchedRef.current = true;
    loadData();
  }, []);

  const getAvgScore = (scores: any) => {
    const vals = Object.values(scores) as number[];
    return (vals.reduce((a, b) => a + b, 0) / vals.length).toFixed(1);
  };

  const handleRefresh = () => {
    setIsRefreshing(true);
    success('刷新中', '正在获取最新差评...');
    setTimeout(() => {
      setIsRefreshing(false);
      loadData();
    }, 2000);
  };

  const handleApproveReply = async (taskId: number) => {
    try {
      await negativeReplyApi.approveTask(String(taskId));
      success('审核通过', `回复已发送 (ID: ${taskId})`);
      loadData();
    } catch (err) {
      error('操作失败', err instanceof Error ? err.message : '请重试');
    }
  };

  const handleRejectReply = async (taskId: number) => {
    try {
      await negativeReplyApi.rejectTask(String(taskId), '用户驳回，需人工处理');
      success('已驳回', `AI 回复已驳回，请手动编写 (ID: ${taskId})`);
      loadData();
    } catch (err) {
      error('操作失败', err instanceof Error ? err.message : '请重试');
    }
  };

  const handleEditReply = async (taskId: number) => {
    try {
      await negativeReplyApi.regenerateReply(String(taskId));
      success('重新生成', `AI 正在重新生成回复草稿 (ID: ${taskId})...`);
      loadData();
    } catch (err) {
      error('操作失败', err instanceof Error ? err.message : '请重试');
    }
  };

  const handleViewTask = (taskId: number, reviewId?: string) => {
    navigate(`/mobile/review-detail/${reviewId || taskId}`);
  };

  if (loading) {
    return (
      <MobileLayout title="差评危机处理">
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

  if (fetchError) {
    return (
      <MobileLayout title="差评危机处理">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <p className="text-sm text-rose-500 mb-4">{fetchError}</p>
            <button onClick={loadData} className="text-sm text-orange-600 font-bold">重试</button>
          </div>
        </div>
      </MobileLayout>
    );
  }

  return (
    <MobileLayout title="差评危机处理">
      <div className="space-y-6 pb-20 animate-in fade-in slide-in-from-bottom-4 duration-500">
        
        {/* Header Stats */}
        <div className="grid grid-cols-2 gap-3">
          <Card className="p-4 bg-rose-50 border-rose-100 text-center">
            <h4 className="text-2xl font-black text-rose-600">{tasks.length}</h4>
            <p className="text-[10px] font-bold text-rose-400 uppercase">待处理差评</p>
          </Card>
          <Card className="p-4 bg-orange-50 border-orange-100 text-center">
            <h4 className="text-2xl font-black text-orange-600">92%</h4>
            <p className="text-[10px] font-bold text-orange-400 uppercase">回复满意度</p>
          </Card>
        </div>

        {/* Refresh Button */}
        <Button 
          variant="outline" 
          className="w-full border-orange-200 text-orange-600 hover:bg-orange-50"
          onClick={handleRefresh}
          disabled={isRefreshing}
        >
          <RefreshCw className={`w-4 h-4 mr-2 ${isRefreshing ? 'animate-spin' : ''}`} />
          {isRefreshing ? '刷新中...' : '刷新差评列表'}
        </Button>
        
        {/* Task List */}
        <div className="space-y-4">
          <h3 className="font-bold text-slate-800 text-sm px-1 flex items-center gap-2 uppercase tracking-wider">
            <AlertCircle className="w-4 h-4 text-rose-500" /> 急需处理 ({tasks.length})
          </h3>
          
          {tasks.map((task) => {
            const avgScore = parseFloat(getAvgScore(task.scores));
            const isLowScore = avgScore < 7;

            return (
              <Card 
                key={task.id} 
                className="p-0 border-none shadow-md overflow-hidden bg-white cursor-pointer hover:shadow-lg transition-all"
                onClick={() => handleViewTask(task.id, task.review_id || task.id)}
              >
                <div className="p-4 border-b border-slate-50">
                  <div className="flex justify-between items-start mb-2">
                    <div className="flex items-center gap-2">
                      <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center">
                        <User className="w-4 h-4 text-slate-400" />
                      </div>
                      <div>
                        <h4 className="text-sm font-bold text-slate-800">{task.user}</h4>
                        <div className="flex gap-0.5">
                          {[...Array(5)].map((_, i) => (
                            <Star key={i} className={cn("w-2.5 h-2.5", i < task.rating ? "text-rose-500 fill-rose-500" : "text-slate-200")} />
                          ))}
                        </div>
                      </div>
                    </div>
                    <Badge className="bg-slate-100 text-slate-500 border-none text-[10px]">{task.platform}</Badge>
                  </div>
                  <p className="text-sm text-slate-600 leading-relaxed italic">"{task.content}"</p>
                </div>

                <div className={cn("p-4", isLowScore ? "bg-amber-50/50" : "bg-orange-50/30")}>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-[10px] font-bold text-orange-600 uppercase tracking-wider flex items-center gap-1">
                      <RefreshCw className="w-3 h-3" /> AI 建议回复草稿
                    </span>
                    <div className="flex gap-1.5">
                      {task.risk === 'high' && (
                        <Badge className="bg-rose-100 text-rose-600 border-none text-[9px] h-4">高风险</Badge>
                      )}
                      <Badge className={cn("text-[9px] h-4 border-none", isLowScore ? "bg-amber-100 text-amber-600" : "bg-emerald-100 text-emerald-600")}>
                        质量分: {avgScore}
                      </Badge>
                    </div>
                  </div>

                  {isLowScore && (
                    <div className="bg-white p-2 rounded-lg border border-amber-200 mb-3 flex items-center gap-2">
                      <AlertTriangle className="w-3.5 h-3.5 text-amber-500" />
                      <p className="text-[10px] text-amber-700 font-medium">
                        本回复质量较低，建议重新生成或人工修改。
                      </p>
                    </div>
                  )}

                  <div className="bg-white p-3 rounded-xl border border-orange-100/50 mb-4 text-xs text-slate-600 leading-relaxed shadow-sm">
                    {task.aiDraft}
                  </div>

                  {/* 4D Quality Score Radar (Horizontal Progress Bars) */}
                  <div className="grid grid-cols-2 gap-x-4 gap-y-2 mb-4 bg-white/50 p-2 rounded-lg">
                    {[
                      { label: '真实性', val: task.scores.realism },
                      { label: '共情力', val: task.scores.empathy },
                      { label: '具体度', val: task.scores.concreteness },
                      { label: '一致性', val: task.scores.consistency },
                    ].map((s, idx) => (
                      <div key={idx} className="space-y-1">
                        <div className="flex justify-between text-[8px] font-bold text-slate-400">
                          <span>{s.label}</span>
                          <span className="text-slate-600">{s.val}/10</span>
                        </div>
                        <div className="h-1 bg-slate-100 rounded-full overflow-hidden">
                          <div 
                            className={cn("h-full", s.val > 7 ? "bg-emerald-400" : "bg-orange-400")} 
                            style={{ width: `${s.val * 10}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className="flex gap-2">
                    <Button 
                      variant="outline" 
                      className="flex-1 h-10 rounded-xl text-xs border-slate-200 bg-white"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleEditReply(task.id);
                      }}
                    >
                      重新生成
                    </Button>
                    <Button 
                      className="flex-[2] h-10 rounded-xl text-xs bg-orange-500 hover:bg-orange-600 text-white gap-2 shadow-md shadow-orange-100"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleApproveReply(task.id);
                      }}
                    >
                      立即发送 <Send className="w-3 h-3" />
                    </Button>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>

        <Button 
          variant="ghost" 
          className="w-full text-slate-400 text-xs py-4"
          onClick={() => success('历史记录', '正在加载已处理的历史记录...')}
        >
          查看已处理的历史记录 <ChevronRight className="w-3 h-3 ml-1" />
        </Button>
      </div>
    </MobileLayout>
  );
};

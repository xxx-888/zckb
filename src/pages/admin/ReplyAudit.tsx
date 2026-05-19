import React, { useState } from 'react';
import { 
  FileCheck, 
  Search, 
  Filter, 
  CheckCircle, 
  XCircle, 
  AlertCircle, 
  MessageSquare, 
  User, 
  ExternalLink, 
  ChevronRight, 
  ShieldAlert, 
  Edit2,
  Trash2,
  RefreshCw
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { AdminLayout } from '../../components/AdminLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';

interface Audit {
  id: number;
  store: string;
  review: string;
  reply: string;
  status: 'pending' | 'approved' | 'rejected';
  risk: 'high' | 'medium' | 'low' | 'none';
  time: string;
}

export const ReplyAudit: React.FC = () => {
  const [selectedAudit, setSelectedAudit] = useState<number | null>(1);
  const [searchQuery, setSearchQuery] = useState('');
  const [showRejectDialog, setShowRejectDialog] = useState(false);
  const [rejectReason, setRejectReason] = useState('');
  const [isRegenerating, setIsRegenerating] = useState(false);
  
  const [audits, setAudits] = useState<Audit[]>([
    { 
      id: 1, 
      store: '香格里拉大酒店·旗舰店', 
      review: '味道还可以，就是上菜太慢了，等了快一个小时。', 
      reply: '尊敬的顾客，非常抱歉让您久等了。由于当天是节假日客流量较大，厨房压力较大导致上菜延时。我们已经记录了您的反馈，并会优化高峰期的出餐流程。下次光临我们将为您赠送精美甜点一份，期待您的再次光顾。',
      status: 'pending',
      risk: 'low',
      time: '10分钟前'
    },
    { 
      id: 2, 
      store: '悦享西餐厅', 
      review: '食材不新鲜，吃完肚子不舒服！', 
      reply: '您好，听到这个消息我们深感抱歉。我们所有的食材都是每日新鲜采购，绝不会出现不新鲜的情况。请问您具体是哪天就餐的？我们需要核实并给您一个满意的答复。',
      status: 'pending',
      risk: 'high',
      time: '30分钟前'
    },
    { 
      id: 3, 
      store: '心心咖啡厅', 
      review: '环境很好，咖啡师很专业。', 
      reply: '感谢您的夸奖！很高兴我们的环境和专业服务能给您留下深刻印象。我们会继续努力，期待您的再次光临！',
      status: 'approved',
      risk: 'none',
      time: '1小时前'
    }
  ]);

  const { success, error } = useToast();

  const filteredAudits = audits.filter(a => 
    a.store.toLowerCase().includes(searchQuery.toLowerCase()) ||
    a.review.toLowerCase().includes(searchQuery.toLowerCase()) ||
    a.reply.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleApprove = (id: number) => {
    setAudits(audits.map(a => 
      a.id === id ? { ...a, status: 'approved' as const } : a
    ));
    success('审核通过', '该回复已通过审核并自动发布');
  };

  const handleReject = (id: number) => {
    if (!rejectReason.trim()) {
      error('拒绝失败', '请填写拒绝原因');
      return;
    }
    setAudits(audits.map(a => 
      a.id === id ? { ...a, status: 'rejected' as const } : a
    ));
    setShowRejectDialog(false);
    setRejectReason('');
    success('已拒绝', '该回复已拒绝，AI 将重新生成');
    
    // 模拟重新生成
    setTimeout(() => {
      setAudits(audits.map(a => 
        a.id === id ? { ...a, reply: a.reply + '\n\n[重新生成] 已根据您的反馈优化回复内容...' } : a
      ));
      success('重新生成完成', 'AI 已根据反馈重新生成回复');
    }, 2000);
  };

  const handleEditReply = (id: number, newReply: string) => {
    setAudits(audits.map(a => 
      a.id === id ? { ...a, reply: newReply } : a
    ));
    success('修改成功', '回复内容已更新');
  };

  const handleBatchApprove = () => {
    const pendingCount = audits.filter(a => a.status === 'pending').length;
    setAudits(audits.map(a => 
      a.status === 'pending' ? { ...a, status: 'approved' as const } : a
    ));
    success('批量通过', `已批量通过 ${pendingCount} 条待审核回复`);
  };

  const handleDeleteAudit = (id: number) => {
    const audit = audits.find(a => a.id === id);
    setAudits(audits.filter(a => a.id !== id));
    success('删除成功', `审核项 "${audit?.store}" 已删除`);
  };

  const handleRegenerate = (id: number) => {
    setIsRegenerating(true);
    success('重新生成', 'AI 正在根据原评价重新生成回复...');
    setTimeout(() => {
      setIsRegenerating(false);
      const audit = audits.find(a => a.id === id);
      if (audit) {
        setAudits(audits.map(a => 
          a.id === id ? { ...a, reply: a.reply + '\n\n[重新生成] ' + a.reply.split('').reverse().join('') } : a
        ));
        success('生成完成', 'AI 已重新生成回复，请审核');
      }
    }, 2000);
  };

  const selectedAuditData = audits.find(a => a.id === selectedAudit);

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">AI 回复审核</h2>
            <p className="text-slate-500 mt-1">审核系统自动生成的回复内容，确保品牌调性与合规性</p>
          </div>
          <div className="flex gap-2">
            <Button 
              variant="outline" 
              className="gap-2"
              onClick={handleBatchApprove}
            >
              <CheckCircle className="w-4 h-4 text-emerald-500" /> 
              全部通过
            </Button>
            <Button 
              className="bg-indigo-600 hover:bg-indigo-700 text-white gap-2"
              onClick={() => success('刷新列表', '正在刷新审核列表...')}
            >
              <RefreshCw className="w-4 h-4" />
              刷新
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Audit List */}
          <div className="lg:col-span-5 space-y-4">
            <Card className="p-4 border-none shadow-sm bg-white">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <input 
                  placeholder="搜索店铺或内容..." 
                  className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-indigo-500/20" 
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
            </Card>

            <div className="space-y-3 h-[calc(100vh-280px)] overflow-y-auto pr-2 custom-scrollbar">
              {filteredAudits.map((audit) => (
                <Card 
                  key={audit.id} 
                  className={cn(
                    "p-4 border-none shadow-sm cursor-pointer transition-all hover:shadow-md",
                    selectedAudit === audit.id ? "ring-2 ring-indigo-500 bg-indigo-50/30" : "bg-white"
                  )}
                  onClick={() => setSelectedAudit(audit.id)}
                >
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="text-sm font-bold text-slate-900 truncate flex-1 mr-2">{audit.store}</h4>
                    <span className="text-[10px] text-slate-400 whitespace-nowrap">{audit.time}</span>
                  </div>
                  <p className="text-xs text-slate-500 line-clamp-1 mb-3 italic">"{audit.review}"</p>
                  <div className="flex items-center justify-between">
                    <Badge className={cn(
                      "text-[10px] h-5 border-none",
                      audit.status === 'pending' ? "bg-amber-100 text-amber-700" : 
                      audit.status === 'approved' ? "bg-emerald-100 text-emerald-700" : 
                      "bg-rose-100 text-rose-700"
                    )}>
                      {audit.status === 'pending' ? '待审核' : audit.status === 'approved' ? '已通过' : '已拒绝'}
                    </Badge>
                    {audit.risk === 'high' && (
                      <Badge className="bg-rose-100 text-rose-700 text-[10px] h-5 border-none gap-1">
                        <ShieldAlert className="w-3 h-3" /> 高风险
                      </Badge>
                    )}
                    {audit.risk === 'medium' && (
                      <Badge className="bg-amber-100 text-amber-700 text-[10px] h-5 border-none gap-1">
                        <AlertCircle className="w-3 h-3" /> 中风险
                      </Badge>
                    )}
                  </div>
                </Card>
              ))}
            </div>
          </div>

          {/* Audit Detail */}
          <div className="lg:col-span-7">
            {selectedAuditData ? (
              <Card className="h-full border-none shadow-sm flex flex-col bg-white">
                <div className="p-6 border-b border-slate-50">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="text-lg font-bold text-slate-900">审核详情</h3>
                      <p className="text-sm text-slate-500 mt-1">流水号: AUD-20260508-{selectedAuditData.id}</p>
                    </div>
                    <div className="flex gap-2">
                      {selectedAuditData.status === 'pending' && (
                        <>
                          <Button 
                            variant="outline" 
                            size="sm" 
                            className="text-rose-600 hover:bg-rose-50 border-rose-200"
                            onClick={() => setShowRejectDialog(true)}
                          >
                            <XCircle className="w-4 h-4 mr-2" /> 拒绝并重生成
                          </Button>
                          <Button 
                            size="sm" 
                            className="bg-indigo-600 hover:bg-indigo-700 text-white"
                            onClick={() => handleApprove(selectedAuditData.id)}
                          >
                            <CheckCircle className="w-4 h-4 mr-2" /> 审核通过
                          </Button>
                        </>
                      )}
                      {selectedAuditData.status === 'approved' && (
                        <Badge className="bg-emerald-100 text-emerald-700 border-none text-[10px] h-6">
                          <CheckCircle className="w-3 h-3 mr-1" /> 已通过
                        </Badge>
                      )}
                      {selectedAuditData.status === 'rejected' && (
                        <Badge className="bg-rose-100 text-rose-700 border-none text-[10px] h-6">
                          <XCircle className="w-3 h-3 mr-1" /> 已拒绝
                        </Badge>
                      )}
                    </div>
                  </div>
                </div>

                <div className="p-6 space-y-8 flex-1 overflow-y-auto">
                  <div className="space-y-3">
                    <div className="flex items-center gap-2 text-sm font-bold text-slate-700">
                      <MessageSquare className="w-4 h-4 text-slate-400" /> 用户原评价
                    </div>
                    <div className="p-4 bg-slate-50 rounded-xl border border-slate-100">
                      <p className="text-sm text-slate-600 leading-relaxed">
                        {selectedAuditData.review}
                      </p>
                    </div>
                  </div>

                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2 text-sm font-bold text-slate-700">
                        <FileCheck className="w-4 h-4 text-indigo-500" /> AI 生成回复
                      </div>
                      <Button 
                        variant="ghost" 
                        size="sm"
                        className="h-7 text-xs text-indigo-600"
                        onClick={() => handleRegenerate(selectedAuditData.id)}
                        disabled={isRegenerating}
                      >
                        {isRegenerating ? <RefreshCw className="w-3 h-3 animate-spin mr-1" /> : <Edit2 className="w-3 h-3 mr-1" />}
                        {isRegenerating ? '生成中...' : '重新生成'}
                      </Button>
                    </div>
                    <div className="p-5 bg-indigo-50/30 rounded-xl border border-indigo-100 relative group">
                      <textarea 
                        className="w-full bg-transparent border-none outline-none text-sm text-slate-700 leading-relaxed resize-none h-32"
                        defaultValue={selectedAuditData.reply}
                        onBlur={(e) => handleEditReply(selectedAuditData.id, e.target.value)}
                      />
                      <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <Button variant="ghost" size="icon" className="h-7 w-7">
                          <Edit2 className="w-3.5 h-3.5 text-indigo-600" />
                        </Button>
                      </div>
                    </div>
                    <p className="text-[10px] text-slate-400 italic">提示：可直接在上方区域修改回复内容后提交审核。</p>
                  </div>

                  <div className="p-4 bg-amber-50 rounded-xl border border-amber-100 space-y-2">
                    <div className="flex items-center gap-2 text-xs font-bold text-amber-700">
                      <AlertCircle className="w-4 h-4" /> 风险提示 (Risk Analysis)
                    </div>
                    <p className="text-xs text-amber-600 leading-relaxed">
                      {selectedAuditData.risk === 'high' ? 
                        '该回复可能加剧用户不满，建议采用"补偿+承诺"策略。AI 检测到评论涉及"食材新鲜度"投诉，已采用对应纠错模型。' : 
                        selectedAuditData.risk === 'medium' ?
                        '该回复引用了具体的优惠补偿措施，请确保门店已授权该额度的补偿权限。' :
                        '该回复符合品牌调性，未发现合规性风险。'}
                    </p>
                  </div>
                </div>

                {showRejectDialog && (
                  <div className="p-6 border-t border-slate-50">
                    <div className="space-y-3">
                      <label className="text-xs font-bold text-slate-500">拒绝原因</label>
                      <textarea 
                        className="w-full h-20 p-3 bg-slate-50 border border-slate-200 rounded-lg text-sm resize-none outline-none focus:ring-2 focus:ring-rose-500/20"
                        placeholder="请填写拒绝原因，AI 将根据此反馈重新生成回复..."
                        value={rejectReason}
                        onChange={(e) => setRejectReason(e.target.value)}
                      />
                      <div className="flex gap-2 justify-end">
                        <Button 
                          variant="ghost" 
                          size="sm"
                          onClick={() => { setShowRejectDialog(false); setRejectReason(''); }}
                        >
                          取消
                        </Button>
                        <Button 
                          size="sm"
                          className="bg-rose-600 hover:bg-rose-700 text-white"
                          onClick={() => handleReject(selectedAuditData.id)}
                        >
                          确认拒绝并重生成
                        </Button>
                      </div>
                    </div>
                  </div>
                )}
              </Card>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-slate-400 bg-white/50 rounded-2xl border-2 border-dashed border-slate-200">
                <FileCheck className="w-12 h-12 mb-4 opacity-20" />
                <p className="text-sm">请从左侧选择一个待审核项进行查看</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </AdminLayout>
  );
};

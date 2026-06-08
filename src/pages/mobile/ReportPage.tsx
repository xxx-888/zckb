import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  FileText,
  Calendar,
  Download,
  Sparkles,
  Copy,
  CheckCircle2,
  ChevronRight,
  Store,
  Clock,
  TrendingUp,
  BookOpen,
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { Button } from '../../components/ui/button';
import { MobileLayout } from '../../components/MobileLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';

interface ReportTemplate {
  id: string;
  title: string;
  desc: string;
  icon: React.ElementType;
  color: string;
  bgColor: string;
  type: 'weekly' | 'monthly_ops' | 'monthly_asset';
}

const reportTemplates: ReportTemplate[] = [
  {
    id: 'weekly',
    title: '客户数据周报',
    desc: '营业额、套餐核销、门店运营指标周度汇总与分析',
    icon: TrendingUp,
    color: 'text-orange-600',
    bgColor: 'bg-orange-50',
    type: 'weekly',
  },
  {
    id: 'monthly_ops',
    title: '月度代运营执行报告',
    desc: '月度运营执行情况、KPI完成度、问题与改进',
    icon: BookOpen,
    color: 'text-indigo-600',
    bgColor: 'bg-indigo-50',
    type: 'monthly_ops',
  },
  {
    id: 'monthly_asset',
    title: '月度客户资产分析报告',
    desc: '客户资产全貌分析，包含评价、流量、转化等',
    icon: FileText,
    color: 'text-emerald-600',
    bgColor: 'bg-emerald-50',
    type: 'monthly_asset',
  },
];

export const ReportPage: React.FC = () => {
  const { success } = useToast();
  const navigate = useNavigate();
  const [generating, setGenerating] = useState<string | null>(null);
  const [generated, setGenerated] = useState<Record<string, boolean>>({});
  const [copiedPrompt, setCopiedPrompt] = useState(false);

  const handleGenerate = (template: ReportTemplate) => {
    setGenerating(template.id);
    // 模拟生成过程
    setTimeout(() => {
      setGenerating(null);
      setGenerated(prev => ({ ...prev, [template.id]: true }));
      success('报告生成', `${template.title}已生成`);
    }, 2000);
  };

  const handleExport = (template: ReportTemplate) => {
    success('导出报告', `${template.title} PDF 正在导出...`);
  };

  const handleAIPrompt = () => {
    const prompt = `请基于以下门店数据生成运营分析报告：
- 门店：犇犇牛牛牛（大学城店）
- 时间：5.24-31号
- 营业额：¥124,580（环比+43.4%）
- 美团营业额：¥31,290 | 抖音营业额：¥78,900
- 到店人数：1,458 | 接待桌数：486 | 人均：¥85.4
- 美团曝光55,363次，访问5,283次，购买273人
- 抖音页面曝光753人，购买105人，核销72人
- 差评关键词：室内抽烟
- 美团星级4.8，点评4.0，抖音4.7
- 榜单：美团人气榜第1名，点评热门榜第2名，抖音人气榜第6名`;

    const copyPrompt = async () => {
      try {
        if (navigator.clipboard?.writeText) {
          await navigator.clipboard.writeText(prompt);
        } else {
          // HTTP 环境下 clipboard API 不可用，降级用 execCommand
          const ta = document.createElement('textarea');
          ta.value = prompt;
          ta.style.cssText = 'position:fixed;left:-9999px';
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
        }
        setCopiedPrompt(true);
        success('AI提示词', '已复制到剪贴板，可粘贴到 ChatGPT 等 AI 工具中使用');
        setTimeout(() => setCopiedPrompt(false), 3000);
      } catch {
        // 最后降级：弹窗让用户手动复制
        window.prompt('请手动复制以下提示词：', prompt);
      }
    };
    copyPrompt();
  };

  return (
    <MobileLayout title="客户报告">
      <div className="pb-24 space-y-4">

        {/* 门店 + 时间信息 */}
        <Card className="p-4 bg-gradient-to-r from-slate-900 to-slate-800 border-slate-700">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Store className="w-4 h-4 text-white/70" />
              <span className="text-sm font-bold text-white">犇犇牛牛牛（大学城店）</span>
            </div>
            <div className="flex items-center gap-1.5 text-white/60">
              <Clock className="w-3.5 h-3.5" />
              <span className="text-xs">数据截止至本周</span>
            </div>
          </div>
        </Card>

        {/* 报告模板 */}
        <div>
          <p className="text-xs font-bold text-slate-700 mb-3 px-1">选择报告模板</p>
          <div className="space-y-3">
            {reportTemplates.map((template) => (
              <Card key={template.id} className="bg-white border-slate-100 shadow-sm overflow-hidden">
                <div className="p-4">
                  <div className="flex items-start gap-3">
                    <div className={cn("w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0", template.bgColor)}>
                      <template.icon className={cn("w-5 h-5", template.color)} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-bold text-slate-900">{template.title}</p>
                      <p className="text-[11px] text-slate-400 mt-0.5 leading-relaxed">{template.desc}</p>
                    </div>
                  </div>
                </div>
                <div className="border-t border-slate-100 px-4 py-2.5 flex items-center justify-end gap-2 bg-slate-50/50">
                  {generated[template.id] ? (
                    <>
                      <Button size="sm" variant="outline" className="h-7 text-[10px] gap-1"
                        onClick={() => handleExport(template)}>
                        <Download className="w-3 h-3" />导出PDF
                      </Button>
                      <Button size="sm" className="h-7 text-[10px] gap-1 bg-slate-900 hover:bg-slate-800"
                        onClick={() => navigate('/mobile/report-preview?type=' + template.id)}>
                        查看 <ChevronRight className="w-3 h-3" />
                      </Button>
                    </>
                  ) : (
                    <Button size="sm"
                      className={cn("h-7 text-[10px] gap-1",
                        generating === template.id ? "bg-slate-300" : "bg-slate-900 hover:bg-slate-800")}
                      disabled={generating === template.id}
                      onClick={() => handleGenerate(template)}>
                      {generating === template.id ? (
                        <>
                          <div className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                          生成中...
                        </>
                      ) : (
                        <>
                          <Sparkles className="w-3 h-3" />自动生成
                        </>
                      )}
                    </Button>
                  )}
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* AI 分析预留接口 */}
        <Card className="p-4 bg-white border-slate-100 shadow-sm">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-7 h-7 rounded-lg bg-purple-50 flex items-center justify-center">
              <Sparkles className="w-3.5 h-3.5 text-purple-500" />
            </div>
            <span className="text-sm font-bold text-slate-700">AI 分析</span>
            <Badge className="text-[8px] bg-purple-50 text-purple-600 border-purple-200">即将上线</Badge>
          </div>
          <p className="text-xs text-slate-500 leading-relaxed mb-3">
            将当前门店数据打包为标准提示词，复制后可粘贴到 ChatGPT、文心一言等外部 AI 工具中获取深度分析。未来将内置 AI 分析能力实现一键生成。
          </p>
          <Button size="sm"
            className={cn("w-full text-xs gap-2 h-9",
              copiedPrompt ? "bg-emerald-600 hover:bg-emerald-700" : "bg-purple-600 hover:bg-purple-700")}
            onClick={handleAIPrompt}>
            {copiedPrompt ? (
              <><CheckCircle2 className="w-4 h-4" />已复制到剪贴板</>
            ) : (
              <><Copy className="w-4 h-4" />生成AI分析提示词并复制</>
            )}
          </Button>
        </Card>
      </div>
    </MobileLayout>
  );
};

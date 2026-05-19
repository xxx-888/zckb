import React, { useState } from 'react';
import { AdminLayout } from '../../components/AdminLayout';
import { 
  Bell, 
  Plus, 
  MessageSquare, 
  Bot, 
  Smartphone, 
  Webhook, 
  CheckCircle2, 
  AlertCircle, 
  History, 
  Settings2,
  Send,
  Trash2,
  Edit,
  PlayCircle,
  Clock,
  ExternalLink,
  Save,
  FileText,
  AlertTriangle
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Switch } from '../../components/ui/switch';
import { Badge } from '../../components/ui/badge';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../../components/ui/tabs';
import { cn } from '../../lib/utils';

// Mock Data for channels
const MOCK_CHANNELS = [
  { id: '1', name: '总部企业微信', type: 'wechat', url: 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx', status: 'online', description: '用于全量差评即时预警' },
  { id: '2', name: '运营中心飞书', type: 'feishu', url: 'https://open.feishu.cn/open-apis/bot/v2/hook/xxx', status: 'online', description: '用于周报数据推送' },
  { id: '3', name: '技术告警钉钉', type: 'dingtalk', url: 'https://oapi.dingtalk.com/robot/send?access_token=xxx', status: 'offline', description: '系统异常监控' },
];

// Mock Data for rules
const MOCK_RULES = [
  { id: '1', name: '实时差评预警', channel: '总部企业微信', type: '差评监控', condition: '风险等级 >= 中', frequency: '即时', status: true },
  { id: '2', name: '门店周报推送', channel: '运营中心飞书', type: '周报推送', condition: '每周一 09:00', frequency: '每周', status: true },
  { id: '3', name: '核心指标异常告警', channel: '总部企业微信', type: '看板推送', condition: '好评率下降 > 10%', frequency: '即时', status: false },
];

// Mock Data for history
const MOCK_HISTORY = [
  { id: '1', time: '2026-05-09 10:24:15', channel: '企业微信', status: 'success', recipient: '全员群', content: '【实时预警】门店：徐汇美罗城店 收到一条高风险差评...', latency: '120ms' },
  { id: '2', time: '2026-05-09 09:00:00', channel: '飞书', status: 'success', recipient: '运营管理组', content: '【运营周报】本周口碑健康度评分：88分，环比上升2%...', latency: '450ms' },
  { id: '3', time: '2026-05-08 23:45:12', channel: '钉钉', status: 'failed', recipient: '技术团队', content: '【系统告警】美团API连接超时，重试中...', latency: '3200ms', error: 'Connect Timeout' },
];

export const NotificationConfig: React.FC = () => {
  const [activeTab, setActiveTab] = useState('channels');
  const [testStatus, setTestStatus] = useState<'idle' | 'testing' | 'success' | 'error'>('idle');

  const handleTestConnection = () => {
    setTestStatus('testing');
    setTimeout(() => {
      setTestStatus('success');
      setTimeout(() => setTestStatus('idle'), 3000);
    }, 1500);
  };

  return (
    <AdminLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-slate-900 tracking-tight">通知配置管理</h2>
            <p className="text-slate-500 mt-1">管理系统推送渠道、预警规则及内容模板</p>
          </div>
          <div className="flex gap-3">
            <Button variant="outline" className="gap-2">
              <History className="w-4 h-4" />
              推送历史
            </Button>
            <Button className="bg-amber-500 hover:bg-amber-600 gap-2">
              <Plus className="w-4 h-4" />
              新增规则
            </Button>
          </div>
        </div>

        <Tabs defaultValue="channels" onValueChange={setActiveTab} className="w-full">
          <TabsList className="bg-white border border-slate-200 p-1 rounded-xl w-fit">
            <TabsTrigger value="channels" className="rounded-lg data-[state=active]:bg-amber-50 data-[state=active]:text-amber-600">渠道管理</TabsTrigger>
            <TabsTrigger value="rules" className="rounded-lg data-[state=active]:bg-amber-50 data-[state=active]:text-amber-600">通知规则</TabsTrigger>
            <TabsTrigger value="templates" className="rounded-lg data-[state=active]:bg-amber-50 data-[state=active]:text-amber-600">内容模板</TabsTrigger>
            <TabsTrigger value="monitor" className="rounded-lg data-[state=active]:bg-amber-50 data-[state=active]:text-amber-600">推送监控</TabsTrigger>
            <TabsTrigger value="test" className="rounded-lg data-[state=active]:bg-amber-50 data-[state=active]:text-amber-600">推送测试</TabsTrigger>
          </TabsList>

          {/* 1. 推送渠道管理 */}
          <TabsContent value="channels" className="mt-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {MOCK_CHANNELS.map(channel => (
                <Card key={channel.id} className="p-6 border-slate-200 hover:shadow-md transition-shadow">
                  <div className="flex justify-between items-start mb-4">
                    <div className={cn(
                      "p-3 rounded-xl",
                      channel.type === 'wechat' ? "bg-emerald-50 text-emerald-600" :
                      channel.type === 'feishu' ? "bg-blue-50 text-blue-600" :
                      "bg-indigo-50 text-indigo-600"
                    )}>
                      {channel.type === 'wechat' && <Bot className="w-6 h-6" />}
                      {channel.type === 'feishu' && <MessageSquare className="w-6 h-6" />}
                      {channel.type === 'dingtalk' && <Smartphone className="w-6 h-6" />}
                    </div>
                    <Badge variant={channel.status === 'online' ? 'default' : 'secondary'} className={cn(
                      channel.status === 'online' ? "bg-emerald-500" : "bg-slate-300"
                    )}>
                      {channel.status === 'online' ? '运行中' : '离线'}
                    </Badge>
                  </div>
                  <h3 className="font-bold text-slate-900 text-lg mb-1">{channel.name}</h3>
                  <p className="text-slate-500 text-sm mb-4 line-clamp-2">{channel.description}</p>
                  
                  <div className="space-y-3 mb-6">
                    <div className="text-xs text-slate-400 font-medium uppercase tracking-wider">Webhook URL</div>
                    <div className="bg-slate-50 p-2 rounded border border-slate-100 text-xs font-mono truncate text-slate-600">
                      {channel.url}
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <Button variant="outline" size="sm" className="flex-1" onClick={handleTestConnection}>
                      {testStatus === 'testing' && channel.id === '1' ? '测试中...' : '测试连接'}
                    </Button>
                    <Button variant="ghost" size="sm" className="text-slate-500 hover:text-slate-900">
                      <Edit className="w-4 h-4" />
                    </Button>
                    <Button variant="ghost" size="sm" className="text-rose-500 hover:text-rose-600">
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </Card>
              ))}
              <Card className="p-6 border-dashed border-2 border-slate-200 bg-slate-50/50 flex flex-col items-center justify-center text-center group cursor-pointer hover:bg-slate-50 transition-colors">
                <div className="w-12 h-12 rounded-full bg-slate-200 flex items-center justify-center mb-4 group-hover:bg-amber-100 group-hover:text-amber-600 transition-colors">
                  <Plus className="w-6 h-6 text-slate-500 group-hover:text-amber-600" />
                </div>
                <h3 className="font-bold text-slate-600 group-hover:text-slate-900">添加新渠道</h3>
                <p className="text-slate-400 text-sm mt-1">支持企微、钉钉、飞书、Webhook等</p>
              </Card>
            </div>
          </TabsContent>

          {/* 2. 通知规则配置 */}
          <TabsContent value="rules" className="mt-6">
            <Card className="overflow-hidden border-slate-200">
              <table className="w-full text-left">
                <thead className="bg-slate-50 border-b border-slate-200">
                  <tr>
                    <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">规则名称</th>
                    <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">类型</th>
                    <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">推送渠道</th>
                    <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">触发条件</th>
                    <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">状态</th>
                    <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider text-right">操作</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {MOCK_RULES.map(rule => (
                    <tr key={rule.id} className="hover:bg-slate-50/50 transition-colors">
                      <td className="px-6 py-4">
                        <div className="font-medium text-slate-900">{rule.name}</div>
                      </td>
                      <td className="px-6 py-4">
                        <Badge variant="outline" className="font-normal">{rule.type}</Badge>
                      </td>
                      <td className="px-6 py-4 text-slate-600">{rule.channel}</td>
                      <td className="px-6 py-4 text-slate-600 font-mono text-xs">{rule.condition}</td>
                      <td className="px-6 py-4">
                        <Switch checked={rule.status} />
                      </td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex justify-end gap-2">
                          <Button variant="ghost" size="sm" className="text-slate-400 hover:text-slate-900">
                            <Edit className="w-4 h-4" />
                          </Button>
                          <Button variant="ghost" size="sm" className="text-rose-400 hover:text-rose-600">
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <div className="p-4 bg-slate-50/50 border-t border-slate-100 flex justify-center">
                <Button variant="ghost" className="text-amber-600 gap-2 hover:bg-amber-50">
                  <Plus className="w-4 h-4" /> 查看更多规则
                </Button>
              </div>
            </Card>

            <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card className="p-6 border-slate-200">
                <h4 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
                  <Settings2 className="w-4 h-4 text-amber-500" />
                  高级配置：推送窗口
                </h4>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-sm font-medium">夜间免打扰</div>
                      <div className="text-xs text-slate-500">22:00 - 08:00 期间除高风险告警外不推送</div>
                    </div>
                    <Switch defaultChecked />
                  </div>
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-sm font-medium">合并推送</div>
                      <div className="text-xs text-slate-500">同门店同类信息 5 分钟内仅推送一次</div>
                    </div>
                    <Switch defaultChecked />
                  </div>
                </div>
              </Card>
              <Card className="p-6 border-slate-200">
                <h4 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-rose-500" />
                  告警升级机制
                </h4>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-sm font-medium">差评超时未回复提醒</div>
                      <div className="text-xs text-slate-500">差评超过 2 小时未回复，自动同步给区域经理</div>
                    </div>
                    <Switch defaultChecked />
                  </div>
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-sm font-medium">食安问题立即熔断</div>
                      <div className="text-xs text-slate-500">发现疑似食安词汇，5分钟内未确认自动上报总部</div>
                    </div>
                    <Switch defaultChecked />
                  </div>
                </div>
              </Card>
            </div>
          </TabsContent>

          {/* 3. 推送内容模板管理 */}
          <TabsContent value="templates" className="mt-6">
            <div className="flex gap-6 h-[600px]">
              <div className="w-1/3 space-y-3 overflow-y-auto pr-2">
                <div className="bg-amber-50 p-4 rounded-xl border border-amber-100 flex items-center gap-3 cursor-pointer">
                  <div className="p-2 bg-amber-500 rounded-lg">
                    <AlertCircle className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <div className="font-bold text-amber-900 text-sm">【实时预警】差评详情</div>
                    <div className="text-amber-700 text-xs mt-1">最近修改：2小时前</div>
                  </div>
                </div>
                <div className="bg-white p-4 rounded-xl border border-slate-200 flex items-center gap-3 cursor-pointer hover:bg-slate-50">
                  <div className="p-2 bg-slate-100 rounded-lg">
                    <FileText className="w-5 h-5 text-slate-600" />
                  </div>
                  <div>
                    <div className="font-bold text-slate-900 text-sm">【周报推送】运营概览</div>
                    <div className="text-slate-500 text-xs mt-1">最近修改：3天前</div>
                  </div>
                </div>
                <div className="bg-white p-4 rounded-xl border border-slate-200 flex items-center gap-3 cursor-pointer hover:bg-slate-50">
                  <div className="p-2 bg-slate-100 rounded-lg">
                    <Bell className="w-5 h-5 text-slate-600" />
                  </div>
                  <div>
                    <div className="font-bold text-slate-900 text-sm">【看板推送】异常波动</div>
                    <div className="text-slate-500 text-xs mt-1">最近修改：1周前</div>
                  </div>
                </div>
                <Button variant="outline" className="w-full border-dashed border-2 py-8 flex flex-col gap-2">
                  <Plus className="w-5 h-5" />
                  <span>创建新模板</span>
                </Button>
              </div>

              <div className="flex-1 flex flex-col gap-4">
                <Card className="flex-1 flex flex-col p-6 border-slate-200">
                  <div className="flex justify-between items-center mb-6">
                    <h4 className="font-bold text-slate-900">模板编辑：【实时预警】差评详情</h4>
                    <div className="flex gap-2">
                      <Button variant="outline" size="sm">重置</Button>
                      <Button className="bg-amber-500 hover:bg-amber-600 size-sm gap-2">
                        <Save className="w-4 h-4" /> 保存修改
                      </Button>
                    </div>
                  </div>
                  
                  <div className="flex-1 flex gap-6 overflow-hidden">
                    <div className="flex-1 flex flex-col gap-4">
                      <div className="space-y-2">
                        <label className="text-sm font-medium text-slate-700">模板标题</label>
                        <Input defaultValue="【智能口碑实时预警】您有一条新差评待处理" />
                      </div>
                      <div className="flex-1 space-y-2 flex flex-col">
                        <label className="text-sm font-medium text-slate-700">正文内容 (Markdown)</label>
                        <textarea 
                          className="flex-1 w-full bg-slate-50 p-4 rounded-lg border border-slate-200 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-amber-500/20"
                          defaultValue={`### 🚨 差评实时预警

**门店名称**：{store_name}
**风险等级**：{risk_level}
**发现时间**：{find_time}

**评价内容**：
> {content}

**AI分析建议**：
{ai_advice}

[立即处理并回复]({handle_url})`}
                        />
                      </div>
                      <div className="flex flex-wrap gap-2">
                        <Badge className="bg-slate-100 text-slate-600 hover:bg-slate-200 cursor-pointer">{`{store_name}`}</Badge>
                        <Badge className="bg-slate-100 text-slate-600 hover:bg-slate-200 cursor-pointer">{`{risk_level}`}</Badge>
                        <Badge className="bg-slate-100 text-slate-600 hover:bg-slate-200 cursor-pointer">{`{content}`}</Badge>
                        <Badge className="bg-slate-100 text-slate-600 hover:bg-slate-200 cursor-pointer">{`{find_time}`}</Badge>
                        <Badge className="bg-slate-100 text-slate-600 hover:bg-slate-200 cursor-pointer">{`{platform}`}</Badge>
                      </div>
                    </div>
                    
                    <div className="w-80 flex flex-col gap-4">
                      <label className="text-sm font-medium text-slate-700 flex items-center gap-2">
                        预览 (企业微信样式)
                      </label>
                      <div className="flex-1 bg-slate-900 rounded-2xl p-4 overflow-y-auto relative">
                        {/* Mock Mobile UI */}
                        <div className="bg-white rounded-lg p-3 text-sm shadow-sm">
                          <h4 className="font-bold text-slate-900 mb-2">🚨 差评实时预警</h4>
                          <p className="text-slate-700 mb-1"><span className="font-semibold">门店名称</span>：徐汇美罗城店</p>
                          <p className="text-slate-700 mb-1"><span className="font-semibold">风险等级</span>：<span className="text-rose-500">高风险</span></p>
                          <p className="text-slate-700 mb-2"><span className="font-semibold">发现时间</span>：2026-05-09 10:24</p>
                          <div className="bg-slate-50 border-l-4 border-slate-200 p-2 text-slate-500 mb-3 italic">
                            味道真的很差，里面的肉都是酸的，服务员还态度不好...
                          </div>
                          <p className="font-semibold text-slate-900 mb-1 text-xs">AI分析建议：</p>
                          <p className="text-xs text-slate-600 mb-3">经核实属于食安风险，请立即联系店长核实菜品新鲜度，并在15分钟内回复顾客进行致歉。已生成参考话术...</p>
                          <div className="pt-2 border-t border-slate-100 text-blue-600 font-medium text-center">
                            立即处理并回复
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </Card>
              </div>
            </div>
          </TabsContent>

          {/* 4. 推送监控 */}
          <TabsContent value="monitor" className="mt-6 space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card className="p-4 border-slate-200">
                <div className="text-slate-500 text-sm mb-1">今日总推送</div>
                <div className="text-2xl font-bold">1,284</div>
                <div className="mt-2 text-xs text-emerald-500 flex items-center gap-1">
                  <Clock className="w-3 h-3" /> 环比昨日 +12%
                </div>
              </Card>
              <Card className="p-4 border-slate-200">
                <div className="text-slate-500 text-sm mb-1">成功率</div>
                <div className="text-2xl font-bold text-emerald-600">99.8%</div>
                <div className="mt-2 text-xs text-slate-400">平均延迟 240ms</div>
              </Card>
              <Card className="p-4 border-slate-200">
                <div className="text-slate-500 text-sm mb-1">失败重试中</div>
                <div className="text-2xl font-bold text-amber-500">2</div>
                <div className="mt-2 text-xs text-slate-400">最近重试: 12:04:15</div>
              </Card>
              <Card className="p-4 border-slate-200">
                <div className="text-slate-500 text-sm mb-1">活跃通道</div>
                <div className="text-2xl font-bold">8/9</div>
                <div className="mt-2 text-xs text-rose-500 flex items-center gap-1">
                  <AlertCircle className="w-3 h-3" /> 钉钉通道连接异常
                </div>
              </Card>
            </div>

            <Card className="overflow-hidden border-slate-200">
              <div className="p-4 border-b border-slate-100 flex justify-between items-center bg-white">
                <h4 className="font-bold text-slate-900">最近推送记录</h4>
                <div className="flex gap-2">
                  <Input placeholder="搜索接收人/内容" className="w-64 h-8 text-xs" />
                  <Button variant="outline" size="sm">筛选</Button>
                </div>
              </div>
              <table className="w-full text-left">
                <thead className="bg-slate-50 border-b border-slate-200">
                  <tr>
                    <th className="px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">时间</th>
                    <th className="px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">渠道</th>
                    <th className="px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">接收对象</th>
                    <th className="px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">内容摘要</th>
                    <th className="px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">状态</th>
                    <th className="px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wider text-right">响应时间</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {MOCK_HISTORY.map(log => (
                    <tr key={log.id} className="hover:bg-slate-50/50 transition-colors">
                      <td className="px-6 py-4 text-xs text-slate-500 font-mono">{log.time}</td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2">
                          <div className={cn(
                            "w-2 h-2 rounded-full",
                            log.channel === '企业微信' ? "bg-emerald-500" :
                            log.channel === '飞书' ? "bg-blue-500" : "bg-indigo-500"
                          )}></div>
                          <span className="text-sm text-slate-700">{log.channel}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-slate-600">{log.recipient}</td>
                      <td className="px-6 py-4">
                        <div className="text-sm text-slate-900 truncate max-w-xs">{log.content}</div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-1">
                          {log.status === 'success' ? (
                            <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                          ) : (
                            <AlertCircle className="w-4 h-4 text-rose-500" />
                          )}
                          <span className={cn(
                            "text-xs font-medium",
                            log.status === 'success' ? "text-emerald-600" : "text-rose-600"
                          )}>
                            {log.status === 'success' ? '成功' : '失败'}
                          </span>
                        </div>
                        {log.error && <div className="text-[10px] text-rose-400 mt-1">{log.error}</div>}
                      </td>
                      <td className="px-6 py-4 text-right text-xs text-slate-400 font-mono">
                        {log.latency}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <div className="p-4 bg-slate-50 border-t border-slate-100 flex justify-between items-center">
                <div className="text-xs text-slate-500">共 5,283 条推送记录</div>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" disabled>上一页</Button>
                  <Button variant="outline" size="sm">下一页</Button>
                </div>
              </div>
            </Card>
          </TabsContent>

          {/* 5. 推送测试 */}
          <TabsContent value="test" className="mt-6">
            <Card className="max-w-4xl mx-auto p-8 border-slate-200">
              <div className="mb-8">
                <h3 className="text-xl font-bold text-slate-900 mb-2">推送模拟测试</h3>
                <p className="text-slate-500">输入测试数据并选择渠道，验证通知推送的最终展示效果</p>
              </div>

              <div className="grid grid-cols-2 gap-8">
                <div className="space-y-6">
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-slate-700">选择推送渠道</label>
                    <select className="w-full bg-white border border-slate-200 rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-amber-500/20 focus:outline-none">
                      <option>总部企业微信机器人 (Wechat)</option>
                      <option>运营中心飞书机器人 (Feishu)</option>
                      <option>自定义 Webhook</option>
                    </select>
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm font-medium text-slate-700">模拟场景数据</label>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-1">
                        <label className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">门店名称</label>
                        <Input defaultValue="北京三里屯店" />
                      </div>
                      <div className="space-y-1">
                        <label className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">风险等级</label>
                        <select className="w-full bg-slate-50 border border-slate-200 rounded p-2 text-xs">
                          <option>高风险</option>
                          <option>中风险</option>
                          <option>低风险</option>
                        </select>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm font-medium text-slate-700">评价正文模拟</label>
                    <textarea 
                      className="w-full h-32 bg-slate-50 p-4 rounded-lg border border-slate-200 text-sm focus:outline-none"
                      defaultValue="在这里面吃出了钢丝球，太可怕了，差评！服务员还没人理我。"
                    />
                  </div>

                  <Button className="w-full bg-amber-500 hover:bg-amber-600 h-11 text-lg font-bold gap-2">
                    <Send className="w-5 h-5" /> 立即发起测试推送
                  </Button>
                </div>

                <div className="space-y-4">
                  <div className="text-sm font-medium text-slate-700">实时测试反馈</div>
                  <div className="bg-slate-900 rounded-xl p-6 min-h-[300px] font-mono text-sm">
                    <div className="flex items-center gap-2 text-emerald-400 mb-2">
                      <PlayCircle className="w-4 h-4" /> [SYSTEM] 开始推送测试任务...
                    </div>
                    <div className="text-slate-400 mb-1">2026-05-09 10:45:01 {"->"} 加载内容模板: 【实时预警】差评详情</div>
                    <div className="text-slate-400 mb-1">2026-05-09 10:45:01 {"->"} 变量渲染成功: {"{store_name}"} {"=>"} 北京三里屯店</div>
                    <div className="text-slate-400 mb-1">2026-05-09 10:45:01 {"->"} 正在连接 Webhook 节点...</div>
                    <div className="flex items-center gap-2 text-emerald-400 mb-1">
                      <CheckCircle2 className="w-4 h-4" /> [SUCCESS] 渠道响应：HTTP 200 OK
                    </div>                    <div className="text-slate-300 mt-4 p-3 bg-slate-800 rounded border border-slate-700">
                      {`{
  "errcode": 0,
  "errmsg": "ok",
  "msgid": "MSGID_7823412938471"
}`}
                    </div>
                    <div className="text-slate-500 mt-4 italic text-xs">
                      测试耗时: 382ms | 推送结果已同步至监控日志
                    </div>
                  </div>
                  
                  <div className="p-4 bg-amber-50 rounded-xl border border-amber-100 flex gap-3">
                    <AlertCircle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
                    <div className="text-xs text-amber-800 leading-relaxed">
                      提示：测试推送将真实发送到对应渠道的接收端，请确保接收人已知晓这是测试信息，或使用专门的测试渠道进行验证。
                    </div>
                  </div>
                </div>
              </div>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </AdminLayout>
  );
};

export default NotificationConfig;

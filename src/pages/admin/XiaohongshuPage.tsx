import React, { useState } from 'react';
import { 
  Search, 
  Download, 
  RefreshCw, 
  CheckCircle, 
  Clock, 
  AlertCircle,
  BarChart3
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { AdminLayout } from '../../components/AdminLayout';
import { useToast } from '../../hooks/use-toast';

interface CrawlTask {
  task_id: string;
  status: string;
  keywords: string[];
  max_count: number;
  crawled_count: number;
  data: any[];
}

export const XiaohongshuPage: React.FC = () => {
  const [tasks, setTasks] = useState<CrawlTask[]>([]);
  const [keywords, setKeywords] = useState<string>('');
  const [maxCount, setMaxCount] = useState<number>(100);
  const [loading, setLoading] = useState(false);
  const { success, error } = useToast();

  const handleCreateTask = async () => {
    if (!keywords.trim()) {
      error('输入错误', '请输入关键词');
      return;
    }

    setLoading(true);
    try {
      const keywordList = keywords.split(',').map(k => k.trim()).filter(k => k);
      
      // 模拟API调用
      const newTask: CrawlTask = {
        task_id: `task_${Date.now()}`,
        status: 'running',
        keywords: keywordList,
        max_count: maxCount,
        crawled_count: 0,
        data: []
      };
      
      setTasks([newTask, ...tasks]);
      setKeywords('');
      success('任务创建成功', `已开始采集关键词: ${keywordList.join(', ')}`);
      
      // 模拟进度更新
      simulateProgress(newTask.task_id);
    } catch (err) {
      error('创建失败', '无法创建采集任务');
    } finally {
      setLoading(false);
    }
  };

  const simulateProgress = (taskId: string) => {
    const interval = setInterval(() => {
      setTasks(prevTasks => {
        const updatedTasks = prevTasks.map(task => {
          if (task.task_id === taskId && task.status === 'running') {
            const newCount = Math.min(task.crawled_count + 10, task.max_count);
            return {
              ...task,
              crawled_count: newCount,
              status: newCount >= task.max_count ? 'completed' : 'running'
            };
          }
          return task;
        });
        return updatedTasks;
      });
    }, 2000);

    // 停止模拟
    setTimeout(() => clearInterval(interval), 30000);
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'running':
        return <Badge className="bg-blue-100 text-blue-700">采集中</Badge>;
      case 'completed':
        return <Badge className="bg-emerald-100 text-emerald-700">已完成</Badge>;
      case 'failed':
        return <Badge className="bg-rose-100 text-rose-700">失败</Badge>;
      default:
        return <Badge className="bg-slate-100 text-slate-700">{status}</Badge>;
    }
  };

  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">小红书采集管理</h2>
            <p className="text-slate-500 mt-1">采集小红书平台评价数据</p>
          </div>
          <Button 
            className="bg-rose-600 hover:bg-rose-700 text-white gap-2"
            onClick={handleCreateTask}
            disabled={loading}
          >
            <RefreshCw className="w-4 h-4" />
            创建采集任务
          </Button>
        </div>

        {/* 创建任务表单 */}
        <Card className="p-6">
          <h3 className="text-lg font-bold mb-4">新建采集任务</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                关键词（用逗号分隔）
              </label>
              <input
                type="text"
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
                placeholder="例如：美食,餐厅,评价"
                className="w-full p-2 border border-slate-200 rounded-md"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                最大采集数量
              </label>
              <input
                type="number"
                value={maxCount}
                onChange={(e) => setMaxCount(parseInt(e.target.value))}
                min={10}
                max={1000}
                className="w-full p-2 border border-slate-200 rounded-md"
              />
            </div>
            <Button 
              className="bg-rose-600 hover:bg-rose-700 text-white gap-2"
              onClick={handleCreateTask}
              disabled={loading}
            >
              <Search className="w-4 h-4" />
              开始采集
            </Button>
          </div>
        </Card>

        {/* 任务列表 */}
        <div className="space-y-4">
          <h3 className="text-lg font-bold">采集任务列表</h3>
          
          {tasks.length === 0 ? (
            <Card className="p-8 text-center">
              <BarChart3 className="w-12 h-12 text-slate-300 mx-auto mb-4" />
              <p className="text-slate-500">暂无采集任务</p>
              <p className="text-sm text-slate-400 mt-1">点击"创建采集任务"开始采集小红书数据</p>
            </Card>
          ) : (
            tasks.map(task => (
              <Card key={task.task_id} className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h4 className="font-bold">任务 ID: {task.task_id}</h4>
                    <p className="text-sm text-slate-500">
                      关键词: {task.keywords.join(', ')}
                    </p>
                  </div>
                  {getStatusBadge(task.status)}
                </div>
                
                {/* 进度条 */}
                <div className="mb-4">
                  <div className="flex justify-between text-sm text-slate-600 mb-1">
                    <span>采集进度</span>
                    <span>{task.crawled_count} / {task.max_count}</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2.5">
                    <div 
                      className="bg-rose-600 h-full rounded-full transition-all duration-500"
                      style={{ width: `${(task.crawled_count / task.max_count) * 100}%` }}
                    ></div>
                  </div>
                </div>
                
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" className="gap-1">
                    <Download className="w-3.5 h-3.5" />
                    导出数据
                  </Button>
                  <Button variant="outline" size="sm" className="gap-1">
                    <BarChart3 className="w-3.5 h-3.5" />
                    查看数据
                  </Button>
                </div>
              </Card>
            ))
          )}
        </div>
      </div>
    </AdminLayout>
  );
};

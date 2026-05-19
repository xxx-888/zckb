import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, HelpCircle, Book, Video, MessageCircle, ChevronRight, Search } from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';

export const HelpCenter: React.FC = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  
  const helpCategories = [
    {
      icon: '📖',
      title: '快速入门',
      items: [
        '如何添加店铺',
        '如何查看评价',
        '如何设置自动回复',
        '如何导出数据'
      ]
    },
    {
      icon: '⚙️',
      title: '功能指南',
      items: [
        'AI分析功能详解',
        '竞品对标使用教程',
        '小红书数据采集指南',
        '多平台账号关联'
      ]
    },
    {
      icon: '❓',
      title: '常见问题',
      items: [
        '为什么收不到通知',
        '如何修改密码',
        '数据同步失败怎么办',
        '如何升级版本'
      ]
    }
  ];

  const filteredCategories = helpCategories.map(category => ({
    ...category,
    items: category.items.filter(item => 
      item.toLowerCase().includes(searchQuery.toLowerCase())
    )
  })).filter(category => category.items.length > 0);

  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      {/* Header */}
      <div className="bg-white px-6 py-4 flex items-center gap-4 shadow-sm">
        <button 
          onClick={() => navigate('/mobile/settings')}
          className="text-slate-600 hover:bg-slate-100 p-2 rounded-xl transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <h1 className="text-lg font-bold text-slate-900">帮助中心</h1>
      </div>

      <div className="p-6 space-y-6">
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input 
            type="text" 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="搜索帮助文档..."
            className="w-full bg-white border border-slate-200 rounded-2xl py-4 pl-12 pr-4 focus:ring-2 focus:ring-indigo-600 focus:border-transparent transition-all outline-none text-sm"
          />
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-3 gap-3">
          <button className="bg-white rounded-2xl p-4 shadow-sm space-y-2 hover:bg-slate-50 transition-colors">
            <Book className="w-6 h-6 text-indigo-600 mx-auto" />
            <p className="text-xs font-bold text-slate-700">使用文档</p>
          </button>
          <button className="bg-white rounded-2xl p-4 shadow-sm space-y-2 hover:bg-slate-50 transition-colors">
            <Video className="w-6 h-6 text-rose-600 mx-auto" />
            <p className="text-xs font-bold text-slate-700">视频教程</p>
          </button>
          <button className="bg-white rounded-2xl p-4 shadow-sm space-y-2 hover:bg-slate-50 transition-colors">
            <MessageCircle className="w-6 h-6 text-green-600 mx-auto" />
            <p className="text-xs font-bold text-slate-700">联系客服</p>
          </button>
        </div>

        {/* Help Categories */}
        <div className="space-y-4">
          {filteredCategories.map((category, idx) => (
            <div key={idx} className="space-y-3">
              <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-1 flex items-center gap-2">
                <span className="text-base">{category.icon}</span>
                {category.title}
              </h4>
              <div className="bg-white rounded-2xl overflow-hidden shadow-sm">
                <div className="divide-y divide-slate-50">
                  {category.items.map((item, itemIdx) => (
                    <button 
                      key={itemIdx}
                      className="w-full flex items-center justify-between p-4 active:bg-slate-50 transition-colors"
                    >
                      <span className="text-sm text-slate-700">{item}</span>
                      <ChevronRight className="w-4 h-4 text-slate-300" />
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Contact Support */}
        <Card className="p-6 border-slate-100 shadow-sm bg-white">
          <div className="w-12 h-12 rounded-xl bg-orange-50 flex items-center justify-center mb-4">
            <HelpCircle className="w-6 h-6 text-orange-500" />
          </div>
          <h3 className="font-bold text-lg text-slate-900 mb-2">需要更多帮助？</h3>
          <p className="text-sm text-slate-400 mb-4">我们的客服团队随时为您服务</p>
          <Button 
            className="bg-orange-50 hover:bg-orange-100 text-orange-600 border-orange-200"
          >
            联系在线客服
          </Button>
        </Card>

        {/* Version Info */}
        <p className="text-center text-[10px] text-slate-300 font-medium">
          智策口碑 移动端 v2.4.0 (20260514)
        </p>
      </div>
    </div>
  );
};

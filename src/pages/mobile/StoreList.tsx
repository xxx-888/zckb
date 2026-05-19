import React, { useState } from 'react';
import { 
  Store, 
  Search, 
  ChevronRight, 
  TrendingUp, 
  Star,
  MapPin,
  Activity,
  ArrowLeft
} from 'lucide-react';
import { Card } from '../../components/ui/card';
import { Badge } from '../../components/ui/badge';
import { Button } from '../../components/ui/button';
import { MobileLayout } from '../../components/MobileLayout';
import { cn } from '../../lib/utils';
import { useToast } from '../../hooks/use-toast';
import { useNavigate } from 'react-router-dom';

export const StoreList: React.FC = () => {
  const { success } = useToast();
  const navigate = useNavigate();
  const [searchKeyword, setSearchKeyword] = useState('');

  const stores = [
    { id: 1, name: '王府井总店', score: 4.9, reviews: 120, health: 98, trend: 'up', address: '北京市东城区王府井大街88号', platformCount: 4 },
    { id: 2, name: '三里屯店', score: 4.8, reviews: 85, health: 95, trend: 'up', address: '北京市朝阳区三里屯路12号', platformCount: 4 },
    { id: 3, name: '天河城店', score: 4.7, reviews: 64, health: 88, trend: 'down', address: '广州市天河区天河城购物中心3楼', platformCount: 3 },
    { id: 4, name: '南京路店', score: 4.6, reviews: 92, health: 92, trend: 'up', address: '上海市黄浦区南京东路168号', platformCount: 4 },
    { id: 5, name: '春熙路店', score: 4.5, reviews: 78, health: 90, trend: 'stable', address: '成都市锦江区春熙路88号', platformCount: 3 },
  ];

  const filteredStores = stores.filter(store => 
    store.name.toLowerCase().includes(searchKeyword.toLowerCase())
  );

  const handleStoreClick = (storeId: number, storeName: string) => {
    success('门店详情', `正在查看"${storeName}"的详细数据...`);
    navigate(`/mobile/store-detail/${storeId}`);
  };

  const handleBack = () => {
    navigate('/mobile/dashboard');
  };

  return (
    <MobileLayout title="门店列表">
      <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500 pb-20">
        
        {/* Search Bar */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            placeholder="搜索门店名称..."
            value={searchKeyword}
            onChange={(e) => setSearchKeyword(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-100 rounded-2xl text-sm focus:outline-none focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all"
          />
        </div>

        {/* Stats Summary */}
        <div className="bg-white p-4 rounded-2xl shadow-sm border border-slate-100">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-bold text-slate-800 flex items-center gap-2">
              <Store className="w-4 h-4 text-orange-500" />
              全部门店
            </h3>
            <Badge variant="outline" className="text-[10px] border-slate-100 bg-slate-50 text-slate-500">
              {filteredStores.length} 家门店
            </Badge>
          </div>
          <div className="grid grid-cols-3 gap-2">
            <div className="text-center p-2 bg-orange-50 rounded-xl">
              <div className="text-lg font-bold text-orange-600">{stores.length}</div>
              <div className="text-[9px] text-orange-600/70 font-medium">门店总数</div>
            </div>
            <div className="text-center p-2 bg-emerald-50 rounded-xl">
              <div className="text-lg font-bold text-emerald-600">4.7</div>
              <div className="text-[9px] text-emerald-600/70 font-medium">平均评分</div>
            </div>
            <div className="text-center p-2 bg-blue-50 rounded-xl">
              <div className="text-lg font-bold text-blue-600">439</div>
              <div className="text-[9px] text-blue-600/70 font-medium">总评论数</div>
            </div>
          </div>
        </div>

        {/* Store List */}
        <div className="space-y-3">
          {filteredStores.map((store) => (
            <Card 
              key={store.id}
              className="p-4 border-none shadow-sm bg-white cursor-pointer hover:shadow-md transition-all active:bg-slate-50"
              onClick={() => handleStoreClick(store.id, store.name)}
            >
              <div className="flex items-start justify-between">
                <div className="flex gap-3 flex-1">
                  <div className="w-12 h-12 rounded-2xl bg-orange-50 flex items-center justify-center flex-shrink-0">
                    <Store className="w-6 h-6 text-orange-500" />
                  </div>
                  <div className="flex flex-col flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <h4 className="text-sm font-bold text-slate-800">{store.name}</h4>
                      {store.trend === 'up' ? (
                        <TrendingUp className="w-3.5 h-3.5 text-emerald-500" />
                      ) : store.trend === 'down' ? (
                        <TrendingUp className="w-3.5 h-3.5 text-rose-500 rotate-180" />
                      ) : (
                        <div className="w-3.5 h-3.5 rounded-full border-2 border-slate-300"></div>
                      )}
                    </div>
                    <div className="flex items-center gap-1 mb-2">
                      <MapPin className="w-3 h-3 text-slate-400" />
                      <span className="text-[10px] text-slate-500 line-clamp-1">{store.address}</span>
                    </div>
                    <div className="flex items-center gap-3 flex-wrap">
                      <div className="flex items-center gap-1">
                        <Star className="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
                        <span className="text-xs font-bold text-slate-700">{store.score}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Activity className="w-3.5 h-3.5 text-blue-400" />
                        <span className="text-[10px] text-slate-500">{store.reviews} 评论</span>
                      </div>
                      <Badge 
                        className={cn(
                          "text-[9px] px-1.5 h-4 border-none",
                          store.health >= 95 ? "bg-emerald-100 text-emerald-700" :
                          store.health >= 90 ? "bg-orange-100 text-orange-700" :
                          "bg-rose-100 text-rose-700"
                        )}
                      >
                        健康值 {store.health}
                      </Badge>
                    </div>
                  </div>
                </div>
                <ChevronRight className="w-5 h-5 text-slate-300 flex-shrink-0 ml-2" />
              </div>
            </Card>
          ))}
        </div>

        {filteredStores.length === 0 && (
          <div className="text-center py-12">
            <Store className="w-12 h-12 text-slate-200 mx-auto mb-3" />
            <p className="text-sm text-slate-400">未找到匹配的门店</p>
          </div>
        )}
      </div>
    </MobileLayout>
  );
};

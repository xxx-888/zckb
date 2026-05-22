import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { storesApi, Store } from '../api/stores';
import { useToast } from '../hooks/use-toast';

interface StoreContextType {
  stores: Store[];
  selectedStoreId: string;
  setSelectedStoreId: (storeId: string) => void;
  loading: boolean;
  currentStore: Store | undefined;
}

const StoreContext = createContext<StoreContextType | undefined>(undefined);

export const StoreProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [stores, setStores] = useState<Store[]>([]);
  const [selectedStoreId, setSelectedStoreId] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const { success } = useToast();

  useEffect(() => {
    const fetchStores = async () => {
      try {
        setLoading(true);
        console.log('[StoreContext] 开始获取店铺列表...');
        const response = await storesApi.getStores({ page: 1, page_size: 100 });
        console.log('[StoreContext] API 响应:', response);
        const storeList = response.items || [];
        console.log('[StoreContext] 获取到店铺数量:', storeList.length);
        setStores(storeList);
        
        // 默认选中第一个店铺
        if (storeList.length > 0 && !selectedStoreId) {
          console.log('[StoreContext] 默认选中店铺:', storeList[0].id, storeList[0].name);
          setSelectedStoreId(storeList[0].id);
        } else if (storeList.length === 0) {
          console.warn('[StoreContext] 没有获取到店铺数据！');
        }
      } catch (err) {
        console.error('[StoreContext] 获取店铺列表失败:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchStores();
  }, []);

  const handleSetSelectedStoreId = (storeId: string) => {
    setSelectedStoreId(storeId);
    const store = stores.find(s => s.id === storeId);
    success('切换店铺', `已切换到「${store?.name || '未知店铺'}」`);
  };

  const currentStore = stores.find(s => s.id === selectedStoreId);

  return (
    <StoreContext.Provider
      value={{
        stores,
        selectedStoreId,
        setSelectedStoreId: handleSetSelectedStoreId,
        loading,
        currentStore,
      }}
    >
      {children}
    </StoreContext.Provider>
  );
};

export const useStore = (): StoreContextType => {
  const context = useContext(StoreContext);
  if (context === undefined) {
    throw new Error('useStore must be used within a StoreProvider');
  }
  return context;
};

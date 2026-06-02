import React, { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import { storesApi, Store } from '../api/stores';
import { useToast } from '../hooks/use-toast';

interface StoreContextType {
  stores: Store[];
  selectedStoreId: string;
  setSelectedStoreId: (storeId: string) => void;
  loading: boolean;
  currentStore: Store | undefined;
  refresh: () => void;
}

const StoreContext = createContext<StoreContextType | undefined>(undefined);

export const StoreProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [stores, setStores] = useState<Store[]>([]);
  const [selectedStoreId, setSelectedStoreId] = useState<string>(() => localStorage.getItem('zc_selected_store_id') || '');
  const [loading, setLoading] = useState(true);
  const { success } = useToast();

  const fetchStores = useCallback(async () => {
    try {
      setLoading(true);
      const response = await storesApi.getStores({ page: 1, page_size: 100 });
      const storeList = response.items || [];
      setStores(storeList);
    } catch (err) {
      console.error('[StoreContext] 获取店铺列表失败:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStores();
  }, [fetchStores]);

  // 页面从后台切回前台时自动刷新店铺列表
  useEffect(() => {
    const handleVisibility = () => {
      if (!document.hidden) {
        fetchStores();
      }
    };
    document.addEventListener('visibilitychange', handleVisibility);
    return () => document.removeEventListener('visibilitychange', handleVisibility);
  }, [fetchStores]);

  // 当店铺列表加载完成且没有选中店铺时，自动选中第一个（或 localStorage 中保存的）
  useEffect(() => {
    if (stores.length > 0 && !selectedStoreId) {
      const savedId = localStorage.getItem('zc_selected_store_id');
      const targetStore = savedId ? stores.find(s => s.id === savedId) : null;
      const targetId = targetStore ? targetStore.id : stores[0].id;
      setSelectedStoreId(targetId);
      localStorage.setItem('zc_selected_store_id', targetId);
    }
  }, [stores, selectedStoreId]);

  const handleSetSelectedStoreId = (storeId: string) => {
    setSelectedStoreId(storeId);
    localStorage.setItem('zc_selected_store_id', storeId);
    const store = stores.find(s => s.id === storeId);
    success('切换店铺', `已切换到「${store?.name || '未知店铺'}」`);
    window.dispatchEvent(new CustomEvent('zc-store-changed', { detail: store }));
  };

  const currentStore = stores.find(s => s.id === selectedStoreId);

  const refresh = useCallback(() => {
    fetchStores();
  }, [fetchStores]);

  return (
    <StoreContext.Provider
      value={{
        stores,
        selectedStoreId,
        setSelectedStoreId: handleSetSelectedStoreId,
        loading,
        currentStore,
        refresh,
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

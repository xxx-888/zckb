import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Store, MapPin, Phone, Mail, Upload, Check, Loader2 } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';
import { storesApi } from '../../api/stores';

export const StoreSettings: React.FC = () => {
  const navigate = useNavigate();
  const { success, error } = useToast();
  
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [storeId, setStoreId] = useState<string | null>(null);
  
  const [formData, setFormData] = useState({
    storeName: '',
    address: '',
    phone: '',
    email: '',
    description: ''
  });

  // 获取选中的门店ID并加载数据
  useEffect(() => {
    const storedStoreId = localStorage.getItem('zc_selected_store_id');
    if (!storedStoreId) {
      error('未选择门店', '请先在首页选择门店');
      setLoading(false);
      return;
    }
    
    setStoreId(storedStoreId);
    loadStoreInfo(storedStoreId);
  }, []);

  const loadStoreInfo = async (id: string) => {
    try {
      setLoading(true);
      const store = await storesApi.getStoreById(id);
      setFormData({
        storeName: store.name || '',
        address: store.address || '',
        phone: store.phone || '',
        email: store.email || '',
        description: store.description || ''
      });
    } catch (err: any) {
      error('加载失败', err.message || '无法获取门店信息');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    if (!formData.storeName.trim()) {
      error('请输入店铺名称', '店铺名称不能为空');
      return;
    }
    
    if (!storeId) {
      error('未选择门店', '请先在首页选择门店');
      return;
    }
    
    try {
      setSaving(true);
      await storesApi.updateStore(storeId, {
        name: formData.storeName,
        address: formData.address,
        phone: formData.phone,
        email: formData.email,
        description: formData.description
      });
      success('保存成功', '店铺信息已更新');
      setTimeout(() => navigate('/mobile/settings'), 1000);
    } catch (err: any) {
      error('保存失败', err.message || '更新门店信息时出现错误');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-indigo-600 animate-spin" />
      </div>
    );
  }

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
        <h1 className="text-lg font-bold text-slate-900">店铺信息设置</h1>
      </div>

      <div className="p-6 space-y-6">
        {/* Store Logo */}
        <div className="text-center mb-8">
          <div className="relative inline-block">
            <div className="w-24 h-24 bg-slate-200 rounded-2xl flex items-center justify-center">
              <Store className="w-12 h-12 text-slate-400" />
            </div>
            <button className="absolute bottom-0 right-0 bg-indigo-600 text-white p-2 rounded-xl shadow-lg">
              <Upload className="w-4 h-4" />
            </button>
          </div>
          <p className="text-xs text-slate-400 mt-2">点击上传店铺Logo</p>
        </div>

        {/* Form */}
        <div className="space-y-4">
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">店铺名称</label>
            <input 
              type="text" 
              value={formData.storeName}
              onChange={(e) => handleInputChange('storeName', e.target.value)}
              className="w-full bg-white border border-slate-200 rounded-2xl py-4 px-4 focus:ring-2 focus:ring-indigo-600 focus:border-transparent transition-all outline-none text-sm"
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              <MapPin className="w-3 h-3 inline mr-1" />
              店铺地址
            </label>
            <input 
              type="text" 
              value={formData.address}
              onChange={(e) => handleInputChange('address', e.target.value)}
              className="w-full bg-white border border-slate-200 rounded-2xl py-4 px-4 focus:ring-2 focus:ring-indigo-600 focus:border-transparent transition-all outline-none text-sm"
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              <Phone className="w-3 h-3 inline mr-1" />
              联系电话
            </label>
            <input 
              type="tel" 
              value={formData.phone}
              onChange={(e) => handleInputChange('phone', e.target.value)}
              className="w-full bg-white border border-slate-200 rounded-2xl py-4 px-4 focus:ring-2 focus:ring-indigo-600 focus:border-transparent transition-all outline-none text-sm"
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              <Mail className="w-3 h-3 inline mr-1" />
              联系邮箱
            </label>
            <input 
              type="email" 
              value={formData.email}
              onChange={(e) => handleInputChange('email', e.target.value)}
              className="w-full bg-white border border-slate-200 rounded-2xl py-4 px-4 focus:ring-2 focus:ring-indigo-600 focus:border-transparent transition-all outline-none text-sm"
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">店铺简介</label>
            <textarea 
              value={formData.description}
              onChange={(e) => handleInputChange('description', e.target.value)}
              rows={4}
              className="w-full bg-white border border-slate-200 rounded-2xl py-4 px-4 focus:ring-2 focus:ring-indigo-600 focus:border-transparent transition-all outline-none text-sm resize-none"
            />
          </div>
        </div>

        {/* Save Button */}
        <Button 
          onClick={handleSave}
          disabled={saving}
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-7 text-lg font-bold shadow-xl shadow-indigo-100 mt-6 disabled:opacity-50"
        >
          {saving ? (
            <>
              <Loader2 className="w-5 h-5 mr-2 animate-spin" />
              保存中...
            </>
          ) : (
            <>
              <Check className="w-5 h-5 mr-2" />
              保存修改
            </>
          )}
        </Button>
      </div>
    </div>
  );
};

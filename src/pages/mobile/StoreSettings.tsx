import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Store, MapPin, Phone, Mail, Upload, Check } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';

export const StoreSettings: React.FC = () => {
  const navigate = useNavigate();
  const { success, error } = useToast();
  
  const [formData, setFormData] = useState({
    storeName: '香格里拉大酒店',
    address: '北京市朝阳区建国门外大街1号',
    phone: '010-88888888',
    email: 'service@shangri-la.com',
    description: '豪华五星级酒店，提供顶级服务体验'
  });

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = () => {
    if (!formData.storeName.trim()) {
      error('请输入店铺名称', '店铺名称不能为空');
      return;
    }
    success('保存成功', '店铺信息已更新');
    setTimeout(() => navigate('/mobile/settings'), 1000);
  };

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
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-7 text-lg font-bold shadow-xl shadow-indigo-100 mt-6"
        >
          <Check className="w-5 h-5 mr-2" />
          保存修改
        </Button>
      </div>
    </div>
  );
};

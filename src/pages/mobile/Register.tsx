import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Store, User, Phone, Lock, Shield, CheckCircle2, AlertCircle } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';
import { authApi } from '../../api/auth';

export const Register: React.FC = () => {
  const navigate = useNavigate();
  const { success, error } = useToast();
  
  const [formData, setFormData] = useState({
    storeName: '',
    contactName: '',
    phone: '',
    verifyCode: '',
    password: '',
    confirmPassword: '',
    agreeTerms: false
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [codeLoading, setCodeLoading] = useState(false);
  const [countdown, setCountdown] = useState(0);

  const handleInputChange = (field: string, value: string | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSendCode = async () => {
    if (!formData.phone.trim()) {
      error('请输入手机号', '手机号不能为空');
      return;
    }

    if (!/^1[3-9]\d{9}$/.test(formData.phone)) {
      error('手机号格式错误', '请输入正确的手机号码');
      return;
    }

    setCodeLoading(true);
    
    try {
      await authApi.sendRegisterCode(formData.phone);
      success('验证码已发送', `验证码已发送到 ${formData.phone}`);
      
      setCountdown(60);
      const timer = setInterval(() => {
        setCountdown(prev => {
          if (prev <= 1) {
            clearInterval(timer);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    } catch (err: any) {
      const errorMessage = err.backendMessage || err.message || '验证码发送失败';
      console.error('Send code error:', { message: errorMessage, response: err.response?.data });
      error('发送失败', errorMessage);
    } finally {
      setCodeLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();

    // 表单验证
    if (!formData.storeName.trim()) {
      error('请输入商家名称', '商家名称不能为空');
      return;
    }

    if (!formData.contactName.trim()) {
      error('请输入联系人姓名', '联系人姓名不能为空');
      return;
    }

    if (!formData.phone.trim()) {
      error('请输入手机号', '手机号不能为空');
      return;
    }

    if (!/^1[3-9]\d{9}$/.test(formData.phone)) {
      error('手机号格式错误', '请输入正确的手机号码');
      return;
    }

    if (!formData.verifyCode.trim()) {
      error('请输入验证码', '验证码不能为空');
      return;
    }

    if (!formData.password) {
      error('请输入密码', '密码不能为空');
      return;
    }

    if (formData.password.length < 6) {
      error('密码长度不足', '密码长度不能少于6位');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      error('密码不一致', '两次输入的密码不一致');
      return;
    }

    if (!formData.agreeTerms) {
      error('请同意用户协议', '请勾选同意用户协议和隐私政策');
      return;
    }

    setLoading(true);

    try {
      // 调用后端注册API
      const registerData = {
        phone: formData.phone.trim(),
        username: formData.contactName.trim(),
        password: formData.password,
        verifyCode: formData.verifyCode,
        password_confirm: formData.confirmPassword,
      };
      
      await authApi.register(registerData);
      success('注册成功', '欢迎入驻智策口碑！即将跳转到登录页面...');
      
      setTimeout(() => {
        navigate('/mobile/login');
      }, 2000);
    } catch (err: any) {
      // 优先使用后端返回的错误信息
      const errorMessage = err.backendMessage || err.message || '注册失败，请重试';
      console.error('Register error:', { message: errorMessage, response: err.response?.data });
      error('注册失败', errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex flex-col font-sans">
      {/* Header */}
      <div className="bg-indigo-600 px-6 py-4 flex items-center gap-4">
        <button 
          onClick={() => navigate('/mobile/login')}
          className="text-white hover:bg-white/10 p-2 rounded-xl transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <h1 className="text-lg font-bold text-white">商家入驻</h1>
      </div>

      {/* Registration Form */}
      <div className="flex-1 px-6 py-8">
        <form onSubmit={handleRegister} className="space-y-5">
          <div className="space-y-1 mb-6">
            <h2 className="text-xl font-black text-slate-900">创建商家账号</h2>
            <p className="text-sm text-slate-400">填写基本信息，开启智能口碑管理</p>
          </div>

          {/* 商家名称 */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">商家名称</label>
            <div className="relative">
              <Store className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input 
                type="text" 
                value={formData.storeName}
                onChange={(e) => handleInputChange('storeName', e.target.value)}
                placeholder="请输入商家名称"
                className="w-full bg-slate-50 border-none rounded-2xl py-4 pl-12 pr-4 focus:ring-2 focus:ring-indigo-600 transition-all outline-none text-sm"
              />
            </div>
          </div>

          {/* 联系人姓名 */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">联系人姓名</label>
            <div className="relative">
              <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input 
                type="text" 
                value={formData.contactName}
                onChange={(e) => handleInputChange('contactName', e.target.value)}
                placeholder="请输入联系人姓名"
                className="w-full bg-slate-50 border-none rounded-2xl py-4 pl-12 pr-4 focus:ring-2 focus:ring-indigo-600 transition-all outline-none text-sm"
              />
            </div>
          </div>

          {/* 手机号 + 验证码按钮 */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">手机号码</label>
            <div className="flex gap-3">
              <div className="relative flex-1">
                <Phone className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input 
                  type="tel" 
                  value={formData.phone}
                  onChange={(e) => handleInputChange('phone', e.target.value.replace(/\D/g, '').slice(0, 11))}
                  placeholder="请输入手机号"
                  maxLength={11}
                  className="w-full bg-slate-50 border-none rounded-2xl py-4 pl-12 pr-4 focus:ring-2 focus:ring-indigo-600 transition-all outline-none text-sm"
                />
              </div>
              <Button
                type="button"
                onClick={handleSendCode}
                disabled={codeLoading || countdown > 0}
                className="whitespace-nowrap bg-indigo-50 text-indigo-600 hover:bg-indigo-100 rounded-2xl px-6 text-sm font-bold disabled:opacity-50"
              >
                {countdown > 0 ? `${countdown}s` : codeLoading ? '发送中...' : '获取验证码'}
              </Button>
            </div>
          </div>

          {/* 验证码 */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">验证码</label>
            <div className="relative">
              <Shield className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input 
                type="text" 
                value={formData.verifyCode}
                onChange={(e) => handleInputChange('verifyCode', e.target.value)}
                placeholder="请输入验证码"
                maxLength={6}
                className="w-full bg-slate-50 border-none rounded-2xl py-4 pl-12 pr-4 focus:ring-2 focus:ring-indigo-600 transition-all outline-none text-sm tracking-widest font-bold"
              />
            </div>
          </div>

          {/* 密码 */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">设置密码</label>
            <div className="relative">
              <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input 
                  type={showPassword ? "text" : "password"}
                  value={formData.password}
                  onChange={(e) => handleInputChange('password', e.target.value.slice(0, 20))}
                  placeholder="请设置登录密码（至少6位）"
                  maxLength={20}
                  className="w-full bg-slate-50 border-none rounded-2xl py-4 pl-12 pr-12 focus:ring-2 focus:ring-indigo-600 transition-all outline-none text-sm"
                />
              <button 
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
              >
                {showPassword ? <AlertCircle className="w-5 h-5" /> : <Shield className="w-5 h-5" />}
              </button>
            </div>
          </div>

          {/* 确认密码 */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">确认密码</label>
            <div className="relative">
              <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input 
                  type={showConfirmPassword ? "text" : "password"}
                  value={formData.confirmPassword}
                  onChange={(e) => handleInputChange('confirmPassword', e.target.value.slice(0, 20))}
                  placeholder="请再次输入密码"
                  maxLength={20}
                  className="w-full bg-slate-50 border-none rounded-2xl py-4 pl-12 pr-12 focus:ring-2 focus:ring-indigo-600 transition-all outline-none text-sm"
                />
              <button 
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
              >
                {showConfirmPassword ? <AlertCircle className="w-5 h-5" /> : <Shield className="w-5 h-5" />}
              </button>
            </div>
          </div>

          {/* 同意协议 */}
          <div className="flex items-start gap-3 pt-2">
            <button
              type="button"
              onClick={() => handleInputChange('agreeTerms', !formData.agreeTerms)}
              className="mt-0.5 flex-shrink-0"
            >
              {formData.agreeTerms ? (
                <CheckCircle2 className="w-5 h-5 text-indigo-600" />
              ) : (
                <div className="w-5 h-5 rounded-full border-2 border-slate-300" />
              )}
            </button>
            <p className="text-xs text-slate-500 leading-relaxed">
              我已阅读并同意 <span className="text-indigo-600 font-bold">《用户服务协议》</span> 和 <span className="text-indigo-600 font-bold">《隐私政策》</span>
            </p>
          </div>

          {/* 注册按钮 */}
          <Button 
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-7 text-lg font-bold shadow-xl shadow-indigo-100 disabled:opacity-50 mt-6"
          >
            {loading ? '注册中...' : '立即注册'}
          </Button>

          {/* 返回登录 */}
          <div className="text-center pt-4">
            <p className="text-xs text-slate-400">
              已有账号？ <button 
                type="button" 
                onClick={() => navigate('/mobile/login')}
                className="text-indigo-600 font-bold"
              >立即登录</button>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

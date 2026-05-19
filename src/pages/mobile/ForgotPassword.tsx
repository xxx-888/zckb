import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Phone, Shield, Lock, CheckCircle2, AlertCircle } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';

export const ForgotPassword: React.FC = () => {
  const navigate = useNavigate();
  const { success, error } = useToast();
  
  const [formData, setFormData] = useState({
    phone: '',
    verifyCode: '',
    newPassword: '',
    confirmPassword: ''
  });
  
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [codeLoading, setCodeLoading] = useState(false);
  const [countdown, setCountdown] = useState(0);
  const [step, setStep] = useState(1); // 1: 验证手机号, 2: 重置密码, 3: 完成

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSendCode = () => {
    if (!formData.phone.trim()) {
      error('请输入手机号', '手机号不能为空');
      return;
    }

    if (!/^1[3-9]\d{9}$/.test(formData.phone)) {
      error('手机号格式错误', '请输入正确的手机号码');
      return;
    }

    setCodeLoading(true);
    
    // 模拟发送验证码
    setTimeout(() => {
      setCodeLoading(false);
      success('验证码已发送', `验证码已发送到 ${formData.phone}`);
      
      // 开始倒计时
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
    }, 1000);
  };

  const handleVerifyPhone = (e: React.FormEvent) => {
    e.preventDefault();

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

    setLoading(true);

    // 模拟验证
    setTimeout(() => {
      setLoading(false);
      setStep(2);
      success('验证成功', '请设置新密码');
    }, 1000);
  };

  const handleResetPassword = (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.newPassword) {
      error('请输入新密码', '新密码不能为空');
      return;
    }

    if (formData.newPassword.length < 6) {
      error('密码长度不足', '密码长度不能少于6位');
      return;
    }

    if (formData.newPassword !== formData.confirmPassword) {
      error('密码不一致', '两次输入的密码不一致');
      return;
    }

    setLoading(true);

    // 模拟重置密码
    setTimeout(() => {
      setLoading(false);
      setStep(3);
      success('密码重置成功', '请使用新密码登录');
    }, 1500);
  };

  const handleBackToLogin = () => {
    navigate('/mobile/login');
  };

  return (
    <div className="min-h-screen bg-white flex flex-col font-sans">
      {/* Header */}
      <div className="bg-indigo-600 px-6 py-4 flex items-center gap-4">
        {step !== 3 && (
          <button 
            onClick={() => step === 1 ? navigate('/mobile/login') : setStep(1)}
            className="text-white hover:bg-white/10 p-2 rounded-xl transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
        )}
        <h1 className="text-lg font-bold text-white">
          {step === 1 ? '忘记密码' : step === 2 ? '重置密码' : '完成'}
        </h1>
      </div>

      {/* Progress Steps */}
      <div className="px-6 py-4 bg-indigo-50">
        <div className="flex items-center justify-between max-w-xs mx-auto">
          <div className={`flex items-center justify-center w-8 h-8 rounded-full text-sm font-bold ${
            step >= 1 ? 'bg-indigo-600 text-white' : 'bg-slate-300 text-white'
          }`}>
            1
          </div>
          <div className={`flex-1 h-1 mx-2 ${
            step >= 2 ? 'bg-indigo-600' : 'bg-slate-300'
          }`} />
          <div className={`flex items-center justify-center w-8 h-8 rounded-full text-sm font-bold ${
            step >= 2 ? 'bg-indigo-600 text-white' : 'bg-slate-300 text-white'
          }`}>
            2
          </div>
          <div className={`flex-1 h-1 mx-2 ${
            step >= 3 ? 'bg-indigo-600' : 'bg-slate-300'
          }`} />
          <div className={`flex items-center justify-center w-8 h-8 rounded-full text-sm font-bold ${
            step >= 3 ? 'bg-indigo-600 text-white' : 'bg-slate-300 text-white'
          }`}>
            3
          </div>
        </div>
        <div className="flex justify-between max-w-xs mx-auto mt-2">
          <span className={`text-xs ${step >= 1 ? 'text-indigo-600 font-bold' : 'text-slate-400'}`}>验证身份</span>
          <span className={`text-xs ${step >= 2 ? 'text-indigo-600 font-bold' : 'text-slate-400'}`}>重置密码</span>
          <span className={`text-xs ${step >= 3 ? 'text-indigo-600 font-bold' : 'text-slate-400'}`}>完成</span>
        </div>
      </div>

      {/* Form Content */}
      <div className="flex-1 px-6 py-8">
        {/* Step 1: 验证手机号 */}
        {step === 1 && (
          <form onSubmit={handleVerifyPhone} className="space-y-5 animate-in fade-in duration-300">
            <div className="space-y-1 mb-6">
              <h2 className="text-xl font-black text-slate-900">验证手机号码</h2>
              <p className="text-sm text-slate-400">请输入注册时的手机号，我们将发送验证码</p>
            </div>

            {/* 手机号 */}
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">手机号码</label>
              <div className="relative">
                <Phone className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input 
                  type="tel" 
                  value={formData.phone}
                  onChange={(e) => handleInputChange('phone', e.target.value)}
                  placeholder="请输入注册手机号"
                  maxLength={11}
                  className="w-full bg-slate-50 border-none rounded-2xl py-4 pl-12 pr-4 focus:ring-2 focus:ring-indigo-600 transition-all outline-none text-sm"
                />
              </div>
            </div>

            {/* 验证码 */}
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">验证码</label>
              <div className="flex gap-3">
                <div className="relative flex-1">
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

            {/* 下一步按钮 */}
            <Button 
              type="submit"
              disabled={loading}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-7 text-lg font-bold shadow-xl shadow-indigo-100 disabled:opacity-50 mt-6"
            >
              {loading ? '验证中...' : '下一步'}
            </Button>
          </form>
        )}

        {/* Step 2: 重置密码 */}
        {step === 2 && (
          <form onSubmit={handleResetPassword} className="space-y-5 animate-in fade-in duration-300">
            <div className="space-y-1 mb-6">
              <h2 className="text-xl font-black text-slate-900">设置新密码</h2>
              <p className="text-sm text-slate-400">请设置一个新的登录密码</p>
            </div>

            {/* 新密码 */}
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">新密码</label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input 
                  type={showPassword ? "text" : "password"}
                  value={formData.newPassword}
                  onChange={(e) => handleInputChange('newPassword', e.target.value)}
                  placeholder="请设置新密码（至少6位）"
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

            {/* 确认新密码 */}
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-500 uppercase tracking-wider">确认新密码</label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input 
                  type={showConfirmPassword ? "text" : "password"}
                  value={formData.confirmPassword}
                  onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
                  placeholder="请再次输入新密码"
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

            {/* 重置按钮 */}
            <Button 
              type="submit"
              disabled={loading}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-7 text-lg font-bold shadow-xl shadow-indigo-100 disabled:opacity-50 mt-6"
            >
              {loading ? '重置中...' : '重置密码'}
            </Button>
          </form>
        )}

        {/* Step 3: 完成 */}
        {step === 3 && (
          <div className="text-center animate-in zoom-in duration-500">
            <div className="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <CheckCircle2 className="w-12 h-12 text-green-600" />
            </div>
            <h2 className="text-2xl font-black text-slate-900 mb-2">密码重置成功！</h2>
            <p className="text-sm text-slate-400 mb-8">请使用新密码登录您的账号</p>
            
            <Button 
              onClick={handleBackToLogin}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-7 text-lg font-bold shadow-xl shadow-indigo-100"
            >
              返回登录
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};

import React, { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Brain, Lock, User, ArrowRight, Eye, EyeOff } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';
import { authApi } from '../../api/auth';

export const Login: React.FC = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { success, error } = useToast();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // 表单验证
    if (!phone.trim()) {
      error('请输入账号', '账号不能为空');
      return;
    }
    
    if (!password) {
      error('请输入密码', '密码不能为空');
      return;
    }

    setLoading(true);

    try {
      const response = await authApi.login({
        phone: phone.trim(),
        password: password,
      });
      
      success('登录成功', '欢迎回来！');
      
      // 记住我
      if (rememberMe) {
        localStorage.setItem('rememberedPhone', phone);
      }
      
      // 登录后跳转：优先跳回原页面，否则按角色跳转
      const redirect = searchParams.get('redirect');
      if (redirect) {
        navigate(decodeURIComponent(redirect), { replace: true });
      } else if (response.user.role === 'HQ' || response.user.role === 'OPERATOR') {
        navigate('/mobile/dashboard');
      } else {
        navigate('/mobile/dashboard');
      }
    } catch (err: any) {
      // 优先显示后端返回的错误信息
      const errorMessage = err.backendMessage || err.message || '账号或密码错误';
      console.error('Login error:', {
        message: errorMessage,
        status: err.status,
        response: err.response?.data,
      });
      error('登录失败', errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // 检查是否有记住的账号
  React.useEffect(() => {
    const remembered = localStorage.getItem('rememberedPhone');
    if (remembered) {
      setPhone(remembered);
      setRememberMe(true);
    }
  }, []);

  return (
    <div className="min-h-screen bg-white flex flex-col font-sans">
      {/* Top Graphic */}
      <div className="h-[40vh] bg-indigo-600 rounded-b-[4rem] relative flex items-center justify-center overflow-hidden">
        <div className="absolute top-[-10%] right-[-10%] w-64 h-64 bg-indigo-500 rounded-full opacity-20 blur-3xl"></div>
        <div className="absolute bottom-[-10%] left-[-10%] w-64 h-64 bg-indigo-400 rounded-full opacity-20 blur-3xl"></div>
        
        <div className="text-center z-10 animate-in fade-in zoom-in duration-700">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-white/10 backdrop-blur-md rounded-3xl mb-6 border border-white/20 shadow-2xl">
            <Brain className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-3xl font-black text-white tracking-tight">智策口碑</h1>
          <p className="text-indigo-100 mt-2 font-medium">商家智能口碑管理专家</p>
        </div>
      </div>

      {/* Login Form */}
      <div className="flex-1 px-8 pt-12">
        <form onSubmit={handleLogin} className="space-y-6 animate-in slide-in-from-bottom-8 duration-700 delay-200">
          <div className="space-y-1">
            <h2 className="text-2xl font-black text-slate-900">欢迎回来</h2>
            <p className="text-sm text-slate-400">请登录您的商家账户</p>
          </div>

          <div className="space-y-4 pt-4">
            <div className="space-y-2">
              <div className="relative">
                <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input 
                  type="tel" 
                  value={phone}
                  onChange={(e) => {
                    const value = e.target.value.replace(/\D/g, '').slice(0, 11);
                    setPhone(value);
                  }}
                  placeholder="手机号"
                  maxLength={11}
                  className="w-full bg-slate-50 border-none rounded-2xl py-4 pl-12 pr-4 focus:ring-2 focus:ring-indigo-600 transition-all outline-none"
                />
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input 
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value.slice(0, 20))}
                  placeholder="登录密码"
                  maxLength={20}
                  className="w-full bg-slate-50 border-none rounded-2xl py-4 pl-12 pr-12 focus:ring-2 focus:ring-indigo-600 transition-all outline-none"
                />
                <button 
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>
          </div>
          
          <div className="flex items-center justify-between">
            <label className="flex items-center gap-2 cursor-pointer group">
              <input 
                type="checkbox" 
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="w-4 h-4 rounded border-slate-200 text-indigo-600 focus:ring-indigo-600" 
              />
              <span className="text-xs text-slate-500 group-hover:text-slate-700 transition-colors">记住我</span>
            </label>
            <button 
              type="button" 
              onClick={() => navigate('/mobile/forgot-password')}
              className="text-xs text-indigo-600 hover:text-indigo-700 font-bold"
            >忘记密码?</button>
          </div>
          
          <Button 
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-7 text-lg font-bold shadow-xl shadow-indigo-100 group disabled:opacity-50"
          >
            {loading ? '登录中...' : '登录'}
            {!loading && <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />}
          </Button>
          
          <div className="pt-8 text-center">
            <p className="text-xs text-slate-400">
              还没有账号？ <button 
                type="button" 
                onClick={() => navigate('/mobile/register')}
                className="text-indigo-600 font-bold"
              >立即申请入驻</button>
            </p>
          </div>
        </form>
      </div>

      {/* Admin Link */}
      <div className="pb-8 px-8 text-center">
        <button 
          onClick={() => navigate('/admin')}
          className="text-[10px] text-slate-300 hover:text-slate-500 uppercase tracking-widest font-bold border-t border-slate-50 pt-4 w-full"
        >
          系统管理员入口
        </button>
      </div>
    </div>
  );
};

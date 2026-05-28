import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck, Lock, User, ArrowRight, Eye, EyeOff, Settings2, Loader2 } from 'lucide-react';
import { Button } from '../../components/ui/button';
import { useToast } from '../../hooks/use-toast';
import { authApi } from '../../api/auth';

export const AdminLogin: React.FC = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { success, error: showError } = useToast();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (!username.trim()) {
      setError('请输入管理员账号');
      return;
    }
    
    if (!password) {
      setError('请输入密码');
      return;
    }
    
    setIsLoading(true);
    
    try {
      const result = await authApi.login({ phone: username, password });
      
      // 仅限 SUPER_ADMIN（系统管理员）可登录后台
      const role = result.user.role;
      if (role === 'SUPER_ADMIN') {
        success('登录成功', '正在跳转到管理后台...');
        navigate('/admin/dashboard');
      } else {
        // 非 HQ 角色：提示后自动跳转到移动端
        showError('权限不足', '无后台管理权限，正在跳转到移动端...');
        // 保留登录状态（token 不清除，移动端可用）
        setTimeout(() => {
          navigate('/mobile/dashboard');
        }, 1500);
      }
    } catch (err: any) {
      const msg = err.message || '登录失败';
      setError(msg);
      showError('登录失败', msg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-6 font-sans">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-10 animate-in fade-in zoom-in duration-700">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-amber-500 rounded-3xl shadow-xl shadow-amber-500/20 mb-6">
            <Settings2 className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-3xl font-black text-white tracking-tight">智策口碑</h1>
          <p className="text-slate-400 mt-2 font-medium">系统管理后台 · 管理中心</p>
        </div>

        {/* Login Card */}
        <div className="bg-slate-800 p-8 rounded-[2rem] shadow-2xl border border-slate-700 animate-in slide-in-from-bottom-8 duration-700 delay-200">
          <form onSubmit={handleLogin} className="space-y-6">
            <div className="space-y-2">
              <label className="text-sm font-bold text-slate-300 ml-1">管理员账号</label>
              <div className="relative">
                <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                <input 
                  type="text" 
                  placeholder="请输入后台管理账号"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full bg-slate-900 border-none text-white rounded-2xl py-4 pl-12 pr-4 focus:ring-2 focus:ring-amber-500 transition-all outline-none placeholder:text-slate-600"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-bold text-slate-300 ml-1">登录密码</label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                <input 
                  type={showPassword ? "text" : "password"}
                  placeholder="请输入密码"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-slate-900 border-none text-white rounded-2xl py-4 pl-12 pr-12 focus:ring-2 focus:ring-amber-500 transition-all outline-none placeholder:text-slate-600"
                />
                <button 
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 transition-colors"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between px-1">
              <label className="flex items-center gap-2 cursor-pointer group">
                <input 
                  type="checkbox" 
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="w-4 h-4 rounded border-slate-700 bg-slate-900 text-amber-500 focus:ring-amber-500 focus:ring-offset-slate-800" 
                />
                <span className="text-xs text-slate-400 group-hover:text-slate-300 transition-colors">记住我</span>
              </label>
              <button type="button" className="text-xs text-amber-500 hover:text-amber-400 font-bold" onClick={() => showError('找回密码', '请联系系统管理员重置密码')}>找回密码?</button>
            </div>

            <Button 
              className="w-full bg-amber-500 hover:bg-amber-600 text-white rounded-2xl py-7 text-lg font-bold shadow-lg shadow-amber-500/20 group"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                  登录中...
                </>
              ) : (
                <>
                  登录系统
                  <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                </>
              )}
            </Button>

            {error && (
              <div className="bg-rose-500/10 border border-rose-500/20 rounded-xl p-3 text-rose-400 text-sm text-center">
                {error}
              </div>
            )}
          </form>
        </div>

        {/* Footer */}
        <p className="text-center mt-10 text-slate-500 text-sm">
          © 2026 智策口碑管理系统 · 技术支持
        </p>
      </div>
    </div>
  );
};

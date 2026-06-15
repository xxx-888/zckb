import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

interface MobileGuardProps {
  children: React.ReactNode;
}

/**
 * 移动端路由守卫
 * 检查 auth_token 和 user_info 是否存在，未登录则重定向到登录页
 * 登录页、注册页、忘记密码页等公开页面不需要守卫
 */
export const MobileGuard: React.FC<MobileGuardProps> = ({ children }) => {
  const location = useLocation();
  const token = localStorage.getItem('auth_token');
  const userStr = localStorage.getItem('user_info');

  // 已有有效认证信息，放行
  if (token && userStr) {
    return <>{children}</>;
  }

  // 清除可能残留的不一致数据
  localStorage.removeItem('auth_token');
  localStorage.removeItem('user_info');

  // 未登录，重定向到登录页，并携带原始路径以便登录后回跳
  const returnUrl = encodeURIComponent(location.pathname + location.search);
  return <Navigate to={`/mobile/login?redirect=${returnUrl}`} replace />;
};

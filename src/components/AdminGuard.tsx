import React from 'react';
import { Navigate } from 'react-router-dom';
import { authApi } from '../api/auth';

interface AdminGuardProps {
  children: React.ReactNode;
}

/**
 * 管理后台路由守卫
 * 仅 HQ 和 SUPER_ADMIN 角色可以访问，其他角色重定向到移动端首页
 */
export const AdminGuard: React.FC<AdminGuardProps> = ({ children }) => {
  const user = authApi.getStoredUser();

  // 未登录 → 跳转登录页
  if (!user) {
    return <Navigate to="/admin" replace />;
  }

  // 非 HQ 和 SUPER_ADMIN 角色 → 跳转移动端
  if (!['HQ', 'SUPER_ADMIN'].includes(user.role)) {
    return <Navigate to="/mobile/dashboard" replace />;
  }

  return <>{children}</>;
};

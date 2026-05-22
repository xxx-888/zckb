import { api } from '@/lib/api';

// 类型定义
export interface LoginRequest {
  username_or_phone: string;
  password: string;
}

export interface RegisterRequest {
  phone: string;
  password: string;
  username: string;
  verifyCode: string;
  email?: string;
  password_confirm?: string;
}

export interface UserInfo {
  id: string;
  phone: string;
  email: string | null;
  username: string;
  role: string;
  avatar: string | null;
  status: string;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: UserInfo;
}

// API 函数
export const authApi = {
  // 登录
  login: async (data: { phone: string; password: string }): Promise<AuthResponse> => {
    // 将 phone 映射为 username_or_phone（后端期望的字段名）
    const loginData = {
      username_or_phone: data.phone,
      password: data.password,
    };
    const response = await api.post<any, any>('/v1/auth/login', loginData);
    if (response.code === 200 && response.data) {
      // 保存token
      localStorage.setItem('auth_token', response.data.access_token);
      localStorage.setItem('user_info', JSON.stringify(response.data.user));
      return response.data;
    }
    throw new Error(response.message || '登录失败');
  },

  // 注册
  register: async (data: RegisterRequest): Promise<AuthResponse> => {
    const response = await api.post<any, any>('/v1/auth/register', data);
    if (response.code === 200 && response.data) {
      localStorage.setItem('auth_token', response.data.access_token);
      localStorage.setItem('user_info', JSON.stringify(response.data.user));
      return response.data;
    }
    throw new Error(response.message || '注册失败');
  },

  // 获取当前用户
  getCurrentUser: async (): Promise<UserInfo> => {
    const response = await api.get<any>('/v1/auth/current');
    if (response.code === 200 && response.data) {
      return response.data;
    }
    throw new Error(response.message || '获取用户信息失败');
  },

  // 登出
  logout: async (): Promise<void> => {
    try {
      await api.post('/v1/auth/logout');
    } finally {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_info');
    }
  },

  // 获取本地保存的用户信息
  getStoredUser: (): UserInfo | null => {
    const userStr = localStorage.getItem('user_info');
    return userStr ? JSON.parse(userStr) : null;
  },

  // 检查是否已登录
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('auth_token');
  },

  // 发送注册验证码
  sendRegisterCode: async (phone: string): Promise<void> => {
    const response = await api.post('/v1/auth/register/send-code', { phone });
    if (response.code !== 200) {
      throw new Error(response.message || '发送验证码失败');
    }
  },

  // 发送验证码（忘记密码）
  sendVerifyCode: async (phone: string): Promise<void> => {
    const response = await api.post('/v1/auth/forgot-password/send-code', { phone });
    if (response.code !== 200) {
      throw new Error(response.message || '发送验证码失败');
    }
  },

  // 验证验证码（忘记密码）
  verifyCode: async (phone: string, code: string): Promise<void> => {
    const response = await api.post('/v1/auth/forgot-password/verify-code', { phone, code });
    if (response.code !== 200) {
      throw new Error(response.message || '验证码错误');
    }
  },

  // 重置密码
  resetPassword: async (phone: string, code: string, newPassword: string): Promise<void> => {
    const response = await api.post('/v1/auth/forgot-password/reset', { phone, code, new_password: newPassword });
    if (response.code !== 200) {
      throw new Error(response.message || '重置密码失败');
    }
  },
};

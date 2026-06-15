import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

/**
 * 统一API客户端配置
 * 包含所有请求/响应拦截器、错误处理
 *
 * 请求流程:
 * 1. 前端请求路径: /api/dashboard/xxx
 * 2. Vite代理匹配 /api 前缀，转发到 http://localhost:8000/dashboard/xxx
 * 3. 后端接收 /dashboard/xxx 路由
 */

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

// ═══════════════════════════════════════════════════════════
// 401 处理：防止多个并行 401 响应同时触发多次重定向
// 使用模块级标志位 + 延迟跳转，确保只执行一次清理+跳转
// ═══════════════════════════════════════════════════════════
let isHandling401 = false;

function handle401Unauthorized(responseData?: any) {
  if (isHandling401) return; // 已在处理中，跳过
  isHandling401 = true;

  const message = responseData?.message || '登录已过期，请重新登录';
  console.warn('[API] 401 未授权:', message);

  // 清除本地存储的认证信息
  localStorage.removeItem('auth_token');
  localStorage.removeItem('user_info');

  // 根据当前路径决定跳转到哪个登录页
  const currentPath = window.location.pathname;
  const isAdmin = currentPath.startsWith('/admin');
  const loginPath = isAdmin ? '/admin' : '/mobile/login';

  // 如果当前不在登录页，则跳转
  if (currentPath !== loginPath && currentPath !== '/mobile/login' && currentPath !== '/admin') {
    // 延迟跳转，让其他并行请求的 401 也能被捕获（避免中断）
    setTimeout(() => {
      window.location.href = loginPath;
      // 跳转完成后重置标志位（页面会重新加载，但以防万一）
      setTimeout(() => { isHandling401 = false; }, 1000);
    }, 300);
  } else {
    // 已在登录页，只需重置标志位
    isHandling401 = false;
  }
}

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // 请求拦截器
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('auth_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // 响应拦截器
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        return response.data;
      },
      (error) => {
        const statusCode = error.response?.status;
        const responseData = error.response?.data;
        const suppress404 = error.config?._suppress404;

        // ═══════════════════════════════════════════════
        // 401 未授权：token 过期或无效，清除凭据并重定向到登录页
        // ═══════════════════════════════════════════════
        if (statusCode === 401) {
          handle401Unauthorized(responseData);

          const message = responseData?.message || '登录已过期，请重新登录';
          const err: any = new Error(message);
          err.response = error.response;
          err.status = 401;
          err.isAuthError = true;
          return Promise.reject(err);
        }

        // 402 订阅过期：延迟跳转，避免立即 location.href 中断所有并行请求
        if (statusCode === 402) {
          const message = responseData?.message || '订阅已过期，请续费';
          if (window.location.pathname !== '/mobile/subscription') {
            console.warn('[API] 订阅过期:', message);
            // 延迟跳转，让并行请求先完成
            setTimeout(() => {
              window.location.href = '/mobile/subscription';
            }, 500);
          }
          const err: any = new Error(message);
          err.response = error.response;
          err.status = 402;
          return Promise.reject(err);
        }

        // 404 且标记了 suppress404：不打 error log，直接 reject
        if (suppress404 && statusCode === 404) {
          console.warn(`[API] 404 (suppressed): ${error.config?.url}`);
        } else {
          // FastAPI 422 错误：提取 detail 中的具体校验信息
          let backendMessage = responseData?.message;
          if (!backendMessage && statusCode === 422 && responseData?.detail) {
            const details = Array.isArray(responseData.detail)
              ? responseData.detail.map((d: any) => `${d.loc?.join('.')}: ${d.msg}`).join('; ')
              : JSON.stringify(responseData.detail);
            backendMessage = `参数校验失败: ${details}`;
          }

          const message = backendMessage || `请求失败 (${statusCode || '网络错误'})`;

          console.error('API Error:', {
            url: error.config?.url,
            status: statusCode,
            message: backendMessage,
            data: error.response?.data,
          });

          const err = new Error(message);
          (err as any).response = error.response;
          (err as any).status = statusCode;
          (err as any).backendMessage = backendMessage;

          return Promise.reject(err);
        }

        // suppress404 + 404：构造一个 rejected promise，让 fetchAPI 的 catch 处理
        const err: any = new Error(responseData?.message || 'Not Found');
        err.response = error.response;
        err.status = statusCode;
        return Promise.reject(err);
      }
    );
  }

  // 通用请求方法
  async get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.client.get(url, config);
  }

  async post<T = any, R = any>(url: string, data?: T, config?: AxiosRequestConfig): Promise<R> {
    return this.client.post(url, data, config);
  }

  async put<T = any, R = any>(url: string, data?: T, config?: AxiosRequestConfig): Promise<R> {
    return this.client.put(url, data, config);
  }

  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.client.delete(url, config);
  }

  async patch<T = any, R = any>(url: string, data?: T, config?: AxiosRequestConfig): Promise<R> {
    return this.client.patch(url, data, config);
  }
}

export const api = new ApiClient();

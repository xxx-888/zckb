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

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: BASE_URL,
      timeout: 10000,
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

        // 402 订阅过期：重定向到订阅页面
        if (statusCode === 402) {
          const message = responseData?.message || '订阅已过期，请续费';
          // 避免重复跳转
          if (window.location.pathname !== '/mobile/subscription') {
            // 用 toast 提示（如果可用），然后跳转
            console.warn('[API] 订阅过期:', message);
            window.location.href = '/mobile/subscription';
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

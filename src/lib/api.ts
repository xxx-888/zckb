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
        // 优先使用后端返回的错误信息
        const backendMessage = error.response?.data?.message;
        const statusCode = error.response?.status;
        const message = backendMessage || `请求失败 (${statusCode || '网络错误'})`;
        
        console.error('API Error:', {
          url: error.config?.url,
          status: statusCode,
          message: backendMessage,
          data: error.response?.data,
        });
        
        // 创建一个包含后端错误信息的错误对象
        const err = new Error(message);
        (err as any).response = error.response;
        (err as any).status = statusCode;
        (err as any).backendMessage = backendMessage;
        
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
}

export const api = new ApiClient();

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    host: true,
    proxy: {
      // 代理 /api 请求到后端 FastAPI 服务
      // 前端请求: /api/auth/login
      // 直接转发到: http://localhost:8000/api/auth/login
      // 后端路由已配置 /api 前缀，无需重写
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})

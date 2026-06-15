import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import fs from 'fs'

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
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      }, 
      '/v1': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/v1/, '/api/v1'),
      },
    },
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const url = req.url || '';
        // 必须放行 /api 和 /v1 前缀（代理路径），否则会被 SPA fallback 拦截
        if (url.startsWith('/api') || url.startsWith('/v1') || /\.\w+$/.test(url.split('?')[0])) {
          return next();
        }
        const indexHtml = fs.readFileSync(
          path.resolve(__dirname, 'index.html'),
          'utf-8'
        );
        res.setHeader('Content-Type', 'text/html');
        res.end(indexHtml);
      });
    },
  },
})

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
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
    // SPA fallback: 所有非静态资源请求都返回 index.html
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const url = req.url || '';
        if (url.startsWith('/api') || /\.\w+$/.test(url.split('?')[0])) {
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

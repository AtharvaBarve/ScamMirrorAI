import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'node:path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
    // Serve index.html for all unknown requests to allow client-side routing
    configureServer: (server) => {
      server.middlewares.use((req, res, next) => {
        console.log('Middleware triggered for:', req.method, req.path);
        if (req.method === 'GET' && !req.path.includes('.') && !req.path.startsWith('/api')) {
          console.log('Serving index.html for path:', req.path);
          const indexHtml = path.join(__dirname, 'public', 'index.html');
          return res.sendFile(indexHtml);
        }
        next();
      });
    },
  },
});
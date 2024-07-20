import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5555',
        changeOrigin: true,
        secure: false,
      }
      // "/api": "http://127.0.0.1:5555",
      // '/api': {
      //   target: 'http://localhost:5555',
      //   // changeOrigin: true,
      //   secure: false,
      //   configure: (proxy, options) => {
      //     // proxy will be an instance of 'http-proxy'
      //     proxy.on('error', (err, _req, _res) => {
      //       console.log('proxy error', err);
      //     });
      //     proxy.on('proxyReq', (proxyReq, req, _res) => {
      //       console.log('Sending Request to the Target:', req.method, req.url);
      //     });
      //     proxy.on('proxyRes', (proxyRes, req, _res) => {
      //       console.log('Received Response from the Target:', proxyRes.statusCode, req.url);
      //     });
      //   },
      // }
    }
  }
})

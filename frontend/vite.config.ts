import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig({
  plugins: [vue(), vueJsx(), vueDevTools()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://fastapi-service:8000',
        changeOrigin: true,
        secure: false,
      },
      '/canvas': {
        target: 'http://canvas.docker',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/canvas/, ''),
        secure: false,
      },
      '/gov-api': {
        target: 'https://www.gov.kz',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/gov-api/, ''), // Убираем префикс /gov-api в запросе
        secure: true, // Для безопасного соединения (https)
      },
    },
  },
})

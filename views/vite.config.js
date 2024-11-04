import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@':path.resolve(__dirname, './src')
    }
  },
  optimizeDeps: {
    include: ['axios'], // Asegúrate de incluir Axios para la optimización
  },
  server: {
    proxy: {
      '/auth': {
        target: 'http://localhost:5000', // URL de tu backend Flask
        changeOrigin: true,
      },
    },
  },
})
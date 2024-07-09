/// <reference types="vitest" />
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
let ip = 'http://192.168.2.51:45454/'
// let ip = 'http://192.168.2.139:45454/'

export default defineConfig({
  base: './',
  test: { globals: true, environment: 'jsdom' },
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@components': fileURLToPath(new URL('./src/components', import.meta.url)),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: ip,
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api/, ''), // 不可以省略rewrite
      },
    },
  },
  build: {
    target: 'esnext',
    outDir: 'E:/exploitation/collection/server/static2',
    emptyOutDir: true,
    minify: 'terser',
    terserOptions: {
      compress: {
        //生产环境时移除console
        drop_console: true,
        drop_debugger: true,
      },
    },
  },
})

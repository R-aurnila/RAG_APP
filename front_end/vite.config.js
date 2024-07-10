import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 5173,
    host: true,  // Ensure Vite runs on port 81 inside the container
    strictPort: true,  // Ensure Vite fails if the port is already in use
    hmr: {
      host: 'localhost',  // Host for Hot Module Replacement
    },
  },
})

import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
// import vueDevTools from 'vite-plugin-vue-devtools'
// import Inspector from 'unplugin-vue-inspector/vite' // OR vite-plugin-vue-inspector


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    // vueDevTools({
    //   launchEditor: 'code-insiders',
    // }),
    // Inspector({
    //   enabled: true,
    //   toggleButtonVisibility: 'always',
    //   launchEditor: 'code',
    // })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})

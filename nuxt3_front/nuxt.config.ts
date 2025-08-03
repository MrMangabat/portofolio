import vuetify from 'vite-plugin-vuetify';

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  
    runtimeConfig: {
    // Server-side (SSR) - talks to API Gateway container
    apiBaseUrl: process.env.NUXT_API_BASE_URL,
    // Client-side (CSR) - talks to localhost
    public: {
      // ✅ Put API base in public so it's accessible everywhere
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL
    }
  },

  compatibilityDate: '2025-05-15',
  devtools: { enabled: true },

  css: [
    'vuetify/styles',
    '@mdi/font/css/materialdesignicons.css'
  ],
  build: {
    transpile: ['vuetify']
  },
  vite: {
    define: { 'process.env.DEBUG': false },
    plugins: [
      vuetify({ autoImport: true })
    ]
  },

  modules: [
    // '@nuxt/content',
    '@nuxt/eslint',
    '@nuxt/fonts',
    '@nuxt/icon',
    '@nuxt/image',
    '@nuxt/scripts',
    '@nuxt/test-utils',
    '@nuxt/ui',
    '@pinia/nuxt'
  ]
})
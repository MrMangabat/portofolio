// This is the main entry point for the Vue.js application.
import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue"; // Main component, all other components are nested here
import router from "./router";
import loadConfig from "./config";

// Vuetify
import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { aliases, mdi } from "vuetify/iconsets/mdi";

// Create Vuetify instance
const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: "mdi",
    aliases,
    sets: {
      mdi,
    },
  },
});

// Wait for the config to load BEFORE initializing the Vue app
loadConfig().then((config) => {
  window.APP_CONFIG = config; // Store globally
  console.log("Loaded Config:", window.APP_CONFIG); // Debugging

  const app = createApp(App);
  app.use(createPinia());
  app.use(router);
  app.use(vuetify);
  
  // Now mount the app AFTER config is loaded
  app.mount("#app");
}).catch((error) => {
  console.error("Failed to load config:", error);
});

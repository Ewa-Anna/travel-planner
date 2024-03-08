import { registerPlugins } from "@/plugins";
import App from "./App.vue";
import router from "./router";
import axios from "axios";
import { createApp } from "vue";

const DEV_URL = "http://127.0.0.1:8000";
axios.defaults.baseURL = DEV_URL;

/* eslint-disable @typescript-eslint/no-unsafe-argument */
const app = createApp(App);

registerPlugins(app);

createApp(App)
  .use(router, axios)
  .mount("#app" as string);

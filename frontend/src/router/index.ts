import {
  createRouter,
  createWebHistory,
  type RouteRecordRaw,
} from "vue-router";

import Home from "../components/Home.vue";
import Login from "../components/Login.vue";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;

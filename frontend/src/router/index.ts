import {
  createRouter,
  createWebHistory,
  type RouteRecordRaw
} from 'vue-router'

import Home from '../views/Home.vue'
import Login from '../components/Auth/Login.vue'
import Register from '../components/Auth/Register.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/about',
    name: 'About',
    component: async () => await import('../views/About.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL as string),
  routes
})

export default router

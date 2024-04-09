import { createRouter, createWebHistory } from 'vue-router'
import Test from '@/components/Test/index.vue'
const routes = [
  {
    path: '/test',
    name: 'test',
    component: Test,
  },
]
const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

import { createRouter, createWebHistory } from 'vue-router'
import Test from '@/components/Test/index.vue'
import DIframe from '@/views/DIframe.vue'
const routes = [
  {
    path: '/test',
    name: 'test',
    component: Test,
  },
  {
    path: '/iframe',
    name: 'iframe',
    component: DIframe,
  },
]
const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

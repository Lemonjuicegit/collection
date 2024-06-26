import { createRouter, createWebHashHistory } from 'vue-router'
import DIframe from '@/views/DIframe.vue'
import Dexf from '@/views/Dexf.vue'
import Test from '@/views/Test.vue'
const routes = [
  {
    path: '/iframe',
    name: 'iframe',
    component: DIframe,
  },
  {
    path: '/Dexf',
    name: 'Dexf',
    component: Dexf,
  }
]
const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router

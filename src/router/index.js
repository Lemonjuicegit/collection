import { createRouter, createWebHistory } from 'vue-router'
import Dexf from '@/views/Dexf.vue'
import manage_api from '@/api/manage'

const routes = [
  {
    path: '/:xm_name',
    name: 'home',
    component: () => import('@/views/Collection/index.vue'),
    props: true,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/Dexf',
    name: 'Dexf',
    component: Dexf
  },
  {
    path: '/error/:code/:msg',
    name: 'error',
    component: () => import('@/views/Err.vue'),
    props: true,
    meta: {
      requiresAuth: false
    }
  },
  {
    path: '/manage',
    name: 'manage',
    component: () => import('@/views/Manage/index.vue')
  },
  {
    path: '/test',
    name: 'test',
    component: () => import('@/views/test/index.vue')
  }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})
router.beforeEach(async (to) => {
  let user = sessionStorage.getItem('user')
  if (!user) {
    let res = (await manage_api.getUser()).data
    sessionStorage.setItem('user', JSON.stringify(res))
  }
  if (to.meta.requiresAuth) {
    const path_list = await manage_api.eqPath(to.params.xm_name)
    if (path_list.code === 200) {
      return true
    } else if (path_list.code === 403) {
      return { ame: 'error', params: { code: path_list.code, msg: path_list.msg } }
    }
  }
  return true
})

export default router

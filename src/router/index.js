import { createRouter, createWebHistory } from 'vue-router'
import manage_api from '@/api/manage'
import api from '@/api/manage'

const routes = [
  {
    path: '/:xm_name',
    name: 'xmname',
    component: () => import('@/views/Collection/index.vue'),
    props: true,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/Dexf',
    name: 'Dexf',
    component: () => import('@/views/Dexf.vue')
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
  if (to.name === 'error') {
    return true
  }
  let ip_access = await api.ipAccessAuthorization(window.location.hostname)
  if (ip_access.state === -1) {
    console.log(ip_access)
    return { name: 'error', params: { code: 403, msg: ip_access.res } }
  }
  if (!user) {
    let res = (await manage_api.getUser()).data
    sessionStorage.setItem('user', JSON.stringify(res))
  }
  if (to.meta.requiresAuth) {
    const path_list = await manage_api.eqPath(to.params.xm_name)
    if (path_list.code === 200) {
      return true
    } else if (path_list.code === 403) {
      return { name: 'error', params: { code: path_list.code, msg: path_list.msg } }
    }
  }
  return true
})
export default router

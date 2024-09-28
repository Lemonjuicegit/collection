import { defineStore } from 'pinia'
import api from '@/api/manage'

export const useStore = defineStore('store', {
  state: () => {
    const data = {
      menuitemURL: [],
      ediTabsValue: '',
      edititle: false, // 时候编辑名字
      expandNode: [], // 左侧菜单节点展开
      url: '',
      permissions: 0,
      laftSideWidth: 200,
      user: '',
      router: {}
    }
    return data
  },
  actions: {
    // 你可以在这里添加方法来更新权限信息
    updatePermissions(newPermissions) {
      this.permissions = newPermissions
    },
    async setUser() {
      let res = (await api.getUser()).data
      sessionStorage.setItem('user', JSON.stringify(res))
      this.user = res
    },
    async setRouter(xm_name) {
      // let routerName = getRouter()
      let res = await api.getRouter(xm_name)
      this.router = res
    }
  }
})

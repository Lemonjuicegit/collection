import { defineStore } from 'pinia'

export const useStore = defineStore('store1', {
  state: () => {
    return {
      urlarr: [],
      menuitem: {},
      menuitemURL: [],
      Router: {},
      ediTabsValue: '',
      edititle: false,
      list: [],
      active: '',
    }
  },
  getters: {
    permissions: (state) => state.menuitemURL[state.active] ?state.menuitemURL[state.active].permissions:0,
    title: (state) => state.menuitemURL[state.active] ? state.menuitemURL[state.active].title:'',
    tableData: (state) => state.menuitemURL[state.active] ?
      state.menuitemURL[state.active].data.map((item) => ({
        title: item.title,
        name: item.name,
        URL: item.URL,
      })):[],
  },
  persist: true,
})

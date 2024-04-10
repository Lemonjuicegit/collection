import { reactive } from 'vue'
import { defineStore } from 'pinia'
import { xm_name } from '@/config'

export const useStore = defineStore('store', {
  state: () => {
    let data = reactive({})
    data[xm_name] = {
      urlarr: [],
      menuitem: {},
      menuitemURL: [],
      ediTabsValue: '',
      edititle: false,
      url:'',
    }
    return data
  },
  persist: true,
})

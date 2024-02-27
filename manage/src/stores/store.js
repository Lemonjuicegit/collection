import { ref, reactive } from 'vue'
import { defineStore } from 'pinia'

export const useStore = defineStore('store1', {
  state: () => {
    return {
      urlarr: reactive([]),
      menuitem: reactive({}),
      menuitemURL: reactive([]),
      Router:reactive({}),
      ediTabsValue: ref(''),
      edititle: ref(false),
    }
  },
  persist: true,
})

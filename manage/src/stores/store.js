import { ref, reactive } from 'vue'
import { defineStore } from 'pinia'

export const useStore = defineStore('store', {
  state: () => {
    return {
      urlarr: reactive([]),
      menuitem: reactive({}),
      menuitemURL: reactive([]),
      Router:reactive({}),
      editableTabsValue: ref(''),
      edititle: ref(false),
      Permissions: ref(0),
    }
  },
  persist: true,
})

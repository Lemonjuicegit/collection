import { ref, reactive } from 'vue'
import { defineStore } from 'pinia'

export const useStore = defineStore('counter', () => {
  const urlarr = reactive([
  ])
  const menuitem = reactive({})
  const menuitemURL = reactive([])
  const editableTabsValue = ref('')
  const edititle = ref(false)
  
  return {
    urlarr,
    menuitem,
    menuitemURL,
    editableTabsValue,
    edititle,
  }
})

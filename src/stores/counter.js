import { ref, reactive } from 'vue'
import { defineStore } from 'pinia'

export const useStore = defineStore('counter', () => {
  const urlarr = reactive([
  ])
  const menuitem = reactive({ 表1: false, 表2: false })
  const menuitemURL = reactive([
    {
      title: '表1',
      name: '表1',
      URL: 'https://www.kdocs.cn/wo/sl/v31xu8h1?app_id=1p1s84MLyzLWGQjZrQIYlq',
    },
    {
      title: '表2',
      name: '表2',
      URL: 'https://www.kdocs.cn/wo/sl/v33U3FPN?app_id=4NhEwy4hboKZRG1Wq9mYU',
    },
  ])
  const editableTabsValue = ref('')
  return {
    urlarr,
    menuitem,
    menuitemURL,
    editableTabsValue,
  }
})

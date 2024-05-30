import { defineStore } from 'pinia'
import { xm_name } from '@/config'
export const useTagsStore = defineStore('tags', {
  state: () => {
    let data = {}
    data[xm_name] = {
      list: [],
      active: '',
    }
    return data
  },

  persist: true,
})

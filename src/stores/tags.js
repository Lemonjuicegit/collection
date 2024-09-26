import { defineStore } from 'pinia'
import { xm_name } from '@/config'

export const useTagsStore = defineStore('tags', {
  state: () => {
    const data = { list: [], active: '' }
    return data
  }
})

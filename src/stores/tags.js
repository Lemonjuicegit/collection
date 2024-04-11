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
  getters: {
    show: (state) => {
      return state[xm_name].list.length > 0
    },
    nameList: (state) => {
      return state[xm_name].list.map((item) => item.name)
    },
  },
  actions: {
    delTagsItem(index) {
      const delItem = this[xm_name].list[index]
      this[xm_name].list.splice(index, 1)
      const item = this[xm_name].list[index]
        ? this[xm_name].list[index]
        : this[xm_name].list[index - 1]
      if (this[xm_name].active === delItem.name) {
        this[xm_name].active = item.name
      }
      if (this[xm_name].list.length === 0) {
        this[xm_name].active = ''
      }
    },
    setTagsItem(name, title, url, path) {
      const isExist = this.nameList.some((item) => {
        return item === name
      })
      if (!isExist) {
        this[xm_name].list.push({ name, title, url, path })
      }
    },
    clearTags() {
      this[xm_name].list = []
    },
    closeTagsOther(data) {
      this[xm_name].list = data
    },
  },
  persist: true,
})

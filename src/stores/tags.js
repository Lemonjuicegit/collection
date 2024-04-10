import { defineStore } from 'pinia'
export const useTagsStore = defineStore('tags', {
  state: () => {
    return {
      list: [],
      active: '',
    }
  },
  getters: {
    show: (state) => {
      return state.list.length > 0
    },
    nameList: (state) => {
      return state.list.map((item) => item.name)
    },
  },
  actions: {
    delTagsItem(index) {
      const delItem = this.list[index]
      console.log(delItem)
      this.list.splice(index, 1)
      // if (this.list) {
      //   this.active = this.list[index].name
      //   console.log(this.active)
      //   console.log(index)
      // }
      
    },
    setTagsItem(name, title, path, url) {
      const isExist = this.nameList.some((item) => {
        return item === name
      })
      if (!isExist) {
        this.list.push({ name, title, path, url })
      }
    },
    clearTags() {
      this.list = []
    },
    closeTagsOther(data) {
      this.list = data
    },
    closeCurrentTag(data) {
      for (let i = 0, len = this.list.length; i < len; i++) {
        const item = this.list[i]
        if (item.path === data.$route.fullPath) {
          if (i < len - 1) {
            data.$router.push(this.list[i + 1].path)
          } else if (i > 0) {
            data.$router.push(this.list[i - 1].path)
          } else {
            data.$router.push('/')
          }
          this.list.splice(i, 1)
          break
        }
      }
    },
  },
  persist: true,
})

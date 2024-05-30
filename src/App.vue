<script setup>
import { ref, reactive, onBeforeMount, computed } from 'vue'
// import { useDraggable } from 'vue-draggable-plus'
import Tabs from '@/components/DTabs/tags.vue'
import { DeleteFilled, EditPen } from '@element-plus/icons-vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from '@/stores/store'
import { useTagsStore } from '@/stores/tags'
import { xm_name, permissions } from '@/config'
import { uuid } from '@/utils'
import api from '@/api'
const store = useStore()
const tagsStore = useTagsStore()
const ruleFormRef = ref()
const Nopage = ref(false)
const titleName = ref('')
const delURL = ref(false)
const editURLName = ref(false)
const addURL = ref(false)
const editPopoverVisible = ref(false)
const menuitemURL = ref([])
const ruleForm = reactive({
  name: '',
  url: ''
})
const router = useRouter()
onBeforeMount(async () => {
  let res = await api.getmenuitemURL()
  if (!res.data) {
    Nopage.value = true
    return
  }
  menuitemURL.value = res.data

  store[xm_name].permissions = (await api.getPermissions()).data
  permissions.forEach(item => {
    if ((item & store[xm_name].permissions) === 4) {
      addURL.value = true
    } else if ((item & store[xm_name].permissions) === 1) {
      delURL.value = true
    } else if ((item & store[xm_name].permissions) === 2) {
      editURLName.value = true
    }
  })
  res = await api.getTitle()
  titleName.value = res.data
})
const addTab = (title, name, url, path) => {
  tagsStore[xm_name].active = name
  const isExist = tagsStore[xm_name].list.map(item => item.name).some((item) => {
    return item === name
  })
  if (!isExist) {
    tagsStore[xm_name].list.push({ name, title, path })
  }
  if (!store[xm_name].menuitem[name]) {
    store[xm_name].menuitem[name] = true
    store[xm_name].urlarr.push({
      title,
      name,
      url,
      path
    })
  }
  console.log(tagsStore[xm_name].list)
  store[xm_name].ediTabsValue = name
}

const submitForm = async (formEl) => {
  if (!formEl) return
  let key = uuid()
  store[xm_name].menuitem[key] = false
  menuitemURL.value.push({
    title: ruleForm.name,
    name: key,
    URL: ruleForm.url,
    path: '/iframe',
    editName: false,
  })
  await api.addmenuitemURL({
    title: ruleForm.name,
    name: key,
    URL: ruleForm.url,
    path: '/iframe'
  })
}
const remMenuItem = async (index, targetName) => {
  menuitemURL.value = menuitemURL.value.filter((item) => item.name !== menuitemURL.value[index].name)
  await api.delmenuitemURL(index)
  const tabs = store[xm_name].urlarr
  let activeName = store[xm_name].ediTabsValue
  if (activeName === targetName) {
    tabs.forEach((tab, index) => {
      if (tab.name === targetName) {
        const nextTab = tabs[index + 1] || tabs[index - 1]
        if (nextTab) {
          activeName = nextTab.name
        }
      }
    })
  }
  store[xm_name].ediTabsValue = activeName
  store[xm_name].urlarr = tabs.filter((tab) => tab.name !== targetName)
}
const EditMenuItemName = (e) => {
  menuitemURL.value[index].editName = true
}
const setMenuItemName = async (index) => {
  menuitemURL.value[index].editName = false
  await api.setmenuitemName(index, menuitemURL.value[index].title)
}

const remove = (node, data) => {
  const parent = node.parent
  const children = parent.data.children || parent.data
  const index = children.findIndex((d) => d.id === data.id)
  children.splice(index, 1)
  menuitemURL.value = [...menuitemURL.value]
}



const onTagsClick = (name) => {
  tagsStore[xm_name].active = name
}
const onClose = (item) => {
  if (item) tagsStore[xm_name].active = item.name

}

const closeTags = (curItem) => {
  tagsStore[xm_name].list = curItem
}

const handleNodeClick = (data) => {
  if (!('children' in data)) {
    router.push(data.path)
    tagsStore[xm_name].active = data.name
    const isExist = tagsStore[xm_name].list.map(item => item.name).some((item) => {
      return item === data.name
    })
    if (!isExist) {
      tagsStore[xm_name].list.push(data)
    }
    if (!store[xm_name].menuitem[data.name]) {
      store[xm_name].menuitem[data.name] = true
      store[xm_name].urlarr.push(data)
    }
    store[xm_name].ediTabsValue = data.name
  }

}
const allowDrop = (draggingNode, dropNode, type) => {
  if (!('children' in draggingNode.data)) {
    return type !== 'inner'
  } else {
    return true
  }
}
const allowDrag = (draggingNode) => {
  return !draggingNode.data.label.includes('Level three 3-1-1')
}
const defaultProps = {
  children: 'children',
  label: 'title',
  id: 'id'
}
</script>
<template>
  <div class="common-layout" style="height:100%">
    <el-result v-if="Nopage" icon="error" title="页面不存在" />
    <el-container style="height:100%">
      <el-aside width="200px" height="100%" style="display: flex;flex-direction: column ;">
        <div style="display: flex; justify-content: space-between;align-items:center ">
          <h1 v-if="!store[xm_name].edititle" style="padding: 10px; color: #000000; text-align: left">{{ titleName }}</h1>
          <el-button size="small" type="info">...</el-button>
        </div>
        <el-tree style="max-width: 600px;height: 880px;" :data="menuitemURL" :props="defaultProps" draggable
          @node-click="handleNodeClick">
          <template #default="{ node, data }">
            <span>{{ node.label }}</span>
            <span style="width: 10px;" />
            <el-popover placement="bottom" :width="200" trigger="click" :hide-after="50">
              <template #reference>
                <el-tag type="warning" @click="(e) => e.stopPropagation()" size="small"><el-icon>
                    <EditPen />
                  </el-icon></el-tag>
              </template>
              <el-button type="warning" size="small">改名</el-button>
              <el-button type="warning" size="small" @click="remove(node, data)">删除</el-button>
            </el-popover>
          </template>
        </el-tree>
        <el-popover placement="top" :width="180" style="align-self: flex-end">
          <el-form ref="ruleFormRef" :model="ruleForm" status-icon>
            <el-form-item label="名字">
              <el-input v-model="ruleForm.name" />
            </el-form-item>
            <el-form-item label="网址">
              <el-input v-model="ruleForm.url" />
            </el-form-item>
          </el-form>
          <div style="text-align: right; margin: 0">
            <el-button size="small" @click="submitForm(ruleFormRef)">确认</el-button>
          </div>
          <template #reference>
            <el-button v-if="addURL" size="small" style="background-color:#D4D7DE; color: #000000">添加网址</el-button>
          </template>
        </el-popover>
      </el-aside>
      <el-divider direction="vertical" style="height: 100%;" />
      <el-main style="padding: 5px;">
        <Tabs :list="tagsStore[xm_name].list" :active="tagsStore[xm_name].active" @close="onClose"
          @tags-click="onTagsClick" @close-tags="closeTags" />
        <div class="content" style="height: 95%;">
          <router-view v-slot="{ Component }">
            <transition name="move" mode="out-in">
              <keep-alive>
                <component style="height: 100%;" :is="Component"></component>
              </keep-alive>
            </transition>
          </router-view>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<style scoped>
.move-enter-active,
.move-leave-active {
  transition: opacity 1s ease;
}

.move-enter-from,
.move-leave-to {
  opacity: 0;
}
</style>

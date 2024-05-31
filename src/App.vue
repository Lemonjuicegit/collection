<script setup>
import { ref, reactive, onBeforeMount, computed, h, watch } from 'vue'
// import { useDraggable } from 'vue-draggable-plus'
import Tabs from '@/components/DTabs/tags.vue'
import EditMenuItemForm from '@/components/EditMenuItemForm.vue'
import { DeleteFilled, EditPen, Delete } from '@element-plus/icons-vue'
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
const menuitemURL = ref([])
const popoverVisible = ref(false) // 显隐弹出框
const ruleForm = reactive({
  title: '',
  URL: ''
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
watch(menuitemURL, async (data) => {
  await api.upmenuitemURL(data)
})
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
  ElMessageBox.confirm(
    '你是否要删除该节点!',
    '删除确认',
    {
      type: 'warning',
      icon: Delete,
      showCancelButton: false,
      confirmButtonText: '确认',
    }
  ).then(() => {
    const parent = node.parent
    const children = parent.data.children || parent.data
    const index = children.findIndex((d) => {
      return d.name === data.name
    })
    children.splice(index, 1)
    menuitemURL.value = [...menuitemURL.value]
  })
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
  // 节点点击
  if (data.child) {
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
const onAddNode = (data) => {
  // 添加子节点
  const newChild = { title: '新建节点', name: uuid(), URL: '', path: '/iframe', child: true }
  data.children.push(newChild)
  menuitemURL.value = [...menuitemURL.value]
}
const handleExpand = (data) => {
  // 记录节点展开
  if (store[xm_name].expandNode.indexOf(data.name) === -1) store[xm_name].expandNode.push(data.name)
}
const handlCollapse = (data)=>{
  store[xm_name].expandNode = store[xm_name].expandNode.filter(item => item !== data.name)
}
const onEditPopover = (e) => {
  popoverVisible.value = true
  e.stopPropagation()
}
const onEditMenuItem = (data) => {
  // 修改节点
  if (data.child) {
    ruleForm.title = data.title
    ruleForm.URL = data.URL
    ElMessageBox({
      title: '修改',
      message: () => h(EditMenuItemForm, {
        form: ruleForm
      }),
      confirmButtonText: '确认',
      center: true,
      buttonSize: 'small'
    }).then(() => {
      data.title = ruleForm.title
      data.URL = ruleForm.URL
      menuitemURL.value = [...menuitemURL.value]
    })
  } else {
    ruleForm.title = data.title
    ElMessageBox({
      title: '修改分组名称',
      message: () => h(ElForm, [h(ElFormItem, { label: '分组名称' }, [h(ElInput, { modelValue: ruleForm.title, 'onUpdate:modelValue': value => { ruleForm.title = value }, })])]),
      confirmButtonText: '确认',
      center: true,
      buttonSize: 'small'
    }).then(() => {
      data.title = ruleForm.title
      menuitemURL.value = [...menuitemURL.value]
    })
  }
}
const onAddGroup = () => {
  menuitemURL.value.push({
    title: '新建分组',
    name: uuid(),
    "child": false,
    children: []
  })
}
const handleDragEnd = async (data) => {
  await api.upmenuitemURL(data)
}
const defaultProps = {
  children: 'children',
  label: 'title',
  name: 'name'
}
</script>
<template>
  <div class="common-layout" style="height:100%">
    <el-result v-if="Nopage" icon="error" title="页面不存在" />
    <el-container style="height:100%">
      <el-aside width="200px" height="100%" style="display: flex;flex-direction: column ;">
        <div style="display: flex; justify-content: space-between;align-items:center ">
          <h1 v-if="!store[xm_name].edititle" style="padding: 10px; color: #000000; text-align: left">{{ titleName }}</h1>
          <el-button size="small" type="success" @click="onAddGroup">添加分组</el-button>
        </div>
        <el-tree :default-expanded-keys="store[xm_name].expandNode" node-key="name"
          style="max-width: 600px;height: 880px;" :data="menuitemURL" :props="defaultProps" draggable
          @node-click="handleNodeClick" @node-expand="handleExpand" @node-drag-end="handleDragEnd(menuitemURL)" @node-collapse="handlCollapse">
          <template #default="{ node, data }">
            <span>{{ node.label }}</span>
            <span style="width: 10px;" />
            <el-popover placement="bottom" :width="200" trigger="click" :hide-after="50">
              <template #reference>
                <el-tag :type="data.child ? 'success' : 'warning'" @click="onEditPopover" size="small"
                  effect="dark"><el-icon>
                    <EditPen />
                  </el-icon></el-tag>
              </template>
              <el-button type="warning" size="small" @click="onEditMenuItem(data)">{{ data.child
                ? '修改' : '改名' }}</el-button>
              <el-button type="warning" size="small" @click="remove(node, data)">删除</el-button>
              <el-button v-if="!data.child" type="warning" size="small" @click="onAddNode(data)">添加</el-button>
            </el-popover>
          </template>
        </el-tree>
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

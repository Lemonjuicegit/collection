<script setup name="Collection">
import { EditPen, Delete } from '@element-plus/icons-vue'
import { useStore } from '@/stores/store'
import { useTagsStore } from '@/stores/tags'
import { editItemOptions, editGroup } from './formData'
import { inArray, getDelId } from '@/utils'
import useCollection from '@/hooks/useCollection'
import api from '@/api/manage'
const { collAdd, collDel, collEdit } = useCollection()
const store = useStore()
const tagsStore = useTagsStore()
// const router = useRouter()
const container = ref(null)
const props = defineProps({
  xm_name: { type: String, default: '' }
})
const state = reactive({
  titleName: '',
  dataItemTree: {},
  minWidth: 20,
  initFormData: {},
  editOptions: [],
  URL: ''
})

const RefreshData = async () => {
  await store.setRouter(props.xm_name)
  let res = await api.getItemTree(props.xm_name)
  state.dataItemTree = res.data
}

const defaultProps = {
  children: 'children',
  label: 'title',
  name: 'name'
}
const editRouterDialog = ref(false)
onMounted(async () => {
  // await api.add_use()
  await RefreshData()
  state.titleName = store.router.title
  document.title = store.router.title
})

// watch(dataItemTree, async (data) => {
// await api.updataItemTree(data)
// })

const remove = (node, item) => {
  collDel({ del_type: 'dataItem', item, dataItemModel: state.dataItemTree, node })
}

const onTagsClick = (item) => {
  state.URL = item.URL
}

const closeTags = (curItem) => {
  tagsStore.list = curItem
}

const handleNodeClick = (data) => {
  // 节点点击
  if (!data.is_group) {
    // router.push({ name: 'iframe' })
    state.URL = data.URL
    tagsStore.active = data.name
    const isExist = inArray(tagsStore.list, (item) => item.name === data.name)
    if (!isExist) {
      tagsStore.list.push(data)
    }

    // if (!store.menuitem[data.name]) {
    //     store.menuitem[data.name] = true
    //     store.urlarr.push(data)
    // }
    store.ediTabsValue = data.name
  }
}

const onAddNode = async (data) => {
  // 添加子节点
  const newChild = {
    title: '新建节点',
    URL: '',
    path: '/iframe',
    color: '#b3e19d',
    parent_name: data.name,
    router_name: store.router.name,
    is_group: false
  }
  await api.add('dataItemController', newChild)
  await RefreshData()
  // data.children.push(newChild)
  // state.dataItemTree = [...state.dataItemTree]
}
const handleExpand = (data) => {
  // 记录节点展开
  if (store.expandNode.indexOf(data.name) === -1) store.expandNode.push(data.name)
}
const handlCollapse = (data) => {
  let recursion = (a) => {
    if (!a) return
    for (let v of a) {
      if (!v.child) {
        let index = store.expandNode.indexOf(v.name)
        if (index !== -1) {
          store.expandNode.splice(index, 1)
        }
        recursion(v.children)
      }
    }
  }
  recursion(data.children)
  store.expandNode.splice(store.expandNode.indexOf(data.name), 1)
}

const onEditMenuItem = (data) => {
  if (data.is_group) {
    state.editOptions = editGroup
  } else {
    state.editOptions = editItemOptions
  }
  state.initFormData = data
  editRouterDialog.value = true
}
const handleSubmit = async (data) => {
  await collEdit('dataItem', { id: data.id, title: data.title, URL: data.URL })
}
const onAddGroup = async (data) => {
  let group = {
    title: '新建分组',
    color: '#79bbff',
    parent_name: data.name ? data.name : 'top',
    router_name: store.router.name,
    is_group: true
  }
  await api.add('dataItemController', group)
  await RefreshData()
}
const handleDragEnd = async (before, after, inner) => {
  let data = {}
  if (inner === 'inner') {
    data = { id: before.data.id, parent_name: after.data.name }
  } else {
    data = { id: before.data.id, parent_name: after.data.parent_name }
  }
  await collEdit('dataItem', data)
}

const onDropdownClick = (e) => {
  e.stopPropagation()
}
const onColorChange = (data) => {
  collEdit('dataItem', { id: data.id, color: data.color })
}
const undertint = (col) => {
  // 浅色
  let rgb = col.match(/^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i)
  rgb = rgb
    .slice(1, 4)
    .map((item) => {
      let num = parseInt(item, 16)
      return Math.floor((255 - num) / 2) + num
    })
    .map((item) => item.toString(16).toUpperCase())
    .join('')
  return `#${rgb}`
}
const onMouseDown = (even) => {
  even.preventDefault()
  let iframe = document.querySelectorAll('iframe')
  if (iframe.length > 0) {
    iframe.forEach((item) => {
      item.classList.add('iframe-events-none')
    })
  }
  container.value.onmousemove = (e) => {
    let width = store.laftSideWidth + e.movementX
    if (width >= state.minWidth) store.laftSideWidth = width
  }
}
const onMouseUp = (e) => {
  e.preventDefault()
  let iframe = document.querySelectorAll('iframe')
  if (iframe.length > 0) {
    iframe.forEach((item) => {
      item.classList.remove('iframe-events-none')
    })
  }
  container.value.onmousemove = null
}
const dropOptions = () => [
  {
    label: '添加网址',
    click: () => collAdd('dataItem', state.dataItemTree)
  },
  {
    label: '添加分组',
    click: () => collAdd('groupItem', state.dataItemTree)
  }
]
</script>
<template>
  <div class="common-layout" style="height: 100%">
    <div class="container" style="" ref="container" @mouseup="onMouseUp">
      <div class="aside" :style="{ width: `${store.laftSideWidth}px` }">
        <div class="aside-header">
          <h4 class="aside-title">{{ state.titleName }}</h4>
          <Dropdown :option="dropOptions()" trigger="hover">
            <el-button type="success" size="small"><i-ep-plus /></el-button>
          </Dropdown>
        </div>
        <el-scrollbar height="1000px">
          <el-tree
            :default-expanded-keys="store.expandNode"
            node-key="name"
            style="height: 100%"
            :data="state.dataItemTree.dataItem"
            :props="defaultProps"
            draggable
            @node-click="handleNodeClick"
            @node-expand="handleExpand"
            @node-drop="handleDragEnd"
            @node-collapse="handlCollapse"
          >
            <template #default="{ node, data }">
              <div
                :class="data.name === tagsStore.active ? 'node-item' : ''"
                :style="{
                  display: 'flex',
                  width: '100%',
                  padding: '3px 5px 3px 5px',
                  backgroundColor: undertint(data.color),
                  borderRadius: '10px'
                }"
              >
                <span
                  :style="{
                    paddingLeft: '10px',
                    paddingRight: '10px',
                    backgroundColor: data.color,
                    borderRadius: '30px'
                  }"
                  >{{ node.label }}</span
                >
                <span style="width: 10px" />
                <div style="margin-left: auto">
                  <el-dropdown
                    trigger="click"
                    size="small"
                    :index="data.name"
                    :hide-on-click="false"
                  >
                    <el-tag
                      :type="data.is_group ? 'success' : 'primary'"
                      plain
                      :color="data.color"
                      @click="onDropdownClick"
                      size="small"
                      effect="dark"
                    >
                      <i-ep-edit-pen />
                    </el-tag>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item @click="onEditMenuItem(data)">修改</el-dropdown-item>
                        <div>
                          <el-dropdown-item @click="remove(node, data)">删除</el-dropdown-item>
                        </div>
                        <div>
                          <el-dropdown-item @click="onAddNode(data)" v-if="data.is_group"
                            >添加网页</el-dropdown-item
                          >
                        </div>
                        <div>
                          <el-dropdown-item @click="onAddGroup(data)" v-if="data.is_group"
                            >添加分组</el-dropdown-item
                          >
                        </div>
                        <el-dropdown-item divided>
                          <input type="color" v-model="data.color" @change="onColorChange(data)" />
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </div>
              </div>
            </template>
          </el-tree>
        </el-scrollbar>
      </div>
      <div class="lin" @mousedown="onMouseDown">
        <div />
      </div>
      <div class="main" style="padding: 5px">
        <DTabs
          v-model:list="tagsStore.list"
          v-model:active="tagsStore.active"
          @tags-click="onTagsClick"
          @close-tags="closeTags"
        />
        <div class="content" style="height: 95%">
          <iframe
            :src="state.URL"
            frameborder="0"
            width="100%"
            height="100%"
            name="iframe"
          ></iframe>
        </div>
      </div>
    </div>
  </div>
  <EditDialog
    v-model="editRouterDialog"
    :options="state.editOptions"
    v-model:data="state.initFormData"
    title="修改"
    @submit="handleSubmit"
  />
</template>

<style src="./style.css" scoped></style>

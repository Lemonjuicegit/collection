<script setup name="Collection">
import { useStore } from '@/stores/store'
import { useTagsStore } from '@/stores/tags'
import { editItemOptions, editGroup } from './formData'
import { inArray } from '@/utils'
import useCollection from '@/hooks/useCollection'
import api from '@/api/manage'
const { collAdd, collDel, collEdit } = useCollection()
const store = useStore()
const tagsStore = useTagsStore()
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

const onTags = (item) => {
  if (item) {
    state.URL = item.URL
  } else {
    state.URL = ''
  }
}

const closeTagsAll = (curItem) => {
  tagsStore.list = curItem
}

const handleNodeClick = (data) => {
  // 节点点击
  console.log(data)
  if (!data.is_group) {
    state.URL = data.URL
    tagsStore.active = data.name
    const isExist = inArray(tagsStore.list, (item) => item.name === data.name)
    if (!isExist) {
      tagsStore.list.push(data)
    }
  }
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

const handleDragEnd = async (before, after, inner) => {
  let data = {}
  if (inner === 'inner') {
    data = { id: before.data.id, parent_name: after.data.name }
  } else {
    data = { id: before.data.id, parent_name: after.data.parent_name }
  }
  await collEdit('dataItem', data)
}

const onColorChange = (color) => {
  collEdit('dataItem', { id: data.id, color })
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
const dropOptions = (data, node) => [
  {
    label: '添加网址',
    click: () => collAdd('dataItem', data),
    hidden: () => {
      console.log(data)
      return data.is_group ? data.is_group : true
    }
  },
  {
    label: '添加分组',
    click: () => collAdd('groupItem', data),
    hidden: () => (data.is_group ? data.is_group : true)
  },
  {
    label: '修改',
    click: () => onEditMenuItem(data),
    hidden: () => (node ? true : false)
  },
  {
    label: '删除',
    click: () => {
      collDel({ del_type: 'dataItem', item: data, dataItemModel: state.dataItemTree, node })
    },
    hidden: () => (node ? true : false)
  }
]
</script>
<template>
  <div class="common-layout" style="height: 100%">
    <div class="container" style="" ref="container" @mouseup="onMouseUp">
      <div class="aside" :style="{ width: `${store.laftSideWidth}px` }">
        <div class="aside-header">
          <h4 class="aside-title">{{ state.titleName }}</h4>
          <Dropdown :option="dropOptions(state.dataItemTree)" trigger="hover">
            <el-button type="success" size="small"><i-ep-plus /></el-button>
          </Dropdown>
        </div>
        <el-scrollbar height="1000px">
          <el-tree
            :default-expanded-keys="store.expandNode"
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
              <MenuTag
                :name="data.name"
                :title="data.title"
                :active="tagsStore.active"
                v-model:color="data.color"
              >
                <template #interior>
                  <Dropdown
                    :isEditColor="true"
                    v-model:color="data.color"
                    :option="dropOptions(data, node)"
                    @color-change="onColorChange"
                  />
                </template>
              </MenuTag>
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
          @tags-click="onTags"
          @close-tags="closeTagsAll"
          @close="onTags"
        />
        <div class="content" style="height: 95%">
          <iframe
            :src="state.URL"
            v-if="state.URL"
            frameborder="0"
            width="100%"
            height="100%"
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

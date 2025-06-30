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

const handleSubmit = async (data) => {
  await collEdit('dataItem', [{ id: data.id, title: data.title, URL: data.URL }])
}

const handleDragEnd = async (before, after, inner) => {
  const data = []
  if (inner === 'inner') {
    data.push({ id: before.data.id, parent_name: after.data.name })
  } else {
    data.push({ id: before.data.id, parent_name: after.data.parent_name })
  }
  await collEdit('dataItem', data)
  const sort_array = []
  after.parent.data.children.forEach((item, index) => {
    sort_array.push({ id: item.id, sort: index + 1 })
  })
  await collEdit('dataItem', sort_array)
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
const onMouseUp = () => {
  let iframe = document.querySelectorAll('iframe')
  if (iframe.length > 0) {
    iframe.forEach((item) => {
      item.classList.remove('iframe-events-none')
    })
  }
  container.value.onmousemove = null
}
const hanldeColorChange = (color, data) => {
  collEdit('dataItem', { id: data.id, color })
}
const dropOptions = (data, node) => [
  {
    label: '添加网址',
    name: 'addItem',
    click: () => collAdd('dataItem', data),
    hidden: () => {
      return data.is_group !== undefined ? data.is_group : true
    }
  },
  {
    label: '添加分组',
    name: 'addGroup',
    click: () => collAdd('groupItem', data),
    hidden: () => (data.is_group !== undefined ? data.is_group : true)
  },
  {
    label: '修改',
    name: 'edit',
    click: () => {
      if (data.is_group) {
        state.editOptions = editGroup
      } else {
        state.editOptions = editItemOptions
      }
      state.initFormData = data
      editRouterDialog.value = true
    },
    hidden: () => (node ? true : false)
  },
  {
    label: '删除',
    name: 'del',
    click: () => {
      collDel({ del_type: 'dataItem', item: data, dataItemModel: state.dataItemTree, node })
    },
    hidden: () => (node ? true : false)
  },
  {
    name: 'color',
    hidden: () => (node ? true : false)
  }
]
</script>
<template>
  <div class="common-layout" style="height: 100%">
    <div class="container" style="" ref="container" @mouseup.prevent="onMouseUp">
      <div class="aside" :style="{ width: `${store.laftSideWidth}px` }">
        <div class="aside-header">
          <h4 class="aside-title">{{ state.titleName }}</h4>
          <Dropdown :width="40" :option="dropOptions(state.dataItemTree)">
            <el-button color="#79bbff" size="small">
              <i-ep-plus />
            </el-button>
          </Dropdown>
        </div>
        <el-scrollbar height="100%">
          <el-tree
            :default-expanded-keys="store.expandNode"
            style="height: 100%"
            :data="state.dataItemTree.dataItem"
            :props="defaultProps"
            :allow-drop="(_, dropNode) => dropNode.data.is_group"
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
                  <Dropdown :isEditColor="true" :width="40" :option="dropOptions(data, node)"
                    ><el-button size="small" :color="data.color"><i-ep-edit-pen /> </el-button>
                    <template #color>
                      <el-button color="#FFFFFF">
                        <input
                          v-model="data.color"
                          type="color"
                          @change="hanldeColorChange(data.color, data)"
                        />
                      </el-button>
                    </template>
                  </Dropdown>
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

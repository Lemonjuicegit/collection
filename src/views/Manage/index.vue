<script setup name="Manage">
import Main from './Main.vue'
import { inArray } from '@/utils'
import api from '@/api/manage'
import useCollection from '@/hooks/useCollection'
const { collAdd, collDel, collEdit } = useCollection()
const state = reactive({
  listColor: '#f89898',
  tagList: [],
  active: '',
  dataTree: {},
  routerData: []
})

onMounted(async () => {
  let res = await api.getRouterList()
  let dataTree = await api.getDataTree()
  state.dataTree = dataTree.data
  state.routerData = res.data
  console.log(dataTree)
})

const routerData = computed(() => {
  let routerData = []
  Object.values(state.dataTree).forEach((value) => {
    routerData.push(value)
  })
  return routerData
})

const handlMenuClick = (data) => {
  let isExist = inArray(state.tagList, (item) => item.name === data.name)
  if (!isExist) {
    state.tagList.push(data)
  }
  state.active = data.name
}
</script>
<template>
  <LayoutBase :minWidth="250">
    <template #aside-header>
      <div class="aside-header">
        <p class="aside-title">办公网址管理</p>
        <el-button size="small" type="success" @click="collAdd('router', state.dataTree)">
          <i-ep-plus />
        </el-button>
      </div>
    </template>
    <template #aside>
      <div v-for="(item, key) in routerData" :key="key" style="margin: 10px">
        <MenuTag
          :name="item.name"
          :title="item.title"
          :active="state.active"
          @menu-click="handlMenuClick"
        >
          <template #interior>
            <el-button
              @click.stop="collDel({ del_type: 'router', item, dataTree: state.dataTree })"
              type="danger"
              size="small"
            >
              <i-ep-delete-filled />
            </el-button>
          </template>
        </MenuTag>
      </div>
    </template>
    <template #header>
      <DTabs v-model:list="state.tagList" v-model:active="state.active" />
    </template>
    <template #main>
      <Main v-if="state.dataTree[state.active]" v-model:data="state.dataTree[state.active]" />
    </template>
  </LayoutBase>
</template>
<style src="./style.css" scoped></style>

<script setup name="ManageMain">
import useCollection from '@/hooks/useCollection'
import { editItemOptions, editGroup, defaultProps } from './formData'

const { collAdd, collDel, collEdit } = useCollection()
const editDialog = ref(false)
const dataItemModel = defineModel('data')
const state = reactive({
  editOptions: editItemOptions,
  initFormData: {}
})
const dropOptions = (data) => [
  {
    label: '添加网址',
    click: () => collAdd('dataItem', data),
    hidden: () => {
      console.log(data)
      return true
    }
  },
  {
    label: '添加分组',
    click: () => collAdd('groupItem', data)
  }
]

const onRouterTitleChange = async (value) => {
  console.log(value)
  await collEdit('router', { id: dataItemModel.value.id, title: value })
}
const onRouterPathChange = async (value) => {
  await collEdit('router', { id: dataItemModel.value.id, path: value })
}

const handlNodeDrop = async (before, after, inner) => {
  let data = {}
  if (inner === 'inner') {
    data = { id: before.data.id, parent_name: after.data.name }
  } else {
    data = { id: before.data.id, parent_name: after.data.parent_name }
  }
  await collEdit('dataItem', data)
}

const onEditItem = (data) => {
  if (data.is_group) {
    state.editOptions = editGroup
  } else {
    state.editOptions = editItemOptions
  }
  state.initFormData = data
  editDialog.value = true
}
const handleSubmit = async (data) => {
  collEdit('dataItem', { id: data.id, title: data.title, URL: data.URL })
}
const onColorChange = (data) => {
  collEdit('dataItem', { id: data.id, color: data.color })
}
</script>
<template>
  <div class="main">
    <el-form label-width="auto" style="width: 100%">
      <el-form-item label="路由标题">
        <el-input v-model="dataItemModel.title" @change="onRouterTitleChange" />
      </el-form-item>
      <el-form-item label="路由名称">
        <el-input v-model="dataItemModel.path" @change="onRouterPathChange" />
      </el-form-item>
      <el-form-item> </el-form-item>
    </el-form>
    <el-card>
      <template #header>
        <div style="gap: 20px; display: flex">
          <span>网址管理</span>
          <Dropdown :option="dropOptions(dataItemModel)" trigger="hover">
            <el-button type="success" size="small"><i-ep-plus /></el-button>
          </Dropdown>
        </div>
      </template>
      <el-scrollbar height="500px" style="width: 100%">
        <div style="width: 100%">
          <el-tree
            node-key="name"
            style="height: 100%"
            :data="dataItemModel.dataItem"
            :props="defaultProps"
            :allow-drop="(_, dropNode) => dropNode.data.is_group"
            draggable
            @node-drop="handlNodeDrop"
          >
            <template #default="{ node, data }">
              <MenuTag :name="data.name" :title="data.title" v-model:color="data.color">
                <template #outside>
                  <div style="gap: 10px; display: flex; margin-left: 10px">
                    <div v-if="!data.is_group">
                      <el-link v-if="data.URL" :href="data.URL" target="_blank" type="primary"
                        >跳转</el-link
                      >
                      <el-link v-else type="primary" disabled>空网址</el-link>
                    </div>
                    <Dropdown v-if="data.is_group" :option="dropOptions(data)" trigger="hover">
                      <el-button type="success" size="small"><i-ep-plus /></el-button>
                    </Dropdown>
                    <el-button type="success" size="small" @click.stop="onEditItem(data)"
                      ><i-ep-edit
                    /></el-button>
                    <el-button
                      type="danger"
                      size="small"
                      @click="collDel({ del_type: 'dataItem', item: data, dataItemModel, node })"
                      ><i-ep-delete-filled
                    /></el-button>
                    <input
                      type="color"
                      v-model="data.color"
                      @change="onColorChange(data)"
                      @click="(e) => e.stopPropagation()"
                    />
                  </div>
                </template>
              </MenuTag>
            </template>
          </el-tree>
        </div>
      </el-scrollbar>
    </el-card>
  </div>
  <EditDialog
    v-model="editDialog"
    :options="state.editOptions"
    v-model:data="state.initFormData"
    title="修改"
    @submit="handleSubmit"
  />
</template>

<style scoped>
.main {
  width: 95%;
  display: flex;
  flex-direction: column;
}
</style>

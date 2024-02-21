<script setup>
import { ref, reactive, onBeforeMount } from 'vue'
import DTabs from '@/components/DTabs/index.vue'
import { DeleteFilled, EditPen } from '@element-plus/icons-vue'
import { useStore } from '@/stores/counter'
import { uuid } from '@/utils'
import api from '@/api'
const store = useStore()
const ruleFormRef = ref()
const titleName = ref('')
const ruleForm = reactive({
  name: '',
  url: ''
})
onBeforeMount(async () => {
  let res = await api.getmenuitemURL()
  store.menuitemURL = res.data
  store.menuitemURL.forEach(item => {
    store.menuitem[item.name] = false
  })
  res = await api.getTitle()
  titleName.value = res.data
})
const addTab = (title, name, url) => {
  if (!store.menuitem[name]) {
    store.menuitem[name] = true
    store.urlarr.push({
      title,
      name,
      url
    })
  }
  store.editableTabsValue = name
}

const submitForm = async (formEl) => {
  if (!formEl) return
  console.log(uuid())
  let key = uuid()
  store.menuitem[key] = false
  store.menuitemURL.push({
    title: ruleForm.name,
    name: key,
    URL: ruleForm.url
  })
  await api.addmenuitemURL({
    title: ruleForm.name,
    name: key,
    URL: ruleForm.url
  })
}
const setTitleName = async () => {
  store.edititle = !store.edititle
  await api.setTitle(titleName.value)
}
const remMenuItem = async (index) => {
  store.menuitemURL = store.menuitemURL.filter((item) => item.name !== store.menuitemURL[index].name)
  await api.delmenuitemURL(index)
}
const EditMenuItemName = async (index) => {
  store.menuitemURL = store.menuitemURL.filter((item) => item.name !== store.menuitemURL[index].name)
  await api.delmenuitemURL(index)
}
</script>
<template>
  <div class="common-layout" style="height:100%">
    <el-container style="height:100%">
      <el-aside width="200px" height="100%" style="display: flex;flex-direction: column ;background-color:#D4D7DE;">
        <h1 @click="store.edititle = !store.edititle" v-if="!store.edititle"
          style="padding: 10px; color: #000000; text-align: center">{{ titleName }}</h1>
        <el-input v-if="store.edititle" @blur="setTitleName" size="large" v-model="titleName" />
        <el-menu background-color="#D4D7DE" text-color="#fff" active-text-color="#ffd04b" class="el-menu-vertical-demo"
          style="height: 880px;">
          <el-menu-item style="padding: 5px;" :index="U.name" v-for="(U, index) in store.menuitemURL">
            <el-button @click="remMenuItem(index)" :icon="DeleteFilled" circle type="danger" size="small"/>
            <el-button @click="EditMenuItemName(index)" :icon="EditPen" circle type="primary" size="small"/>
            <div style="padding: 2px;"></div>
            <el-button @click="() => addTab(U.title, U.name, U.URL)" text color="#E6A23C">{{ U.title }}</el-button>
          </el-menu-item>
        </el-menu>
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
            <el-button size="small" style="background-color:#D4D7DE; color: #000000">添加网址</el-button>
          </template>
        </el-popover>
      </el-aside>
      <el-main style="padding: 5px;">
        <d-tabs />
      </el-main>
    </el-container>
  </div>
</template>

<style scoped></style>

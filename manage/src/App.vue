<script setup>
import { ref, reactive, onBeforeMount } from 'vue'
import Tabs from '@/components/DTabs/tags.vue'
import DTab from '@/components/DTabs/DTab.vue'
import { DeleteFilled, EditPen } from '@element-plus/icons-vue'
import { useStore } from '@/stores/store'
import { uuid } from '@/utils'
import api from '@/api'
const store = useStore()
const ruleFormRef = ref()
const ruleForm = reactive({
  routerName: '',
})
const state = reactive({
  title:''
})
onBeforeMount(async () => {
  let Router = await api.getRouter()
  let menuitem = await api.getmenuitem()
  store.Router = Router.data.map(item => ({ title : item , editName:false}))
  store.menuitemURL = menuitem.data
  Router.data.forEach(item => {
    store.menuitem[item.name] = false
  })
})
const addTab = (title, name) => {
  store.active = title

  let isExist = store.list.map(item=>item.title).some((item) => {
    return item === title
  })
  if (!isExist) {
    store.list.push({ name: title, title, path:'' })
  }
  
  state.title = title
  if (!store.menuitem[name]) {
    store.menuitem[name] = true
    store.urlarr.push({
      title,
      name
    })
  }
 store.menuitemURL[store.active]
  store.ediTabsValue = name
}

const submitForm = async (formEl) => {
  if (!formEl) return
  let key = uuid()
  let regex = /^[a-zA-Z0-9]*$/
  if (!regex.test(ruleForm.routerName)) {
    return
  }
  await api.addRouter(ruleForm.routerName)
  store.Router.push({ title: ruleForm.routerName, editName: false })
}
const remMenuItem = async (index) => {
  await api.delRouter(index)
}
const editMenuItemName = async (index) => {
  store.Router[index].editName = true
}
const setMenuItemName = async (index) => {
  store.Router[index].editName = false
  await api.setmenuitemName(index, store.menuitemURL[index].title)
}

const rulesRouter = reactive({
  routerName: [
    { pattern: /^[a-zA-Z0-9]*$/, message: '路由名只能包含字母和数字', trigger: 'change' },
  ],
})
const onTagsClick = (name)=>{
  store.active = name
}
const closeTags = (curItem) => {
  console.log(curItem.length)
  store.list = curItem
  if(curItem.length === 0){
    store.active = ''
  }

}

</script>
<template>
  <div class="common-layout" style="height:100%">
    <el-container style="height:100%">
      <el-aside width="200px" height="100%" style="display: flex;flex-direction: column ;background-color:#D4D7DE;">
        <h1 style="padding: 10px; color: #000000; text-align: center">共享网站管理</h1>
        <div style="border: 1px solid #606266;"/>
        <el-menu background-color="#D4D7DE" text-color="#fff" active-text-color="#ffd04b"
          style="height: 880px;">
          <el-menu-item style="padding: 1px;height: 40px; " :index="String(index)" v-for="(R, index) in store.Router">
            <el-popconfirm title="是否删除" cancel-button-text="取消" confirm-button-text="确认" @confirm="remMenuItem(R.title)">
              <template #reference>
                <el-button :icon="DeleteFilled" circle type="danger" size="small" />
              </template>
            </el-popconfirm>
            <el-button @click="editMenuItemName(index)" :icon="EditPen" circle type="primary" size="small" />
            <div style="padding: 2px;"></div>
            <el-button v-if="!R.editName" @click="addTab(R.title, String(index))" text color="#E6A23C" >{{ R.title }}</el-button>
            <el-input v-if="R.editName" @blur="setMenuItemName(index)" v-model="store.Router[index].title" />
          </el-menu-item>
        </el-menu>

        <el-popover trigger="click" :width="250" style="align-self: flex-end">
          <el-form ref="ruleFormRef" :rules="rulesRouter" :model="ruleForm" status-icon >
            <el-form-item label="路由名" prop="routerName">
              <el-input v-model="ruleForm.routerName"/>
            </el-form-item>
          </el-form>
          <div style="text-align: right; margin: 0">
            <el-button size="small" @click="submitForm(ruleFormRef)">确认</el-button>
          </div>
          <template #reference>
            <el-button size="small" style="background-color:#D4D7DE; color: #000000">添加路由</el-button>
          </template>
        </el-popover>
      </el-aside>
      <el-main style="padding: 5px;">
        <Tabs :list="store.list" :active="store.active" @tags-click="onTagsClick" @close-tags="closeTags" />
        <DTab v-show="store.active"
        :permissions="store.permissions"
        :title="store.title"
        :data="store.tableData"
        />
      </el-main>
    </el-container>
  </div>
</template>

<style scoped>

</style>

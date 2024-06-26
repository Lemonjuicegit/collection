<script setup>
import { ref, reactive, onBeforeMount, h, watch } from 'vue'
// import { useDraggable } from 'vue-draggable-plus'
import Tabs from '@components/DTabs/tags.vue'
import EditMenuItemForm from '@components/EditMenuItemForm.vue'
import { EditPen, Delete } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { useStore } from '@/stores/store'
import { useTagsStore } from '@/stores/tags'
import { xm_name } from '@/config'
import { uuid } from '@/utils'
import api from '@/api'
const store = useStore()
const tagsStore = useTagsStore()
const Nopage = ref(false)
const titleName = ref('')
const menuitemURL = ref([]) // 菜单项
const popoverVisible = ref(false) // 显隐弹出框
const ruleForm = reactive({
  title: '',
  URL: ''
})
const router = useRouter()

onBeforeMount(async () => {
  await api.add_use()

  let res = await api.getmenuitemURL()
  if (!res.data) {
    Nopage.value = true
    return
  }
  menuitemURL.value = res.data
  //获取Title
  res = await api.getTitle()
  titleName.value = res.data
})
watch(menuitemURL, async (data) => {
  await api.upmenuitemURL(data)
})

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
  const newChild = { title: '新建节点', name: uuid(), URL: '', path: '/iframe', color: '#b3e19d', child: true }
  data.children.push(newChild)
  menuitemURL.value = [...menuitemURL.value]
}
const handleExpand = (data) => {
  // 记录节点展开
  if (store[xm_name].expandNode.indexOf(data.name) === -1) store[xm_name].expandNode.push(data.name)
}
const handlCollapse = (data) => {
  let recursion = (a)=>{
    for (let v of a){
      if (!v.child){
        let index = store[xm_name].expandNode.indexOf(v.name)
        if(index !== -1){
          store[xm_name].expandNode.splice(index,1)
        }
        recursion(v.children)
      }
    }
  }
  recursion(data.children)
  store[xm_name].expandNode.splice(store[xm_name].expandNode.indexOf(data.name), 1)
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
    child: false,
    color: "#79bbff",
    children: []
  })
}
const handleDragEnd = async (data) => {
  await api.upmenuitemURL(data)
}

const onDropdownClick = (e) => {
  e.stopPropagation()
}
const selectColor = () => {
  menuitemURL.value = [...menuitemURL.value]
}

const undertint = (col) => {
  // 浅色
  let rgb = col.match(/^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i)
  rgb = rgb.slice(1, 4).map(item => {
    let num = parseInt(item, 16)
    return Math.floor((255 - num) / 2) + num
  }).map(item => item.toString(16).toUpperCase()).join('')
  return `#${rgb}`
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
      <el-aside height="100%" style="display: flex;flex-direction: column ;width:250px;">
        <div style="display: flex; justify-content: space-between;align-items:center ">
          <h1 style="padding: 10px; color: #000000; text-align: left">{{ titleName }}</h1>
          <el-button v-permission="'addGroup'" size="small" type="success" @click="onAddGroup">添加分组</el-button>
        </div>
        <el-tree :default-expanded-keys="store[xm_name].expandNode" node-key="name"
          style=" height: 100%;" :data="menuitemURL" :props="defaultProps" draggable
          @node-click="handleNodeClick" @node-expand="handleExpand" @node-drag-end="handleDragEnd(menuitemURL)"
          @node-collapse="handlCollapse">
          <template #default="{ node, data }">
            <div :class="data.name === tagsStore[xm_name].active ? 'node-item' : ''" :style="{
              display: 'flex',
              width: '100%',
              padding: '3px 5px 3px 5px',
              backgroundColor: undertint(data.color),
              borderRadius: '10px',
            }">
              <span :style="{
                paddingLeft: '10px',
                paddingRight: '10px',
                backgroundColor: data.color,
                borderRadius: '30px'
              }">{{ node.label }}</span>
              <span style="width: 10px;" />
              <div v-permission="'edit'" style="margin-left: auto;" >
                <el-dropdown trigger="click" size="small" :index="data.name" :hide-on-click="false">
                  <el-tag :type="data.child ? 'success' : 'primary'" plain :color="data.color"
                    @click="onDropdownClick" size="small" effect="dark"><el-icon>
                      <EditPen />
                    </el-icon></el-tag>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item  @click="onEditMenuItem(data)">{{ data.child
                        ? '修改' : '改名' }}</el-dropdown-item>
                      <div v-permission="'delURL'">
                        <el-dropdown-item @click="remove(node, data)">删除</el-dropdown-item>
                      </div>
                      <div v-permission="'addURL'">
                        <el-dropdown-item  @click="onAddNode(data)" v-if="!data.child">添加</el-dropdown-item>
                      </div>
                        <el-dropdown-item  divided>
                            <input type="color" v-model="data.color" @change="selectColor"/>
                          </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>

              </div>
            </div>
          </template>
        </el-tree>
      </el-aside>
      <el-divider direction="vertical" style="height: 100%;"/>
      <el-main style="padding: 5px;">
        <Tabs v-model:list="tagsStore[xm_name].list" v-model:active="tagsStore[xm_name].active" @tags-click="onTagsClick"
          @close-tags="closeTags" />
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

.el-tree-node {
  margin-top: 20px;
  /* 根据需要调整上间距 */
  margin-bottom: 20px;
  /* 根据需要调整下间距 */
}

.node-item {
  box-shadow: 0px 0px 5px 1px rgba(0, 0, 0, 0.3);
  border: 1px solid #79bbff;
}
</style>

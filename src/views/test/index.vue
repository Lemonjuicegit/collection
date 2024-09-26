<script setup>
import api from '@/api'
import manage_api from '@/api/manage'
import Dropdown from '@/components/Dropdown/index.vue'
import useCollection from '@/hooks/useCollection'
const { message } = useCollection()
const state = reactive({
  list: [],
  percentage: 0
})
onMounted(async () => {
  state.list = [
    {
      title: 'getPathList',
      value: await api.eqPath('xm1')
    },
    {
      title: 'getRouterList',
      value: await manage_api.getRouterList()
    }
    // {
    //   title: 'getDataTree',
    //   value: await manage_api.getDataTree()
    // }
  ]
})
const onClick = () => {
  console.log('测试2')
  message('测试', async () => {
    console.log('测试')
  })
}
</script>
<template>
  <el-scrollbar height="1000px">
    <div v-for="item in state.list">
      <el-card>
        <template #header>
          <div class="card-header">
            <span style="color: #79bbff">{{ item.title }}</span>
          </div>
        </template>
        <p>{{ item.value }}</p>
      </el-card>
      <el-button @click="onClick">测试</el-button>
    </div>
  </el-scrollbar>
</template>
<style lang="scss" scoped></style>

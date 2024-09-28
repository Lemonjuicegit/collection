<script setup>
import manage_api from '@/api/manage'
import Dropdown from '@/components/Dropdown/index.vue'
import useCollection from '@/hooks/useCollection'
const { message } = useCollection()
const onClick = () => {
  console.log('测试2')
  message('测试', async () => {
    console.log('测试')
  })
}
const defaultProps = {
  children: 'children',
  label: 'title',
  name: 'name'
}

const state = reactive({
  list: [
    {
      title: '节点1',
      name: 'name',
      testlist: [
        {
          title: '节点1-1',
          hidden: true
        },
        {
          title: '节点1-2',
          hidden: true
        }
      ]
    }
  ],
  percentage: 0
})
const onclick = (data) => {
  console.log(data)
}
</script>
<template :prop>
  <el-dropdown trigger="click">
    <slot>
      <el-tag plain size="small" @click.stop="() => {}" effect="dark"><i-ep-edit-pen /> </el-tag>
    </slot>
    <template #dropdown>
      <template>
        <el-dropdown-menu>
          <template v-for="item in state.list[0].testlist">
            <el-dropdown-item v-if="item.hidden ? item.hidden : true" :command="item.title">
              {{ item.title }}
            </el-dropdown-item>
          </template>
        </el-dropdown-menu>
      </template>
    </template>
  </el-dropdown>
</template>
<style lang="scss" scoped></style>

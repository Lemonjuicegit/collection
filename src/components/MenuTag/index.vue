<script setup name="MenuTag">
import { EditPen, Delete } from '@element-plus/icons-vue'
const props = defineProps({
  option: {
    type: Object,
    default: () => ({})
  },
  active: {
    type: String,
    default: ''
  }
})

const colorModel = defineModel('color', { default: '#b3e19d' })
const emit = defineEmits(['menu-click'])

const onDropdownClick = (e) => {
  //阻止点击事件传递
  e.stopPropagation()
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
const selectColor = () => {
  console.log('selectColor')
}
const onClick = () => {
  emit('menu-click', props.option)
}
</script>
<template>
  <div
    @click="onClick"
    :class="props.option.name === props.active ? 'node-item' : ''"
    :style="{
      display: 'flex',
      width: '100%',
      padding: '3px 5px 3px 5px',
      backgroundColor: undertint(colorModel),
      borderRadius: '10px'
    }"
  >
    <span
      :style="{
        paddingLeft: '10px',
        paddingRight: '10px',
        backgroundColor: colorModel,
        borderRadius: '30px'
      }"
      >{{ props.option.title }}</span
    >
    <span style="margin: auto" />
    <div v-if="props.option.dropdownHidden" style="margin-left: auto">
      <el-dropdown trigger="click" size="small" :index="props.option.name" :hide-on-click="false">
        <el-tag
          type="primary"
          plain
          :color="colorModel"
          @click="onDropdownClick"
          size="small"
          effect="dark"
          ><i-ep-edit-pen
        /></el-tag>
        <template #dropdown>
          <el-dropdown-menu>
            <div v-for="(item, index) in props.option.dropdownOption" :key="index">
              <el-dropdown-item
                v-if="item.hidden ? item.hidden(item) : true"
                @click="item.click(item)"
                >{{ item.label }}</el-dropdown-item
              >
            </div>
            <el-dropdown-item v-if="props.isEditColor" divided>
              <input type="color" v-model="colorModel" @change="selectColor" />
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
    <slot name="interior" />
  </div>
  <slot name="outside" />
</template>
<style src="./style.css" scoped></style>

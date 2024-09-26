<script setup name="Dropdown">
const props = defineProps({
  option: {
    type: Object,
    default: () => ({})
  },
  size: {
    type: String,
    default: 'small'
  },
  color: {
    type: String,
    default: '#b3e19d'
  },
  isEditColor: {
    type: Boolean,
    default: false
  },
  trigger: {
    type: String,
    default: 'click'
  }
})
const colorModel = defineModel('color')
const emit = defineEmits(['dropdown-click'])

const onDropdownClick = () => {
  emit('dropdown-click')
}
// onMounted(() => {
//   console.log('colorModel', props.option)
// })
</script>
<template>
  <el-dropdown :trigger="props.trigger" :size="props.small" :hide-on-click="false">
    <slot>
      <el-tag
        type="primary"
        plain
        :color="props.color"
        @click.stop="onDropdownClick"
        size="small"
        effect="dark"
        ><i-ep-edit-pen />
      </el-tag>
    </slot>
    <template #dropdown>
      <el-dropdown-menu>
        <template v-for="(item, index) in props.option" :key="index">
          <el-dropdown-item @click.stop="item.click(item)">
            {{ item.label }}
          </el-dropdown-item>
        </template>
        <el-dropdown-item v-if="props.isEditColor" divided>
          <input type="color" v-model="colorModel" @change="selectColor" />
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>
<style lang="scss" scoped></style>

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
const emit = defineEmits(['dropdown-click', 'color-change'])

const selectColor = () => {
  emit('color-change', colorModel)
}
onMounted(() => {
  console.log('props.option', props.option)
})
</script>
<template>
  <el-dropdown :trigger="props.trigger" :size="props.small">
    <slot>
      <el-tag plain :color="colorModel" size="small" @click.stop="() => {}" effect="dark"
        ><i-ep-edit-pen />
      </el-tag>
    </slot>
    <template #dropdown>
      <el-dropdown-menu>
        <template v-for="item in props.option">
          <el-dropdown-item
            v-if="item.hidden ? item.hidden() : true"
            @click.stop="item.click(item)"
          >
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

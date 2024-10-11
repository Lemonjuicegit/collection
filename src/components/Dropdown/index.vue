<script setup name="Dropdown">
const props = defineProps({
  option: {
    type: Object,
    default: () => ({})
  },
  isEditColor: {
    type: Boolean,
    default: false
  },
  trigger: {
    type: String,
    default: 'click'
  },
  isArrowIcon: {
    type: Boolean,
    default: false
  },
  color: {
    type: String,
    default: ''
  },
  width: {
    type: Number,
    default: 50
  }
})
const emit = defineEmits(['command', 'color-change'])

const handleCommand = (data) => {
  if (data.click) {
    data.click()
  }
  emit('command', data)
}
</script>
<template>
  <el-popover
    popper-style="display: flex;flex-direction: column;border: none;padding: 0;min-width: 80px;"
    placement="bottom"
    :width="props.width"
    :trigger="props.trigger"
  >
    <template #reference>
      <div @click.stop>
        <slot />
      </div>
    </template>
    <template v-for="item in props.option">
      <slot :name="item.name" :item="item">
        <el-button v-if="item.hidden ? item.hidden() : true" @click.stop="handleCommand(item)" text>
          {{ item.label }}
        </el-button>
      </slot>
    </template>
  </el-popover>
</template>
<style scoped>
.el-button {
  margin: 0;
}
</style>

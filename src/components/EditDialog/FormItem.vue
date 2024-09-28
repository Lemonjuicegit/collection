<script setup>
const props = defineProps({
  option: {
    type: Object,
    default: () => ({})
  },
  disabled: {
    type: Boolean,
    default: false
  },
  width: {
    type: [Number, String],
    default: '200px'
  }
})
const modelValue = defineModel()
const emit = defineEmits(['change'])
const change = (val) => {
  emit('change', val)
}
</script>
<template>
  <div>
    <el-input
      v-if="!props.option.type || props.option.type == 'text'"
      v-model="modelValue"
      :readonly="props.option.readonly"
      :disabled="disabled"
      clearable
      @input="change"
      :style="{ width: props.width }"
    />
  </div>
</template>
<style lang="scss" scoped></style>



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
const emit = defineEmits(['change', 'toCheck'])
const change = (val) => {
  emit('change', val)
}
const toCheck = () => {
  const value = event.target.value
  // isShow.value = !isShow.value
  if (
    (!value || !props.option.regex || props.option.regex.test(value)) &&
    props.option.emptyWarning
  ) {
    emit('to-check', event)
    // const isShow = ref(true)
  }
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
    @blur="toCheck" 
    :style="{width: props.width}"
    />
  </div>
</template>
<style lang="scss" scoped></style>
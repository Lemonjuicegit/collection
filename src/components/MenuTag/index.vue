<script setup name="MenuTag">
const props = defineProps({
  name: {
    type: String,
    default: ''
  },
  title: {
    type: String,
    default: ''
  },
  active: {
    type: String,
    default: ''
  }
})

const active = computed(() => {
  return props.name === props.active
})
const colorModel = defineModel('color', { default: '#b3e19d' })
const emit = defineEmits(['menu-click'])

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
const onClick = () => {
  emit('menu-click', { name: props.name, title: props.title })
}
</script>
<template>
  <div @click="onClick" :class="active ? 'node-item menu-tag' : 'menu-tag'">
    <span class="title">{{ props.title }}</span>
    <span style="margin: auto" />
    <slot name="interior" />
  </div>
  <slot name="outside" />
</template>
<style scoped>
.node-item {
  box-shadow: 0px 0px 5px 1px rgba(0, 0, 0, 0.3);
  border: 1px solid #79bbff;
}

.menu-tag {
  display: flex;
  width: 100%;
  padding: 3px 5px 3px 5px;
  background-color: v-bind('undertint(colorModel)');
  border-radius: 10px;
}
.title {
  padding-left: 10px;
  padding-right: 10px;
  background-color: v-bind(colorModel);
  border-radius: 30px;
}
</style>

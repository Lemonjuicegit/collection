<script setup>
// import { useStore } from '@/stores/store'
// const store = useStore()
onBeforeMount(() => {
  window.onbeforeunload = null
})
</script>
<template>
  <RouterView v-slot="{ Component }">
    <keep-alive>
      <component :is="Component"></component>
    </keep-alive>
  </RouterView>
</template>

<template>
    <div>
     <iframe :src="store.url" frameborder="0" width="100%" height="885px"></iframe>
    </div>
</template>

<script setup>
import { useStore } from '@/stores/store'
const store = useStore()
</script>

<style lang="scss" scoped>

</style>
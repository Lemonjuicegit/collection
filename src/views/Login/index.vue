<template>
    <div>

    </div>
</template>

<script setup>
import { useStore } from '@/stores/store'
const store = useStore()
onBeforeMount(async () => {
    await store.setUser()
    await store.setRouter()
})
</script>

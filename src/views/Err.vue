
<script setup>
import Error from '@/components/Error/index.vue'
const route = useRoute()
</script>
<template>
    <Error :code="route.meta.code" :msg="route.meta.msg" />
</template>

<style lang="scss" scoped></style>
<template>
    <div>
        <template v-for="item in tagsStore.list">
            <iframe v-show="item.name === tagsStore.active" :src="item.url" frameborder="0" width="100%" height="885px"
                name="iframe"></iframe>
        </template>
    </div>
</template>

<script setup>
import { useTagsStore } from '@/stores/tags'
const tagsStore = useTagsStore()
</script>

<style lang="scss" scoped></style>
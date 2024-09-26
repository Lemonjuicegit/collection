<template>
    <div>
        <template v-for="item in tagsStore.list">
            <iframe v-show="onShow(item.name)" :src="item.URL" frameborder="0" width="100%" height="100%"
                name="iframe"></iframe>
        </template>
    </div>
</template>
<script setup>
import { useTagsStore } from '@/stores/tags'
const tagsStore = useTagsStore()
const onShow = (name) => {
    return name === tagsStore.active
}
</script>

<style scoped>

</style>
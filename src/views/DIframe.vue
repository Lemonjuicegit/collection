<template>
    <div>
        <template v-for="item in tagsStore[xm_name].list">
            <iframe v-show="onShow(item.name)" :src="item.URL" frameborder="0" width="100%" height="100%"
                name="iframe"></iframe>
        </template>
    </div>
</template>
<script setup>
import { useTagsStore } from '@/stores/tags'
import { xm_name } from '@/config'
const tagsStore = useTagsStore()
const onShow = (name) => {
    return name === tagsStore[xm_name].active
}
</script>

<style scoped>

</style>
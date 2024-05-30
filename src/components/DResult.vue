<template>
    <div class="result">
        <el-progress  v-if="store.res_type === 1" :stroke-width="3" :percentage="store.percentage" :format="format" />
        <el-progress v-if="store.res_type === 2" :indeterminate="true" />
        <p>{{ store.res }}</p>
    </div>
</template>

<script setup>
const props = defineProps(['res_type','res','percentage'])
const format = (percentage) => (`${percentage}%`)
</script>

<style scoped>
.result {
    width: 100%;
    height: 20px;
}
</style>
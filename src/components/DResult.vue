<template>
    <transition name="el-fade-in-linear">
        <el-card>
            <el-progress v-if="props.type === 1" :stroke-width="3" :percentage="props.percentage" :format="format" />
            <el-progress v-if="props.type === 2" :stroke-width="3" :format="format" :percentage="100" :duration="5"
                :indeterminate="true" />
            <p>{{ props.res }}</p>
        </el-card>
    </transition>
</template>

<script setup>
const props = defineProps(['type', 'res', 'percentage'])
const format = (percentage) => { (percentage === 100 ? '正在处理' : `${percentage}%`) }
</script>

<style scoped>
.result {
    width: 100%;
    height: 20px
}
</style>
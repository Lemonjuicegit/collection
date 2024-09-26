
<script setup>
defineProps({
    code: {
        type: String,
        default: ""
    },
    msg: {
        type: String,
        default: ""
    }
})

</script>
<template>
    <el-result icon="error" :title="code" :sub-title="msg">
    </el-result>
</template>

<style lang="scss" scoped></style>
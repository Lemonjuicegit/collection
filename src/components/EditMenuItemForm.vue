<template>
    <div>
        <el-form size="small" :model="props.form" label-width="auto">
            <el-form-item label="节点名">
                <el-input v-model="props.form.title" />
            </el-form-item>
            <el-form-item label="URL">
                <el-input v-model="props.form.URL" />
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup>
const props = defineProps(['form'])
</script>

<style  scoped></style>
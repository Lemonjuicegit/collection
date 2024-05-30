<template>
    <div style="display: flex; align-items: center;">
        <el-upload ref="upload" :limit="1" :http-request="openFile" :on-exceed="handleExceed" :show-file-list="false" :accept="props.accept">
            <template #trigger>
                <el-button size="small">{{ props.text }}</el-button>
            </template>
        </el-upload>
        <span style="padding-right: 10px;">:</span>
        <el-tag v-if="state.tagif" size="small" effect="light" type="info" style="">{{ state.name }}</el-tag>
    </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { genFileId } from 'element-plus'
const props = defineProps(['onChange', 'text','accept'])
const upload = ref()
const state = reactive({
    tagif: false,
    name: '',
})
const handleExceed = (files) => {
    upload.value.clearFiles()
    const file = files[0]
    file.uid = genFileId()
    upload.value.handleStart(file)
    state.name = file.name
    state.tagif = true
    props.onChange(file)
}
const openFile = async (file) => {
    state.name = file.file.name
    state.tagif = true
    props.onChange(file.file)
}
</script>

<style scoped></style>
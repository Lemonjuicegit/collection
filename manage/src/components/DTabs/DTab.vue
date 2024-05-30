<template>
    <div>
        <el-form ref="form" :model="formdata" label-width="auto" label-position="top">
            <el-form-item>
                <el-button color="#626aef" :plain="true" type="primary" @click="onSubmit"
                    :loading="loadingSave">保存</el-button>
            </el-form-item>
            <el-form-item label="标题">
                <el-input v-model="formdata.title" />
            </el-form-item>
            <el-form-item label="可执行的操作">
                <el-checkbox-group v-model="formdata.operate">
                    <el-checkbox label="1">删除网址</el-checkbox>
                    <el-checkbox label="2">修改网址名</el-checkbox>
                    <el-checkbox label="4">添加网址</el-checkbox>
                </el-checkbox-group>
            </el-form-item>
            <el-form-item label="添加网址">
                <el-table :data="formdata.tableData" style="width: 100%;">
                    <el-table-column prop="name" label="名称" width="150">
                        <template #default="scope">
                            <el-input type="text" v-model="scope.row.title" clearable />
                        </template>
                    </el-table-column>
                    <el-table-column prop="URL" label="地址">
                        <template #default="scope">
                            <el-input type="text" v-model="scope.row.URL" clearable />
                        </template>
                    </el-table-column>
                    <el-table-column fixed="right" label="" width="60">
                        <template #default="scope">
                            <el-popconfirm title="是否删除" cancel-button-text="取消" confirm-button-text="确认"
                                @confirm="remURL(scope.row)">
                                <template #reference>
                                    <el-button size="small" type="danger">删除</el-button>
                                </template>
                            </el-popconfirm>
                        </template>
                    </el-table-column>
                    <el-table-column fixed="right" label="" width="60">
                        <template #default="scope">
                            <el-link :href="scope.row.URL" target="_blank" type="success">跳转</el-link>
                        </template>
                    </el-table-column>
                </el-table>
                <el-button class="mt-4" style="width: 100%;font-size: 20px;" @click="onAddItem">+</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup>
/**
 * @
*/
import { ref, reactive, onBeforeMount, watch  } from 'vue'
import permissions from '@/config'
import api from '@/api'
import { uuid } from '@/utils'
const loadingSave = ref(false)
const formdata = reactive({
    title: '',
    operate: [],
    tableData: []
})
onBeforeMount(() => {
    permissions.forEach(item => {
        if ((props.permissions & item) === item) {
            formdata.operate.push(String(item))
        }
    })
    formdata.title = props.title
    formdata.tableData = props.data
})

const props = defineProps(['permissions', 'data', 'title'])
watch(() => props, () => {
    permissions.forEach(item => {
        if ((props.permissions & item) === item) {
            formdata.operate.push(String(item))
        }
    })
    formdata.title = props.title
    formdata.tableData = props.data
}, { deep: true })
const onSubmit = async () => {
    loadingSave.value = true
    let per = 0
    formdata.operate.forEach(item => {
        per = parseInt(item) | per
    })
    await api.reviseMenuitemURL(props.xmname, {
        data: formdata.tableData.map(item => ({ title: item.title, name: item.name, URL: item.URL, path: '/iframe' })),
        title: formdata.title,
        permissions: per
    })
    ElMessage({
        message: '保存成功',
        type: 'success',
    })
    loadingSave.value = false
}
const onAddItem = () => {
    let id = uuid()
    formdata.tableData.push({
        title: '',
        name: id,
        URL: '',
    })
}
const remURL = (item) => {
    formdata.tableData = formdata.tableData.filter(v => v.name !== item.name)
}
</script>

<style lang="scss" scoped></style>
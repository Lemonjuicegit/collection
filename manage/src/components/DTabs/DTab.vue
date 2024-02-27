<template>
    <div>
        <el-form ref="form" :model="formdata" label-width="auto" label-position="top" size="small">
            <el-form-item>
                <el-button type="primary" @click="onSubmit">保存</el-button>
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
                    <el-table-column fixed="right"  label="" width="80">
                        <template #default="scope">
                            <el-button size="small" type="danger"
                                @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <el-button class="mt-4" style="width: 100%;font-size: 20px;" @click="onAddItem">+</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup>
import { ref, reactive, onBeforeMount } from 'vue'
import { useStore } from '@/stores/store'
import permissions from '@/config'
import api from '@/api'
import { uuid } from '@/utils'
const store = useStore()
const formdata = reactive({
    title: '',
    operate: [],
    tableData: []
})
const props = defineProps(['xmname'])
onBeforeMount(() => {
    console.log(store.menuitemURL)
    permissions.forEach(item => {
        if ((store.menuitemURL[props.xmname].permissions & item) === item) {
            formdata.operate.push(String(item))
        }
    })
    formdata.title = store.menuitemURL[props.xmname].title
    formdata.tableData = store.menuitemURL[props.xmname].menuitemURL.map(item => ({ title: item.title,name: item.name, URL: item.URL }))
})
const onSubmit = async () => {
    let per = 0
    formdata.operate.forEach(item => {
        per = parseInt(item) | per
    })
    api.reviseMenuitemURL(props.xmname, {
        menuitemURL: formdata.tableData,
        title: formdata.title,
        permissions: per
    })
}
const onAddItem = () => {
    let id = uuid()
    formdata.tableData.push({
        title: '',
        name: id,
        URL: ''
    })
}
</script>

<style lang="scss" scoped></style>
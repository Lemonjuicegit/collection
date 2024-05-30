<template>
    <div style="padding: 20px 20px 20px 20px;">
        <el-card style="max-width: 1500px;">
            <template #header>
                <div class="card-header">
                    <el-button @click="open1" size="small" type="success" plain>确认</el-button>
                    <h3>
                        不动产登记数据质量提升exf
                    </h3>
                </div>
            </template>
            <d-upload text="gdb数据库" :on-change="openFile" />
        </el-card>
        <div style="height: 10px;"></div>
        <el-card style="max-width: 1500px">
            <template #header>
                <div class="card-header">
                    <el-button @click="open1" size="small" type="success" plain>确认</el-button>
                    <h3>
                        LQ-exf
                    </h3>
                </div>
            </template>
            <d-upload text="gdb数据库" :on-change="openFile" />
        </el-card>
        <div style="height: 10px;"></div>
        <el-card style="max-width: 1500px">
            <template #header>
                <div class="card-header">
                    <el-button @click="open1" size="small" type="success" plain>确认</el-button>
                    <h3>
                        LF-exf
                    </h3>
                </div>
            </template>
            <d-upload text="gdb数据库" :on-change="openFile" />
        </el-card>
    </div>
</template>

<script setup>
import { ElNotification } from 'element-plus'
import { h } from 'vue'
import DUpload from '@/components/DUpload.vue'
import DResult from '@/components/DResult.vue'
import api from '@/api'
const openFile = async (file) => {
    await api.upload(file, 'gdb')
    let gdbname = file.name.split('.')[0]
    console.log(gdbname)
    ElMessage({
        showClose: true,
        message: '上传数据成功',
        type: 'success',
        duration: 5000,
    })
}
const open1 = () => {
    ElNotification({
        title: 'Title',
        message: h('i', { style: 'color: teal' }, 'This is a reminder'),
        duration: 0,
    })
}
</script>

<style scoped>
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

</style>
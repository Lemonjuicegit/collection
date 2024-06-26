<template>
    <div style="display: flex;flex-flow: column ;justify-content: space-between">
        <div style="padding: 20px 20px 20px 20px;">
            <el-card style="max-width: 1500px;">
                <template #header>
                    <div class="card-header">
                        <el-button @click="onHcExf" size="small" type="success" plain>确认</el-button>
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
                        <el-button @click="onLqExf" size="small" type="success" plain>确认</el-button>
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
        <d-result :type="state.resType" :res="state.res" :percentage="state.percentage" />
    </div>
</template>

<script setup>
import {reactive } from 'vue'
import DUpload from '@/components/DUpload.vue'
import DResult from '@/components/DResult.vue'
import api from '@/api'
import exf_api from '@/api/exf_api'
const state = reactive({
    resType: 0,
    res: '',
    percentage: 0,
    gdbname: '',
    apiState: 0,
})
const openFile = async (file) => {
    await api.upload(file, 'gdb')
    state.gdbname = file.name.split('.')[0]
    ElMessage({
        showClose: true,
        message: '上传数据成功',
        type: 'success',
        duration: 5000,
    })
}
const onLqExf = async () => {
    let whilestate = 0
    while (whilestate !== 1) {
        let res = await exf_api.lqexf(`${state.gdbname}.gdb`, state.apiState)
        state.resType = 2
        state.apiState = res.data.state
        switch (state.apiState) {
            case -1:
                state.res = res.data.res
                state.resType = 0
                break
            case 1:
                state.res = res.data.res
                state.resType = 2
                break
            case 2:
                state.res = '完成!'
                await api.download('林权exf', '林权exf.zip')
                state.resType = 0
                whilestate = 1
                break
            default:
                state.res = '出现了意外的情况!'
                state.resType = 0
                whilestate = 1
                break
        }

    }
}
const onHcExf = async () => {
    let whilestate = 0
    while (whilestate !== 1) {
        let res = await exf_api.hcexf(`${state.gdbname}.gdb`, state.apiState)
        state.resType = 2
        state.apiState = res.data.state
        switch (state.apiState) {
            case -1:
                state.res = res.data.res
                state.resType = 0
                break
            case 1:
                state.res = res.data.res
                state.resType = 2
                break
            case 2:
                state.res = '完成!'
                await api.download('合川exf数据', '合川exf数据.zip')
                state.resType = 0
                whilestate = 1
                break
            default:
                state.res = '出现了意外的情况!'
                state.resType = 0
                whilestate = 1
                break
        }

    }
}
const open1 = () => {

}
</script>

<style scoped>
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>
<template>
    <el-tabs v-model="store[xm_name].ediTabsValue" type="card" closable @tab-remove="removeTab" style="padding: 5px;">
        <el-tab-pane v-for="item in store[xm_name].urlarr" :key="item.name" :label="item.title" :name="item.name">
            <template #label><span class="my-label">{{ item.title }}</span></template>
            <iframe :src="item.url" frameborder="0" width="100%" height="885px"></iframe>
        </el-tab-pane>
    </el-tabs>
</template>

<script setup>
import { useStore } from '@/stores/store'
import {xm_name} from '@/config'
const store = useStore()
const removeTab = (targetName) => {
    const tabs = store[xm_name].urlarr
    let activeName = store[xm_name].ediTabsValue
    store[xm_name].menuitem[targetName] = false
    if (activeName === targetName) {
        tabs.forEach((tab, index) => {
            if (tab.name === targetName) {
                const nextTab = tabs[index + 1] || tabs[index - 1]
                if (nextTab) {
                    activeName = nextTab.name
                }
            }
        })
    }
    store[xm_name].ediTabsValue = activeName
    store[xm_name].urlarr = tabs.filter((tab) => tab.name !== targetName)
}
</script>

<style scoped>
.my-label {
  font-size: 15px;
}
</style>
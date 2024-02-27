<template>
    <el-tabs v-model="store.ediTabsValue" type="card" closable @tab-remove="removeTab" style="padding: 5px;">
        <el-tab-pane v-for="item in store.urlarr" :key="item.name" :label="item.title" :name="item.name">
            <template #label><span class="my-label">{{ item.title }}</span></template>
            <DTab :xmname="item.title"/>
        </el-tab-pane>
    </el-tabs>
</template>

<script setup>
import { useStore } from '@/stores/store'
import DTab from './DTab.vue'
const store = useStore()
const removeTab = (targetName) => {
    const tabs = store.urlarr
    let activeName = store.ediTabsValue
    store.menuitem[targetName] = false
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
    store.ediTabsValue = activeName
    store.urlarr = tabs.filter((tab) => tab.name !== targetName)
}
</script>

<style scoped>
.my-label {
    font-size: 15px;
}
</style>
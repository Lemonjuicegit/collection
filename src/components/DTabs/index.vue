<template>
    <el-tabs v-model="store.editableTabsValue" type="card" closable @tab-remove="removeTab" style="padding: 5px;">
        <el-tab-pane v-for="item in store.urlarr" :key="item.name" :label="item.title" :name="item.name">
            <template #label><span class="my-label">{{ item.title }}</span></template>
            <iframe :src="item.url" frameborder="0" width="100%" height="885px"></iframe>
        </el-tab-pane>
    </el-tabs>
</template>

<script setup>
import { useStore } from '@/stores/counter'
const store = useStore()
const removeTab = (targetName) => {
    const tabs = store.urlarr
    let activeName = store.editableTabsValue
    console.log(targetName)
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
    store.editableTabsValue = activeName
    store.urlarr = tabs.filter((tab) => tab.name !== targetName)
}
</script>

<style scoped>
.my-label {
  font-size: 15px;
}
</style>
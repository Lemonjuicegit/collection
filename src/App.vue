<script setup>
import { ref, reactive } from 'vue'
import DTabs from '@/components/DTabs/index.vue'
import { useStore } from '@/stores/counter'
const store = useStore()
const addTab = (targetName,url) => {
  if(store.menuitem[targetName]){
    store.editableTabsValue = targetName
  }else{
    store.menuitem[targetName] = true
    store.urlarr.push({
      title: targetName,
      name: targetName,
      url
    })
    store.editableTabsValue = targetName
  }
}
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="200px" height="100vh" style="display: flex;flex-flow: row wrap;">
        <el-menu  @open="handleOpen" @close="handleClose" style="align-self: flex-start;">
          <el-menu-item :index="U.name" @click="() => addTab(U.name, U.URL)" v-for="U in store.menuitemURL">
            {{ U.name }}
          </el-menu-item>
        </el-menu>
        <el-button>sdsas</el-button>
      </el-aside>
      <el-main>
        <d-tabs />
      </el-main>
    </el-container>
  </div>
</template>

<style scoped></style>

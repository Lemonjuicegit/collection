<script setup>
import { ref, reactive, onBeforeMount } from 'vue'
import { useDraggable } from 'vue-draggable-plus'
import Tabs from '@/components/DTabs/tags.vue'
import DMenu from '@/components/DMenu/DMenu.vue'
import { DeleteFilled, EditPen } from '@element-plus/icons-vue'
import { useStore } from '@/stores/store'
import { useTagsStore } from '@/stores/tags'
import { xm_name, permissions } from '@/config'
import { uuid } from '@/utils'
import api from '@/api'
const store = useStore()
const tagsStore = useTagsStore()
const ruleFormRef = ref()
const draggable = ref()
const Nopage = ref(false)
const titleName = ref('')
const delURL = ref(false)
const editURLName = ref(false)
const addURL = ref(false)
const menuitemURL = ref([])
const ruleForm = reactive({
    name: '',
    url: ''
})
onBeforeMount(async () => {
    let res = await api.getmenuitemURL()
    if (!res.data) {
        Nopage.value = true
        return
    }
    menuitemURL.value = res.data.map((item) => {
        return {
            ...item,
            editName: false,
        }
    })
    store[xm_name].menuitem = []
    menuitemURL.value.forEach(item => {
        store[xm_name].menuitem[item.name] = false
    })
    store[xm_name].urlarr.forEach(item => {
        store[xm_name].menuitem[item.name] = true
    })
    store[xm_name].permissions = (await api.getPermissions()).data
    permissions.forEach(item => {
        if ((item & store[xm_name].permissions) === 4) {
            addURL.value = true
        } else if ((item & store[xm_name].permissions) === 1) {
            delURL.value = true
        } else if ((item & store[xm_name].permissions) === 2) {
            editURLName.value = true
        }
    })
    res = await api.getTitle()
    titleName.value = res.data
})
const addTab = (title, name, url, path) => {
    tagsStore[xm_name].active = name
    const isExist = tagsStore[xm_name].list.map(item => item.name).some((item) => {
        return item === name
    })
    if (!isExist) {
        tagsStore[xm_name].list.push({ name, title, path })
    }
    if (!store[xm_name].menuitem[name]) {
        store[xm_name].menuitem[name] = true
        store[xm_name].urlarr.push({
            title,
            name,
            url,
            path
        })
    }
    console.log(tagsStore[xm_name].list)
    store[xm_name].ediTabsValue = name
}

const submitForm = async (formEl) => {
    if (!formEl) return
    let key = uuid()
    store[xm_name].menuitem[key] = false
    menuitemURL.value.push({
        title: ruleForm.name,
        name: key,
        URL: ruleForm.url,
        path: '/iframe',
        editName: false,
    })
    await api.addmenuitemURL({
        title: ruleForm.name,
        name: key,
        URL: ruleForm.url,
        path: '/iframe'
    })
}
const remMenuItem = async (index, targetName) => {
    menuitemURL.value = menuitemURL.value.filter((item) => item.name !== menuitemURL.value[index].name)
    await api.delmenuitemURL(index)
    const tabs = store[xm_name].urlarr
    let activeName = store[xm_name].ediTabsValue
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
const EditMenuItemName = async (index) => {
    menuitemURL.value[index].editName = true
}
const setMenuItemName = async (index) => {
    menuitemURL.value[index].editName = false
    await api.setmenuitemName(index, menuitemURL.value[index].title)
}

useDraggable(draggable, menuitemURL, {
    animation: 150,
    async onUpdate() {
        await api.upmenuitemURL(menuitemURL.value.map(v => {
            return {
                title: v.title,
                name: v.name,
                URL: v.URL,
                path: v.path
            }
        }))
    }
})

const onTagsClick = (name) => {
    tagsStore[xm_name].active = name
}

const closeTags = (curItem) => {
    tagsStore[xm_name].list = curItem
}
</script>
<template>
    <div class="common-layout" style="height:100%">
        <el-result v-if="Nopage" icon="error" title="页面不存在" />
        <el-container style="height:100%">
            <el-aside width="200px" height="100%" style="display: flex;flex-direction: column ;background-color:#D4D7DE;">
                <h1 v-if="!store[xm_name].edititle" style="padding: 10px; color: #000000; text-align: center">{{ titleName
                }}</h1>
                <el-menu background-color="#D4D7DE" text-color="#fff" active-text-color="#ffd04b"
                    class="el-menu-vertical-demo" style="height: 880px;">
                    <div ref="draggable">
                        <template v-for="(U, index) in menuitemURL">
                            <el-menu-item v-if="U.level === 1" el-menu-item style="padding: 1px;height: 40px; "
                                :index="U.name" v-for="(U, index) in menuitemURL">
                                <el-popconfirm v-if="delURL" title="是否删除" cancel-button-text="取消" confirm-button-text="确认"
                                    @confirm="remMenuItem(index, U.name)">
                                    <template #reference>
                                        <el-button circle type="danger" :icon="DeleteFilled" size="small" />
                                    </template>
                                </el-popconfirm>
                                <el-button v-if="editURLName" @click="EditMenuItemName(index)" :icon="EditPen" circle
                                    type="primary" size="small" />
                                <div style="padding: 2px;"></div>
                                <el-button v-if="!U.editName" @click="addTab(U.title, U.name, U.URL, U.path)" text
                                    color="#E6A23C"><router-link :to="U.path">{{ U.title }}</router-link></el-button>
                                <el-input v-if="U.editName" @blur="setMenuItemName(index)"
                                    v-model="menuitemURL[index].title" />
                            </el-menu-item>
                            <el-sub-menu v-else :index="U.name">
                                <template v-for="(Child, index) in U.data">

                                </template>
                            </el-sub-menu>
                        </template>
                    </div>
                </el-menu>
                <el-popover placement="top" :width="180" style="align-self: flex-end">
                    <el-form ref="ruleFormRef" :model="ruleForm" status-icon>
                        <el-form-item label="名字">
                            <el-input v-model="ruleForm.name" />
                        </el-form-item>
                        <el-form-item label="网址">
                            <el-input v-model="ruleForm.url" />
                        </el-form-item>
                    </el-form>
                    <div style="text-align: right; margin: 0">
                        <el-button size="small" @click="submitForm(ruleFormRef)">确认</el-button>
                    </div>
                    <template #reference>
                        <el-button v-if="addURL" size="small"
                            style="background-color:#D4D7DE; color: #000000">添加网址</el-button>
                    </template>
                </el-popover>
            </el-aside>
            <el-main style="padding: 5px;">
                <Tabs :list="tagsStore[xm_name].list" :active="tagsStore[xm_name].active" @tags-click="onTagsClick"
                    @close-tags="closeTags" />
                <div class="content" style="height: 95%;">
                    <router-view v-slot="{ Component }">
                        <transition name="move" mode="out-in">
                            <keep-alive>
                                <component style="height: 100%;" :is="Component"></component>
                            </keep-alive>
                        </transition>
                    </router-view>
                </div>
            </el-main>
        </el-container>
    </div>
</template>

<style scoped>
.move-enter-active,
.move-leave-active {
    transition: opacity 1s ease;
}

.move-enter-from,
.move-leave-to {
    opacity: 0;
}
</style>

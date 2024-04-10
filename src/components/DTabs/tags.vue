<template>
	<div class="tags" v-if="tagsStore.show">
		<ul>
			<li class="tags-li" v-for="(item, index) in tagsStore.list" :class="{ active: isActive(item.name) }" :key="index"
				@click="setUrl(item.name)">
				<router-link to="/iframe">{{ item.title }}</router-link>
				<el-icon @click="closeTags(index)">
					<Close />
				</el-icon>
			</li>
		</ul>
		<div class="tags-close-box">
			<el-dropdown @command="handleTags">
				<el-button size="small" type="primary">
					标签选项
					<el-icon class="el-icon--right">
						<arrow-down />
					</el-icon>
				</el-button>
				<template #dropdown>
					<el-dropdown-menu size="small">
						<el-dropdown-item command="other">关闭其他</el-dropdown-item>
						<el-dropdown-item command="all">关闭所有</el-dropdown-item>
					</el-dropdown-menu>
				</template>
			</el-dropdown>
		</div>
	</div>
</template>

<script setup>
import { useTagsStore } from '@/stores/tags';
import { useStore } from '@/stores/store';
import { useRoute, useRouter } from 'vue-router';
import { Close, ArrowDown } from '@element-plus/icons-vue'
const route = useRoute();
const router = useRouter();
const store = useStore()
const tagsStore = useTagsStore();
const isActive = (name) => {
	console.log(name)
	console.log(tagsStore.active)
	return name === tagsStore.active;
};
const setUrl = (name) => {
	tagsStore.active = name
}
// 关闭单个标签
const closeTags = (index) => {
	
	// tagsStore.active = tagsStore.list[index-2].name
	tagsStore.delTagsItem(index);
};

// 关闭全部标签
const closeAll = () => {
	tagsStore.clearTags();
};
// 关闭其他标签
const closeOther = () => {
	const curItem = tagsStore.list.filter(item => {
		return item.name === tagsStore.active;
	});
	tagsStore.closeTagsOther(curItem);
};
const handleTags = (command) => {
	command === 'other' ? closeOther() : closeAll();
};

// 关闭当前页面的标签页
// tags.closeCurrentTag({
//     $router: router,
//     $route: route
// });
</script>

<style>
.tags {
	position: relative;
	height: 30px;
	overflow: hidden;
	background: #fff;
	padding-right: 120px;
	box-shadow: 0 5px 10px #ddd;
}

.tags ul {
	box-sizing: border-box;
	width: 100%;
	height: 100%;
}

.tags-li {
	display: flex;
	align-items: center;
	float: left;
	margin: 3px 5px 2px 3px;
	border-radius: 3px;
	font-size: 12px;
	overflow: hidden;
	cursor: pointer;
	height: 23px;
	border: 1px solid #e9eaec;
	background: #fff;
	padding: 0 5px 0 12px;
	color: #666;
	-webkit-transition: all 0.3s ease-in;
	-moz-transition: all 0.3s ease-in;
	transition: all 0.3s ease-in;
}

.tags-li:not(.active):hover {
	background: #f8f8f8;
}

.tags-li.active {
	color: #fff;
	background-color: var(--el-color-primary);
}

.tags-li-title {
	float: left;
	max-width: 80px;
	overflow: hidden;
	white-space: nowrap;
	text-overflow: ellipsis;
	margin-right: 5px;
	color: #666;
}

.tags-li.active .tags-li-title {
	color: #fff;
}

.tags-close-box {
	position: absolute;
	right: 0;
	top: 0;
	box-sizing: border-box;
	padding-top: 1px;
	text-align: center;
	width: 110px;
	height: 30px;
	background: #fff;
	box-shadow: -3px 0 15px 3px rgba(0, 0, 0, 0.1);
	z-index: 10;
}
</style>

<template>
	<div class="tags">
		<ul>
			<li class="tags-li" v-for="(item, index) in list" :class="{ active: isActive(item.name) }" :key="index">
				<router-link :to="item.path" @click="handleClick(item.name)">{{ item.title }}</router-link>
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
import { Close, ArrowDown } from '@element-plus/icons-vue'
const active = defineModel('active')
const list = defineModel('list')
const emit = defineEmits(['tags-click', 'close', 'close-tags']);


const isActive = (name) => {
	return name === active.value
}

const handleClick = (name) => {
	active.value = name
	emit('tags-click', name)
}

// 关闭单个标签
const closeTags = (index) => {
	const delItem = list.value[index]
	list.value.splice(index, 1)
	if (active.value === delItem.name) {
		const item = list.value[index]
			? list.value[index]
			: list.value[index - 1]
		active.value = item.name
		emit('close', item)
	} else {
		emit('close', 0)
	}
}

// 关闭全部标签
const closeAll = () => {
	list.value = []
	emit('close-tags', [])
}
// 关闭其他标签
const closeOther = () => {
	const curItem = list.value.filter(item => {
		return item.name === active.value;
	});
	list.value = curItem
	emit('close-tags', curItem)
}
const handleTags = (command) => {
	command === 'other' ? closeOther() : closeAll();
}
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

<script setup>
import FormItem from './FormItem.vue'
const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  options: {
    type: Array,
    default: []
  },
  formData: {
    type: Object,
    default: () => ({})
  },
  formRules: {
    type: Array,
    default: () => []
  },

})
const model = defineModel({ default: false })
const formData = defineModel('data')
const emit = defineEmits(['submit'])
const submit = (formData) => {
  model.value = false
  emit('submit', formData)
}
const toCheck = (formItem, event)=> {
  const child = document.createElement('div')
  child.id = 'spaceWarn'
  child.style.color = 'var(--el-color-warning)'
  child.style.fontSize = '10px'
  child.style.position = 'absolute'
  child.style.marginTop = '15px'
  child.textContent = '输入内容包含空格'
  const data = event.target.value
  const judgeSpace = new RegExp(/\s+/g)
  if (data != '') {
    if (formItem.type == undefined) {
      if (judgeSpace.test(data)) {
        event.target.offsetParent.style.boxShadow = '0 0 0 1px var(--el-color-warning) inset'
        if (event.target.labels[0].children.length < 1) {
          event.target.labels[0].append(child)
        }
      } else {
        event.target.offsetParent.style.boxShadow = ''
        const childrenlist = event.target.labels[0].children
        for (var i = 0; i < childrenlist.length; i++) {
          if (childrenlist[i].id == 'spaceWarn') {
            event.target.labels[0].children[i].remove()
          }
        }
      }
    } else if (formItem.type == 'textarea') {
      if (judgeSpace.test(data)) {
        event.target.style.boxShadow = '0 0 0 1px var(--el-color-warning) inset'
        if (event.target.labels[0].children.length < 1) {
          event.target.labels[0].append(child)
        }
      } else {
        event.target.style.boxShadow = ''
        const childrenlist = event.target.labels[0].children
        for (var i = 0; i < childrenlist.length; i++) {
          if (childrenlist[i].id == 'spaceWarn') {
            event.target.labels[0].children[i].remove()
          }
        }
      }
    }
  } else {
    if (formItem.type == undefined) {
      event.target.offsetParent.style.boxShadow = ''
      const childrenlist = event.target.labels[0].children
      for (var i = 0; i < childrenlist.length; i++) {
        if (childrenlist[i].id == 'spaceWarn') {
          event.target.labels[0].children[i].remove()
        }
      }
    } else if (formItem.type == 'textarea') {
      event.target.style.boxShadow = ''
      const childrenlist = event.target.labels[0].children
      for (var i = 0; i < childrenlist.length; i++) {
        if (childrenlist[i].id == 'spaceWarn') {
          event.target.labels[0].children[i].remove()
        }
      }
    }
  }
}
</script>
<template>
  <el-dialog v-model="model" :title="props.title" :close-on-click-modal="false" :draggable="true" buttonSize="small">
    <el-form ref="formRef" :model="formData" :rules="formRules" :inline="true">
      <el-row>
        <el-col v-for="(formItem, index) in props.options" :key="index" :span="formItem.span || 8">
          <slot :name="`${formItem.prop}-full`" :formData="formData">
            <el-form-item :label="formItem.label" :prop="formItem.prop">
              <slot :name="formItem.prop" :formData="formData">
                <FormItem :width="formItem.width" :option="formItem" v-model="formData[formItem.prop]"
                  :disabled="formItem.disabled" @to-check="toCheck(formItem, $event)" />
              </slot>
            </el-form-item>
          </slot>
          </el-col>
        </el-row>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="submit(formData)">确认</el-button>
        <el-button type="primary" @click="model = false">
          取消
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style lang="scss" scoped></style>

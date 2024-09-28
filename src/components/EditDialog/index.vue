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
                  :disabled="formItem.disabled"/>
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

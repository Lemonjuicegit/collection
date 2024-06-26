import api from '../api'
export default async (app, perint) => {
  const per = [
    { name: 'delURL', value: 1 },
    { name: 'edit', value: 2 },
    { name: 'addURL', value: 4 },
    { name: 'addGroup', value: 8 },
  ]
  perint = (await api.getPermissions()).data
  app.directive('permission', {
    beforeMount(el, binding) {
      // 当指令第一次绑定到元素时调用
      const permission = binding.value // 获取绑定到指令的值，即权限名称
      const hasPermission = per
        .map(item => {
            if((item.value & perint) === item.value){
                return item.name
        }})
        .includes(permission)
      // 如果用户没有权限，则隐藏元素
      if (!hasPermission) {
        el.remove()
      }
    }
  })
}

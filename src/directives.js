export const propagation = {
  // 当被绑定的元素插入到DOM中时……
  inserted: function (el, binding, vnode) {
    // 这里监听所有类型的事件，但你可以根据需要调整它（例如，只监听点击事件）
    el.addEventListener(
      'click',
      function (e) {
        // 阻止事件冒泡
        e.stopPropagation()

        // 如果绑定值是一个函数，则在阻止冒泡后执行它
        if (typeof binding.value === 'function') {
          binding.value(e)
        }
      },
      true
    ) // 使用捕获模式（如果必要）
  }
}

// import api from '../api'
// export default async (app, perint) => {
//   const per = [
//     { name: 'delURL', value: 1 },
//     { name: 'edit', value: 2 },
//     { name: 'addURL', value: 4 },
//     { name: 'addGroup', value: 8 }
//   ]
//   perint = (await api.getPermissions()).data
//   app.directive('permission', {
//     beforeMount(el, binding) {
//       // 当指令第一次绑定到元素时调用
//       const permission = binding.value // 获取绑定到指令的值，即权限名称
//       const hasPermission = per
//         .map((item) => {
//           if ((item.value & perint) === item.value) {
//             return item.name
//           }
//         })
//         .includes(permission)
//       // 如果用户没有权限，则隐藏元素
//       if (!hasPermission) {
//         el.remove()
//       }
//     }
//   })
// }

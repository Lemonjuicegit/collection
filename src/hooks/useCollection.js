import { getDelId, filterEmptyValues } from '@/utils'
import api from '@/api/manage'
const useCollection = () => {
  const hooks = {
    message(text, callback) {
      return ElMessageBox.confirm(text, {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(async () => {
          await callback()
          ElMessage({
            type: 'success',
            message: '成功!'
          })
        })
        .catch((res) => {
          ElMessage({
            type: 'info',
            message: '已取消'
          })
        })
    },
    async collAdd(add_type, item) {
      let res
      const sort = item.dataItem
        ? item.dataItem.length + 1
        : item.children
          ? item.children.length + 1
          : 1
      if (add_type === 'router') {
        res = await api.add('routerController', { title: '新建路由', router_type: 'collection' })
      } else if (add_type === 'dataItem') {
        let data = {
          title: '新网址',
          path: '/iframe',
          parent_name: item.is_group ? item.name : 'top',
          router_name: item.router_name ? item.router_name : item.name,
          is_group: false,
          sort
        }
        res = await api.add('dataItemController', data)
      } else if (add_type === 'groupItem') {
        let data = {
          title: '新建分组',
          parent_name: item.is_group ? item.name : 'top',
          router_name: item.router_name ? item.router_name : item.name,
          is_group: true,
          sort
        }
        res = await api.add('dataItemController', data)
      }
      if (item.is_group) {
        item.children = item.children || []
        item.children.push(res.data[0])
      } else if (item.dataItem) {
        item.dataItem.push(res.data[0])
      } else {
        let routerRes = res.data[0]
        item[routerRes.name] = {
          ...routerRes,
          dataItem: []
        }
      }
    },
    collDel(option) {
      const { del_type, item, dataItemModel, node, dataTree } = option
      if (del_type === 'router') {
        hooks.message('这将会删除该路由下所有的数据,是否确认删除?', async () => {
          await api.del('dataItemController', [item.id])
          let select_data = await api.select('dataItemController', { router_name: item.name })
          let dataItemIds = select_data.map((d) => d.id)
          if (dataItemIds) await api.del('dataItemController', dataItemIds)
          await api.del('routerController', [item.id])
          delete dataTree[item.name]
        })
      } else if (del_type === 'dataItem') {
        hooks.message('确认删除?', async () => {
          let ids = getDelId(item)
          await api.del('dataItemController', ids)
          const parent = node.parent
          const children = parent.data.children || parent.data
          const index = children.findIndex((d) => d.id === item.id)
          children.splice(index, 1)
          dataItemModel.dataItem = [...dataItemModel.dataItem]
        })
      }
    },
    async collEdit(edit_type, item) {
      let data = filterEmptyValues(item)
      if (edit_type === 'router') {
        await api.update('routerController', data)
      } else if (edit_type === 'dataItem') {
        await api.update('dataItemController', data)
      }
    }
  }
  return hooks
}
export default useCollection

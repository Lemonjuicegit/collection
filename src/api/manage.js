import request from './request'

export default {
  getRouterList: () =>
    request.get({
      url: '/collection/routerController/list'
    }),
  getDataTree: () =>
    request.get({
      url: '/collection/routerController/tree'
    }),
  getUser: () => {
    return request.get({ url: '/get_user' })
  },
  getRouter: (path) => {
    return request.post({
      url: '/collection/routerController/router',
      data: { path }
    })
  },
  dataItemList: () => {
    return request.get({
      url: '/collection/dataItemController/list'
    })
  },
  getItemTree: (router_path) => {
    return request.get({
      url: `/collection/routerController/item_tree?args=${router_path}`
    })
  },
  select: (apiUrl, data) => {
    return request.post({
      url: `/collection/${apiUrl}/select`,
      data
    })
  },
  update: (apiUrl, data) => {
    return request.post({
      url: `/collection/${apiUrl}/update`,
      data
    })
  },
  add: (apiUrl, data) => {
    return request.post({
      url: `/collection/${apiUrl}/add`,
      data
    })
  },
  del: (apiUrl, data) => {
    return request.delete({
      url: `/collection/${apiUrl}/delete`,
      data
    })
  },
  eqPath: (path) => {
    return request.get({
      url: `/collection/routerController/eq_path?path=${path}`
    })
  }
}

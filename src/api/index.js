import axios from 'axios'
import { saveAs } from 'file-saver'
import request from './request'
import { config } from './config'

const { base_url, xm_name } = config
const api = {
  add_use: () => axios.post(`${base_url}/add_use`),
  upload: (file, filetype = '') => {
    const formData = new FormData()
    formData.append('file', file)
    return axios.post(`${base_url}/upload?filetype=${filetype}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  download: (fileArr, filename) =>
    axios({
      url: `${base_url}/download?filename=${fileArr}`,
      method: 'post',
      responseType: 'blob',
      headers: {
        'Content-Type': 'octet-stream;charset=UTF-8'
      }
    }).then((req) => {
      if (req.data === 404) {
        ElMessage({
          type: 'info',
          message: '没有找到下载的文件'
        })
        return
      }
      saveAs(req.data, filename)
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
  getItemTree: (router_name) => {
    return request.post({
      url: '/collection/routerController/item_tree',
      data: { router_name }
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
export default api

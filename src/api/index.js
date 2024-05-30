import axios from 'axios'
import {xm_name} from '@/config'
import { saveAs } from 'file-saver'
const api = {
  upload: (file, filetype = '') => {
  const formData = new FormData()
  formData.append('file', file)
  return axios.post(`/api/upload?filetype=${filetype}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
},
download : (fileArr, filename) =>
  axios({
    url: `/api/download?filename=${fileArr}`,
    method: 'post',
    responseType: 'blob',
    headers: {
      'Content-Type': 'octet-stream;charset=UTF-8',
    },
  }).then((req) => {
    if (req.data === 404) {
      ElMessage({
        type: 'info',
        message: '没有找到下载的文件',
      })
      return
    }
     saveAs(req.data, filename)
  }),
  getmenuitemURL: () => axios.post(`/api/getmenuitemURL`, { xm_name }),
  upmenuitemURL: (data) => axios.post(`/api/upmenuitemURL`, { xm_name, data }),
  addmenuitemURL: (menuitemURL) =>
    axios.post(`/api/addmenuitemURL`, { xm_name, menuitemURL }),
  getTitle: () => axios.post(`/api/gettitle`, { xm_name }),
  setTitle: (title) => axios.post(`/api/settitle`, { xm_name, title }),
  getPermissions: () => axios.post(`/api/getPermissions`, { xm_name }),
  delmenuitemURL: (id) => axios.post(`/api/delmenuitemURL`, { xm_name, id }),
  setmenuitemName: (id, menuitemName) =>
    axios.post(`/api/setmenuitemName`, { xm_name, id, menuitemName }),
}
export default api

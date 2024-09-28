import axios from 'axios'
import { saveAs } from 'file-saver'
import { config } from './config'

const { base_url } = config
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
    })
}
export default api

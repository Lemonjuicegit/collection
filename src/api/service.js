import axios from 'axios'
import { config } from './config'

const { result_code, base_url, request_timeout } = config
const service = axios.create({
  baseURL: base_url, // api 的 base_url
  timeout: request_timeout, // 请求超时时间
  withCredentials: false, // 禁用 Cookie 等信息
})
service.interceptors.request.use(
  (conf) => {
    const user = sessionStorage.getItem('user')
    if (user && user !== 'undefined') {
      const token = user
        ? JSON.parse(user).accessToken
        : ''
      if (token) {
        conf.headers.Token = token
      }
    }
    return conf
  },
  (err) => {}
)
service.interceptors.response.use(
  async (response) => {
    const { data } = response
    const config = response.config
    if (!data) {
      //返回“[HTTP]请求没有返回值”;
      throw new Error()
    }
    // 未设置状态码则默认成功状态
    const code = data.code || result_code
    // 二进制数据则直接返回
    if (
      response.request.responseType === 'blob' ||
      response.request.responseType ===
        'arraybuffer'
    ) {
      return response.data
    }

    return response.data
  },
  (err) => {}
)
export default service

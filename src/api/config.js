import { getRouter } from '@/utils'
const config = {
  /**
   * api请求基础路径
   */
  base_url: import.meta.env.VITE_BASE_URL,
  /**
   * 接口成功返回状态码
   */
  result_code: 200,

  /**
   * 接口请求超时时间
   */
  request_timeout: 30000,

  /**
   * 默认接口请求类型
   * 可选值：application/x-www-form-urlencoded multipart/form-data
   */
  default_headers: 'application/json',

  xm_name: location.href.split('/')[3],
}

export { config }

import { config } from './config'
import service from './service'

const { default_headers } = config
const request = (option) => {
  const { url, method, params, data, headersType, responseType, header } = option
  return service({
    url: url,
    method,
    params,
    data,
    responseType: responseType,
    headers: {
      'Content-Type': headersType || default_headers,
      ...header
    }
  })
}

export default {
  get: async (option) => {
    const res = await request({ method: 'GET', ...option })
    return res
  },
  post: async (option) => {
    console.log('option', option)
    const res = await request({ method: 'POST', ...option })
    return res
  },
  postOriginal: async (option) => {
    const res = await request({ method: 'POST', ...option })
    return res
  },
  delete: async (option) => {
    const res = await request({ method: 'DELETE', ...option })
    return res.data
  },
  put: async (option) => {
    const res = await request({ method: 'PUT', ...option })
    return res.data
  },
  download: async (option) => {
    const res = await request({
      method: 'GET',
      responseType: 'blob',
      ...option
    })
    return res
  },
  upload: async (option) => {
    option.headersType = 'multipart/form-data'
    const res = await request({ method: 'POST', ...option })
    return res
  }
}

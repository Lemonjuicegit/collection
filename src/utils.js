function uuid() {
  let d = new Date().getTime()
  if (window.performance && typeof window.performance.now === 'function') {
    d += performance.now()
  }
  let uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    let r = (d + Math.random() * 16) % 16 | 0 // d是随机种子
    d = Math.floor(d / 16)
    return (c == 'x' ? r : (r & 0x3) | 0x8).toString(16)
  })
  return uuid
}
// 判断数据是否过期
function isExpired(key) {
  const value = sessionStorage.getItem(key)
  const data = JSON.parse(value)
  if (Date.now() > data.expires) {
    sessionStorage.removeItem(key)
    return true // 已过期
  }
  return false // 未过期
}

// 设置数据过期时间
function setWithExpires(key, value, expires) {
  const data = {
    value: value,
    expires: Date.now() + expires * 60000
  }
  sessionStorage.setItem(key, JSON.stringify(data))
}

// 获取存储数据
function getWithExpires(key) {
  if (isExpired(key)) {
    return null
  }
  const value = sessionStorage.getItem(key)
  const data = JSON.parse(value)
  return data.value
}

// 示例代码
// setWithExpires('name', 'alice', 1000) // 存储一个名为'name'的数据，过期时间为1秒
// getWithExpires('name') // 检查'name'是否过期，若未过期，则返回此数据
const setRouter = () => {
  const xm_name = location.href.split('/')[3]
  sessionStorage.setItem('routerName', JSON.stringify(xm_name))
}
const getRouter = () => {
  let routerName = sessionStorage.getItem('routerName')
  return JSON.parse(routerName)
}
const inArray = (list, contrast) => {
  const isExist = list.some((item) => {
    return contrast(item)
  })
  return isExist
}

const getDelId = (tree_data) => {
  let ids = []
  const fun = (data) => {
    if (data.is_group && data.children) {
      ids.push(data.id)
      data.children.forEach((item) => {
        fun(item)
      })
    } else {
      ids.push(data.id)
    }
  }
  fun(tree_data)
  return ids
}
const filterEmptyValues = (obj) => {
  const filteredObj = {}
  Object.keys(obj).forEach((key) => {
    if (obj[key] !== null && obj[key] !== undefined && !Number.isNaN(obj[key]) && obj[key] !== 0) {
      filteredObj[key] = obj[key]
    }
  })
  return filteredObj
}
export {
  uuid,
  isExpired,
  setWithExpires,
  getWithExpires,
  setRouter,
  getRouter,
  inArray,
  getDelId,
  filterEmptyValues
}

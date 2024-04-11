import axios from 'axios'
const api = {
  getmenuitem: () => axios.get(`/api/manage/getmenuitem`),

  getRouter: () => axios.get(`/api/manage/getRouter`),
  addRouter: (routerName) => axios.post(`/api/addRouter`, { routerName }),
  delRouter: (routerName) =>
    axios.post(`/api/manage/delRouter`, { routerName }),
  reviseMenuitemURL: (routerName, menuitemURL) =>
    axios.post(`/api/manage/reviseMenuitemURL`, { routerName, menuitemURL }),
}
export default api

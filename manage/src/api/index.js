import axios from 'axios'
const xm_name = location.href.split('/').slice(-2, -1)[0]
const api = {
  getmenuitemURL: () => axios.post(`/api/getmenuitemURL`, { xm_name }),
  getmenuitem: () => axios.get(`/api/getmenuitem`),
  addmenuitemURL: (menuitemURL) =>
    axios.post(`/api/addmenuitemURL`, { xm_name, menuitemURL }),
  delmenuitemURL: (id) => axios.post(`/api/delmenuitemURL`, { xm_name, id }),
  setmenuitemName: (id, menuitemName) =>
    axios.post(`/api/setmenuitemName`, { xm_name, id, menuitemName }),
  getRouter: () => axios.get(`/api/getRouter`),
  addRouter: (routerName) => axios.post(`/api/addRouter`, { routerName }),
  delRouter: (routerName) => axios.post(`/api/delRouter`, { routerName }),
}
export default api

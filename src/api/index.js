import axios from 'axios'
import {xm_name} from '@/config'
const api = {
  getmenuitemURL: () => axios.post(`/api/getmenuitemURL`, { xm_name }),
  addmenuitemURL: (menuitemURL) =>
    axios.post(`/api/addmenuitemURL`, { xm_name, menuitemURL }),
  getTitle: () => axios.post(`/api/gettitle`, { xm_name }),
  setTitle: (title) => axios.post(`/api/settitle`, { xm_name, title }),
  delmenuitemURL: (id) => axios.post(`/api/delmenuitemURL`, { xm_name, id }),
  setmenuitemName: (id, menuitemName) =>
    axios.post(`/api/setmenuitemName`, { xm_name, id, menuitemName }),
}
export default api

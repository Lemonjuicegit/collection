import axios from 'axios'
const api = {
  lqexf: (gdb, state) => axios.post(`/api/exf/lqexf`, { gdb, state }),
  hcexf: (gdb, state) => axios.post(`/api/exf/hcexf`, { gdb, state }),
}
export default api
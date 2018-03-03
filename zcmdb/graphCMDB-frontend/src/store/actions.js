import * as types from './mutation-types'
import { getArangoData } from '@/api'

const actions = {
  initAccountMapping ({ commit }) {
    getArangoData('Account').then(data => {
      let payload = {}
      for (let i = 0; i < data.length; i++) {
        let [k, v] = [data[i]['_key'], data[i]['Name']]
        payload[k] = v
      }
      commit(types.INIT_ACCOUNT_MAPPING, payload)
    })
  }
}

export default actions


import * as types from './mutation-types'

const mutations = {
  [types.INIT_ACCOUNT_MAPPING] (state, payload) {
    state.accountMapping = payload
  }
}
export default mutations

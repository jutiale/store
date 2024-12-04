import { createStore } from 'vuex'
import { authenticationService } from '@/services/authenticationService';


const store = createStore({
  state () {
    return {
      user: authenticationService.getCurrentUser()
    }
  },
  mutations: {
    setUser (state, user) {
      state.user = user
    },
    deleteUser(state) {
      state.user = null
    }
  }
})

export {
  store
}
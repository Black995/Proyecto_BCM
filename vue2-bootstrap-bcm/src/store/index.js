
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        numberNotifications: null
    },
    mutations: {
        changenumberNotif: (state, number) => {
            state.numberNotifications = number;
        }
    }
})

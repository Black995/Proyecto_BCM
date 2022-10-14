
import Vuex from 'vuex'

export const store = new Vuex.Store({
    state: {
        numberNotifications: null
    },
    mutations: {
        changenumberNotif: (state, number) => {
            state.numberNotifications = number;
        }
    }
})
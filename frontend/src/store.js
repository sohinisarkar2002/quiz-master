import { createStore } from 'vuex';
import axios from 'axios';

const store = createStore({
    state() {
        return {
            user: JSON.parse(localStorage.getItem('user')) || null,
            token: localStorage.getItem('token') || null,
        };
    },
    mutations: {
        setUser(state, user) {
            state.user = user;
            localStorage.setItem('user', JSON.stringify(user));
        },
        setToken(state, token) {
            state.token = token;
            localStorage.setItem('token', token);
        },
        logout(state) {
            state.user = null;
            state.token = null;
            localStorage.removeItem('user');
            localStorage.removeItem('token');
        }
    },
    actions: {
        async login({ commit }, credentials) {
            try {
                const response = await axios.post('http://localhost:5000/auth/login', credentials);
                commit('setUser', response.data.user);
                commit('setToken', response.data.token);
                return response;
            } catch (error) {
                throw error;
            }
        },
        logout({ commit }) {
            commit('logout');
        }
    }
});

export default store;
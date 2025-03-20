import { createRouter, createWebHistory } from 'vue-router';
import store from './store';
import AdminDashboard from './views/AdminDashboard.vue';
import UserDashboard from './views/UserDashboard.vue';
import QuizPage from './views/QuizPage.vue';
import Login from './views/Login.vue';
import Register from './views/Register.vue';

const routes = [
    { path: '/', component: Login },
    { path: '/register', component: Register },
    { path: '/admin', component: AdminDashboard, meta: { requiresAuth: true, role: 'admin' } },
    { path: '/user', component: UserDashboard, meta: { requiresAuth: true, role: 'user' } },
    { path: '/quiz', component: QuizPage, meta: { requiresAuth: true } }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach((to, from, next) => {
    const user = store.state.user;
    if (to.meta.requiresAuth && !user) {
        next('/');
    } else if (to.meta.role && user && user.role !== to.meta.role) {
        next('/');
    } else {
        next();
    }
});

export default router;
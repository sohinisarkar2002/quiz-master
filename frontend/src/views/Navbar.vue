<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Quiz App</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item" v-if="!user">
                        <router-link class="nav-link" to="/">Login</router-link>
                    </li>
                    <li class="nav-item" v-if="!user">
                        <router-link class="nav-link" to="/register">Register</router-link>
                    </li>
                    <li class="nav-item" v-if="user">
                        <router-link class="nav-link" to="/user">Dashboard</router-link>
                    </li>
                    <li class="nav-item" v-if="user">
                        <router-link class="nav-link" to="/quiz">Quizzes</router-link>
                    </li>
                    <li class="nav-item" v-if="user">
                        <button class="btn btn-danger" @click="handleLogout">Logout</button>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
import { computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default {
    setup() {
        const store = useStore();
        const router = useRouter();
        const user = computed(() => store.state.user);

        const handleLogout = () => {
            store.dispatch('logout');
            router.push('/');
        };

        return { user, handleLogout };
    }
};
</script>
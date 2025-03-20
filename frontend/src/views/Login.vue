<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card p-4">
            <h2 class="text-center">Login</h2>
            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input 
                  type="email" 
                  v-model="email" 
                  class="form-control" 
                  required
                >
              </div>
              <div class="mb-3">
                <label class="form-label">Password</label>
                <input 
                  type="password" 
                  v-model="password" 
                  class="form-control" 
                  required
                >
              </div>
              <button 
                type="submit" 
                class="btn btn-primary w-100"
                :disabled="isLoading"
              >
                {{ isLoading ? 'Logging in...' : 'Login' }}
              </button>
              <p v-if="errorMessage" class="text-danger mt-3">{{ errorMessage }}</p>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { useStore } from 'vuex';
  import { useRouter } from 'vue-router';
  
  export default {
    setup() {
      const store = useStore();
      const router = useRouter();
      const email = ref('');
      const password = ref('');
      const isLoading = ref(false);
      const errorMessage = ref('');
  
      const handleLogin = async () => {
        isLoading.value = true;
        errorMessage.value = '';
  
        try {
          await store.dispatch('login', { email: email.value, password: password.value });
          router.push('/user');
        } catch (error) {
          errorMessage.value = 'Invalid email or password. Please try again.';
        } finally {
          isLoading.value = false;
        }
      };
  
      return { email, password, handleLogin, isLoading, errorMessage };
    }
  };
  </script>
  
  <style>
  .card { box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
  </style>
  
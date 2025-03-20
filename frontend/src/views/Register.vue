<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card p-4">
            <h2 class="text-center">Register</h2>
            <form @submit.prevent="handleRegister">
              <div class="mb-3">
                <label class="form-label">Username</label>
                <input 
                  type="text" 
                  v-model="username" 
                  class="form-control" 
                  required
                >
              </div>
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input 
                  type="email" 
                  v-model="email" 
                  class="form-control" 
                  @blur="validateEmail"
                  required
                >
                <small v-if="!isEmailValid" class="text-danger">Invalid email format</small>
              </div>
              <div class="mb-3">
                <label class="form-label">Password</label>
                <input 
                  type="password" 
                  v-model="password" 
                  class="form-control" 
                  @input="checkPasswordStrength"
                  required
                >
                <small v-if="passwordStrength" :class="passwordStrengthClass">
                  {{ passwordStrength }}
                </small>
              </div>
              <button 
                type="submit" 
                class="btn btn-primary w-100"
                :disabled="isLoading || !isEmailValid || !passwordStrengthValid"
              >
                {{ isLoading ? 'Registering...' : 'Register' }}
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
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  export default {
    setup() {
      const router = useRouter();
      const username = ref('');
      const email = ref('');
      const password = ref('');
      const isLoading = ref(false);
      const errorMessage = ref('');
      const isEmailValid = ref(true);
      const passwordStrength = ref('');
      const passwordStrengthValid = ref(false);
  
      const validateEmail = () => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        isEmailValid.value = emailRegex.test(email.value);
      };
  
      const checkPasswordStrength = () => {
        if (password.value.length < 6) {
          passwordStrength.value = 'Weak';
          passwordStrengthValid.value = false;
        } else if (password.value.length < 10) {
          passwordStrength.value = 'Medium';
          passwordStrengthValid.value = true;
        } else {
          passwordStrength.value = 'Strong';
          passwordStrengthValid.value = true;
        }
      };
  
      const handleRegister = async () => {
        isLoading.value = true;
        errorMessage.value = '';
  
        try {
          await axios.post('http://localhost:5000/auth/register', {
            username: username.value,
            email: email.value,
            password: password.value
          });
          alert('Registration successful!');
          router.push('/');
        } catch (error) {
          errorMessage.value = 'Registration failed. Please try again.';
        } finally {
          isLoading.value = false;
        }
      };
  
      return {
        username,
        email,
        password,
        handleRegister,
        isLoading,
        errorMessage,
        isEmailValid,
        passwordStrength,
        passwordStrengthValid,
        passwordStrengthClass: ref({
          Weak: 'text-danger',
          Medium: 'text-warning',
          Strong: 'text-success'
        })
      };
    }
  };
  </script>
  
  <style>
  .card { box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
  </style>
  
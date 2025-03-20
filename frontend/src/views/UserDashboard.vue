<template>
  <div class="container mt-4">
    <h2 class="text-center">User Dashboard</h2>
    <p class="text-center">Welcome, {{ user?.username }}!</p>
    
    <div v-if="quizzes.length" class="mt-4">
      <h3>Available Quizzes</h3>
      <ul class="list-group">
        <li v-for="quiz in quizzes" :key="quiz.id" class="list-group-item d-flex justify-content-between align-items-center">
          {{ quiz.title }}
          <button class="btn btn-primary" @click="startQuiz(quiz.id)">Start Quiz</button>
        </li>
      </ul>
    </div>
    <p v-else class="text-center">No quizzes available at the moment.</p>

    <div class="text-center mt-4">
      <button class="btn btn-danger" @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { computed, ref, onMounted } from "vue";
import axios from "axios";

export default {
  setup() {
    const store = useStore();
    const router = useRouter();
    const user = computed(() => store.state.user);
    const quizzes = ref([]);

    const fetchQuizzes = async () => {
      try {
        const response = await axios.get("http://localhost:5000/quizzes");
        quizzes.value = response.data;
      } catch (error) {
        console.error("Error fetching quizzes:", error);
      }
    };

    const startQuiz = (quizId) => {
      router.push(`/quiz/${quizId}`);
    };

    const logout = () => {
      store.dispatch("logout");
      router.push("/login");
    };

    onMounted(fetchQuizzes);

    return { user, quizzes, startQuiz, logout };
  },
};
</script>
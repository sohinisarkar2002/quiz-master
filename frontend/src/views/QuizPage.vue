<template>
  <div>
    <h2>{{ quiz.title }}</h2>
    <p>Time left: {{ timeLeft }}s</p>
    <div v-for="(question, index) in quiz.questions" :key="index">
      <p>{{ question.text }}</p>
      <div v-for="option in question.options" :key="option.id">
        <input type="radio" :name="'q' + index" v-model="answers[index]" :value="option.id" />
        {{ option.text }}
      </div>
    </div>
    <button @click="submitQuiz">Submit</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      quiz: {},
      answers: {},
      timeLeft: 60,
    };
  },
  created() {
    this.fetchQuiz();
    this.startTimer();
  },
  methods: {
    async fetchQuiz() {
      const res = await axios.get("/api/user/quiz");
      this.quiz = res.data;
    },
    startTimer() {
      const interval = setInterval(() => {
        if (this.timeLeft > 0) this.timeLeft--;
        else clearInterval(interval);
      }, 1000);
    },
    async submitQuiz() {
      const score = this.calculateScore();
      await axios.post("/api/user/quiz/attempt", { quiz_id: this.quiz.id, score });
      alert("Quiz submitted!");
    },
    calculateScore() {
      let correct = 0;
      
      this.quiz.questions.forEach((q, index) => {
        const selectedAnswer = this.answers[index];

        // Skip unanswered questions
        if (!selectedAnswer) return;

        // Check for multiple correct answers
        const correctOptions = Array.isArray(q.correct_option) 
          ? q.correct_option 
          : [q.correct_option];

        if (correctOptions.includes(selectedAnswer)) {
          correct++;
        }
      });

      return (correct / this.quiz.questions.length) * 100;
    },
  },
};
</script>

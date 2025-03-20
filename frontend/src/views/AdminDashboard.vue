<template>
  <div>
    <h2>Admin Dashboard</h2>

    <!-- Quiz Statistics -->
    <div class="stats">
      <p>Total Users: {{ stats.total_users }}</p>
      <p>Total Quizzes: {{ stats.total_quizzes }}</p>
      <p>Total Attempts: {{ stats.total_attempts }}</p>
    </div>

    <canvas id="quizChart"></canvas>

    <!-- Manage Subjects -->
    <h2>Manage Subjects</h2>

    <!-- Search Bar -->
    <input v-model="searchQuery" placeholder="Search Subjects" />

    <form @submit.prevent="addSubject">
      <input v-model="newSubject" placeholder="Enter Subject Name" />
      <button type="submit" :disabled="loading">Add Subject</button>
    </form>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <p v-if="loading">Loading subjects...</p>

    <ul v-if="!loading">
      <li v-for="subject in filteredSubjects" :key="subject.id">
        <span v-if="editingSubjectId !== subject.id">{{ subject.name }}</span>
        <input v-else v-model="editedSubject" />

        <button @click="startEditing(subject)" v-if="editingSubjectId !== subject.id">Edit</button>
        <button @click="saveEdit(subject.id)" v-else>Save</button>
        <button @click="deleteSubject(subject.id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';
import axios from 'axios';

export default {
  data() {
    return {
      stats: {
        total_users: 0,
        total_quizzes: 0,
        total_attempts: 0,
        quiz_performance: [],
      },
      subjects: [],
      newSubject: "",
      searchQuery: "", // Search input state
      loading: false,
      errorMessage: "",
      editingSubjectId: null,
      editedSubject: "",
    };
  },
  computed: {
    filteredSubjects() {
      return this.subjects.filter((subject) =>
        subject.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  created() {
    this.fetchSubjects();
  },
  mounted() {
    this.fetchStats();
  },
  methods: {
    // Fetch Quiz Stats
    async fetchStats() {
      try {
        const response = await axios.get('/admin/stats');
        this.stats = response.data;
        if (this.stats.quiz_performance.length) {
          this.renderChart();
        }
      } catch (error) {
        console.error('Error fetching stats:', error);
      }
    },
    // Render Chart
    renderChart() {
      const ctx = document.getElementById('quizChart').getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.stats.quiz_performance.map(q => q.quiz),
          datasets: [{
            label: 'Average Score',
            data: this.stats.quiz_performance.map(q => q.avg_score),
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
          }]
        }
      });
    },
    // Fetch Subjects
    async fetchSubjects() {
      try {
        this.loading = true;
        const res = await axios.get("/api/admin/subjects");
        this.subjects = res.data;
      } catch (error) {
        this.errorMessage = "Failed to load subjects.";
      } finally {
        this.loading = false;
      }
    },
    // Add Subject
    async addSubject() {
      if (!this.newSubject.trim()) return;
      try {
        await axios.post("/api/admin/subject", { name: this.newSubject });
        this.newSubject = "";
        this.fetchSubjects();
      } catch (error) {
        this.errorMessage = "Error adding subject.";
      }
    },
    // Delete Subject
    async deleteSubject(id) {
      try {
        await axios.delete(`/api/admin/subject/${id}`);
        this.fetchSubjects();
      } catch (error) {
        this.errorMessage = "Error deleting subject.";
      }
    },
    // Start Editing Subject
    startEditing(subject) {
      this.editingSubjectId = subject.id;
      this.editedSubject = subject.name;
    },
    // Save Edited Subject
    async saveEdit(id) {
      if (!this.editedSubject.trim()) return;
      try {
        await axios.put(`/api/admin/subject/${id}`, { name: this.editedSubject });
        this.editingSubjectId = null;
        this.fetchSubjects();
      } catch (error) {
        this.errorMessage = "Error updating subject.";
      }
    }
  }
};
</script>

<style>
.stats {
  display: flex;
  gap: 20px;
}
.error {
  color: red;
}
</style>

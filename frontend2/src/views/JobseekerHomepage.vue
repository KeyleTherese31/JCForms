<template>
  <div class="homepage">
    <div class="card">
      <h2 class="text-xl font-semibold mb-4">Hello, {{ applicantName }} 👋</h2>
      <p class="mb-6 text-sm text-gray-600">Please pick an option below to get started:</p>

      <div class="button-group mb-6">
        <button @click="goToTest">Take Tests</button>
        <button @click="requestRetake">Request Retake Tests</button>
      </div>

      <br>
      <div class="score-section mb-6">
        <h3 class="text-md font-medium mb-2">Your Current Scores</h3>
        <ul class="text-sm text-left">
          <li v-for="(item, index) in filteredScores" :key="index">
            {{ item.category }}: {{ item.display }}
          </li>
          <li v-if="filteredScores.length === 0">No available scores yet.</li>
        </ul>
      </div>

      <button class="logout-btn" @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      applicantName: 'Juan Dela Cruz',
      scores: {
        'Image Pattern Analysis': { score: 5, total: 10 },
        'Basic Math': { score: 7, total: 10 },
        'Problem Analysis': { score: 8, total: 10 },
        'Reading Comprehension': { score: 6, total: 10 },
        'Pre Interview Questionnaire': { score: 9, total: 10 },
      }
    };
  },
  computed: {
    filteredScores() {
      return Object.entries(this.scores)
        .filter(([, value]) => value && value.score != null && value.total != null)
        .map(([category, value]) => ({
          category,
          display: `${value.score}/${value.total}`
        }));
    }
  },
  methods: {
    goToTest() {
      this.$router.push('/take-test');
    },
    requestRetake() {
      this.$router.push('/retake-request');
    },
    logout() {
      this.$router.push('/mobile-login');
    }
  }
};
</script>

<style scoped>
.homepage {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #ffa726, #ef5350);
  font-family: 'Segoe UI', sans-serif;
}

.card {
  background: white;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
  text-align: center;
  width: 90%;
  max-width: 400px;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

button {
  padding: 12px 20px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;
}

button:first-child {
  background-color: #42a5f5;
  color: white;
}

button:first-child:hover {
  background-color: #1e88e5;
}

button:last-child {
  background-color: #ffe082;
  color: #333;
}

button:last-child:hover {
  background-color: #ffca28;
}

.score-section {
  background-color: #f5f5f5;
  padding: 1rem;
  border-radius: 8px;
  text-align: left;
}

.logout-btn {
  margin-top: 20px;
  background: none;
  color: #e53935;
  font-size: 14px;
  text-decoration: underline;
  cursor: pointer;
}
</style>

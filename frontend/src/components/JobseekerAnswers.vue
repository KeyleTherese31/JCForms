<template>
  <div class="answers-container">
    <button class="back-btn" @click="goBack">← Back to Dashboard</button>
    <h1>Jobseeker's Answer Entries</h1>
      

    <div class="tabs">
      <button :class="{ active: currentTab === 'scores' }" @click="currentTab = 'scores'">Jobseekers List of Scores</button>
      <button :class="{ active: currentTab === 'details' }" @click="currentTab = 'details'">Jobseeker's Answer Sheet and Score</button>
    </div>

    <div v-if="currentTab === 'scores'" class="tab-content">
      <h2>List of Scores</h2>
      <input type="date" v-model="filter.startDate" />
      <input type="date" v-model="filter.endDate" />
      <button @click="filterScores">Filter</button>
      <button @click="downloadScores">Download Table</button>

      <table class="score-table">
        <thead>
          <tr>
            <th>Jobseeker</th>
            <th v-for="test in testList" :key="test">{{ test }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredScores" :key="user.id">
            <td>{{ user.name }}</td>
            <td v-for="score in user.scores" :key="score.test">{{ score.value }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="currentTab === 'details'" class="tab-content">
      <h2>Answer Sheet and Score</h2>
      <div v-for="jobseeker in jobseekerAnswers" :key="jobseeker.id" class="jobseeker-card">
        <h3>{{ jobseeker.name }}</h3>
        <div class="btn-row">
          <button @click="preview(jobseeker)">Preview</button>
          <button @click="download(jobseeker)">Download</button>
          <button :disabled="jobseeker.retakeGranted" @click="grantRetake(jobseeker)">Retake</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'JobseekerAnswers',
  data() {
    return {
      currentTab: 'scores',
      filter: {
        startDate: '',
        endDate: ''
      },
      testList: ['TEST1', 'TEST2', 'TEST3', 'TEST4', 'PRE-INTERVIEW'],
      jobseekerScores: [], // fetched from API
      filteredScores: [],
      jobseekerAnswers: [] // fetched from API
    };
  },
  methods: {
    goBack() {
        this.$router.push('/dashboard'); // adjust path if needed
    },
    filterScores() {
      const start = new Date(this.filter.startDate);
      const end = new Date(this.filter.endDate);
      this.filteredScores = this.jobseekerScores.filter(user =>
        user.date && new Date(user.date) >= start && new Date(user.date) <= end
      );
    },
    downloadScores() {
      // convert filteredScores to CSV or PDF and trigger download
    },
    preview(jobseeker) {
    console.log('Previewing jobseeker:', jobseeker);
    // TODO: Implement preview logic
    },
    download(jobseeker) {
    console.log('Downloading answer sheet for:', jobseeker);
    // TODO: Implement download logic
    },
    grantRetake(jobseeker) {
      // send API request to allow retake (handled by frontend2)
      jobseeker.retakeGranted = true;
      // Optional: show confirmation or feedback
    }
  },
  mounted() {
    // fetch jobseekerScores and jobseekerAnswers from your backend API
  }
};
</script>

<style scoped>
.answers-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #64b5f6, #8e24aa);
  font-family: 'Segoe UI', sans-serif;
  color: #333;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  flex-wrap: wrap;
  justify-content: center;
}

.tabs button {
  padding: 12px 24px;
  font-size: 16px;
  background: #e0e0e0;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.tabs button.active {
  background-color: #3949ab;
  color: white;
}

.back-btn {
  align-self: flex-start;
  margin-bottom: 20px;
  background-color: transparent;
  color: white;
  font-size: 16px;
  border: none;
  cursor: pointer;
  transition: color 0.3s ease;
}

.back-btn:hover {
  color: #bbdefb;
}

.tab-content {
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 1000px;
}

.score-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.score-table th,
.score-table td {
  padding: 12px;
  border: 1px solid #ccc;
  text-align: center;
  font-size: 15px;
}

.score-table th {
  background-color: #f5f5f5;
}

input[type='date'] {
  padding: 8px 10px;
  margin: 5px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 14px;
}

button {
  font-size: 14px;
  padding: 10px 18px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: background 0.3s ease;
  background-color: #3949ab;
  color: white;
}

button:hover {
  background-color: #303f9f;
}

.jobseeker-card {
  background: #f9f9f9;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.jobseeker-card h3 {
  margin-bottom: 10px;
  color: #333;
}

.btn-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
</style>

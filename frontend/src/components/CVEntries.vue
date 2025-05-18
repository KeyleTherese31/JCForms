<template>
  <div class="cv-entries-container">
    <div class="card">
      <button class="back-btn" @click="goBack">← Back to Dashboard</button>

      <h1>Jobseeker's CV Form Entries</h1>
      <p>Browse, preview, download, or evaluate submitted CVs.</p>

      <div v-if="cvEntries.length" class="cv-list">
                <div v-for="entry in cvEntries" :key="entry.id" class="cv-item">
          <div class="cv-info">
            <strong>{{ entry.first_name }} {{ entry.last_name }}</strong>
          </div>
          <div class="cv-actions">
            <button @click="previewCv(entry)">Preview</button>
            <button @click="downloadCv(entry)">Download</button>
            <button @click="evaluateCv(entry)">Evaluate</button>
          </div>
        </div>
      </div>

      <div v-else>
        <p>No CV entries found.</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CvFormEntries',
  data() {
    return {
      cvEntries: [],
    };
  },
  methods: {
    async fetchCvEntries() {
      try {
        const response = await axios.get('http://localhost:8000/api/submit-cv/');
        this.cvEntries = response.data;
      } catch (error) {
        console.error('Error fetching CV entries:', error);
      }
    },
    goBack() {
      this.$router.push('/dashboard');
    },
    previewCv(entry) {
      this.$router.push({ name: 'PreviewCV', params: { id: entry.id } });
    },
    downloadCv(entry) {
      alert(`Download feature not implemented yet for ${entry.first_name} ${entry.last_name}. View data in developer tools.`);
    },
    evaluateCv(entry) {
      alert(`Evaluating ${entry.first_name} ${entry.last_name}'s CV:\n(Placeholder for evaluation logic)`);
    },
  },
  mounted() {
    this.fetchCvEntries();
  },
};
</script>

<style scoped>
.cv-entries-container {
  display: flex;
  justify-content: center;
  align-items: start;
  min-height: 100vh;
  background: linear-gradient(135deg, #64b5f6, #8e24aa);
  padding-top: 50px;
  font-family: 'Segoe UI', sans-serif;
}

.card {
  background: #fff;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
  text-align: left;
  width: 90%;
  max-width: 800px;
}

.back-btn {
  margin-bottom: 20px;
  background: none;
  border: none;
  color: #3949ab;
  font-size: 16px;
  cursor: pointer;
  text-align: left;
  padding: 0;
}

.back-btn:hover {
  text-decoration: underline;
}

.card h1 {
  margin-bottom: 10px;
  color: #333;
}

.card p {
  margin-bottom: 25px;
  font-size: 16px;
  color: #555;
}

.cv-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.cv-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.cv-info {
  font-size: 16px;
  color: #333;
}

.cv-actions {
  display: flex;
  gap: 10px;
}

button {
  padding: 8px 14px;
  font-size: 14px;
  background-color: #3949ab;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
}

button:hover {
  background-color: #303f9f;
}
</style>

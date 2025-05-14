<template>
  <div class="dashboard-container">
    <div class="card">
      <h1>Admin Dashboard</h1>
      <p>Select a section to manage:</p>
      <div class="button-group">
        <button @click="goTo('tests')">Test & Questions</button>
        <button @click="goTo('answers')">Jobseeker's Answer Entries</button>
        <button @click="goTo('cvforms')">Jobseeker's CV Form Entries</button>
        <button @click="goTo('settings')">Settings</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardPage',
  methods: {
    goTo(section) {
      switch (section) {
        case 'tests':
          this.$router.push('/tests');
          break;
        case 'answers':
          this.$router.push('/answers');
          break;
        case 'cvforms':
          this.$router.push('/cvforms');
          break;
        case 'settings':
          this.$router.push('/settings');
          break;
      }
    },
  },
};
</script>

<style scoped>
.dashboard-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #64b5f6, #8e24aa);
  font-family: 'Segoe UI', sans-serif;
}

.card {
  background: #fff;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
  text-align: center;
  width: 90%;
  max-width: 500px;
}

.card h1 {
  margin-bottom: 15px;
  color: #333;
}

.card p {
  margin-bottom: 25px;
  font-size: 16px;
  color: #555;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

button {
  padding: 12px;
  font-size: 16px;
  background-color: #3949ab;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;
}

button:hover {
  background-color: #303f9f;
}
</style>

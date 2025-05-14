<template>
  <div class="welcome-container">
    <div class="card">
      <img src="@/assets/image.png" alt="JCForms Logo" class="logo d-block mx-auto mb-3" />
      <h1>Welcome to JCForms</h1>
      <p>Please select your role to continue:</p>
      <div class="button-group">
        <button @click="goToAdmin">I am an Admin</button>
        <button @click="goToJobseeker">I am a Jobseeker</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WelcomePage',
  methods: {
    goToAdmin() {
      this.$router.push('/login'); // Routes to Admin Login Page
    },
    goToJobseeker() {
      // Redirect to external jobseeker site
      window.location.href = 'https://jobcrest.com/jobseeker-site/';
    },
  },
}
</script>

<style scoped>
.welcome-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #e7d362, #2460cf);
  font-family: 'Segoe UI', sans-serif;
}

.logo {
  max-width: 200px;
  border-radius: 8px;
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
  padding: 12px 20px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;
}

button:first-child {
  background-color: #1e88e5;
  color: white;
}

button:first-child:hover {
  background-color: #1565c0;
}

button:last-child {
  background-color: #ffca28;
  color: #333;
}

button:last-child:hover {
  background-color: #fbc02d;
}
</style>

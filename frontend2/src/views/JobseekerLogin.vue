<template>
  <div class="jobseeker-login">
    <div class="card">
      <img src="@/assets/image.png" alt="JobCrest Logo" class="logo" />
      <h2>Welcome Jobseeker</h2>
      <p>Select an option to continue:</p>
      <div class="button-group">
        <button @click="goToNewJobseeker">New Jobseeker</button>
        <button @click="goToExistingJobseeker">Existing Jobcrest Applicant</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'JobseekerLogin',
  methods: {
    goToNewJobseeker() {
      this.$router.push('/cv-form');
    },
    goToExistingJobseeker() {
      this.$router.push('/mobile-login');
    },
  },
};
</script>

<style scoped>
.jobseeker-login {
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

.logo {
  max-width: 150px;
  border-radius: 8px;
  margin-bottom: 20px;
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
</style>

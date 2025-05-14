<template>
  <div class="login-container">
    <div class="card">
      <img src="@/assets/image.png" alt="JCForms Logo" class="logo mb-3" />
      <h2>Admin Login</h2>
      <form @submit.prevent="handleLogin">
        <input v-model="username" type="text" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Login</button>
      </form>
      <p class="divider">or</p>
      <button @click="goToRegister" class="register-btn">Create New Admin Account</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    handleLogin() {
      // Replace with your actual login logic
      console.log('Logging in with:', this.username, this.password);
      // Example: this.$router.push('/dashboard');
    },
    goToRegister() {
      this.$router.push('/register'); // Route to registration page
    },
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #2460cf, #e7d362);
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
  max-width: 120px;
  border-radius: 8px;
}

h2 {
  margin-bottom: 20px;
  color: #333;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

input {
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

button {
  padding: 12px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;
}

button[type="submit"] {
  background-color: #1e88e5;
  color: white;
}

button[type="submit"]:hover {
  background-color: #1565c0;
}

.register-btn {
  margin-top: 10px;
  background-color: #ffca28;
  color: #333;
}

.register-btn:hover {
  background-color: #fbc02d;
}

.divider {
  margin: 15px 0;
  font-weight: bold;
  color: #666;
}
</style>

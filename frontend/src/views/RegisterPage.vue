<template>
  <div class="register-container">
    <div class="card">
      <img src="@/assets/image.png" alt="JCForms Logo" class="logo mb-3" />
      <h2>Create Admin Account</h2>
      <form @submit.prevent="handleRegister">
        <input v-model="username" type="text" placeholder="Username" required />
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <input v-model="confirmPassword" type="password" placeholder="Confirm Password" required />
        <button type="submit">Register</button>
      </form>
      <p class="back-link">
        Already have an account?
        <router-link to="/login">Login here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterPage',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
    };
  },
  methods: {
    async handleRegister() {
      if (this.password !== this.confirmPassword) {
        alert('Passwords do not match!');
        return;
      }

      try {
        await axios.post('http://localhost:8000/api/admin/register/', {
          username: this.username,
          email: this.email,
          password: this.password,
        });

        alert('Registration successful. You can now log in.');
        this.$router.push('/login');
      } catch (error) {
        console.error('Registration error:', error);
        const errorMsg = error.response?.data?.error || 'Something went wrong during registration.';
        alert(`Registration failed: ${errorMsg}`);
      }
    },
  },
};
</script>

<style scoped>
.register-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #e7d362, #2460cf);
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
  background-color: #1e88e5;
  color: white;
}

button:hover {
  background-color: #1565c0;
}

.back-link {
  margin-top: 15px;
  font-size: 14px;
  color: #555;
}

.back-link a {
  color: #1e88e5;
  text-decoration: none;
  font-weight: bold;
}

.back-link a:hover {
  text-decoration: underline;
}
</style>

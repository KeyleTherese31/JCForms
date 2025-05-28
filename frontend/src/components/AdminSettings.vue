<template>
  <div class="form-container">
    <div class="card">
      <button class="back-btn" @click="goBack">← Back to Dashboard</button>

      <h2>Settings</h2>

      <form @submit.prevent="updateProfile">
        <div class="form-group">
          <label for="username">Username:</label>
          <input id="username" v-model="profile.username" type="text" required />
        </div>

        <div class="form-group">
          <label for="password">New Password:</label>
          <input
            id="password"
            v-model="profile.password"
            type="password"
            placeholder="Leave blank to keep current"
          />
        </div>

        <div class="form-group">
          <label for="fullname">Full Name:</label>
          <input id="fullname" v-model="profile.fullname" type="text" />
        </div>

        <div class="form-group">
          <label for="email">Email:</label>
          <input id="email" v-model="profile.email" type="email" required />
        </div>

        <button class="submit-btn" type="submit" :disabled="loading">
          {{ loading ? 'Saving...' : 'Save Profile' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "AdminSettings",
  data() {
    return {
      profile: {
        username: "",
        password: "",
        fullname: "",
        email: ""
      },
      loading: false
    };
  },
  created() {
    this.loadProfile();
  },
  methods: {
    async loadProfile() {
      try {
        const token = localStorage.getItem('access_token');

        const response = await axios.get('http://localhost:8000/api/admin/profile/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        const data = response.data;
        this.profile.username = data.username;
        this.profile.fullname = data.fullname;
        this.profile.email = data.email;
      } catch (error) {
        console.error("Failed to load profile:", error);
        alert("Error loading profile.");
      }
    },

    async updateProfile() {
      this.loading = true;
      try {
        const token = localStorage.getItem('access_token');

        const updatePayload = {
          username: this.profile.username,
          fullname: this.profile.fullname,
          email: this.profile.email
        };

        if (this.profile.password.trim()) {
          updatePayload.password = this.profile.password;
        }

        await axios.put('http://localhost:8000/api/admin/update/', updatePayload, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        alert("Profile updated successfully!");
        this.profile.password = "";
      } catch (error) {
        console.error("Profile update failed:", error);
        alert("Failed to update profile. Please check your input or try again later.");
      } finally {
        this.loading = false;
      }
    },

    goBack() {
      this.$router.push('/dashboard');
    }
  }
};
</script>

<style scoped>
.form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #64b5f6, #8e24aa);
  font-family: "Segoe UI", sans-serif;
  padding: 1rem;
}

.card {
  background: #fff;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 600px;
  text-align: left;
}

.back-btn {
  background: none;
  border: none;
  color: #3949ab;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  margin-bottom: 20px;
  padding: 0;
  transition: color 0.3s ease;
}

.back-btn:hover {
  color: #1e40af;
}

h2 {
  margin-bottom: 20px;
  color: #333;
  font-weight: 600;
  font-size: 24px;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

input[type="text"],
input[type="password"],
input[type="email"] {
  width: 100%;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

input[type="text"]:focus,
input[type="password"]:focus,
input[type="email"]:focus {
  outline: none;
  border-color: #3949ab;
}

.submit-btn {
  margin-top: 30px;
  background-color: #3949ab;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s ease;
  width: 100%;
}

.submit-btn:hover:not(:disabled) {
  background-color: #303f9f;
}

.submit-btn:disabled {
  background-color: #7e87bf;
  cursor: not-allowed;
}
</style>

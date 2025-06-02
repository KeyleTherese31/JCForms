<template>
  <div class="dashboard-container superadmin-bg">
    <div class="card">
      <h1>Superadmin Control Panel</h1>
      <p>Manage Admin Accounts</p>

      <div v-if="loading">Loading admins...</div>
      <div v-else class="admin-list"> 
        <div v-for="admin in admins" :key="admin.id" class="admin-card">
          <p><strong>{{ admin.username }}</strong> ({{ admin.email }})</p>
          <button 
            @click="deactivateAdmin(admin.id)" 
            :disabled="admin.deactivating"
            class="super-btn"
          >
            {{ admin.deactivating ? 'Processing...' : 'Deactivate' }}
          </button>
        </div>
      </div>
      <br>
      <div>
        <button class="back-btn" @click="goBack">Back</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SuperadminPanel',
  data() {
    return {
      admins: [],
      loading: true,
    };
  },
  methods: {
    goBack() {
      this.$router.push('/dashboard');
    },

    async fetchAdmins() {
      this.loading = true;
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          alert('You are not logged in. Please log in first.');
          this.loading = false;
          this.$router.push('/login');
          return;
        }

        const res = await axios.get('http://localhost:8000/api/admin-users/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.admins = res.data;
      } catch (error) {
        console.error('Error fetching admins', error);
        alert('Failed to load admin list. Please check your login status.');
        if (error.response && error.response.status === 401) {
          localStorage.clear();
          this.$router.push('/login');
        }
      } finally {
        this.loading = false;
      }
    },

    async deactivateAdmin(adminId) {
      const confirmDeactivate = window.confirm('Are you sure you want to deactivate this admin?');
      if (!confirmDeactivate) return;

      const admin = this.admins.find(a => a.id === adminId);
      if (!admin) {
        alert('Admin not found');
        return;
      }

      // Mark as deactivating (optional UI feedback)
      admin.deactivating = true;

      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          alert('You are not logged in. Please log in first.');
          this.$router.push('/login');
          return;
        }

        await axios.post(`http://localhost:8000/api/deactivate-admin/${adminId}/`, {}, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        alert('Admin successfully deactivated.');
        await this.fetchAdmins(); // refresh list
      } catch (err) {
        console.error('Error deactivating admin', err);
        alert('Failed to deactivate admin.');
      } finally {
        admin.deactivating = false;
      }
    }
  },
  mounted() {
    this.fetchAdmins();
  }
};
</script>

<style scoped>
.dashboard-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #2460cf, #e7d362);
  font-family: 'Segoe UI', sans-serif;
}

.superadmin-bg {
  background: linear-gradient(135deg, #7F55B1, #F49BAB);
}

.card {
  background: #FFE1E0;
  color: #333;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
  text-align: center;
  width: 90%;
  max-width: 500px;
}

.back-btn {
  margin-bottom: 15px;
  background-color: #42a5f5;
  color: white;
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

h1 {
  margin-bottom: 10px;
  color: #333;
}

p {
  margin-bottom: 20px;
  color: #555;
}

.admin-list {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.admin-card {
  background: white;
  padding: 15px 20px;
  border-radius: 10px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

button.super-btn {
  background-color: #9B7EBD;
  color: white;
  font-weight: bold;
  padding: 10px 18px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;
}

button.super-btn:hover:not(:disabled) {
  background-color: #7F55B1;
}

button.super-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  color: #666;
}
</style>

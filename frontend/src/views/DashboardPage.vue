<template>
  <div class="dashboard-container" :class="{ 'superadmin-bg': isSuperadmin }">
    <div class="card">
      <h1>{{ dashboardTitle }}</h1>
      <p>Select a section to manage:</p>

      <div class="button-group">
        <button @click="goTo('tests')">Test & Questions</button>
        <button v-if="isSuperadmin" @click="goTo('testpanel')">Manage Tests & Questions</button>
        <button @click="goTo('answers')">Jobseeker's Answer Entries</button>
        <button @click="goTo('cvforms')">Jobseeker's CV Form Entries</button>
        <button @click="goTo('settings')">Settings</button>
        <button v-if="isSuperadmin" @click="goTo('adminpanel')">Superadmin Panel</button>
      </div>

      <div class="footer">
        <p>Logged in as: <strong>{{ username }}</strong> ({{ role }})</p>
        <button class="logout-btn" @click="logout">Logout</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardPage',
  data() {
    return {
      username: localStorage.getItem('admin_user'),
      role: localStorage.getItem('admin_role'),
    };
  },
  computed: {
    isSuperadmin() {
      return this.role === 'superadmin';
    },
    dashboardTitle() {
      return this.isSuperadmin ? 'Superadmin Dashboard' : 'Admin Dashboard';
    },
  },
  methods: {
    goTo(section) {
      const routes = {
        tests: '/tests',
        testpanel: '/testpanel',
        answers: '/answers',
        cvforms: '/cvforms',
        settings: '/settings',
        adminpanel: '/adminpanel', // new route for superadmin
      };
      this.$router.push(routes[section]);
    },
    logout() {
      if (confirm("Are you sure you want to logout?")) {
        localStorage.clear();
        this.$router.push("/login");
      }
    },
  },
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
  background: white;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
  text-align: center;
  width: 90%;
  max-width: 500px;
}

.superadmin-bg .card {
  background: #FFE1E0;
  color: #333;
}

h1 {
  margin-bottom: 10px;
  color: #333;
}

p {
  margin-bottom: 20px;
  color: #555;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.button-group button {
  padding: 12px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;
  background-color: #1e88e5;
  color: white;
}

.button-group button:hover {
  background-color: #1565c0;
}

.super-btn {
  background-color: #9B7EBD;
  color: white;
  font-weight: bold;
}

.super-btn:hover {
  background-color: #7F55B1;
}

.footer {
  margin-top: 20px;
  color: #666;
}

.logout-btn {
  margin-top: 10px;
  background: #e53935;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.logout-btn:hover {
  background: #c62828;
}
</style>

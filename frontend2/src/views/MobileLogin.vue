<template>
  <div class="jobseeker-login">
    <div class="card">
      <img src="@/assets/image.png" alt="JobCrest Logo" class="logo" />
      <h2>Mobile Login</h2>
      <p>Enter your mobile number to continue:</p>
      <input
        v-model="mobile"
        type="tel"
        placeholder="e.g. 09171234567"
        class="input"
      />
      <div class="button-group">
        <button @click="submitMobile">Submit</button>
        <button @click="goBack">Back</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MobileLogin',
  data() {
    return {
      mobile: '',
    };
  },
  methods: {
    async submitMobile() {
      if (!this.mobile || !/^09\d{9}$/.test(this.mobile)) {
        alert('Please enter a valid mobile number (e.g. 09171234567).');
        return;
      }

      try {
        const response = await axios.post('http://localhost:8000/api/jobseeker-login/', {
          mobile: this.mobile,
        });

        if (response.data.exists) {
          this.$router.push(`/js-homepage?mobile=${this.mobile}`);
        } else {
          alert('Mobile number not found. Please register as a new jobseeker.');
        }
      } catch (error) {
        console.error(error);
        alert('An error occurred while checking your mobile number.');
      }
    },
    goBack() {
      this.$router.push('/');
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

.input {
  padding: 12px;
  font-size: 16px;
  width: 100%;
  margin-top: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-sizing: border-box;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 20px;
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

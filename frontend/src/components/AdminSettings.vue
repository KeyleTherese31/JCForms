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
          <input id="email" v-model="profile.email" type="email" />
        </div>

        <div class="form-group">
          <label for="profileImage">Profile Image:</label>
          <input id="profileImage" type="file" accept="image/*" @change="onImageChange" />
          <div v-if="imagePreview" class="image-preview">
            <img :src="imagePreview" alt="Profile Preview" />
          </div>
        </div>

        <button class="submit-btn" type="submit" :disabled="loading">
          {{ loading ? 'Saving...' : 'Save Profile' }}
        </button>
      </form>

      <button class="submit-btn logout-btn" @click="logout" type="button">
        Log Out
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "AdminSettings",
  data() {
    return {
      profile: {
        username: "",
        password: "",
        fullname: "",
        email: "",
        imageFile: null,
      },
      imagePreview: null,
      loading: false,
    };
  },
  created() {
    this.loadProfile();
  },
  methods: {
    loadProfile() {
      // Replace this with your actual logic/API call
      const currentUser = {
        username: "adminUser",
        fullname: "Admin Name",
        email: "admin@example.com",
        imageUrl: null,
      };
      this.profile.username = currentUser.username;
      this.profile.fullname = currentUser.fullname;
      this.profile.email = currentUser.email;
      this.imagePreview = currentUser.imageUrl || null;
    },
    onImageChange(event) {
      const file = event.target.files[0];
      if (file && file.type.startsWith("image/")) {
        this.profile.imageFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imagePreview = e.target.result;
        };
        reader.readAsDataURL(file);
      } else {
        this.profile.imageFile = null;
        this.imagePreview = null;
      }
    },
    async updateProfile() {
      this.loading = true;

      const formData = new FormData();
      formData.append("username", this.profile.username);
      if (this.profile.password) {
        formData.append("password", this.profile.password);
      }
      formData.append("fullname", this.profile.fullname);
      formData.append("email", this.profile.email);
      if (this.profile.imageFile) {
        formData.append("profileImage", this.profile.imageFile);
      }

      try {
        // TODO: Call your API here to update the profile
        await new Promise((resolve) => setTimeout(resolve, 1000));
        alert("Profile updated successfully!");
        this.profile.password = "";
      } catch (error) {
        alert("Failed to update profile.");
      } finally {
        this.loading = false;
      }
    },
    logout() {
      // TODO: Add your logout logic here
      alert("Logging out...");
      this.$router.push("/login");
    },
    goBack() {
      // Using Vue Router to navigate back to dashboard
      this.$router.push('/dashboard');
    },
  },
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

.card h2 {
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

input[type="text"],
input[type="password"],
input[type="email"],
input[type="file"] {
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

.image-preview {
  margin-top: 10px;
  max-width: 120px;
  max-height: 120px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 3px 8px rgba(57, 73, 171, 0.3);
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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

.logout-btn {
  background-color: #e53935;
  margin-top: 15px;
}

.logout-btn:hover {
  background-color: #b71c1c;
}
</style>

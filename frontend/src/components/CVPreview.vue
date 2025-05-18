<template>
  <div class="cv-entries-container">
    <div class="card cv-preview">
      <button class="back-btn" @click="$router.back()">← Back</button>

      <div v-if="loading">Loading CV data...</div>
      <div v-else-if="error" class="error-msg">{{ error }}</div>
      <div v-else-if="cv">
        <h1>{{ (cv.first_name + ' ' + cv.last_name + "'S CV").toUpperCase() }}</h1>

        <div class="cv-section" v-for="(value, key) in cv" :key="key">
          <strong>{{ formatLabel(key).toUpperCase() }}:</strong>

          <div v-if="isObject(value)" class="nested-object">
            <template v-if="key.toLowerCase() === 'education'">
              <div
                v-for="(edu, eduKey) in value"
                :key="eduKey"
                class="cv-entry-block"
              >
                <strong>{{ formatValue(eduKey) }}</strong>
                <div class="sub-fields">
                  <template v-for="(val, subKey) in edu" :key="subKey">
                    <div>
                      <strong>{{ formatLabel(subKey).toUpperCase() }}:</strong>
                      {{ formatValue(val) }}
                    </div>
                  </template>
                </div>
              </div>
            </template>

            <template v-else-if="key.toLowerCase() === 'scholarships'">
              <div v-if="value.length === 0 || (value.length === 1 && isEmptyObject(value[0]))">N/A</div>
              <div
                v-else
                v-for="(scholarship, index) in value"
                :key="index"
                class="cv-entry-block"
              >
                <div v-for="(val, subKey) in scholarship" :key="subKey">
                  <strong>{{ formatLabel(subKey).toUpperCase() }}:</strong> {{ formatValue(val) }}
                </div>
              </div>
            </template>

            <template v-else-if="key.toLowerCase() === 'family'">
              <div v-if="Object.keys(value).length === 0">N/A</div>
              <div v-else class="family-section">
                <div
                  v-for="(member, relation) in value"
                  :key="relation"
                  class="cv-entry-block"
                >
                  <h4>{{ formatLabel(relation) }}</h4>
                  <ul>
                    <li><strong>Full Name:</strong> {{ formatValue(member.first_name) }} {{ formatValue(member.last_name) }}</li>
                    <li><strong>Age:</strong> {{ formatValue(member.age) }}</li>
                    <li><strong>Occupation:</strong> {{ formatValue(member.occupation) }}</li>
                  </ul>
                </div>
              </div>
            </template>

            <template v-else>
              <div class="cv-entry-block">
                <template v-for="(val, subKey) in value" :key="subKey">
                  <div>
                    <strong>{{ formatLabel(subKey).toUpperCase() }}:</strong> {{ formatValue(val) }}
                  </div>
                </template>
              </div>
            </template>
          </div>

          <div v-else-if="Array.isArray(value)">
            <div v-if="value.length === 0">N/A</div>
            <div
              v-else
              v-for="(item, index) in value"
              :key="index"
              class="cv-entry-block"
            >
              <div v-if="isObject(item)">
                <div v-for="(subVal, subKey) in item" :key="subKey">
                  <strong>{{ formatLabel(subKey).toUpperCase() }}:</strong> {{ formatValue(subVal) }}
                </div>
              </div>
              <div v-else>
                {{ formatValue(item) }}
              </div>
            </div>
          </div>

          <div v-else>
            {{ formatValue(value) }}
          </div>
        </div>
      </div>

      <div v-else>
        <p>No CV data found.</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CVPreview",
  data() {
    return {
      cv: null,
      loading: true,
      error: null,
    };
  },
  methods: {
    formatLabel(key) {
      return String(key)
        .replace(/_/g, " ")
        .replace(/\b\w/g, (c) => c.toUpperCase());
    },
    isObject(value) {
      return value !== null && typeof value === "object" && !Array.isArray(value);
    },
    formatValue(value) {
      if (value === null || value === "") return "N/A";
      if (typeof value === "string") return value.toUpperCase();
      if (typeof value === "number") return value.toString();
      if (typeof value === "boolean") return value ? "YES" : "NO";
      return String(value).toUpperCase();
    },
    isEmptyObject(obj) {
      return Object.keys(obj).length === 0 && obj.constructor === Object;
    },
  },
  async created() {
    const id = this.$route.params.id;
    try {
      const response = await axios.get(`http://localhost:8000/api/submit-cv/${id}/`);
      const data = response.data;

      if (data.FAMILY && typeof data.FAMILY === "string") {
        try {
          data.FAMILY = JSON.parse(data.FAMILY);
        } catch (e) {
          console.warn("Failed to parse FAMILY field:", e);
        }
      }

      this.cv = data;
    } catch (error) {
      console.error("Error fetching CV:", error);
      this.error = `Failed to load CV data: ${error.response?.status || ""} ${error.message}`;
    } finally {
      this.loading = false;
    }
  },
};
</script>

<style scoped>
.cv-entries-container {
  display: flex;
  justify-content: center;
  align-items: start;
  min-height: 100vh;
  background: linear-gradient(135deg, #64b5f6, #8e24aa);
  padding-top: 50px;
  font-family: "Segoe UI", sans-serif;
}

.card {
  background: #fff;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
  text-align: left;
  width: 90%;
  max-width: 800px;
}

.back-btn {
  margin-bottom: 20px;
  background: none;
  border: none;
  color: #3949ab;
  font-size: 16px;
  cursor: pointer;
  text-align: left;
  padding: 0;
}

.back-btn:hover {
  text-decoration: underline;
}

.cv-section {
  margin-bottom: 20px;
  font-size: 16px;
  color: #333;
  white-space: normal;
}

.cv-entry-block {
  padding: 0.75rem 1rem;
  margin: 1rem 0;
  background-color: #f9f9f9;
  border-left: 4px solid #007acc;
  border-radius: 6px;
}

.nested-object {
  margin-left: 15px;
  margin-top: 5px;
  padding-left: 10px;
}

.sub-fields > div {
  margin-bottom: 6px;
}

ul {
  padding-left: 20px;
  margin: 0;
  list-style-type: disc;
}

li {
  margin-bottom: 5px;
}

h1 {
  margin-bottom: 20px;
  color: #333;
}

.error-msg {
  color: #b00020;
  font-weight: bold;
  margin-bottom: 20px;
}

.family-section {
  margin-top: 1rem;
}
</style>

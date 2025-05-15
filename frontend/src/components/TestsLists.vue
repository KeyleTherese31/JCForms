<template>
  <div class="admin-view-container">
    <div class="card">
      <button class="back-btn" @click="goBack">← Back to Dashboard</button>

      <h2>View Questions & Answer Keys</h2>

      <!-- Test Category Selector -->
      <div class="form-group">
        <label for="testCategorySelect">Test Category</label>
        <select id="testCategorySelect" v-model="selectedCategory" @change="loadQuestions">
          <option disabled value="">-- Select a Category --</option>
          <option v-for="category in testCategories" :key="category" :value="category">
            {{ category }}
          </option>
        </select>
      </div>

      <!-- Questions List -->
      <div v-if="questions.length > 0" class="questions-list">
        <div v-for="(q, idx) in questions" :key="q.id" class="question-card">
          <div class="question-header">
            <strong>Q{{ idx + 1 }} - {{ q.questionFormat.replace(/_/g, ' ') }}</strong>
          </div>

          <div class="question-content">
            <div v-if="q.questionType === 'text'">
              <p>{{ q.questionText }}</p>
            </div>
            <div v-else-if="q.questionType === 'image' && q.questionImageUrl">
              <img :src="q.questionImageUrl" alt="Question Image" class="question-image" />
            </div>
          </div>

          <div class="answer-key" v-if="q.hasAnswerKey">
            <strong>Answer Key:</strong>
            <template v-if="q.questionFormat === 'multiple_choice' || q.questionFormat === 'checkboxes'">
              <ul>
                <li v-for="(choice, i) in q.choices" :key="i" :class="{ correct: choice.isCorrect }">
                  {{ choice.text }}
                </li>
              </ul>
            </template>
            <template v-else>
              <span>{{ q.answerKey }}</span>
            </template>
          </div>
        </div>
      </div>

      <div v-else-if="selectedCategory">
        <p>No questions found for this category.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      testCategories: [
        'Image Pattern Analysis',
        'Basic Math',
        'Problem Analysis and Solving',
        'Reading Comprehension',
        'Pre Interview Questionnaire',
        'Sentence Completion',
        'Other'
      ],
      selectedCategory: '',
      questions: []
    };
  },
  methods: {
    async loadQuestions() {
      // Your existing fetch logic here
    },
    goBack() {
      // Using Vue Router to navigate back to dashboard
      this.$router.push('/dashboard');
    }
  }
};
</script>

<style scoped>
.admin-view-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  background: linear-gradient(135deg, #64b5f6, #8e24aa);
  font-family: 'Segoe UI', sans-serif;
  padding: 2rem 1rem;
}

.card {
  background: #fff;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 700px;
  text-align: left;
  position: relative;
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
  margin-bottom: 25px;
  color: #333;
  font-weight: 600;
  font-size: 26px;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  font-weight: 600;
  color: #333;
  display: block;
  margin-bottom: 0.5rem;
}

select {
  width: 100%;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

select:focus {
  outline: none;
  border-color: #3949ab;
}

.questions-list {
  margin-top: 2rem;
}

.question-card {
  border: 1px solid #ddd;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 1.5rem;
  background: #fafafa;
}

.question-header {
  font-weight: 700;
  color: #3949ab;
  margin-bottom: 12px;
  font-size: 18px;
}

.question-content p {
  font-size: 16px;
  color: #222;
}

.question-image {
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.answer-key {
  margin-top: 15px;
  font-weight: 600;
  color: #333;
}

.answer-key ul {
  list-style: none;
  padding-left: 0;
  margin-top: 6px;
}

.answer-key li {
  padding: 6px 12px;
  border-radius: 6px;
  margin-bottom: 6px;
  background: #e3eafc;
  color: #3949ab;
}

.answer-key li.correct {
  background: #c8e6c9;
  color: #2e7d32;
  font-weight: 700;
}

p {
  font-size: 16px;
  color: #555;
}
</style>

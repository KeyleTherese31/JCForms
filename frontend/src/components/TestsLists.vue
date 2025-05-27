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

          <div class="answer-key">
            <strong>Answer Key:</strong>

            <template v-if="q.questionFormat === 'multiple_choice' || q.questionFormat === 'checkboxes'">
              <template v-if="Array.isArray(q.choices) && q.choices.length">
                <ul v-if="q.choices.some(c => c.isCorrect)">
                  <li
                    v-for="(choice, i) in q.choices.filter(c => c.isCorrect)"
                    :key="i"
                    class="correct"
                  >
                    ✔ {{ choice.text || '[No Text]' }}
                  </li>
                </ul>
                <p v-else>No correct answer marked in choices.</p>
              </template>
              <p v-else>No choices found for this question.</p>
            </template>

            <template v-else>
              <span v-if="q.answerKey && q.answerKey.trim() !== ''">{{ q.answerKey }}</span>
              <span v-else>No correct answer provided.</span>
            </template>
          </div>

          <!-- Edit/Delete Buttons for Superadmin -->
          <div v-if="isSuperadmin" class="question-actions">
            <button @click="editQuestion(q)" class="edit-btn">✏️ Edit</button>
            <button @click="deleteQuestion(q.id)" class="delete-btn">🗑 Delete</button>
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
import axios from 'axios';

export default {
  data() {
    return {
      testCategories: [
        'Image Pattern Analysis',
        'Basic Math',
        'Problem Analysis',
        'Reading Comprehension',
        'Pre Interview Questionnaire',
        'Sentence Completion',
        'Other'
      ],
      selectedCategory: '',
      questions: [],
      isSuperadmin: localStorage.getItem('role') === 'superadmin'
    };
  },
  methods: {
    goBack() {
      this.$router.push('/dashboard');
    },
    async loadQuestions() {
      if (!this.selectedCategory) return;

      try {
        const encodedCategory = encodeURIComponent(this.selectedCategory);
        const response = await axios.get(`http://localhost:8000/api/questions/${encodedCategory}/`);
        console.log('Raw question data:', response.data);

        this.questions = response.data
          .map(q => ({
            id: q.id,
            questionType: q.question_type,
            questionFormat: q.question_format,
            questionText: q.question_text,
            questionImageUrl: q.question_image_url,
            answerKey: q.answer_key,
            hasAnswerKey: q.has_answer_key,
            choices: (q.choices || []).map(c => ({
              text: c.text || c.label || '',
              isCorrect: c.isCorrect || c.is_correct === true
            }))
          }))
          .sort((a, b) => a.id - b.id); // sort by ID
      } catch (error) {
        console.error('Error fetching questions:', error);
        this.questions = [];
      }
    },
    editQuestion(question) {
      this.$router.push({ name: 'EditQuestion', params: { id: question.id } });
    },
    async deleteQuestion(questionId) {
      if (!confirm('Are you sure you want to delete this question?')) return;

      try {
        await axios.delete(`http://localhost:8000/api/questions/delete/${questionId}/`);
        this.questions = this.questions
          .filter(q => q.id !== questionId)
          .sort((a, b) => a.id - b.id); // re-sort after deletion
      } catch (err) {
        console.error('Error deleting question:', err);
        alert('Failed to delete the question.');
      }
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
  border-left: 4px solid #2e7d32;
}

.question-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.edit-btn,
.delete-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.edit-btn {
  background-color: #fff3cd;
  color: #856404;
}

.delete-btn {
  background-color: #f8d7da;
  color: #721c24;
}

p {
  font-size: 16px;
  color: #555;
}
</style>

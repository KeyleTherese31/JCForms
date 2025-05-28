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

          <!-- Superadmin Management Buttons -->
          <div v-if="isSuperadmin" class="question-actions">
            <button class="edit-btn" @click="openEditModal(q)">Edit</button>
            <button class="delete-btn" @click="openDeleteModal(q)">Delete</button>
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
        </div>
      </div>
      <div v-else-if="selectedCategory">
        <p>No questions found for this category.</p>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal" @click.self="closeEditModal">
      <div class="modal-content">
        <h3>Edit Question</h3>
        <label>Question Text</label>
        <textarea v-model="editableQuestion.questionText" rows="4" />

        <label>Answer Key</label>
        <input type="text" v-model="editableQuestion.answerKey" />

        <div class="modal-actions">
          <button class="btn-save" @click="updateQuestion">Save</button>
          <button class="btn-cancel" @click="closeEditModal">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Delete Modal -->
    <div v-if="showDeleteModal" class="modal" @click.self="closeDeleteModal">
      <div class="modal-content">
        <p>Are you sure you want to delete this question?</p>
        <div class="modal-actions">
          <button class="btn-delete" @click="confirmDelete">Yes, Delete</button>
          <button class="btn-cancel" @click="closeDeleteModal">Cancel</button>
        </div>
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
      isSuperadmin: localStorage.getItem('admin_role') === 'superadmin', // <-- fixed this only

      showEditModal: false,
      editableQuestion: null,

      showDeleteModal: false,
      questionToDelete: null
    };
  },
  methods: {
    goBack() {
      this.$router.push('/dashboard');
    },

    async loadQuestions() {
      if (!this.selectedCategory) {
        this.questions = [];
        return;
      }
      try {
        const encodedCategory = encodeURIComponent(this.selectedCategory);
        const response = await axios.get(`http://localhost:8000/api/questions/${encodedCategory}/`);

        this.questions = response.data.map(q => ({
          id: q.id,
          questionType: q.question_type,
          questionFormat: q.question_format,
          questionText: q.question_text,
          questionImageUrl: q.question_image, // Adjust according to your backend
          answerKey: q.answer_key,
          choices: Array.isArray(q.choices)
            ? q.choices.map(c => ({
                text: c.text || c.label || '',
                isCorrect: c.is_correct === true || c.isCorrect === true
              }))
            : []
        }));
      } catch (error) {
        console.error('Error fetching questions:', error.response || error);
        this.questions = [];
      }
    },

    // EDIT MODAL LOGIC
    openEditModal(question) {
      this.editableQuestion = JSON.parse(JSON.stringify(question));
      this.showEditModal = true;
    },
    closeEditModal() {
      this.showEditModal = false;
      this.editableQuestion = null;
    },
    async updateQuestion() {
      if (!this.editableQuestion) return;

      try {
        const { id, questionText, answerKey } = this.editableQuestion;

        await axios.put(`http://localhost:8000/api/questions/${id}/`, {
          question_text: questionText,
          answer_key: answerKey
        });

        this.showEditModal = false;
        await this.loadQuestions();
      } catch (error) {
        console.error('Error updating question:', error.response || error);
        alert('Failed to update question. See console for details.');
      }
    },

    // DELETE MODAL LOGIC
    openDeleteModal(question) {
      this.questionToDelete = question;
      this.showDeleteModal = true;
    },
    closeDeleteModal() {
      this.showDeleteModal = false;
      this.questionToDelete = null;
    },
    async confirmDelete() {
      if (!this.questionToDelete) return;

      try {
        await axios.delete(`http://localhost:8000/api/questions/${this.questionToDelete.id}/`);
        this.showDeleteModal = false;
        await this.loadQuestions();
      } catch (error) {
        console.error('Error deleting question:', error.response || error);
        alert('Failed to delete question. See console for details.');
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
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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
  position: relative;
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
  white-space: pre-wrap;
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
  margin-bottom: 12px;
}

.edit-btn,
.delete-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 14px;
  user-select: none;
}

.edit-btn {
  background-color: #64b5f6;
  color: #fff;
}

.edit-btn:hover {
  background-color: #42a5f5;
}

.delete-btn {
  background-color: #e57373;
  color: #fff;
}

.delete-btn:hover {
  background-color: #ef5350;
}

/* Modal Styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.48);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 1rem;
  box-sizing: border-box;
}

.modal-content {
  background-color: #fff;
  padding: 25px 30px;
  max-width: 450px;
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
  animation: fadeInScale 0.3s ease forwards;
  text-align: left;
  user-select: text;
}

@keyframes fadeInScale {
  0% {
    opacity: 0;
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 20px;
  font-weight: 700;
  color: #3949ab;
  font-size: 22px;
}

.modal-content label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.modal-content textarea,
.modal-content input[type='text'] {
  width: 100%;
  padding: 10px 12px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #ccc;
  box-sizing: border-box;
  resize: vertical;
  transition: border-color 0.3s ease;
}

.modal-content textarea:focus,
.modal-content input[type='text']:focus {
  outline: none;
  border-color: #3949ab;
}

.modal-actions {
  margin-top: 25px;
  display: flex;
  justify-content: flex-end;
  gap: 15px;
}

.modal-actions button {
  padding: 8px 18px;
  font-weight: 700;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
  user-select: none;
  border: none;
  transition: background-color 0.25s ease;
}

.btn-save {
  background-color: #64b5f6;
  color: #fff;
}

.btn-save:hover {
  background-color: #42a5f5;
}

.btn-cancel {
  background-color: #ddd;
  color: #333;
}

.btn-cancel:hover {
  background-color: #bbb;
}

.btn-delete {
  background-color: #e57373;
  color: #fff;
}

.btn-delete:hover {
  background-color: #ef5350;
}
</style>

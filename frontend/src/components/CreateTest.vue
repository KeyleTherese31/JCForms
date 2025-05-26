<template>
  <div class="form-container">
    <div class="card">
      <h2>Create / Edit Question</h2>

      <!-- Test Category -->
      <div class="form-group">
        <label>Test Category</label>
        <select v-model="form.test_category">
          <option v-for="category in testCategories" :key="category" :value="category">
            {{ category }}
          </option>
        </select>
      </div>

      <!-- Question Type -->
      <div class="form-group">
        <label>Question Type</label>
        <select v-model="form.question_type">
          <option value="text">Text</option>
          <option value="image">Image</option>
        </select>
      </div>

      <!-- Question Content -->
      <div class="form-group" v-if="form.question_type === 'text'">
        <label>Question Text</label>
        <textarea v-model="form.question_text" rows="3"></textarea>
      </div>

      <div class="form-group" v-if="form.question_type === 'image'">
        <label>Upload Question Image</label>
        <input type="file" @change="handleImageUpload" />
        <small><i>Image upload not supported in submission yet.</i></small>
      </div>

      <!-- Question Format -->
      <div class="form-group">
        <label>Question Format</label>
        <select v-model="form.question_format">
          <option value="multiple_choice">Multiple Choice</option>
          <option value="true_false">True / False</option>
          <option value="short_answer">Short Answer</option>
          <option value="long_answer">Long Answer</option>
          <option value="checkboxes">Checkboxes</option>
        </select>
      </div>

      <!-- Has Answer Key -->
      <div class="form-group">
        <label><input type="checkbox" v-model="form.has_answer_key" /> Has Answer Key?</label>
      </div>

      <!-- Answer Choices -->
      <div v-if="form.question_format === 'multiple_choice' || form.question_format === 'checkboxes'">
        <h3>Answer Choices</h3>
        <div class="choice-row" v-for="(choice, index) in form.choices" :key="index">
          <input
            type="text"
            v-model="choice.text"
            placeholder="Choice text"
            class="choice-input"
          />
          <input
            type="checkbox"
            v-model="choice.is_correct"
            :title="form.question_format === 'multiple_choice' ? 'Correct Answer' : 'Correct Option'"
          />
          <button class="remove-btn" @click="removeChoice(index)">✕</button>
        </div>
        <button class="add-btn" @click="addChoice">Add Choice</button>
      </div>

      <!-- Answer Key -->
      <div
        v-if="form.has_answer_key &&
              form.question_format &&
              (form.question_format === 'true_false' || form.question_format.includes('answer'))"
        class="form-group"
      >
        <label>Answer Key</label>
        <input v-model="form.answer_key" placeholder="Answer key (e.g. True, short text)" />
      </div>

      <!-- Buttons -->
      <div class="button-group">
        <button class="submit-btn" @click="saveCurrentQuestion">Save This Question</button>
        <button class="submit-btn secondary" @click="submitAllQuestions" :disabled="questions.length === 0">
          Submit All Questions
        </button>
      </div>

      <!-- List of Saved Questions -->
      <div v-if="questions.length">
        <h3>Saved Questions: {{ questions.length }}</h3>
        <ul>
          <li v-for="(q, idx) in questions" :key="idx">
            {{ idx + 1 }}. {{ q.question_text || 'Image Question' }} ({{ q.question_format }})
          </li>
        </ul>
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
      form: {
        test_category: '',
        question_type: 'text',
        question_text: '',
        question_image: null,
        question_format: 'multiple_choice',
        has_answer_key: true,
        answer_key: '',
        choices: []
      },
      questions: []
    };
  },
  methods: {
    handleImageUpload(event) {
      const file = event.target.files[0];
      this.form.question_image = file;
    },
    addChoice() {
      this.form.choices.push({ text: '', is_correct: false });
    },
    removeChoice(index) {
      this.form.choices.splice(index, 1);
    },
    resetForm() {
      this.form = {
        test_category: '',
        question_type: 'text',
        question_text: '',
        question_image: null,
        question_format: 'multiple_choice',
        has_answer_key: true,
        answer_key: '',
        choices: []
      };
    },
    saveCurrentQuestion() {
      const questionCopy = JSON.parse(JSON.stringify(this.form));
      questionCopy.question_image = this.form.question_image;
      this.questions.push(questionCopy);
      alert('Question saved locally.');
      this.resetForm();
    },
    async submitAllQuestions() {
      if (!this.questions.length) return alert("No questions to submit.");

      const formData = new FormData();

      this.questions.forEach((q, index) => {
        formData.append(`questions[${index}][test_category]`, q.test_category);
        formData.append(`questions[${index}][question_type]`, q.question_type);
        formData.append(`questions[${index}][question_format]`, q.question_format);
        formData.append(`questions[${index}][has_answer_key]`, q.has_answer_key);
        formData.append(`questions[${index}][answer_key]`, q.answer_key || '');

        if (q.question_type === 'text') {
          formData.append(`questions[${index}][question_text]`, q.question_text);
        } else if (q.question_type === 'image' && q.question_image) {
          formData.append(`questions[${index}][question_image]`, q.question_image);
        }

        if (q.question_format === 'multiple_choice' || q.question_format === 'checkboxes') {
          formData.append(`questions[${index}][choices]`, JSON.stringify(q.choices));
        }
      });

      try {
        const response = await fetch('http://localhost:8000/api/questions/bulk/', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) throw new Error('Submission failed.');

        alert('Questions successfully submitted to the backend!');
        this.questions = [];
      } catch (error) {
        console.error('Error submitting questions:', error);
        alert('Submission failed. Please try again.');
      }
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
  background: linear-gradient(135deg, #7F55B1, #F49BAB);
  font-family: 'Segoe UI', sans-serif;
  padding: 1rem;
}

.card {
  background: #FFE1E0;
  color: #333;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
  text-align: left;
}

.card h2 {
  margin-bottom: 20px;
  color: #6A1B9A;
  font-weight: 700;
  font-size: 24px;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #4A148C;
}

textarea,
input[type="text"],
input[type="file"],
select {
  width: 100%;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #BA68C8;
  font-size: 14px;
  background-color: #fff5f5;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

textarea:focus,
input[type="text"]:focus,
select:focus {
  outline: none;
  border-color: #7F55B1;
  box-shadow: 0 0 0 3px rgba(127, 85, 177, 0.2);
}

.choice-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 0.75rem;
}

.choice-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #CE93D8;
  border-radius: 8px;
  font-size: 14px;
  background-color: #fff5f5;
}

.remove-btn {
  background: none;
  color: #D32F2F;
  font-weight: bold;
  border: none;
  cursor: pointer;
  font-size: 20px;
  line-height: 1;
  padding: 0 8px;
}

.add-btn {
  background-color: #7F55B1;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s ease;
}

.add-btn:hover {
  background-color: #6A1B9A;
}

.submit-btn {
  margin-top: 30px;
  background-color: #7F55B1;
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

.submit-btn:hover {
  background-color: #6A1B9A;
}

h3 {
  margin-bottom: 8px;
  font-weight: 600;
  color: #4A148C;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.submit-btn.secondary {
  background-color: #BA68C8;
}

.submit-btn.secondary:hover {
  background-color: #9C27B0;
}
</style>

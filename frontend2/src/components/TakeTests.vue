<template>
  <div class="homepage">
    <div class="card">
      <button class="back-btn" @click="goBack">← Back</button>
      <h2>Take a Test</h2>

      <!-- Category Selector -->
      <div class="form-group">
        <label for="testCategorySelect">Select Test Category</label>
        <select id="testCategorySelect" v-model="selectedCategory" @change="loadQuestions">
          <option disabled value="">-- Choose Category --</option>
          <option v-for="category in testCategories" :key="category" :value="category">
            {{ category }}
          </option>
        </select>
      </div>

      <!-- Questions -->
      <form v-if="questions.length > 0" @submit.prevent="submitAnswers">
        <div v-for="(q, idx) in questions" :key="q.id" class="question-block">
          <p><strong>Q{{ idx + 1 }} - {{ q.questionFormat.replace(/_/g, ' ') }}</strong></p>

          <div v-if="q.questionType === 'text'">{{ q.questionText }}</div>
          <img
            v-else-if="q.questionType === 'image'"
            :src="q.questionImageUrl"
            alt="Question Image"
            class="question-image"
          />

          <!-- Input Types -->
          <div class="input-group">
            <!-- Multiple Choice -->
            <div v-if="q.questionFormat === 'multiple_choice'">
              <label v-for="(choice, i) in q.choices" :key="i">
                <input type="radio" :name="'q_' + q.id" :value="choice.text" v-model="answers[q.id]" />
                {{ choice.text }}
              </label>
            </div>

            <!-- Checkboxes -->
            <div v-else-if="q.questionFormat === 'checkboxes'">
              <label v-for="(choice, i) in q.choices" :key="i">
                <input
                  type="checkbox"
                  :value="choice.text"
                  v-model="answers[q.id]"
                  :name="'q_' + q.id + '_cb'"
                />
                {{ choice.text }}
              </label>
            </div>

            <!-- True or False -->
            <div v-else-if="q.questionFormat === 'true_false'" class="true-false">
              <label>
                <input type="radio" :name="'q_' + q.id" value="True" v-model="answers[q.id]" />
                <span :class="{ selected: answers[q.id] === 'True' }">True</span>
              </label>
              <label>
                <input type="radio" :name="'q_' + q.id" value="False" v-model="answers[q.id]" />
                <span :class="{ selected: answers[q.id] === 'False' }">False</span>
              </label>
            </div>

            <!-- Short Answer -->
            <div v-else-if="q.questionFormat === 'short_answer'">
              <input type="text" v-model="answers[q.id]" placeholder="Your answer" />
            </div>

            <!-- Paragraph -->
            <div v-else-if="q.questionFormat === 'paragraph'">
              <textarea v-model="answers[q.id]" rows="3" placeholder="Your answer"></textarea>
            </div>
          </div>
        </div>

        <button type="submit">Submit Test</button>
      </form>

      <p v-else-if="selectedCategory">No questions found for this category.</p>
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
      answers: {},
      timerInterval: null  // ensure you have this if using countdown
    };
  },
  methods: {
    goBack() {
      this.$router.push('/js-homepage');
    },

    // Load questions by category
    async loadQuestions() {
      if (!this.selectedCategory) return;

      try {
        const res = await axios.get(
          `http://localhost:8000/api/questions/${encodeURIComponent(this.selectedCategory)}/`
        );

        this.questions = res.data.map(q => ({
          id: q.id,
          questionType: q.question_type,
          questionFormat: q.question_format,
          questionText: q.question_text,
          questionImageUrl: q.question_image,
          choices: Array.isArray(q.choices)
            ? q.choices.map(c => ({
                text: c.text || c.label || '',
                isCorrect: !!c.is_correct
              }))
            : []
        }));

        // Reset answers
        this.answers = {};
        this.questions.forEach(q => {
          this.answers[q.id] = q.questionFormat === 'checkboxes' ? [] : '';
        });

      } catch (err) {
        console.error("Error loading questions:", err);
      }
    },

    // Submit answers (manual or auto)
    async submitAnswers(auto = false) {
        const jobseekerId = this.$route.params.id;

        if (!jobseekerId) {
            alert("Jobseeker ID is missing. Cannot submit test.");
            return;
        }

        const payload = Object.entries(this.answers).map(([questionId, answer]) => ({
            question_id: parseInt(questionId),
            answer: Array.isArray(answer) ? answer.join(', ') : answer
        }));

        try {
            await axios.post('http://localhost:8000/api/submit-test/', {
            jobseeker_id: jobseekerId,
            answers: payload
            });

            if (this.timerInterval) clearInterval(this.timerInterval);

            alert(auto ? "Time's up! Test auto-submitted." : "Test submitted!");
            this.goBack();
        } catch (err) {
            console.error("Submission error:", err.response?.data || err.message);
            alert("Submission failed.");
        }
    },
    mounted() {
        const jobseekerId = this.$route.params.id;
        if (!jobseekerId || jobseekerId === ':id') {
            alert('Invalid jobseeker ID.');
            this.$router.push('/mobile-login');  // or wherever
            return;
        }
        // Use jobseekerId as needed...
    }
  }
};
</script>

<style scoped>
.homepage {
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
  text-align: left;
  width: 90%;
  max-width: 600px;
  overflow-y: auto;
  max-height: 90vh;
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

h2 {
  margin-bottom: 20px;
  font-size: 24px;
}

.form-group {
  margin-bottom: 20px;
}

select {
  width: 100%;
  padding: 10px;
  font-size: 15px;
  border-radius: 6px;
  border: 1px solid #ccc;
  margin-top: 5px;
}

.question-block {
  margin-bottom: 25px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.input-group {
  margin-top: 10px;
}

.input-group label {
  display: block;
  margin-bottom: 8px;
}

input[type='text'],
textarea {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  margin-top: 5px;
}

button[type='submit'] {
  width: 100%;
  background-color: #42a5f5;
  color: white;
  padding: 12px 20px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  margin-top: 20px;
  cursor: pointer;
  transition: background 0.3s ease;
}

button[type='submit']:hover {
  background-color: #1e88e5;
}

.true-false {
  display: flex;
  gap: 10px;
  margin-top: 8px;
}

.true-false span {
  padding: 8px 16px;
  background: #eee;
  border-radius: 6px;
  display: inline-block;
}

.true-false span.selected {
  background-color: #42a5f5;
  color: white;
}

.question-image {
  width: 100%;
  max-height: 200px;
  object-fit: contain;
  margin-top: 10px;
  border-radius: 6px;
}
</style>

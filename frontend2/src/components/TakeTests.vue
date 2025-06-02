<template>
  <div class="homepage">
    <div class="fixed-navbar">
      <div class="timer">Time Left: {{ formattedTime }}</div>
      <button type="submit" class="submit-btn" @click="submitAnswers">Submit Test</button>
    </div>

    <div class="card">
      <h2>Take a Test</h2>

      <form @submit.prevent>
        <div v-for="category in testCategories" :key="category" class="accordion">
          <div class="accordion-header" @click="toggleAccordion(category)">
            <h3>{{ category }}</h3>
            <span>{{ isAccordionOpen(category) ? '-' : '+' }}</span>
          </div>

          <div v-show="isAccordionOpen(category)" class="accordion-body">
            <div v-if="questionsByCategory[category] && questionsByCategory[category].length">
              <div
                v-for="(q, idx) in questionsByCategory[category]"
                :key="q.id"
                class="question-block"
              >
                <p><strong>Q{{ idx + 1 }} - {{ q.questionFormat.replace(/_/g, ' ') }}</strong></p>

                <div v-if="q.questionType === 'text'">{{ q.questionText }}</div>
                <img
                  v-else-if="q.questionType === 'image'"
                  :src="q.questionImageUrl"
                  alt="Question Image"
                  class="question-image"
                />

                <div class="input-group">
                  <div v-if="q.questionFormat === 'multiple_choice'">
                    <label v-for="(choice, i) in q.choices" :key="i">
                      <input type="radio" :name="'q_' + q.id" :value="choice.text" v-model="answers[q.id]" />
                      {{ choice.text }}
                    </label>
                  </div>

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

                  <div v-else-if="q.questionFormat === 'short_answer'">
                    <input type="text" v-model="answers[q.id]" placeholder="Your answer" />
                  </div>

                  <div v-else-if="q.questionFormat === 'long_answer'">
                    <textarea v-model="answers[q.id]" rows="5" placeholder="Your answer"></textarea>
                  </div>
                </div>
              </div>
            </div>
            <p v-else>No questions found for this category.</p>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { reactive, ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    const route = useRoute();

    const testCategories = [
      'Image Pattern Analysis',
      'Basic Math',
      'Problem Analysis',
      'Reading Comprehension',
      'Pre Interview Questionnaire',
      'Sentence Completion',
    ];

    const questionsByCategory = reactive({});
    const openAccordions = reactive({});
    const answers = reactive({});
    const timer = ref(3600); // 1 hour = 3600 seconds
    const formattedTime = ref('60:00');
    let timerInterval = null;

    const updateFormattedTime = () => {
      const minutes = Math.floor(timer.value / 60);
      const seconds = timer.value % 60;
      formattedTime.value = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    };

    const startTimer = () => {
      timerInterval = setInterval(() => {
        if (timer.value <= 0) {
          clearInterval(timerInterval);
          submitAnswers(true);
        } else {
          timer.value--;
          updateFormattedTime();
        }
      }, 1000);
    };

    const goBack = () => {
      router.push('/js-homepage');
    };

    const loadQuestionsForCategory = async (category) => {
      try {
        const res = await axios.get(`http://localhost:8000/api/questions/${encodeURIComponent(category)}/`);
        const formattedQuestions = res.data.map(q => ({
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
        questionsByCategory[category] = formattedQuestions;
        formattedQuestions.forEach(q => {
          if (!(q.id in answers)) {
            answers[q.id] = q.questionFormat === 'checkboxes' ? [] : '';
          }
        });
      } catch (err) {
        console.error(`Error loading questions for ${category}:`, err);
      }
    };

    const toggleAccordion = (category) => {
      openAccordions[category] = !openAccordions[category];
      if (!questionsByCategory[category]) {
        loadQuestionsForCategory(category);
      }
    };

    const isAccordionOpen = (category) => {
      return !!openAccordions[category];
    };

    const submitAnswers = async (auto = false) => {
      const jobseekerId = route.params.id;
      if (!jobseekerId) {
        alert('Jobseeker ID is missing. Cannot submit test.');
        return;
      }

      const payload = Object.entries(answers).map(([questionId, answer]) => ({
        question_id: parseInt(questionId),
        answer: Array.isArray(answer) ? answer.join(', ') : answer
      }));

      try {
        await axios.post('http://localhost:8000/api/submit-test/', {
          jobseeker_id: jobseekerId,
          answers: payload
        });

        if (timerInterval) clearInterval(timerInterval);

        alert(auto ? "Time's up! Test auto-submitted." : 'Test submitted!');
      } catch (err) {
        console.error('Submission error:', err.response?.data || err.message);
        alert('Submission failed.');
      }
    };

    onMounted(() => {
      const jobseekerId = route.params.id;
      if (!jobseekerId || jobseekerId === ':id') {
        alert('Invalid jobseeker ID.');
        router.push('/mobile-login');
      } else {
        updateFormattedTime();
        startTimer();
      }
    });

    return {
      testCategories,
      questionsByCategory,
      openAccordions,
      answers,
      goBack,
      toggleAccordion,
      isAccordionOpen,
      submitAnswers,
      formattedTime
    };
  }
};
</script>

<style scoped>
.homepage {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #ffa726, #ef5350);
  font-family: 'Segoe UI', sans-serif;
  padding-top: 80px;
}

.fixed-navbar {
  position: fixed;
  top: 0;
  width: 100%;
  background: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 1000;
}

.timer {
  font-size: 16px;
  font-weight: bold;
}

.submit-btn {
  background-color: #42a5f5;
  color: white;
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.card {
  background: white;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
  text-align: left;
  width: 90%;
  max-width: 700px;
  overflow-y: auto;
  max-height: 85vh;
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

.accordion {
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-bottom: 15px;
  background-color: #f8f8f8;
}

.accordion-header {
  padding: 12px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
}

.accordion-body {
  padding: 10px 15px;
}

.question-block {
  margin-bottom: 25px;
  padding: 15px;
  background-color: #fff;
  border-radius: 8px;
  border: 1px solid #ddd;
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
  resize: vertical;
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
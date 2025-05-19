<template>
  <div class="jobseeker-cv-page">
    <div class="jobseeker-cv-form container py-4">
      <div class="flex justify-start mb-4">
        <button class="back-button" @click="goBack">Back</button>
      </div>

      <div class="flex justify-center mb-4">
        <img src="@/assets/image.png" alt="JobCrest Logo" class="img" />
      </div>

      <h2 class="text-2xl text-center font-semibold mb-6">Curriculum Vitae Form</h2>

      <form @submit.prevent="submitForm" class="space-y-6">
        <div class="text-center mb-4 text-lg font-medium">
          Section {{ currentSection }} of {{ totalSections }}
        </div>

        <!-- Position and Date -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium">Position Applied for</label>
            <input type="text" v-model="form.position" class="input" required />
          </div>
          <div>
            <label class="block text-sm font-medium">Date Applied</label>
            <input type="date" v-model="form.date_applied" class="input" readonly />
          </div>
        </div>

        <!-- Sections -->
        <div v-if="currentSection === 1">
          <fieldset class="section">
            <legend class="section-title">I. PERSONAL IDENTITY</legend>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <input class="input" v-model="form.last_name" placeholder="Last Name" required />
              <input class="input" v-model="form.first_name" placeholder="First Name" required />
              <input class="input" v-model="form.middle_name" placeholder="Middle Name" />
            </div>
            <input class="input" v-model="form.address" placeholder="Full Address" />
            <input class="input" v-model="form.contact_no" placeholder="Contact No." />
            <label class="block text-sm font-medium mt-2">Date of Birth</label>
            <input type="date" v-model="form.dob" class="input" />
            <input class="input" v-model="form.pob" placeholder="Place of Birth" />
            <input class="input" type="email" v-model="form.email" placeholder="Email Address" />
            <input class="input" v-model="form.national_id" placeholder="National ID No." />
            <input class="input" v-model="form.sss_no" placeholder="SSS No." />
            <div>
              <label class="block text-sm font-medium">TIN No.</label>
              <input class="input" v-model="form.tin_no" :disabled="form.tin_new" />
              <label class="inline-flex items-center mt-1">
                <input type="checkbox" v-model="form.tin_new" class="mr-2" /> NEW
              </label>
            </div>
            <input class="input" v-model="form.pagibig" placeholder="Pag-Ibig (HDMF) No." />
            <input class="input" v-model="form.philhealth" placeholder="Philhealth No." />
            <input class="input" v-model="form.civil_status" placeholder="Civil Status" />
            <input class="input" v-model="form.no_dependents" placeholder="No. of Dependents" />
          </fieldset>
        </div>

        <div v-if="currentSection === 2"> 
          <fieldset class="section">
            <legend class="section-title">II. EDUCATIONAL BACKGROUND</legend>
            <div 
              v-for="(level, key) in form.education" 
              :key="key" 
              class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4"
            >
            <br>
              <input
                class="input"
                v-model="level.course"
                :placeholder="key === 'computer' ? 'Computer Literacy' : key === 'machine' ? 'Machine Handled' : key.charAt(0).toUpperCase() + key.slice(1) + ' Course'"
              />
              <input
                v-if="!['computer', 'machine'].includes(key)"
                class="input"
                v-model="level.school"
                placeholder="School"
              />
              <input
                v-if="!['computer', 'machine'].includes(key)"
                class="input"
                v-model="level.year"
                placeholder="Year Graduated"
              />
            </div>

            <div class="mt-4">
              <label class="block font-medium mb-2">Scholarships</label>
              <div v-for="(scholar, index) in form.scholarships" :key="index" class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-2">
                <input class="input" v-model="scholar.title" placeholder="Scholarship Title" />
                <input class="input" v-model="scholar.institution" placeholder="Institution" />
              </div>
            </div>
          </fieldset>
        </div>

        <div v-if="currentSection === 3">
          <fieldset class="section">
            <legend class="section-title">III. FAMILY BACKGROUND</legend>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
              <input class="input" v-model="form.family.spouse.last_name" placeholder="Spouse's Last Name" />
              <input class="input" v-model="form.family.spouse.first_name" placeholder="Spouse's First Name" />
              <input class="input" v-model="form.family.spouse.age" placeholder="Spouse's Age" />
              <input class="input" v-model="form.family.spouse.occupation" placeholder="Spouse's Occupation" />
            </div>
            <br>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
              <input class="input" v-model="form.family.father.last_name" placeholder="Father's Last Name" />
              <input class="input" v-model="form.family.father.first_name" placeholder="Father's First Name" />
              <input class="input" v-model="form.family.father.age" placeholder="Father's Age" />
              <input class="input" v-model="form.family.father.occupation" placeholder="Father's Occupation" />
            </div>
            <br>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
              <input class="input" v-model="form.family.mother.last_name" placeholder="Mother's Last Name" />
              <input class="input" v-model="form.family.mother.first_name" placeholder="Mother's First Name" />
              <input class="input" v-model="form.family.mother.age" placeholder="Mother's Age" />
              <input class="input" v-model="form.family.mother.occupation" placeholder="Mother's Occupation" />
            </div>
          </fieldset>
        </div>

        <div v-if="currentSection === 4">
          <fieldset class="section">
            <legend class="section-title">IV. EMPLOYMENT HISTORY</legend>
            <div
              v-for="(job, index) in [...form.employment, {}, {}].slice(0, 2)"
              :key="index"
              class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-2"
            >
              <br>
              <input class="input" v-model="job.employer" placeholder="Employer" />
              <input class="input" v-model="job.address" placeholder="Address" />
              <input class="input" v-model="job.position" placeholder="Position" />
              <input class="input" v-model="job.dates" placeholder="Tenure" />
            </div>
          </fieldset>
        </div>

        <div v-if="currentSection === 5">
          <fieldset class="section">
            <legend class="section-title">V. REFERENCES</legend>
            <div
              v-for="(ref, index) in [...form.references, {}, {}].slice(0, 2)"
              :key="index"
              class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-2"
            >
              <br>
              <input class="input" v-model="ref.name" placeholder="Name" />
              <input class="input" v-model="ref.position" placeholder="Position" />
              <input class="input" v-model="ref.contact" placeholder="Contact Information" />
              <input class="input" v-model="ref.years_known" placeholder="Yrs. Known" />
            </div>
          </fieldset>
        </div>

        <div v-if="currentSection === 6">
          <fieldset class="section">
            <legend class="section-title">VI. DECLARATION</legend>
            <p style="font-style: italic;">
            I hereby acknowledge that the above information is true and correct to the best of my knowledge and ability, and any false statements made by me on this application or any supplementary records attached thereto shall be sufficient grounds for disqualification from the company.</p>
            <input type="file" @change="handleSignatureUpload" accept="image/*" class="mt-2" />
            <div v-if="signatureUrl" class="mt-4">
              <img :src="signatureUrl" alt="Signature Preview" class="max-h-32" />
            </div>
          </fieldset>
        </div>

        <div v-if="currentSection === 7">
          <fieldset class="section">
            <legend class="section-title">VII. FINAL CONFIRMATION</legend>
            <p>Please review all your entries before submission. You can use the Previous button to go back.</p>
          </fieldset>
        </div>

        <!-- Navigation Buttons -->
        <div class="flex justify-between">
          <button type="button" class="btn-nav" @click="prevSection" :disabled="currentSection === 1">Previous</button>
          <button type="button" class="btn-nav" @click="nextSection" :disabled="currentSection === totalSections">Next</button>
          <button class="btn-submit" type="submit" v-if="currentSection === totalSections">Submit</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      theme: 'light',
      currentSection: 1,
      totalSections: 7,
      form: {
        position: '',
        date_applied: new Date().toISOString().split('T')[0],
        last_name: '',
        first_name: '',
        middle_name: '',
        address: '',
        contact_no: '',
        dob: '',
        pob: '',
        email: '',
        national_id: '',
        sss_no: '',
        tin_no: '',
        tin_new: false,
        pagibig: '',
        philhealth: '',
        civil_status: '',
        no_dependents: '',
        education: {
          college: { course: '', school: '', year: '' },
          vocational: { course: '', school: '', year: '' },
          highschool: { course: '', school: '', year: '' },
          computer: { course: '' },
          machine: { course: '' },
        },
        scholarships: [{ title: '', institution: '' }],
        family: {
          father: { last_name: '', first_name: '', age: '', occupation: '' },
          mother: { last_name: '', first_name: '', age: '', occupation: '' },
          spouse: { last_name: '', first_name: '', age: '', occupation: '' },
        },
        employment: [
          { employer: '', address: '', position: '', dates: '' },
          { employer: '', address: '', position: '', dates: '' },
        ],
        references: [
          { name: '', position: '', contact: '' },
          { name: '', position: '', contact: '' },
        ],
      },
      signatureFile: null,
      signatureUrl: '',
    };
  },
  methods: {
    toggleTheme() {
      this.theme = this.theme === 'light' ? 'dark' : 'light';
    },
    goBack() {
      this.$router.push('/');
    },
    nextSection() {
      if (this.currentSection < this.totalSections) this.currentSection++;
    },
    prevSection() {
      if (this.currentSection > 1) this.currentSection--;
    },
    handleSignatureUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.signatureFile = file;
        this.signatureUrl = URL.createObjectURL(file);
      }
    },
    async submitForm() {
      try {
        const formData = new FormData();

        // Append all form fields
        for (const key in this.form) {
          if (typeof this.form[key] === 'object') {
            formData.append(key, JSON.stringify(this.form[key]));
          } else {
            formData.append(key, this.form[key]);
          }
        }

        // Attach the signature file if it exists
        if (this.signatureFile) {
          formData.append('signature', this.signatureFile);
        }

        const response = await axios.post('http://localhost:8000/api/submit-cv/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data', // Let Axios handle it automatically, this line is optional
          },
        });

        if (response.status === 200 || response.status === 201) {
          alert('CV submitted successfully!');
          this.$router.push('/js-homepage');
        } else {
          alert('Unexpected response. Please try again.');
        }

      } catch (error) {
        console.error('Form submission failed:', error);
        alert('Failed to submit CV. Please try again.');
      }
    }
  },
};
</script>


<style scoped>
.input {
  text-transform: uppercase;
}
.jobseeker-cv-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #ffa726, #ef5350);
  font-family: 'Segoe UI', sans-serif;
  padding: 2rem 1rem;
}

.jobseeker-cv-form {
  width: 100%;
  max-width: 800px;
  background: white;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
}

.img {
  max-width: 150px;
  border-radius: 8px;
  margin-bottom: 20px;
}

h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #333;
}

.input {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background-color: white;
  color: #111827;
}

.section {
  border: 2px solid #e5e7eb;
  padding: 1rem;
  border-radius: 0.75rem;
  margin-bottom: 1rem;
  background-color: #fafafa;
}

.section-title {
  font-weight: bold;
  margin-bottom: 1rem;
  color: #374151;
  font-size: 1.125rem;
}

button {
  padding: 12px 20px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;
  gap: 10px;
}

.btn-nav {
  background-color: #42a5f5;
  color: white;
}

.btn-nav:hover {
  background-color: #1e88e5;
}

.btn-submit {
  background-color: #10b981;
  color: white;
}

.btn-submit:hover {
  background-color: #059669;
}

.back-button {
  padding: 10px 16px;
  background-color: #9e9e9e;
  color: white;
  border-radius: 8px;
}

.back-button:hover {
  background-color: #757575;
}
</style>

<template>
  <div class="jobseeker-cv-page">
    <div class="jobseeker-cv-form container py-4">
      <div class="flex justify-start mb-4">
        <button class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600" @click="goBack">
          Back
        </button>
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
            <input class="input" v-model="form.civil_status" placeholder="Civil Status and No. of Dependents" />
          </fieldset>
        </div>

        <div v-if="currentSection === 2">
          <fieldset class="section">
            <legend class="section-title">II. EDUCATIONAL BACKGROUND</legend>
            <div v-for="(level, key) in form.education" :key="key" class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <input class="input" v-model="level.course" :placeholder="key.charAt(0).toUpperCase() + key.slice(1) + ' Course'" />
              <input v-if="key !== 'graduate' && key !== 'skills' && key !== 'computer' && key !== 'machine'" class="input" v-model="level.school" placeholder="School" />
              <input v-if="key !== 'graduate' && key !== 'skills' && key !== 'computer' && key !== 'machine'" class="input" v-model="level.year" placeholder="Year Graduated" />
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
              <input class="input" v-model="form.family.father.last_name" placeholder="Father's Last Name" />
              <input class="input" v-model="form.family.father.first_name" placeholder="Father's First Name" />
              <input class="input" v-model="form.family.father.age" placeholder="Father's Age" />
              <input class="input" v-model="form.family.father.occupation" placeholder="Father's Occupation" />
            </div>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
              <input class="input" v-model="form.family.mother.last_name" placeholder="Mother's Last Name" />
              <input class="input" v-model="form.family.mother.first_name" placeholder="Mother's First Name" />
              <input class="input" v-model="form.family.mother.age" placeholder="Mother's Age" />
              <input class="input" v-model="form.family.mother.occupation" placeholder="Mother's Occupation" />
            </div>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
              <input class="input" v-model="form.family.spouse.last_name" placeholder="Spouse's Last Name" />
              <input class="input" v-model="form.family.spouse.first_name" placeholder="Spouse's First Name" />
              <input class="input" v-model="form.family.spouse.age" placeholder="Spouse's Age" />
              <input class="input" v-model="form.family.spouse.occupation" placeholder="Spouse's Occupation" />
            </div>
            <div>
              <label class="block font-medium mb-2">Siblings</label>
              <div v-for="(sibling, index) in form.family.siblings" :key="index" class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-2">
                <input class="input" v-model="sibling.last_name" placeholder="Last Name" />
                <input class="input" v-model="sibling.first_name" placeholder="First Name" />
                <input class="input" v-model="sibling.age" placeholder="Age" />
                <input class="input" v-model="sibling.occupation" placeholder="Occupation" />
              </div>
            </div>
          </fieldset>
        </div>

        <div v-if="currentSection === 4">
          <fieldset class="section">
            <legend class="section-title">IV. EMPLOYMENT HISTORY</legend>
            <div v-for="(job, index) in form.employment" :key="index" class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-2">
              <input class="input" v-model="job.employer" placeholder="Employer" />
              <input class="input" v-model="job.address" placeholder="Address" />
              <input class="input" v-model="job.position" placeholder="Position" />
              <input class="input" v-model="job.dates" placeholder="Inclusive Dates" />
            </div>
          </fieldset>
        </div>

        <div v-if="currentSection === 5">
          <fieldset class="section">
            <legend class="section-title">V. CHARACTER REFERENCES</legend>
            <div v-for="(ref, index) in form.references" :key="index" class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-2">
              <input class="input" v-model="ref.name" placeholder="Name" />
              <input class="input" v-model="ref.position" placeholder="Position" />
              <input class="input" v-model="ref.contact" placeholder="Contact Information" />
            </div>
          </fieldset>
        </div>

        <div v-if="currentSection === 6">
          <fieldset class="section">
            <legend class="section-title">VI. SIGNATURE</legend>
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
          <button class="btn-nav" @click="prevSection" :disabled="currentSection === 1">Previous</button>
          <button class="btn-nav" @click="nextSection" :disabled="currentSection === totalSections">Next</button>
          <button class="btn-submit" type="submit" v-if="currentSection === totalSections">Submit</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
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
        education: {
          college: { course: '', school: '', year: '' },
          vocational: { course: '', school: '', year: '' },
          highschool: { course: '', school: '', year: '' },
          graduate: { course: '' },
          skills: { course: '' },
          computer: { course: '' },
          machine: { course: '' },
        },
        scholarships: [{ title: '', institution: '' }],
        family: {
          father: { last_name: '', first_name: '', age: '', occupation: '' },
          mother: { last_name: '', first_name: '', age: '', occupation: '' },
          spouse: { last_name: '', first_name: '', age: '', occupation: '' },
          siblings: [{ last_name: '', first_name: '', age: '', occupation: '' }],
        },
        employment: [{ employer: '', address: '', position: '', dates: '' }],
        references: [{ name: '', position: '', contact: '' }],
      },
      signatureUrl: '',
    };
  },
  methods: {
    toggleTheme() {
      this.theme = this.theme === 'light' ? 'dark' : 'light';
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
        this.signatureUrl = URL.createObjectURL(file); // Placeholder
      }
    },
    submitForm() {
      alert('Form submitted!');
    },
    goBack() {
      this.$router.go(-1);
    },
  },
};
</script>

<style scoped>
.img {
  max-width: 80px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.jobseeker-cv-page {
  background-color: #f3f4f6;
  color: #1f2937;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}

.jobseeker-cv-form {
  width: 100%;
  max-width: 800px;
  background-color: white;
  padding: 2rem;
  border-radius: 0.75rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background-color: white;
  color: #111827;
}

.section {
  border: 2px solid #e5e7eb;
  padding: 1rem;
  border-radius: 0.5rem;
}

.section-title {
  font-weight: bold;
  margin-bottom: 1rem;
}

.btn-nav {
  padding: 0.5rem 1rem;
  background-color: #3b82f6;
  color: white;
  border-radius: 0.375rem;
  transition: background-color 0.3s;
}

.btn-nav:hover {
  background-color: #2563eb;
}

.btn-submit {
  padding: 0.5rem 1.25rem;
  background-color: #10b981;
  color: white;
  border-radius: 0.375rem;
}

.btn-submit:hover {
  background-color: #059669;
}
</style>
<template>
  <div :class="['jobseeker-cv-page', theme]">
    <div class="jobseeker-cv-form container py-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <button class="btn btn-secondary" @click="goBack">
          Back
        </button>
        <button class="btn btn-outline-light" @click="toggleTheme">
          Toggle {{ theme === 'light' ? 'Dark' : 'Light' }} Mode
        </button>
      </div>

      <img src="@/assets/image.png" alt="JobCrest Logo" class="logo mb-3" />

      <h2 class="text-center mb-4">Curriculum Vitae Form</h2>

      <form @submit.prevent="submitForm">
        <div class="text-center mb-3">
          <strong>Section {{ currentSection }} of {{ totalSections }}</strong>
        </div>

        <!-- Position and Admin Only Section -->
        <div class="form-group">
          <label>Position Applied for:</label>
          <input type="text" v-model="form.position" class="form-control" required />
        </div>
        <div class="form-group">
          <label>Date Applied:</label>
          <input type="date" v-model="form.date_applied" class="form-control" readonly />
        </div>

        <!-- Personal Identity -->
        <fieldset v-show="currentSection === 1" class="mt-4">
          <legend>I. PERSONAL IDENTITY</legend>
          <div class="form-row">
            <div class="col"><input class="form-control" v-model="form.last_name" placeholder="Last Name" required /></div>
            <div class="col"><input class="form-control" v-model="form.first_name" placeholder="First Name" required /></div>
            <div class="col"><input class="form-control" v-model="form.middle_name" placeholder="Middle Name" /></div>
          </div>
          <input class="form-control mt-2" v-model="form.address" placeholder="Full Address" />
          <input class="form-control mt-2" v-model="form.contact_no" placeholder="Contact No." />
          <label class="mt-2">Date of Birth:</label>
          <input type="date" v-model="form.dob" class="form-control" />
          <input class="form-control mt-2" v-model="form.pob" placeholder="Place of Birth" />
          <input class="form-control mt-2" v-model="form.email" type="email" placeholder="Email Address" />
          <input class="form-control mt-2" v-model="form.national_id" placeholder="National ID No." />
          <input class="form-control mt-2" v-model="form.sss_no" placeholder="SSS No." />
          <div class="form-group mt-2">
            <label>TIN No.:</label>
            <input class="form-control" v-model="form.tin_no" :disabled="form.tin_new" />
            <div class="form-check">
              <input type="checkbox" v-model="form.tin_new" class="form-check-input" id="tinNew" />
              <label for="tinNew" class="form-check-label">NEW</label>
            </div>
          </div>
          <input class="form-control mt-2" v-model="form.pagibig" placeholder="Pag-Ibig (HDMF) No." />
          <input class="form-control mt-2" v-model="form.philhealth" placeholder="Philhealth No." />
          <input class="form-control mt-2" v-model="form.civil_status" placeholder="Civil Status and No. of Dependents" />
        </fieldset>

        <!-- Educational Background -->
        <fieldset v-show="currentSection === 2" class="mt-4">
          <legend>II. EDUCATIONAL BACKGROUND</legend>
          <!-- Detailed Fields -->
          <div class="form-group">
            <label>College</label>
            <div class="form-row">
              <div class="col">
                <input class="form-control" v-model="form.education.college.course" placeholder="Course/Degree" />
              </div>
              <div class="col">
                <input class="form-control" v-model="form.education.college.school" placeholder="School/Location" />
              </div>
              <div class="col">
                <input class="form-control" v-model="form.education.college.year" placeholder="Year Attended" />
              </div>
            </div>
          </div>

          <div class="form-group">
            <label>Vocational</label>
            <div class="form-row">
              <div class="col">
                <input class="form-control" v-model="form.education.vocational.course" placeholder="Course" />
              </div>
              <div class="col">
                <input class="form-control" v-model="form.education.vocational.school" placeholder="School/Location" />
              </div>
              <div class="col">
                <input class="form-control" v-model="form.education.vocational.year" placeholder="Year Attended" />
              </div>
            </div>
          </div>

          <div class="form-group">
            <label>High School</label>
            <div class="form-row">
              <div class="col">
                <input class="form-control" v-model="form.education.highschool.course" placeholder="Course" />
              </div>
              <div class="col">
                <input class="form-control" v-model="form.education.highschool.school" placeholder="School/Location" />
              </div>
              <div class="col">
                <input class="form-control" v-model="form.education.highschool.year" placeholder="Year Attended" />
              </div>
            </div>
          </div>

          <!-- Simplified Fields -->
          <div class="form-group">
            <label>Graduate Studies</label>
            <input class="form-control" v-model="form.education.graduate.course" placeholder="(If any, just specify details)" />
          </div>

          <div class="form-group">
            <label>Special Course/Skills</label>
            <input class="form-control" v-model="form.education.skills.course" placeholder="List special skills/courses" />
          </div>

          <div class="form-group">
            <label>Computer Literacy</label>
            <input class="form-control" v-model="form.education.computer.course" placeholder="Briefly describe skills/software" />
          </div>

          <div class="form-group">
            <label>Machina/Stn Handled</label>
            <input class="form-control" v-model="form.education.machine.course" placeholder="List machinery/stations handled" />
          </div>
        </fieldset>

        <!-- Scholarships / Licenses -->
        <fieldset v-show="currentSection === 3" class="mt-4">
          <legend>III. SCHOLARSHIPS / LICENSES</legend>
          <div v-for="(item, i) in form.scholarships" :key="i" class="form-row mb-2">
            <div class="col">
              <input class="form-control" v-model="item.title" placeholder="Scholarship/Award/License" />
            </div>
            <div class="col">
              <input class="form-control" v-model="item.institution" placeholder="Institution" />
            </div>
          </div>
        </fieldset>

        <!-- Family Background -->
        <fieldset v-show="currentSection === 4" class="mt-4">
          <legend>IV. FAMILY BACKGROUND</legend>
          <div v-for="(person, key) in form.family" :key="key" class="form-group">
            <label>{{ person.label }}</label>
            <div class="form-row">
              <div class="col">
                <input class="form-control" v-model="person.last_name" placeholder="Last Name" />
              </div>
              <div class="col">
                <input class="form-control" v-model="person.first_name" placeholder="First Name" />
              </div>
              <div class="col">
                <input class="form-control" v-model="person.age" placeholder="Age" />
              </div>
              <div class="col">
                <input class="form-control" v-model="person.occupation" placeholder="Occupation" />
              </div>
            </div>
          </div>
        </fieldset>

        <!-- Employment History -->
        <fieldset v-show="currentSection === 5" class="mt-4">
          <legend>V. EMPLOYMENT HISTORY</legend>
          <div v-for="(job, i) in form.employment" :key="i" class="form-row mb-2">
            <div class="col">
              <input class="form-control" v-model="job.employer" placeholder="Employer" />
            </div>
            <div class="col">
              <input class="form-control" v-model="job.address" placeholder="Address" />
            </div>
            <div class="col">
              <input class="form-control" v-model="job.position" placeholder="Position" />
            </div>
            <div class="col">
              <input class="form-control" v-model="job.dates" placeholder="Dates Employed" />
            </div>
          </div>
        </fieldset>

        <!-- References -->
        <fieldset v-show="currentSection === 6" class="mt-4">
          <legend>VI. REFERENCES</legend>
          <div v-for="(ref, i) in form.references" :key="i" class="form-row mb-2">
            <div class="col">
              <input class="form-control" v-model="ref.name" placeholder="Name" />
            </div>
            <div class="col">
              <input class="form-control" v-model="ref.position" placeholder="Position" />
            </div>
            <div class="col">
              <input class="form-control" v-model="ref.contact" placeholder="Contact" />
            </div>
          </div>
        </fieldset>

        <!-- Signature -->
        <fieldset v-show="currentSection === 7" class="mt-4">
          <legend>VII. SIGNATURE</legend>
          <div class="form-group">
            <label>Signature</label>
            <input type="file" @change="handleSignatureUpload" />
            <p v-if="signatureUrl">Uploaded Signature:</p>
            <img :src="signatureUrl" alt="Signature" class="img-fluid" />
          </div>
        </fieldset>

        <div class="d-flex justify-content-between mt-4">
          <button class="btn btn-primary" @click="prevSection" :disabled="currentSection === 1">Previous</button>
          <button class="btn btn-primary" @click="nextSection" :disabled="currentSection === totalSections">Next</button>
          <button class="btn btn-success" type="submit" v-if="currentSection === totalSections">Submit</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      theme: "light",
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
          machine: { course: '' }
        },
        scholarships: [{ title: '', institution: '' }],
        family: {
          father: { last_name: '', first_name: '', age: '', occupation: '' },
          mother: { last_name: '', first_name: '', age: '', occupation: '' },
          spouse: { last_name: '', first_name: '', age: '', occupation: '' },
          siblings: [{ last_name: '', first_name: '', age: '', occupation: '' }]
        },
        employment: [{ employer: '', address: '', position: '', dates: '' }],
        references: [{ name: '', position: '', contact: '' }]
      },
      signatureUrl: ''
    };
  },
  methods: {
    toggleTheme() {
      this.theme = this.theme === 'light' ? 'dark' : 'light';
    },
    nextSection() {
      if (this.currentSection < this.totalSections) {
        this.currentSection++;
      }
    },
    prevSection() {
      if (this.currentSection > 1) {
        this.currentSection--;
      }
    },
    handleSignatureUpload(event) {
      const file = event.target.files[0];
      if (file) {
        // Handle file upload logic here
        // For example, upload it to Supabase Storage
        const signatureUrl = 'path_to_uploaded_file'; // Replace with actual URL after upload
        this.signatureUrl = signatureUrl;
        }
    },
    submitForm() {
        // Handle form submission logic here
        alert("Form submitted!");
        },
        goBack() {
        // Implement the back button logic, like navigating to a previous page
        this.$router.go(-1);
        }
     }
 };
</script>

<style scoped>
.jobseeker-cv-page {
  background-color: var(--background-color);
  color: var(--text-color);
}

.jobseeker-cv-form {
  max-width: 900px;
  margin: auto;
  background-color: var(--form-bg-color);
  padding: 20px;
  border-radius: 10px;
}

form input,
form select,
form textarea {
  margin-bottom: 15px;
}

form fieldset {
  border: 2px solid var(--form-border-color);
  padding: 20px;
}

fieldset legend {
  font-weight: bold;
}

img.logo {
  width: 150px;
}

.btn {
  margin-top: 20px;
}

.dark {
  --background-color: #121212;
  --text-color: #ffffff;
  --form-bg-color: #1e1e1e;
  --form-border-color: #444;
}

.light {
  --background-color: #ffffff;
  --text-color: #000000;
  --form-bg-color: #f9f9f9;
  --form-border-color: #ccc;
}
</style>


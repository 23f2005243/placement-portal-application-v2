<template>
  <div>
    <h2>Create Placement Drive</h2>
    <form @submit.prevent="createDrive">
      <div>
        <label for="name">Drive Name:</label>
        <input type="text" id="name" v-model="form.dname" required />
      </div>
      <div>
        <label for="job_title">Job Title:</label>
        <input type="text" id="job_title" v-model="form.job_title" required />
      </div>
      <div>
        <label for="job_description">Job Description:</label>
        <input type="text" id="job_description" v-model="form.job_description" required />
      </div>
      <div>
        <label for="eligible_dept">Eligible Department:</label>
        <input type="text" id="eligible_dept" v-model="form.eligible_dept" required />
      </div>
      <div>
        <label for="min_gpa">Minimum Required GPA:</label>
        <input type="text" id="min_gpa" v-model="form.min_gpa" required />
      </div>
      <div>
        <label for="eligible_yog">Eligible Graduation Year:</label>
        <input type="text" id="eligible_yog" v-model="form.eligible_yog" required />
      </div>
      <div>
        <label for="salary">Salary (LPA):</label>
        <input type="number" id="salary" v-model.number="form.salary" required />
      </div>
      <div>
        <label for="location">Location:</label>
        <input type="text" id="location" v-model="form.location" required />
      </div>
      <div>
        <label for="interview_type">Interview Type:</label>
        <select id="interview_type" name="interview_type" v-model="form.interview_type" required>
          <option value="Onsite">Onsite</option>
          <option value="Online">Online</option>
          <option value="Hybrid">Hybrid</option>
        </select>
      </div>
      <div>
        <label for="application_deadline">Application Deadline:</label>
        <input type="date" id="application_deadline" v-model="form.application_deadline" required />
      </div>
      <div><br /></div>
      <button
        type="submit"
        style="
          background-color: green;
          color: white;
          padding: 5px 10px;
          cursor: pointer;
          margin-right: 5px;
        "
      >
        Create Drive
      </button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CompanyCreateDrive',
  data() {
    return {
      form: {
        dname: '',
        job_title: '',
        job_description: '',
        eligible_dept: '',
        min_gpa: '',
        eligible_yog: '',
        salary: 0,
        location: '',
        interview_type: '',
        application_deadline: '',
      },
    }
  },
  methods: {
    async createDrive() {
      try {
        const token = localStorage.getItem('token')
        await axios.post('http://localhost:5000/api/create/drive', this.form, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        alert('Placement drive created successfully!')
        this.form = {
          dname: '',
          job_title: '',
          job_description: '',
          eligible_dept: '',
          min_gpa: '',
          eligible_yog: '',
          salary: 0,
          location: '',
          interview_type: '',
          application_deadline: '',
        }
        this.$emit('drive-created')
      } catch (error) {
        console.error('Error creating placement drive:', error)
        alert(error.response.data.message)
      }
    },
  },
}
</script>

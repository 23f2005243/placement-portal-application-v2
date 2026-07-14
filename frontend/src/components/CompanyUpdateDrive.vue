<template>
  <div>
    <h2>Update Placement Drive</h2>
    <form @submit.prevent="updateDrive">
      <div>
        <label for="name">Drive Name:</label>
        <input type="text" id="name" v-model="form.dname" disabled />
      </div>
      <div>
        <label for="job_title">Job Title:</label>
        <input type="text" id="job_title" v-model="form.job_title" />
      </div>
      <div>
        <label for="job_description">Job Description:</label>
        <input type="text" id="job_description" v-model="form.job_description" />
      </div>
      <div>
        <label for="eligible_dept">Eligible Department:</label>
        <input type="text" id="eligible_dept" v-model="form.eligible_dept" />
      </div>
      <div>
        <label for="min_gpa">Minimun Required GPA:</label>
        <input type="text" id="min_gpa" v-model="form.min_gpa" />
      </div>
      <div>
        <label for="eligible_yog">Eligible Graduation Year:</label>
        <input type="text" id="eligible_yog" v-model="form.eligible_yog" />
      </div>
      <div>
        <label for="salary">Salary (LPA):</label>
        <input type="number" id="salary" v-model.number="form.salary" />
      </div>
      <div>
        <label for="location">Location:</label>
        <input type="text" id="location" v-model="form.location" />
      </div>
      <div>
        <label for="interview_type">Interview Type:</label>
        <select id="interview_type" name="interview_type" v-model="form.interview_type">
          <option value="Onsite">Onsite</option>
          <option value="Online">Online</option>
          <option value="Hybrid">Hybrid</option>
        </select>
      </div>
      <div>
        <label for="application_deadline">Application Deadline:</label>
        <input type="date" id="application_deadline" v-model="form.application_deadline" />
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
        Update Drive
      </button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CompanyUpdateDrive',
  emits: ['back', 'drive-updated'],
  props: {
    driveId: {
      type: Number,
      required: true,
    },
  },
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
    async updateDrive() {
      try {
        const token = localStorage.getItem('token')

        await axios.put(`http://localhost:5000/api/update/drive/${this.driveId}`, this.form, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        alert('Placement drive updated successfully!')

        this.$emit('drive-updated')
        this.$emit('back')
      } catch (error) {
        console.error('Error updating placement drive:', error)
        alert(error.response?.data?.message || 'Failed to update drive')
      }
    },
    async fetchDrive() {
      try {
        const token = localStorage.getItem('token')

        const res = await axios.get(
          `http://localhost:5000/api/company/view-drive/${this.driveId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        )

        this.form = res.data
      } catch (error) {
        console.error(error)
      }
    },
  },
  mounted() {
    this.fetchDrive()
  },
}
</script>

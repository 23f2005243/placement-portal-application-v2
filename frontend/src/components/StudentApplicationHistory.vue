<template>
  <div>
    <div>My Application History</div>
    <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>Drive Name</th>
          <th>Company Name</th>
          <th>Job Title</th>
          <th>Application Type</th>
          <th>Interview Type</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="application in application_history" :key="application.aid">
          <td>{{ application.drive_name }}</td>
          <td>{{ application.company_name }}</td>
          <td>{{ application.job_title }}</td>
          <td>{{ application.application_type }}</td>
          <td>{{ application.interview_type }}</td>
          <td>{{ application.status }}</td>
        </tr>
      </tbody>
    </table></div>
  </div>
  <div><br /></div>
</template>
<script>
import axios from 'axios'

export default {
  name: 'StudentApplicationHistory',
  data() {
    return {
      application_history: [],
    }
  },
  methods: {
    async fetchApplicationHistory() {
      const token = localStorage.getItem('token')
      const res = await axios.get('http://localhost:5000/api/get/student/my-history', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      this.application_history = res.data
    },
  },

  mounted() {
    this.fetchApplicationHistory()
  },
}
</script>

<style scoped>
table {
  max-height: 500px;
  overflow: auto;
  width: 100%;
  border: 2px solid #333;
}

th,
td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: center;
}

th {
  font-weight: bold;
}
</style>

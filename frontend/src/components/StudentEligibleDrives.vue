<template>
  <div>
    <h2>Eligible Placement Drives</h2>
    <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>Drive Id</th>
          <th>Drive Name</th>
          <th>Company Name</th>
          <th>Job Title</th>
          <th>Salary (LPA)</th>
          <th>Location</th>
          <th>Application Deadline</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="drive in eligible_drives" :key="drive.did">
          <td>{{ drive.did }}</td>
          <td>{{ drive.dname }}</td>
          <td>{{ drive.cname }}</td>
          <td>{{ drive.job_title }}</td>
          <td>{{ drive.salary }}</td>
          <td>{{ drive.location }}</td>
          <td>{{ drive.application_deadline }}</td>
        </tr>
      </tbody>
    </table></div>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  data() {
    return {
      eligible_drives: [],
    }
  },
  methods: {
    async fetchEligibleDrives() {
      const token = localStorage.getItem('token')

      const res = await axios.get('http://localhost:5000/api/get/student/eligible-drives', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      this.eligible_drives = res.data
    },
  },
  mounted() {
    this.fetchEligibleDrives()
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

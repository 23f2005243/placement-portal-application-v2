<template>
  <div v-if="activeTab === 'applied_drives'">
    <div>Applied Drives</div>
    <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>Drive Name</th>
          <th>Company Name</th>
          <th>Application Date</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="application in application_details" :key="application.aid">
          <td>{{ application.drive_name }}</td>
          <td>{{ application.company_name }}</td>
          <td>{{ application.application_date }}</td>
          <td>{{ application.status }}</td>
          <td>
            <button
              @click="viewDrive(application.did)"
              style="
                background-color: blue;
                color: white;
                padding: 5px 10px;
                cursor: pointer;
                margin-right: 5px;
              "
            >
              View
            </button>
          </td>
        </tr>
      </tbody>
    </table></div>
  </div>
  <div><br /></div>
  <main>
    <StudentAppliedDriveView
      v-if="activeTab === 'viewDrive'"
      :driveId="selectedDriveId"
      @back="activeTab = 'applied_drives'"
    />
  </main>
</template>
<script>
import axios from 'axios'
import StudentAppliedDriveView from './StudentAppliedDriveView.vue'

export default {
  name: 'StudentAppliedDrives',
  components: { StudentAppliedDriveView },
  data() {
    return {
      application_details: [],
      activeTab: 'applied_drives',
      selectedDriveId: null,
    }
  },
  methods: {
    async fetchAppliedDrives() {
      const token = localStorage.getItem('token')
      const res = await axios.get('http://localhost:5000/api/student/get/applied-drives', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      this.application_details = res.data
    },
    viewDrive(driveId) {
      this.selectedDriveId = driveId
      this.activeTab = 'viewDrive'
    },
  },

  mounted() {
    this.fetchAppliedDrives()
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

<template>
  <div>
    <div>All Placement Drives</div>
    <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>Drive Name</th>
          <th>Job Title</th>
          <th>Application Deadline</th>
          <th>Number of Applicants</th>
          <th>Drive Status</th>
          <th>Deletion Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="drive in drive_details" :key="drive.did">
          <td>{{ drive.dname }}</td>
          <td>{{ drive.job_title }}</td>
          <td>{{ drive.application_deadline }}</td>
          <td>{{ drive.numOfApplicants }}</td>
          <td>{{ drive.status }}</td>
          <td>{{ drive.deletion_status }}</td>
          <td>
            <button
              v-if="drive.deletion_status === false"
              @click="viewDrive(drive.did)"
              style="
                background-color: blue;
                color: white;
                padding: 5px 10px;
                cursor: pointer;
                margin-right: 5px;
              "
            >
              View Drive
            </button>
            <button
              v-if="drive.status === 'Approved' && drive.deletion_status === false"
              @click="viewApplications(drive.did)"
              style="
                background-color: blue;
                color: white;
                padding: 5px 10px;
                cursor: pointer;
                margin-right: 5px;
              "
            >
              View Applications
            </button>
          </td>
        </tr>
      </tbody>
    </table></div>
  </div>
  <div><br /></div>
  <CompanyViewDrive
    v-if="activeTab === 'viewDrive'"
    :key="selectedDriveId"
    :driveId="selectedDriveId"
    @back="handleBack"
    @drive-deleted="handleDriveDeleted"
    @drive-updated="fetchCompanyDrives"
  />
  <CompanyUpdateDriveApplication
    v-if="activeTab === 'viewApplications'"
    :driveId="selectedDriveId"
    @back="activeTab = 'drives'"
  />
</template>
<script>
import axios from 'axios'
import CompanyUpdateDriveApplication from './CompanyUpdateDriveApplication.vue'
import CompanyViewDrive from './CompanyViewDrive.vue'

export default {
  name: 'CompanyDrives',
  components: { CompanyUpdateDriveApplication, CompanyViewDrive },
  data() {
    return {
      drive_details: [],
      activeTab: 'drives',
      selectedDriveId: null,
    }
  },
  methods: {
    async fetchCompanyDrives() {
      const token = localStorage.getItem('token')
      const res = await axios.get('http://localhost:5000/api/get/company/drives', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      this.drive_details = res.data
    },
    viewDrive(driveId) {
      this.selectedDriveId = driveId
      this.activeTab = 'viewDrive'
    },
    viewApplications(driveId) {
      this.selectedDriveId = driveId
      this.activeTab = 'viewApplications'
    },
    handleBack() {
      this.activeTab = 'drives'
      this.fetchCompanyDrives()
    },

    handleDriveDeleted() {
      this.activeTab = 'drives'
      this.fetchCompanyDrives()
    },
  },

  mounted() {
    this.fetchCompanyDrives()
  },
}
</script>

<style scoped>
table {
  width: 100%;
  border: 2px solid #333;
}

th,
td {
  max-height: 500px;
  overflow: auto;
  border: 1px solid #ddd;
  padding: 12px;
  text-align: center;
}

th {
  font-weight: bold;
}
</style>

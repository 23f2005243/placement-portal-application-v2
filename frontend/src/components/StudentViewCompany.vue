<template>
  <div><br /></div>
  <div v-if="activeTab === 'viewCompany'">
    <header>
      <h2>Company Details</h2>
      <button @click="back()">Back</button>
    </header>
    <div><br /></div>
    <div v-if="company">
      <p><strong>Company Name:</strong> {{ company.cname }}</p>
      <p>
        <strong>Company Website:</strong
        ><a :href="company.c_website" target="_blank" rel="noopener noreferrer">Visit Website</a>
      </p>
      <p><strong>Company Overview:</strong> {{ company.cabout }}</p>
      <p><strong>Company HR:</strong> {{ company.hr_contact }}</p>
    </div>
    <div><br /></div>
    <div>
      <div>Current Company Drives:</div>
      <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Drive Name</th>
            <th>Job Title</th>
            <th>Application Deadline</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="drive in drive_details" :key="drive.did">
            <td>{{ drive.dname }}</td>
            <td>{{ drive.job_title }}</td>
            <td>{{ drive.application_deadline }}</td>
            <td>
              <button
                @click="viewDrive(drive.did)"
                style="
                  background-color: blue;
                  color: white;
                  padding: 5px 10px;
                  cursor: pointer;
                  margin-right: 5px;
                "
              >
                View Details
              </button>
            </td>
          </tr>
        </tbody>
      </table></div>
    </div>
  </div>

  <StudentViewDrive
    v-else-if="activeTab === 'viewDrive'"
    :driveId="selectedDriveId"
    @back="backToCompany"
  />
</template>
<script>
import axios from 'axios'
import StudentViewDrive from './StudentViewDrive.vue'

export default {
  name: 'StudentViewCompany',
  components: { StudentViewDrive },
  props: {
    companyId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      company: null,
      drive_details: [],
      selectedDriveId: null,
      activeTab: 'viewCompany',
      loading: true,
    }
  },
  mounted() {
    this.fetchCompanyDetails()
  },
  methods: {
    async fetchCompanyDetails() {
      try {
        const token = localStorage.getItem('token')

        const res = await axios.get(
          `http://localhost:5000/api/student/view-company/${this.companyId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        )

        this.company = res.data.company
        this.drive_details = res.data.drives
      } catch (error) {
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    back() {
      this.activeTab = 'organizations'
    },
    viewDrive(driveId) {
      this.selectedDriveId = driveId
      this.activeTab = 'viewDrive'
    },
    backToCompany() {
      this.activeTab = 'viewCompany'
      this.selectedDriveId = null
    },
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

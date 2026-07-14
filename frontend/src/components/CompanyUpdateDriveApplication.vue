<template>
  <div><br /></div>
  <div v-if="activeTab === 'viewApplications'">
    <header>
      <h2>Update Applications for the drive:</h2>
      <button @click="back()">Back</button>
    </header>
    <div><br /></div>
    <div v-if="drive">
      <p><strong>Drive Name:</strong> {{ drive.dname }}</p>
      <p><strong>Job Title:</strong> {{ drive.job_title }}</p>
    </div>
    <div>
      <div><br /></div>
      <div>Received Applications:</div>
      <table>
        <thead>
          <tr>
            <th>Student Name</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="application in applications_detail" :key="application.aid">
            <td>{{ application.sname }}</td>
            <td>
              <button
                @click="reviewApplication(application.aid)"
                style="
                  background-color: blue;
                  color: white;
                  padding: 5px 10px;
                  cursor: pointer;
                  margin-right: 5px;
                "
              >
                Review Application
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <CompanyReviewApplication
    v-else-if="activeTab === 'reviewApplication'"
    :key="selectedApplicationId"
    :applicationId="selectedApplicationId"
    @back="backToApplications"
  />
</template>
<script>
import axios from 'axios'
import CompanyReviewApplication from './CompanyReviewApplication.vue'

export default {
  name: 'CompanyUpdateDriveApplication',
  components: { CompanyReviewApplication },
  props: {
    driveId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      drive: null,
      applications_detail: [],
      selectedApplicationId: null,
      activeTab: 'viewApplications',
      loading: true,
    }
  },
  mounted() {
    this.fetchApplicationsDetail()
  },
  methods: {
    async fetchApplicationsDetail() {
      try {
        const token = localStorage.getItem('token')

        const res = await axios.get(
          `http://localhost:5000/api/company/view-applications/${this.driveId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        )

        this.drive = res.data.drive
        this.applications_detail = res.data.applications
      } catch (error) {
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    back() {
      this.$emit('back')
    },
    reviewApplication(applicationId) {
      this.selectedApplicationId = applicationId
      this.activeTab = 'reviewApplication'
    },
    backToApplications() {
      this.activeTab = 'viewApplications'
      this.selectedApplicationId = null
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

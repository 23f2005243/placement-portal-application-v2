<template>
  <div><br /></div>
  <div>
    <header>
      <h2>Drive Details</h2>
      <button @click="back()">Back</button>
    </header>
    <div><br /></div>
    <div v-if="activeTab === 'view' && drive">
      <p><strong>Drive Id:</strong> {{ drive.did }}</p>
      <p><strong>Drive Name:</strong> {{ drive.dname }}</p>
      <p><strong>Job Title:</strong> {{ drive.job_title }}</p>
      <p><strong>Job Description:</strong> {{ drive.job_description }}</p>
      <p><strong>Eligible Department:</strong> {{ drive.eligible_dept }}</p>
      <p><strong>Minimum Required GPA:</strong> {{ drive.min_gpa }}</p>
      <p><strong>Eligible Graduation Year:</strong> {{ drive.eligible_yog }}</p>
      <p><strong>Salary (LPA):</strong> {{ drive.salary }}</p>
      <p><strong>Location:</strong> {{ drive.location }}</p>
      <p><strong>Interview Type:</strong> {{ drive.interview_type }}</p>
      <p><strong>Application Deadline:</strong> {{ drive.application_deadline }}</p>
      <p><strong>Status:</strong> {{ drive.status }}</p>
      <div><br /></div>
      <button
        @click="updateDrive(drive.did)"
        style="
          background-color: green;
          color: white;
          padding: 5px 10px;
          cursor: pointer;
          margin-right: 5px;
        "
      >
        Update
      </button>
      <button
        @click="deleteDrive(drive.did)"
        style="background-color: red; color: white; padding: 5px 10px; cursor: pointer"
      >
        Delete
      </button>
    </div>
    <CompanyUpdateDrive
      v-if="activeTab === 'update'"
      :driveId="drive.did"
      @drive-updated="onDriveUpdated"
    />
  </div>
</template>
<script>
import axios from 'axios'
import CompanyUpdateDrive from './CompanyUpdateDrive.vue'

export default {
  name: 'CompanyViewDrive',
  emits: ['back', 'drive-deleted'],
  components: { CompanyUpdateDrive },
  props: {
    driveId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      drive: null,
      loading: true,
      activeTab: 'view',
    }
  },

  methods: {
    async fetchDriveDetails() {
      const token = localStorage.getItem('token')

      const res = await axios.get(`http://localhost:5000/api/company/view-drive/${this.driveId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      this.drive = res.data
    },
    back() {
      this.$emit('back')
    },
    async deleteDrive(driveId) {
      try {
        const token = localStorage.getItem('token')

        await axios.put(
          `http://localhost:5000/api/delete/drive/${driveId}`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        )

        alert('Drive deleted successfully')

        this.$emit('drive-deleted')
      } catch (error) {
        console.error(error)
        alert(error.response?.data?.message || 'Delete failed')
      }
    },
    updateDrive() {
      this.activeTab = 'update'
    },
    async onDriveUpdated() {
      this.activeTab = 'view'
      this.fetchDriveDetails()
    },
  },
  mounted() {
    this.fetchDriveDetails()
  },
}
</script>

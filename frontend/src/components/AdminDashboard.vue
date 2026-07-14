<template>
  <div>
    <header>
      <h1>Admin Dashboard</h1>
      <button @click="logout()">Logout</button>
    </header>
    <div><br /></div>
    <div>
      <div>
        <h3>Total number of Students: {{ stats.total_students }}</h3>
      </div>
      <div>
        <h3>Total number of Companies: {{ stats.total_companies }}</h3>
      </div>
      <div>
        <h3>Total number of Placement Drives: {{ stats.total_drives }}</h3>
      </div>
      <div>
        <h3>Total number of Applications: {{ stats.total_applications }}</h3>
      </div>
    </div>
    <div><br /></div>
    <nav>
      <button
        @click="activeTab = 'Companies'"
        :class="{ active: activeTab === 'Companies' }"
        style="
          background-color: purple;
          color: white;
          padding: 5px 10px;
          cursor: pointer;
          margin-right: 5px;
        "
      >
        Companies
      </button>
      <button
        @click="activeTab = 'Students'"
        :class="{ active: activeTab === 'Students' }"
        style="
          background-color: purple;
          color: white;
          padding: 5px 10px;
          cursor: pointer;
          margin-right: 5px;
        "
      >
        Students
      </button>
      <button
        @click="activeTab = 'PlacementDrives'"
        :class="{ active: activeTab === 'PlacementDrives' }"
        style="
          background-color: purple;
          color: white;
          padding: 5px 10px;
          cursor: pointer;
          margin-right: 5px;
        "
      >
        Placement Drives
      </button>
      <button
        @click="activeTab = 'Applications'"
        :class="{ active: activeTab === 'Applications' }"
        style="
          background-color: purple;
          color: white;
          padding: 5px 10px;
          cursor: pointer;
          margin-right: 5px;
        "
      >
        Student Applications
      </button>
      <button
        @click="activeTab = 'summary'"
        :class="{ active: activeTab === 'summary' }"
        style="
          background-color: purple;
          color: white;
          padding: 5px 10px;
          cursor: pointer;
          margin-right: 5px;
        "
      >
        Summary
      </button>
      <button
        @click="activeTab = 'search'"
        :class="{ active: activeTab === 'search' }"
        style="
          background-color: purple;
          color: white;
          padding: 5px 10px;
          cursor: pointer;
          margin-right: 5px;
        "
      >
        Search
      </button>
    </nav>
    <div><br /></div>
    <main>
      <AdminCompanies
        v-if="activeTab === 'Companies'"
        @company-approved="onCompanyApproved"
        @company-rejected="onCompanyRejected"
        @company-blacklisted="onCompanyBlacklisted"
      />
      <AdminStudents
        v-if="activeTab === 'Students'"
        @student-activated="onStudentActivated"
        @student-deactivated="onStudentDeactivated"
      />
      <AdminDrives
        v-if="activeTab === 'PlacementDrives'"
        @drive-approved="onDriveApproved"
        @drive-rejected="onDriveRejected"
      />
      <AdminApplications v-if="activeTab === 'Applications'" />
      <AdminSummary v-if="activeTab === 'summary'" />
      <AdminSearch v-if="activeTab === 'search'" />
    </main>
    <div></div>
  </div>
</template>
<script>
import axios from 'axios'
import AdminCompanies from './AdminCompanies.vue'
import AdminStudents from './AdminStudents.vue'
import AdminDrives from './AdminDrives.vue'
import AdminApplications from './AdminApplications.vue'
import AdminSummary from '../components/AdminSummary.vue'
import AdminSearch from './AdminSearch.vue'

export default {
  name: 'AdminDashboard',
  components: { AdminCompanies, AdminStudents, AdminDrives, AdminApplications, AdminSummary, AdminSearch },

  data() {
    return {
      activeTab: 'Applications',
      stats: {
        total_students: 0,
        total_companies: 0,
        total_drives: 0,
        total_applications: 0,
      },
    }
  },
  methods: {
    async fetchDashboardStats() {
      try {
        const token = localStorage.getItem('admin_token')
        const res = await axios.get('http://localhost:5000/api/admin/dashboard-stats', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        this.stats = res.data
      } catch (err) {
        console.error(err)
      }
    },
    logout() {
      localStorage.removeItem('admin_token')
      this.$router.push('/')
    },
    onCompanyApproved() {
      this.activeTab = 'Companies'
    },
    onCompanyRejected() {
      this.activeTab = 'Companies'
    },
    onCompanyBlacklisted() {
      this.activeTab = 'Companies'
    },
    onStudentActivated() {
      this.activeTab = 'Students'
    },
    onStudentDeactivated() {
      this.activeTab = 'Students'
    },
    onDriveApproved() {
      this.activeTab = 'PlacementDrives'
    },
    onDriveRejected() {
      this.activeTab = 'PlacementDrives'
    },
  },
  mounted() {
    this.fetchDashboardStats()
  },
}
</script>

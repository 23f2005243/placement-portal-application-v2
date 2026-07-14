<template>
  <div>
    <header>
      <h1>Company Dashboard</h1>
      <button @click="logout()">Logout</button>
    </header>
    <div><br></div>
    <div v-if="company">
      <p><strong>Company Id:</strong> {{ company.cid }}</p>
      <p><strong>Company Name:</strong> {{ company.cname }}</p>
      <p><strong>Website:</strong><a :href="company.c_website" target="_blank" rel="noopener noreferrer">Visit Website</a></p>
      <p><strong>Location:</strong> {{ company.clocation }}</p>
      <p><strong>HR Contact:</strong> {{ company.hr_contact }}</p>
      <p><strong>Approval Status:</strong> {{ company.approval_status }}</p>
    </div>
    <div><br></div>
    <nav>
      <button @click="activeTab = 'create'" style="background-color: purple; color: white; padding: 5px 10px; cursor: pointer; margin-right: 5px;">Create New Drive</button>
      <button @click="activeTab = 'drives'" style="background-color: purple; color: white; padding: 5px 10px; cursor: pointer; margin-right: 5px;">Placement Drives</button>
      <button @click="activeTab = 'summary'" :class="{ active: activeTab === 'summary' }" style="background-color: purple; color: white; padding: 5px 10px; cursor: pointer; margin-right: 5px;">Summary</button>
    </nav>
    <div><br></div>
    <main>
      <CompanyCreateDrive v-if="activeTab === 'create'" :companyId="companyId" />
      <CompanyDrives v-if="activeTab === 'drives'" :companyId="companyId" @drive-deleted="onDriveDeleted"/>
      <CompanySummary v-if="activeTab === 'summary'" />
    </main>
  </div>
</template>
<script>
import axios from 'axios'
import CompanyCreateDrive from '../components/CompanyCreateDrive.vue';
import CompanyDrives from '../components/CompanyDrives.vue';
import CompanySummary from '../components/CompanySummary.vue';


export default {
  name: 'CompanyDashboard',
  components: { CompanyCreateDrive, CompanyDrives, CompanySummary },
  data() {
    return {
      activeTab: 'drives',
      companyId: null,
      company: null,
      loading: true
    }
  },
  mounted() {
    this.getCompanyInfo();
  },
  methods: {
    getCompanyInfo() {
      // Extract company ID from JWT token
      const token = localStorage.getItem('token');
      if (token) {
        const payload = JSON.parse(atob(token.split('.')[1]));
        this.companyId = payload.sub || payload.cid;
        
        // Fetch company details
        this.fetchCompanyDetails();
      }
    },
    async fetchCompanyDetails() {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get(`http://localhost:5000/api/company/${this.companyId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.company = res.data;
      } catch (error) {
        console.error('Failed to fetch company details:', error);
      } finally {
        this.loading = false;
      }
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
    },
    onDriveDeleted() {
      this.activeTab = 'PlacementDrives'
    },
  }
}
</script>
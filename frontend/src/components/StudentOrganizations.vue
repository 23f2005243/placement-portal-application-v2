<template>
  <div>
    <div>Organizations</div>
    <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>Company Name</th>
          <th>Website</th>
          <th>Headquater</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="company in company_details" :key="company.cid">
          <td>{{ company.cname }}</td>
          <td>
            <a :href="company.c_website" target="_blank" rel="noopener noreferrer">Visit Website</a>
          </td>
          <td>{{ company.clocation }}</td>
          <td>
            <button
              @click="viewCompany(company.cid)"
              style="
                background-color: blue;
                color: white;
                padding: 5px 10px;
                cursor: pointer;
                margin-right: 5px;
              "
            >
              View Company
            </button>
          </td>
        </tr>
      </tbody>
    </table></div>
  </div>
  <div><br /></div>
  <StudentViewCompany
    v-if="activeTab === 'viewCompany'"
    :key="selectedCompanyId"
    :companyId="selectedCompanyId"
    @back="activeTab = 'organizations'"
  />
</template>
<script>
import axios from 'axios'
import StudentViewCompany from './StudentViewCompany.vue'

export default {
  name: 'StudentOrganizations',
  components: { StudentViewCompany },

  data() {
    return {
      company_details: [],
      activeTab: 'organizations',
      selectedCompanyId: null,
    }
  },
  methods: {
    async fetchOrganizations() {
      const token = localStorage.getItem('token')
      const res = await axios.get('http://localhost:5000/api/get/organizations', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      this.company_details = res.data
    },
    viewCompany(companyId) {
      this.selectedCompanyId = companyId
      this.activeTab = 'viewCompany'
    },
  },

  mounted() {
    this.fetchOrganizations()
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

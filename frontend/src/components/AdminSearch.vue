<template>
  <div>
    <h3>Search Company or Student</h3>
    <br />
    <label>
      <input type="radio" value="company" v-model="searchType" />
      Company
    </label>
    <label>
      <input type="radio" value="student" v-model="searchType" />
      Student
    </label>
    <br /><br />
    <input v-model="searchText" placeholder="Search Company/Student Name or ID" />
    <button @click="search">Search</button>
    <p v-if="message">{{ message }}</p>
  </div>
  <br />
  <div>
    <table v-if="searchType === 'company'">
      <thead>
        <tr>
          <th>Company Id</th>
          <th>Company Name</th>
          <th>HR Contact</th>
          <th>Location</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
      <tr v-for="company in results" :key="company.cid">
        <td>{{ company.cid }}</td>
        <td>{{ company.cname }}</td>
        <td>{{ company.hr_contact }}</td>
        <td>{{ company.clocation }}</td>
        <td>{{ company.status }}</td>
      </tr>
      </tbody>
    </table>
    <table v-else-if="searchType === 'student'">
      <thead>
        <tr>
          <th>Student Id</th>
          <th>Student Name</th>
          <th>Department</th>
          <th>Grade Point Average</th>
          <th>Year of Graduation</th>
          <th>Contact</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="student in results" :key="student.sid">
          <td>{{ student.sid }}</td>
          <td>{{ student.sname }}</td>
          <td>{{ student.sdepartment }}</td>
          <td>{{ student.gpa }}</td>
          <td>{{ student.yog }}</td>
          <td>{{ student.contact }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  name: 'AdminSearch',

  data() {
    return {
      searchType: 'company',
      searchText: '',
      results: [],
      message: '',
    }
  },

  methods: {
    async search() {
      try {
        const token = localStorage.getItem('admin_token')

        if (!this.searchText.trim()) {
          this.message = 'Please enter a name or ID.'
          this.results = []
          return
        }

        const endpoint = this.searchType === 'company' ? 'company' : 'student'

        const response = await axios.get(
          `http://localhost:5000/api/admin/search/${endpoint}?query=${this.searchText}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        )

        this.results = response.data

        if (this.results.length === 0) {
          this.message = 'No matching records found.'
        } else {
          this.message = ''
        }
      } catch (error) {
        console.error(error)

        this.message = error.response?.data?.message || 'Error while searching.'

        this.results = []
      }
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

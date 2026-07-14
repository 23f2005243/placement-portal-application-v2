<template>
  <div><br></div>
  <div>
    <header>
      <h2>Student Application Details:</h2>
      <button @click="back()">Back</button>
    </header>
    <div><br></div>
    <div v-if="application">
      <p><strong>Application Id:</strong> {{ application.aid }}</p>
      <p><strong>Student Name:</strong> {{ application.sname }}</p>
      <p><strong>Student Department:</strong> {{ application.sdepartment }}</p>
      <p><strong>Company Name:</strong> {{ application.cname }}</p>
      <p><strong>Drive Name:</strong> {{ application.dname }}</p>
      <p><strong>Job Title:</strong> {{ application.job_title }}</p>
      <p><strong>Salary (LPA):</strong> {{ application.salary }}</p>
      <p><strong>Status:</strong> {{ application.status }}</p>
      <p><strong>Resume:</strong> <a :href="application.resume" target="_blank" rel="noopener noreferrer">View Resume</a></p>
    </div>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  name: 'AdminViewApplication',
  props: {
        applicationId: {
            type: Number,
            required: true
        }
    },
  data() {
    return {
      application: null,
      loading: true
    }
  },
  mounted() {
    this.fetchApplicationDetails();
  },
  methods: {
    async fetchApplicationDetails() {
  try {
    const token = localStorage.getItem("admin_token");
    

    const res = await axios.get(
      `http://localhost:5000/api/admin/view-application/${this.applicationId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    this.application = res.data;
  } catch (error) {
    console.error(error);
  } finally {
    this.loading = false;
  }
},
 back() {
            this.$emit('back');
        }
  }
}
</script>
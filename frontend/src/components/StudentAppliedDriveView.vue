<template>
  <div><br></div>
  <div>
    <header>
      <h2>Applied Drive Details</h2>
      <button @click="back()">Back</button>
    </header>
    <div v-if="drive">
      <p><strong>Drive Id:</strong> {{ drive.did }}</p>
      <p><strong>Drive Name:</strong> {{ drive.dname }}</p>
      <p><strong>Company Name:</strong> {{ drive.cname }}</p>
      <p><strong>Job Title:</strong> {{ drive.job_title }}</p>
      <p><strong>Job Description:</strong> {{ drive.job_description }}</p>
      <p><strong>Salary (LPA):</strong> {{ drive.salary }}</p>
      <p><strong>Location:</strong> {{ drive.location }}</p>
      <p><strong>Interview Type:</strong> {{ drive.interview_type }}</p>
    </div>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  name: 'StudentAppliedDriveView',
  props: {
        driveId: {
            type: Number,
            required: true
        }
    },
  data() {
    return {
      drive: null,
      loading: true
    }
  },
  mounted() {
    this.fetchDriveDetails();
  },
  methods: {
    async fetchDriveDetails() {
  try {
    const token = localStorage.getItem("token");
    

    const res = await axios.get(
      `http://localhost:5000/api/student/view-applied-drive/${this.driveId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    this.drive = res.data;
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
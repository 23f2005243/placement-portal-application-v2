<template>
  <div><br></div>
  <div>
    <header>
      <h2>Drive Details</h2>
      <button @click="back()">Back</button>
    </header>
    <div><br></div>
    <div v-if="drive">
      <p><strong>Drive Id:</strong> {{ drive.did }}</p>
      <p><strong>Drive Name:</strong> {{ drive.dname }}</p>
      <p><strong>Job Title:</strong> {{ drive.job_title }}</p>
      <p><strong>Job Description:</strong> {{ drive.job_description }}</p>
      <p><strong>Eligible Department:</strong> {{ drive.eligible_dept }}</p>
      <p><strong>Minimum required GPA:</strong> {{ drive.min_gpa }}</p>
      <p><strong>Eligible Graduation Year:</strong> {{ drive.eligible_yog }}</p>
      <p><strong>Salary (LPA):</strong> {{ drive.salary }}</p>
      <p><strong>Location:</strong> {{ drive.location }}</p>
      <p><strong>Interview Type:</strong> {{ drive.interview_type }}</p>
      <p><strong>Application Deadline:</strong> {{ drive.application_deadline }}</p>
      <p><strong>Status:</strong> {{ drive.status }}</p>
    </div>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  name: 'AdminViewDrive',
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
    const token = localStorage.getItem("admin_token");
    

    const res = await axios.get(
      `http://localhost:5000/api/admin/view-drive/${this.driveId}`,
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
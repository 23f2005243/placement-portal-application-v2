<template>
  <div >
    <div>Registered Students</div>
    <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Department</th>
          <th>Graduation Year</th>
          <th>Contact</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="student in student_details" :key="student.sid">
          <td>{{ student.sname }}</td>
          <td>{{ student.sdepartment }}</td>
          <td>{{ student.yog }}</td>
          <td>{{ student.contact }}</td>
          <td>{{ student.status }}</td>
          <td>
            <button
              @click="activateStudent(student.sid)"
              style="
                background-color: green;
                color: white;
                padding: 5px 10px;
                cursor: pointer;
                margin-right: 5px;
              "
            >
              Activate
            </button>
            <button
              @click="deactivateStudent(student.sid)"
              style="background-color: red; color: white; padding: 5px 10px; cursor: pointer"
            >
              Deactivate
            </button>
          </td>
        </tr>
      </tbody>
    </table></div>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  name: 'AdminStudents',
  data() {
    return {
      student_details: [],
    }
  },
  methods: {
    async fetchStudentDetails() {
      const token = localStorage.getItem('admin_token')
      const res = await axios.get('http://localhost:5000/api/get/registered-students', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      // Implement API call to fetch student details and update student_details array
      this.student_details = res.data
    },
    async activateStudent(studentId) {
      const token = localStorage.getItem('admin_token')
      await axios.put(
        `http://localhost:5000/api/admin/${studentId}/activate/student`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      )
      this.$emit('student-activated')
      this.fetchStudentDetails()
    },
    async deactivateStudent(studentId) {
      const token = localStorage.getItem('admin_token')
      await axios.put(
        `http://localhost:5000/api/admin/${studentId}/deactivate/student`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      )
      this.$emit('student-deactivated')
      this.fetchStudentDetails()
    },
  },

  mounted() {
    this.fetchStudentDetails()
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

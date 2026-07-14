<template>
    <div><br></div>
  <div>
    <h2>Apply for the Drive:</h2>
    <form @submit.prevent="applyForDrive">
      <div>
        <label for="drive_id">Drive Id:</label>
        <input type="text" id="drive_id" name="did" v-model="form.did" disabled />
      </div>
      <div>
        <label for="drive_name">Drive Name:</label>
        <input type="text" id="drive_name" name="dname" v-model="form.dname" disabled />
      </div>
      <div>
        <label for="student_id">Student Id:</label>
        <input type="text" id="student_id" name="sid" v-model="form.sid" disabled />
      </div>
      <div>
        <label for="student_name">Student Name:</label>
        <input type="text" id="student_name" name="sname" v-model="form.sname" disabled />
      </div>
      <div>
        <label for="apply_type">Application Type:</label>
        <select id="apply_type" name="atype" v-model="form.atype" required>
          <option value="Direct">Direct</option>
          <option value="Referral">Referral</option>
        </select>
      </div>
      <div>
        <label for="apply_date">Application Date:</label>
        <input type="date" id="apply_date" name="application_date" v-model="form.application_date" required />
      </div>
      <div>
        <label for="student_resume">Student Resume:</label>
        <input type="url" id="student_resume" name="resume" v-model="form.resume" required />
      </div>
      <div><br></div>
      <button type="submit" style="
          background-color: green;
          color: white;
          padding: 5px 10px;
          cursor: pointer;
          margin-right: 5px;
        ">Apply</button>
      <button type="button" @click="$emit('back')">Back</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'StudentApplyForDrive',
    props: {
        driveId: Number
    },
    data() {
        return {
            form: {
                did: "",
                dname: "",
                sid: "",
                sname: "",
                atype: "",
                application_date: "",
                resume: ""
            }
        }
    },
    methods: {
        async fetchApplicationData() {

            try {

                const token = localStorage.getItem("token");

                const res = await axios.get(
                    `http://localhost:5000/api/student/apply-drive/${this.driveId}`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                );

                this.form = res.data;
            } catch (error) {
                console.error(error);
            }

        },
        async applyForDrive() {

            try {

                const token = localStorage.getItem("token");

                await axios.post(

                    `http://localhost:5000/api/student/apply-drive/${this.driveId}`,

                    {

                        atype: this.form.atype,

                        application_date: this.form.application_date,

                        resume: this.form.resume

                    },

                    {

                        headers: {

                            Authorization: `Bearer ${token}`

                        }

                    }

                );

                alert("Applied Successfully");

                this.$emit("back");

            }

            catch (err) {

                alert(err.response?.data?.message);

            }
        },
        
    },
    mounted() {
            this.fetchApplicationData()
        }
}
</script>

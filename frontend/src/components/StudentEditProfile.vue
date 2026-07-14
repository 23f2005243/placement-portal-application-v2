<template>
    <div>
        <h2>Edit student profile:</h2>
        <form @submit.prevent="handleEdit">
            <div>
                <label for="student_name">Student Name:</label>
                <input type="text" id="student_name" name="sname" v-model="form.sname" disabled />
            </div>
            <div>
                <label for="student_department">Department Name:</label>
                <input type="text" id="student_department" name="sdepartment" v-model="form.sdepartment" disabled />
            </div>
            <div>
                <label for="student_year">Year Of Graduation:</label>
                <input type="text" id="student_year" name="yog" v-model="form.yog" disabled />
            </div>
            <div>
                <label for="student_gpa">Grade Point Average (GPA):</label>
                <input type="text" id="student_gpa" name="gpa" v-model="form.gpa" />
            </div>
            <div>
                <label for="student_contact">Student Contact:</label>
                <input type="text" id="student_contact" name="contact" v-model="form.contact" />
            </div>
            <div>
                <label for="student_resume">Student Resume:</label>
                <input type="url" id="student_resume" name="resume" v-model="form.resume" />
            </div>
            <div><br></div>
            <button type="submit" style="background-color: green; color: white; padding: 5px 10px; cursor: pointer; margin-right: 5px;">Edit Profile</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'StudentEditProfile',
    props: {
        studentId: {
            type: [String, Number],
            required: true
        }
    },
    data() {
        return {
            form: {
                sname: '',
                sdepartment: '',
                yog: '',
                gpa: '',
                contact: '',
                resume: ''
            }
        }
    },
    methods: {
        async fetchStudentProfile() {
            try {
                const token = localStorage.getItem('token')
                const res = await axios.get(`http://localhost:5000/api/student/${this.studentId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                })
                this.form = res.data
            } catch (error) {
                console.error('Failed to fetch student profile:', error)
            }
        },
        async handleEdit() {
            try {
                const token = localStorage.getItem('token')
                console.log('Sending edit request for student:', this.studentId);
                const editData = {
                    gpa: this.form.gpa,
                    contact: this.form.contact,
                    resume: this.form.resume
                }
                console.log('Edit data:', editData);
                const response = await axios.put(
                    `http://localhost:5000/api/student/edit-profile/${this.studentId}`,
                    editData,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                )
                console.log('Response:', response.data);
                alert('Profile updated successfully!')
                await this.fetchStudentProfile()
                this.$emit('profile-updated', this.form)
            } catch (error) {
                console.error('Full error:', error);
                console.error('Error response:', error.response);
                const errorMsg = error.response?.data?.message || error.message || 'Unknown error';
                alert('Failed to update profile: ' + errorMsg)
            }
        }
    },
    mounted() {
        this.fetchStudentProfile()
    }
}
</script>

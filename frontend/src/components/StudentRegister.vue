<template>
<div>
    <h1>Registering student user:</h1>
    <form @submit.prevent="handleRegister">
        <div>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" v-model="form.username" required>
        </div>
        <div>
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" v-model="form.email" required>
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" v-model="form.password" required>
        </div> 
        <div> 
            <label for="utype">Type:</label>
            <select id="utype" name="utype" v-model="form.utype" required>
                <option value="student">Student</option>
            </select>
        </div>
        <div><br><br></div>

        <h1>Registering student profile:</h1>
        <div>
            <label for="student_name">Student Name:</label>
            <input type="text" id="student_name" name="sname" v-model="form.sname" required>
        </div>
        <div>
            <label for="student_department">Department Name:</label>
            <input type="text" id="student_department" name="sdepartment" v-model="form.sdepartment" required>
        </div>
        <div>
            <label for="student_gpa">Grade Point Average (GPA):</label>
            <input type="text" id="student_gpa" name="gpa" v-model="form.gpa" required>
        </div>
        <div>
            <label for="student_year">Year Of Graduation:</label>
            <input type="text" id="student_year" name="yog" v-model="form.yog" required>
        </div>
        <div>
            <label for="student_contact">Student Contact:</label>
            <input type="number" id="student_contact" name="contact" v-model="form.contact" required>
        </div>
        <div>
            <label for="student_resume">Student Resume:</label>
            <input type="url" id="student_resume" name="resume" v-model="form.resume">
        </div>
        <div><br></div>
        <button type="submit">Register</button>
    </form>
    <div><br></div>
    <a href="#" @click.prevent="$emit('login-here')">Already have an account? Login</a>
</div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'StudentRegister',
    emits:['registered'],
    data() {
        return {
            form: {
                username: '',
                email: '',
                password: '',
                utype: 'student',
                sname: '',
                sdepartment: '',
                gpa: '',
                yog: '',
                contact: '',
                resume: ''
            }
        };
    },
    methods: {
        async handleRegister() {
            try {
                await axios.post('http://localhost:5000/api/student/register', this.form)
                this.$emit('registered')
            } catch (error) {
                console.error('Registration failed:', error);
            }
            
        }
    }
}
</script>
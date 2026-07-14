<template>
<div>
    <h1>Registering company user:</h1>
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
                <option value="company">Company</option>
            </select>
        </div>

        <div><br><br></div>
        <h1>Registering company profile:</h1>
        <div>
            <label for="company_name">Company Name:</label>
            <input type="text" id="company_name" name="cname" v-model="form.cname" required>
        </div>
        <div>
            <label for="company_description">Company About:</label>
            <textarea id="company_description" name="cabout" v-model="form.cabout" required></textarea> 
        </div>
        <div>
            <label for="company_location">Company Location:</label>
            <input type="text" id="company_location" name="clocation" v-model="form.clocation" required>
        </div>
        <div>
            <label for="company_hr">Company HR Contact:</label>
            <input type="email" id="company_hr" name="hr_contact" v-model="form.hr_contact" required>
        </div>
        <div>
            <label for="company_website">Company Website:</label>
            <input type="url" id="company_website" name="c_website" v-model="form.c_website" required>
        </div>
        <button type="submit">Register</button>
    </form>
    <div><br></div>
    <a href="#" @click.prevent="$emit('login-here')">Already have an account? Login</a>
</div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'CompanyRegister',
    emits:['registered'],
    data() {
        return {
            form: {
                username: '',
                email: '',
                password: '',
                utype: 'company',
                cname: '',
                cabout: '',
                clocation: '',
                hr_contact: '',
                c_website: '',
                approval_status: 'pending'
            }
        };
    },
    methods: {
        async handleRegister() {
            try {
                await axios.post('http://localhost:5000/api/company/register', this.form)
                this.$emit('registered')
            } catch (error) {
                console.error('Registration failed:', error);
            }
            
        }
    }
}
</script>
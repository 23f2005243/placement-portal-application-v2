<template>
  <div>
    <h1>Student Login</h1>
    <div><br></div>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" v-model="form.username" required>
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" v-model="form.password" required>
      </div>
      <div><br></div>
      <button type="submit">Login</button>
    </form>
    <div><br></div>
    <a href="#" @click.prevent="$emit('register-here')">Do not have an account ? Register</a>

  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'StudentLogin',
  data () {
    return {
      form: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    async handleLogin () {
      try {
        const response = await axios.post('http://localhost:5000/api/student/login', this.form)
        console.log('Login response:', response.data)
        localStorage.setItem('token', response.data.data.access_token)
        this.$emit('logged-in')
      } catch (error) {
        console.error('Login error:', error)
        if (error.response) {
          alert(error.response.data.message)
        } else {
          alert('Something went wrong.')
        }
      }
    }
  }
}
</script>
<template>
<div>
  <div v-if="!isLoggedIn">
      <StudentLogin v-if="!showRegister" @logged-in="handlelogin" @register-here="showRegister =true"/>
      <StudentRegister v-else  @registered="handleRegistration" @login-here="showRegister =false"/>
  </div>

<div v-else>
    <StudentDashboard  />
</div>


</div>

</template>

<script>
import StudentDashboard from '@/components/StudentDashboard.vue';
import StudentLogin from '../components/StudentLogin.vue'
import StudentRegister from '../components/StudentRegister.vue'

export default {
  name: 'StudentView',
  components: {
    StudentLogin,
    StudentDashboard,
    StudentRegister
  },
  data () {
    return {
      isLoggedIn: false,
      showRegister: true
    }
  },
  methods: {
    handleRegistration() {
      this.showRegister = false;
      this.isLoggedIn = false;
    },
    handlelogin() {
      this.isLoggedIn = true;
    }
  }
}
</script>
<template>
    <div>
        <header>
            <h1>Student Dashboard</h1>
            <button @click="logout()">Logout</button>
        </header>
        <div><br></div>
        <div v-if="student">
            <p><strong>Student Id:</strong> {{ student.sid }}</p>
            <p><strong>Name:</strong> {{ student.sname }}</p>
            <p><strong>Department:</strong> {{ student.sdepartment }}</p>
            <p><strong>GPA:</strong> {{ student.gpa }}</p>
            <p><strong>Graduation Year:</strong> {{ student.yog }}</p>
            <p><strong>Contact:</strong> {{ student.contact }}</p>
            <p><strong>Resume:</strong> <a :href="student.resume" target="_blank" rel="noopener noreferrer">View Resume</a></p>
            <p><strong>Account Status:</strong> {{ student.status }}</p>
        </div>
        <div><br></div>
        <nav>
            <button @click="activeTab = 'edit_profile'" :class="{ active: activeTab === 'edit_profile' }" style="background-color: purple; color: white; padding: 5px 10px; cursor: pointer; margin-right: 5px;">Edit Profile</button>
            <button @click="activeTab = 'organizations'" :class="{ active: activeTab === 'organizations' }" style="background-color: purple; color: white; padding: 5px 10px; cursor: pointer; margin-right: 5px;">Organizations</button>
            <button @click="activeTab = 'applied_drives'" :class="{ active: activeTab === 'applied_drives' }" style="background-color: purple; color: white; padding: 5px 10px; cursor: pointer; margin-right: 5px;">Applied Drives</button>
            <button @click="activeTab = 'application_history'" :class="{ active: activeTab === 'application_history' }" style="background-color: purple; color: white; padding: 5px 10px; cursor: pointer; margin-right: 5px;">My Application History</button>
            <button @click="activeTab = 'summary'" :class="{ active: activeTab === 'summary' }" style="background-color: purple; color: white; padding: 5px 10px; cursor: pointer; margin-right: 5px;">Summary</button>
            <button @click="activeTab = 'eligibility'" :class="{ active: activeTab === 'eligibility' }" style="background-color: purple; color: white; padding: 5px 10px; cursor: pointer; margin-right: 5px;">Eligibility Filter</button>
        </nav>
        <div><br></div>
        <main>
            <StudentEditProfile v-if="activeTab === 'edit_profile'" :studentId="studentId" @profile-updated="onProfileUpdated" />
            <StudentOrganizations v-if="activeTab === 'organizations'" />
            <StudentAppliedDrives v-if="activeTab === 'applied_drives'" />
            <StudentApplicationHistory v-if="activeTab === 'application_history'" />
            <StudentSummary v-if="activeTab === 'summary'" />
            <StudentEligibleDrives v-if="activeTab === 'eligibility'" />
        </main>
    </div>
</template>
<script>
import axios from 'axios'
import StudentOrganizations from './StudentOrganizations.vue'
import StudentAppliedDrives from './StudentAppliedDrives.vue'
import StudentEditProfile from './StudentEditProfile.vue'
import StudentApplicationHistory from './StudentApplicationHistory.vue';
import StudentSummary from '../components/StudentSummary.vue';
import StudentEligibleDrives from './StudentEligibleDrives.vue';

export default {
    name: 'StudentDashboard',
    components: { StudentOrganizations, StudentAppliedDrives, StudentEditProfile, StudentApplicationHistory, StudentSummary, StudentEligibleDrives },
    data() {
        return {
            activeTab: 'organizations',
            studentId: null,
            student: null,
            loading: true
        }
    },
    mounted() {
        this.getStudentInfo();
    },
    methods: {
        getStudentInfo() {
            // Extract student ID from JWT token
            const token = localStorage.getItem('token');
            if (token) {
                const payload = JSON.parse(atob(token.split('.')[1]));
                this.studentId = payload.sub || payload.sid;
                
                // Fetch student details
                this.fetchStudentDetails();
            }
        },
        async fetchStudentDetails() {
            try {
                const token = localStorage.getItem('token');
                const res = await axios.get(`http://localhost:5000/api/student/${this.studentId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                this.student = res.data;
                console.log('Student details loaded:', this.student);
            } catch (error) {
                console.error('Failed to fetch student details:', error);
            } finally {
                this.loading = false;
            }
        },
        async fetchStudentHistory() {
            try {
                const token = localStorage.getItem('token');
                const res = await axios.get('http://localhost:5000/api/get/student/my-history', {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                this.student = res.data;
                console.log('Student appliaction history loaded:', this.student);
            } catch (error) {
                console.error('Failed to fetch student aplication history:', error);
            } finally {
                this.loading = false;
            }
        },
        logout() {
            localStorage.removeItem('token')
            this.$router.push('/')
        },
        onProfileUpdated() {
            // Refresh student details when profile is updated
            this.fetchStudentDetails();
            // Switch to show updated profile
            this.activeTab = 'organizations';
        }
    },
}
</script>

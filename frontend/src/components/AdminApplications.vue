<template>
    <div>
        <div>Student Applications:</div>
        <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Student Name</th>
                    <th>Drive Name</th>
                    <th>Company Name</th>
                    <th>Application Date</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="application in application_details" :key="application.aid">
                    <td>{{ application.student_name }}</td>
                    <td>{{ application.drive_name }}</td>
                    <td>{{ application.company_name }}</td>
                    <td>{{ application.application_date }}</td>
                    <td>{{ application.status }}</td>
                    <td><button @click="viewApplication(application.aid)"
                            style="background-color: blue; color: white; padding: 5px 10px; cursor: pointer; margin-right: 5px;">
                            View
                        </button></td>
                </tr>
            </tbody>
        </table></div>
    </div>
    <div><br></div>
    <main>
        <AdminViewApplication v-if="activeTab === 'viewApplication'" :applicationId="selectedApplicationId"
            @back="activeTab = 'Applications'" />
    </main>
</template>
<script>
import axios from 'axios';
import AdminViewApplication from './AdminViewApplication.vue';

export default {
    name: 'AdminApplications',
    components: { AdminViewApplication },
    data() {
        return {
            application_details: [],
            activeTab: 'Applications',
            selectedApplicationId: null
        }
    },
    methods: {
        async fetchApplicationDetails() {
            const token = localStorage.getItem('admin_token');
            const res = await axios.get('http://localhost:5000/api/get/student-applications', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            // Implement API call to fetch application details and update application_details array
            this.application_details = res.data;
        },
        viewApplication(applicationId) {
            this.selectedApplicationId = applicationId;
            this.activeTab = 'viewApplication';
        }
    },

    mounted() {
        this.fetchApplicationDetails();
    }

}
</script>

<style scoped>
table {
    width: 100%;
    max-height: 500px;
    overflow: auto;
    border: 2px solid #333;
}

th, td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: center;
}

th {
    font-weight: bold;
}

</style>
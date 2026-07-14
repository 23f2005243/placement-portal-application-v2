<template>
    <div>
        <div>Placement Drives:</div>
        <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Drive Name</th>
                    <th>Company Name</th>
                    <th>Job Title</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="drive in drive_details" :key="drive.did">
                    <td>{{ drive.dname }}</td>
                    <td>{{ drive.cname }}</td>
                    <td>{{ drive.job_title }}</td>
                    <td>{{ drive.status }}</td>
                    <td><button @click="viewDrive(drive.did)"
                            style="background-color: blue; color: white; padding: 5px 10px; cursor: pointer; margin-right: 5px;">
                            View
                        </button>
                        <button @click="approveDrive(drive.did)"
                            style="background-color: green; color: white; padding: 5px 10px; cursor: pointer; margin-right: 5px;">
                            Approve
                        </button>
                        <button @click="rejectDrive(drive.did)"
                            style="background-color: red; color: white; padding: 5px 10px; cursor: pointer;">
                            Reject
                        </button>
                    </td>
                </tr>
            </tbody>
        </table></div>
    </div>
    <div><br></div>
    <main>
        <AdminViewDrive v-if="activeTab === 'viewDrive'" :driveId="selectedDriveId" @back="activeTab = 'drives'" />
    </main>
</template>
<script>
import axios from 'axios';
import AdminViewDrive from './AdminViewDrive.vue';

export default {
    name: 'AdminDrives',
    components: { AdminViewDrive },

    data() {
        return {
            drive_details: [],
            activeTab: 'drives',
            selectedDriveId: null
        }
    },
    methods: {
        async fetchDriveDetails() {
            const token = localStorage.getItem('admin_token');
            const res = await axios.get('http://localhost:5000/api/get/placement-drives', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            // Implement API call to fetch drive details and update drive_details array
            this.drive_details = res.data;
        },
        viewDrive(driveId) {
            this.selectedDriveId = driveId;
            this.activeTab = 'viewDrive';
        },
        async approveDrive(driveId) {
            const token = localStorage.getItem('admin_token');
            await axios.put(`http://localhost:5000/api/admin/${driveId}/approve/drive`, {}, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            this.$emit('drive-approved')
            this.fetchDriveDetails();



        },
        async rejectDrive(driveId) {
            const token = localStorage.getItem('admin_token');
            await axios.put(`http://localhost:5000/api/admin/${driveId}/reject/drive`, {}, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            this.$emit('drive-rejected')
            this.fetchDriveDetails();


        }
    },

    mounted() {
        this.fetchDriveDetails();
    }

}
</script>

<style scoped>
table {
    max-height: 500px;
    overflow: auto;
    width: 100%;
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
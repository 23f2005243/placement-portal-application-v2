<template>
    <div><br></div>
    <div  v-if="activeTab === 'viewDrive'">
        <header>
            <h2>Drive Details</h2>
            <button @click="back()">Back</button>
        </header>
        <div><br></div>
        <div v-if="drive">
            <p><strong>Drive Id:</strong> {{ drive.did }}</p>
            <p><strong>Drive Name:</strong> {{ drive.dname }}</p>
            <p><strong>Company Name:</strong> {{ drive.cname }}</p>
            <p><strong>Job Title:</strong> {{ drive.job_title }}</p>
            <p><strong>Job Description:</strong> {{ drive.job_description }}</p>
            <p><strong>Eligible Department:</strong> {{ drive.eligible_dept }}</p>
            <p><strong>Minimum Required GPA:</strong> {{ drive.min_gpa }}</p>
            <p><strong>Eligible Graduation Year:</strong> {{ drive.eligible_yog }}</p>
            <p><strong>Salary (LPA):</strong> {{ drive.salary }}</p>
            <p><strong>Location:</strong> {{ drive.location }}</p>
            <p><strong>Interview Type:</strong> {{ drive.interview_type }}</p>
            <p><strong>Application Deadline:</strong> {{ drive.application_deadline }}</p>
            <div><br></div>
            <button @click="applyDrive"
            style="background-color: green; color: white; padding: 5px 10px; cursor: pointer; margin-right: 5px;">Apply
            Drive</button>
        </div>
    </div>
    
    <StudentApplyForDrive
        v-else
        :driveId="driveId"
        @back="activeTab='viewDrive'"
    />
</template>
<script>
import axios from 'axios'
import StudentApplyForDrive from './StudentApplyForDrive.vue';

export default {
    name: 'StudentViewDrive',
    components:{
        StudentApplyForDrive
    },
    props: {
        driveId:Number
    },
    data() {
        return {
            drive: null,
            loading: true,
            activeTab:"viewDrive"
        }
    },
    mounted() {
        this.fetchDriveDetails();
    },
    methods: {
        async fetchDriveDetails() {
            try {
                const token = localStorage.getItem("token");


                const res = await axios.get(
                    `http://localhost:5000/api/student/view-drive/${this.driveId}`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                );

                this.drive = res.data;
            } catch (error) {
                console.error(error);
            } finally {
                this.loading = false;
            }
        },
        applyDrive(){

            this.activeTab="applyDrive";

        },
        back() {
            this.$emit('back');
        }
    }
}
</script>
<template>
    <div><br></div>
    <div>
        <header>
            <h2>Review Student Application Details:</h2>
            <button @click="back()">Back</button>
        </header>
        <div><br></div>
        <div v-if="application">
            <p><strong>Student Name:</strong> {{ application.sname }}</p>
            <p><strong>Student Department:</strong> {{ application.sdepartment }}</p>
            <p><strong>Drive Name:</strong> {{ application.dname }}</p>
            <p><strong>Job Title:</strong> {{ application.job_title }}</p>
            <p><strong>Status:</strong> {{ application.status }}</p>
            <p><strong>Resume:</strong> <a :href="application.resume" target="_blank" rel="noopener noreferrer">View Resume</a></p>
            <div><br></div>
            <form @submit.prevent="selectionStatus">
                <div>
                    <label for="selection_status">Selection Status:</label>
                    <select id="selection_status" name="status" v-model="form.status" required>
                        <option value="Shortlisted">Shortlisted</option>
                        <option value="Selected">Selected</option>
                        <option value="Rejected">Rejected</option>
                    </select>
                </div>
                <div><br></div>
                <button type="submit" style="background-color: green; color: white; padding: 5px 10px; cursor: pointer; margin-right: 5px;">Update Selection Status</button>
            </form>
        </div>
    </div>
</template>
<script>
import axios from 'axios'

export default {
    name: 'CompanyReviewApplication',
    props: {
        applicationId: {
            type: Number,
            required: true
        }
    },
    data() {
        return {
            application: null,
            loading: true,
            form: {
                status: ""
            }
        }
    },
    mounted() {
        this.fetchApplicationDetails();
    },
    methods: {
        async fetchApplicationDetails() {
            try {
                const token = localStorage.getItem("token");


                const res = await axios.get(
                    `http://localhost:5000/api/company/review-application/${this.applicationId}`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                );

                this.application = res.data;
                this.form.status = res.data.status;
            } catch (error) {
                console.error(error);
            } finally {
                this.loading = false;
            }
        },
        back() {
            this.$emit('back');
        },
        async selectionStatus() {
            try {
                const token = localStorage.getItem("token");

                await axios.put(
                    `http://localhost:5000/api/company/update-selection-status/${this.applicationId}`,
                    {
                        status: this.form.status
                    },
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                );

                this.application.status = this.form.status;

                alert("Selection status updated successfully.");

            } catch (error) {
                console.error(error);
                alert("Failed to update selection status.");
            }
        }
    }
}
</script>
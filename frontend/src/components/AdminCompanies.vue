<template>
    <div>
        <div>Registered Companies</div>
        <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Company Name</th>
                    <th>Website</th>
                    <th>Headquater</th>
                    <th>Approval Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="company in company_details" :key="company.cid">
                    <td>{{ company.cname }}</td>
                    <td><a :href="company.c_website" target="_blank" rel="noopener noreferrer">Visit Website</a></td>
                    <td>{{ company.clocation }}</td>
                    <td>{{ company.approval_status }}</td>
                    <td><button v-if="company.approval_status === 'Approved'"
                            @click="blacklistCompany(company.cid)"
                            style="background-color: grey; color: white; padding: 5px 10px; cursor: pointer; margin-right: 5px;">
                            Blacklist
                        </button></td>
                </tr>
            </tbody>
        </table></div>
    </div>

    <div>
        <div>Company Applications</div>
        <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th>Company Name</th>
                    <th>Website</th>
                    <th>Headquater</th>
                    <th>Approval Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="company_app in company_applications" :key="company_app.cid">
                    <td>{{ company_app.cname }}</td>
                    <td><a :href="company_app.c_website" target="_blank" rel="noopener noreferrer">Visit Website</a></td>
                    <td>{{ company_app.clocation }}</td>
                    <td>{{ company_app.approval_status }}</td>
                    <td>
                        <button v-if="company_app.approval_status === 'Pending'"
                            @click="approveCompany(company_app.cid)"
                            style="background-color: green; color: white; padding: 5px 10px; cursor: pointer; margin-right: 5px;">
                            Approve
                        </button>
                        <button @click="rejectCompany(company_app.cid)" v-if="company_app.approval_status === 'Pending'"
                            style="background-color: red; color: white; padding: 5px 10px; cursor: pointer;">
                            Reject
                        </button>
                    </td>
                </tr>
            </tbody>
        </table></div>
    </div>
    <div><br></div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'AdminCompanies',
    data() {
        return {
            company_details: [],
            company_applications: []
        }
    },
    methods: {
        async fetchCompanyDetails() {
            const token = localStorage.getItem('admin_token');
            const res = await axios.get('http://localhost:5000/api/get/registered-companies', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            // Implement API call to fetch company details and update company_details array
            this.company_details = res.data;
        },
        async fetchCompanyApplications() {
            const token = localStorage.getItem('admin_token');
            const res = await axios.get('http://localhost:5000/api/get/company-applications', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            // Implement API call to fetch company applications and update company_applications array
            this.company_applications = res.data;
        },
        async approveCompany(companyId) {
            const token = localStorage.getItem('admin_token');
            await axios.put(`http://localhost:5000/api/admin/${companyId}/approve/company`, {}, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            this.$emit('company-approved')
            this.fetchCompanyDetails();
            this.fetchCompanyApplications(); // Refresh the company applications list
            

        },
        async rejectCompany(companyId) {
            const token = localStorage.getItem('admin_token');
            await axios.put(`http://localhost:5000/api/admin/${companyId}/reject/company`, {}, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            this.$emit('company-rejected')
            this.fetchCompanyDetails();
            this.fetchCompanyApplications(); // Refresh the company applications list
            
        },
        async blacklistCompany(companyId) {
            const token = localStorage.getItem('admin_token');
            await axios.put(`http://localhost:5000/api/admin/${companyId}/blacklist/company`, {}, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            this.$emit('company-blacklisted')
            this.fetchCompanyDetails();
            this.fetchCompanyApplications(); // Refresh the company applications list
            

        },
    },

    mounted() {
        this.fetchCompanyDetails();
        this.fetchCompanyApplications();
    }

}
</script>

<style scoped>
table {
    width: 100%;
    max-height: 500px;
    overflow: auto;
    border: 2px solid #333;
    margin-bottom: 30px;
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

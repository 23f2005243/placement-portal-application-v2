<template>
  <div>
    <h2>Student Placement Statistics Summary</h2>
    <div><br /></div>
    <p><strong>Total Applications:</strong> {{ summary.total_applied }}</p>
    <p><strong>Total Shortlisted:</strong> {{ summary.total_shortlisted }}</p>
    <p><strong>Total Selected:</strong> {{ summary.total_selected }}</p>
    <p><strong>Total Rejected:</strong> {{ summary.total_rejected }}</p>
    <div><br /></div>
    <button @click="triggerExport">Export My Application Report</button>
    <div><br /></div>
    <div v-if="summary.company_names.length">
      <h3>Applications by Company</h3>
      <div>
        <Bar :data="barChartData" :options="chartOptions" />
      </div>
    </div>
    <div><br /><br /></div>
    <div v-if="summary.total_applied > 0">
      <h3>Application Status Distribution</h3>
      <div>
        <Pie :data="pieChartData" :options="chartOptions" />
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  ArcElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'

import { Bar, Pie } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend)

export default {
  name: 'StudentSummary',
  components: { Bar, Pie },
  data() {
    return {
      summary: {
        company_names: [],
        application_counts: [],
        total_applied: 0,
        total_shortlisted: 0,
        total_selected: 0,
        total_rejected: 0,
      },
      exmsg: null,
    }
  },
  computed: {
    barChartData() {
      return {
        labels: this.summary.company_names || [],
        datasets: [
          {
            label: 'Applications',
            data: this.summary.application_counts || [],
            backgroundColor: '#42A5F5',
          },
        ],
      }
    },

    pieChartData() {
      return {
        labels: ['Shortlisted', 'Selected', 'Rejected'],
        datasets: [
          {
            data: [
              this.summary.total_shortlisted || 0,
              this.summary.total_selected || 0,
              this.summary.total_rejected || 0,
            ],
            backgroundColor: ['#FFC107', '#4CAF50', '#F44336'],
          },
        ],
      }
    },

    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          },
        },
      }
    },
  },

  methods: {
    async fetchSummary() {
      try {
        const response = await axios.get('http://localhost:5000/api/student/summary', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })
        console.log(response.data)
        this.summary = response.data
      } catch (error) {
        console.error('Error fetching summary:', error)
      }
    },
    async triggerExport() {
      const token = localStorage.getItem('token')
      const response = await axios.get('http://localhost:5000/api/export/applications', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      this.exmsg = response.data
      console.log(this.exmsg)
      alert('check your mail!!')
    },
  },
  mounted() {
    this.fetchSummary()
  },
}
</script>

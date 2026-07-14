<template>
  <div>
    <h2>Admin Placement Statistics Summary</h2>
    <div><br /></div>
    <p><strong>Total Companies:</strong> {{ summary.total_companies }}</p>
    <p><strong>Total Drives:</strong> {{ summary.total_drives }}</p>
    <p><strong>Total Applications:</strong> {{ summary.total_applications }}</p>
    <p><strong>Total Selected:</strong> {{ summary.total_selected }}</p>
    <div><br /></div>
    <div>
      <h3>Placement Drives Conducted by Company</h3>
      <div>
      <Bar :data="driveChartData" :options="chartOptions" /></div>
    </div>
    <div><br /><br /></div>
    <div>
      <h3>Applications vs Selected by Company</h3>
      <div>
      <Bar :data="applicationChartData" :options="chartOptions" /></div>
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
  CategoryScale,
  LinearScale,
} from 'chart.js'

import { Bar } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default {
  name: 'AdminSummary',
  components: { Bar },
  data() {
    return {
      summary: {
        company_names: [],
        drive_counts: [],
        applied_counts: [],
        selected_counts: [],
        total_companies: 0,
        total_drives: 0,
        total_applications: 0,
        total_selected: 0,
      },
    }
  },
  computed: {
    driveChartData() {
      return {
        labels: this.summary.company_names,
        datasets: [
          {
            label: 'Drives Conducted',
            data: this.summary.drive_counts,
            backgroundColor: '#42A5F5',
          },
        ],
      }
    },
    applicationChartData() {
      return {
        labels: this.summary.company_names,
        datasets: [
          {
            label: 'Students Applied',
            data: this.summary.applied_counts,
            backgroundColor: '#42A5F5',
          },
          {
            label: 'Students Selected',
            data: this.summary.selected_counts,
            backgroundColor: '#4CAF50',
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
        scales: {
          x: {
            stacked: false,
          },
          y: {
            beginAtZero: true,
            ticks: {
              precision: 0,
            },
          },
        },
      }
    },
  },

  methods: {
    async fetchSummary() {
      try {
        const response = await axios.get('http://localhost:5000/api/admin/summary', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('admin_token')}`,
          },
        })
        this.summary = response.data
      } catch (error) {
        console.error('Error fetching summary:', error)
      }
    },
  },
  mounted() {
    this.fetchSummary()
  },
}
</script>

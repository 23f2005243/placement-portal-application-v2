<template>
  <div>
    <h2>Company Placement Statistics Summary</h2>
    <div><br /></div>
    <p><strong>Total Drives Conducted:</strong> {{ summary.total_drives }}</p>
    <p><strong>Total Students Applied:</strong> {{ summary.total_applied }}</p>
    <p><strong>Total Students Selected:</strong> {{ summary.total_selected }}</p>
    <div><br /></div>
    <div v-if="summary.drive_names.length">
      <h3>Applications vs Selected (Drive-wise)</h3>
      <div>
      <Bar :data="driveChartData" :options="chartOptions" /></div>
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
  name: 'CompanySummary',
  components: { Bar },
  data() {
    return {
      summary: {
        drive_names: [],
        applied_counts: [],
        selected_counts: [],
        total_drives: 0,
        total_applied: 0,
        total_selected: 0
      }
    }
  },
  computed: {
    driveChartData() {
        return {
            labels: this.summary.drive_names || [],
            datasets: [
                {
                    label: "Applied",
                    data: this.summary.applied_counts || [],
                    backgroundColor: "#42A5F5"
                },
                {
                    label: "Selected",
                    data: this.summary.selected_counts || [],
                    backgroundColor: "#4CAF50"
                }
            ]
        }
    },

    chartOptions() {
        return {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: "top"
                }
            },
            scales: {
                x: {
                    stacked: false
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    }
},

  methods: {
    async fetchSummary() {
      try {
        const response = await axios.get('http://localhost:5000/api/company/summary', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        })
        this.summary = response.data
      } catch (error) {
        console.error('Error fetching summary:', error)
      }
    }
  },
  mounted() {
    this.fetchSummary()
  },
}
</script>

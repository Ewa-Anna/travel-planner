<template>
  <div class="popular-accommodations">
    <p class="title">Most popular accommodations</p>
    <canvas ref="pieChart" class="chart"></canvas>
  </div>
</template>

<script>
import apiClient from "../../utils/apiClient";
import Chart from "chart.js/auto";
import "chartjs-adapter-moment";

export default {
  data() {
    return {
      accommodations: [],
      chart: null,
    };
  },
  mounted() {
    this.fetchPopularAccommodations();
  },
  methods: {
    fetchPopularAccommodations() {
      apiClient
        .get("http://127.0.0.1:8000/analytics/popular-accommodations/")
        .then((response) => {
          this.accommodations = response.data;
        })
        .catch((error) => {
          console.error("Error fetching popular accommodations:", error);
        });
    },
    createPieChart() {
      const ctx = this.$refs.pieChart.getContext("2d");
      this.chart = new Chart(ctx, {
        type: "pie",
        data: {
          labels: this.accommodations.map(
            (accommodation) => accommodation.name,
          ),
          datasets: [
            {
              label: "Trip Count",
              data: this.accommodations.map(
                (accommodation) => accommodation.num_trips,
              ),
              backgroundColor: [
                "rgba(255, 99, 132, 0.6)",
                "rgba(54, 162, 235, 0.6)",
                "rgba(255, 206, 86, 0.6)",
                "rgba(75, 192, 192, 0.6)",
                "rgba(153, 102, 255, 0.6)",
                "rgba(255, 159, 64, 0.6)",
              ],
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
        },
      });
    },
  },
  watch: {
    accommodations: {
      handler() {
        if (this.chart) {
          this.chart.destroy();
        }
        this.createPieChart();
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
.popular-accommodations {
  padding: 20px;
}

.title {
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
}

.chart {
  width: 100%;
  max-width: 400px;
  margin: auto;
}
</style>

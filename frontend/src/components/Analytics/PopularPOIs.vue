<template>
  <div class="popular-pois">
    <p class="title">Most popular Point of Interests</p>
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
      pois: [],
      chart: null,
    };
  },
  mounted() {
    this.fetchPopularPOIs();
  },
  methods: {
    fetchPopularPOIs() {
      apiClient
        .get("http://127.0.0.1:8000/analytics/popular-pois/")
        .then((response) => {
          this.pois = response.data;
        })
        .catch((error) => {
          console.error("Error fetching popular pois:", error);
        });
    },
    createPieChart() {
      const ctx = this.$refs.pieChart.getContext("2d");
      this.chart = new Chart(ctx, {
        type: "pie",
        data: {
          labels: this.pois.map((poi) => poi.name),
          datasets: [
            {
              label: "Trip Count",
              data: this.pois.map((poi) => poi.num_trips),
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
    pois: {
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
.popular-pois {
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

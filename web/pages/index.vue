<template>
  <div class="container">
    <!-- <line-chart
      :chart-data="chartData"
      :options="chartOptions"
      v-if="estimation"
    /> -->
    <line-chart
      :chart-data="chartData"
      v-if="estimation"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      estimation: [],
      // chartDataValues: [],
      chartColors: [
        // rgb(255,255,0),
        // rgb(0,255,255),
        // rgb(255,0,255),
        // rgb(255,0,0),
      ],
      // chartLabels: ["red", "blue", "yellow", "green"],
      chartOptions: {
        // maintainAspectRatio: false,
        // animation: {
        //   duration: 1500,
        //   easing: "easeInOutCubic"
        // }
      }
    };
  },
  async asyncData({ params }) {
    const est_data = await import(`~/static/output.json`);
    console.log(est_data);
    return {
      estimation: {
        infection: est_data.estimation.infection,
        recovered: est_data.estimation.recovered,
        deaths: est_data.estimation.deaths
      }
    };
  },
  computed: {
    chartData() {
      return {
        datasets: [
          {
            data: this.estimation.infection,
            // backgroundColor: this.chartColors
          },
          {
            data: this.estimation.recovered,
            // backgroundColor: this.chartColors
          },
          {
            data: this.estimation.deaths,
            // backgroundColor: this.chartColors
          },
        ],
        // labels: this.chartLabels,
      };
    }
  }
};
</script>

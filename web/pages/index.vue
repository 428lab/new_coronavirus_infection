<template>
  <div class="container">
    <!-- <line-chart
      :chart-data="chartData"
      :options="chartOptions"
      v-if="estimation"
    />-->
    <line-chart v-if="estimation" :chartdata="chartData" :options="chartOptions" />
  </div>
</template>

<script>
require("date-utils");
export default {
  data() {
    return {
      estimation: [],
      labels: [],
      // chartDataValues: [],
      chartColors: [
        // rgb(255,255,0),
        // rgb(0,255,255),
        // rgb(255,0,255),
        // rgb(255,0,0),
      ],
      // chartLabels: ["red", "blue", "yellow", "green"],
      chartOptions: {}
    };
  },
  async asyncData({ params }) {
    const est_data = await import(`~/static/output.json`);
    const labelsData = Object.keys(est_data.fact.infected).map(key => {
      return key;
    });
    const firstDateString = labelsData.shift();
    const firstDate = new Date(firstDateString);
    const labels = est_data.estimation.infection.map((e, i) =>
      firstDate.add(i).toFormat("YYYY/MM/DD")
    );

    return {
      labels: labels,
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
        labels: this.labels,
        datasets: [
          {
            label: "infection",
            borderColor: "red",
            fill: false,
            data: this.estimation.infection
            // backgroundColor: this.chartColors
          },
          {
            label: "recovered",
            borderColor: "blue",
            fill: false,
            data: this.estimation.recovered
            // backgroundColor: this.chartColors
          },
          {
            label: "deaths",
            borderColor: "black",
            fill: false,
            data: this.estimation.deaths
            // backgroundColor: this.chartColors
          }
        ]
      };
    }
  }
};
</script>

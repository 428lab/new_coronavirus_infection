<template>
  <div class="container">
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
      chartColors: [],
      chartOptions: {
        scales: {
          yAxes: [
            {
              id: "y-axis-stac",
              stacked: true,
              display: false,
              ticks: {
                max: 1000
              }
            },
            {
              id: "y-axis-no-stac",
              stacked: false,
              display: true,
              ticks: {
                max: 1000
              }
            }
          ]
        }
      }
    };
  },
  async asyncData({ params }) {
    const est_data = await import(`~/static/output.json`);
    const labelsData = Object.keys(est_data.fact.infected).map(key => {
      return key;
    });
    const firstDateString = labelsData.shift();
    const firstDate = new Date(firstDateString);
    const labels = est_data.estimation.infection.map((e, i) => {
      return new Date(firstDateString).add({ days: i }).toFormat("YYYY/MM/DD");
    });

    let fact = {};
    Object.keys(est_data.fact).map(key => {
      fact[key] = Object.keys(est_data.fact[key]).map(date => {
        return est_data.fact[key][date];
      });
    });

    return {
      labels: labels,
      estimation: est_data.estimation,
      fact: fact
    };
  },
  computed: {
    chartData() {
      // console.log(this.fact);
      return {
        labels: this.labels,
        datasets: [
          {
            label: "estimation infection",
            borderColor: "red",
            fill: false,
            data: this.estimation.infection,
            yAxisID: "y-axis-no-stac"
          },
          {
            label: "estimation recovered",
            borderColor: "blue",
            fill: false,
            data: this.estimation.recovered,
            yAxisID: "y-axis-no-stac"
          },
          {
            label: "estimation deaths",
            borderColor: "black",
            fill: false,
            data: this.estimation.deaths,
            yAxisID: "y-axis-no-stac"
          },
          {
            type: "bar",
            label: "infection",
            borderColor: "red",
            backgroundColor: "red",
            // fill: false,
            data: this.fact.infected,
            yAxisID: "y-axis-stac"
          },
          {
            type: "bar",
            label: "recovered",
            borderColor: "blue",
            backgroundColor: "blue",
            fill: false,
            data: this.fact.recovered,
            yAxisID: "y-axis-stac"
          },
          {
            type: "bar",
            label: "deaths",
            borderColor: "black",
            backgroundColor: "black",
            fill: false,
            data: this.fact.deaths,
            yAxisID: "y-axis-stac"
          }
        ]
      };
    }
  }
};
</script>

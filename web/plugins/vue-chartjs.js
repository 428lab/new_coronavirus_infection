import Vue from 'vue';
import { Line, Doughnut, Bar, mixins } from 'vue-chartjs';
const { reactiveProp } = mixins;

Vue.component('doughnut-chart', {
  extends: Doughnut,
  mixins: [reactiveProp],
  props: {
    options: {
      type: Object,
      default: () => { },
    },
  },
  mounted() {
    this.renderChart(this.chartData, this.options);
  },
});

Vue.component('line-chart', {
  extends: Line,
  // mixins: [reactiveProp],
  props: {
    chartdata: {
      type: Object,
      default: () => null
    },
    options: {
      type: Object,
      default: () => null,
    },
  },
  mounted() {
    this.renderChart(this.chartdata, this.options);
  },
});

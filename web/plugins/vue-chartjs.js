import Vue from 'vue';
import { Line, mixins } from 'vue-chartjs';

Vue.component('line-chart', {
  extends: Line,
  mixins: [mixins.reactiveProp],
  props: {
    chartData: {
      type: Object,
      default: () => null
    },
    options: {
      type: Object,
      default: () => null,
    },
  },
  mounted() {
    this.renderChart(this.chartData, this.options);
  },
});

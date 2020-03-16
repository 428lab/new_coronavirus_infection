<template>
  <div class="mt-4">
    <b-modal v-model="modalShow" hide-header hide-footer>
      <h2 class="h3">免責事項</h2>
      <hr />
      <p class="mt-3">
        この予測は、感染者数、回復者数、死者数のデータをもとにしたものとなります。
      </p>
      <p>
        SEIRモデルと呼ばれる数理モデルにその数値を当てはめているため、環境側面等は一切考慮されていません。
      </p>
      <p>
        あくまで実績数値をもとに数式とプログラムによる予測ということをご理解いただいた上でのグラフ閲覧をお願いしております。
      </p>
      <div class="text-center">
        <button class="btn btn-lg btn-danger my-3" @click="modalShow = false">
          私は上記の内容に了承します
        </button>
      </div>
    </b-modal>
    <div class="container">
      <div class="d-flex align-items-center justify-content-between">
        <h1 class="h3">COVID-19 感染者数予測</h1>
        <!-- <div>
          <span class="p-2">
            SNSでシェア
          </span>
          <a
            href="https://www.facebook.com/share.php?u=https://estimate_covid-19.428lab.net"
            class="text-center"
          >
            <span class=" p-2 bg-facebook">
              <img src="/blandlogo/facebook.svg" height="28px" />
            </span>
          </a>
          <a
            href="https://twitter.com/share?text=新型コロナウイルスの感染者数を数理モデルで予測する - 四谷ラボ&url=https://estimate_covid-19.428lab.net&hashtags=新型コロナウイルス,COVID-19"
            class="text-center"
          >
            <span class=" p-2 bg-twitter">
              <img src="/blandlogo/twitter.svg" height="28px" />
            </span>
          </a>
        </div> -->
      </div>
      <div class="form-row align-items-center justify-content-end">
        <div class="col-auto">
          <label for="staticEmail" class="col-form-label">Country : </label>
        </div>
        <div class="col-auto">
          <select
            class="form-control"
            v-model="selectCountry"
            @change="setData(selectCountry)"
          >
            <option v-for="item in countries" :key="item.id">{{ item }}</option>
          </select>
        </div>
      </div>
      <!-- <button @click="setData()"></button> -->
      <line-chart
        v-if="estimation"
        :chartdata="chartData"
        :options="chartOptions"
        class="mt-3"
      />
    </div>
    <footer class="mt-5">
      <div class="container">
        <div>
          制作・運営:
          <a href="https://twitter.com/SHINOHARATTT" target="_blank"
            >T.Shinohara</a
          >,
          <a href="https://twitter.com/uesitananame55" target="_blank"
            >Zinntikumugai</a
          ><br />
          開発リポジトリ:
          <a
            href="https://github.com/428lab/new_coronavirus_infection"
            target="_blank"
            >GitHub</a
          ><br />
          もとのブログ記事:
          <a
            href="https://blog.428lab.net/entry/2020/03/02/080000"
            target="_blank"
            >四谷ラボ公式ブログ</a
          >
        </div>
        <div class="text-center mt-2">
          &copy; 2020 -
          <a href="https://428lab.net" target="_blank">四谷ラボ</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
require("date-utils");
export default {
  data() {
    return {
      modalShow: true,
      selectCountry: "Japan",
      countries: [],
      est_data: {},
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
              ticks: {
                max: 1000
              }
            }
          ],
          xAxes: [
            {
              id: "x-axis-stac",
              stacked: true,
              display: false
            },
            {
              id: "x-axis-no-stac",
              stacked: false
            }
          ]
        }
      }
    };
  },
  async asyncData({ params }) {
    const est_data = (await import(`~/assets/output.json`)).default;
    let countries = Object.keys(est_data).map(key => {
      return key;
    });
    const labelsData = Object.keys(est_data["Japan"].fact.infected).map(key => {
      return key;
    });
    const firstDateString = labelsData.shift();
    const firstDate = new Date(firstDateString);
    const labels = est_data["Japan"].estimation.infection.map((e, i) => {
      return new Date(firstDateString).add({ days: i }).toFormat("YYYY/MM/DD");
    });

    let fact = {};
    Object.keys(est_data["Japan"].fact).map(key => {
      fact[key] = Object.keys(est_data["Japan"].fact[key]).map(date => {
        return est_data["Japan"].fact[key][date];
      });
    });
    return {
      labels: labels,
      estimation: est_data["Japan"].estimation,
      fact: fact,
      countries: countries,
      est_data: est_data
    };
  },
  methods: {
    setData(country) {
      // console.log(country);
      const labelsData = Object.keys(this.est_data[country].fact.infected).map(
        key => {
          return key;
        }
      );
      const firstDateString = labelsData.shift();
      const firstDate = new Date(firstDateString);
      const labels = this.est_data[country].estimation.infection.map((e, i) => {
        return new Date(firstDateString)
          .add({ days: i })
          .toFormat("YYYY/MM/DD");
      });

      let fact = {};
      Object.keys(this.est_data[country].fact).map(key => {
        fact[key] = Object.keys(this.est_data[country].fact[key]).map(date => {
          return this.est_data[country].fact[key][date];
        });
      });
      console.log(fact);
      this.labels = labels;
      this.estimation = this.est_data[country].estimation;
      this.fact = fact;
    }
  },
  computed: {
    chartData() {
      return {
        labels: this.labels,
        datasets: [
          {
            label: "感染者数（推定）",
            borderColor: "#F44",
            fill: false,
            pointRadius: 0,
            pointHoverRadius: 10,
            data: this.estimation.infection,
            xAxisID: "x-axis-no-stac",
            yAxisID: "y-axis-no-stac"
          },
          {
            label: "回復者数（推定）",
            borderColor: "#4A4",
            fill: false,
            pointRadius: 0,
            pointHoverRadius: 10,
            data: this.estimation.recovered,
            xAxisID: "x-axis-no-stac",
            yAxisID: "y-axis-no-stac"
          },
          {
            label: "死者数（推定）",
            borderColor: "#222",
            fill: false,
            pointRadius: 0,
            pointHoverRadius: 10,
            data: this.estimation.deaths,
            xAxisID: "x-axis-no-stac",
            yAxisID: "y-axis-no-stac"
          },
          {
            type: "bar",
            label: "感染者数",
            borderColor: "#E88",
            backgroundColor: "#E88",
            data: this.fact.infected,
            xAxisID: "x-axis-stac",
            yAxisID: "y-axis-stac"
          },
          {
            type: "bar",
            label: "回復者数",
            borderColor: "#8C8",
            backgroundColor: "#8C8",
            borderWidth: 3,
            data: this.fact.recovered,
            xAxisID: "x-axis-stac",
            yAxisID: "y-axis-stac"
          },
          {
            type: "bar",
            label: "死者数",
            borderColor: "#555",
            backgroundColor: "#555",
            borderWidth: 3,
            data: this.fact.deaths,
            xAxisID: "x-axis-stac",
            yAxisID: "y-axis-stac"
          }
        ]
      };
    }
  }
};
</script>

<style>
.bg-twitter {
  background-color: #1da1f2;
}
.bg-facebook {
  background-color: #1778f2;
}
</style>

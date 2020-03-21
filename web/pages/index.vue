<template>
  <div class="bg-light">
    <b-modal v-model="modalShow" hide-header hide-footer>
      <h2 class="h3 text-danger text-center"><strong>免責事項</strong></h2>
      <hr />
      <p class="mt-3">
        このグラフは、四谷ラボ公式ブログの
        <a
          href="https://blog.428lab.net/entry/2020/03/02/080000"
          target="_blank"
          >新型コロナウイルス感染者数を数理モデルで推定
        </a>
        という記事のスクリプトを使用しています。<br />
        現時点での各国の発症者数・回復者数・死者数をもとにSEIRモデルを用いて今後の広がり方を予測したものとなります。
        <br />SEIRモデルでは気温や湿度、また人の動きなどのパラメータはないため、環境側面等は一切考慮されません。
        <br />あくまで現段階での実績数値をもとに、プログラムによる予測ということをご理解いただいた上でのグラフ閲覧をお願いしております。
      </p>
        <hr>
      <p>
        グラフの更新は1時間に1回、自動更新されます。もとのデータが更新されていない場合は変化しません。
      </p>
      <p>
        <strong>
          このグラフによる将来予測については一切の保証はありません。予測が外れたとしても、我々は一切それについて責務を追うことはありません。
        </strong>
        <br />
      </p>
      <div class="text-center">
        <button
          class="btn btn-lg btn-outline-danger my-3"
          @click="modalShow = false"
        >
          了承します
        </button>
      </div>
    </b-modal>
    <div class="container bg-white pt-4 pb-4">
      <div class="d-md-flex align-items-center justify-content-between">
        <h1 class="h3">COVID-19の感染予測</h1>
      </div>
      <div class="d-sm-flex">
        <div class="d-flex flex-fill mt-2">
          <div class="">
            <label for="staticEmail" class="col-form-label">Country :</label>
          </div>
          <div class="flex-fill ml-2">
            <select
              class="form-control"
              v-model="selectCountry"
              @change="setData(selectCountry)"
            >
              <option v-for="item in countries" :key="item.id">{{
                item
              }}</option>
            </select>
          </div>
        </div>
        <div class="ml-3 mt-2 text-right">
          <a
            href="https://twitter.com/share?text=新型コロナウイルスの発症者数を数理モデルで予測する - 四谷ラボ&url=https://covid19.428lab.net&hashtags=新型コロナウイルス,COVID_19,新型コロナウイルス対策サイト"
            target="_blank"
            class="btn bg-twitter text-white"
          >
            <img src="/blandlogo/twitter.svg" height="14px" /> ツイート
          </a>
          <a
            href="https://www.facebook.com/share.php?u=https://covid19.428lab.net"
            target="_blank"
            class="btn bg-facebook text-white"
          >
            <img src="/blandlogo/facebook.svg" height="14px" /> シェア
          </a>
        </div>
      </div>
      <div class="alert alert-info mt-3">
        <strong
          ><a href="javascript:void(0);" @click="modalShow = true">免責事項</a
          >は、必ずお読みください。</strong
        >
      </div>
      <div style="height:60vh;" class="mt-3">
        <line-chart
          v-if="chart"
          :chart-data="chart"
          :options="options"
          style="height:60vh;"
        />
      </div>
      <div class="mt-3">
        <strong>前回データ取得日時</strong>
        {{ lastUpdate }}
      </div>
      <div class="mt-2">
        <strong>発症者数ピーク(予測) </strong>
        {{ peak.date }} 時点で
        {{ peak.max.toFixed().replace(/(\d)(?=(\d{3})+$)/g, "$1,") }}人
      </div>
    </div>
    <footer class="">
      <div class="pt-3 pb-5 container bg-dark text-white">
        <div>
          もとのブログ記事：
          <a
            href="https://blog.428lab.net/entry/2020/03/02/080000"
            target="_blank"
            >四谷ラボ公式ブログ</a
          >
          <br />データソース：
          <a
            href="https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset"
            target="_blank"
            >Kaggle</a
          >
          <br />開発リポジトリ：
          <a
            href="https://github.com/428lab/new_coronavirus_infection"
            target="_blank"
            >GitHub</a
          >
          <br />制作・運営：
          <a href="https://twitter.com/SHINOHARATTT" target="_blank"
            >T.Shinohara</a
          >,
          <a href="https://twitter.com/uesitananame55" target="_blank"
            >Zinntikumugai</a
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
      chart: null,
      modalShow: true,
      selectCountry: "Japan",
      countries: [],
      est_data: {},
      estimation: {
        infection: [],
        recovered: [],
        deaths: []
      },
      fact: {
        infected: [],
        recovered: [],
        deaths: []
      },
      labels: [],
      peak: {
        day: null,
        max: 0
      },
      lastUpdate: null,
      options: {
        responsive: true,
        maintainAspectRatio: false,
      }
    };
  },
  async asyncData({ params }) {
    const est_data = (await import(`~/assets/output.json`)).default;
    let countries = Object.keys(est_data).map(key => {
      return key;
    });
    return {
      countries: countries,
      est_data: est_data
    };
  },
  mounted() {
    this.setData(this.$data.selectCountry);
  },
  methods: {
    setData(country) {
      const labelsData = Object.keys(this.est_data[country].fact.infected).map(
        key => key
      );
      const firstDateString = labelsData.shift();
      const firstDate = new Date(firstDateString);
      let scaleMax = 0;
      let peak = { day: firstDateString, max: 0 };
      const labels = this.est_data[country].estimation.infection.map((e, i) => {
        const date = new Date(firstDateString)
          .add({ days: i })
          .toFormat("YYYY/MM/DD");
        if (peak.max < e) {
          peak.max = e;
          scaleMax = e;
          peak.date = date;
        }
        return date;
      });

      this.est_data[country].estimation.recovered.map(e => {
        if (scaleMax < e) scaleMax = e;
      });

      this.est_data[country].estimation.deaths.map(e => {
        if (scaleMax < e) scaleMax = e;
      });

      let fact = {};
      Object.keys(this.est_data[country].fact).map(key => {
        fact[key] = Object.keys(this.est_data[country].fact[key]).map(date => {
          return this.est_data[country].fact[key][date];
        });
      });

      console.log(this.est_data[country].fact["infected"]);
      labels.forEach(e => {
        let sum = 0;
        if (this.est_data[country].fact["infected"][e])
          sum += this.est_data[country].fact["infected"][e];
        if (this.est_data[country].fact["recovered"][e])
          sum += this.est_data[country].fact["recovered"][e];
        if (this.est_data[country].fact["deaths"][e])
          sum += this.est_data[country].fact["deaths"][e];

        if (scaleMax < sum) scaleMax = sum;
      });

      scaleMax = Math.round(scaleMax * 1.1);

      this.$data.labels = labels;
      this.estimation = this.est_data[country].estimation;
      this.$data.fact = fact;
      this.$data.peak = peak;
      this.$data.lastUpdate = this.est_data[country]["last_update"];
      this.$data.chart = this.chartData;
    }
  },
  computed: {
    chartData() {
      return {
        labels: this.labels,
        datasets: [
          {
            label: "発症者数（推定）",
            borderColor: "#F44",
            fill: false,
            pointRadius: 0,
            pointHoverRadius: 10,
            data: this.estimation.infection,
            stack: false,
          },
          {
            label: "回復者数（推定）",
            borderColor: "#4A4",
            fill: false,
            pointRadius: 0,
            pointHoverRadius: 10,
            data: this.estimation.recovered,
            stack: false,
          },
          {
            label: "死者数（推定）",
            borderColor: "#222",
            fill: false,
            pointRadius: 0,
            pointHoverRadius: 10,
            data: this.estimation.deaths,
            stack: false,
          },
          {
            type: "bar",
            label: "発症者数",
            borderColor: "#E88",
            backgroundColor: "#E88",
            data: this.fact.infected,
            stack: true,
          },
          {
            type: "bar",
            label: "回復者数",
            borderColor: "#8C8",
            backgroundColor: "#8C8",
            borderWidth: 3,
            data: this.fact.recovered,
            stack: true,
          },
          {
            type: "bar",
            label: "死者数",
            borderColor: "#555",
            backgroundColor: "#555",
            borderWidth: 3,
            data: this.fact.deaths,
            stack: true,
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

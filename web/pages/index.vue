<template>
  <div class="bg-light">
    <b-modal v-model="modalShow" hide-header hide-footer>
      <h2 class="h3 text-danger text-center">
        <strong>{{ $t("messageTitle") }}</strong>
      </h2>
      <hr />
      <p class="mt-3">
        {{ $t("message1") }}<br />
        {{ $t("message2") }} <br />
        {{ $t("message3") }} <br />
        {{ $t("message4") }}
      </p>
      <hr />
      <p>
        {{ $t("message5") }}
      </p>
      <p>
        <strong> {{ $t("message6") }} </strong>
        <br />
      </p>
      <div class="text-center">
        <button
          class="btn btn-lg btn-outline-danger my-3"
          @click="modalShow = false"
        >
          {{ $t("messageButton") }}
        </button>
      </div>
    </b-modal>
    <div class="container bg-white pt-4 pb-4">
      <div class="d-md-flex align-items-center justify-content-between">
        <h1 class="h3">{{ $t("siteTitle") }}</h1>
      </div>
      <div class="d-sm-flex">
        <div class="d-flex flex-fill mt-2">
          <div class="">
            <label for="staticEmail" class="col-form-label">{{
              $t("selectCountry")
            }}</label>
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
            href="javascript:void(0);"
            class="mr-2"
            @click="changeLocale('ja')"
          >
            <img
              src="/country_flag/jp.svg"
              alt=""
              height="24px"
              class="border"
            />
          </a>
          <a
            href="javascript:void(0);"
            class="mr-2"
            @click="changeLocale('en')"
          >
            <img
              src="/country_flag/us.svg"
              alt=""
              height="24px"
              width="36px"
              class="border"
            />
          </a>
          <a
            href="https://twitter.com/share?text=新型コロナウイルスの発症者数を数理モデルで予測する - 四谷ラボ&url=https://covid19.428lab.net&hashtags=新型コロナウイルス,COVID_19,新型コロナウイルス対策サイト"
            target="_blank"
            class="btn bg-twitter text-white"
          >
            <img src="/blandlogo/twitter.svg" height="14px" />
            {{ $t("sns-twitter") }}
          </a>
          <a
            href="https://www.facebook.com/share.php?u=https://covid19.428lab.net"
            target="_blank"
            class="btn bg-facebook text-white"
          >
            <img src="/blandlogo/facebook.svg" height="14px" />
            {{ $t("sns-facebook") }}
          </a>
        </div>
      </div>
      <div class="alert alert-info mt-3">
        <strong>
          <a href="javascript:void(0);" @click="modalShow = true">{{
            $t("disclaimer")
          }}</a></strong
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
        <strong>{{ $t("lastUpdate") }}</strong> : {{ lastUpdate }}
      </div>
      <div class="mt-2">
        <strong>{{ $t("peakOutbreak") }}</strong> :
        {{ peak.max.toFixed().replace(/(\d)(?=(\d{3})+$)/g, "$1,")
        }}{{ $t("peakCount") }} {{ $t("peakNowEn") }}{{ peak.date
        }}{{ $t("peakNowJa") }}
      </div>
    </div>
    <footer class="">
      <div class="pt-3 pb-5 container bg-dark text-white">
        <div>
          {{ $t("originalArticle") }}
          <a
            href="https://blog.428lab.net/entry/2020/03/02/080000"
            target="_blank"
            >{{ $t("yotsuya_lab_blog") }}</a
          >
          <br />{{ $t("originalDataSource") }}
          <a
            href="https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset"
            target="_blank"
            >Kaggle</a
          >
          <br />{{ $t("repository") }}
          <a
            href="https://github.com/428lab/new_coronavirus_infection"
            target="_blank"
            >GitHub</a
          >
          <br />{{ $t("build") }}
          <a href="https://twitter.com/SHINOHARATTT" target="_blank"
            >T.Shinohara</a
          >,
          <a href="https://twitter.com/uesitananame55" target="_blank"
            >Zinntikumugai</a
          >
        </div>
        <div class="text-center mt-2">
          &copy; 2020 -
          <a href="https://428lab.net" target="_blank">{{
            $t("yotsuya_lab")
          }}</a>
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
        maintainAspectRatio: false
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
    changeLocale(locale) {
      this.$i18n.setLocaleCookie(locale);
      this.$router.go(0);
    },
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
            label: this.$t("graphTitleOutbreak2"),
            borderColor: "#F44",
            fill: false,
            pointRadius: 0,
            pointHoverRadius: 10,
            data: this.estimation.infection,
            stack: false
          },
          {
            label: this.$t("graphTitleRecoverd2"),
            borderColor: "#4A4",
            fill: false,
            pointRadius: 0,
            pointHoverRadius: 10,
            data: this.estimation.recovered,
            stack: false
          },
          {
            label: this.$t("graphTitleDeath2"),
            borderColor: "#222",
            fill: false,
            pointRadius: 0,
            pointHoverRadius: 10,
            data: this.estimation.deaths,
            stack: false
          },
          {
            type: "bar",
            label: this.$t("graphTitleOutbreak"),
            borderColor: "#E88",
            backgroundColor: "#E88",
            data: this.fact.infected,
            stack: true
          },
          {
            type: "bar",
            label: this.$t("graphTitleRecoverd"),
            borderColor: "#8C8",
            backgroundColor: "#8C8",
            borderWidth: 3,
            data: this.fact.recovered,
            stack: true
          },
          {
            type: "bar",
            label: this.$t("graphTitleDeath"),
            borderColor: "#555",
            backgroundColor: "#555",
            borderWidth: 3,
            data: this.fact.deaths,
            stack: true
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

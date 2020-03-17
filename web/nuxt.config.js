
export default {
  mode: 'spa',
  /*
  ** Headers of the page
  */
  head: {
    title: '新型コロナウイルス COVID-19の今後の感染予測 - 四谷ラボ',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '新型コロナウイルス COVID-19の感染者数から、SEIRモデルを用いて未来の感染予測を行っています。' },
      { hid: 'http-equiv', 'http-equiv': 'x-dns-prefetch-control', content: 'on' },
      // ogp
      { hid: 'og:site_name', property: 'og:site_name', content: '新型コロナウイルス COVID-19の今後の感染予測 - 四谷ラボ' },
      { hid: 'og:type', property: 'og:type', content: 'website' },
      { hid: 'og:url', property: 'og:url', content: 'https://covid19.428lab.net/' },
      { hid: 'og:title', property: 'og:title', content: '新型コロナウイルス COVID-19の今後の感染予測 - 四谷ラボ' },
      { hid: 'og:description', property: 'og:description', content: '新型コロナウイルス COVID-19の感染者数から、SEIRモデルを用いて未来の感染予測を行っています。' },
      { hid: 'og:image', property: 'og:image', content: 'yotsuyalab_8.webp' },
      // ogp:facebook
      { property: 'article:author', content: 'https://www.facebook.com/%E5%9B%9B%E8%B0%B7%E3%83%A9%E3%83%9C-102455797824507/' },
      // { property: 'fb:app_id', content: 'FacebookAppID' },
      // ogp:twitter
      { name: 'twitter:card', content: 'summary_large_image' },
      { name: 'twitter:site', content: '@lab_428' },
      { name: 'twitter:title', content: '新型コロナウイルス COVID-19の今後の感染予測 - 四谷ラボ' },
      { name: 'twitter:url', content: 'https://covid19.428lab.net/' },
      { name: 'twitter:description', content: '新型コロナウイルス COVID-19の感染者数から、SEIRモデルを用いて未来の感染予測を行っています。' },
      { name: 'twitter:image', content: 'yotsuyalab_8.webp' },

    ],
    link: [
      { rel: 'apple-touch-icon', href: '/apple-touch-icon.png', sizes: '180x180' },
      { rel: 'icon alternate', type: 'image/png', href: '/android-chrome-192x192.png', sizes: '192x192' },
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },
  /*
  ** Global CSS
  */
  css: [
  ],
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    {
      src: '@/plugins/vue-chartjs',
      ssr: false,
    },
  ],
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
    ['@nuxtjs/google-analytics', {
      id: 'UA-159420374-3'
    }]
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    // Doc: https://bootstrap-vue.js.org
    'bootstrap-vue/nuxt',
    // Doc: https://github.com/nuxt-community/dotenv-module
    '@nuxtjs/dotenv',
  ],
  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
    extend (config, ctx) {
    }
  }
}

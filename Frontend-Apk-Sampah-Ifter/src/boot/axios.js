import { boot } from 'quasar/wrappers'
import api from 'src/utils/api'

export default boot(({ app }) => {
  // Buat global property di Vue app
  app.config.globalProperties.$api = api

  // Atau inject ke composition API
  app.provide('api', api)
})

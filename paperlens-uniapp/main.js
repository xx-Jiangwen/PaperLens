import App from './App'

// #ifndef VUE3
import Vue from 'vue'
import './uni.promisify.adaptor'
Vue.config.productionTip = false
App.mpType = 'app'
const app = new Vue({
  ...App
})
app.$mount()
// #endif

// #ifdef VUE3
import { createSSRApp } from 'vue'
import pinia from './stores'
import config from './api/config.js'

export function createApp() {
  const app = createSSRApp(App)
  app.use(pinia)
  // 全局注入配置
  app.provide('config', config)
  app.config.globalProperties.$config = config
  return {
    app
  }
}
// #endif
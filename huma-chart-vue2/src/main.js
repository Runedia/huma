import Vue from 'vue'

Vue.config.productionTip = false

import App from './App.vue'

import './assets/themes/index'

new Vue({
    render: (h) => h(App),
}).$mount('#app')

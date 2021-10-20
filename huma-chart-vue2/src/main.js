import Vue from 'vue'

Vue.config.productionTip = false

import App from './App.vue'

import './assets/themes/index'
import router from './router'

import mdiVue from 'mdi-vue/v2'
import * as mdijs from '@mdi/js'

Vue.use(mdiVue, {
    icons: mdijs,
})

new Vue({
    router,
    render: (h) => h(App),
}).$mount('#app')

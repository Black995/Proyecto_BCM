/*!

 =========================================================
 * Vue Paper Dashboard - v2.0.0
 =========================================================

 * Product Page: http://www.creative-tim.com/product/paper-dashboard
 * Copyright 2019 Creative Tim (http://www.creative-tim.com)
 * Licensed under MIT (https://github.com/creativetimofficial/paper-dashboard/blob/master/LICENSE.md)

 =========================================================

 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

 */
import Vue from "vue";
import App from "./App";
import router from "./router/index";

import PaperDashboard from "./plugins/paperDashboard";
import "vue-notifyjs/themes/default.css";

// Import Bootstrap and BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// Import Prime Vue style libraries
import 'primevue/resources/themes/saga-blue/theme.css'       //theme
import 'primevue/resources/primevue.min.css'                 //core css
import 'primeicons/primeicons.css'                           //icons

/**
 * Carpeta con los estilos globales de la app
 */
import '@/assets/css/main.scss'


Vue.use(PaperDashboard);

/**
 * Bootstrap Vue
 */
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import { BButton } from 'bootstrap-vue'
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)
Vue.use(BootstrapVue)
Vue.component('b-button', BButton)


/**
 * Font Awesome
 */
// Ejemplo para usar iconos de font awesome
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
Vue.component('font-awesome-icon', FontAwesomeIcon);
import { library } from '@fortawesome/fontawesome-svg-core'
import { faPlus, faTrash, faPenToSquare, faClipboardList, faSearch, faComputer, faChartLine, faUsers } from '@fortawesome/free-solid-svg-icons'
library.add(faPlus, faTrash, faPenToSquare, faClipboardList, faSearch, faComputer, faChartLine, faUsers)

/**
 * Prime Vue
 */
import PrimeVue from 'primevue/config';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
// Componentes de Prime Vue
Vue.use(PrimeVue)
Vue.component("DataTable", DataTable)
Vue.component("Column", Column)
Vue.component("ColumnGroup", ColumnGroup)
Vue.component("InputText", InputText)
Vue.component("Button", Button)

/**
 * Apex Chart
 */
import VueApexCharts from 'vue-apexcharts'
Vue.use(VueApexCharts)

Vue.component('apexchart', VueApexCharts)

/* eslint-disable no-new */
new Vue({
  router,
  render: h => h(App)
}).$mount("#app");

import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import PrimeVue from 'primevue/config';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';
//import LoadScript from "vue-plugin-load-script";

// Estilos de bootstrap
import 'bootstrap/dist/css/bootstrap.css'
// Estilos de primevue
import 'primevue/resources/themes/saga-blue/theme.css'       //theme
import 'primevue/resources/primevue.min.css'                 //core css
import 'primeicons/primeicons.css'                           //icons

Vue.config.productionTip = false
Vue.use(PrimeVue);
//Vue.use(LoadScript);
// Componentes de Prime Vue
Vue.component('DataTable', DataTable);
Vue.component('Column', Column);
Vue.component('ColumnGroup', ColumnGroup);
// Librerías complementarias


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

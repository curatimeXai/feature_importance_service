import './assets/app.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import {useDashboardStore} from "@/stores/dashboard.js";
import mitt from 'mitt';
const emitter = mitt();

const app = createApp(App)

app.use(createPinia())
app.config.globalProperties.emitter = emitter;
app.mount('#app')

const dashboardStore=useDashboardStore()
dashboardStore.datasetColumns = columns;

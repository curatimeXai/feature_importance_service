import './assets/css/app.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import {useDashboardStore} from "@/stores/dashboard.js";
import mitt from 'mitt';
import {createMemoryHistory, createRouter, createWebHashHistory} from "vue-router";
import {routes} from "@/routes.js";

const emitter = mitt();

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})
const app = createApp(App)
app.provide('eventBus',emitter);
app.use(router)
app.use(createPinia())
// app.config.globalProperties.emitter = emitter;
app.mount('#app')

const dashboardStore=useDashboardStore()
dashboardStore.datasetColumns = columns;

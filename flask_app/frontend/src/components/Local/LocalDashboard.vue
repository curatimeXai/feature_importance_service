<script setup>
import Chart from "@/components/Chart.vue";
import Http from "@/helpers/Http.js"
import {useDashboardStore} from "@/stores/dashboard.js";
import {inject, onBeforeUnmount, onMounted, ref, watch} from "vue";
import useEmitter from "@/composables/useEmitter.js";
import OverviewBadge from "@/components/OverviewBadge.vue";
import LocalOverview from "@/components/Local/LocalOverview.vue";

const dashboardStore = useDashboardStore();
const emitter = inject('eventBus');

const chartsRef = ref([])
const localOverview = ref(null)
const modules = [
  {
    chartUrl: `/${dashboardStore.model}/breakdown`,
    title: 'Break Down Chart',
    explanations: [
      'The intercept stands for the mean probability of having heart disease across the whole dataset.',
      'The intercept stands for the mean probability of having heart disease across the whole dataset.',
      'The horizontal bars show the contribution of each risk factor.',
      'Positive contribution increases the risk factor and negative contribution decreases it.'
    ]
  }, {
    chartUrl: `/${dashboardStore.model}/shapley`,
    title: 'Shapley Chart',
    explanations: [
      "This chart helps you compare each risk factor and see it's contribution, given the current input.",
      'The intercept stands for the mean probability of having heart disease across the whole dataset.',
      'The horizontal bars show the contribution of each risk factor.',
      'Positive contribution increases the risk factor and negative contribution decreases it.',
      'The main difference to "Risk Factors (Accumulative)" is that here are multiple permutations averaged given the current input'
    ]
  },
     {
    chartUrl: `/${dashboardStore.model}/ceterisparabus/BMI/`,
    title: 'Ceteris Paribus',
    explanations: [
    ]
  },
]

const load = () => {
  chartsRef.value.forEach((chart, index) => {
    chart.load(Http.get(modules[index].chartUrl, dashboardStore.sidebarFormData));
  })
}

const unsubscribe = dashboardStore.$onAction(({name, after}) => {
  if (name === 'setSidebarFormData') {
    after(() => load());
  }
})

onMounted(() => {
  load();
})
onBeforeUnmount(() => {
  unsubscribe();
})

</script>

<template>
  <div id="dashboardView">
    <LocalOverview ref="localOverview"></LocalOverview>
    <template v-for="(module,idx) in modules">
      <div class="flex g-1">
        <Chart ref="chartsRef" class="col-8"></Chart>
        <div class="col-4">
          <h4>{{ module.title }}</h4>
          <ul>
            <li v-for="explanation in module.explanations">{{ explanation }}</li>
          </ul>
          {{ module.explanation }}
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>

</style>
<script setup>
import Chart from "@/components/Chart.vue";
import Http from "@/helpers/Http.js"
import {useDashboardStore} from "@/stores/dashboard.js";
import {inject, onBeforeUnmount, onMounted, ref} from "vue";
import useEmitter from "@/composables/useEmitter.js";

const emitter = inject('eventBus');
const dashboardStore = useDashboardStore();
const chartsRef = ref([])
const datasetBoxPlot = ref(null);
const datasetBarCharts = ref(null);
const datasetPieChart = ref(null);
const modules = [
  {
    url: `/${dashboardStore.model}/vip`,
    title: 'Variable Importance Chart',
    explanations: [
      'This chart displays how the model would be less accurate if a certain variable would be completely random.',
      'This chart underlines the importance of a certain variable to the model.',
      'Drop-out loss refers to the loss function of the mode. The lower the loss function value, the better the model is.',
      'In this case, the higher the drop-out loss the more important is the variable.'
    ]
  },
  {
    url: `/${dashboardStore.model}/pdp/BMI/`,
    title: 'Partial Dependency Chart',
    explanations: [
      'The x-axis represents the possible values of the feature you\'re analyzing.',
      'The y-axis represents the model\'s predicted outcome.',
      'The line shows the average prediction across all data points in the training set, for each value on the x-axis. (Remember, all other features are held constant while this average is calculated).'
    ],
  },

]
emitter.on('switchAggregatedProfiles', (newProfile) => {
  chartsRef.value[1].load(Http.get(`/${dashboardStore.model}/pdp/${newProfile}`));
})
const unsubscribe = dashboardStore.$onAction(({name, after}) => {
  if (name === 'setSidebarFormData') {
    after(() => chartsRef.value[1].load(Http.get(`/${dashboardStore.model}/pdp/${dashboardStore.sidebarFormData}`)));
  }
})
onMounted(() => {
  chartsRef.value.forEach((chart, index) => {
    chart.load(Http.get(modules[index].url));
  })
  datasetPieChart.value.load(Http.get(`/dataset/${dashboardStore.dataset}/piecharts`))
  datasetBarCharts.value.load(Http.get(`/dataset/${dashboardStore.dataset}/barcharts`))
  datasetBoxPlot.value.load(Http.get(`/dataset/${dashboardStore.dataset}/boxplots`))
})

onBeforeUnmount(() => {
  unsubscribe()
})

</script>

<template>
  <div id="dashboardView" class="row">
    <Chart ref="datasetPieChart" class="col-12"></Chart>
    <Chart ref="datasetBarCharts" class="col-12"></Chart>
    <Chart ref="datasetBoxPlot" class="col-8"></Chart>
    <div class="col-4">
      <h4>Boxplot Chart</h4>
      <ul>
        <li>The boxes represent to most frequent 75% values of the dataset</li>
        <li>The other 25% are between the margins</li>
        <li>All other outliers are represented as dots</li>
      </ul>
    </div>
    <template v-for="(module,index) in modules">
      <Chart ref="chartsRef" class="col-8"></Chart>
      <div class="col-4">
        <h4>{{ module.title }}</h4>
        <ul>
          <li v-for="explanation in module.explanations">{{ explanation }}</li>
        </ul>
      </div>
    </template>
  </div>
</template>

<style scoped>

</style>
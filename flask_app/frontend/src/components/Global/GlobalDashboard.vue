<script setup>
import Chart from "@/components/Chart.vue";
import Http from "@/helpers/Http.js"
import {useDashboardStore} from "@/stores/dashboard.js";
import {onMounted, ref} from "vue";
import useEmitter from "@/composables/useEmitter.js";

const emitter = useEmitter();
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
      'DALEX\'s variable importance chart provides a visual and easy-to-interpret way to identify the most critical features for your model\'s performance.'
    ]
  },
  {
    url: `/${dashboardStore.model}/pdp/BMI`,
    title: 'Partial Dependency Chart',
    explanations: [
      'The x-axis represents the values of the feature you\'re analyzing.',
      'The y-axis represents the model\'s predicted outcome (e.g., probability for classification, value for regression).',
      'The line shows the average prediction across all data points in the training set, for each value on the x-axis. (Remember, all other features are held constant while this average is calculated).'
    ],
  },

]
emitter.on('switchAggregatedProfiles', (newProfile) => {
  chartsRef.value[1].load(Http.get(`/${dashboardStore.model}/pdp/${newProfile}`));
})
onMounted(() => {
  chartsRef.value.forEach((chart, index) => {
    chart.load(Http.get(modules[index].url));
  })
  datasetPieChart.value.load(Http.get(`/dataset/${dashboardStore.dataset}/piecharts`))
  datasetBarCharts.value.load(Http.get(`/dataset/${dashboardStore.dataset}/barcharts`))
  datasetBoxPlot.value.load(Http.get(`/dataset/${dashboardStore.dataset}/boxplots`))
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
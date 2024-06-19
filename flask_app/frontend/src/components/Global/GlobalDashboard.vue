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
const datasetPieChart = ref(null);
const modules = [
  {
    url: `/${dashboardStore.model}/vip`,
    explanation: 'DALEX\'s variable importance chart provides a visual and easy-to-interpret way to identify the most critical features for your model\'s performance.'
  },
  {
    url: `/${dashboardStore.model}/pdp/BMI`,
    explanation: 'The x-axis represents the values of the feature you\'re analyzing.\n' +
        'The y-axis represents the model\'s predicted outcome (e.g., probability for classification, value for regression).\n' +
        'The line shows the average prediction across all data points in the training set, for each value on the x-axis. (Remember, all other features are held constant while this average is calculated).'
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
  datasetBoxPlot.value.load(Http.get(`/dataset/${dashboardStore.dataset}/boxplots`))
})

</script>

<template>
  <div id="dashboardView" class="row">
    <Chart ref="datasetPieChart" class="col-12"></Chart>
    <Chart ref="datasetBoxPlot" class="col-8"></Chart>
    <template v-for="(module,index) in modules">
      <Chart ref="chartsRef" class="col-8"></Chart>
      <div class="col-4">{{ module.explanation }}</div>
    </template>
  </div>
</template>

<style scoped>

</style>
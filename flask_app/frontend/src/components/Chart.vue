<script setup>
import Plotly from 'plotly.js-dist'
import {ref, defineProps, onMounted, watch} from 'vue'
import Loader from "@/components/Loader.vue";
import {useDashboardStore} from "@/stores/dashboard.js";

const props = defineProps({
  chartData: {
    type: Object,
    default: {data: [], layout: []},
  }
});

const dashboardStore = useDashboardStore();
const chartData = ref(props.chartData);
const chartId = dashboardStore.getChartId()
const chartBuild = ref(false);
const loading = ref(true)

function startLoading() {
  loading.value = true
}

function stopLoading() {
  loading.value = false
}

function setChartData(data) {
  chartData.value = data
}

function buildChart() {
  if (document.getElementById(chartId)) {
    Plotly.newPlot(chartId, chartData.value.data, chartData.value.layout).then(() => {
      stopLoading();
    })
  }
}

function load(promise) {
  document.getElementById(chartId).innerHTML = ''
  startLoading()
  promise.then(async (response) => {
    chartData.value = await response.json()
  })
}

defineExpose({
  startLoading,
  stopLoading,
  setChartData,
  buildChart,
  load,
})

onMounted(()=>{
  if (chartBuild.value!==true&&chartData.value.data.length>0) {
    buildChart()
  }
})

watch(() => chartData.value, (newValue) => {
  if (newValue.data.length > 0) {
    buildChart()
  }
})

</script>

<template>
  <div>
    <Loader v-if="loading"></Loader>
    <div :id="chartId">
    </div>
  </div>
</template>

<style scoped>

</style>
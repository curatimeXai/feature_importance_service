<script setup>
import Plotly from 'plotly.js-dist'
import {ref, defineProps, onMounted} from 'vue'
import Loader from "@/components/Loader.vue";

const props = defineProps({
  chartId: String,
});

const loading = ref(true)

function load(promise) {
  document.getElementById(props.chartId).innerHTML = ''
  loading.value = true
  promise.then(async (response) => {
    const chartData = await response.json()
    Plotly.newPlot(props.chartId, chartData.data, chartData.layout)
  }).finally(() => {
    loading.value = false;
  })
}

defineExpose({
  load
})

</script>

<template>
  <div>
    <Loader v-if="loading"></Loader>
    <div :id="props.chartId" class="chart-wrapper">
    </div>
  </div>
</template>

<style scoped>

</style>
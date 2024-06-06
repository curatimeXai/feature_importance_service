<script setup>
import Chart from "@/components/Chart.vue";
import Http from "@/helpers/Http.js"
import {useDashboardStore} from "@/stores/dashboard.js";
import {onMounted, ref} from "vue";
import useEmitter from "@/composables/useEmitter.js";

const emitter = useEmitter();

const chartsRef = ref([])
const chartsUrls = [
  '/xdg/vip',
  '/xdg/pdp'
]
// emitter.on('submitSidebar', () => {
//   console.log('on submit')
//   chartsRef.value.forEach((chart, index) => {
//     chart.load(Http.get(chartsUrls[index], dashboardStore.sidebarFormData));
//   })
// })
onMounted(()=>{
  chartsRef.value.forEach((chart, index) => {
    chart.load(Http.get(chartsUrls[index]));
  })
})

</script>

<template>
  <div id="dashboardView" class="row col-10">
      <Chart ref="chartsRef" class="col-8" v-for="(chartUrl,index) in chartsUrls" :chart-id="'chart'+(index+2)"></Chart>
  </div>
</template>

<style scoped>

</style>
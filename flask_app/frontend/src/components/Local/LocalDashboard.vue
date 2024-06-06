<script setup>
import Chart from "@/components/Chart.vue";
import Http from "@/helpers/Http.js"
import {useDashboardStore} from "@/stores/dashboard.js";
import {ref, watch} from "vue";
import useEmitter from "@/composables/useEmitter.js";
import OverviewBadge from "@/components/OverviewBadge.vue";
import LocalOverview from "@/components/Local/LocalOverview.vue";

const dashboardStore = useDashboardStore();
const emitter = useEmitter();

const chartsRef = ref([])
const modules = [
  {
    chartUrl: '/xdg/breakdown',
    explanation: 'The chart shows a vertical line representing the final model prediction.\n' +
        'The X-axis represents the model\'s prediction value.\n' +
        'The Y-axis lists the variables (features) used by the model.\n' +
        'Colored bars on the chart represent the contribution of each variable to the final prediction.\n' +
        'Green bars indicate the reduction of the probability of having heart disease.\n' +
        'Red bars indicate the increase of the probability of having heart disease.\n' +
        'The size of the bar reflects the impact of the variable. '
  }, {
    chartUrl: '/xdg/shapley',
    explanation: 'A DALEX Shapley chart is a bar chart that visualizes this feature contribution. \n' +
        'Each bar represents a feature in the model\'s data.\n' +
        'The size of the bar shows the impact of that feature on the prediction. Positive values mean the feature pushed the prediction in a certain direction, while negative values indicate the opposite.\n' +
        'Green bars indicate good contribution to the heart disease prediction, and red bars represent bad contributions.'
  },
]

emitter.on('submitSidebar', () => {
  console.log('on submit')
  chartsRef.value.forEach((chart, index) => {
    chart.load(Http.get(modules[index].chartUrl, dashboardStore.sidebarFormData));
  })
})

</script>

<template>
  <div id="dashboardView" class="row">
    <LocalOverview></LocalOverview>
    <template v-for="(module,idx) in modules">
      <Chart ref="chartsRef" class="col-8" :chart-id="'chart'+idx"></Chart>
      <div class="col-4">{{module.explanation}}</div>
    </template>
  </div>
</template>

<style scoped>

</style>
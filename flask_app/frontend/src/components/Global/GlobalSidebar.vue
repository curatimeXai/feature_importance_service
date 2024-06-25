<script setup>
import {inject} from "vue";
import {useDashboardStore} from "@/stores/dashboard.js";

const dashboardStore = useDashboardStore();
function onSwitchLineChart(event) {
  dashboardStore.setSidebarFormData(event.target.value)
}
</script>

<template>
  <div>
    <label class="row col-12 space-between" for="${label_for}">
      <span class="flex v-align-center col-6">
       Probability by Value:
      </span>
      <select @change="onSwitchLineChart($event)" class="col-6">
        <option>BMI</option>
        <option value="PhysicalHealth">Physical Health</option>
        <option value="MentalHealth">Mental Health</option>
        <option value="SleepTime">Sleep Time</option>
      </select>
    </label>
  </div>
</template>

<style scoped>

</style>
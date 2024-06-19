<script setup>
import {useDashboardStore} from "@/stores/dashboard.js";

const dashboardStore = useDashboardStore();
</script>

<template>
  <div>
    <label class="row col-4 space-between" for="${label_for}">
      <span class="flex v-align-center col-6">
        Current Model
      </span>
      <select v-model="dashboardStore.model" class="col-6">
        <option selected value="xdg">Xdgboost</option>
        <option value="svm">Support Vector Machine</option>
        <option value="rand_forest">Random Forest</option>
        <option value="dnn">Deep Neural Network</option>
        <option value="lr">Linear</option>
      </select>
    </label>
  </div>
</template>

<style scoped>

</style>
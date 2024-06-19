<script setup>
import {useDashboardStore} from "@/stores/dashboard.js";

const dashboardStore = useDashboardStore();
</script>

<template>
  <button @click="dashboardStore.nestedView='model'" class="col-12 mb-1">Model</button>
  <button @click="dashboardStore.nestedView='dataset'" class="col-12 mb-1">Dataset</button>
  <button @click="dashboardStore.nestedView='frequent-questions'" class="col-12 mb-1">Frequent questions</button>
</template>

<style scoped>

</style>
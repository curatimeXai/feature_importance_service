<script setup>
import {useDashboardStore} from "@/stores/dashboard.js";

const dashboardStore = useDashboardStore();
</script>

<template>
  <div>
    <RouterLink class="router-link-button mb-1" to="/settings/model">
      Model
    </RouterLink>
    <RouterLink class="router-link-button mb-1" to="/settings/dataset">
      Dataset
    </RouterLink>
    <RouterLink class="router-link-button" to="/settings/questions">
      Frequent Questions
    </RouterLink>
  </div>
</template>

<style scoped>

</style>
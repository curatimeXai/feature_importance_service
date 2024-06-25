<script setup>
import {useDashboardStore} from "@/stores/dashboard.js";
import TooltipTrigger from "@/components/TooltipTrigger.vue";

const dashboardStore = useDashboardStore();
</script>

<template>
  <div>
    <RouterLink class="router-link-button mb-1" to="/settings/model">
      Predictive Model
    </RouterLink>
    <div class="flex v-align-center mb-1">
      <RouterLink class="router-link-button col-12" to="/settings/dataset">
        Dataset
      </RouterLink>
      <TooltipTrigger
          :tooltip-text="'Supervised models use datasets to train their prediction function on.' +
         ' The bigger and more detailed the dataset is, the higher is the possibility that the model trains well.'">
      </TooltipTrigger>
    </div>
    <RouterLink class="router-link-button mb-1" to="/settings/questions">
      Frequent Questions
    </RouterLink>
  </div>
</template>

<style scoped>

</style>
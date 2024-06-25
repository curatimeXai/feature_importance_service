<script setup>
import {useDashboardStore} from "@/stores/dashboard.js";

const dashboardStore = useDashboardStore();
</script>

<template>
  <div class="flex g-1">
    <div class="col-6">
      <h4><i class="fa fa-triangle-exclamation" style="color: var(--warning-color);"></i>
        Currently it's only possible to use one dataset.
      </h4>
      <label class="row space-between" style="align-self: flex-start">
      <span class="flex v-align-center col-6">
        Current Dataset
      </span>
        <select v-model="dashboardStore.dataset" class="col-6" disabled>
          <option selected value="kaggle_heart_disease_2020">American Survey 2020, 300k Rows</option>
        </select>
      </label>
    </div>
    <div class="col-6" v-if="dashboardStore.dataset==='kaggle_heart_disease_2020'">
      <h4>American Survey 2020 Columns:</h4>
      <ul>
        <li v-for="(column,key) in dashboardStore.datasetColumns">
          <b>
            {{ column.title ? column.title : key }}
          </b>
          {{ Object.hasOwn(column, 'explanation') ? ': ' + column.explanation : '' }}
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>

</style>
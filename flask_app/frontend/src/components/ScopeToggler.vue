<script setup>
import {ref} from "vue";
import {useDashboardStore} from "@/stores/dashboard.js";

const dashboardStore = useDashboardStore();

const toggleWrapper = ref();

function toggle(event, view) {
  toggleWrapper.value.childNodes.forEach(spanWithoutClasses => {
    spanWithoutClasses.className = '';
  });
  event.target.className = 'active';
  dashboardStore.view = view
}
</script>

<template>
  <div ref="toggleWrapper" class="scope-toggler mb-1">
    <span @click="toggle($event,'local')" class="active">Local</span>
    <span @click="toggle($event,'global')">Global</span>
    <span @click="toggle($event,'settings')">
      <i class="fa fa-cog"></i>
    </span>
  </div>
</template>

<style scoped>

</style>
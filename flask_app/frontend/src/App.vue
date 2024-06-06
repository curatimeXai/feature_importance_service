<script setup>
import LocalDashboard from "@/components/Local/LocalDashboard.vue";
import Sidebar from "@/components/Sidebar.vue";
import GlobalDashboard from "@/components/Global/GlobalDashboard.vue";
import SettingsView from "@/components/Settings/SettingsView.vue";
import {useDashboardStore} from "@/stores/dashboard.js";
const dashboardStore=useDashboardStore()
</script>

<template>
  <main class="flex col-12 mt-1">
    <Sidebar></Sidebar>
    <div class="col-10" style="margin-left: 18%">
      <LocalDashboard v-if="dashboardStore.view==='local'"></LocalDashboard>
      <GlobalDashboard v-if="dashboardStore.view==='global'"></GlobalDashboard>
      <SettingsView v-if="dashboardStore.view==='settings'"></SettingsView>
    </div>


  </main>
</template>

<style scoped>

</style>

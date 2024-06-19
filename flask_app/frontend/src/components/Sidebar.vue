<script setup>
import ScopeToggler from "@/components/ScopeToggler.vue";
import LocalSidebar from "@/components/Local/LocalSidebar.vue";
import GlobalSidebar from "@/components/Global/GlobalSidebar.vue";
import SettingsSidebar from "@/components/Settings/SettingsSidebar.vue";
import {useDashboardStore} from "@/stores/dashboard.js";

const dashboardStore = useDashboardStore();

</script>

<template>
  <div class="col-2 capsule" style="position: fixed; top: 10px;">
    <div>
      <ScopeToggler></ScopeToggler>
      <LocalSidebar v-if="dashboardStore.view==='local'"></LocalSidebar>
      <GlobalSidebar v-if="dashboardStore.view==='global'"></GlobalSidebar>
      <SettingsSidebar v-if="dashboardStore.view==='settings'"></SettingsSidebar>
    </div>
  </div>
</template>

<style scoped>

</style>
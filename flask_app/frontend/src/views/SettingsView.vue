<script setup>

import DatasetSettings from "@/components/Settings/DatasetSettings.vue";
import ModelSettings from "@/components/Settings/ModelSettings.vue";
import FrequentQuestions from "@/components/Settings/FrequentQuestions.vue";
import {useDashboardStore} from "@/stores/dashboard.js";
import LocalSidebar from "@/components/Local/LocalSidebar.vue";
import ScopeToggler from "@/components/ScopeToggler.vue";
import LocalDashboard from "@/components/Local/LocalDashboard.vue";
import SettingsSidebar from "@/components/Settings/SettingsSidebar.vue";

const dashboardStore = useDashboardStore();
dashboardStore.nestedView = 'model'
</script>

<template>
  <div class="col-2 capsule" style="position: fixed; top: 10px;">
    <ScopeToggler></ScopeToggler>
    <SettingsSidebar></SettingsSidebar>
  </div>
  <div class="capsule" style="margin-left: 19%; z-index: -1; position: absolute; width: 78%;">
    <ModelSettings v-if="dashboardStore.nestedView==='model'"></ModelSettings>
    <DatasetSettings v-if="dashboardStore.nestedView==='dataset'"></DatasetSettings>
    <FrequentQuestions v-if="dashboardStore.nestedView==='frequent-questions'"></FrequentQuestions>
  </div>
</template>

<style scoped>

</style>
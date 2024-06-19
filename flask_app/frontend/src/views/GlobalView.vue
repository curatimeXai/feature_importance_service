<script setup>

import ScopeToggler from "@/components/ScopeToggler.vue";
import GlobalSidebar from "@/components/Global/GlobalSidebar.vue";
import GlobalDashboard from "@/components/Global/GlobalDashboard.vue";
</script>

<template>
  <div class="col-2 capsule" style="position: fixed; top: 10px;">
    <ScopeToggler></ScopeToggler>
    <GlobalSidebar></GlobalSidebar>
  </div>
  <div class="capsule" style="margin-left: 19%; z-index: -1; position: absolute; width: 78%;">
    <GlobalDashboard></GlobalDashboard>
  </div>
</template>

<style scoped>

</style>
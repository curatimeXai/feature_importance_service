<script setup>

import LocalDashboard from "@/components/Local/LocalDashboard.vue";
import LocalSidebar from "@/components/Local/LocalSidebar.vue";
import ScopeToggler from "@/components/ScopeToggler.vue";
</script>

<template>
  <div class="col-2 capsule" style="
      position: fixed;
      top: 10px;
      height: 96vh;
      overflow-y: auto;
      overflow-x: hidden;">
    <ScopeToggler></ScopeToggler>
    <LocalSidebar></LocalSidebar>
  </div>
  <div class="capsule" style="margin-left: 19%; z-index: -1; position: absolute; width: 78%;">
    <LocalDashboard></LocalDashboard>
  </div>
</template>

<style scoped>

</style>
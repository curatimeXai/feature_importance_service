<script setup>

import {ref} from "vue";
import ScopeToggler from "@/components/ScopeToggler.vue";

const overlay = ref(null)

function openTutorial() {
  overlay.value.show();
}
</script>

<template>
  <div>
    <RouterLink class="tutorial" @click="openTutorial()" to="/tutorial">
      <i class="fa fa-circle-info" style="
        border-radius: 30px;
        border: 2px solid var(--bright-color);
        background: var(--bright-color);">
      </i>
    </RouterLink>
  </div>
</template>

<style scoped>
.tutorial {
  position: fixed;
  bottom: 5px;
  right: 2%;
  color: var(--primary-color);
  font-size: 60px;
}
</style>
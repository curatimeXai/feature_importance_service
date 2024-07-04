<script setup>
import {ref} from "vue";

const collapsed=ref(true)
</script>

<template>
  <div class="collapsible">
    <div @click="collapsed=!collapsed" style="cursor: pointer;">
      <slot name="title"></slot>
      <i v-if="collapsed" class="fa fa-chevron-right" style="color: var(--primary-color)"></i>
      <i v-else class="fa fa-chevron-up" style="color: var(--primary-color)"></i>
    </div>
    <div v-if="!collapsed" style="border-top: 1px solid var(--primary-color); padding-top: 10px">
      <slot name="collapsible"></slot>
    </div>
  </div>
</template>

<style scoped>
.collapsible{
  padding: 10px;
  border: 1px solid var(--primary-color);
  border-radius: var(--border-radius);
}

</style>
<script setup>

import {ref, defineExpose} from "vue";

const overlay = ref(null)

function show() {
  overlay.value.style.display = 'block'
}

function hide() {
  overlay.value.style.display = 'none'
}

defineExpose({show, hide})
</script>

<template>
  <div ref="overlay" style="position: fixed;
    display: none;
    width: 100%;
    height: 100%;
    background: white;
    top: 0;
    left: 0;">
    <a @click="hide()" style="position: absolute;
      color: var(--primary-color);
      left: 2%;
      top: 5px;
      font-size: 30px;">
      <i class="fa fa-arrow-left"></i>
    </a>
    <div class="container mt-05">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>

</style>
<script setup>
import {defineProps, ref} from 'vue';

const props = defineProps({
  name: {
    type: String,
    default: '',
    required: false
  }
})

const select = ref(null)

function onClick(event) {
  console.log('test')
  const clickEvent = new MouseEvent('mousedown', {
    'view': window,
    'bubbles': true,
    'cancelable': true
  });
  select.value.dispatchEvent(clickEvent)
}
</script>

<template>
  <div style="position: relative">
    <select ref="select" class="col-12" :name="name">
      <slot></slot>
    </select>
    <span style="position: absolute; top: 26%; right: 10px; pointer-events: none;color: var(--primary-color)">
      <i class="fa fa-chevron-down" style="pointer-events: none;"></i></span>
  </div>
</template>

<style scoped>

</style>
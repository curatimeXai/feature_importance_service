<script setup>
import {ref} from 'vue';

const loader = ref(null)

function show() {
  loader.value.style.display = 'block';
}

function hide() {
  loader.value.style.display = 'none';

}
</script>

<template>
  <div ref="loader" class="loader-background mb-1" style="display: block; height: 400px;">
    <div class="loader">
      <svg height="200" width="200">
        <circle id="circle" cx="100" cy="100" r="50" stroke="#C1002A" stroke-width="5" fill="transparent"></circle>
      </svg>
    </div>
  </div>
</template>

<style scoped>

</style>
<script setup>
import {defineProps, ref, defineModel} from "vue";

const props = defineProps({
  min: Number,
  max: Number,
  name: String
})
const rangeValue = ref(Math.floor(props.max / 2)+Math.floor(props.min))
const inputValue = ref(Math.floor(props.max / 2)+Math.floor(props.min))

</script>

<template>
  <div class="row col-3">
    <input v-model="inputValue" @input="rangeValue=parseInt(Math.floor(inputValue));" class="mb-05 col-12" type="number" :name="name" :min="parseInt(min)"
           :max="parseInt(max)">
    <input v-model="rangeValue" @input="inputValue=parseInt(Math.floor(rangeValue))" class="col-12" type="range" step="1" :min="parseInt(min)"
           :max="parseInt(max)">
  </div>
</template>

<style scoped>

</style>
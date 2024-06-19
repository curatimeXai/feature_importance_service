<script setup>
import useEmitter from "@/composables/useEmitter.js";

const emitter = useEmitter();

function onSwitchLineChart(event) {
  console.log('emit')
  emitter.emit('switchAggregatedProfiles', event.target.value)
}
</script>

<template>
  <div>
    <label class="row col-12 space-between" for="${label_for}">
      <span class="flex v-align-center col-6">
       Aggregated Profiles
      </span>
      <select @change="onSwitchLineChart($event)" class="col-6">
        <option>BMI</option>
        <option value="PhysicalHealth">Physical Health</option>
        <option value="MentalHealth">Mental Health</option>
        <option value="SleepTime">Sleep Time</option>
      </select>
    </label>
  </div>
</template>

<style scoped>

</style>
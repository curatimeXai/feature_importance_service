<script setup>

import Collapsible from "@/components/Collapsible.vue";
</script>

<template>
  <div>
    <div class="mb-1">
      Frequent Questions
    </div>
    <div class="row space-between">
      <Collapsible class="col-6">
        <template v-slot:title>
          What does Bogalusa stand for?
        </template>
        <template v-slot:collapsible>
          Bogalusa is a village in the USA, where a famous heart disease study took place from 1973 until today.
        </template>
      </Collapsible>
      <Collapsible class="col-6">
        <template v-slot:title>
          What is this dashboard for?
        </template>
        <template v-slot:collapsible>
          This dashboard is ment for workers in the medical field (especially cardiologists) to get acquainted with
          AI-tools and help build trust in AI-models .
        </template>
      </Collapsible>
       <Collapsible class="col-6">
        <template v-slot:title>
          Why is this dashboad only for heart disease prediction?
        </template>
        <template v-slot:collapsible>
          One of  the main death causes are related to heart problems and this dashboard is ment to help doctors
          diagnose patients better and see heart disease risks better.
        </template>
      </Collapsible>
    </div>
  </div>
</template>

<style scoped>

</style>
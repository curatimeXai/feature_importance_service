<script setup>

</script>

<template>
  <div>
    <h4><i class="fa fa-triangle-exclamation" style="color: var(--warning-color);"></i>
      Currently it's only possible to use one dataset.
    </h4>
    <label class="row col-6 space-between" for="${label_for}">
      <span class="flex v-align-center col-6">
        Current Dataset
      </span>
      <select class="col-6" disabled>
        <option selected value="heart_2020">American Survey 2020, 300k Rows</option>
      </select>
    </label>
  </div>
</template>

<style scoped>

</style>
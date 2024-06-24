<script setup>
import {ref} from "vue";
import {useDashboardStore} from "@/stores/dashboard.js";

const props=defineProps({
  disabled:{
    type: Boolean,
    default: false,
  }
})

const dashboardStore = useDashboardStore();

const toggleWrapper = ref();

function toggle(event, view) {
  toggleWrapper.value.childNodes.forEach(spanWithoutClasses => {
    spanWithoutClasses.classList.remove('active');
  });
  event.currentTarget.classList.add('active');
  dashboardStore.view = view
}
</script>

<template>
  <div ref="toggleWrapper" class="scope-toggler mb-1" :class="props.disabled?'disabled':''">
    <RouterLink to="/"
                title="In local scope you can input different risk factors and see their influence of the probability of having heart disease">
      Local
    </RouterLink>
    <RouterLink to="/global" title="In global scope you can see the analysis of the model on the whole dataset">Global
    </RouterLink>
    <RouterLink to="/settings/model">
      <i class="fa fa-cog"></i>
    </RouterLink>
  </div>
</template>

<style scoped>

</style>
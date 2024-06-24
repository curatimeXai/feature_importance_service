<script setup>
import TutorialBubble from "@/components/TutorialBubble.vue";
import {useRoute} from "vue-router";
import Tooltip from "@/components/Tooltip.vue";

const route = useRoute();
</script>

<template>
  <main class="flex col-12 mt-1">
    <RouterView></RouterView>
    <TutorialBubble v-if="route.path!=='/tutorial'"></TutorialBubble>
  </main>
  <tooltip></tooltip>
</template>

<style scoped>

</style>

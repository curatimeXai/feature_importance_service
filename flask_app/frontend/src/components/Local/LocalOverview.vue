<script setup>
import OverviewBadge from "@/components/OverviewBadge.vue";
import {onBeforeMount, ref} from "vue";
import useEmitter from "@/composables/useEmitter.js";
import Http from "@/helpers/Http.js";
import {useDashboardStore} from "@/stores/dashboard.js";
import Loader from "@/components/Loader.vue";

const dashboardStore = useDashboardStore();
const emitter = useEmitter();

const overviewData = ref(null)

emitter.on('submitSidebar', () => {
  overviewData.value=null
  Http.get(`/${dashboardStore.model}/overview`, dashboardStore.sidebarFormData).then(async response => {
    overviewData.value = await response.json();
  })
})


</script>

<template>
  <div class="col-12 row" style="gap: 10px;">
    <Loader v-if="overviewData===null"></Loader>
    <template v-else>
      <div class="row space-between" style="gap: 10px;">
        <OverviewBadge :title-prop="'Prediction'"
                       :subtitle-prop="(overviewData['prediction']).toLocaleString('en-EN', {minimumFractionDigits: 0, maximumFractionDigits: 2})"
                       :suffix="'%'" :parser-function-name="null"
                       :icon-prop="overviewData['prediction']<30?'fa fa-thumbs-up':'fa fa-thumbs-down'"
                       :color-prop="overviewData['prediction']<30?'var(--positive-color)':'var(--negative-color)'">
        </OverviewBadge>
        <OverviewBadge v-for="badgeData in overviewData['features']"
                       :title-prop="badgeData[0]"
                       :subtitle-prop="badgeData[1]"
                       :suffix="'%'"
                       :parser-function-name="'parseInverseNumeric'"
                       style="flex-grow: 1;">
        </OverviewBadge>
      </div>
    </template>
  </div>
</template>

<style scoped>

</style>
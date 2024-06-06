<script setup>
import OverviewBadge from "@/components/OverviewBadge.vue";
import {onBeforeMount, ref} from "vue";
import useEmitter from "@/composables/useEmitter.js";
import Http from "@/helpers/Http.js";
import {useDashboardStore} from "@/stores/dashboard.js";
import Loader from "@/components/Loader.vue";

const dashboardStore = useDashboardStore();
const emitter = useEmitter();

const badgesRef = ref([])
const overviewData = ref(null)

emitter.on('submitSidebar', () => {
  Http.get('/xdg/overview', dashboardStore.sidebarFormData).then(async response => {
    overviewData.value = await response.json();
  })
})


</script>

<template>
  <div class="col-8" style="gap: 10px;">
    <Loader v-if="overviewData===null"></Loader>
    <template v-else>
      <div class="flex justify-center mb-1">
        <OverviewBadge :title-prop="'Prediction'"
                       :subtitle-prop="overviewData['prediction']"
                       :parser-function-name="'parseNumeric'">
        </OverviewBadge>
      </div>
      <div class="row space-between" style="gap: 10px;">
        <OverviewBadge v-for="badgeData in overviewData['features']"
                       :title-prop="badgeData[0]"
                       :subtitle-prop="badgeData[1]"
                       style="flex-grow: 1;"
                       :parser-function-name="'parseInverseNumeric'">
        </OverviewBadge>
      </div>
    </template>
  </div>
</template>

<style scoped>

</style>
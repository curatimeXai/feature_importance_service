import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useDashboardStore = defineStore('dashboard', () => {
  const view = ref('local')
  const datasetColumns = ref(null)
  const sidebarFormData=ref(null)

  function switchView(newView) {
    view.value = newView;
  }

  return {view, sidebarFormData, datasetColumns, switchView}
})

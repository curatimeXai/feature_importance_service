<script setup>
import {ref, onMounted, watch, inject} from "vue";
import {storeToRefs} from 'pinia'
import {useDashboardStore} from "@/stores/dashboard.js";
import SliderInput from "@/components/Inputs/SliderInput.vue";
import useEmitter from "@/composables/useEmitter.js";
import TooltipTrigger from "@/components/TooltipTrigger.vue";
import Select from "@/components/Inputs/Select.vue";

const dashboardStore = useDashboardStore();
const inputs = ref([
  {
    key: 'weight',
    title: 'Weight',
  }, {
    key: 'height',
    title: 'Height',
  }, {
    key: 'PhysicalHealth',
    title: 'Good Physical Health (days)',
    tooltip: 'For how many days during the past 30 days was the physical health good? Example: 30 days would mean that I had a good physical health in the past 30 days.'
  }, {
    key: 'MentalHealth',
    title: 'Good Mental Health (days)',
    tooltip: 'For how many days during the past 30 days was the mental health good? Example: 30 days would mean that I had a good mental health in the past 30 days.'
  }, {
    key: 'SleepTime',
    title: 'Sleep Time (hours)',
    tooltip: 'Average sleep time in the past Month. Amount of sleep time can have an significant effect on the probability of having heart disease.'
  }, {
    key: 'AgeCategory',
    title: 'Age Category',
  }, {
    key: 'Sex',
    title: 'Sex Health',
  }, {
    //   key: 'Race',
    //   title: 'Race',
    // }, {
    key: 'Diabetic',
    title: 'Diabetic',
  }, {
    key: 'GenHealth',
    title: 'General Health',
  }, {
    key: 'Smoking',
    title: 'Has Smoked',
    tooltip: 'Has smoked more than 100 cigarettes.'
  }, {
    key: 'AlcoholDrinking',
    title: 'Drinks Alcohol',
  }, {
    key: 'Stroke',
    title: 'Had Stroke',
  }, {
    key: 'DiffWalking',
    title: 'Has difficulties walking',
    tooltip: 'Has difficulties walking or climbing stairs.'
  }, {
    key: 'PhysicalActivity',
    title: 'Is physically active',
    tooltip: 'Was physically active in the last month.'
  }, {
    key: 'Asthma',
    title: 'Has Asthma',
  }, {
    key: 'KidneyDisease',
    title: 'Has Kidney Disease',
  }, {
    key: 'SkinCancer',
    title: 'Has Skin Cancer',
  },
])
const sidebarForm = ref()
const emitter = inject('eventBus');

function getFormData() {
  let tempFormData = {}
  Array.from(sidebarForm.value.elements).forEach((input) => {
    if (input.name.length > 0)
      tempFormData[input.name] = input.type === 'checkbox' ? input.checked : input.value
  })
  return tempFormData
}

function randomize() {
  Array.from(sidebarForm.value.elements).forEach((input) => {
    if (input.name.length > 0) {
      if (input.tagName === 'SELECT') {
        const optionsNr = input.options.length
        input.selectedIndex = Math.floor(Math.random() * optionsNr);
      }
      if (input.type === 'range') {
        let randVal = parseInt(Math.random() * (parseInt(input.max) - parseInt(input.min)) + parseInt(input.min))
        let numberInput = input.parentElement.querySelector('input[type="number"]')
        input.value = randVal;
        numberInput.value = randVal
      }
      if (input.type === 'checkbox') {
        input.checked = Math.random() >= 0.5;
      }
    }
  })
}

function onSubmit() {
  console.log('submit')
  dashboardStore.setSidebarFormData(getFormData())
}

onMounted(() => {
  dashboardStore.sidebarFormData = getFormData();
});

</script>
<template>
  <div v-if="dashboardStore.datasetColumns">
    <form ref="sidebarForm" @submit.prevent="onSubmit()">
      <div>
        <div class="input-group mb-1">
          <label class="row col-12">
              <span class="flex v-align-center space-between col-9">
                {{ 'Weight (kg)' }}
                <TooltipTrigger
                    :tooltip-text="'Weight and height are used to calculate BMI. People are considered overweight for BMI > 26'"></TooltipTrigger>
              </span>
            <SliderInput :name="'weight'" :min="50" :max="200"></SliderInput>
          </label>
        </div>
        <div class="input-group mb-1">
          <label class="row col-12" for="slider">
              <span class="flex v-align-center space-between col-9">
                {{ 'Height (cm)' }}
              </span>
            <SliderInput :name="'height'" :min="100" :max="220"></SliderInput>
          </label>
        </div>
        <template v-for="inputDef in inputs">
          <div
              v-if="dashboardStore.datasetColumns[inputDef.key]&&dashboardStore.datasetColumns[inputDef.key]['type']==='numerical'"
              class="input-group mb-1">
            <label class="row col-12">
              <span class="flex v-align-center space-between col-9">
                {{ inputDef.title }}
                <TooltipTrigger v-if="inputDef.tooltip" :tooltip-text="inputDef.tooltip"></TooltipTrigger>
              </span>
              <SliderInput :name="inputDef.key" :min="dashboardStore.datasetColumns[inputDef.key]['values'][0]"
                           :max="dashboardStore.datasetColumns[inputDef.key]['values'][1]"></SliderInput>
            </label>
          </div>
          <div
              v-if="dashboardStore.datasetColumns[inputDef.key]&&dashboardStore.datasetColumns[inputDef.key]['type']==='category'"
              class="input-group mb-1">
            <label class="row col-12 space-between">
              <span class="flex v-align-center col-6">
                 {{ inputDef.title }}
                <TooltipTrigger v-if="inputDef.tooltip" :tooltip-text="inputDef.tooltip"></TooltipTrigger>
              </span>
              <Select class="col-6" :name="inputDef.key">
                <option v-for="(key,value) in dashboardStore.datasetColumns[inputDef.key]['values']">{{
                    value
                  }}
                </option>
              </Select>
            </label>
          </div>
          <div
              v-if="dashboardStore.datasetColumns[inputDef.key]&&dashboardStore.datasetColumns[inputDef.key]['type']==='boolean'"
              class="input-group mb-1">
            <label class="row col-12 space-between v-align-center">
              <span class="flex v-align-center space-between col-9">
                 {{ inputDef.title }}
                <TooltipTrigger v-if="inputDef.tooltip" :tooltip-text="inputDef.tooltip"></TooltipTrigger>
              </span>
              <input type="checkbox" :name="inputDef.key" class="col-3">
            </label>
          </div>
        </template>
      </div>
      <div class="flex" style="gap: 10px">
        <button id="randomizer" type="button" @click="randomize" class="col-6">Randomize</button>
        <button type="submit" class="col-6">Analyze</button>
      </div>
    </form>
  </div>
</template>

<style scoped>

</style>
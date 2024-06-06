<script setup>
import {ref, onMounted, watch} from "vue";
import {storeToRefs} from 'pinia'
import {useDashboardStore} from "@/stores/dashboard.js";
import SliderInput from "@/components/Inputs/SliderInput.vue";
import useEmitter from "@/composables/useEmitter.js";
import Tooltip from "@/components/Tooltip.vue";

const store = useDashboardStore();

const inputs = ref([
  {
    key: 'BMI',
    title: 'Body Mass Index',
    tooltip: 'Body Mass Index is an important measurement for checking whether someone is probably obese. (> 26)'
  }, {
    key: 'PhysicalHealth',
    title: 'Physical Health',
    tooltip: 'For how many days during the past 30 days was the physical health good?'
  }, {
    key: 'MentalHealth',
    title: 'Mental Health',
    tooltip: 'For how many days during the past 30 days was the mental health good?'
  }, {
    key: 'SleepTime',
    title: 'Sleep Time',
    tooltip: 'Amount of sleep time can have an significant effect on the probability of having heart disease.'
  }, {
    key: 'AgeCategory',
    title: 'Age Category',
  }, {
    key: 'Sex',
    title: 'Sex Health',
  }, {
    key: 'Race',
    title: 'Race',
  }, {
    key: 'Diabetic',
    title: 'Diabetic',
  }, {
    key: 'GenHealth',
    title: 'General Health',
  }, {
    key: 'Smoking',
    title: 'Is Smoking',
  }, {
    key: 'AlcoholDrinking',
    title: 'Drinks alcohol',
  }, {
    key: 'Stroke',
    title: 'Had Stroke',
  }, {
    key: 'DiffWalking',
    title: 'Has difficulties walking',
  }, {
    key: 'PhysicalActivity',
    title: 'Is physically active',
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
const emitter = useEmitter();

function setFormData() {
  store.sidebarFormData = {}
  Array.from(sidebarForm.value.elements).forEach((input) => {
    if (input.name.length > 0)
      store.sidebarFormData[input.name] = input.type === 'checkbox' ? input.checked : input.value
  })
  console.log('emit')
  emitter.emit('submitSidebar')
}

function randomize() {
  Array.from(sidebarForm.value.elements).forEach((input) => {
    if (input.name.length > 0) {
      if (input.tagName === 'SELECT') {
        const optionsNr = input.options.length
        input.selectedIndex = Math.floor(Math.random() * optionsNr);
      }
      if (input.type === 'range') {
        let randVal = parseInt(Math.random() * (input.max - input.min) + input.min)
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

//
// onMounted(() => {
//   if (sidebarForm.value) {
//     setFormData();
//   }
// });


watch(() => sidebarForm.value, (newValue) => {
  if (newValue) {
    setFormData();
  }
});

</script>
<template>
  <div v-if="store.datasetColumns">
    <form ref="sidebarForm" @submit.prevent="setFormData($event)">
      <div>
        <template v-for="inputDef in inputs">
          <div v-if="store.datasetColumns[inputDef.key]['type']==='numerical'" class="input-group mb-1">
            <label class="row col-12" for="${label_for}">
              <span class="flex v-align-center space-between col-9">
                {{ inputDef.title }}
                <Tooltip v-if="inputDef.tooltip" :tooltip-text="inputDef.tooltip"></Tooltip>
              </span>
              <SliderInput :name="inputDef.key" :min="store.datasetColumns[inputDef.key]['values'][0]"
                           :max="store.datasetColumns[inputDef.key]['values'][1]"></SliderInput>
            </label>
          </div>
          <div v-if="store.datasetColumns[inputDef.key]['type']==='category'" class="input-group mb-1">
            <label class="row col-12 space-between" for="${label_for}">
              <span class="flex v-align-center col-6">
                 {{ inputDef.title }}
                <Tooltip v-if="inputDef.tooltip" :tooltip-text="inputDef.tooltip"></Tooltip>
              </span>
              <Tooltip v-if="inputDef.tooltip" :tooltip-text="inputDef.tooltip"></Tooltip>
              <select class="col-6" :name="inputDef.key">
                <option v-for="(key,value) in store.datasetColumns[inputDef.key]['values']">{{ value }}</option>
              </select>
            </label>
          </div>
          <div v-if="store.datasetColumns[inputDef.key]['type']==='boolean'" class="input-group mb-1">
            <label class="row col-12 space-between" for="'checkbox">
              <span class="flex v-align-center col-6">
                 {{ inputDef.title }}
                <Tooltip v-if="inputDef.tooltip" :tooltip-text="inputDef.tooltip"></Tooltip>
              </span>
              <Tooltip v-if="inputDef.tooltip" :tooltip-text="inputDef.tooltip"></Tooltip>
              <input type="checkbox" :name="inputDef.key" class="col-6">
            </label>
          </div>
        </template>
      </div>
      <div class="row">
        <button id="randomizer" type="button" @click="randomize">Randomize</button>
        <button type="submit">Explain</button>
      </div>
    </form>
  </div>
</template>

<style scoped>

</style>
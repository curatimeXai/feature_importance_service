<script setup>
import {defineProps, onMounted, ref} from "vue";

const props = defineProps({
  titleProp: String,
  subtitleProp: {
    type: String | Number,
    default: 0
  },
  iconProp: {
    type: String,
    default: 'fa fa-circle'
  },
  colorProp: {
    type: String,
    default: 'var(--middle-color)'
  },
  suffix: {
    type: String,
    default: ''
  },
  parserFunctionName: {
    type: String | null,
    default: 'parseNumeric'
  }
})

const title = ref(props.titleProp)
const subtitle = ref(props.subtitleProp)
const icon = ref(props.iconProp)
const color = ref(props.colorProp)

const lang = 'en-EN';

const parsers = {
  parseNumeric: () => {
    let parsed = parseFloat(subtitle.value)
    let localParsed = parsed.toLocaleString(lang, {minimumFractionDigits: 0, maximumFractionDigits: 2});
    if (parsed > 0) {
      subtitle.value = '+' + localParsed;
      color.value = 'var(--positive-color)'
      icon.value = 'fa fa-thumbs-up'
    }
    if (parsed < 0) {
      subtitle.value = localParsed;
      color.value = 'var(--negative-color)'
      icon.value = 'fa fa-thumbs-down'
    }
  },
  parseInverseNumeric: () => {
    let parsed = parseFloat(subtitle.value)
    let localParsed = parsed.toLocaleString(lang, {minimumFractionDigits: 0, maximumFractionDigits: 2});
    if (parsed < 0) {
      subtitle.value = localParsed
      color.value = 'var(--positive-color)'
      icon.value = 'fa fa-thumbs-up'
    }
    if (parsed > 0) {
      subtitle.value = '+' + localParsed;
      color.value = 'var(--negative-color)'
      icon.value = 'fa fa-thumbs-down'
    }
  }

}


onMounted(() => {
  if (props.parserFunctionName) {
    parsers[props.parserFunctionName]();
  }
})

</script>

<template>
  <div class="badge" :style="`border: 1px solid ${color};`">
    <h4>{{ title }}</h4>
    <div style="color: #371ea3;">{{ subtitle + suffix }}</div>
    <div style="font-size: 30px;" :style="`color: ${color};`">
      <i :class="icon"></i>
    </div>
  </div>
</template>

<style scoped>

</style>
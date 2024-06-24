<script setup>
import {defineProps} from "vue";

const props = defineProps({
  width: {
    default: 30,
    type: Number
  },
  tooltipText: String
})

function tooltipShow($event) {
  let tooltipElem = document.getElementById('tooltip')
  let boundary = $event.target.getBoundingClientRect()
  tooltipElem.style.top = boundary.top + 'px'
  tooltipElem.style.left = (boundary.left + 30) + 'px'
  tooltipElem.innerText = props.tooltipText
  tooltipElem.style.opacity = 1
  tooltipElem.style.visibility = 'visible'
}

function tooltipHide($event) {
  let tooltipElem = document.getElementById('tooltip')
  tooltipElem.innerText = ''
  tooltipElem.style.opacity = 0
  tooltipElem.style.visibility = 'hidden'

}
</script>

<template>
  <div @mouseenter="tooltipShow($event)" @mouseleave="tooltipHide($event)" class="tooltip-container mr-1">
    <svg :style="'width: '+props.width+'px'" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle opacity="0.5" cx="12" cy="12" r="10" stroke="#C1002A" stroke-width="1.5"/>
      <path
          d="M10.125 8.875C10.125 7.83947 10.9645 7 12 7C13.0355 7 13.875 7.83947 13.875 8.875C13.875 9.56245 13.505 10.1635 12.9534 10.4899C12.478 10.7711 12 11.1977 12 11.75V13"
          stroke="#C1002A" stroke-width="1.5" stroke-linecap="round"/>
      <circle cx="12" cy="16" r="1" fill="#C1002A"/>
    </svg>
  </div>
</template>

<style scoped>

</style>
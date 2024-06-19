<script setup>

import ScopeToggler from "@/components/ScopeToggler.vue";
</script>

<template>
  <RouterLink to="/"
              style="position: absolute;
                    color: var(--bright-color);
                    left: 2%;
                    top: 5px;
                    font-size: 30px;">
    <i class="fa fa-arrow-left"></i>
  </RouterLink>
  <div class="container">
    <div class="capsule">
      <h1>Tutorial</h1>
      <ScopeToggler :disabled="true"></ScopeToggler>
      <div class="flex g-1">
        <div class="col-4">
          <h4>Local Scope</h4>
          <p>On local scope you can input different caracteristics of a patient and see which risk factors contribute or
            reduct the probability of having heart disease</p>
        </div>
        <div class="col-4">
          <h4>Global Scope</h4>
          <p>On global scope, there are multiple views that help you understand the whole dataset and current model</p>
        </div>
        <div class="col-4">
          <h4>Settings</h4>
          <p>In settings you can change the current active model or dataset</p>
        </div>
      </div>
      <div class="flex g-1 mb-2">
        <div>
          <h2>Step 1: Input</h2>
          <h4>Input the attributes of a person. You could also just randomize the input.</h4>
          <p><b>Example:</b> Here, I just put my own stats in with some differences like:</p>
          <ul>
            <li>Physical Health: only 23/30 days where I had good physical health</li>
            <li>Sleep Time: I slept in average only 3 hours (not really)</li>
            <li>Age Category: Me as an old person. How would the heart disease probability would look like?</li>
            <li>General Health: Poor, since I live an unhealthy lifestyle as an old person.</li>
            <li>The checkboxes are all unchecked</li>
          </ul>
        </div>
        <img src="../assets/images/local_sidebar_alex_bad_upper.png" alt="Me as an old person">
      </div>
      <div class="mb-1">
        <div class="flex g-1 mb-1">
          <div>
            <h2>Step 2: Analyze the output</h2>
            <h4>Overview</h4>
            <p>
              In the overview, we can clearly see that there is a high risk of having heart disease.<br>
              The risk factors are listed from strongest positive risk factors to the worse ones.
            </p>
          </div>
<!--          todo: give example-->
          <img class="col-6" src="../assets/images/local_dashboard_overview_bad.png" alt="Me as an old person">
        </div>
        <div class="flex g-1 mb-1">
          <div>
            <h4>Risk Factors (Accumulative), so called "Break Down Chart"</h4>
            <p>
              This chart is useful for viewing which risk factor increases the probability to some degree.
            </p>
            <p>In this example, because of General Health, Age Category, Sleep Time and Physical Health the probability
              increases to over 50%.</p>
            <p>However, because of the other factors, the probability also decreases.</p>
            <p><i class="fa fa-circle-exclamation" style="color: var(--warning-color);"></i> All probability values in
              charts are written in mathematical writing. This means that <b>10% is 0.1</b>.</p>
          </div>
<!--          todo: Explain some bars-->
          <img class="col-8" src="../assets/images/local_dashboard_break_down_chart.png" alt="Me as an old person">
        </div>
        <div class="flex g-1 mb-1">
          <div>
            <h4>Risk Factors (Comparison), so called "Shapley Chart"</h4>
            <p>
              This chart is rather relevant for comparing the influence of certain risk factors.
            </p>
          </div>
<!--          todo: why is there a difference between breakdown and shapley in terms of contribution-->
<!--          todo: give examples-->
          <img class="col-8" src="../assets/images/local_dashboard_shapley_chart.png" alt="Me as an old person">
        </div>
      </div>
      <div>
        <h2>Step 3</h2>
        <p>Check infos about the model and dataset in the global scope</p>
      </div>
      <div>
        <h2>Optional Step</h2>
        <p>Try other models out.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
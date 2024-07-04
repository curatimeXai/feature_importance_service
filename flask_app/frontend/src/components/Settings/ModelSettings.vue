<script setup xmlns="http://www.w3.org/1999/html">
import {useDashboardStore} from "@/stores/dashboard.js";
import {computed, onMounted, ref} from "vue";
import Http from "@/helpers/Http.js";

const dashboardStore = useDashboardStore();
const accuracy = ref(null)
const computedAccuracy=computed(()=>{
  if (accuracy.value!==null) {
      return (parseFloat(accuracy.value)*100).toLocaleString('en-EN', {minimumFractionDigits: 0, maximumFractionDigits: 2})+'%';
  }
  return 0
})
function loadAccuracy() {
  accuracy.value = null
  Http.get(`/${dashboardStore.model}/accuracy`).then(async (response) => {
    accuracy.value = await response.json()
  })
}

onMounted(() => {
  loadAccuracy();
})
</script>

<template>
  <div class="flex g-1">
    <div class="col-6 mt-2">
      <label class="row space-between mb-1" style="align-self: flex-start">
      <span class="flex v-align-center col-6">
        Current Model
      </span>
        <select v-model="dashboardStore.model" @change="loadAccuracy" class="col-6">
          <option selected value="xgb">XGBoost</option>
          <option value="svm">Support Vector Machine</option>
          <option value="rand_forest">Random Forest</option>
          <option value="dnn">Deep Neural Network</option>
          <option value="lr">Logistic Regression</option>
        </select>
      </label>
      <div class="flex">
        <div class="col-6">Accuracy:</div>
        <div class="col-6">{{ accuracy === null ? 'loading...' : computedAccuracy }}</div>
      </div>
    </div>
    <div class="col-6" v-if="dashboardStore.model==='xgb'">
      <h4>XGBoost</h4>
      <ul>
        <li>Tree-based model</li>
        <li>Stands for eXtreme Gradient Boosting</li>
        <li>Known for high performance and speed</li>
        <li>Handles missing data efficiently</li>
        <li>Supports parallel processing</li>
        <li>Can be used for classification and regression tasks</li>
      </ul>
    </div>
    <div class="col-6" v-if="dashboardStore.model==='svm'">
      <h4>Support Vector Machine</h4>
      <ul>
        <li>Supervised learning model</li>
        <li>Effective for high-dimensional spaces</li>
        <li>Used for classification and regression tasks</li>
        <li>Utilizes the concept of decision planes</li>
        <li>Supports both linear and non-linear classification</li>
        <li>Employs kernel trick for non-linear problems</li>
        <li>Robust to overfitting, especially in high-dimensional space</li>
        <li>Popular in text and image classification</li>
      </ul>
    </div>
    <div class="col-6" v-if="dashboardStore.model==='rand_forest'">
      <h4>Random Forest</h4>
      <ul>
        <li>Ensemble learning method</li>
        <li>Combines multiple decision trees</li>
        <li>Can be used for classification and regression tasks</li>
        <li>Reduces overfitting compared to individual decision trees</li>
        <li>Uses bootstrap aggregating (bagging) technique</li>
        <li>Provides feature importance measures</li>
        <li>Handles large datasets with higher dimensionality</li>
        <li>Robust to noise and outliers</li>
        <li>Works well with both categorical and continuous data</li>
      </ul>
    </div>
    <div class="col-6" v-if="dashboardStore.model==='dnn'">
      <h4>Deep Neural Network (DNN)</h4>
      <ul>
        <li>Type of artificial neural network</li>
        <li>Contains multiple hidden layers</li>
        <li>Inspired by the structure of the human brain</li>
        <li>Capable of learning complex patterns</li>
        <li>Requires large amounts of data and computational power</li>
        <li>Utilizes activation functions like ReLU, sigmoid, and tanh</li>
        <li>Trained using backpropagation and gradient descent</li>
        <li>Benefited from advancements in GPU technology</li>
      </ul>
    </div>
    <div class="col-6" v-if="dashboardStore.model==='lr'">
      <h4>Logistic Regression</h4>
      <ul>
        <li>Statistical model for binary classification</li>
        <li>Predicts the probability of a binary outcome</li>
        <li>Uses the logistic (sigmoid) function</li>
        <li>Estimates parameters using maximum likelihood estimation</li>
        <li>Assumes a linear relationship between input features and the log-odds of the outcome</li>
        <li>Interpretable model, useful for understanding feature impact</li>
        <li>Can be extended to multiclass classification using techniques like one-vs-rest</li>
        <li>Often used in medical, social sciences, and marketing applications</li>
        <li>Handles both continuous and categorical data</li>
      </ul>
    </div>
  </div>

</template>

<style scoped>

</style>
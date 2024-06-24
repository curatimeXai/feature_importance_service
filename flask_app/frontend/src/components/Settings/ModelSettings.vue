<script setup xmlns="http://www.w3.org/1999/html">
import {useDashboardStore} from "@/stores/dashboard.js";

const dashboardStore = useDashboardStore();
</script>

<template>
  <div class="flex g-1">
    <label class="row col-6 space-between mt-2" style="align-self: flex-start">
      <span class="flex v-align-center col-6">
        Current Model
      </span>
      <select v-model="dashboardStore.model" class="col-6">
        <option selected value="xgb">XGBoost</option>
        <option value="svm">Support Vector Machine</option>
        <option value="rand_forest">Random Forest</option>
        <option value="dnn">Deep Neural Network</option>
        <option value="lr">Logistic Regression</option>
      </select>
    </label>
    <div class="col-6" v-if="dashboardStore.model==='xgb'">
      <h4>XGBoost</h4>
      <ul>
        <li>Tree-based model</li>
        <li>Stands for eXtreme Gradient Boosting</li>
        <li>Developed by Tianqi Chen</li>
        <li>Known for high performance and speed</li>
        <li>Utilizes gradient boosting framework</li>
        <li>Handles missing data efficiently</li>
        <li>Supports parallel processing</li>
        <li>Widely used in data science competitions</li>
        <li>Provides feature importance metrics</li>
        <li>Can be used for classification and regression tasks</li>
      </ul>
    </div>
    <div class="col-6" v-if="dashboardStore.model==='svm'">
      <h4>Support Vector Machine</h4>
      <ul>
        <li>Supervised learning model</li>
        <li>Effective for high-dimensional spaces</li>
        <li>Used for classification and regression tasks</li>
        <li>Introduced by Vladimir Vapnik and Alexey Chervonenkis</li>
        <li>Utilizes the concept of decision planes</li>
        <li>Maximizes the margin between classes</li>
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
        <li>Developed by Leo Breiman and Adele Cutler</li>
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
        <li>Used for tasks like image recognition, speech recognition, and natural language processing</li>
        <li>Requires large amounts of data and computational power</li>
        <li>Utilizes activation functions like ReLU, sigmoid, and tanh</li>
        <li>Trained using backpropagation and gradient descent</li>
        <li>Benefited from advancements in GPU technology</li>
        <li>Forms the basis of deep learning</li>
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
        <li>Provides coefficients that indicate the importance of each feature</li>
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
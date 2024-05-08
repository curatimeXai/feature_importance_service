import os

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score


class DescriptiveCharts:
    def __init__(self, data_path, sample_size=200):
        self.data = pd.read_csv(data_path)
        self.data = self.data.drop(columns=[self.data.columns[0]])

    def create_scatter_plot(self,x, y, xlabel, ylabel):
        plt.figure(figsize=(8, 6))
        plt.scatter(self.data[x], self.data[y], alpha=0.5)
        plt.title(f"{xlabel} vs {ylabel}")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()

    def box_plot(self,col):
        self.data.boxplot(column=col)
        plt.title(f"Boxplot {col}")
        plt.grid(True)
        plt.show()

    def plot_a_and_b(self, col):
        unique_vals = descriptive.data[col].unique()
        unique_vals.sort()
        probs = []
        for unique_val in unique_vals:
            count_heart_dis = descriptive.data[descriptive.data[col] == unique_val]["HeartDisease"].count()
            probs.append(count_heart_dis / descriptive.data.shape[0])

        plt.plot(unique_vals, probs, marker='o', linestyle='-')
        plt.show()

    def plot_a_given_b(self, col):
        groups = descriptive.data.groupby([col])
        probabilities = groups['HeartDisease'].mean()
        plt.plot(probabilities.index, probabilities.values, marker='o', linestyle='-')
        plt.title(f"HeartDisease given {col}")
        plt.show()

    def plot_distribution(self,col):
        distribution = self.data[col].value_counts()
        zipped = list(zip(distribution.index, distribution.values))
        zipped_sorted = sorted(zipped, key=lambda x: x[0])
        x_values = [item[0] for item in zipped_sorted]
        y_values = [item[1] for item in zipped_sorted]

        # Plotting the distribution as a bar plot
        plt.plot(x_values, y_values, marker='o', linestyle='-')
        plt.title(f"Distribution of {col}")
        plt.show()

data_path='/home/alex/UniProjects/BachelorXAI/datasets/dataset_2020_2022/2020/heart_2020_cleaned_numerical.csv'
descriptive = DescriptiveCharts(data_path)
descriptive.data['BMI_Rounded'] = descriptive.data['BMI'].round().astype(int)


descriptive.box_plot('AgeCategory')
descriptive.plot_a_and_b('BMI_Rounded')
descriptive.plot_a_and_b('AgeCategory')
descriptive.plot_distribution('AgeCategory')
descriptive.plot_a_and_b('PhysicalHealth')
descriptive.plot_a_given_b('PhysicalHealth')

# phys_health_groups=descriptive.data.groupby(['PhysicalHealth'])
# phys_health_probabilities = phys_health_groups['HeartDisease'].mean()
# plt.plot(phys_health_probabilities.index, phys_health_probabilities.values, marker='o', linestyle='-')
# plt.show()

# grouped_by_booleans=descriptive.data.groupby(['Smoking','AlcoholDrinking','Stroke','DiffWalking','PhysicalActivity','Asthma','KidneyDisease','SkinCancer'])
# booleans_probabilities = grouped_by_booleans['HeartDisease'].mean()
# plt.plot(booleans_probabilities.index, booleans_probabilities.values, marker='o', linestyle='-')
# plt.show()

#
# descriptive.create_scatter_plot("BMI", "HeartDisease", "BMI", "Heart Disease")
# descriptive.create_scatter_plot("Smoking", "AlcoholDrinking", "Smoking", "Alcohol Drinking")
# descriptive.create_scatter_plot("PhysicalHealth", "MentalHealth", "Physical Health", "Mental Health")
# descriptive.create_scatter_plot("AgeCategory", "SleepTime", "Age Category", "Sleep Time")
# descriptive.create_box_plot("HeartDisease", "BMI", "Has HeartDisease", "BMI")


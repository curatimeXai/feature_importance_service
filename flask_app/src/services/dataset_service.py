import math
import os

import numpy as np
import pandas as pd

from src.helpers import get_datasets_path


class DatasetService:
    def __init__(self):
        self.datasets_paths = [
            get_datasets_path('dataset_2020_2022/2020/heart_2020_cleaned.csv'),
            get_datasets_path('dataset_2020_2022/2020/heart_2020_cleaned_numerical.csv'),
            get_datasets_path('dataset_2020_2022/2022/heart_2022_no_nans_numerical.csv'),
        ]
        self.kaggle_heart_disease_2020 = pd.read_csv(self.datasets_paths[1])
        self.kaggle_heart_disease_2020 = self.kaggle_heart_disease_2020.drop(columns=[self.kaggle_heart_disease_2020.columns[0], 'Race'])
        self.kaggle_heart_disease_2020_columns = {
            'HeartDisease': {'title': 'Heart Disease', 'type': 'boolean', 'values': {'No': 0, 'Yes': 1}},
            'Smoking': {'type': 'boolean', 'values': {'No': 0, 'Yes': 1}},
            'AlcoholDrinking': {'title': 'Drinking Alcohol', 'type': 'boolean', 'values': {'No': 0, 'Yes': 1}},
            'Stroke': {'title': 'Had Stroke', 'type': 'boolean', 'values': {'No': 0, 'Yes': 1}},
            'DiffWalking': {'title': 'Has Difficulties Walking', 'type': 'boolean', 'values': {'No': 0, 'Yes': 1}},
            'PhysicalActivity': {'title': 'Has Physical Activity', 'type': 'boolean', 'values': {'No': 0, 'Yes': 1}},
            'Asthma': {'title': 'Has Asthma', 'type': 'boolean', 'values': {'No': 0, 'Yes': 1}},
            'KidneyDisease': {'title': 'Has Kidney Disease', 'type': 'boolean', 'values': {'No': 0, 'Yes': 1}},
            'SkinCancer': {'title': 'Has Skin Cancer', 'type': 'boolean', 'values': {'No': 0, 'Yes': 1}},
            'Sex': {'type': 'category', 'values': {'Male': 1, 'Female': 2}},
            'AgeCategory': {'title': 'Age Category', 'type': 'category', 'values': {
                "18-24": 1,
                "25-29": 2,
                "30-34": 3,
                "35-39": 4,
                "40-44": 5,
                "45-49": 6,
                "50-54": 7,
                "55-59": 8,
                "60-64": 9,
                "65-69": 10,
                "70-74": 11,
                "75-79": 12,
                "80 or older": 13,
            }},
            # 'Race': {'type': 'category', 'values': {
            #     "White": 1,
            #     "Black": 2,
            #     "Asian": 3,
            #     "Hispanic": 4,
            #     "American Indian/Alaskan Native": 5,
            #     "Other": 6,
            # }},
            'Diabetic': {'type': 'category', 'values': {
                "No": 2,
                "Yes": 1,
                "Yes (during pregnancy)": 3,
                "No, borderline diabetes": 4,
            }},
            'GenHealth': {'title': 'General Health', 'type': 'category', 'values': {
                "Poor": 1,
                "Fair": 2,
                "Good": 3,
                "Very good": 4,
                "Excellent": 5,
            }},
            'BMI': {'type': 'numerical', 'values': [self.kaggle_heart_disease_2020['BMI'].min(), self.kaggle_heart_disease_2020['BMI'].max()]},
            'PhysicalHealth': {'title': 'Physical Health', 'type': 'numerical', 'invertValue': True,
                               'values': [self.kaggle_heart_disease_2020['PhysicalHealth'].min(),
                                          self.kaggle_heart_disease_2020['PhysicalHealth'].max()]},
            'MentalHealth': {'title': 'Mental Health', 'type': 'numerical', 'invertValue': True,
                             'values': [self.kaggle_heart_disease_2020['MentalHealth'].min(), self.kaggle_heart_disease_2020['MentalHealth'].max()]},
            'SleepTime': {'title': 'Sleep Time', 'type': 'numerical',
                          'values': [self.kaggle_heart_disease_2020['SleepTime'].min(), self.kaggle_heart_disease_2020['SleepTime'].max()]},
        }

    def transform_2020_input(self, input):
        transformed_input = []
        X = self.kaggle_heart_disease_2020.drop(columns=['HeartDisease'])
        for col in X.columns:
            if self.kaggle_heart_disease_2020_columns[col]['type'] == 'boolean':
                transformed_input.append(1 if input[col] == 'true' else 0)
            if self.kaggle_heart_disease_2020_columns[col]['type'] == 'category':
                transformed_input.append(self.kaggle_heart_disease_2020_columns[col]['values'][input[col]])
            if self.kaggle_heart_disease_2020_columns[col]['type'] == 'numerical':
                if self.kaggle_heart_disease_2020_columns[col].get('invertValue', False):
                    transformed_input.append(abs(float(input[col]) - self.kaggle_heart_disease_2020_columns[col]['values'][1]))
                else:
                    transformed_input.append(float(input[col]))

        return transformed_input

    def calculateBMI(self, weight, height):
        bmi = int(weight) / (int(height) / 100) ** 2
        if (bmi < 12):
            bmi = 12
        if (bmi > 92):
            bmi = 92
        return bmi

    def get_numerical_columns(self, dataset_columns):
        columns = getattr(self, dataset_columns)
        numerical_columns = []
        for col, col_settings, in columns.items():
            if col_settings['type'] == 'numerical':
                numerical_columns.append(col)

        return numerical_columns

    def get_boolean_columns(self, dataset_columns):
        columns = getattr(self, dataset_columns)
        boolean_columns = []
        for col, col_settings, in columns.items():
            if col_settings['type'] == 'boolean':
                boolean_columns.append(col)

        return boolean_columns

    def get_categorical_columns(self, dataset_columns):
        columns = getattr(self, dataset_columns)
        category_columns = []
        for col, col_settings, in columns.items():
            if col_settings['type'] == 'category':
                category_columns.append(col)

        return category_columns

    def convert_int64_to_int(self,data):
        if isinstance(data, dict):
            return {k: self.convert_int64_to_int(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.convert_int64_to_int(i) for i in data]
        elif isinstance(data, np.int64):
            return int(data)
        else:
            return data
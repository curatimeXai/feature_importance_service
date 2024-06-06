import math

import pandas as pd


class DatasetService:
    def __init__(self):
        self.datasets_paths = [
            '/home/alex/UniProjects/BachelorXAI/datasets/dataset_2020_2022/2020/heart_2020_cleaned.csv',
            '/home/alex/UniProjects/BachelorXAI/datasets/dataset_2020_2022/2020/heart_2020_cleaned_numerical.csv',
            '/home/alex/UniProjects/BachelorXAI/datasets/dataset_2020_2022/2022/heart_2022_no_nans_numerical.csv'
        ]
        self.data_2020 = pd.read_csv(self.datasets_paths[1])
        self.data_2020 = self.data_2020.drop(columns=[self.data_2020.columns[0]])
        self.columns_2020 = {
            'HeartDisease': {'title': 'Heart Disease', 'type': 'boolean', 'values': {'No': 0, 'Yes': 1}},
            'Smoking': {'type': 'boolean', 'values': {'No': 0, 'Yes': 1}},
            'AlcoholDrinking': {'title': 'Drinking alcohol', 'type': 'boolean', 'values': {'No': 0, 'Yes': 1}},
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
            'Race': {'type': 'category', 'values': {
                "White": 1,
                "Black": 2,
                "Asian": 3,
                "Hispanic": 4,
                "American Indian/Alaskan Native": 5,
                "Other": 6,
            }},
            'Diabetic': {'type': 'category', 'values': {
                "Yes": 1,
                "No": 2,
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
            'BMI': {'type': 'numerical', 'values': [self.data_2020['BMI'].min(), self.data_2020['BMI'].max()]},
            'PhysicalHealth': {'title': 'Physical Health', 'type': 'numerical', 'invertValue': True,
                               'values': [self.data_2020['PhysicalHealth'].min(),
                                          self.data_2020['PhysicalHealth'].max()]},
            'MentalHealth': {'title': 'Mental Health', 'type': 'numerical', 'invertValue': True,
                             'values': [self.data_2020['MentalHealth'].min(), self.data_2020['MentalHealth'].max()]},
            'SleepTime': {'title': 'Sleep Time', 'type': 'numerical',
                          'values': [self.data_2020['SleepTime'].min(), self.data_2020['SleepTime'].max()]},
        }

    def transform_2020_input(self, input):
        transformed_input = []
        X = self.data_2020.drop(columns=['HeartDisease'])
        for col in X.columns:
            if self.columns_2020[col]['type'] == 'boolean':
                transformed_input.append(1 if input[col] == 'on' else 0)
            if self.columns_2020[col]['type'] == 'category':
                transformed_input.append(self.columns_2020[col]['values'][input[col]])
            if self.columns_2020[col]['type'] == 'numerical':
                if self.columns_2020[col].get('invertValue', False):
                    transformed_input.append(abs(float(input[col]) - self.columns_2020[col]['values'][1]))
                else:
                    transformed_input.append(float(input[col]))

        return transformed_input

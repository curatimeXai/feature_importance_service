import inspect
import math
import os
import time

import dalex
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, log_loss

from src.services.dataset_service import DatasetService


class HeartDiseaseClassifier:
    def __init__(self, data_path=None, data=None, data_sample=0, stratify=False, model=None, ):
        start = time.time()
        if data_path is not None:
            self.data = pd.read_csv(data_path)
            self.data = self.data.drop(columns=[self.data.columns[0]])
            self.data = self.data.drop(columns=['Race'])
        if data is not None:
            self.data = data

        if stratify == True:
            true_df = self.data[self.data['HeartDisease'] == 1]
            false_df = self.data[self.data['HeartDisease'] == 0].sample(true_df.shape[0], random_state=42)
            self.data = pd.concat([true_df, false_df])

        if data_sample > 0:
            self.data = self.data.sample(n=data_sample, random_state=42)

        self.dataset_service = DatasetService()
        self.X = self.data.drop(columns=['HeartDisease'])
        self.y = self.data['HeartDisease']
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.X_normalized = self.scaler.fit_transform(self.X)
        self.X_normalized = pd.DataFrame(self.X_normalized, columns=self.X.columns)
        self.X_train, self.X_temp, self.y_train, self.y_temp = train_test_split(self.X_normalized, self.y,
                                                                                test_size=0.2, random_state=42)
        self.X_dev, self.X_test, self.y_dev, self.y_test = train_test_split(self.X_temp, self.y_temp, test_size=0.5,
                                                                            random_state=42)
        self.model = model
        self.explainer = None
        self.dalex_explainer = None
        end = time.time()
        print(f"HeartDiseaseClassifier __init__ time: {end - start}")

    def train(self, X=None, y=None, epochs=1, batch_size=32, increments=-1, is_dnn=False, callbacks=None):
        train_data = self.X_train if X is None else X
        target_data = self.y_train if y is None else y
        if is_dnn:
            history = self.model.fit(train_data, target_data, epochs=epochs, batch_size=batch_size,
                                     callbacks=callbacks)
            return history.history['accuracy']
        accuracies = []
        for i in range(epochs):
            if increments == -1:
                self.model.fit(train_data, target_data)
                accuracies.append(accuracy_score(self.y_dev, self.model.predict(self.X_dev)))
                continue

            for j in range(0, len(train_data), increments):
                end_index = min(j + increments, len(train_data))
                X_batch = train_data[j:end_index]
                y_batch = target_data[j:end_index]
                self.model.fit(X_batch, y_batch)
                if j % increments == 0:
                    y_pred_val = self.model.predict(self.X_dev)
                    accuracy = accuracy_score(self.y_dev, y_pred_val)
                    accuracies.append(accuracy)

        return accuracies

    def test_accuracy(self):
        y_pred_test = self.model.predict(self.X_test)
        test_accuracy = accuracy_score(self.y_test, (np.array(y_pred_test) > 0.5).astype(int).flatten())
        return test_accuracy

    def log_likelihood(self):
        y_prob_val = self.model.predict_proba(self.X_dev)
        return log_loss(self.y_dev, y_prob_val)

    def plot_accuracy(self, accuracies):
        plt.plot(range(len(accuracies)), accuracies)

    def load_model(self, model_path=None):
        start = time.time()
        if model_path is not None and os.path.exists(model_path):
            self.model = joblib.load(model_path)

        end = time.time()
        print(f"{inspect.stack()[0][3]} time: {end - start}")

    def model_is_saved(self, model_path):
        return os.path.exists(model_path)

    def load_explainer(self, explainer_path=None):
        if explainer_path is not None and os.path.exists(explainer_path):
            self.explainer = joblib.load(explainer_path)
        else:
            self.explainer = shap.Explainer(self.model.predict, self.X_sample)

    def load_dalex_explainer(self, explainer_path=None, X=None, y=None):
        start = time.time()
        if explainer_path is not None and os.path.exists(explainer_path):
            with open(explainer_path, 'rb') as fd:
                self.dalex_explainer = dalex.Explainer.load(fd)
        else:
            # explainer_data = pd.DataFrame(self.X_normalized, columns=self.X.columns) if X is None else X
            explainer_data = self.X_normalized if X is None else X
            explainer_targets = self.y if y is None else y
            self.dalex_explainer = dalex.Explainer(self.model, explainer_data, explainer_targets)

        end = time.time()
        print(f"{inspect.stack()[0][3]} time: {end - start}")

    def shap_analysis(self, sample_ind=20):
        shap_values = self.explainer(self.X_test[:100])
        feature_index = self.X.columns.get_loc("AgeCategory")
        shap.partial_dependence_plot(
            feature_index, self.model.predict, self.X_sample, model_expected_value=True,
            feature_expected_value=True, ice=False,
            shap_values=shap_values[sample_ind:sample_ind + 1, :],
        )

        interaction_index = self.X.columns.get_loc("Sex")
        shap.dependence_plot(
            feature_index, shap_values.values, self.X_test[:100],
            interaction_index=interaction_index,
            feature_names=self.X.columns)

        shap.plots.waterfall(shap_values[0])

        shap.plots.beeswarm(shap_values)

    def save_model(self, filename="trained_models/example_model.pkl"):
        joblib.dump(self.model, filename)

    def save_explainer(self, filename="trained_models/example_explainer.pkl"):
        joblib.dump(self.explainer, filename)

    def save_dalex_explainer(self, filename="trained_models/example_explainer.pkl"):
        with open(filename, 'wb') as fd:
            self.dalex_explainer.dump(fd)

    def denormalize_shapley(self, dalex_result, input):
        start = time.time()
        result_tpl = np.array([dalex_result.result['variable_name'], dalex_result.result['variable_value'],
                               dalex_result.result['variable']]).T

        for i, col in enumerate(self.X.columns):
            parsed_val = input[col]
            if self.dataset_service.kaggle_heart_disease_2020_columns[col]['type'] == 'numerical':
                parsed_val = int(float(input[col]))
            if self.dataset_service.kaggle_heart_disease_2020_columns[col]['type'] == 'boolean':
                parsed_val = 'Yes' if input[col] == 'true' else 'No'
            result_tpl[result_tpl[:, 0] == col, 2] = \
                f"{self.dataset_service.kaggle_heart_disease_2020_columns[col].get('title', col)} = {parsed_val}"

        dalex_result.result['variable'] = result_tpl[:, 2]
        end = time.time()
        print(f"{inspect.stack()[0][3]} time: {end - start}")
        return dalex_result

    def denormalize_bd_result(self, dalex_result, input):
        start = time.time()
        result_tpl = np.array([dalex_result.result['variable_name'], dalex_result.result['variable_value'],
                               dalex_result.result['variable']]).T
        # temp_result = pd.DataFrame(columns=self.X.columns)
        for i, col in enumerate(self.X.columns):
            parsed_val = input[col]
            if self.dataset_service.kaggle_heart_disease_2020_columns[col]['type'] == 'numerical':
                parsed_val = int(float(input[col]))
            if self.dataset_service.kaggle_heart_disease_2020_columns[col]['type'] == 'boolean':
                parsed_val = 'Yes' if input[col] == 'true' else 'No'
            result_tpl[result_tpl[:, 0] == col, 2] = \
                f"{self.dataset_service.kaggle_heart_disease_2020_columns[col].get('title', col)} = {parsed_val}"

        dalex_result.result['variable'] = result_tpl[:, 2]
        end = time.time()
        print(f"{inspect.stack()[0][3]} time: {end - start}")
        return dalex_result

    def denormalize_variable_row(self, col, denormalized_val):
        if (col in self.dataset_service.kaggle_heart_disease_2020_columns
                and self.dataset_service.kaggle_heart_disease_2020_columns[col]['type'] in ['boolean', 'category']):
            parsed_val = self.get_first_key_by_value(
                self.dataset_service.kaggle_heart_disease_2020_columns[col]['values'],
                int(denormalized_val[0]))
        else:
            parsed_val = int(np.floor(denormalized_val)[0])

        readable_varname = self.dataset_service.kaggle_heart_disease_2020_columns[col].get('title', col)

        return f'{readable_varname} = {parsed_val}'


    def denormalize_dalex_dataframe(self, dalex_result, variable):
        dataset_service = DatasetService()
        filtered_df = dalex_result.result[self.X.columns]
        denormalized = self.scaler.inverse_transform(filtered_df)
        dalex_result.result[self.X.columns] = denormalized
        filtered_df[variable] = dalex_result.result['_original_']
        denormalized_original = self.scaler.inverse_transform(filtered_df)
        dalex_result.result['_original_'] = denormalized_original[:, self.X.columns.get_loc(variable)]
        # readable_varnames = []
        # for varname in dalex_result.result['variable']:
        #     readable_varnames.append(
        #         dataset_service.kaggle_heart_disease_2020_columns[varname]['title'] if 'title' in
        #                                                                                dataset_service.kaggle_heart_disease_2020_columns[
        #                                                                                    varname] else varname)
        #
        # dalex_result.result['variable'] = readable_varnames
        return dalex_result

    def denormalize_x_y(self, dalex_result, variable):
        start = time.time()
        temp_result = pd.DataFrame(columns=self.X.columns)

        result_row = [0] * len(self.X.columns)
        for val in dalex_result.result['_x_']:
            result_row[self.X.columns.get_loc(variable)] = val
            temp_result.loc[len(temp_result.index)] = result_row

        denormalized_original = self.scaler.inverse_transform(temp_result)
        dalex_result.result['_x_'] = denormalized_original[:, self.X.columns.get_loc(variable)]
        dalex_result.result['_yhat_'] = dalex_result.result['_yhat_'].apply(lambda x: x * 100)
        end = time.time()
        print(f"{inspect.stack()[0][3]} time: {end - start}")
        return dalex_result

    def rename_variables(self, dalex_result):
        dataset_service = DatasetService()
        readable_varnames = []
        for varname in dalex_result.result['variable']:
            if varname in dataset_service.kaggle_heart_disease_2020_columns and 'title' in \
                    dataset_service.kaggle_heart_disease_2020_columns[varname]:
                readable_varnames.append(dataset_service.kaggle_heart_disease_2020_columns[varname]['title'])
            else:
                readable_varnames.append(varname)
        dalex_result.result['variable'] = readable_varnames
        return dalex_result

    def get_first_key_by_value(self, d, target_value):
        for key, value in d.items():
            if value == target_value:
                return key
        return None

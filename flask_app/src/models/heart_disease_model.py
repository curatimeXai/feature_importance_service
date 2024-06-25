import inspect
import math
import os
import time

import dalex
import joblib
import matplotlib.pyplot as plt
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

        self.X = self.data.drop(columns=['HeartDisease'])
        self.y = self.data['HeartDisease']
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.X_normalized = self.scaler.fit_transform(self.X)
        self.X_normalized = pd.DataFrame(self.X_normalized, columns=self.X.columns)
        self.X_train, self.X_temp, self.y_train, self.y_temp = train_test_split(self.X_normalized, self.y,
                                                                                test_size=0.2, random_state=42)
        self.X_val, self.X_test, self.y_val, self.y_test = train_test_split(self.X_temp, self.y_temp, test_size=0.5,
                                                                            random_state=42)
        self.model = model
        self.explainer = None
        self.dalex_explainer = None
        end = time.time()
        print(f"HeartDiseaseClassifier __init__ time: {end - start}")

    def train(self, X=None, y=None, epochs=1, batch_size=32, increments=-1, is_dnn=False, callbacks=None):
        accuracies = []
        train_data = self.X_train if X is None else X
        target_data = self.y_train if y is None else y
        if is_dnn:
            history = self.model.fit(train_data, target_data, epochs=epochs, batch_size=batch_size,
                                     callbacks=callbacks)
            return history.history['accuracy']
        for i in range(epochs):
            if increments == -1:
                self.model.fit(train_data, target_data)
                accuracies.append(accuracy_score(self.y_val, self.model.predict(self.X_val)))
                continue

            for j in range(0, len(train_data), increments):
                end_index = min(j + increments, len(train_data))
                X_batch = train_data[j:end_index]
                y_batch = target_data[j:end_index]
                self.model.fit(X_batch, y_batch)
                if j % increments == 0:
                    y_pred_val = self.model.predict(self.X_val)
                    accuracy = accuracy_score(self.y_val, y_pred_val)
                    accuracies.append(accuracy)

        return accuracies

    def test_accuracy(self):
        y_pred_test = self.model.predict(self.X_test)
        test_accuracy = accuracy_score(self.y_test, y_pred_test)
        return test_accuracy

    def log_likelihood(self):
        y_prob_val = self.model.predict_proba(self.X_val)
        return log_loss(self.y_val, y_prob_val)

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

    def denormalize_shapley(self,shap_result):
        start = time.time()
        dataset_service = DatasetService()  # Assuming this can be reused and is not changing per call

        result_tpl = pd.DataFrame({
            'variable_name': shap_result.result['variable_name'],
            'variable_value': shap_result.result['variable_value'],
            'variable': shap_result.result['variable']
        })

        dim = math.floor(len(result_tpl['variable']) / self.X.columns.size)
        temp_result = pd.DataFrame(result_tpl['variable_value'].values.reshape(dim, self.X.columns.size),
                                   columns=self.X.columns)
        new_variable_values = self.scaler.inverse_transform(temp_result)
        for i, col in enumerate(temp_result.columns):
            if col in result_tpl['variable_name'].values:
                parsed_val = math.floor(new_variable_values[0][i])
                if dataset_service.kaggle_heart_disease_2020_columns[col]['type'] in ['boolean', 'category']:
                    parsed_val = self.get_first_key_by_value(
                        dataset_service.kaggle_heart_disease_2020_columns[col]['values'], parsed_val)

                readable_varname = dataset_service.kaggle_heart_disease_2020_columns[col].get('title', col)
                result_tpl.loc[result_tpl['variable_name'] == col, 'variable']=f'{readable_varname} = {parsed_val}'

        shap_result.result['variable'] = result_tpl['variable'].values

        end = time.time()
        print(f"{inspect.stack()[0][3]} time: {end - start}")
        return shap_result

    def denormalize_bd_result(self, dalex_result):
        start = time.time()
        dataset_service = DatasetService()
        result_tpl = pd.DataFrame({
            'variable_name': dalex_result.result['variable_name'],
            'variable_value': dalex_result.result['variable_value'],
            'variable': dalex_result.result['variable']
        })

        temp_result = pd.DataFrame([None] * len(self.X.columns), index=self.X.columns).T

        temp_result.loc[0, result_tpl['variable_name']] = result_tpl['variable_value'].values
        temp_result = temp_result[self.X.columns]
        new_variable_values = self.scaler.inverse_transform(temp_result)

        for i, col in enumerate(temp_result.columns):
            if col in result_tpl['variable_name'].values:
                parsed_val = math.floor(new_variable_values[0][i])
                if dataset_service.kaggle_heart_disease_2020_columns[col]['type'] in ['boolean', 'category']:
                    parsed_val = self.get_first_key_by_value(
                        dataset_service.kaggle_heart_disease_2020_columns[col]['values'], parsed_val)

                readable_varname = dataset_service.kaggle_heart_disease_2020_columns[col].get('title', col)
                result_tpl.loc[result_tpl['variable_name']==col,'variable']=f'{readable_varname} = {parsed_val}'

        dalex_result.result['variable'] = result_tpl['variable'].values

        end = time.time()
        print(f"{inspect.stack()[0][3]} time: {end - start}")
        return dalex_result

    def denormalize_dalex_dataframe(self, dalex_result, variable):
        dataset_service = DatasetService()
        filtered_df = dalex_result.result[self.X.columns]
        denormalized = self.scaler.inverse_transform(filtered_df)
        dalex_result.result[self.X.columns] = denormalized
        filtered_df[variable] = dalex_result.result['_original_']
        denormalized_original = self.scaler.inverse_transform(filtered_df)
        dalex_result.result['_original_'] = denormalized_original[:, self.X.columns.get_loc(variable)]
        readable_varnames = []
        for varname in dalex_result.result['variable']:
            readable_varnames.append(
                dataset_service.kaggle_heart_disease_2020_columns[varname]['title'] if 'title' in
                                                                                       dataset_service.kaggle_heart_disease_2020_columns[
                                                                                           varname] else varname)

        dalex_result.result['variable'] = readable_varnames
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

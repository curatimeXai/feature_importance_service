import math
import os

import dalex
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
import xgboost
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, log_loss

from src.dataset_service import DatasetService


class XdgHeartDiseaseClassifier:
    def __init__(self, data_path=None, data=None, sample_size=200):
        if data_path is not None:
            self.data = pd.read_csv(data_path)
            self.data = self.data.drop(columns=[self.data.columns[0]])
        if data is not None:
            self.data = data
        self.X = self.data.drop(columns=['HeartDisease'])
        self.y = self.data['HeartDisease']
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.X_normalized = self.scaler.fit_transform(self.X)
        self.X_train, self.X_temp, self.y_train, self.y_temp = train_test_split(self.X_normalized, self.y,
                                                                                test_size=0.2, random_state=42)
        self.X_val, self.X_test, self.y_val, self.y_test = train_test_split(self.X_temp, self.y_temp, test_size=0.5,
                                                                            random_state=42)
        self.model = None
        self.X_sample = shap.utils.sample(self.X, sample_size)
        self.explainer = None
        self.dalex_explainer = None

    def train(self, epochs=1, increments=-1):
        accuracies = []
        for i in range(epochs):
            if increments == -1:
                self.model.fit(self.X_train, self.y_train)
                accuracies.append(accuracy_score(self.y_val, self.model.predict(self.X_val)))
                continue

            for j in range(0, len(self.X_train), increments):
                end_index = min(j + increments, len(self.X_train))
                X_batch = self.X_train[j:end_index]
                y_batch = self.y_train[j:end_index]
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

    def load_model(self, model_path=None, model=SVC(kernel='poly')):
        if model_path is not None and os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            self.model = xgboost.XGBClassifier()

    def model_is_saved(self, model_path):
        return os.path.exists(model_path)

    def load_explainer(self, explainer_path=None):
        if explainer_path is not None and os.path.exists(explainer_path):
            self.explainer = joblib.load(explainer_path)
        else:
            self.explainer = shap.Explainer(self.model.predict, self.X_sample)

    def load_dalex_explainer(self, explainer_path=None):
        if explainer_path is not None and os.path.exists(explainer_path):
            with open(explainer_path, 'rb') as fd:
                self.dalex_explainer = dalex.Explainer.load(fd)
        else:
            self.dalex_explainer = dalex.Explainer(self.model, self.X_train, self.y_train)

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

    def save_model(self, filename="models/example_model.pkl"):
        joblib.dump(self.model, filename)

    def save_explainer(self, filename="models/example_explainer.pkl"):
        joblib.dump(self.explainer, filename)

    def save_dalex_explainer(self, filename="models/example_explainer.pkl"):
        with open(filename, 'wb') as fd:
            self.dalex_explainer.dump(fd)

    def denormalize_dalex_result(self, dalex_result):
        dataset_service=DatasetService()
        result_tpl = np.array([dalex_result.result['variable_name'], dalex_result.result['variable_value'],
                               dalex_result.result['variable']]).T
        temp_result = pd.DataFrame(columns=self.X.columns)
        old_result = [0]*len(self.X.columns)
        for i, col in enumerate(self.X.columns):
            for var_name, var_value, variable in result_tpl:
                if col == var_name:
                    old_result[i] = var_value

        temp_result.loc[len(temp_result.index)] = old_result
        new_variable_values = self.scaler.inverse_transform(temp_result)

        for i, col in enumerate(self.X.columns):
            for j, (var_name, var_value, variable) in enumerate(result_tpl):
                if col == var_name:
                    parsed_val = math.floor(new_variable_values[0][i])
                    if dataset_service.columns_2020[var_name]['type'] in ['boolean','category']:
                        parsed_val = self.get_first_key_by_value(dataset_service.columns_2020[var_name]['values'],
                                                               parsed_val)

                    result_tpl[j, 2] = f'{var_name} = {parsed_val}'

        dalex_result.result['variable'] = result_tpl[:, 2]
        return dalex_result

    def denormalize_dalex_dataframe(self, dalex_result,variable):
        filtered_df=dalex_result.result[self.X.columns]
        denormalized=self.scaler.inverse_transform(filtered_df)
        dalex_result.result[self.X.columns]=denormalized
        filtered_df[variable]=dalex_result.result['_original_']
        denormalized_original=self.scaler.inverse_transform(filtered_df)
        dalex_result.result['_original_']=denormalized_original[:,self.X.columns.get_loc(variable)]
        return dalex_result

    def get_first_key_by_value(self, d, target_value):
        for key, value in d.items():
            if value == target_value:
                return key
        return None

import os

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import shap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score


class HeartDiseaseClassifier:
    def __init__(self, data_path, sample_size=200):
        self.data = pd.read_csv(data_path)
        self.X = self.data.drop(columns=['HeartDisease', self.data.columns[0]])
        self.y = self.data['HeartDisease']
        self.scaler = StandardScaler()
        self.X_normalized = self.scaler.fit_transform(self.X.values)
        self.X_train, self.X_temp, self.y_train, self.y_temp = train_test_split(self.X_normalized, self.y,
                                                                                test_size=0.2, random_state=42)
        self.X_val, self.X_test, self.y_val, self.y_test = train_test_split(self.X_temp, self.y_temp, test_size=0.5,
                                                                            random_state=42)
        self.model = None
        self.X_sample = shap.utils.sample(self.X.values, sample_size)
        self.explainer = None

    def train(self, check_interval=100):
        accuracies = []
        for i in range(0, len(self.X_train), check_interval):
            end_index = min(i + check_interval, len(self.X_train))
            X_batch = self.X_train[i:end_index]
            y_batch = self.y_train[i:end_index]
            self.model.fit(X_batch, y_batch)
            if i % check_interval == 0:
                y_pred_val = self.model.predict(self.X_val)
                accuracy = accuracy_score(self.y_val, y_pred_val)
                accuracies.append(accuracy)

        return accuracies

    def test(self):
        y_pred_test = self.model.predict(self.X_test)
        test_accuracy = accuracy_score(self.y_test, y_pred_test)
        return test_accuracy

    def plot_accuracy(self, accuracies):
        plt.plot(range(len(accuracies)), accuracies)
        plt.show()

    def load_model(self, model_path=None,model=SVC(kernel='poly')):
        if model_path is not None and os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            self.model = model

    def model_is_saved(self, model_path):
        return os.path.exists(model_path)

    def load_explainer(self, explainer_path=None):
        if explainer_path is not None and os.path.exists(explainer_path):
            self.explainer = joblib.load(explainer_path)
        else:
            self.explainer = shap.KernelExplainer(self.model.predict, self.X_sample)

    def shap_analysis(self, sample_ind=20):
        shap_values = self.explainer(self.X_test[:200])
        feature_index = self.X.columns.get_loc("AgeCategory")
        shap.partial_dependence_plot(
            feature_index, self.model.predict, self.X_sample, model_expected_value=True,
            feature_expected_value=True, ice=False,
            shap_values=shap_values[sample_ind:sample_ind+1,:],
        )

        interaction_index = self.X.columns.get_loc("Sex")
        shap.dependence_plot(
            feature_index, shap_values.values, self.X_test[:200],
            interaction_index=interaction_index,
            feature_names=self.X.columns)

        shap.plots.waterfall(shap_values[0])

        shap.plots.beeswarm(shap_values)

        shap.summary_plot(shap_values, self.X_test[:200], plot_type="bar")

    # def shap_analysis_2(self, sample_ind=20):
    #     shap_values = self.explainer(self.X_test[:100])
    #     feature_index = self.X.columns.get_loc("AgeCategory")
    #     interaction_index = self.X.columns.get_loc("Sex")
    #     shap.dependence_plot(
    #         feature_index, shap_values.values, self.X_test[:100],
    #         interaction_index=interaction_index,
    #         feature_names=['AgeCategory','Sex'])

    def save_model(self, filename="models/example_model.pkl"):
        joblib.dump(self.model, filename)

    def save_explainer(self, filename="models/example_explainer.pkl"):
        joblib.dump(self.explainer, filename)
# Example usage:
model=SVC(kernel='poly')
model_path= "/src/models/svm_model.pkl"
explainer_path= "/src/explainers/svm_explainer.pkl"
data_path= '/datasets/dataset_2020_2022/2020/heart_2020_cleaned_numerical.csv'
do_train=True
classifier = HeartDiseaseClassifier(data_path,
                                    sample_size=100)
classifier.load_model(model_path,model)
if do_train or not classifier.model_is_saved(model_path):
    accuracies = classifier.train()
    classifier.save_model(model_path)
    classifier.plot_accuracy(accuracies)
classifier.load_explainer(explainer_path=explainer_path)
# classifier.save_explainer(explainer_path)
test_accuracy = classifier.test()
print("Final Testing Accuracy:", test_accuracy)
classifier.shap_analysis()
# classifier.shap_analysis_2()

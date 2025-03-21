import base64

import numpy as np
import pandas as pd
import plotly.io as pio

from src.helpers import get_trained_models_path, get_explainers_path
from src.models.heart_disease_model import HeartDiseaseClassifier
from src.services.dataset_service import DatasetService


MODEL_PATH = get_trained_models_path("dnn_model.pkl")
EXPLAINER_PATH = get_explainers_path("dnn_explainer.pkl")

def dnn_accuracy():
    dataset_service = DatasetService()
    classifier = HeartDiseaseClassifier(data=dataset_service.kaggle_heart_disease_2020)
    classifier.load_model(MODEL_PATH)
    return classifier.test_accuracy()


def dnn_variable_importance_image():
    dataset_service = DatasetService()
    classifier = HeartDiseaseClassifier(data=dataset_service.kaggle_heart_disease_2020)
    classifier.load_model(MODEL_PATH)
    classifier.load_dalex_explainer(EXPLAINER_PATH)
    vi = classifier.dalex_explainer.model_parts()
    vi_plotly = vi.plot(show=False)
    image_bytes = pio.to_image(vi_plotly, format='png')
    plot_url = base64.b64encode(image_bytes).decode('utf-8')
    return 'data:image/png;base64,' + plot_url


def dnn_variable_importance():
    dataset_service = DatasetService()
    classifier = HeartDiseaseClassifier(data=dataset_service.kaggle_heart_disease_2020)
    classifier.load_model(MODEL_PATH)
    classifier.load_dalex_explainer(EXPLAINER_PATH)
    vi = classifier.dalex_explainer.model_parts()
    renamed_variables_vi = classifier.rename_variables(vi)
    return renamed_variables_vi.plot(show=False, title="Probability by Value (Aggregated)", max_vars=16).to_json()


def dnn_model_performance():
    dataset_service = DatasetService()
    classifier = HeartDiseaseClassifier(data=dataset_service.kaggle_heart_disease_2020)
    classifier.load_model(MODEL_PATH)
    classifier.load_dalex_explainer(EXPLAINER_PATH)
    mp = classifier.dalex_explainer.model_performance(model_type='classification')
    return mp.plot(geom="roc", show=False).to_json()


def dnn_pdp(variable):
    dataset_service = DatasetService()
    classifier = HeartDiseaseClassifier(data=dataset_service.kaggle_heart_disease_2020)
    classifier.load_model(MODEL_PATH)
    classifier.load_dalex_explainer(EXPLAINER_PATH)
    pdp_num = classifier.dalex_explainer.model_profile(type='partial', label="pdp", variables=[variable])
    denormalized_pdp = classifier.denormalize_x_y(pdp_num, variable)
    return denormalized_pdp.plot(show=False, title="Probability by Value (Aggregated)").to_json()


def dnn_break_down(input):
    dataset_service = DatasetService()
    classifier = HeartDiseaseClassifier(data=dataset_service.kaggle_heart_disease_2020)
    inputDf = pd.DataFrame(columns=classifier.X.columns)
    inputDf.loc[len(inputDf.index)] = dataset_service.transform_2020_input(input)
    scaled_input = classifier.scaler.transform(inputDf)
    classifier.load_model(MODEL_PATH)
    classifier.load_dalex_explainer(EXPLAINER_PATH)
    bd_normal = classifier.dalex_explainer.predict_parts(scaled_input, N=100, type='break_down')
    bd_denormalized = classifier.denormalize_bd_result(bd_normal,input)
    # bd_normal = classifier.dalex_explainer.predict_parts(classifier.X_test_denormalized.iloc[0], type='break_down', label=classifier.y_test_denormalized.iloc[0])
    # bd_interactions = classifier.dalex_explainer.predict_parts(classifier.X_test[0], type='break_down_interactions',
    #                                     label=classifier.y_test[0])
    # return bd_normal.plot(bd_interactions, show=False).to_json()
    return bd_denormalized.plot(show=False, vcolors=["#371ea3", "#f05a71", "#8bdcbe"], title='Risk Factors (Accumulative)',max_vars=16).to_json()


def dnn_overview(input):
    dataset_service = DatasetService()
    classifier = HeartDiseaseClassifier(data=dataset_service.kaggle_heart_disease_2020)
    inputDf = pd.DataFrame(columns=classifier.X.columns)
    inputDf.loc[len(inputDf.index)] = dataset_service.transform_2020_input(input)
    scaled_input = classifier.scaler.transform(inputDf)
    classifier.load_model(MODEL_PATH)
    classifier.load_dalex_explainer(EXPLAINER_PATH)
    bd_normal = classifier.dalex_explainer.predict_parts(scaled_input, N=100, type='break_down')
    bd_denormalized = classifier.denormalize_bd_result(bd_normal,input)
    bd_denormalized.result['contribution'] = bd_denormalized.result['contribution'].apply(lambda x: x * 100)
    overview = np.array([bd_denormalized.result['variable'], bd_denormalized.result['contribution']]).T
    filtered_overview = overview[overview[:, 0] != 'intercept']
    prediction = filtered_overview[filtered_overview[:, 0] == 'prediction']
    features = filtered_overview[filtered_overview[:, 0] != 'prediction']
    sorted_features = features[features[:, 1].argsort()]
    return {'prediction': prediction[0, 1], 'features': sorted_features.tolist()}


def dnn_shapley(input):
    dataset_service = DatasetService()
    classifier = HeartDiseaseClassifier(data=dataset_service.kaggle_heart_disease_2020)
    inputDf = pd.DataFrame(columns=classifier.X.columns)
    inputDf.loc[len(inputDf.index)] = dataset_service.transform_2020_input(input)
    scaled_input = classifier.scaler.transform(inputDf)
    classifier.load_model(MODEL_PATH)
    classifier.load_dalex_explainer(EXPLAINER_PATH)
    shapl = classifier.dalex_explainer.predict_parts(scaled_input, N=100, type='shap', B=10)
    shapl_denormalized = classifier.denormalize_shapley(shapl,input)
    return shapl_denormalized.plot(show=False, vcolors=["#371ea3", "#f05a71", "#8bdcbe"]).to_json()


def dnn_ceteris_parabus(input, variable):
    dataset_service = DatasetService()
    classifier = HeartDiseaseClassifier(data=dataset_service.kaggle_heart_disease_2020)
    inputDf = pd.DataFrame(columns=classifier.X.columns)
    inputDf.loc[len(inputDf.index)] = dataset_service.transform_2020_input(input)
    scaled_input = classifier.scaler.transform(inputDf)
    classifier.load_model(MODEL_PATH)
    classifier.load_dalex_explainer(EXPLAINER_PATH)
    cp = classifier.dalex_explainer.predict_profile(scaled_input, variables=[variable])
    cp_denormalized = classifier.denormalize_dalex_dataframe(cp, variable)
    return cp_denormalized.plot(
        show=False,
        title=f"Risk Factor {dataset_service.kaggle_heart_disease_2020_columns[variable].get('title', variable)} by value").to_json()
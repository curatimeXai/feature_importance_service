import base64
import json
from io import StringIO

import plotly
import plotly.io as pio

from matplotlib import pyplot as plt
from torch._C._return_types import topk

from src.xdg_model import XdgHeartDiseaseClassifier

DATA_PATH='/home/alex/UniProjects/BachelorXAI/datasets/dataset_2020_2022/2020/heart_2020_cleaned_numerical.csv'
MODEL_PATH= "/home/alex/UniProjects/BachelorXAI/src/models/xdg_model.pkl"
EXPLAINER_PATH= "/home/alex/UniProjects/BachelorXAI/src/explainers/xdg_explainer.pkl"
def xdg_accuracy():
    classifier = XdgHeartDiseaseClassifier(DATA_PATH,
                                           sample_size=100)
    classifier.load_model(MODEL_PATH)
    return classifier.test_accuracy()

def xdg_variable_importance_image():
    classifier = XdgHeartDiseaseClassifier(DATA_PATH, sample_size=100)
    classifier.load_model(MODEL_PATH)
    classifier.load_dalex_explainer(EXPLAINER_PATH)
    vi = classifier.dalex_explainer.model_parts()
    vi_plotly=vi.plot(show=False)
    image_bytes=pio.to_image(vi_plotly,format='png')
    plot_url = base64.b64encode(image_bytes).decode('utf-8')
    return 'data:image/png;base64,'+plot_url

def xdg_variable_importance():
    classifier = XdgHeartDiseaseClassifier(DATA_PATH, sample_size=100)
    classifier.load_model(MODEL_PATH)
    classifier.load_dalex_explainer(EXPLAINER_PATH)
    vi = classifier.dalex_explainer.model_parts()
    return vi.plot(show=False).to_json()

def xdg_break_down():
    classifier = XdgHeartDiseaseClassifier(DATA_PATH, sample_size=100)
    classifier.load_model(MODEL_PATH)
    classifier.load_dalex_explainer(EXPLAINER_PATH)
    bd_normal = classifier.dalex_explainer.predict_parts(classifier.X_test[0], type='break_down', label=classifier.y_test[0])
    bd_interactions = classifier.dalex_explainer.predict_parts(classifier.X_test[0], type='break_down_interactions',
                                        label=classifier.y_test[0])
    return bd_normal.plot(bd_interactions, show=False).to_json()

def xdg_shapley():
    classifier = XdgHeartDiseaseClassifier(DATA_PATH, sample_size=100)
    classifier.load_model(MODEL_PATH)
    classifier.load_dalex_explainer(EXPLAINER_PATH)
    shapl = classifier.dalex_explainer.predict_parts(classifier.X_test[0], type='shap', B=10, label=classifier.y_test[0])
    return shapl.plot(show=False).to_json()

def xdg_ceteris_parabus():
    classifier = XdgHeartDiseaseClassifier(DATA_PATH, sample_size=100)
    classifier.load_model(MODEL_PATH)
    classifier.load_dalex_explainer(EXPLAINER_PATH)
    cp = classifier.dalex_explainer.predict_profile(classifier.X_test[0], label=classifier.y_test[0])
    return cp.plot(show=False).to_json()

def xdg_model_performance():
    classifier = XdgHeartDiseaseClassifier(DATA_PATH, sample_size=100)
    classifier.load_model(MODEL_PATH)
    classifier.load_dalex_explainer(EXPLAINER_PATH)
    mp = classifier.dalex_explainer.model_performance(model_type='classification')
    return mp.plot(geom="roc",show=False).to_json()
def xdg_pdp():
    classifier = XdgHeartDiseaseClassifier(DATA_PATH, sample_size=100)
    classifier.load_model(MODEL_PATH)
    classifier.load_dalex_explainer(EXPLAINER_PATH)
    pdp_num = classifier.dalex_explainer.model_profile(type='partial', label="pdp")
    return pdp_num.plot(show=False).to_json()
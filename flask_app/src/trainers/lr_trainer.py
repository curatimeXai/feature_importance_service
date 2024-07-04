import matplotlib.pyplot as plt
import pandas as pd
import xgboost
from dotenv import load_dotenv
from sklearn.linear_model import LogisticRegression

from src.helpers import get_trained_models_path, get_explainers_path
from src.models.heart_disease_model import HeartDiseaseClassifier
from src.services.dataset_service import DatasetService
load_dotenv()

dataset_service=DatasetService()
data_path = dataset_service.datasets_paths['processed_kaggle_2020']

MODEL_PATH = get_trained_models_path("lr_model2.pkl")
EXPLAINER_PATH = get_explainers_path("lr_explainer2.pkl")

do_train = True
classifier = HeartDiseaseClassifier(data_path, model=LogisticRegression())
accuracies = classifier.train()
classifier.save_model(MODEL_PATH)
if len(accuracies) > 1:
    classifier.plot_accuracy(accuracies)
    plt.show()

classifier.load_dalex_explainer(explainer_path=EXPLAINER_PATH)
classifier.save_dalex_explainer(EXPLAINER_PATH)
test_accuracy = classifier.test_accuracy()
log_likelihood = classifier.log_likelihood()
print(f"Final Testing Acc: {test_accuracy} Likelihood: {log_likelihood}")

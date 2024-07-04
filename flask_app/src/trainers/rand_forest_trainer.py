import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv
from keras import Sequential
from keras.layers import Dense
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from src.helpers import get_trained_models_path, get_explainers_path
from src.models.heart_disease_model import HeartDiseaseClassifier
from src.services.dataset_service import DatasetService
load_dotenv()

dataset_service=DatasetService()
data_path = dataset_service.datasets_paths['processed_kaggle_2020']

MODEL_PATH = get_trained_models_path("rand_forest_model2.pkl")
EXPLAINER_PATH = get_explainers_path("rand_forest_explainer2.pkl")

do_train=True

classifier = HeartDiseaseClassifier(data_path,
                                    model=RandomForestClassifier(n_estimators=25, criterion='gini', random_state=42, max_depth=6))
X_train_with_headers=pd.DataFrame(classifier.X_train, columns=classifier.X.columns)
accuracies = classifier.train(X=X_train_with_headers)
classifier.save_model(MODEL_PATH)
classifier.plot_accuracy(accuracies)
if len(accuracies) > 1:
    plt.show()

classifier.load_dalex_explainer(explainer_path=EXPLAINER_PATH)
classifier.save_dalex_explainer(EXPLAINER_PATH)
test_accuracy = classifier.test_accuracy()
log_likelihood = classifier.log_likelihood()
print(f"Final Testing Acc: {test_accuracy} Likelihood: {log_likelihood}")

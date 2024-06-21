import matplotlib.pyplot as plt
import pandas as pd
import xgboost
from sklearn.linear_model import LogisticRegression

from src.helpers import get_trained_models_path, get_explainers_path
from src.models.heart_disease_model import HeartDiseaseClassifier
from src.services.dataset_service import DatasetService

dataset_service=DatasetService()
data_path = dataset_service.datasets_paths[1]

MODEL_PATH = get_trained_models_path("lr_model2.pkl")
EXPLAINER_PATH = get_explainers_path("lr_explainer2.pkl")

do_train = True
classifier = HeartDiseaseClassifier(data_path, model=LogisticRegression())
classifier.load_model(MODEL_PATH)
if do_train or not classifier.model_is_saved(MODEL_PATH):
    accuracies = classifier.train()
    classifier.save_model(MODEL_PATH)
    if len(accuracies) > 1:
        classifier.plot_accuracy(accuracies)
        plt.show()

classifier.load_dalex_explainer(explainer_path=EXPLAINER_PATH)
classifier.save_dalex_explainer(EXPLAINER_PATH)
# inputDf = pd.DataFrame(columns=classifier.X.columns)
# inputDf.loc[len(inputDf.index)] = classifier.X.iloc[141, :].tolist()
# scaled_input = classifier.scaler.transform(inputDf)
# classifier.dalex_explainer.predict_parts(scaled_input, type='break_down').plot()
test_accuracy = classifier.test_accuracy()
log_likelihood = classifier.log_likelihood()
print(f"Final Testing Acc: {test_accuracy} Likelihood: {log_likelihood}")

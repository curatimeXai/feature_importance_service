import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv
from sklearn.svm import SVC

from src.helpers import get_trained_models_path, get_explainers_path
from src.models.heart_disease_model import HeartDiseaseClassifier
from src.services.dataset_service import DatasetService
load_dotenv()

dataset_service=DatasetService()
data_path = dataset_service.datasets_paths[1]
MODEL_PATH = get_trained_models_path("svm_model.pkl")
EXPLAINER_PATH = get_explainers_path("svm_explainer.pkl")
do_train=True
classifier = HeartDiseaseClassifier(data_path,
                                    data_sample=50000,
                                    model=SVC(kernel='linear',probability=True))
if do_train or not classifier.model_is_saved(MODEL_PATH):
    print('start training')
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

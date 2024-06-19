import matplotlib.pyplot as plt
import pandas as pd
import xgboost
from sklearn.linear_model import LogisticRegression

from src.models.heart_disease_model import HeartDiseaseClassifier
from src.services.dataset_service import DatasetService

dataset_service=DatasetService()
data_path = dataset_service.datasets_paths[1]
model_path= "/home/alex/UniProjects/BachelorXAI/flask_app/src/store/trained_models/lr_model2.pkl"
explainer_path= "/home/alex/UniProjects/BachelorXAI/flask_app/src/store/explainers/lr_explainer2.pkl"
do_train = True
classifier = HeartDiseaseClassifier(data_path, model=LogisticRegression())
classifier.load_model(model_path)
if do_train or not classifier.model_is_saved(model_path):
    accuracies = classifier.train()
    classifier.save_model(model_path)
    if len(accuracies) > 1:
        classifier.plot_accuracy(accuracies)
        plt.show()

classifier.load_dalex_explainer(explainer_path=explainer_path)
classifier.save_dalex_explainer(explainer_path)
# inputDf = pd.DataFrame(columns=classifier.X.columns)
# inputDf.loc[len(inputDf.index)] = classifier.X.iloc[141, :].tolist()
# scaled_input = classifier.scaler.transform(inputDf)
# classifier.dalex_explainer.predict_parts(scaled_input, type='break_down').plot()
test_accuracy = classifier.test_accuracy()
log_likelihood = classifier.log_likelihood()
print(f"Final Testing Acc: {test_accuracy} Likelihood: {log_likelihood}")

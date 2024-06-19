import matplotlib.pyplot as plt
import pandas as pd
from sklearn.svm import SVC

from src.models.heart_disease_model import HeartDiseaseClassifier
from src.services.dataset_service import DatasetService

dataset_service=DatasetService()
data_path = dataset_service.datasets_paths[1]
model_path= "/home/alex/UniProjects/BachelorXAI/flask_app/src/store/trained_models/svm_model2.pkl"
explainer_path= "/home/alex/UniProjects/BachelorXAI/flask_app/src/store/explainers/svm_explainer2.pkl"
do_train=True
classifier = HeartDiseaseClassifier(data_path,
                                    data_sample=100000,
                                    model=SVC(kernel='linear',probability=True))
if do_train or not classifier.model_is_saved(model_path):
    print('start training')
    X_train_with_headers=pd.DataFrame(classifier.X_train, columns=classifier.X.columns)
    accuracies = classifier.train(X=X_train_with_headers)
    classifier.save_model(model_path)
    classifier.plot_accuracy(accuracies)
    if len(accuracies) > 1:
        plt.show()

classifier.load_dalex_explainer(explainer_path=explainer_path)
classifier.save_dalex_explainer(explainer_path)
test_accuracy = classifier.test_accuracy()
log_likelihood = classifier.log_likelihood()
print(f"Final Testing Acc: {test_accuracy} Likelihood: {log_likelihood}")

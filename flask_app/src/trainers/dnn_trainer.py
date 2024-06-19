import matplotlib.pyplot as plt
import pandas as pd
from keras import Sequential
from keras.layers import Dense
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from src.models.heart_disease_model import HeartDiseaseClassifier
from src.services.dataset_service import DatasetService

dataset_service=DatasetService()
model_path = "/home/alex/UniProjects/BachelorXAI/flask_app/src/store/trained_models/dnn_model2.pkl"
explainer_path = "/home/alex/UniProjects/BachelorXAI/flask_app/src/store/explainers/dnn_explainer2.pkl"
data_path = dataset_service.datasets_paths[1]
do_train = False

model = Sequential()
model.add(Dense(64, input_dim=16, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

classifier = HeartDiseaseClassifier(data_path,
                                    model=model)
classifier.load_model(model_path)
if do_train or not classifier.model_is_saved(model_path):
    print('start training')
    accuracies = classifier.train(epochs=3, batch_size=32, is_dnn=True)
    classifier.save_model(model_path)
    classifier.plot_accuracy(accuracies)
    if len(accuracies) > 1:
        plt.show()

classifier.load_dalex_explainer(explainer_path=explainer_path)
classifier.save_dalex_explainer(explainer_path)

loss, accuracy = classifier.model.evaluate(classifier.X_test, classifier.y_test)
print(f"Final Testing Acc: {accuracy} Likelihood: {loss}")
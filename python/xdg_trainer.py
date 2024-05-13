import matplotlib.pyplot as plt

from src.xdg_model import XdgHeartDiseaseClassifier

# Example usage:
# model=SVC(kernel='poly')
model_path= "/home/alex/UniProjects/BachelorXAI/src/models/xdg_model.pkl"
# model_path=None
explainer_path= "/home/alex/UniProjects/BachelorXAI/src/explainers/xdg_explainer.pkl"
# explainer_path=None
data_path= '/home/alex/UniProjects/BachelorXAI/datasets/dataset_2020_2022/2020/heart_2020_cleaned_numerical.csv'
do_train=True
classifier = XdgHeartDiseaseClassifier(data_path,
                                       sample_size=100)
classifier.load_model(model_path)
if do_train or not classifier.model_is_saved(model_path):
    accuracies = classifier.train()
    classifier.save_model(model_path)
    classifier.plot_accuracy(accuracies)
    plt.show()

classifier.load_explainer(explainer_path=explainer_path)
classifier.save_explainer(explainer_path)
test_accuracy = classifier.test_accuracy()
log_likelihood = classifier.log_likelihood()
print(f"Final Testing Acc: {test_accuracy} Likelihood: {log_likelihood}")

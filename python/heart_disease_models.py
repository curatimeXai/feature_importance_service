import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import classification_report
import colorama
from colorama import Back
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
import shap
import sklearn

main_dataset = pd.read_csv('../datasets/dataset_old/heart.csv')
main_dataset = pd.DataFrame(main_dataset)

print(main_dataset.shape)
'''
Age : Age of the patient
Sex : Sex of the patient
exang: exercise induced angina (1 = yes; 0 = no)
caa: number of major vessels (0-4)
cp : Chest Pain type chest pain type Value 1: typical angina Value 2: atypical angina Value 3: non-anginal pain Value 4: asymptomatic
trtbps : resting blood pressure (in mm Hg)
chol : cholestoral in mg/dl fetched via BMI sensor
fbs : (fasting blood sugar > 120 mg/dl) (1 = true; 0 = false)
rest_ecg : resting electrocardiographic results Value 0: normal Value 1: having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV) Value 2: showing probable or definite left ventricular hypertrophy by Estes' criteria
thalach : maximum heart rate achieved
ST_Slope: the slope of the peak exercise ST segment [Up: upsloping, Flat: flat, Down: downsloping]
target : 0= less chance of heart attack 1= more chance of heart attack
'''
main_dataset.head(10).style.set_properties(**{'background-color': '#F6E7E8',
                           'color': 'black',
                           'border-color': 'black'})


def describe(dataset):
    variables = []
    dtypes = []
    count = []
    unique = []
    missing = []
    min_ = []
    max_ = []

    for item in dataset.columns:
        variables.append(item)
        dtypes.append(dataset[item].dtype)
        count.append(len(dataset[item]))
        unique.append(len(dataset[item].unique()))
        missing.append(dataset[item].isna().sum())

        if dataset[item].dtypes == 'float64' or dataset[item].dtypes == 'int64':
            min_.append(dataset[item].min())
            max_.append(dataset[item].max())
        else:
            min_.append('Str')
            max_.append('Str')

    output = pd.DataFrame({
        'variable': variables,
        'dtype': dtypes,
        'count': count,
        'unique': unique,
        'missing value': missing,
        'Min': min_,
        'Max': max_
    })

    return output



print(describe(main_dataset))

Features = main_dataset.drop(columns='target')
Features = pd.DataFrame(Features)

scaler = MinMaxScaler()
Norm_data = scaler.fit_transform(Features)
Norm_df = pd.DataFrame(Norm_data, columns= Features.columns)
Norm_df.head(10).style.set_properties(**{'background-color': '#F6E7E8',
                           'color': 'black',
                           'border-color': 'black'})

X = Norm_df#This dataframe is created for features
y = main_dataset['target'].values.reshape(-1,1)

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2, random_state=40)

#models
'''
SVC with Diff C and diff kernel
KNeighbors range(2,20) p=1 & p=2
DecisionTreeClassifier with variable depth
RandomForestClassifier with variable estimators
'''

def plot_acc(x,train_acc,test_acc,title='Acc'):
    plt.xticks(x)
    plt.title(title)
    plt.plot(x,train_acc,label='Train Accuracy')
    plt.plot(x,test_acc,label='Test Accuracy')
    plt.legend()
    plt.show()

def calculate_ice(knn_model):
    # 200 instances for use as the background distribution INSTEAD of 100 in the docs
    X200 = shap.utils.sample(X, 200)

    # compute the SHAP values for the linear model
    explainer = shap.Explainer(knn_model.predict, X200)
    shap_values = explainer(X)

    # make a standard partial dependence plot
    sample_ind = 20
    # use "HouseAge" instead of "MedInc", as it is less gaussian
    shap.partial_dependence_plot(
        "age", knn_model.predict, X200, model_expected_value=True,
        feature_expected_value=True, ice=True,
        shap_values=shap_values[sample_ind:sample_ind + 1, :],
    )

knn_models = []
def knn_train(power=1):
    training_acc = []
    test_acc = []

    range_k = range(2,20)

    for number_k in range_k:
        knn = KNeighborsClassifier(n_neighbors = number_k, p=power)
        knn.fit (X_train, y_train.ravel())
        knn_models.append(knn)
        training_acc.append(knn.score(X_train,y_train))
        test_acc.append(knn.score(X_test, y_test))

    return range_k,training_acc,test_acc



ks_1,knn_train_acc1,knn_test_acc1=knn_train(power=1)

best_model_index=np.argmax(knn_test_acc1)
knn_model=knn_models[best_model_index]
calculate_ice(knn_model)

plot_acc(ks_1,knn_train_acc1,knn_test_acc1,'KNN power 1')
ks_2,knn_train_acc2,knn_test_acc2=knn_train(power=2)
plot_acc(ks_2,knn_train_acc2,knn_test_acc2,'KNN power 2')



def svc_train(kernel='linear'):
    training_acc = []
    test_acc = []
    C = [0.5,0.6,0.7,0.8,0.9,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,
        26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50]
    #Kernel = {'linear', 'poly', 'rbf', 'sigmoid'}

    for C_ in C:
        SVM = SVC(C= C_, kernel= 'sigmoid')
        SVM.fit (X_train, y_train.ravel())
        training_acc.append(SVM.score(X_train,y_train))
        test_acc.append(SVM.score(X_test, y_test))

    return C,training_acc,test_acc

Cs_1,svc_train_acc1,svc_test_acc1=svc_train(kernel='linear')
plot_acc(Cs_1,svc_train_acc1,svc_test_acc1,'SVM linear')
Cs_2,svc_train_acc2,svc_test_acc2=svc_train(kernel='poly')
plot_acc(Cs_2,svc_train_acc2,svc_test_acc2,'SVM poly')
Cs_3,svc_train_acc3,svc_test_acc3=svc_train(kernel='rbf')
plot_acc(Cs_3,svc_train_acc3,svc_test_acc3,'SVM rbf')
Cs_4,svc_train_acc4,svc_test_acc4=svc_train(kernel='sigmoid')
plot_acc(Cs_4,svc_train_acc4,svc_test_acc4,'SVM sigmoid')

def  decision_tree_train(criterion='gini'):
    training_acc = []
    test_acc = []
    max_depth = range(1,20)
    #Criterion = gini, entropy, log_loss

    for depth in max_depth:
        DT = DecisionTreeClassifier(max_depth=depth, criterion=criterion, random_state=4)
        DT.fit(X_train, y_train.ravel())
        training_acc.append(DT.score(X_train, y_train))
        test_acc.append(DT.score(X_test, y_test))

    return max_depth, training_acc, test_acc

depths_1,decision_tree_train_acc1,decision_tree_test_acc1=decision_tree_train(criterion='gini')
plot_acc(depths_1,decision_tree_train_acc1,decision_tree_test_acc1,'Decision Tree gini')
depths_2,decision_tree_train_acc2,decision_tree_test_acc2=decision_tree_train(criterion='entropy')
plot_acc(depths_2,decision_tree_train_acc2,decision_tree_test_acc2,'Decision Tree entropy')
depths_3,decision_tree_train_acc3,decision_tree_test_acc3=decision_tree_train(criterion='log_loss')
plot_acc(depths_3,decision_tree_train_acc3,decision_tree_test_acc3,'Decision Tree log_loss')

def random_forest_train(criterion='gini'):
    training_acc = []
    test_acc = []
    n_estimators = range(5, 100)
    # Criterion = gini, entropy

    for estimator in n_estimators:
        RF = RandomForestClassifier(n_estimators=estimator, criterion=criterion, random_state=40, max_depth=2)
        RF.fit(X_train, y_train.ravel())
        training_acc.append(RF.score(X_train, y_train))
        test_acc.append(RF.score(X_test, y_test))

    return n_estimators, training_acc, test_acc

estimators_1,random_forest_train_acc1,random_forest_test_acc1=random_forest_train(criterion='gini')
plot_acc(estimators_1,random_forest_train_acc1,random_forest_test_acc1,'Random Forest gini')
estimators_2,random_forest_train_acc2,random_forest_test_acc2=random_forest_train(criterion='entropy')
plot_acc(estimators_2,random_forest_train_acc2,random_forest_test_acc2,'Random Forest entropy')

trained_models = {
    'knn': {
        'knn_p1': knn_test_acc1,
        'knn_p2': knn_test_acc2,
    },
    'svm': {
        'svc_linear': svc_test_acc1,
        'svc_poly': svc_test_acc2,
        'svc_rbf': svc_test_acc3,
        'svc_sigmoid': svc_test_acc4,
    },
    'decision_tree': {
        'decision_tree_gini': decision_tree_test_acc1,
        'decision_tree_entropy': decision_tree_test_acc2,
        'decision_tree_log_loss': decision_tree_test_acc3,
    },
    'random_forest': {
        'random_forest_gini': random_forest_test_acc1,
        'random_forest_entropy': random_forest_test_acc2,
    },
}

best_models = {
    'knn': {},
    'svm': {},
    'decision_tree': {},
    'random_forest': {},
}
categories=[]
vals=[]
for model, data_types in trained_models.items():
    max_model_acc=0
    max_model_name=''
    for specific_model, data_type in data_types.items():
        if max(data_type)>max_model_acc:
            max_model_acc=max(data_type)
            max_model_name=specific_model
    best_models[model][max_model_name]=max_model_acc
    categories.append(max_model_name)
    vals.append(max_model_acc)

plt.barh(categories,vals)
plt.xlabel('Values')
plt.ylabel('Categories')
plt.title('Horizontal Bar Chart Example')
plt.show()

print(best_models)
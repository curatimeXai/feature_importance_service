library("DALEX")
library("e1071")  # for SVM
heart_csv <- "/datasets/dataset_2020_2022/2020/heart_2020_cleaned_numerical_old.csv"
heart_data <- read.csv(heart_csv)
heart_data <- heart_data[1:10000,]
heart_data<- heart_data[,-1]
smp_size <- floor(0.8 * nrow(heart_data))

## set the seed to make your partition reproducible
set.seed(123)
train_ind <- sample(seq_len(nrow(heart_data)), size = smp_size)

heart_data_train <- heart_data[train_ind, ]
heart_data_test <- heart_data[-train_ind, ]
# heart_data <- heart_data[1:1000,]


for (col in names(heart_data)) {
  print(col)
  print(unique(heart_data[[col]])[1:15])
}

model_svm <- svm(HeartDisease ~ ., data = heart_data_train, probability = TRUE)
heart_data_wo_target <- heart_data_train[, -which(names(heart_data_train) == 'HeartDisease')]

explainer_svm <- explain(model_svm,
                         data = heart_data_wo_target,
                         y = heart_data_train$HeartDisease,
                         label = "SVM Model")
bd<-predict_profile(explainer_svm,new_observation =heart_data_test[1,])
plot(bd)
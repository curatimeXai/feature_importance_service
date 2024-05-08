library("DALEX")
library("e1071")  # for SVM

# Assuming you have your own data stored in a data frame called my_data
# Replace "my_data" with the name of your data frame

# Train SVM model
heart_csv <- "/home/alex/UniProjects/BachelorXAI/python/dataset_old/heart.csv"
heart_data <- read.csv(heart_csv)

model_svm <- svm(target ~ ., data = heart_data, probability = TRUE)
print(names(heart_data))
heart_data_wo_target<-heart_data[, -which(names(heart_data)=='target')]
# Create DALEX explainer
explainer_svm <- explain(model_svm,
                         data = heart_data_wo_target,
                         y = heart_data$target,
                         label = "SVM Model")
saveRDS(explainer_svm, file = "explainer_svm.rds")

library("DALEX")
library("e1071")  # for SVM

heart_csv <- "/home/alex/UniProjects/BachelorXAI/datasets/dataset_2020_2022/2020/heart_2020_cleaned.csv"
heart_data <- read.csv(heart_csv)
# heart_data <- heart_data[1:1000,]


for (col in names(heart_data)) {
  print(col)
  print(unique(heart_data[[col]])[1:15])
}


convert_to_boolean <- function(x) {
  ifelse(x == "Yes", 1,
         ifelse(x == "No", 0, NA))
}

convert_diabetic_to_integer <- function(x) {
  ifelse(x == "Yes", 1,
         ifelse(x == "No", 2,
                ifelse(x == "Yes (during pregnancy)", 3,
                       ifelse(x == "No, borderline diabetes", 4, NA))))
}

convert_sex_to_integer <- function(x) {
  ifelse(x == "Male", 1,
         ifelse(x == "Female", 2, NA))
}

convert_age_to_integer <- function(x) {
  ifelse(
    x == "18-24", 1,
    ifelse(x == "25-29", 2,
           ifelse(x == "30-34", 3,
                  ifelse(x == "35-39", 4,
                         ifelse(x == "40-44", 5,
                                ifelse(x == "45-49", 6,
                                       ifelse(x == "50-54", 7,
                                              ifelse(x == "55-59", 8,
                                                     ifelse(x == "60-64", 9,
                                                            ifelse(x == "65-69", 10,
                                                                   ifelse(x == "70-74", 11,
                                                                          ifelse(x == "75-79", 12,
                                                                                 ifelse(x == "80 or older", 13, NA)))))))))))))
}

convert_race_to_integer <- function(x) {
  ifelse(
    x == "White", 1,
    ifelse(x == "Black", 2,
           ifelse(x == "Asian", 3,
                  ifelse(x == "Hispanic", 4,
                         ifelse(x == "American Indian/Alaskan Native", 5,
                                ifelse(x == "Other", 6, NA))))))
}

convert_general_health_to_integer <- function(x) {
  ifelse(
    x == "Poor", 1,
    ifelse(x == "Fair", 2,
           ifelse(x == "Good", 3,
                  ifelse(x == "Very good", 4,
                         ifelse(x == "Excellent", 5, NA)))))
}

heart_data$HeartDisease <- convert_to_boolean(heart_data$HeartDisease)
heart_data$Smoking <- convert_to_boolean(heart_data$Smoking)
heart_data$AlcoholDrinking <- convert_to_boolean(heart_data$AlcoholDrinking)
heart_data$Stroke <- convert_to_boolean(heart_data$Stroke)
heart_data$DiffWalking <- convert_to_boolean(heart_data$DiffWalking)
heart_data$Sex <- convert_sex_to_integer(heart_data$Sex)
heart_data$AgeCategory <- convert_age_to_integer(heart_data$AgeCategory)
heart_data$Race <- convert_race_to_integer(heart_data$Race)
heart_data$Diabetic <- convert_diabetic_to_integer(heart_data$Diabetic)
heart_data$PhysicalActivity <- convert_to_boolean(heart_data$PhysicalActivity)
heart_data$GenHealth <- convert_general_health_to_integer(heart_data$GenHealth)
heart_data$Asthma <- convert_to_boolean(heart_data$Asthma)
heart_data$KidneyDisease <- convert_to_boolean(heart_data$KidneyDisease)
heart_data$SkinCancer <- convert_to_boolean(heart_data$SkinCancer)

print("heart data prep done")
write.csv(heart_data, "/home/alex/UniProjects/BachelorXAI/datasets/dataset_2020_2022/2020/heart_2020_cleaned_numerical.csv", row.names = TRUE)

# model_svm <- svm(HeartDisease ~ ., data = heart_data, probability = TRUE)
# print(names(heart_data))
# heart_data_wo_target <- heart_data[, -which(names(heart_data) == 'HeartDisease')]
#
# explainer_svm <- explain(model_svm,
#                          data = heart_data_wo_target,
#                          y = heart_data$HeartDisease,
#                          label = "SVM Model")
# saveRDS(explainer_svm, file = "explainer_svm_large.rds")

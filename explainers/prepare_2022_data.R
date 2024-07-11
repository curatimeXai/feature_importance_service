library("DALEX")
library("r2r")
heart_csv <- "/home/alex/UniProjects/BachelorXAI/datasets/dataset_2020_2022/2022/heart_2022_no_nans.csv"
heart_data <- read.csv(heart_csv)
# heart_data <- heart_data[1:1000,]

# TODO replace this with a script in flaskapp
for (col in names(heart_data)) {
  print(col)
  print(unique(heart_data[[col]])[1:15])
}


convert_to_boolean <- function(x) {
  ifelse(x == "Yes", 1,
         ifelse(x == "No", 0, NA))
}

convert_haddiabetes_to_integer <- function(x) {
  ifelse(x == "No", 1,
         ifelse(x == "No, pre-diabetes or borderline diabetes", 2,
                ifelse(x == "Yes, but only during pregnancy (female)", 3,
                       ifelse(x == "Yes", 4, NA))))
}

convert_sex_to_integer <- function(x) {
  ifelse(x == "Male", 1,
         ifelse(x == "Female", 2, NA))
}

convert_age_to_integer <- function(x) {
  ifelse(
    x == "Age 18 to 24", 1,
    ifelse(x == "Age 25 to 29", 2,
           ifelse(x == "Age 30 to 34", 3,
                  ifelse(x == "Age 35 to 39", 4,
                         ifelse(x == "Age 40 to 44", 5,
                                ifelse(x == "Age 45 to 49", 6,
                                       ifelse(x == "Age 50 to 54", 7,
                                              ifelse(x == "Age 55 to 59", 8,
                                                     ifelse(x == "Age 60 to 64", 9,
                                                            ifelse(x == "Age 65 to 69", 10,
                                                                   ifelse(x == "Age 70 to 74", 11,
                                                                          ifelse(x == "Age 75 to 79", 12,
                                                                                 ifelse(x == "Age 80 or older", 13, NA)))))))))))))
}

convert_race_to_integer <- function(x) {
  ifelse(
    x == "White only, Non-Hispanic", 1,
    ifelse(x == "Black only, Non-Hispanic", 2,
           ifelse(x == "Multiracial Non-Hispanic", 3,
                  ifelse(x == "Hispanic", 4,
                         ifelse(x == "Other race only, Non-Hispanic", 5,NA)))))
}

convert_general_health_to_integer <- function(x) {
  ifelse(
    x == "Poor", 1,
    ifelse(x == "Fair", 2,
    ifelse(x == "Good", 3,
    ifelse(x == "Very good", 4,
    ifelse(x == "Excellent", 5, NA)))))
}
convert_tetanuslast10tdap_to_integer <- function(x) {
  ifelse(
    x == "No, did not receive any tetanus shot in the past 10 years", 1,
    ifelse(x == "Yes, received tetanus shot, but not Tdap", 2,
    ifelse(x == "Yes, received tetanus shot but not sure what type", 3,
    ifelse(x == "Yes, received Tdap", 4,NA))))
}
convert_ecigaretteusage_to_integer <- function(x) {
  ifelse(
    x == "Never used e-cigarettes in my entire life", 1,
    ifelse(x == "Use them some days", 2,
    ifelse(x == "Not at all (right now)", 3,
    ifelse(x == "Use them every day", 4,NA))))
}
convert_smokingstatus_to_integer <- function(x) {
  ifelse(
    x == "Never smoked", 1,
    ifelse(x == "Former smoker", 2,
    ifelse(x == "Current smoker - now smokes some days", 3,
    ifelse(x == "Current smoker - now smokes every day", 4,NA))))
}
convert_lastcheckuptime_to_integer <- function(x) {
  ifelse(
    x == "5 or more years ago" , 1,
    ifelse(x == "Within past 2 years (1 year but less than 2 years ago)", 2,
    ifelse(x == "Within past 5 years (2 years but less than 5 years ago)", 3,
    ifelse(x == "Within past year (anytime less than 12 months ago)", 4,NA))))
}
convert_removedteeth_to_integer <- function(x) {
  ifelse(
    x == "None of them", 1,
    ifelse(x == "6 or more, but not all", 2,
    ifelse(x == "1 to 5", 3,
    ifelse(x == "All", 4,NA))))
}
convert_covidpos_to_integer <- function(x) {
  ifelse(
    x == "No", 1,
    ifelse(x == "Yes", 2,
           ifelse(x == "Tested positive using home test without a health professional", 3,NA)))
}

states <- c(
  "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
  "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
  "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
  "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
  "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
  "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
  "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
  "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
  "Washington", "West Virginia", "Wisconsin", "Wyoming"
)
states_map<-hashmap()
states_map[states]<-seq_along(states)

convert_states_to_integer<-function(x){
  if (!is.null(states_map[x])){
    states_map[[x]]
  }else{
    NA
  }
}

heart_data$State <- convert_states_to_integer(heart_data$State)
heart_data$AgeCategory <- convert_age_to_integer(heart_data$AgeCategory)
heart_data$Sex <- convert_sex_to_integer(heart_data$Sex)
heart_data$GeneralHealth <- convert_general_health_to_integer(heart_data$GeneralHealth)
heart_data$LastCheckupTime <- convert_lastcheckuptime_to_integer(heart_data$LastCheckupTime)
heart_data$PhysicalActivities <- convert_to_boolean(heart_data$PhysicalActivities)
heart_data$RemovedTeeth <- convert_removedteeth_to_integer(heart_data$RemovedTeeth)
heart_data$HadHeartAttack <- convert_to_boolean(heart_data$HadHeartAttack)
heart_data$HadAngina <- convert_to_boolean(heart_data$HadAngina)
heart_data$HadStroke <- convert_to_boolean(heart_data$HadStroke)
heart_data$HadAsthma <- convert_to_boolean(heart_data$HadAsthma)
heart_data$HadSkinCancer <- convert_to_boolean(heart_data$HadSkinCancer)
heart_data$HadCOPD <- convert_to_boolean(heart_data$HadCOPD)
heart_data$HadDepressiveDisorder <- convert_to_boolean(heart_data$HadDepressiveDisorder)
heart_data$HadKidneyDisease <- convert_to_boolean(heart_data$HadKidneyDisease)
heart_data$HadArthritis <- convert_to_boolean(heart_data$HadArthritis)
heart_data$HadDiabetes <- convert_haddiabetes_to_integer(heart_data$HadDiabetes)
heart_data$DeafOrHardOfHearing <- convert_to_boolean(heart_data$DeafOrHardOfHearing)
heart_data$BlindOrVisionDifficulty <- convert_to_boolean(heart_data$BlindOrVisionDifficulty)
heart_data$DifficultyConcentrating <- convert_to_boolean(heart_data$DifficultyConcentrating)
heart_data$DifficultyWalking <- convert_to_boolean(heart_data$DifficultyWalking)
heart_data$DifficultyDressingBathing <- convert_to_boolean(heart_data$DifficultyDressingBathing)
heart_data$DifficultyErrands <- convert_to_boolean(heart_data$DifficultyErrands)
heart_data$SmokerStatus <- convert_smokingstatus_to_integer(heart_data$SmokerStatus)
heart_data$ChestScan <- convert_to_boolean(heart_data$ChestScan)
heart_data$ECigaretteUsage <- convert_ecigaretteusage_to_integer(heart_data$ECigaretteUsage)
heart_data$RaceEthnicityCategory <- convert_race_to_integer(heart_data$RaceEthnicityCategory)
heart_data$AlcoholDrinkers <- convert_to_boolean(heart_data$AlcoholDrinkers)
heart_data$HIVTesting <- convert_to_boolean(heart_data$HIVTesting)
heart_data$FluVaxLast12 <- convert_to_boolean(heart_data$FluVaxLast12)
heart_data$PneumoVaxEver <- convert_to_boolean(heart_data$PneumoVaxEver)
heart_data$TetanusLast10Tdap <- convert_tetanuslast10tdap_to_integer(heart_data$TetanusLast10Tdap)
heart_data$HighRiskLastYear <- convert_to_boolean(heart_data$HighRiskLastYear)
heart_data$CovidPos <- convert_covidpos_to_integer(heart_data$CovidPos)

print("heart data prep done")
write.csv(heart_data, "/home/alex/UniProjects/BachelorXAI/datasets/dataset_2020_2022/2022/heart_2022_no_nans_numerical.csv", row.names = TRUE)

# model_svm <- svm(HeartDisease ~ ., data = heart_data, probability = TRUE)
# print(names(heart_data))
# heart_data_wo_target <- heart_data[, -which(names(heart_data) == 'HeartDisease')]
#
# explainer_svm <- explain(model_svm,
#                          data = heart_data_wo_target,
#                          y = heart_data$HeartDisease,
#                          label = "SVM Model")
# saveRDS(explainer_svm, file = "explainer_svm_large.rds")

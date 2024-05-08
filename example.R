library("xai2shiny")
library("ranger")
library("DALEX")

# Creating ML models
model_rf <- ranger(survived ~ .,
                   data = titanic_imputed,
                   classification = TRUE,
                   probability = TRUE)
model_glm <- glm(survived ~ .,
                 data = titanic_imputed,
                 family = "binomial")

# Creating DALEX explainers
explainer_rf <- explain(model_rf,
                     data = titanic_imputed[,-8],
                     y = titanic_imputed$survived)

explainer_glm <- explain(model_glm,
                     data = titanic_imputed[,-8],
                     y = titanic_imputed$survived)

xai2shiny::xai2shiny(explainer_glm, explainer_rf,
                     directory = './',
                     selected_variables = c('gender', 'age'),
                     run = FALSE)
library(plumber)


pr("routes.R") %>%
  pr_run(port=8000)
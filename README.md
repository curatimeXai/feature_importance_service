# Bogalusa: Feature Importance Service

Owner: Sterian-Alexandru Cristea

This service is a dashboard for exploring ai models for heart disease prediction. This service focuses especially on the
features of the predictive model and understanding why and how the model predicted something.

## Project Setup

1. Copy .env.example to .env with ```cp .env.example .env```
2. Change the paths if needed
3. Do pip install -r requirements.txt
4. Go to flask_app and do ```unzip datasets_and_store.zip```
5. ```docker-compose up```

## Scripts

Prepare the dataset by going to ./flask_app/src/scripts and running ```python prepare_2020_dataset.py```

Train the models by going to ./flask_app/src/trainers and running ```python xdg_trainer.py ``` or any  other model trainer.
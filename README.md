# Bogalusa: Feature Importance Service

Owner: Sterian-Alexandru Cristea

This service is a dashboard for exploring ai models for heart disease prediction. This service focuses especially on the
features of the predictive model and understanding why and how the model predicted something.

## Project Setup

1. Copy .env.example to .env with ```cp .env.example .env```
2. Change the paths if needed
3. Do pip install -r requirements.txt
4. Download the dataset from https://www.kaggle.com/datasets/kamilpytlak/personal-key-indicators-of-heart-disease. into ./flask_app/datasets/
5. Prepare the dataset by going to ./flask_app/src/scripts and running ```python prepare_2020_dataset.py```
6. Train the models by going to ./flask_app/src/trainers and running ```python xdg_trainer.py ``` or any  other model trainer.
7. Install npm by going to ./flask_app/frontend adn running ```npm install```
8. Then run ```npm run build``` or if you are developing ```npm run watch```
9. Go back to ./flask_app and run ```python app.py```

## Docker Compose Option 
Simply run ```docker-compose up``` if you have docker-compose installed.

! The dataset and models steps still need to be done !
import pandas as pd
from dotenv import load_dotenv
from src.services.dataset_service import DatasetService
load_dotenv()

if __name__ == '__main__':
    dataset_service = DatasetService()
    kaggle_2020_ds = pd.read_csv(dataset_service.datasets_paths['unprocessed_kaggle_2020'])
    for col, col_settings in dataset_service.kaggle_heart_disease_2020_columns.items():
        if col_settings['type'] in ['category','boolean']:
            #Make categorical/boolean columns to numerical ones
            kaggle_2020_ds[col]=kaggle_2020_ds[col].apply(lambda x: col_settings['values'].get(x,0))
        if col_settings.get('invertValue', False):
            #Invert Bad Physical/Mental Health Days to Good Physical/Mental Health Days
            kaggle_2020_ds[col] = kaggle_2020_ds[col].apply(lambda x: abs(x - col_settings['values'][1]))

    kaggle_2020_ds = kaggle_2020_ds.drop(
        columns=['Race'])
    kaggle_2020_ds.to_csv(dataset_service.datasets_paths['processed_kaggle_2020'])

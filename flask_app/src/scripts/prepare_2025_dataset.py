import pandas as pd
from dotenv import load_dotenv
from src.services.dataset_service import DatasetService
load_dotenv()

if __name__ == '__main__':
    dataset_service = DatasetService()
    ds_2025 = pd.read_csv(
        dataset_service.datasets_paths['unprocessed_2025'])
    for col, col_settings in (dataset_service
            .kaggle_heart_disease_2025_columns.items()):
        if col_settings['type'] in ['category','boolean']:
            #Make categorical/boolean columns to numerical ones
            ds_2025[col]=(ds_2025[col]
                .apply(lambda x: col_settings['values'].get(x,0)))

    ds_2025.to_csv(
        dataset_service.datasets_paths['processed_kaggle_2020'])

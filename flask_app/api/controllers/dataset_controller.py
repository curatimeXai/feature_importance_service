from flask_app.src.dataset_service import DatasetService

def get_2020_dataset_columns():
    dataset_service=DatasetService()
    return dataset_service.columns_2020

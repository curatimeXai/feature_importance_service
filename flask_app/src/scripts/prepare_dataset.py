import pandas as pd

from src.services.dataset_service import DatasetService

if __name__ == '__main__':
    dataset_service = DatasetService()
    kaggle_2020_ds = pd.read_csv(dataset_service.datasets_paths[1])
    for col, col_settings in dataset_service.kaggle_heart_disease_2020_columns.items():
        if col_settings.get('invertValue', False):
            kaggle_2020_ds[col] = kaggle_2020_ds[col].apply(lambda x: abs(x - col_settings['values'][1]))

    kaggle_2020_ds = kaggle_2020_ds.drop(
        columns=[kaggle_2020_ds.columns[0]])

    kaggle_2020_ds.to_csv(
        '/home/alex/UniProjects/BachelorXAI/datasets/dataset_2020_2022/2020/heart_2020_cleaned_numerical.csv')

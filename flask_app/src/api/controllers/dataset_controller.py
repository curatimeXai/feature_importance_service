import math

from plotly import express
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.services.dataset_plot_service import DatasetPlotService
from src.services.dataset_service import DatasetService


def get_2020_dataset_columns():
    dataset_service = DatasetService()
    return dataset_service.convert_int64_to_int(dataset_service.kaggle_heart_disease_2020_columns)


def get_all_boxplots(dataset):
    dataset_service = DatasetService()
    dataset_plot_service = DatasetPlotService(dataset_service.kaggle_heart_disease_2020)
    numerical_columns = dataset_service.get_numerical_columns(dataset + '_columns')
    # plots = []
    fig = dataset_plot_service.box_plots(dataset_service.kaggle_heart_disease_2020, numerical_columns, col_count=4,title='Dataset Numerical Data')
    return fig.to_json()


def get_all_piecharts(dataset):
    dataset_service = DatasetService()
    dataset_plot_service = DatasetPlotService(dataset_service.kaggle_heart_disease_2020)
    boolean_columns = dataset_service.get_boolean_columns(dataset + '_columns')
    # plots = []
    fig = dataset_plot_service.pie_charts(dataset_service.kaggle_heart_disease_2020, boolean_columns, col_count=4,
                                         title='Dataset Boolean Data',map={0: 'No', 1: 'Yes'})
    return fig.to_json()

def get_all_barcharts(dataset):
    dataset_service = DatasetService()
    dataset_plot_service = DatasetPlotService(dataset_service.kaggle_heart_disease_2020)
    categorical_columns = dataset_service.get_categorical_columns(dataset + '_columns')
    # plots = []
    fig = dataset_plot_service.bar_charts(dataset_service.kaggle_heart_disease_2020, categorical_columns, col_count=4,
                                         title='Dataset Categorical Data')
    return fig.to_json()

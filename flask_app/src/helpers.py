import os


def get_datasets_path(path):
    return os.getenv('DATASETS_PATH') + '/' + path


def get_trained_models_path(path):
    return os.getenv('TRAINED_MODELS_PATH') + '/' + path


def get_explainers_path(path):
    return os.getenv('EXPLAINERS_PATH') + '/' + path

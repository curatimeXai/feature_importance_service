import json

from flask import Blueprint, render_template

from src.api.controllers.dataset_controller import get_2020_dataset_columns

base_blueprint = Blueprint('base', __name__)


@base_blueprint.route('/', methods=['GET'])
def get_dashboard():
    columns = get_2020_dataset_columns()
    return render_template('index.html', columns=json.dumps(columns))

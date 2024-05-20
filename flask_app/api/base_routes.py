from flask import Blueprint, render_template

from flask_app.api.controllers.dataset_controller import get_2020_dataset_columns

base_blueprint = Blueprint('base', __name__)


@base_blueprint.route('/', methods=['GET'])
def get_dashboard():
    columns = get_2020_dataset_columns()
    return render_template('temporary_dashboard.html', columns=columns)

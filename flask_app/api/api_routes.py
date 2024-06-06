from flask import Blueprint, jsonify

from api.controllers import dataset_controller

api_blueprint = Blueprint('api', __name__,url_prefix='api')


@api_blueprint.route('/columns/<dataset>', methods=['GET'])
def get_dataset_columns(dataset):
    return jsonify(dataset_controller.get_dataset_columns(dataset))


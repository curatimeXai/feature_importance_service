from flask import Blueprint, jsonify, render_template, request

from src.api.controllers.rand_forest_controller import rand_forest_accuracy, rand_forest_variable_importance_image, rand_forest_variable_importance, \
    rand_forest_break_down, rand_forest_shapley, rand_forest_ceteris_parabus, rand_forest_model_performance, rand_forest_pdp, rand_forest_overview
from src.services.dataset_service import DatasetService

rand_forest_blueprint = Blueprint('rand_forest', __name__, url_prefix='/rand_forest')


@rand_forest_blueprint.route('/accuracy', methods=['GET'])
def get_accuracies():
    result = rand_forest_accuracy()
    return jsonify(result)

@rand_forest_blueprint.route('/vipimage', methods=['GET'])
def get_vip_image():
    result = rand_forest_variable_importance_image()
    return jsonify({'vip': result})

@rand_forest_blueprint.route('/vip', methods=['GET'])
def get_vip():
    result = rand_forest_variable_importance()
    return result

@rand_forest_blueprint.route('/breakdown', methods=['GET'])
def get_breakdown():
    input_parameters = request.args.to_dict()
    dataset_service = DatasetService()
    input_parameters['BMI'] = str(
        dataset_service.calculateBMI(input_parameters.get('weight'), input_parameters.get('height')))
    del input_parameters['weight']
    del input_parameters['height']
    result = rand_forest_break_down(input_parameters)
    return result
@rand_forest_blueprint.route('/shapley', methods=['GET'])
def get_shapley():
    input_parameters = request.args.to_dict()
    dataset_service = DatasetService()
    input_parameters['BMI'] = str(
        dataset_service.calculateBMI(input_parameters.get('weight'), input_parameters.get('height')))
    del input_parameters['weight']
    del input_parameters['height']
    result = rand_forest_shapley(input_parameters)
    return result

@rand_forest_blueprint.route('/overview', methods=['GET'])
def get_overview():
    input_parameters = request.args.to_dict()
    dataset_service = DatasetService()
    input_parameters['BMI']=str(dataset_service.calculateBMI(input_parameters.get('weight'),input_parameters.get('height')))
    del input_parameters['weight']
    del input_parameters['height']
    result = rand_forest_overview(input_parameters)
    return result

@rand_forest_blueprint.route('/ceterisparabus/<variable>/', methods=['GET'])
def get_ceterisparabus(variable):
    input_parameters = request.args.to_dict()
    dataset_service = DatasetService()
    input_parameters['BMI'] = str(
        dataset_service.calculateBMI(input_parameters.get('weight'), input_parameters.get('height')))
    del input_parameters['weight']
    del input_parameters['height']
    result = rand_forest_ceteris_parabus(input_parameters,variable)
    return result
@rand_forest_blueprint.route('/modelperformance', methods=['GET'])
def get_modelperformance():
    result = rand_forest_model_performance()
    return render_template('plotly_chart.html', chart=result)

@rand_forest_blueprint.route('/pdp/<variable>/', methods=['GET'])
def get_pdp(variable):
    result = rand_forest_pdp(variable)
    return result


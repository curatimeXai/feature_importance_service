from flask import Blueprint, jsonify, render_template, request

from src.api.controllers.xdg_controller import xdg_accuracy, xdg_variable_importance_image, xdg_variable_importance, \
    xdg_break_down, xdg_shapley, xdg_ceteris_parabus, xdg_model_performance, xdg_pdp, xdg_overview
from src.services.dataset_service import DatasetService

xdg_blueprint = Blueprint('xdg', __name__, url_prefix='/xdg')


@xdg_blueprint.route('/accuracy', methods=['GET'])
def get_accuracies():
    result = xdg_accuracy()
    return (jsonify({'accuracy': result}))

@xdg_blueprint.route('/vipimage', methods=['GET'])
def get_vip_image():
    result = xdg_variable_importance_image()
    return jsonify({'vip': result})

@xdg_blueprint.route('/vip', methods=['GET'])
def get_vip():
    result = xdg_variable_importance()
    return result

@xdg_blueprint.route('/breakdown', methods=['GET'])
def get_breakdown():
    input_parameters = request.args.to_dict()
    dataset_service = DatasetService()
    input_parameters['BMI'] = str(
        dataset_service.calculateBMI(input_parameters.get('weight'), input_parameters.get('height')))
    del input_parameters['weight']
    del input_parameters['height']
    result = xdg_break_down(input_parameters)
    return result
@xdg_blueprint.route('/shapley', methods=['GET'])
def get_shapley():
    input_parameters = request.args.to_dict()
    dataset_service = DatasetService()
    input_parameters['BMI'] = str(
        dataset_service.calculateBMI(input_parameters.get('weight'), input_parameters.get('height')))
    del input_parameters['weight']
    del input_parameters['height']
    result = xdg_shapley(input_parameters)
    return result

@xdg_blueprint.route('/overview', methods=['GET'])
def get_overview():
    input_parameters = request.args.to_dict()
    dataset_service = DatasetService()
    input_parameters['BMI']=str(dataset_service.calculateBMI(input_parameters.get('weight'),input_parameters.get('height')))
    del input_parameters['weight']
    del input_parameters['height']
    result = xdg_overview(input_parameters)
    return result

@xdg_blueprint.route('/ceterisparabus/<variable>/', methods=['GET'])
def get_ceterisparabus(variable):
    input_parameters = request.args.to_dict()
    result = xdg_ceteris_parabus(input_parameters,variable)
    return render_template('plotly_chart.html', chart=result)
@xdg_blueprint.route('/modelperformance', methods=['GET'])
def get_modelperformance():
    result = xdg_model_performance()
    return render_template('plotly_chart.html', chart=result)

@xdg_blueprint.route('/pdp/<variable>/', methods=['GET'])
def get_pdp(variable):
    result = xdg_pdp(variable)
    return result


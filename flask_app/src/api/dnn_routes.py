from flask import Blueprint, jsonify, render_template, request

from src.api.controllers.dnn_controller import dnn_accuracy, dnn_variable_importance_image, dnn_variable_importance, \
    dnn_break_down, dnn_shapley, dnn_ceteris_parabus, dnn_model_performance, dnn_pdp, dnn_overview
from src.services.dataset_service import DatasetService

dnn_blueprint = Blueprint('dnn', __name__, url_prefix='/dnn')


@dnn_blueprint.route('/accuracy', methods=['GET'])
def get_accuracies():
    result = dnn_accuracy()
    return (jsonify({'accuracy': result}))

@dnn_blueprint.route('/vipimage', methods=['GET'])
def get_vip_image():
    result = dnn_variable_importance_image()
    return jsonify({'vip': result})

@dnn_blueprint.route('/vip', methods=['GET'])
def get_vip():
    result = dnn_variable_importance()
    return result

@dnn_blueprint.route('/breakdown', methods=['GET'])
def get_breakdown():
    input_parameters = request.args.to_dict()
    dataset_service = DatasetService()
    input_parameters['BMI'] = str(
        dataset_service.calculateBMI(input_parameters.get('weight'), input_parameters.get('height')))
    del input_parameters['weight']
    del input_parameters['height']
    result = dnn_break_down(input_parameters)
    return result
@dnn_blueprint.route('/shapley', methods=['GET'])
def get_shapley():
    input_parameters = request.args.to_dict()
    dataset_service = DatasetService()
    input_parameters['BMI'] = str(
        dataset_service.calculateBMI(input_parameters.get('weight'), input_parameters.get('height')))
    del input_parameters['weight']
    del input_parameters['height']
    result = dnn_shapley(input_parameters)
    return result

@dnn_blueprint.route('/overview', methods=['GET'])
def get_overview():
    input_parameters = request.args.to_dict()
    dataset_service = DatasetService()
    input_parameters['BMI']=str(dataset_service.calculateBMI(input_parameters.get('weight'),input_parameters.get('height')))
    del input_parameters['weight']
    del input_parameters['height']
    result = dnn_overview(input_parameters)
    return result

@dnn_blueprint.route('/ceterisparabus/<variable>/', methods=['GET'])
def get_ceterisparabus(variable):
    input_parameters = request.args.to_dict()
    result = dnn_ceteris_parabus(input_parameters,variable)
    return render_template('plotly_chart.html', chart=result)
@dnn_blueprint.route('/modelperformance', methods=['GET'])
def get_modelperformance():
    result = dnn_model_performance()
    return render_template('plotly_chart.html', chart=result)

@dnn_blueprint.route('/pdp/<variable>/', methods=['GET'])
def get_pdp(variable):
    result = dnn_pdp(variable)
    return result


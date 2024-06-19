from flask import Blueprint, jsonify, render_template, request

from src.api.controllers.svm_controller import svm_accuracy, svm_variable_importance_image, svm_variable_importance, \
    svm_break_down, svm_shapley, svm_ceteris_parabus, svm_model_performance, svm_pdp, svm_overview
from src.services.dataset_service import DatasetService

svm_blueprint = Blueprint('svm', __name__, url_prefix='/svm')


@svm_blueprint.route('/accuracy', methods=['GET'])
def get_accuracies():
    result = svm_accuracy()
    return (jsonify({'accuracy': result}))

@svm_blueprint.route('/vipimage', methods=['GET'])
def get_vip_image():
    result = svm_variable_importance_image()
    return jsonify({'vip': result})

@svm_blueprint.route('/vip', methods=['GET'])
def get_vip():
    result = svm_variable_importance()
    return result

@svm_blueprint.route('/breakdown', methods=['GET'])
def get_breakdown():
    input_parameters = request.args.to_dict()
    dataset_service = DatasetService()
    input_parameters['BMI'] = str(
        dataset_service.calculateBMI(input_parameters.get('weight'), input_parameters.get('height')))
    del input_parameters['weight']
    del input_parameters['height']
    result = svm_break_down(input_parameters)
    return result
@svm_blueprint.route('/shapley', methods=['GET'])
def get_shapley():
    input_parameters = request.args.to_dict()
    dataset_service = DatasetService()
    input_parameters['BMI'] = str(
        dataset_service.calculateBMI(input_parameters.get('weight'), input_parameters.get('height')))
    del input_parameters['weight']
    del input_parameters['height']
    result = svm_shapley(input_parameters)
    return result

@svm_blueprint.route('/overview', methods=['GET'])
def get_overview():
    input_parameters = request.args.to_dict()
    dataset_service = DatasetService()
    input_parameters['BMI']=str(dataset_service.calculateBMI(input_parameters.get('weight'),input_parameters.get('height')))
    del input_parameters['weight']
    del input_parameters['height']
    result = svm_overview(input_parameters)
    return result

@svm_blueprint.route('/ceterisparabus/<variable>/', methods=['GET'])
def get_ceterisparabus(variable):
    input_parameters = request.args.to_dict()
    result = svm_ceteris_parabus(input_parameters,variable)
    return render_template('plotly_chart.html', chart=result)
@svm_blueprint.route('/modelperformance', methods=['GET'])
def get_modelperformance():
    result = svm_model_performance()
    return render_template('plotly_chart.html', chart=result)

@svm_blueprint.route('/pdp/<variable>/', methods=['GET'])
def get_pdp(variable):
    result = svm_pdp(variable)
    return result


from flask import Blueprint, jsonify, render_template, request

from src.api.controllers.xgb_controller import xgb_accuracy, xgb_variable_importance_image, xgb_variable_importance, \
    xgb_break_down, xgb_shapley, xgb_ceteris_parabus, xgb_model_performance, xgb_pdp, xgb_overview
from src.services.dataset_service import DatasetService

xgb_blueprint = Blueprint('xgb', __name__, url_prefix='/xgb')


@xgb_blueprint.route('/accuracy', methods=['GET'])
def get_accuracies():
    result = xgb_accuracy()
    return (jsonify({'accuracy': result}))

@xgb_blueprint.route('/vipimage', methods=['GET'])
def get_vip_image():
    result = xgb_variable_importance_image()
    return jsonify({'vip': result})

@xgb_blueprint.route('/vip', methods=['GET'])
def get_vip():
    result = xgb_variable_importance()
    return result

@xgb_blueprint.route('/breakdown', methods=['GET'])
def get_breakdown():
    input_parameters = request.args.to_dict()
    dataset_service = DatasetService()
    input_parameters['BMI'] = str(
        dataset_service.calculateBMI(input_parameters.get('weight'), input_parameters.get('height')))
    del input_parameters['weight']
    del input_parameters['height']
    result = xgb_break_down(input_parameters)
    return result
@xgb_blueprint.route('/shapley', methods=['GET'])
def get_shapley():
    input_parameters = request.args.to_dict()
    dataset_service = DatasetService()
    input_parameters['BMI'] = str(
        dataset_service.calculateBMI(input_parameters.get('weight'), input_parameters.get('height')))
    del input_parameters['weight']
    del input_parameters['height']
    result = xgb_shapley(input_parameters)
    return result

@xgb_blueprint.route('/overview', methods=['GET'])
def get_overview():
    input_parameters = request.args.to_dict()
    dataset_service = DatasetService()
    input_parameters['BMI']=str(dataset_service.calculateBMI(input_parameters.get('weight'),input_parameters.get('height')))
    del input_parameters['weight']
    del input_parameters['height']
    result = xgb_overview(input_parameters)
    return result

@xgb_blueprint.route('/ceterisparabus/<variable>/', methods=['GET'])
def get_ceterisparabus(variable):
    input_parameters = request.args.to_dict()
    result = xgb_ceteris_parabus(input_parameters,variable)
    return render_template('plotly_chart.html', chart=result)
@xgb_blueprint.route('/modelperformance', methods=['GET'])
def get_modelperformance():
    result = xgb_model_performance()
    return render_template('plotly_chart.html', chart=result)

@xgb_blueprint.route('/pdp/<variable>/', methods=['GET'])
def get_pdp(variable):
    result = xgb_pdp(variable)
    return result

